#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do endpoint de atualização
"""

import requests
import json

def teste_endpoint():
    url = 'http://localhost:5000/api/admin/atualizar-ultimos-confrontos'
    data = {
        'admin_key': 'loteca2024admin'
    }
    
    try:
        print('Testando endpoint...')
        response = requests.post(url, json=data)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'Success: {result.get("success")}')
            print(f'Message: {result.get("message")}')
            
            if 'serie_a_updated' in result:
                print(f'Série A atualizados: {result.get("serie_a_updated")}')
                print(f'Série B atualizados: {result.get("serie_b_updated")}')
            else:
                print('Ainda usando o script antigo')
        else:
            print(f'Erro: {response.text}')
            
    except Exception as e:
        print(f'Erro na requisição: {e}')

if __name__ == "__main__":
    teste_endpoint()

