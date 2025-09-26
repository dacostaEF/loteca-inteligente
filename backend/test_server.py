#!/usr/bin/env python3
"""
Teste rápido do servidor
"""
import requests
import time

def test_server():
    print("🔍 [TEST] Verificando servidor...")
    
    try:
        # Testar página principal
        response = requests.get("http://localhost:5000/", timeout=5)
        print(f"✅ [TEST] Página principal: {response.status_code}")
        
        # Testar página loteca
        response = requests.get("http://localhost:5000/loteca", timeout=5)
        print(f"✅ [TEST] Página loteca: {response.status_code}")
        
        # Testar admin
        response = requests.get("http://localhost:5000/admin", timeout=5)
        print(f"✅ [TEST] Página admin: {response.status_code}")
        
        # Testar API classificação
        response = requests.post("http://localhost:5000/api/admin/classificacao", 
                                json={"admin_key": "loteca2024admin", "campeonato": "serie-a"}, 
                                timeout=5)
        print(f"✅ [TEST] API classificação: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 [TEST] API retornou {data.get('total', 0)} times")
            
    except requests.exceptions.ConnectionError:
        print("❌ [TEST] Servidor não está rodando!")
        return False
    except Exception as e:
        print(f"❌ [TEST] Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Aguardar servidor iniciar
    time.sleep(2)
    test_server()
