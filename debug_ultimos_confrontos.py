#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar exatamente como o sistema calcula os últimos confrontos
"""

import csv
import os
from datetime import datetime

def testar_calculo_ultimos_confrontos():
    """
    Testa o cálculo dos últimos confrontos do Flamengo
    """
    print("=== TESTE DE CALCULO DOS ULTIMOS CONFRONTOS - FLAMENGO ===")
    
    arquivo_jogos = "backend/models/Jogos/flamengo/jogos.csv"
    
    if not os.path.exists(arquivo_jogos):
        print(f"ERRO: Arquivo nao encontrado: {arquivo_jogos}")
        return
    
    # Ler o arquivo
    jogos = []
    with open(arquivo_jogos, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jogos.append(row)
    
    print(f"Total de jogos encontrados: {len(jogos)}")
    
    # Ordenar por data (mais recente primeiro)
    def parse_data(data_str):
        try:
            return datetime.strptime(data_str, '%d/%m/%Y')
        except ValueError:
            return datetime(1900, 1, 1)
    
    jogos_ordenados = sorted(jogos, key=lambda x: parse_data(x['Data']), reverse=True)
    
    print("\n=== TODOS OS JOGOS ORDENADOS (MAIS RECENTE PRIMEIRO) ===")
    for i, jogo in enumerate(jogos_ordenados, 1):
        data = jogo['Data']
        time_casa = jogo['Time_Casa']
        gols_casa = jogo['Gols_Casa']
        gols_visitante = jogo['Gols_Visitante']
        time_visitante = jogo['Time_Visitante']
        resultado = jogo['Resultado_Fla']
        
        print(f"{i:2d}. {data} - {time_casa} {gols_casa} x {gols_visitante} {time_visitante} ({resultado})")
    
    print("\n=== ULTIMOS 5 JOGOS ===")
    ultimos_5 = jogos_ordenados[:5]
    for i, jogo in enumerate(ultimos_5, 1):
        data = jogo['Data']
        time_casa = jogo['Time_Casa']
        gols_casa = jogo['Gols_Casa']
        gols_visitante = jogo['Gols_Visitante']
        time_visitante = jogo['Time_Visitante']
        resultado = jogo['Resultado_Fla']
        
        print(f"{i}. {data} - {time_casa} {gols_casa} x {gols_visitante} {time_visitante} ({resultado})")
    
    # Calcular sequência
    print("\n=== CALCULO DA SEQUENCIA ===")
    sequencia = ""
    for i, jogo in enumerate(ultimos_5, 1):
        resultado = jogo['Resultado_Fla']
        
        if resultado == 'Vitoria':
            sequencia += "V"
        elif resultado == 'Empate':
            sequencia += "E"
        elif resultado == 'Derrota':
            sequencia += "D"
        else:
            sequencia += "?"
        
        print(f"Jogo {i}: {resultado} -> {sequencia[-1]}")
    
    print(f"\nSequencia calculada: {sequencia}")
    print(f"Sequencia esperada (do browser): EVE-E")
    
    # Verificar se há diferença
    if sequencia == "EVE-E":
        print("✅ CORRETO: Sequencia bate com o browser!")
    else:
        print("❌ DIFERENTE: Sequencia nao bate com o browser!")
        print(f"Calculado: {sequencia}")
        print(f"Browser:   EVE-E")
        
        # Tentar entender a diferença
        print("\n=== ANALISE DA DIFERENCA ===")
        browser_seq = "EVE-E"
        for i, (calc, browser) in enumerate(zip(sequencia, browser_seq)):
            if calc != browser:
                print(f"Posicao {i+1}: Calculado='{calc}', Browser='{browser}'")

if __name__ == "__main__":
    testar_calculo_ultimos_confrontos()
