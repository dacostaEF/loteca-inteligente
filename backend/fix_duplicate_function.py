#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção cirúrgica da função duplicada carregarClassificacao
"""

def fix_duplicate_function():
    """Corrigir função duplicada carregarClassificacao"""
    print("Corrigindo função duplicada carregarClassificacao...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA: Função duplicada e malformada
    # Linha 3382: }function carregarClassificacao() {
    # Deve ser: } (fechar primeira função)
    # E remover a segunda função duplicada
    
    # Encontrar o problema
    problem_pattern = '}function carregarClassificacao() {'
    
    if problem_pattern in content:
        print("Problema encontrado!")
        
        # Encontrar onde termina a primeira função
        first_function_end = content.find('}function carregarClassificacao() {')
        
        # Encontrar onde termina a segunda função duplicada
        # Procurar pela próxima função ou fim do script
        second_function_start = first_function_end + len(problem_pattern)
        
        # Procurar o fim da segunda função (próxima função ou })
        next_function = content.find('function ', second_function_start)
        if next_function == -1:
            next_function = content.find('</script>', second_function_start)
        
        if next_function != -1:
            # Remover a segunda função duplicada
            content = content[:first_function_end + 1] + content[next_function:]
            print("OK: Segunda função duplicada removida")
        else:
            print("ERRO: Não foi possível encontrar o fim da segunda função")
            return False
    else:
        print("AVISO: Padrão do problema não encontrado")
        return False
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correção da função duplicada aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORREÇÃO DA FUNÇÃO DUPLICADA ===")
    
    success = fix_duplicate_function()
    
    if success:
        print("\nSUCESSO: Função duplicada corrigida!")
        print("Reinicie o servidor para aplicar a correção.")
    else:
        print("\nERRO: Falha na correção!")
