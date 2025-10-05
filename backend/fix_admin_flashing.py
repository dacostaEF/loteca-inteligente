#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o problema de piscar na Central Admin
"""

def fix_admin_flashing():
    """Corrigir problema de piscar na Central Admin"""
    print("Corrigindo problema de piscar na Central Admin...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar a função carregarClassificacao
    start_pattern = 'async function carregarClassificacao() {'
    start_pos = content.find(start_pattern)
    
    if start_pos == -1:
        print("ERRO: Funcao carregarClassificacao nao encontrada!")
        return False
    
    # Encontrar o fim da função (próxima função)
    end_patterns = [
        'async function ',
        'function ',
        '// ==='
    ]
    
    end_pos = len(content)
    for pattern in end_patterns:
        pos = content.find(pattern, start_pos + 1)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    
    # Extrair função atual
    function_content = content[start_pos:end_pos]
    
    # Verificar se já tem a correção
    if 'loadingDebounce' in function_content:
        print("AVISO: Correcao ja aplicada!")
        return True
    
    # Adicionar variável de controle de loading
    new_function = function_content.replace(
        'async function carregarClassificacao() {',
        '''async function carregarClassificacao() {
            // Evitar múltiplos carregamentos simultâneos
            if (window.loadingDebounce) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.loadingDebounce = true;'''
    )
    
    # Adicionar limpeza da variável no final
    new_function = new_function.replace(
        '} catch (error) {',
        '''} catch (error) {
            window.loadingDebounce = false;'''
    )
    
    # Adicionar limpeza no finally
    if '} finally {' in new_function:
        new_function = new_function.replace(
            '} finally {',
            '''} finally {
            window.loadingDebounce = false;'''
        )
    else:
        # Adicionar finally se não existir
        new_function = new_function.replace(
            '        }',
            '''        } finally {
            window.loadingDebounce = false;
        }'''
        )
    
    # Substituir função no arquivo
    new_content = content[:start_pos] + new_function + content[end_pos:]
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Correcao aplicada com sucesso!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DO PROBLEMA DE PISCAR ===")
    
    success = fix_admin_flashing()
    
    if success:
        print("\nSUCESSO: Problema de piscar corrigido!")
        print("Reinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
