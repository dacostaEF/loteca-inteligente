#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⚔️ GERENCIADOR DE CONFRONTOS DIRETOS
Gerencia histórico de confrontos entre clubes para análise H2H
"""

import os
import csv
from typing import List, Dict, Optional
from datetime import datetime

class ConfrontosManager:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), 'Confrontos')
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        """Garante que o diretório base existe"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def get_confronto_file_path(self, clube1: str, clube2: str) -> str:
        """Retorna o caminho do arquivo de confronto entre dois clubes"""
        # Ordenar alfabeticamente para consistência
        clubes = sorted([clube1.lower(), clube2.lower()])
        filename = f"{clubes[0].title()}_vs_{clubes[1].title()}.csv"
        return os.path.join(self.base_path, filename)
    
    def carregar_confrontos(self, clube1: str, clube2: str) -> List[Dict]:
        """Carrega o histórico de confrontos entre dois clubes"""
        try:
            confronto_file = self.get_confronto_file_path(clube1, clube2)
            
            if not os.path.exists(confronto_file):
                print(f"Arquivo de confronto não encontrado: {confronto_file}")
                return []
            
            confrontos = []
            with open(confronto_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    confrontos.append(row)
            
            # Ordenar por data (mais recente primeiro)
            confrontos.sort(key=lambda x: x['data'], reverse=True)
            
            print(f"✅ Carregados {len(confrontos)} confrontos entre {clube1} e {clube2}")
            return confrontos
            
        except Exception as e:
            print(f"❌ Erro ao carregar confrontos: {e}")
            return []
    
    def analisar_confrontos(self, clube1: str, clube2: str, ultimos_n: int = 10) -> Dict:
        """
        Analisa o histórico de confrontos entre dois clubes
        
        Args:
            clube1 (str): Nome do primeiro clube
            clube2 (str): Nome do segundo clube  
            ultimos_n (int): Número de jogos recentes a analisar
            
        Returns:
            Dict: Estatísticas do confronto direto
        """
        confrontos = self.carregar_confrontos(clube1, clube2)
        
        if not confrontos:
            return {
                'total_jogos': 0,
                'vitorias_clube1': 0,
                'empates': 0,
                'vitorias_clube2': 0,
                'ultimos_resultados': '',
                'tendencia': 'Sem dados',
                'clube1': clube1,
                'clube2': clube2
            }
        
        # Analisar apenas os últimos N jogos
        jogos_analisados = confrontos[:ultimos_n]
        
        vitorias_clube1 = 0
        empates = 0
        vitorias_clube2 = 0
        resultados = []
        
        for jogo in jogos_analisados:
            resultado = jogo['resultado_corinthians'].upper()  # Resultado sempre na perspectiva do Corinthians
            
            # Ajustar perspectiva para o clube1
            if clube1.lower() == 'corinthians':
                if resultado == 'V':
                    vitorias_clube1 += 1
                    resultados.append('V')
                elif resultado == 'E':
                    empates += 1
                    resultados.append('E')
                else:  # 'D'
                    vitorias_clube2 += 1
                    resultados.append('D')
            else:  # clube1 é Flamengo
                if resultado == 'V':
                    vitorias_clube2 += 1
                    resultados.append('D')
                elif resultado == 'E':
                    empates += 1
                    resultados.append('E')
                else:  # 'D'
                    vitorias_clube1 += 1
                    resultados.append('V')
        
        # Determinar tendência
        if vitorias_clube1 > vitorias_clube2:
            tendencia = f"Vantagem {clube1}"
        elif vitorias_clube2 > vitorias_clube1:
            tendencia = f"Vantagem {clube2}"
        else:
            tendencia = "Equilíbrio"
        
        return {
            'total_jogos': len(jogos_analisados),
            'vitorias_clube1': vitorias_clube1,
            'empates': empates,
            'vitorias_clube2': vitorias_clube2,
            'ultimos_resultados': ''.join(resultados[:5]),  # Últimos 5 resultados
            'tendencia': tendencia,
            'clube1': clube1,
            'clube2': clube2,
            'historico_completo': jogos_analisados
        }
    
    def get_confronto_resumo(self, clube1: str, clube2: str) -> str:
        """Retorna um resumo do confronto no formato 'XV-YE-ZD'"""
        analise = self.analisar_confrontos(clube1, clube2)
        
        if analise['total_jogos'] == 0:
            return "Sem dados"
        
        return f"{analise['vitorias_clube1']}V-{analise['empates']}E-{analise['vitorias_clube2']}D"
    
    def listar_confrontos_disponiveis(self) -> List[str]:
        """Lista todos os confrontos disponíveis"""
        try:
            if not os.path.exists(self.base_path):
                return []
            
            arquivos = []
            for arquivo in os.listdir(self.base_path):
                if arquivo.endswith('.csv'):
                    arquivos.append(arquivo.replace('.csv', ''))
            
            return sorted(arquivos)
            
        except Exception as e:
            print(f"❌ Erro ao listar confrontos: {e}")
            return []

# Função de conveniência para uso rápido
def get_confronto_direto(clube1: str, clube2: str) -> Dict:
    """Função de conveniência para obter análise de confronto direto"""
    manager = ConfrontosManager()
    return manager.analisar_confrontos(clube1, clube2)

if __name__ == "__main__":
    # Teste do sistema
    print("🔍 TESTANDO SISTEMA DE CONFRONTOS")
    print("=" * 50)
    
    manager = ConfrontosManager()
    
    # Testar Corinthians vs Flamengo
    analise = manager.analisar_confrontos('Corinthians', 'Flamengo')
    
    print(f"📊 ANÁLISE: {analise['clube1']} vs {analise['clube2']}")
    print(f"   Total de jogos: {analise['total_jogos']}")
    print(f"   {analise['clube1']}: {analise['vitorias_clube1']} vitórias")
    print(f"   Empates: {analise['empates']}")
    print(f"   {analise['clube2']}: {analise['vitorias_clube2']} vitórias")
    print(f"   Últimos resultados: {analise['ultimos_resultados']}")
    print(f"   Tendência: {analise['tendencia']}")
    
    # Resumo
    resumo = manager.get_confronto_resumo('Corinthians', 'Flamengo')
    print(f"   Resumo: {resumo}")

