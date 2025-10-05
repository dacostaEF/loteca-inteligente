#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisar backup original para entender estrutura JavaScript
"""

def analyze_backup():
    """Analisar backup original"""
    print("Analisando backup original...")
    
    # Ler backup original
    with open('backend/templates/loteca.html.backup', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Tamanho do arquivo: {len(content)} caracteres")
    
    # Verificar funções JavaScript críticas
    functions_to_check = [
        'function login()',
        'function togglePasswordVisibility()',
        'function logout()',
        'async function carregarClassificacao()'
    ]
    
    print("\n=== FUNCOES NO BACKUP ===")
    for func in functions_to_check:
        if func in content:
            print(f"OK: {func}")
        else:
            print(f"MISSING: {func}")
    
    # Verificar estrutura do script
    script_start = content.find('<script>')
    script_end = content.find('</script>')
    if script_start != -1 and script_end != -1:
        script_content = content[script_start:script_end]
        print(f"\nScript encontrado: {len(script_content)} caracteres")
        
        # Verificar se há await problemático
        if 'await ' in script_content:
            print("AVISO: await encontrado no script")
            await_count = script_content.count('await ')
            print(f"Total de awaits: {await_count}")
        else:
            print("OK: Nenhum await encontrado")
    else:
        print("ERRO: Script nao encontrado")
    
    # Verificar se é o arquivo correto (deve ter admin_interface)
    if 'admin_interface' in content:
        print("OK: Arquivo contem admin_interface")
    else:
        print("AVISO: Arquivo nao contem admin_interface")
    
    return True

if __name__ == "__main__":
    print("=== ANALISE DO BACKUP ORIGINAL ===")
    analyze_backup()
