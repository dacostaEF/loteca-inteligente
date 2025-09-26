#!/usr/bin/env python3
"""
Testar as APIs do admin - especialmente classificação
"""
import requests
import json

BASE_URL = "http://localhost:5000"
ADMIN_KEY = "loteca2024admin"

def test_classificacao_api():
    print("🧪 [TEST] Testando API de classificação...")
    
    url = f"{BASE_URL}/api/admin/classificacao"
    payload = {
        "admin_key": ADMIN_KEY,
        "campeonato": "serie-a"
    }
    
    try:
        print(f"📤 [TEST] POST {url}")
        print(f"📋 [TEST] Payload: {payload}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"📥 [TEST] Status: {response.status_code}")
        print(f"📋 [TEST] Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ [TEST] Sucesso!")
            print(f"📊 [TEST] Success: {data.get('success')}")
            print(f"📊 [TEST] Total: {data.get('total')}")
            print(f"📊 [TEST] Campeonato: {data.get('campeonato')}")
            
            if data.get('classificacao'):
                print(f"🏆 [TEST] Primeiros 3 times:")
                for i, time in enumerate(data['classificacao'][:3]):
                    print(f"   {i+1}. {time.get('time')} - {time.get('pontos')} pts")
        else:
            print(f"❌ [TEST] Erro HTTP: {response.status_code}")
            print(f"📄 [TEST] Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ [TEST] Servidor não está rodando!")
        return False
    except Exception as e:
        print(f"❌ [TEST] Erro: {e}")
        return False
    
    return True

def test_admin_dashboard():
    print("\n🧪 [TEST] Testando dashboard admin...")
    
    url = f"{BASE_URL}/api/admin/dashboard"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"📥 [TEST] Dashboard Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ [TEST] Dashboard OK!")
            print(f"📊 [TEST] Total clubes: {data.get('total_clubes', 'N/A')}")
        else:
            print(f"❌ [TEST] Dashboard erro: {response.text}")
            
    except Exception as e:
        print(f"❌ [TEST] Erro dashboard: {e}")

if __name__ == "__main__":
    print("🚀 [TEST] Iniciando testes da API Admin...")
    
    # Testar se servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ [TEST] Servidor respondendo: {response.status_code}")
    except:
        print("❌ [TEST] Servidor não está rodando! Execute: python app.py")
        exit(1)
    
    # Testar APIs
    test_classificacao_api()
    test_admin_dashboard()
    
    print("\n🏁 [TEST] Testes concluídos!")
