#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisar tamanho do loteca.html
"""

def analyze_loteca_html():
    """Analisar tamanho do loteca.html"""
    print("Analisando loteca.html...")
    
    # Contar linhas
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total de linhas: {len(lines)}")
    
    # Contar caracteres
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Total de caracteres: {len(content)}")
    print(f"Tamanho em KB: {len(content) / 1024:.1f} KB")
    
    # Verificar se tem CSS externo
    if 'loteca.css' in content:
        print("OK: CSS externo encontrado")
    else:
        print("ERRO: CSS externo nao encontrado")
    
    # Verificar se tem JS externo
    if 'cartola-provider.js' in content:
        print("OK: JS externo encontrado")
    else:
        print("ERRO: JS externo nao encontrado")
    
    # Comparar com backup
    try:
        with open('backend/templates/loteca.html.backup', 'r', encoding='utf-8') as f:
            backup_lines = f.readlines()
        print(f"Backup tem: {len(backup_lines)} linhas")
        print(f"Reducao: {len(backup_lines) - len(lines)} linhas")
    except:
        print("Backup nao encontrado")

if __name__ == "__main__":
    print("=== ANALISE DO LOTECA.HTML ===")
    analyze_loteca_html()
