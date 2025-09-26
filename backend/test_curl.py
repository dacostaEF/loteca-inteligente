#!/usr/bin/env python3
"""
Teste com curl direto
"""
import subprocess
import json

def test_curl():
    print("🔍 [CURL] Testando com curl direto...")
    
    # Dados para serie-b
    data = {
        "admin_key": "loteca2024admin",
        "campeonato": "serie-b"
    }
    
    # Comando curl
    cmd = [
        "curl", "-X", "POST",
        "http://localhost:5000/api/admin/classificacao",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data),
        "--silent"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(f"📥 [CURL] Return code: {result.returncode}")
        print(f"📄 [CURL] Response: {result.stdout[:500]}...")
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"✅ [CURL] Success: {response.get('success')}")
            print(f"📊 [CURL] Total: {response.get('total')}")
        
    except Exception as e:
        print(f"❌ [CURL] Erro: {e}")

if __name__ == "__main__":
    test_curl()
