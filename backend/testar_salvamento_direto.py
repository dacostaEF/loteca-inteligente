#!/usr/bin/env python3
"""
Testar salvamento direto via API
"""
import requests
import json

def testar_salvamento():
    print("🧪 [TESTE] Testando salvamento direto...")
    
    # Teste 1: Salvar na Série A
    print("\n1️⃣ [TESTE] Série A - Alterar pontos do Flamengo...")
    
    payload_a = {
        "admin_key": "loteca2024admin",
        "campeonato": "serie-a",
        "updates": [{
            "id": 1,
            "field": "pontos",
            "value": 99
        }]
    }
    
    try:
        response = requests.post("http://localhost:5000/api/admin/classificacao/salvar", 
                               json=payload_a, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 2: Salvar na Série B
    print("\n2️⃣ [TESTE] Série B - Alterar pontos do Santos...")
    
    payload_b = {
        "admin_key": "loteca2024admin",
        "campeonato": "serie-b",
        "updates": [{
            "id": 1,
            "field": "pontos",
            "value": 88
        }]
    }
    
    try:
        response = requests.post("http://localhost:5000/api/admin/classificacao/salvar", 
                               json=payload_b, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    testar_salvamento()
