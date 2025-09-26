#!/usr/bin/env python3
"""
Gerenciador do banco tabelas_classificacao.db
Para a interface administrativa
"""

import sqlite3
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ClassificacaoDB:
    """
    Gerenciador do banco de dados de classificação
    """
    
    def __init__(self, db_path: str = "models/tabelas_classificacao.db"):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Garantir que o banco existe"""
        if not os.path.exists(self.db_path):
            logger.warning(f"Banco {self.db_path} não encontrado")
            return False
        return True
    
    def get_connection(self):
        """Obter conexão com o banco"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            return conn
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def get_classificacao_serie_a(self) -> List[Dict]:
        """Obter classificação da Série A"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        id, posicao, time, pontos, jogos, vitorias, empates, derrotas,
                        gols_pro, gols_contra, saldo_gols, aproveitamento,
                        data_atualizacao, rodada, fonte
                    FROM classificacao_serie_a 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação Série A: {e}")
            return []
    
    def get_classificacao_serie_b(self) -> List[Dict]:
        """Obter classificação da Série B (se existir tabela)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar se existe tabela da Série B
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='classificacao_serie_b'
                """)
                
                if not cursor.fetchone():
                    logger.info("Tabela classificacao_serie_b não existe")
                    return []
                
                cursor.execute("""
                    SELECT 
                        id, posicao, time, pontos, jogos, vitorias, empates, derrotas,
                        gols_pro, gols_contra, saldo_gols, aproveitamento,
                        ultimos_jogos, zona, created_at, updated_at
                    FROM classificacao_serie_b 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação Série B: {e}")
            return []
    
    def update_time_stats(self, time_id: int, campo: str, valor: str, serie: str = 'a') -> bool:
        """Atualizar estatística específica de um time"""
        logger.info(f"🔄 [DB] === INICIANDO UPDATE ===")
        logger.info(f"🔄 [DB] time_id={time_id}, campo={campo}, valor={valor}, serie={serie}")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Campos permitidos para atualização
                campos_permitidos = [
                    'time', 'pontos', 'jogos', 'vitorias', 'empates', 'derrotas',
                    'gols_pro', 'gols_contra', 'ultimos_jogos'
                ]
                
                if campo not in campos_permitidos:
                    logger.error(f"❌ [DB] Campo {campo} não permitido para atualização")
                    return False
                
                logger.info(f"✅ [DB] Campo {campo} é permitido")
                
                # Determinar tabela baseada na série
                tabela = 'classificacao_serie_a' if serie == 'a' else 'classificacao_serie_b'
                logger.info(f"🏆 [DB] Usando tabela: {tabela}")
                
                # Verificar se o ID existe
                cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE id = ?", (time_id,))
                count = cursor.fetchone()[0]
                logger.info(f"🔍 [DB] ID {time_id} existe: {count > 0}")
                
                if count == 0:
                    logger.error(f"❌ [DB] ID {time_id} não encontrado na tabela {tabela}")
                    return False
                
                # Para Série A, usar data_atualizacao; para Série B, usar updated_at
                if serie == 'a':
                    timestamp_field = 'data_atualizacao'
                else:
                    timestamp_field = 'updated_at'
                
                # Verificar se a coluna timestamp existe
                cursor.execute(f"PRAGMA table_info({tabela})")
                colunas = [col[1] for col in cursor.fetchall()]
                logger.info(f"📋 [DB] Colunas disponíveis: {colunas}")
                
                if timestamp_field not in colunas:
                    logger.warning(f"⚠️ [DB] Campo {timestamp_field} não existe, usando apenas atualização do campo")
                    # Atualizar só o campo
                    cursor.execute(f"UPDATE {tabela} SET {campo} = ? WHERE id = ?", (valor, time_id))
                else:
                    # Atualizar o campo com timestamp
                    cursor.execute(f"""
                        UPDATE {tabela} 
                        SET {campo} = ?, {timestamp_field} = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (valor, time_id))
                
                rows_affected = cursor.rowcount
                logger.info(f"📊 [DB] Linhas afetadas: {rows_affected}")
                
                # Recalcular saldo de gols e aproveitamento (só para campos numéricos de estatísticas)
                campos_numericos_stats = ['pontos', 'jogos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra']
                if campo in campos_numericos_stats:
                    logger.info(f"🧮 [DB] Recalculando estatísticas para campo numérico...")
                    cursor.execute(f"""
                        UPDATE {tabela} 
                        SET 
                            saldo_gols = gols_pro - gols_contra,
                            aproveitamento = CASE 
                                WHEN jogos > 0 THEN ROUND((pontos * 100.0) / (jogos * 3), 1)
                                ELSE 0 
                            END
                        WHERE id = ?
                    """, (time_id,))
                    logger.info(f"✅ [DB] Estatísticas recalculadas")
                
                conn.commit()
                logger.info(f"💾 [DB] Commit realizado. Sucesso: {rows_affected > 0}")
                return rows_affected > 0
                
        except Exception as e:
            logger.error(f"💥 [DB] Erro ao atualizar time {time_id}: {e}")
            import traceback
            logger.error(f"📄 [DB] Traceback: {traceback.format_exc()}")
            return False
    
    def get_tables_info(self) -> Dict:
        """Obter informações sobre as tabelas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Listar todas as tabelas
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name LIKE '%classificacao%'
                """)
                
                tabelas = [row[0] for row in cursor.fetchall()]
                
                info = {
                    'tabelas': tabelas,
                    'serie_a_count': 0,
                    'serie_b_count': 0
                }
                
                # Contar registros na Série A
                if 'classificacao_serie_a' in tabelas:
                    cursor.execute("SELECT COUNT(*) FROM classificacao_serie_a")
                    info['serie_a_count'] = cursor.fetchone()[0]
                
                # Contar registros na Série B
                if 'classificacao_serie_b' in tabelas:
                    cursor.execute("SELECT COUNT(*) FROM classificacao_serie_b")
                    info['serie_b_count'] = cursor.fetchone()[0]
                
                return info
                
        except Exception as e:
            logger.error(f"Erro ao obter info das tabelas: {e}")
            return {'tabelas': [], 'serie_a_count': 0, 'serie_b_count': 0}

# Instância global
classificacao_db = ClassificacaoDB()
