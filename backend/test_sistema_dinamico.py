#!/usr/bin/env python3
"""
Teste do Sistema de Carregamento Dinâmico
Verifica se todos os 14 jogos podem ser carregados via API
"""

import requests
import json
import sys
from pathlib import Path

def testar_api_jogo(numero_jogo):
    """Testa a API para um jogo específico"""
    print(f"\n🎯 Testando Jogo {numero_jogo}...")
    
    try:
        # URL da API
        url = f"http://localhost:5000/api/analise/jogo/{numero_jogo}?concurso=concurso_1216"
        
        # Fazer requisição
        response = requests.get(url, timeout=10)
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and data.get('dados'):
                dados = data['dados']
                print(f"✅ Jogo {numero_jogo}: {dados.get('time_casa', 'N/A')} vs {dados.get('time_fora', 'N/A')}")
                print(f"   📊 Probabilidades: {dados.get('probabilidades', {})}")
                print(f"   🔄 Sequência: {dados.get('confrontos_sequence', 'N/A')}")
                print(f"   📝 Análise: {dados.get('analise_rapida', 'N/A')[:50]}...")
                return True
            else:
                print(f"❌ Jogo {numero_jogo}: API retornou dados vazios")
                return False
        else:
            print(f"❌ Jogo {numero_jogo}: Erro HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Jogo {numero_jogo}: Servidor não está rodando")
        return False
    except Exception as e:
        print(f"❌ Jogo {numero_jogo}: Erro inesperado - {e}")
        return False

def verificar_arquivos_json():
    """Verifica se todos os arquivos JSON existem"""
    print("📁 Verificando arquivos JSON...")
    
    diretorio = Path("models/concurso_1216/analise_rapida")
    arquivos_ok = 0
    
    for i in range(1, 15):
        arquivo = diretorio / f"jogo_{i}.json"
        if arquivo.exists():
            print(f"✅ jogo_{i}.json - OK")
            arquivos_ok += 1
        else:
            print(f"❌ jogo_{i}.json - FALTANDO")
    
    print(f"\n📊 Resumo: {arquivos_ok}/14 arquivos encontrados")
    return arquivos_ok == 14

def main():
    """Função principal do teste"""
    print("🚀 TESTE DO SISTEMA DE CARREGAMENTO DINÂMICO")
    print("=" * 60)
    
    # 1. Verificar arquivos JSON
    arquivos_ok = verificar_arquivos_json()
    
    if not arquivos_ok:
        print("\n❌ ERRO: Nem todos os arquivos JSON foram encontrados!")
        print("Execute primeiro o script gerar_jogos_faltantes.py")
        return False
    
    print("\n✅ Todos os arquivos JSON estão presentes!")
    
    # 2. Testar API (se servidor estiver rodando)
    print("\n🔌 Testando API...")
    print("⚠️  Certifique-se de que o servidor Flask está rodando!")
    
    jogos_ok = 0
    
    for i in range(1, 15):
        if testar_api_jogo(i):
            jogos_ok += 1
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"✅ Jogos funcionando: {jogos_ok}/14")
    print(f"📁 Arquivos JSON: {arquivos_ok}/14")
    
    if jogos_ok == 14 and arquivos_ok == 14:
        print("\n🎉 SISTEMA 100% FUNCIONAL!")
        print("✅ Carregamento dinâmico implementado com sucesso!")
        return True
    else:
        print("\n⚠️  Sistema parcialmente funcional")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
