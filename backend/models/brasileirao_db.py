#!/usr/bin/env python3
"""
Sistema de Banco de Dados para Brasileirão
Camada de persistência para dados da classificação
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class BrasileiraoDB:
    """
    Gerenciador de banco de dados para classificação do Brasileirão
    """
    
    def __init__(self, db_path: str = "data/brasileirao.db"):
        self.db_path = db_path
        self.ensure_data_dir()
        self.create_tables()
    
    def ensure_data_dir(self):
        """Garante que o diretório data/ existe"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def get_connection(self):
        """Retorna conexão com o banco"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Cria tabelas necessárias"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS classificacao_serie_a (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    posicao INTEGER NOT NULL,
                    time TEXT NOT NULL,
                    pontos INTEGER NOT NULL,
                    jogos INTEGER NOT NULL,
                    vitorias INTEGER NOT NULL,
                    empates INTEGER NOT NULL,
                    derrotas INTEGER NOT NULL,
                    gols_pro INTEGER NOT NULL,
                    gols_contra INTEGER NOT NULL,
                    saldo_gols INTEGER NOT NULL,
                    aproveitamento REAL NOT NULL,
                    ultimos_jogos TEXT NOT NULL,
                    zona TEXT,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    rodada INTEGER,
                    fonte TEXT DEFAULT 'manual'
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_classificacao_data 
                ON classificacao_serie_a (data_atualizacao DESC)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_classificacao_time 
                ON classificacao_serie_a (time, data_atualizacao DESC)
            """)
    
    def save_classification(self, dados: List[Dict], fonte: str = "api", rodada: int = None):
        """
        Salva classificação completa no banco
        
        Args:
            dados: Lista com dados de cada time
            fonte: Origem dos dados (api, manual, scraping)
            rodada: Número da rodada (opcional)
        """
        with self.get_connection() as conn:
            # Limpar dados antigos da mesma rodada/data
            if rodada:
                conn.execute(
                    "DELETE FROM classificacao_serie_a WHERE rodada = ?", 
                    (rodada,)
                )
            
            # Inserir novos dados
            for time_data in dados:
                conn.execute("""
                    INSERT INTO classificacao_serie_a (
                        posicao, time, pontos, jogos, vitorias, empates, derrotas,
                        gols_pro, gols_contra, saldo_gols, aproveitamento, 
                        ultimos_jogos, zona, rodada, fonte
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    time_data.get('pos'),
                    time_data.get('time'),
                    time_data.get('p'),
                    time_data.get('j'),
                    time_data.get('v'),
                    time_data.get('e'),
                    time_data.get('d'),
                    time_data.get('gp'),
                    time_data.get('gc'),
                    time_data.get('sg'),
                    time_data.get('aproveitamento'),
                    time_data.get('ultimos'),
                    time_data.get('zona', ''),
                    rodada,
                    fonte
                ))
    
    def get_latest_classification(self) -> Optional[List[Dict]]:
        """
        Busca a classificação mais recente
        
        Returns:
            Lista com dados dos times ou None se não houver dados
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM classificacao_serie_a 
                WHERE data_atualizacao = (
                    SELECT MAX(data_atualizacao) FROM classificacao_serie_a
                )
                ORDER BY posicao
            """)
            
            rows = cursor.fetchall()
            if not rows:
                return None
            
            # Converter para formato esperado pelo frontend
            columns = [desc[0] for desc in cursor.description]
            result = []
            
            for row in rows:
                data = dict(zip(columns, row))
                result.append({
                    'pos': data['posicao'],
                    'time': data['time'],
                    'p': data['pontos'],
                    'j': data['jogos'],
                    'v': data['vitorias'],
                    'e': data['empates'],
                    'd': data['derrotas'],
                    'gp': data['gols_pro'],
                    'gc': data['gols_contra'],
                    'sg': data['saldo_gols'],
                    'aproveitamento': data['aproveitamento'],
                    'ultimos': data['ultimos_jogos'],
                    'zona': data['zona'] or '',
                    'data_atualizacao': data['data_atualizacao'],
                    'fonte': data['fonte']
                })
            
            return result
    
    def is_data_fresh(self, max_age_hours: int = 4) -> bool:
        """
        Verifica se os dados ainda estão frescos
        
        Args:
            max_age_hours: Idade máxima em horas
            
        Returns:
            True se dados estão frescos, False caso contrário
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT MAX(data_atualizacao) FROM classificacao_serie_a
            """)
            
            result = cursor.fetchone()[0]
            if not result:
                return False
            
            # Converter string para datetime
            last_update = datetime.fromisoformat(result)
            age = datetime.now() - last_update
            
            return age < timedelta(hours=max_age_hours)
    
    def get_data_age(self) -> Optional[str]:
        """
        Retorna a idade dos dados em formato legível
        
        Returns:
            String descrevendo a idade dos dados
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT MAX(data_atualizacao) FROM classificacao_serie_a
            """)
            
            result = cursor.fetchone()[0]
            if not result:
                return None
            
            last_update = datetime.fromisoformat(result)
            age = datetime.now() - last_update
            
            if age.days > 0:
                return f"{age.days} dias atrás"
            elif age.seconds > 3600:
                hours = age.seconds // 3600
                return f"{hours} horas atrás"
            else:
                minutes = age.seconds // 60
                return f"{minutes} minutos atrás"
    
    def get_team_history(self, team_name: str, limit: int = 10) -> List[Dict]:
        """
        Busca histórico de posições de um time
        
        Args:
            team_name: Nome do time
            limit: Limite de registros
            
        Returns:
            Lista com histórico do time
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT posicao, pontos, data_atualizacao, rodada
                FROM classificacao_serie_a 
                WHERE time = ?
                ORDER BY data_atualizacao DESC
                LIMIT ?
            """, (team_name, limit))
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def cleanup_old_data(self, keep_days: int = 30):
        """
        Remove dados antigos para economizar espaço
        
        Args:
            keep_days: Número de dias para manter
        """
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        with self.get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM classificacao_serie_a 
                WHERE data_atualizacao < ?
            """, (cutoff_date.isoformat(),))
            
            print(f"🗑️ Removidos {cursor.rowcount} registros antigos")

# Instância global para uso na aplicação
brasileirao_db = BrasileiraoDB()

if __name__ == "__main__":
    # Teste básico
    db = BrasileiraoDB("test_brasileirao.db")
    
    # Dados de teste
    test_data = [
        {"pos": 1, "time": "Flamengo", "p": 51, "j": 23, "v": 15, "e": 6, "d": 2, 
         "gp": 48, "gc": 11, "sg": 37, "aproveitamento": 73, "ultimos": "VVEVE", "zona": "libertadores"}
    ]
    
    db.save_classification(test_data, fonte="teste")
    result = db.get_latest_classification()
    
    print("✅ Teste do banco:", result[0] if result else "Erro")
    print("📊 Idade dos dados:", db.get_data_age())
    print("🔄 Dados frescos:", db.is_data_fresh())
