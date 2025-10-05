#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para substituir CSS embutido por referência externa
"""

def replace_css_with_external():
    """Substituir CSS embutido por referência externa"""
    print("Substituindo CSS embutido por referencia externa...")
    
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
    
    # Criar referência externa
    external_css = '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/loteca.css\') }}">'
    
    # Substituir CSS embutido por referência externa
    new_content = content[:start_pos] + external_css + content[end_pos + len(end_tag):]
    
    # Salvar arquivo modificado
    with open('backend/templates/loteca.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("CSS substituido com sucesso!")
    
    # Contar linhas antes e depois
    old_lines = len(content.split('\n'))
    new_lines = len(new_content.split('\n'))
    reduction = old_lines - new_lines
    
    print(f"Linhas antes: {old_lines}")
    print(f"Linhas depois: {new_lines}")
    print(f"Reducao: {reduction} linhas")
    
    return True

if __name__ == "__main__":
    print("=== SUBSTITUICAO DE CSS ===")
    
    success = replace_css_with_external()
    
    if success:
        print("\nSUCESSO: CSS substituido por referencia externa!")
    else:
        print("\nERRO: Falha na substituicao do CSS!")
