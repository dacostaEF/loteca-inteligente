#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da API de classificação da Central Admin
"""

import requests
import json

def test_classification_api():
    """Testar API de classificação"""
    print("=== TESTE DA API DE CLASSIFICACAO ===")
    
    url = 'http://localhost:5000/api/admin/classificacao'
    data = {
        'admin_key': 'loteca2024admin',
        'campeonato': 'serie-a'
    }
    
    try:
        print("Enviando requisicao...")
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Total: {result.get('total')}")
            print(f"Campeonato: {result.get('campeonato')}")
            
            if result.get('classificacao'):
                classificacao = result['classificacao']
                print(f"Times encontrados: {len(classificacao)}")
                if len(classificacao) > 0:
                    print(f"Primeiro time: {classificacao[0].get('time', 'N/A')}")
                    print(f"Pontos do primeiro: {classificacao[0].get('pontos', 'N/A')}")
            else:
                print("ERRO: Nenhuma classificacao retornada!")
                return False
        else:
            print(f"Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Erro na requisicao: {e}")
        return False

def test_serie_b():
    """Testar Série B"""
    print("\n=== TESTE SERIE B ===")
    
    url = 'http://localhost:5000/api/admin/classificacao'
    data = {
        'admin_key': 'loteca2024admin',
        'campeonato': 'serie-b'
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Total: {result.get('total')}")
            
            if result.get('classificacao'):
                classificacao = result['classificacao']
                print(f"Times Série B: {len(classificacao)}")
            else:
                print("ERRO: Nenhuma classificacao Série B!")
                return False
        else:
            print(f"Erro HTTP: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Erro na requisicao: {e}")
        return False

if __name__ == "__main__":
    print("Testando Central Admin...")
    
    # Testar Série A
    serie_a_ok = test_classification_api()
    
    # Testar Série B
    serie_b_ok = test_serie_b()
    
    print("\n=== RESULTADO FINAL ===")
    print(f"Série A: {'OK' if serie_a_ok else 'FALHOU'}")
    print(f"Série B: {'OK' if serie_b_ok else 'FALHOU'}")
    
    if serie_a_ok and serie_b_ok:
        print("\nSUCESSO: APIs funcionando!")
    else:
        print("\nERRO: Problemas nas APIs!")
