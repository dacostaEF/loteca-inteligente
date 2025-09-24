#!/usr/bin/env python3
"""
Script de teste para a API Loteca X-Ray
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(endpoint, description):
    """Testar um endpoint da API"""
    print(f"\n🧪 {description}")
    print(f"📡 GET {endpoint}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📄 Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro: {e}")

def main():
    """Executar todos os testes"""
    print("🚀 TESTANDO API LOTECA X-RAY")
    print("=" * 60)
    
    # Testes
    test_endpoint("/", "Informações da API")
    test_endpoint("/api/br/health", "Health Check")
    test_endpoint("/api/br/clubes", "Lista de Clubes")
    test_endpoint("/api/br/clube/8/stats", "Estatísticas Corinthians")
    test_endpoint("/api/br/clube/13/stats", "Estatísticas Flamengo")
    test_endpoint("/api/br/confronto/corinthians/flamengo", "Confronto Corinthians vs Flamengo")
    test_endpoint("/api/br/mercado/status", "Status do Mercado")
    test_endpoint("/api/br/mappings", "Mapeamento de Clubes")
    
    print("\n" + "="*60)
    print("🌍 TESTANDO API INTERNACIONAL")
    print("="*60)
    
    test_endpoint("/api/int/health", "Health Check Internacional")
    test_endpoint("/api/int/leagues", "Ligas Internacionais")
    test_endpoint("/api/int/league/premier_league/fixtures?days=3", "Fixtures Premier League")
    test_endpoint("/api/int/fixture/1001/analysis", "Análise de Fixture")
    test_endpoint("/api/int/fixtures/upcoming?days=2", "Próximos Jogos")
    test_endpoint("/api/int/recommendations/daily?days=2", "Recomendações Diárias")
    
    print("\n🎯 TESTES CONCLUÍDOS!")
    print("=" * 60)

if __name__ == "__main__":
    main()
