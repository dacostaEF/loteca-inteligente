#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificação de integridade do loteca.html
"""

import os
import re

def verify_file_integrity():
    """Verificar se arquivo principal ainda funciona"""
    print("Verificando integridade do loteca.html...")
    
    file_path = 'backend/templates/loteca.html'
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo nao encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar elementos essenciais
    essential_elements = [
        '<title>Raio-X da Loteca - Loterias Inteligente</title>',
        'initializeTabs()',
        'CentralAdminProvider',
        'carregarTabelaSerieA',
        'function mostrarNotificacao'
    ]
    
    missing_elements = []
    for element in essential_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"ERRO: Elementos essenciais faltando: {missing_elements}")
        return False
    else:
        print("OK: Integridade verificada!")
        return True

def check_static_paths():
    """Verificar se todos os paths estáticos existem"""
    print("Verificando paths estaticos...")
    
    static_files = [
        'static/css/loteca.css',
        'static/js/loteca-core.js',
        'static/js/providers/cartola-provider.js',
        'static/js/providers/admin-provider.js',
        'static/js/providers/international-provider.js',
        'static/js/data/serie-a.js',
        'static/js/data/serie-b.js',
        'static/js/ui/tabs.js',
        'static/js/ui/tables.js',
        'static/js/analysis/recommendations.js'
    ]
    
    missing_files = []
    for file_path in static_files:
        full_path = f'backend/{file_path}'
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"AVISO: Arquivos ainda nao criados: {missing_files}")
        return False
    else:
        print("OK: Todos os arquivos estaticos existem")
        return True

def count_lines():
    """Contar linhas do arquivo principal"""
    file_path = 'backend/templates/loteca.html'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"INFO: Arquivo principal: {len(lines)} linhas")
        return len(lines)
    return 0

if __name__ == "__main__":
    print("=== VERIFICACAO DE INTEGRIDADE ===")
    
    # Verificar integridade
    integrity_ok = verify_file_integrity()
    
    # Verificar paths estáticos
    paths_ok = check_static_paths()
    
    # Contar linhas
    line_count = count_lines()
    
    print("\nRESUMO:")
    print(f"Integridade: {'OK' if integrity_ok else 'FALHOU'}")
    print(f"Paths estaticos: {'OK' if paths_ok else 'AINDA NAO CRIADOS'}")
    print(f"Linhas: {line_count}")
    
    if integrity_ok:
        print("\nSUCESSO: Arquivo principal esta integro!")
    else:
        print("\nERRO: Problemas encontrados!")
