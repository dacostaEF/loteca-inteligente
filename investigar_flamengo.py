#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para investigar a discrepância nos dados do Flamengo
"""

import csv
import os
from datetime import datetime

def investigar_flamengo():
    """
    Investiga os dados do Flamengo em detalhes
    """
    print("=== INVESTIGACAO DETALHADA - FLAMENGO ===")
    
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
    
    print("\n=== ULTIMOS 10 JOGOS (MAIS RECENTE PRIMEIRO) ===")
    for i, jogo in enumerate(jogos_ordenados[:10], 1):
        data = jogo['Data']
        time_casa = jogo['Time_Casa']
        gols_casa = jogo['Gols_Casa']
        gols_visitante = jogo['Gols_Visitante']
        time_visitante = jogo['Time_Visitante']
        resultado = jogo['Resultado_Fla']
        
        print(f"{i:2d}. {data} - {time_casa} {gols_casa} x {gols_visitante} {time_visitante} ({resultado})")
    
    print("\n=== ANALISE DOS ULTIMOS 5 JOGOS ===")
    ultimos_5 = jogos_ordenados[:5]
    
    # Verificar se há algum problema nos dados
    for i, jogo in enumerate(ultimos_5, 1):
        data = jogo['Data']
        time_casa = jogo['Time_Casa']
        gols_casa = jogo['Gols_Casa']
        gols_visitante = jogo['Gols_Visitante']
        time_visitante = jogo['Time_Visitante']
        resultado = jogo['Resultado_Fla']
        
        # Verificar se o resultado faz sentido baseado no placar
        if time_casa == 'Fla':
            # Flamengo jogou em casa
            if int(gols_casa) > int(gols_visitante):
                resultado_esperado = 'Vitoria'
            elif int(gols_casa) < int(gols_visitante):
                resultado_esperado = 'Derrota'
            else:
                resultado_esperado = 'Empate'
        else:
            # Flamengo jogou fora
            if int(gols_visitante) > int(gols_casa):
                resultado_esperado = 'Vitoria'
            elif int(gols_visitante) < int(gols_casa):
                resultado_esperado = 'Derrota'
            else:
                resultado_esperado = 'Empate'
        
        print(f"Jogo {i}: {data}")
        print(f"  Placar: {time_casa} {gols_casa} x {gols_visitante} {time_visitante}")
        print(f"  Resultado no CSV: {resultado}")
        print(f"  Resultado esperado: {resultado_esperado}")
        
        if resultado != resultado_esperado:
            print(f"  AVISO: INCONSISTENCIA DETECTADA!")
        else:
            print(f"  OK: Consistente")
        print()
    
    # Calcular sequência final
    print("=== SEQUENCIA FINAL ===")
    sequencia = ""
    for jogo in ultimos_5:
        resultado = jogo['Resultado_Fla']
        
        if resultado == 'Vitoria':
            sequencia += "V"
        elif resultado == 'Empate':
            sequencia += "E"
        elif resultado == 'Derrota':
            sequencia += "D"
        else:
            sequencia += "?"
    
    print(f"Sequencia calculada: {sequencia}")
    print(f"Sequencia do browser: EVE-E")
    print(f"Sequencia do script: EDEEE")
    
    # Verificar se há algum padrão
    print("\n=== COMPARACAO DETALHADA ===")
    browser_seq = "EVE-E"
    script_seq = "EDEEE"
    
    print("Posicao | Browser | Script | CSV   | Status")
    print("--------|---------|--------|-------|--------")
    for i, (browser, script, csv_char) in enumerate(zip(browser_seq, script_seq, sequencia)):
        status = "OK" if browser == csv_char else "DIF"
        print(f"   {i+1}    |    {browser}    |   {script}    |   {csv_char}   |  {status}")

if __name__ == "__main__":
    investigar_flamengo()
