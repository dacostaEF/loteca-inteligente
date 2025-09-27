import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional

class JogosManager:
    """Gerenciador de jogos dos clubes"""
    
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), 'jogos')
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        """Garante que o diretório base existe"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def ensure_club_directory(self, clube: str):
        """Garante que o diretório do clube existe"""
        club_path = os.path.join(self.base_path, clube.lower())
        if not os.path.exists(club_path):
            os.makedirs(club_path)
        return club_path
    
    def get_jogos_file_path(self, clube: str) -> str:
        """Retorna o caminho do arquivo de jogos do clube"""
        club_path = self.ensure_club_directory(clube)
        return os.path.join(club_path, 'jogos.csv')
    
    def carregar_jogos(self, clube: str) -> List[Dict]:
        """Carrega os jogos de um clube do CSV"""
        try:
            jogos_file = self.get_jogos_file_path(clube)
            
            if not os.path.exists(jogos_file):
                return []
            
            jogos = []
            with open(jogos_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Converter tipos
                    row['gols_casa'] = int(row['gols_casa'])
                    row['gols_visitante'] = int(row['gols_visitante'])
                    row['pontos'] = int(row['pontos'])
                    jogos.append(row)
            
            return jogos
            
        except Exception as e:
            print(f"Erro ao carregar jogos de {clube}: {e}")
            return []
    
    def salvar_jogos(self, clube: str, jogos: List[Dict]) -> bool:
        """Salva os jogos de um clube no CSV"""
        try:
            jogos_file = self.get_jogos_file_path(clube)
            
            # Campos do CSV
            fieldnames = ['data', 'time_casa', 'gols_casa', 'gols_visitante', 
                         'time_visitante', 'local', 'resultado', 'pontos']
            
            with open(jogos_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(jogos)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar jogos de {clube}: {e}")
            return False
    
    def adicionar_jogo(self, clube: str, jogo: Dict) -> bool:
        """Adiciona um novo jogo ao clube"""
        try:
            jogos = self.carregar_jogos(clube)
            jogos.append(jogo)
            return self.salvar_jogos(clube, jogos)
        except Exception as e:
            print(f"Erro ao adicionar jogo para {clube}: {e}")
            return False
    
    def remover_jogo(self, clube: str, index: int) -> bool:
        """Remove um jogo pelo índice"""
        try:
            jogos = self.carregar_jogos(clube)
            if 0 <= index < len(jogos):
                jogos.pop(index)
                return self.salvar_jogos(clube, jogos)
            return False
        except Exception as e:
            print(f"Erro ao remover jogo de {clube}: {e}")
            return False
    
    def atualizar_jogo(self, clube: str, index: int, jogo_atualizado: Dict) -> bool:
        """Atualiza um jogo pelo índice"""
        try:
            jogos = self.carregar_jogos(clube)
            if 0 <= index < len(jogos):
                jogos[index] = jogo_atualizado
                return self.salvar_jogos(clube, jogos)
            return False
        except Exception as e:
            print(f"Erro ao atualizar jogo de {clube}: {e}")
            return False
    
    def calcular_estatisticas(self, clube: str) -> Dict:
        """Calcula estatísticas dos jogos do clube"""
        jogos = self.carregar_jogos(clube)
        
        if not jogos:
            return {
                'total_jogos': 0,
                'vitorias': 0,
                'empates': 0,
                'derrotas': 0,
                'pontos_total': 0,
                'ppg': 0.0,
                'gols_marcados': 0,
                'gols_sofridos': 0,
                'saldo_gols': 0
            }
        
        vitorias = len([j for j in jogos if j['resultado'] == 'Vitória'])
        empates = len([j for j in jogos if j['resultado'] == 'Empate'])
        derrotas = len([j for j in jogos if j['resultado'] == 'Derrota'])
        pontos_total = sum(j['pontos'] for j in jogos)
        
        # Calcular gols (considerando se o clube é mandante ou visitante)
        gols_marcados = 0
        gols_sofridos = 0
        
        for jogo in jogos:
            if jogo['time_casa'].lower() == clube.lower():
                # Clube jogando em casa
                gols_marcados += jogo['gols_casa']
                gols_sofridos += jogo['gols_visitante']
            else:
                # Clube jogando fora
                gols_marcados += jogo['gols_visitante']
                gols_sofridos += jogo['gols_casa']
        
        return {
            'total_jogos': len(jogos),
            'vitorias': vitorias,
            'empates': empates,
            'derrotas': derrotas,
            'pontos_total': pontos_total,
            'ppg': round(pontos_total / len(jogos), 2) if jogos else 0.0,
            'gols_marcados': gols_marcados,
            'gols_sofridos': gols_sofridos,
            'saldo_gols': gols_marcados - gols_sofridos
        }
    
    def listar_clubes_com_jogos(self) -> List[str]:
        """Lista todos os clubes que têm jogos salvos"""
        try:
            if not os.path.exists(self.base_path):
                return []
            
            clubes = []
            for item in os.listdir(self.base_path):
                club_path = os.path.join(self.base_path, item)
                if os.path.isdir(club_path):
                    jogos_file = os.path.join(club_path, 'jogos.csv')
                    if os.path.exists(jogos_file):
                        clubes.append(item)
            
            return clubes
            
        except Exception as e:
            print(f"Erro ao listar clubes: {e}")
            return []

# Instância global
jogos_manager = JogosManager()
