#!/usr/bin/env python3
"""
Debug completo da API de classificação
"""
import sys
import os
import json

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.classificacao_db import classificacao_db
from admin_api import bp_admin
from flask import Flask

def testar_banco():
    print("🔍 [DEBUG] === TESTANDO BANCO DIRETO ===")
    
    try:
        # Verificar se banco existe
        db_path = "models/tabelas_classificacao.db"
        if not os.path.exists(db_path):
            print(f"❌ [DEBUG] Banco não existe: {db_path}")
            return False
            
        print(f"✅ [DEBUG] Banco existe: {db_path}")
        print(f"📊 [DEBUG] Tamanho: {os.path.getsize(db_path)} bytes")
        
        # Testar conexão
        dados = classificacao_db.get_classificacao_serie_a()
        print(f"📋 [DEBUG] Registros encontrados: {len(dados)}")
        
        if dados:
            print("🏆 [DEBUG] Primeiros 3 times:")
            for i, time in enumerate(dados[:3]):
                print(f"   {i+1}. {time}")
                
        return True
        
    except Exception as e:
        print(f"❌ [DEBUG] Erro no banco: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_api_function():
    print("\n🔍 [DEBUG] === TESTANDO FUNÇÃO DA API ===")
    
    try:
        # Simular requisição
        from admin_api import get_classificacao
        from flask import Flask
        app = Flask(__name__)
        
        with app.test_request_context(
            '/api/admin/classificacao', 
            method='POST',
            json={'admin_key': 'loteca2024admin', 'campeonato': 'serie-a'}
        ):
            response = get_classificacao()
            print(f"📥 [DEBUG] Response type: {type(response)}")
            print(f"📋 [DEBUG] Response: {response}")
            
    except Exception as e:
        print(f"❌ [DEBUG] Erro na API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 [DEBUG] Iniciando debug completo...")
    
    if testar_banco():
        testar_api_function()
    
    print("\n🏁 [DEBUG] Debug concluído!")
