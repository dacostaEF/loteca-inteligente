#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover classe do HTML e adicionar referência externa
"""

def remove_class_and_add_reference():
    """Remover classe do HTML e adicionar referência externa"""
    print("Removendo classe do HTML e adicionando referencia externa...")
    
    # Ler arquivo HTML
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar início da classe
    start_pattern = 'class CartolaVerificationProvider {'
    start_pos = content.find(start_pattern)
    
    if start_pos == -1:
        print("ERRO: Classe CartolaVerificationProvider nao encontrada!")
        return False
    
    # Encontrar fim da classe
    end_patterns = [
        'class CentralAdminProvider {',
        'class InternationalProvider {',
        'function ',
        'async function ',
        'document.addEventListener'
    ]
    
    end_pos = len(content)
    for pattern in end_patterns:
        pos = content.find(pattern, start_pos + 1)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    
    # Remover classe do HTML
    new_content = content[:start_pos] + content[end_pos:]
    
    # Adicionar referência externa antes do </head>
    head_end = new_content.find('</head>')
    if head_end == -1:
        print("ERRO: Tag </head> nao encontrada!")
        return False
    
    # Inserir referência ao JavaScript
    js_reference = '    <script src="{{ url_for(\'static\', filename=\'js/providers/cartola-provider.js\') }}"></script>\n'
    new_content = new_content[:head_end] + js_reference + new_content[head_end:]
    
    # Salvar arquivo modificado
    with open('backend/templates/loteca.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Classe removida e referencia adicionada!")
    
    # Contar linhas antes e depois
    old_lines = len(content.split('\n'))
    new_lines = len(new_content.split('\n'))
    reduction = old_lines - new_lines
    
    print(f"Linhas antes: {old_lines}")
    print(f"Linhas depois: {new_lines}")
    print(f"Reducao: {reduction} linhas")
    
    return True

if __name__ == "__main__":
    print("=== REMOCAO DA CLASSE E ADICAO DE REFERENCIA ===")
    
    success = remove_class_and_add_reference()
    
    if success:
        print("\nSUCESSO: Classe removida e referencia adicionada!")
    else:
        print("\nERRO: Falha na remocao da classe!")
