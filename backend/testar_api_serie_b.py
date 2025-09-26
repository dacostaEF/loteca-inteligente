#!/usr/bin/env python3
"""
Testar API para Série B
"""
import requests
import json

def testar_serie_b():
    print("🧪 [TESTE] Testando API para Série B...")
    
    url = "http://localhost:5000/api/admin/classificacao"
    
    # Testar Série A
    payload_a = {
        "admin_key": "loteca2024admin",
        "campeonato": "serie-a"
    }
    
    print("🥇 [TESTE] Testando Série A...")
    try:
        response = requests.post(url, json=payload_a, timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Success: {data.get('success')}")
        print(f"   Total: {data.get('total')}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Testar Série B  
    payload_b = {
        "admin_key": "loteca2024admin",
        "campeonato": "serie-b"
    }
    
    print("\n🥈 [TESTE] Testando Série B...")
    try:
        response = requests.post(url, json=payload_b, timeout=5)
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Success: {data.get('success')}")
        print(f"   Total: {data.get('total')}")
        
        if data.get('classificacao'):
            print("   Primeiros 3 times:")
            for i, time in enumerate(data['classificacao'][:3]):
                print(f"      {i+1}. {time.get('time')} - {time.get('pontos')} pts")
                
    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    testar_serie_b()
