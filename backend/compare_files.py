#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparar arquivo atual com versão que funcionava
"""

def compare_files():
    """Comparar arquivo atual com versão que funcionava"""
    print("=== COMPARACAO DE ARQUIVOS ===")
    
    # Ler arquivo atual
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Ler arquivo que funcionava
    with open('backend/admin_interface.html.broken', 'r', encoding='utf-8') as f:
        working_content = f.read()
    
    print(f"Arquivo atual: {len(current_content)} caracteres")
    print(f"Arquivo que funcionava: {len(working_content)} caracteres")
    
    # Verificar se são iguais
    if current_content == working_content:
        print("OK: ARQUIVOS SAO IDENTICOS!")
        return True
    else:
        print("ERRO: ARQUIVOS SAO DIFERENTES!")
        
        # Encontrar diferenças
        current_lines = current_content.split('\n')
        working_lines = working_content.split('\n')
        
        print(f"Linhas atual: {len(current_lines)}")
        print(f"Linhas que funcionava: {len(working_lines)}")
        
        # Verificar linha 3439 especificamente
        if len(current_lines) >= 3439:
            print(f"\nLinha 3439 atual: {current_lines[3438].strip()}")
        else:
            print("\nArquivo atual tem menos de 3439 linhas")
            
        if len(working_lines) >= 3439:
            print(f"Linha 3439 que funcionava: {working_lines[3438].strip()}")
        else:
            print("Arquivo que funcionava tem menos de 3439 linhas")
        
        return False

if __name__ == "__main__":
    compare_files()
