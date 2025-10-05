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
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Tentar diferentes caminhos possíveis
            possible_paths = [
                "models/tabelas_classificacao.db",
                "backend/models/tabelas_classificacao.db",
                "tabelas_classificacao.db"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.db_path = path
                    break
            else:
                # Se nenhum caminho funcionar, usar o padrão
                self.db_path = "models/tabelas_classificacao.db"
        else:
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
                        ultimos_confrontos, zona, data_atualizacao, rodada, fonte
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
                        ultimos_confrontos, zona, created_at, updated_at
                    FROM classificacao_serie_b 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação Série B: {e}")
            return []
    
    def get_classificacao_premier_league(self) -> List[Dict]:
        """Obter classificação da Premier League"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar se existe tabela da Premier League
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='classificacao_premier_league'
                """)
                
                if not cursor.fetchone():
                    logger.info("Tabela classificacao_premier_league não existe")
                    return []
                
                cursor.execute("""
                    SELECT 
                        id, posicao, clube, pts, pj, vit, e, der,
                        gm, gc, sg, ultimas_5, zona, badge,
                        created_at, updated_at
                    FROM classificacao_premier_league 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação Premier League: {e}")
            return []
    
    def get_classificacao_la_liga(self) -> List[Dict]:
        """Obter classificação da La Liga"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar se existe tabela da La Liga
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='classificacao_la_liga'
                """)
                
                if not cursor.fetchone():
                    logger.info("Tabela classificacao_la_liga não existe")
                    return []
                
                cursor.execute("""
                    SELECT 
                        id, posicao, clube, pts, pj, vit, e, der,
                        gm, gc, sg, ultimas_5, zona, badge,
                        created_at, updated_at
                    FROM classificacao_la_liga 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação La Liga: {e}")
            return []
    
    def get_classificacao_frances(self) -> List[Dict]:
        """Obter classificação da Ligue 1 (França)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar se existe tabela da Ligue 1
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='classificacao_frances'
                """)
                
                if not cursor.fetchone():
                    logger.info("Tabela classificacao_frances não existe")
                    return []
                
                cursor.execute("""
                    SELECT 
                        id, posicao, clube, pts, pj, vit, e, der,
                        gm, gc, sg, ultimas_5, zona, badge,
                        created_at, updated_at
                    FROM classificacao_frances 
                    ORDER BY posicao ASC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao obter classificação Ligue 1: {e}")
            return []
    
    def update_time_stats(self, time_id: int, campo: str, valor: str, serie: str = 'a') -> bool:
        """Atualizar estatística específica de um time"""
        logger.info(f"🔄 [DB] === INICIANDO UPDATE ===")
        logger.info(f"🔄 [DB] time_id={time_id}, campo={campo}, valor={valor}, serie={serie}")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Campos permitidos para atualização (incluindo Premier League)
                campos_permitidos_brasileirao = [
                    'time', 'pontos', 'jogos', 'vitorias', 'empates', 'derrotas',
                    'gols_pro', 'gols_contra', 'ultimos_confrontos'
                ]
                
                campos_permitidos_premier = [
                    'clube', 'pts', 'pj', 'vit', 'e', 'der',
                    'gm', 'gc', 'ultimas_5', 'zona', 'badge'
                ]
                
                # Determinar tabela e campos baseados na série
                if serie == 'premier':
                    tabela = 'classificacao_premier_league'
                    campos_permitidos = campos_permitidos_premier
                elif serie == 'laliga':
                    tabela = 'classificacao_la_liga'
                    campos_permitidos = campos_permitidos_premier  # La Liga usa mesmos campos que Premier
                elif serie == 'ligue1':
                    tabela = 'classificacao_frances'
                    campos_permitidos = campos_permitidos_premier  # Ligue 1 usa mesmos campos que Premier
                elif serie == 'b':
                    tabela = 'classificacao_serie_b'
                    campos_permitidos = campos_permitidos_brasileirao
                else:  # serie == 'a'
                    tabela = 'classificacao_serie_a'
                    campos_permitidos = campos_permitidos_brasileirao
                
                if campo not in campos_permitidos:
                    logger.error(f"❌ [DB] Campo {campo} não permitido para {tabela}")
                    return False
                
                logger.info(f"✅ [DB] Campo {campo} é permitido")
                logger.info(f"🏆 [DB] Usando tabela: {tabela}")
                
                # Verificar se o ID existe
                cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE id = ?", (time_id,))
                count = cursor.fetchone()[0]
                logger.info(f"🔍 [DB] ID {time_id} existe: {count > 0}")
                
                if count == 0:
                    logger.error(f"❌ [DB] ID {time_id} não encontrado na tabela {tabela}")
                    return False
                
                # Determinar campo de timestamp baseado na série
                if serie == 'a':
                    timestamp_field = 'data_atualizacao'
                elif serie in ['premier', 'laliga', 'ligue1']:
                    timestamp_field = 'updated_at'
                else:  # serie == 'b'
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
                
                # Recalcular estatísticas baseado na série
                if serie in ['premier', 'laliga', 'ligue1']:
                    # Para campeonatos internacionais: recalcular SG (saldo de gols)
                    campos_numericos_premier = ['pts', 'pj', 'vit', 'e', 'der', 'gm', 'gc']
                    if campo in campos_numericos_premier:
                        if serie == 'premier':
                            campeonato_nome = "Premier League"
                        elif serie == 'laliga':
                            campeonato_nome = "La Liga"
                        else:  # ligue1
                            campeonato_nome = "Ligue 1"
                        
                        logger.info(f"🧮 [DB] Recalculando estatísticas {campeonato_nome}...")
                        cursor.execute(f"""
                            UPDATE {tabela} 
                            SET sg = gm - gc
                            WHERE id = ?
                        """, (time_id,))
                        logger.info(f"✅ [DB] Saldo de gols recalculado")
                else:
                    # Para Brasileirão: recalcular saldo de gols e aproveitamento
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
                
                # Contar registros na Premier League
                if 'classificacao_premier_league' in tabelas:
                    cursor.execute("SELECT COUNT(*) FROM classificacao_premier_league")
                    info['premier_league_count'] = cursor.fetchone()[0]
                else:
                    info['premier_league_count'] = 0
                
                # Contar registros na La Liga
                if 'classificacao_la_liga' in tabelas:
                    cursor.execute("SELECT COUNT(*) FROM classificacao_la_liga")
                    info['la_liga_count'] = cursor.fetchone()[0]
                else:
                    info['la_liga_count'] = 0
                
                # Contar registros na Ligue 1
                if 'classificacao_frances' in tabelas:
                    cursor.execute("SELECT COUNT(*) FROM classificacao_frances")
                    info['ligue1_count'] = cursor.fetchone()[0]
                else:
                    info['ligue1_count'] = 0
                
                return info
                
        except Exception as e:
            logger.error(f"Erro ao obter info das tabelas: {e}")
            return {'tabelas': [], 'serie_a_count': 0, 'serie_b_count': 0, 'premier_league_count': 0, 'la_liga_count': 0, 'ligue1_count': 0}
    
    def get_last_update(self) -> str:
        """Obter a data/hora da última atualização em qualquer tabela"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Buscar a data mais recente entre todas as tabelas
                queries = [
                    "SELECT MAX(data_atualizacao) as ultima FROM classificacao_serie_a WHERE data_atualizacao IS NOT NULL",
                    "SELECT MAX(updated_at) as ultima FROM classificacao_serie_b WHERE updated_at IS NOT NULL",
                    "SELECT MAX(updated_at) as ultima FROM classificacao_premier_league WHERE updated_at IS NOT NULL",
                    "SELECT MAX(updated_at) as ultima FROM classificacao_la_liga WHERE updated_at IS NOT NULL",
                    "SELECT MAX(updated_at) as ultima FROM classificacao_frances WHERE updated_at IS NOT NULL"
                ]
                
                datas = []
                for query in queries:
                    try:
                        cursor.execute(query)
                        result = cursor.fetchone()
                        if result and result[0]:
                            datas.append(result[0])
                    except Exception:
                        continue  # Tabela pode não existir
                
                if datas:
                    # Retornar a data mais recente
                    return max(datas)
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Erro ao obter última atualização: {e}")
            return None

    def atualizar_ultimos_confrontos_serie_a(self, time_nome, ultimos_confrontos):
        """Atualizar últimos confrontos de um time da Série A"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Atualizar o time específico
                cursor.execute("""
                    UPDATE classificacao_serie_a 
                    SET ultimos_confrontos = ?, data_atualizacao = datetime('now')
                    WHERE time = ?
                """, (ultimos_confrontos, time_nome))
                
                if cursor.rowcount > 0:
                    logger.info(f"✅ [DB] Atualizado {time_nome}: {ultimos_confrontos}")
                    return True
                else:
                    logger.warning(f"⚠️ [DB] Time {time_nome} não encontrado na Série A")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ [DB] Erro ao atualizar {time_nome}: {e}")
            return False

    def atualizar_ultimos_confrontos_serie_b(self, time_nome, ultimos_confrontos):
        """Atualizar últimos confrontos de um time da Série B"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Atualizar o time específico
                cursor.execute("""
                    UPDATE classificacao_serie_b 
                    SET ultimos_confrontos = ?, updated_at = datetime('now')
                    WHERE time = ?
                """, (ultimos_confrontos, time_nome))
                
                if cursor.rowcount > 0:
                    logger.info(f"✅ [DB] Atualizado {time_nome}: {ultimos_confrontos}")
                    return True
                else:
                    logger.warning(f"⚠️ [DB] Time {time_nome} não encontrado na Série B")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ [DB] Erro ao atualizar {time_nome}: {e}")
            return False

# Instância global
classificacao_db = ClassificacaoDB()
