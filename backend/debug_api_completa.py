#!/usr/bin/env python3
"""
Debug completo da API - passo a passo
"""
import requests
import json
import sys
import os

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.classificacao_db import classificacao_db

def debug_completo():
    print("🔍 [DEBUG] === DIAGNÓSTICO COMPLETO ===")
    
    # 1. Testar classe diretamente
    print("\n1️⃣ [DEBUG] Testando classe ClassificacaoDB...")
    
    try:
        dados_a = classificacao_db.get_classificacao_serie_a()
        dados_b = classificacao_db.get_classificacao_serie_b()
        
        print(f"   📊 Série A: {len(dados_a)} registros")
        print(f"   📊 Série B: {len(dados_b)} registros")
        
        if dados_b:
            print("   🏆 Série B - Primeiro time:")
            print(f"      {dados_b[0]}")
    except Exception as e:
        print(f"   ❌ Erro na classe: {e}")
    
    # 2. Testar banco direto
    print("\n2️⃣ [DEBUG] Testando banco SQLite direto...")
    
    try:
        import sqlite3
        conn = sqlite3.connect("models/tabelas_classificacao.db")
        conn.row_factory = sqlite3.Row  # Para dict
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM classificacao_serie_b")
        total = cursor.fetchone()['total']
        print(f"   📊 Total registros Série B: {total}")
        
        if total > 0:
            cursor.execute("SELECT * FROM classificacao_serie_b ORDER BY posicao LIMIT 2")
            times = cursor.fetchall()
            print("   🏆 Primeiros 2 times:")
            for time in times:
                print(f"      {dict(time)}")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Erro no banco: {e}")
    
    # 3. Testar API
    print("\n3️⃣ [DEBUG] Testando API HTTP...")
    
    try:
        url = "http://localhost:5000/api/admin/classificacao"
        payload = {
            "admin_key": "loteca2024admin",
            "campeonato": "serie-b"
        }
        
        response = requests.post(url, json=payload, timeout=5)
        print(f"   📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success')}")
            print(f"   📊 Total: {data.get('total')}")
            print(f"   🏆 Campeonato: {data.get('campeonato')}")
            
            if data.get('classificacao'):
                print("   🎯 Primeiro time da API:")
                print(f"      {data['classificacao'][0]}")
        else:
            print(f"   ❌ Erro HTTP: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro na API: {e}")

if __name__ == "__main__":
    debug_completo()
