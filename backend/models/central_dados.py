#!/usr/bin/env python3
"""
CENTRAL DE DADOS - SISTEMA DE BACKUP E CONTROLE MANUAL
Estrutura hierárquica para gestão completa de clubes e campeonatos
"""

import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

logger = logging.getLogger(__name__)

class CentralDados:
    """
    Classe principal para gerenciamento da central de dados
    Sistema de backup inteligente para o Loteca X-Ray
    """
    
    def __init__(self, db_path: str = "central_dados.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self.init_database()
        logger.info(f"✅ Central de Dados inicializada: {self.db_path}")
    
    def get_connection(self):
        """Obter conexão com o banco"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Criar estrutura completa do banco de dados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. PAÍSES
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100) NOT NULL UNIQUE,
                    codigo_iso VARCHAR(3) NOT NULL UNIQUE,
                    continente VARCHAR(50),
                    ativo BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 2. CAMPEONATOS
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campeonatos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(150) NOT NULL,
                    pais_id INTEGER NOT NULL,
                    nivel INTEGER DEFAULT 1,  -- 1=Elite, 2=Segunda, 3=Terceira...
                    temporada INTEGER NOT NULL,
                    inicio_temporada DATE,
                    fim_temporada DATE,
                    ativo BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pais_id) REFERENCES paises(id),
                    UNIQUE(nome, temporada)
                )
            """)
            
            # 3. CLUBES (entidade central)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clubes (
                    id INTEGER PRIMARY KEY,  -- Usar ID do Cartola FC
                    nome VARCHAR(100) NOT NULL,
                    nome_completo VARCHAR(150),
                    abreviacao VARCHAR(10),
                    apelido VARCHAR(100),
                    cidade VARCHAR(100),
                    estado VARCHAR(50),
                    pais_id INTEGER DEFAULT 1,  -- Brasil por padrão
                    fundacao INTEGER,
                    estadio VARCHAR(150),
                    capacidade_estadio INTEGER,
                    site_oficial TEXT,
                    escudo_url TEXT,
                    escudo_30x30 TEXT,
                    escudo_45x45 TEXT,
                    escudo_60x60 TEXT,
                    escudo_local TEXT,  -- Para escudos salvos localmente
                    cores_principais VARCHAR(50),
                    cor_primaria VARCHAR(7),  -- Hex color
                    cor_secundaria VARCHAR(7),  -- Hex color
                    ativo BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pais_id) REFERENCES paises(id)
                )
            """)
            
            # 4. PARTICIPAÇÕES EM CAMPEONATOS
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clube_campeonatos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clube_id INTEGER NOT NULL,
                    campeonato_id INTEGER NOT NULL,
                    temporada INTEGER NOT NULL,
                    posicao_atual INTEGER,
                    posicao_final INTEGER,
                    pontos INTEGER DEFAULT 0,
                    jogos INTEGER DEFAULT 0,
                    vitorias INTEGER DEFAULT 0,
                    empates INTEGER DEFAULT 0,
                    derrotas INTEGER DEFAULT 0,
                    gols_pro INTEGER DEFAULT 0,
                    gols_contra INTEGER DEFAULT 0,
                    saldo_gols INTEGER DEFAULT 0,
                    aproveitamento DECIMAL(5,2) DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (clube_id) REFERENCES clubes(id),
                    FOREIGN KEY (campeonato_id) REFERENCES campeonatos(id),
                    UNIQUE(clube_id, campeonato_id, temporada)
                )
            """)
            
            # 5. ESTATÍSTICAS ATUAIS (dados do Cartola)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clube_stats_atuais (
                    clube_id INTEGER PRIMARY KEY,
                    total_atletas INTEGER DEFAULT 0,
                    pct_provaveis DECIMAL(5,2) DEFAULT 0,
                    media_pontos_elenco DECIMAL(5,2) DEFAULT 0,
                    preco_medio DECIMAL(8,2) DEFAULT 0,
                    rating DECIMAL(3,2) DEFAULT 0,
                    valor_total_elenco DECIMAL(12,2) DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'Sem dados',
                    fonte VARCHAR(50) DEFAULT 'MANUAL',  -- CARTOLA, MANUAL, API_FOOTBALL
                    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME,  -- Para cache inteligente
                    FOREIGN KEY (clube_id) REFERENCES clubes(id)
                )
            """)
            
            # 6. HISTÓRICO TEMPORAL (evolução)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clube_stats_historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clube_id INTEGER NOT NULL,
                    data DATE NOT NULL,
                    total_atletas INTEGER,
                    pct_provaveis DECIMAL(5,2),
                    media_pontos_elenco DECIMAL(5,2),
                    preco_medio DECIMAL(8,2),
                    rating DECIMAL(3,2),
                    valor_total_elenco DECIMAL(12,2),
                    fonte VARCHAR(50),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (clube_id) REFERENCES clubes(id),
                    UNIQUE(clube_id, data, fonte)
                )
            """)
            
            # 7. CONFIGURAÇÕES DO SISTEMA
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config_sistema (
                    chave VARCHAR(100) PRIMARY KEY,
                    valor TEXT,
                    descricao TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 8. LOG DE OPERAÇÕES
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operacoes_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operacao VARCHAR(50) NOT NULL,
                    tabela VARCHAR(50),
                    registro_id INTEGER,
                    dados_antes TEXT,
                    dados_depois TEXT,
                    usuario VARCHAR(100) DEFAULT 'SISTEMA',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # ÍNDICES PARA PERFORMANCE
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_clubes_ativo ON clubes(ativo)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_stats_data ON clube_stats_historico(data)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_campeonatos_temporada ON campeonatos(temporada)")
            
            conn.commit()
            logger.info("✅ Estrutura do banco criada com sucesso")
    
    def popular_dados_iniciais(self):
        """Popular dados básicos do sistema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # PAÍSES BÁSICOS
            paises_base = [
                (1, 'Brasil', 'BR', 'América do Sul'),
                (2, 'Argentina', 'AR', 'América do Sul'),
                (3, 'Espanha', 'ES', 'Europa'),
                (4, 'Inglaterra', 'GB', 'Europa'),
                (5, 'França', 'FR', 'Europa'),
                (6, 'Alemanha', 'DE', 'Europa'),
                (7, 'Itália', 'IT', 'Europa'),
            ]
            
            cursor.executemany("""
                INSERT OR IGNORE INTO paises (id, nome, codigo_iso, continente)
                VALUES (?, ?, ?, ?)
            """, paises_base)
            
            # CAMPEONATOS BÁSICOS - TEMPORADA 2025
            campeonatos_base = [
                ('Brasileirão Série A', 1, 1, 2025, '2025-04-01', '2025-12-15'),
                ('Brasileirão Série B', 1, 2, 2025, '2025-04-01', '2025-11-30'),
                ('Copa do Brasil', 1, 0, 2025, '2025-02-01', '2025-10-15'),
                ('Premier League', 4, 1, 2025, '2025-08-01', '2026-05-30'),
                ('La Liga', 3, 1, 2025, '2025-08-01', '2026-05-30'),
                ('Serie A', 7, 1, 2025, '2025-08-01', '2026-05-30'),
            ]
            
            cursor.executemany("""
                INSERT OR IGNORE INTO campeonatos 
                (nome, pais_id, nivel, temporada, inicio_temporada, fim_temporada)
                VALUES (?, ?, ?, ?, ?, ?)
            """, campeonatos_base)
            
            # CONFIGURAÇÕES INICIAIS
            config_inicial = [
                ('cache_ttl_minutes', '30', 'TTL do cache em minutos'),
                ('fonte_preferencial', 'CARTOLA', 'Fonte de dados preferencial'),
                ('modo_emergencia', 'false', 'Modo de emergência ativo'),
                ('ultima_sincronizacao', '', 'Última sincronização com APIs'),
            ]
            
            cursor.executemany("""
                INSERT OR IGNORE INTO config_sistema (chave, valor, descricao)
                VALUES (?, ?, ?)
            """, config_inicial)
            
            conn.commit()
            logger.info("✅ Dados iniciais populados")
    
    def salvar_clube(self, dados_clube: Dict[str, Any], fonte: str = 'MANUAL') -> int:
        """
        Salvar/atualizar dados de um clube
        
        Args:
            dados_clube: Dicionário com dados do clube
            fonte: Fonte dos dados (CARTOLA, MANUAL, API_FOOTBALL)
            
        Returns:
            ID do clube salvo
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Inserir/atualizar clube
            cursor.execute("""
                INSERT OR REPLACE INTO clubes 
                (id, nome, nome_completo, abreviacao, apelido, cidade, estado, 
                 escudo_url, escudo_30x30, escudo_45x45, escudo_60x60, escudo_local,
                 cor_primaria, cor_secundaria, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                dados_clube.get('id'),
                dados_clube.get('nome'),
                dados_clube.get('nome_completo'),
                dados_clube.get('abreviacao'),
                dados_clube.get('apelido'),
                dados_clube.get('cidade'),
                dados_clube.get('estado'),
                dados_clube.get('escudo_url'),
                dados_clube.get('escudo_30x30'),
                dados_clube.get('escudo_45x45'), 
                dados_clube.get('escudo_60x60'),
                dados_clube.get('escudo_local'),
                dados_clube.get('cor_primaria'),
                dados_clube.get('cor_secundaria')
            ))
            
            # Salvar estatísticas se fornecidas
            if 'stats' in dados_clube:
                stats = dados_clube['stats']
                cursor.execute("""
                    INSERT OR REPLACE INTO clube_stats_atuais
                    (clube_id, total_atletas, pct_provaveis, media_pontos_elenco,
                     preco_medio, rating, status, fonte, data_atualizacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    dados_clube.get('id'),
                    stats.get('total_atletas', 0),
                    stats.get('pct_provaveis', 0),
                    stats.get('media_pontos_elenco', 0),
                    stats.get('preco_medio', 0),
                    stats.get('rating', 0),
                    stats.get('status', 'Dados reais'),
                    fonte
                ))
            
            conn.commit()
            
            # Log da operação
            self._log_operacao('INSERT/UPDATE', 'clubes', dados_clube.get('id'), 
                             dados=dados_clube, usuario=fonte)
            
            return dados_clube.get('id')
    
    def obter_stats_clube(self, clube_id: int, fonte_preferencial: str = None) -> Dict[str, Any]:
        """
        Obter estatísticas de um clube com fallback inteligente
        
        Args:
            clube_id: ID do clube
            fonte_preferencial: Fonte preferencial (opcional)
            
        Returns:
            Dicionário com estatísticas do clube
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Prioridade: MANUAL > fonte_preferencial > qualquer
            query = """
                SELECT * FROM clube_stats_atuais 
                WHERE clube_id = ?
                ORDER BY 
                    CASE fonte 
                        WHEN 'MANUAL' THEN 1
                        WHEN ? THEN 2
                        ELSE 3
                    END,
                    data_atualizacao DESC
                LIMIT 1
            """
            
            cursor.execute(query, (clube_id, fonte_preferencial or 'CARTOLA'))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            
            return {}
    
    def sincronizar_com_cartola(self, dados_cartola: List[Dict]) -> int:
        """
        Sincronizar dados do Cartola FC com a central
        
        Args:
            dados_cartola: Lista de dados dos clubes do Cartola
            
        Returns:
            Número de clubes sincronizados
        """
        sincronizados = 0
        
        for clube_data in dados_cartola:
            try:
                self.salvar_clube(clube_data, fonte='CARTOLA')
                sincronizados += 1
            except Exception as e:
                logger.error(f"Erro ao sincronizar clube {clube_data.get('id')}: {e}")
        
        # Atualizar configuração
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO config_sistema (chave, valor, updated_at)
                VALUES ('ultima_sincronizacao', ?, CURRENT_TIMESTAMP)
            """, (datetime.now().isoformat(),))
            conn.commit()
        
        logger.info(f"✅ Sincronizados {sincronizados} clubes do Cartola FC")
        return sincronizados
    
    def _log_operacao(self, operacao: str, tabela: str, registro_id: int, 
                     dados: Dict = None, usuario: str = 'SISTEMA'):
        """Log de operações para auditoria"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO operacoes_log 
                (operacao, tabela, registro_id, dados_depois, usuario)
                VALUES (?, ?, ?, ?, ?)
            """, (operacao, tabela, registro_id, str(dados), usuario))
            conn.commit()
    
    def get_estatisticas_sistema(self) -> Dict[str, Any]:
        """Obter estatísticas gerais do sistema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Total de clubes
            cursor.execute("SELECT COUNT(*) FROM clubes WHERE ativo = 1")
            stats['total_clubes'] = cursor.fetchone()[0]
            
            # Clubes por fonte
            cursor.execute("""
                SELECT fonte, COUNT(*) FROM clube_stats_atuais 
                GROUP BY fonte
            """)
            stats['clubes_por_fonte'] = dict(cursor.fetchall())
            
            # Última sincronização
            cursor.execute("""
                SELECT valor FROM config_sistema 
                WHERE chave = 'ultima_sincronizacao'
            """)
            result = cursor.fetchone()
            stats['ultima_sincronizacao'] = result[0] if result else 'Nunca'
            
            # Dados mais antigos
            cursor.execute("""
                SELECT MIN(data_atualizacao) FROM clube_stats_atuais
            """)
            result = cursor.fetchone()
            stats['dados_mais_antigos'] = result[0] if result else None
            
            return stats


# Função de conveniência para inicialização
def inicializar_central_dados():
    """Inicializar a central de dados"""
    central = CentralDados()
    central.popular_dados_iniciais()
    return central


if __name__ == "__main__":
    # Teste da implementação
    print("🏗️ Criando estrutura da Central de Dados...")
    central = inicializar_central_dados()
    
    print("📊 Estatísticas do sistema:")
    stats = central.get_estatisticas_sistema()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("✅ Central de Dados criada com sucesso!")
