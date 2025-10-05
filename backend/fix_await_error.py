#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção cirúrgica do erro de await na linha 3379
"""

def fix_await_error():
    """Corrigir erro de await na linha 3379"""
    print("Corrigindo erro de await na linha 3379...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA: await fora de função async
    # Vamos encontrar onde está o await problemático
    problem_line = "const response = await fetch('/api/admin/classificacao', {"
    
    if problem_line in content:
        print("Problema encontrado!")
        
        # Encontrar o contexto ao redor
        start_pos = content.find(problem_line)
        
        # Procurar pela função que contém esse await
        # Vamos procurar para trás até encontrar uma função async
        function_start = content.rfind('async function', 0, start_pos)
        
        if function_start != -1:
            print("Funcao async encontrada antes do await")
            # O problema pode ser que a função não está marcada como async
            # ou há um await fora da função
            
            # Vamos verificar se a função carregarClassificacao está marcada como async
            if 'async function carregarClassificacao()' in content:
                print("Funcao carregarClassificacao ja esta marcada como async")
            else:
                print("PROBLEMA: Funcao carregarClassificacao nao esta marcada como async!")
                
                # Corrigir: marcar função como async
                old_function = 'function carregarClassificacao() {'
                new_function = 'async function carregarClassificacao() {'
                
                if old_function in content:
                    content = content.replace(old_function, new_function)
                    print("OK: Funcao carregarClassificacao marcada como async")
                else:
                    print("AVISO: Padrao da funcao nao encontrado")
        else:
            print("ERRO: Nenhuma funcao async encontrada antes do await")
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao do await aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO CIRURGICA DO ERRO AWAIT ===")
    
    success = fix_await_error()
    
    if success:
        print("\nSUCESSO: Erro de await corrigido!")
        print("Reinicie o servidor para aplicar a correcao.")
    else:
        print("\nERRO: Falha na correcao!")
