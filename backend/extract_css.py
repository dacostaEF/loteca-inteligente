#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair CSS do loteca.html de forma segura
"""

def extract_css():
    """Extrair CSS do arquivo HTML"""
    print("Extraindo CSS do loteca.html...")
    
    # Ler arquivo HTML
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar início e fim do CSS
    start_tag = '<style>'
    end_tag = '</style>'
    
    start_pos = content.find(start_tag)
    end_pos = content.find(end_tag)
    
    if start_pos == -1 or end_pos == -1:
        print("ERRO: Tags de CSS nao encontradas!")
        return False
    
    # Extrair CSS (sem as tags)
    css_content = content[start_pos + len(start_tag):end_pos]
    
    # Salvar CSS em arquivo separado
    with open('backend/static/css/loteca.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"CSS extraido com sucesso!")
    print(f"Tamanho do CSS: {len(css_content)} caracteres")
    
    return True

def count_css_lines():
    """Contar linhas do CSS extraído"""
    try:
        with open('backend/static/css/loteca.css', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"Linhas do CSS: {len(lines)}")
        return len(lines)
    except FileNotFoundError:
        print("ERRO: Arquivo CSS nao encontrado!")
        return 0

if __name__ == "__main__":
    print("=== EXTRACAO DE CSS ===")
    
    # Extrair CSS
    success = extract_css()
    
    if success:
        # Contar linhas
        line_count = count_css_lines()
        print(f"\nSUCESSO: CSS extraido com {line_count} linhas!")
    else:
        print("\nERRO: Falha na extracao do CSS!")
