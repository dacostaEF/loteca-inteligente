#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair primeira classe JavaScript (CartolaVerificationProvider)
"""

def extract_cartola_provider():
    """Extrair classe CartolaVerificationProvider"""
    print("Extraindo classe CartolaVerificationProvider...")
    
    # Ler arquivo HTML
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar início da classe
    start_pattern = 'class CartolaVerificationProvider {'
    start_pos = content.find(start_pattern)
    
    if start_pos == -1:
        print("ERRO: Classe CartolaVerificationProvider nao encontrada!")
        return False
    
    # Encontrar fim da classe (próxima classe ou função)
    end_patterns = [
        'class CentralAdminProvider {',
        'class InternationalProvider {',
        'function ',
        'async function ',
        'document.addEventListener'
    ]
    
    end_pos = len(content)  # Default: fim do arquivo
    for pattern in end_patterns:
        pos = content.find(pattern, start_pos + 1)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    
    # Extrair classe
    class_content = content[start_pos:end_pos].strip()
    
    # Salvar em arquivo separado
    with open('backend/static/js/providers/cartola-provider.js', 'w', encoding='utf-8') as f:
        f.write(class_content)
    
    print(f"Classe extraida com sucesso!")
    print(f"Tamanho: {len(class_content)} caracteres")
    
    # Contar linhas
    lines = class_content.count('\n') + 1
    print(f"Linhas: {lines}")
    
    return True

def count_remaining_lines():
    """Contar linhas restantes no HTML"""
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = len(content.split('\n'))
    print(f"Linhas restantes no HTML: {lines}")
    return lines

if __name__ == "__main__":
    print("=== EXTRACAO DA PRIMEIRA CLASSE ===")
    
    # Extrair classe
    success = extract_cartola_provider()
    
    if success:
        # Contar linhas restantes
        remaining_lines = count_remaining_lines()
        print(f"\nSUCESSO: Classe extraida!")
        print(f"Arquivo HTML agora tem: {remaining_lines} linhas")
    else:
        print("\nERRO: Falha na extracao da classe!")
