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
        """Calcula estatísticas completas dos jogos do clube"""
        jogos = self.carregar_jogos(clube)
        
        if not jogos:
            return {
                'total_jogos': 0,
                'vitorias': 0,
                'empates': 0,
                'derrotas': 0,
                'pontos_total': 0,
                'ppg': 0.0,
                'ppg_casa': 0.0,
                'ppg_fora': 0.0,
                'aproveitamento_casa': 0.0,
                'aproveitamento_fora': 0.0,
                'gols_marcados': 0,
                'gols_sofridos': 0,
                'saldo_gols': 0,
                'media_gols_marcados': 0.0,
                'media_gols_sofridos': 0.0,
                'clean_sheets': 0,
                'pct_vitorias': 0.0,
                'pct_clean_sheets': 0.0,
                'pontos_ultimos_5': 0,
                'sequencia_atual': '',
                'ultimos_5_resultados': ''
            }
        
        # Estatísticas básicas
        vitorias = len([j for j in jogos if j['resultado'] == 'Vitória'])
        empates = len([j for j in jogos if j['resultado'] == 'Empate'])
        derrotas = len([j for j in jogos if j['resultado'] == 'Derrota'])
        pontos_total = sum(j['pontos'] for j in jogos)
        
        # Separar jogos casa e fora
        jogos_casa = [j for j in jogos if j['time_casa'].lower() == clube.lower()]
        jogos_fora = [j for j in jogos if j['time_casa'].lower() != clube.lower()]
        
        # Calcular gols e clean sheets
        gols_marcados = 0
        gols_sofridos = 0
        clean_sheets = 0
        
        for jogo in jogos:
            if jogo['time_casa'].lower() == clube.lower():
                # Clube jogando em casa
                gols_marcados += jogo['gols_casa']
                gols_sofridos += jogo['gols_visitante']
                if jogo['gols_visitante'] == 0:
                    clean_sheets += 1
            else:
                # Clube jogando fora
                gols_marcados += jogo['gols_visitante']
                gols_sofridos += jogo['gols_casa']
                if jogo['gols_casa'] == 0:
                    clean_sheets += 1
        
        # PPG Casa e Fora
        pontos_casa = sum(j['pontos'] for j in jogos_casa)
        pontos_fora = sum(j['pontos'] for j in jogos_fora)
        ppg_casa = round(pontos_casa / len(jogos_casa), 2) if jogos_casa else 0.0
        ppg_fora = round(pontos_fora / len(jogos_fora), 2) if jogos_fora else 0.0
        
        # Aproveitamento (% de pontos possíveis)
        max_pontos_casa = len(jogos_casa) * 3
        max_pontos_fora = len(jogos_fora) * 3
        aproveitamento_casa = round((pontos_casa / max_pontos_casa) * 100, 1) if max_pontos_casa > 0 else 0.0
        aproveitamento_fora = round((pontos_fora / max_pontos_fora) * 100, 1) if max_pontos_fora > 0 else 0.0
        
        # Últimos 5 jogos
        ultimos_5 = jogos[-5:] if len(jogos) >= 5 else jogos
        pontos_ultimos_5 = sum(j['pontos'] for j in ultimos_5)
        
        # Sequência dos últimos 5 (V, E, D)
        resultados_ultimos_5 = []
        for jogo in ultimos_5:
            if jogo['resultado'] == 'Vitória':
                resultados_ultimos_5.append('V')
            elif jogo['resultado'] == 'Empate':
                resultados_ultimos_5.append('E')
            else:
                resultados_ultimos_5.append('D')
        
        ultimos_5_resultados = ''.join(resultados_ultimos_5)
        
        # Sequência atual (quantos jogos consecutivos do mesmo resultado)
        if jogos:
            ultimo_resultado = jogos[-1]['resultado']
            sequencia_count = 1
            for i in range(len(jogos) - 2, -1, -1):
                if jogos[i]['resultado'] == ultimo_resultado:
                    sequencia_count += 1
                else:
                    break
            
            if ultimo_resultado == 'Vitória':
                sequencia_atual = f"{sequencia_count}V"
            elif ultimo_resultado == 'Empate':
                sequencia_atual = f"{sequencia_count}E"
            else:
                sequencia_atual = f"{sequencia_count}D"
        else:
            sequencia_atual = ''
        
        return {
            'total_jogos': len(jogos),
            'vitorias': vitorias,
            'empates': empates,
            'derrotas': derrotas,
            'pontos_total': pontos_total,
            'ppg': round(pontos_total / len(jogos), 2) if jogos else 0.0,
            'ppg_casa': ppg_casa,
            'ppg_fora': ppg_fora,
            'aproveitamento_casa': aproveitamento_casa,
            'aproveitamento_fora': aproveitamento_fora,
            'gols_marcados': gols_marcados,
            'gols_sofridos': gols_sofridos,
            'saldo_gols': gols_marcados - gols_sofridos,
            'media_gols_marcados': round(gols_marcados / len(jogos), 2) if jogos else 0.0,
            'media_gols_sofridos': round(gols_sofridos / len(jogos), 2) if jogos else 0.0,
            'clean_sheets': clean_sheets,
            'pct_vitorias': round((vitorias / len(jogos)) * 100, 1) if jogos else 0.0,
            'pct_clean_sheets': round((clean_sheets / len(jogos)) * 100, 1) if jogos else 0.0,
            'pontos_ultimos_5': pontos_ultimos_5,
            'sequencia_atual': sequencia_atual,
            'ultimos_5_resultados': ultimos_5_resultados
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
