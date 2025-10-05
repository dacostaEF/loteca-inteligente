#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remover função duplicada carregarClassificacao
"""

def remove_duplicate_function():
    """Remover função duplicada carregarClassificacao"""
    print("Removendo função duplicada carregarClassificacao...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar onde começa a função duplicada (linha 3383)
    lines = content.split('\n')
    
    # Procurar pela linha que contém código solto da função duplicada
    start_line = -1
    for i, line in enumerate(lines):
        if 'const loadingEl = document.getElementById(\'loadingClassificacao\');' in line:
            start_line = i
            break
    
    if start_line == -1:
        print("ERRO: Não foi possível encontrar o início da função duplicada")
        return False
    
    # Procurar onde termina a função duplicada (linha 3519)
    end_line = -1
    for i in range(start_line, len(lines)):
        if 'console.log(\'🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===\');' in lines[i] and i > start_line + 50:
            # Verificar se a próxima linha é o fechamento da função
            if i + 1 < len(lines) and lines[i + 1].strip() == '}':
                end_line = i + 1
                break
    
    if end_line == -1:
        print("ERRO: Não foi possível encontrar o fim da função duplicada")
        return False
    
    print(f"Encontrada função duplicada da linha {start_line + 1} até {end_line + 1}")
    
    # Remover a função duplicada
    new_lines = lines[:start_line] + lines[end_line + 1:]
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("Função duplicada removida!")
    return True

if __name__ == "__main__":
    print("=== REMOÇÃO DA FUNÇÃO DUPLICADA ===")
    
    success = remove_duplicate_function()
    
    if success:
        print("\nSUCESSO: Função duplicada removida!")
        print("Reinicie o servidor para aplicar a correção.")
    else:
        print("\nERRO: Falha na remoção da função duplicada!")
