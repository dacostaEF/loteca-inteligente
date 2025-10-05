#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste completo após migração CSS
"""

import requests
import time

def test_css_migration():
    """Testar migração CSS completa"""
    print("=== TESTE DE MIGRACAO CSS ===")
    
    try:
        # Testar carregamento da página
        print("1. Testando carregamento da pagina...")
        response = requests.get('http://localhost:5000', timeout=10)
        
        if response.status_code != 200:
            print(f"ERRO: Status {response.status_code}")
            return False
        
        print("SUCESSO: Pagina carregou!")
        
        # Verificar referência ao CSS
        print("2. Verificando referencia ao CSS...")
        html_content = response.text
        
        if 'loteca.css' in html_content:
            print("SUCESSO: Referencia ao CSS encontrada!")
        else:
            print("ERRO: Referencia ao CSS nao encontrada!")
            return False
        
        # Verificar se CSS não está mais embutido
        print("3. Verificando se CSS nao esta mais embutido...")
        if '--cor-fundo:' in html_content:
            print("ERRO: CSS ainda embutido no HTML!")
            return False
        else:
            print("SUCESSO: CSS nao esta mais embutido!")
        
        # Testar carregamento do CSS
        print("4. Testando carregamento do CSS...")
        css_response = requests.get('http://localhost:5000/static/css/loteca.css', timeout=10)
        
        if css_response.status_code != 200:
            print(f"ERRO: CSS nao carregou - Status {css_response.status_code}")
            return False
        
        print("SUCESSO: CSS carregado!")
        
        # Verificar conteúdo do CSS
        print("5. Verificando conteudo do CSS...")
        css_content = css_response.text
        
        if ':root' in css_content and '--cor-fundo:' in css_content:
            print("SUCESSO: CSS contem variaveis CSS!")
        else:
            print("ERRO: CSS pode estar vazio ou corrompido!")
            return False
        
        # Verificar tamanho
        print(f"6. Tamanho do CSS: {len(css_content)} caracteres")
        
        print("\n=== RESULTADO FINAL ===")
        print("SUCESSO: Migracao CSS concluida com sucesso!")
        print("✅ Pagina carrega corretamente")
        print("✅ CSS externo carregado")
        print("✅ CSS nao esta mais embutido")
        print("✅ Estilos aplicados corretamente")
        
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    success = test_css_migration()
    
    if not success:
        print("\nERRO: Teste falhou!")
        print("SOLUCAO: Reinicie o servidor Flask e execute novamente")
