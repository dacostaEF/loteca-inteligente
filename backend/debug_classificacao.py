#!/usr/bin/env python3
"""
Debug da classificação - verificar dados no banco
"""
from models.classificacao_db import classificacao_db
import json

print("🔍 [DEBUG] Verificando banco tabelas_classificacao.db...")

try:
    # Verificar se banco existe
    import os
    db_path = "models/tabelas_classificacao.db"
    exists = os.path.exists(db_path)
    print(f"📁 [DEBUG] Banco existe: {exists}")
    
    if exists:
        size = os.path.getsize(db_path) 
        print(f"📊 [DEBUG] Tamanho do banco: {size} bytes")
    
    # Testar conexão
    info = classificacao_db.get_tables_info()
    print(f"📋 [DEBUG] Info das tabelas: {json.dumps(info, indent=2)}")
    
    # Tentar carregar Série A
    print("\n🏆 [DEBUG] Carregando Série A...")
    serie_a = classificacao_db.get_classificacao_serie_a()
    print(f"📊 [DEBUG] Registros encontrados: {len(serie_a)}")
    
    if serie_a:
        print("🎯 [DEBUG] Primeiros 3 times:")
        for i, time in enumerate(serie_a[:3]):
            print(f"   {i+1}. {time.get('time', 'N/A')} - {time.get('pontos', 0)} pts")
    
    # Tentar Série B
    print("\n🥈 [DEBUG] Carregando Série B...")
    serie_b = classificacao_db.get_classificacao_serie_b()
    print(f"📊 [DEBUG] Registros Série B: {len(serie_b)}")
    
except Exception as e:
    print(f"❌ [DEBUG] Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ [DEBUG] Verificação concluída")
