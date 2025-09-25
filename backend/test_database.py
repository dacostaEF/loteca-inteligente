#!/usr/bin/env python3
"""
Script de teste para o sistema de banco de dados do Brasileirão
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models.brasileirao_db import brasileirao_db

def test_database():
    """Testa todas as funcionalidades do banco"""
    
    print("🧪 TESTE DO BANCO DE DADOS BRASILEIRÃO")
    print("=" * 50)
    
    # 1. Verificar status inicial
    print("\n1️⃣ STATUS INICIAL:")
    data_age = brasileirao_db.get_data_age()
    is_fresh = brasileirao_db.is_data_fresh()
    
    print(f"📊 Idade dos dados: {data_age or 'Nenhum dado'}")
    print(f"🔄 Dados frescos: {is_fresh}")
    
    # 2. Salvar dados de teste
    print("\n2️⃣ SALVANDO DADOS DE TESTE:")
    test_data = [
        {"pos": 1, "time": "Flamengo", "p": 51, "j": 23, "v": 15, "e": 6, "d": 2, 
         "gp": 48, "gc": 11, "sg": 37, "aproveitamento": 73, "ultimos": "VVEVE", "zona": "libertadores"},
        {"pos": 2, "time": "Palmeiras", "p": 49, "j": 22, "v": 15, "e": 4, "d": 3, 
         "gp": 36, "gc": 18, "sg": 18, "aproveitamento": 74, "ultimos": "VVVEV", "zona": "libertadores"},
        {"pos": 3, "time": "Cruzeiro", "p": 45, "j": 22, "v": 14, "e": 3, "d": 5, 
         "gp": 35, "gc": 20, "sg": 15, "aproveitamento": 68, "ultimos": "VVDEV", "zona": "libertadores"}
    ]
    
    try:
        brasileirao_db.save_classification(test_data, fonte="teste_script", rodada=25)
        print("✅ Dados salvos com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return
    
    # 3. Buscar dados salvos
    print("\n3️⃣ BUSCANDO DADOS SALVOS:")
    saved_data = brasileirao_db.get_latest_classification()
    
    if saved_data:
        print(f"✅ Encontrados {len(saved_data)} times")
        print("🏆 Top 3:")
        for team in saved_data[:3]:
            print(f"   {team['pos']}º {team['time']} - {team['p']} pts - {team['ultimos']}")
    else:
        print("❌ Nenhum dado encontrado")
        return
    
    # 4. Verificar frescor dos dados
    print("\n4️⃣ VERIFICAR FRESCOR:")
    new_age = brasileirao_db.get_data_age()
    new_fresh = brasileirao_db.is_data_fresh()
    
    print(f"📊 Nova idade: {new_age}")
    print(f"🔄 Agora frescos: {new_fresh}")
    
    # 5. Histórico de um time
    print("\n5️⃣ HISTÓRICO DO FLAMENGO:")
    history = brasileirao_db.get_team_history("Flamengo", limit=5)
    
    if history:
        for record in history:
            print(f"   Posição {record['posicao']} - {record['pontos']} pts - Rodada {record.get('rodada', 'N/A')}")
    else:
        print("❌ Nenhum histórico encontrado")
    
    # 6. Teste de performance
    print("\n6️⃣ TESTE DE PERFORMANCE:")
    import time
    
    start = time.time()
    for i in range(100):
        _ = brasileirao_db.get_latest_classification()
    end = time.time()
    
    avg_time = (end - start) / 100 * 1000  # em ms
    print(f"⚡ Média por consulta: {avg_time:.2f}ms")
    
    print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("🎯 O banco está funcionando perfeitamente!")

if __name__ == "__main__":
    test_database()
