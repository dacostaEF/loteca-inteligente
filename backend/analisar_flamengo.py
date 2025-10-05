#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from models.classificacao_db import ClassificacaoDB

def analisar_flamengo():
    print("=== ANALISE FLAMENGO: CSV vs BANCO ===")
    
    # 1. LER DADOS DO CSV
    csv_path = "models/Jogos/flamengo/jogos.csv"
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jogos = list(reader)
        
        print(f"\nCSV FLAMENGO - Total de jogos: {len(jogos)}")
        print("ULTIMOS 5 JOGOS DO CSV:")
        print("-" * 40)
        
        ultimos_5_csv = jogos[:5]  # Os mais recentes
        for i, jogo in enumerate(ultimos_5_csv, 1):
            resultado = jogo.get('Resultado_Fla', 'N/A')
            data = jogo.get('Data', 'N/A')
            adversario = f"{jogo.get('Time_Casa', '')} x {jogo.get('Time_Visitante', '')}"
            print(f"{i}. {data} | {adversario} | Resultado: {resultado}")
        
        # Calcular sequencia dos ultimos 5
        sequencia_csv = ''.join([jogo.get('Resultado_Fla', 'N')[0] for jogo in ultimos_5_csv])
        print(f"\nSEQUENCIA CSV: {sequencia_csv}")
        
    else:
        print("ERRO: Arquivo CSV do Flamengo nao encontrado!")
        return
    
    # 2. LER DADOS DO BANCO
    print(f"\nBANCO DE DADOS:")
    print("-" * 40)
    
    db = ClassificacaoDB()
    data = db.get_classificacao_serie_a()
    flamengo = next((t for t in data if t['time'] == 'Flamengo'), None)
    
    if flamengo:
        ultimos_banco = flamengo.get('ultimos_confrontos', 'N/A')
        print(f"FLAMENGO NO BANCO: {ultimos_banco}")
        
        # COMPARACAO
        print(f"\nCOMPARACAO:")
        print("-" * 30)
        print(f"CSV:     {sequencia_csv}")
        print(f"BANCO:   {ultimos_banco}")
        
        if sequencia_csv == ultimos_banco:
            print("✅ CONSISTENTE!")
        else:
            print("❌ INCONSISTENTE!")
            print(f"Diferenca: CSV tem {len(sequencia_csv)} chars, Banco tem {len(ultimos_banco)} chars")
    else:
        print("ERRO: Flamengo nao encontrado no banco!")

if __name__ == "__main__":
    analisar_flamengo()
