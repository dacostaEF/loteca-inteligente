#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models.classificacao_db import ClassificacaoDB

def verificar_ultimos_jogos():
    print("=== ANALISE DOS ULTIMOS 5 JOGOS - SERIE A ===")
    
    db = ClassificacaoDB()
    data = db.get_classificacao_serie_a()
    
    print(f"Total de times: {len(data)}")
    print("\nPRIMEIROS 10 TIMES:")
    print("-" * 50)
    
    for i, time in enumerate(data[:10], 1):
        ultimos = time.get('ultimos_confrontos', 'N/A')
        print(f"{i:2d}. {time['time']:15s} | Ultimos: {ultimos:5s}")
    
    print("\nULTIMOS 10 TIMES:")
    print("-" * 50)
    
    for i, time in enumerate(data[10:], 11):
        ultimos = time.get('ultimos_confrontos', 'N/A')
        print(f"{i:2d}. {time['time']:15s} | Ultimos: {ultimos:5s}")
    
    # Análise dos dados
    print("\nANALISE:")
    print("-" * 30)
    
    com_dados = [t for t in data if t.get('ultimos_confrontos')]
    sem_dados = [t for t in data if not t.get('ultimos_confrontos')]
    
    print(f"Times COM dados: {len(com_dados)}")
    print(f"Times SEM dados: {len(sem_dados)}")
    
    if sem_dados:
        print(f"\nTimes sem dados:")
        for time in sem_dados:
            print(f"   - {time['time']}")

if __name__ == "__main__":
    verificar_ultimos_jogos()
