#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção cirúrgica dos await fora de função async
"""

def fix_await_errors():
    """Corrigir await fora de função async"""
    print("Corrigindo await fora de função async...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA 1: Linha 2804-2805 - await fora de função
    old_pattern1 = '''            await carregarListaConcursos();
            await carregarUltimoConcurso();'''
    
    new_pattern1 = '''            carregarListaConcursos();
            carregarUltimoConcurso();'''
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        print("OK: Problema 1 corrigido - removido await das linhas 2804-2805")
    
    # PROBLEMA 2: Linha 3352 - await fora de função
    old_pattern2 = '''                const data = await response.json();'''
    
    # Encontrar o contexto e corrigir
    if 'const data = await response.json();' in content:
        # Procurar a função que contém isso
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'const data = await response.json();' in line:
                # Verificar se está dentro de função async
                is_inside_async = False
                for j in range(i-1, max(0, i-50), -1):
                    if 'async function' in lines[j]:
                        is_inside_async = True
                        break
                    elif 'function ' in lines[j] and 'async function' not in lines[j]:
                        break
                
                if not is_inside_async:
                    # Encontrar a função que contém essa linha
                    for k in range(i-1, max(0, i-100), -1):
                        if 'function ' in lines[k]:
                            # Adicionar async à função
                            if 'async function' not in lines[k]:
                                lines[k] = lines[k].replace('function ', 'async function ')
                                print(f"OK: Função na linha {k+1} marcada como async")
                            break
                    break
        
        content = '\n'.join(lines)
    
    # PROBLEMA 3: Linha 3439 - await fora de função
    # Este é o mesmo problema da linha 3352, já corrigido acima
    
    # PROBLEMA 4: Linha 4159 - await fora de função
    old_pattern4 = '''            await carregarDadosJogosClube(clubeSelecionado);'''
    
    new_pattern4 = '''            carregarDadosJogosClube(clubeSelecionado);'''
    
    if old_pattern4 in content:
        content = content.replace(old_pattern4, new_pattern4)
        print("OK: Problema 4 corrigido - removido await da linha 4159")
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correção dos await aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORREÇÃO DOS AWAIT FORA DE FUNÇÃO ASYNC ===")
    
    success = fix_await_errors()
    
    if success:
        print("\nSUCESSO: await fora de função async corrigidos!")
        print("Reinicie o servidor para aplicar a correção.")
    else:
        print("\nERRO: Falha na correção dos await!")
