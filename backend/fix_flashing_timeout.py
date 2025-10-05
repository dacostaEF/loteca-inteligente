#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção cirúrgica do piscar - remover setTimeout duplicados
"""

def fix_flashing_timeout():
    """Corrigir setTimeout duplicados que causam piscar"""
    print("Corrigindo setTimeout duplicados que causam piscar...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA 1: setTimeout na linha 2792-2794
    old_pattern1 = '''                // Carregar apenas se não estiver carregando
                if (!window.carregandoClassificacao) {
                    setTimeout(() => {
                        carregarClassificacao();
                    }, 100);
                }'''
    
    new_pattern1 = '''                // Carregar diretamente sem setTimeout
                if (!window.carregandoClassificacao) {
                    carregarClassificacao();
                }'''
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        print("OK: Problema 1 corrigido - removido setTimeout de 100ms")
    else:
        print("AVISO: Padrão 1 não encontrado")
    
    # PROBLEMA 2: setTimeout na linha 3194-3196
    old_pattern2 = '''            // Carregar nova classificação
            setTimeout(() => {
                carregarClassificacao();
            }, 300);'''
    
    new_pattern2 = '''            // Carregar nova classificação diretamente
            carregarClassificacao();'''
    
    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
        print("OK: Problema 2 corrigido - removido setTimeout de 300ms")
    else:
        print("AVISO: Padrão 2 não encontrado")
    
    # PROBLEMA 3: Adicionar controle de estado mais robusto
    control_var = '''
        // Controle de estado para evitar piscar
        let isClassificacaoLoading = false;'''
    
    if 'isClassificacaoLoading' not in content:
        # Inserir após as configurações
        config_end = content.find('const API_BASE = window.location.port')
        if config_end != -1:
            line_end = content.find('\n', config_end)
            content = content[:line_end + 1] + control_var + content[line_end + 1:]
            print("OK: Variável de controle adicionada")
    
    # PROBLEMA 4: Modificar carregarClassificacao para usar controle de estado
    old_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');'''
    
    new_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            // Controle de estado para evitar chamadas múltiplas
            if (isClassificacaoLoading) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            isClassificacaoLoading = true;
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');'''
    
    if old_function_start in content:
        content = content.replace(old_function_start, new_function_start)
        print("OK: Controle de estado adicionado à função")
    else:
        print("AVISO: Padrão da função não encontrado")
    
    # PROBLEMA 5: Adicionar limpeza do estado no final da função
    old_function_end = '''            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    new_function_end = '''            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
            
            // Limpar estado de carregamento
            isClassificacaoLoading = false;
        }'''
    
    if old_function_end in content:
        content = content.replace(old_function_end, new_function_end)
        print("OK: Limpeza de estado adicionada")
    else:
        print("AVISO: Padrão do final da função não encontrado")
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correção do piscar aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORREÇÃO CIRÚRGICA DO PISCAR ===")
    
    success = fix_flashing_timeout()
    
    if success:
        print("\nSUCESSO: setTimeout duplicados corrigidos!")
        print("Mudanças aplicadas:")
        print("1. Removido setTimeout de 100ms")
        print("2. Removido setTimeout de 300ms")
        print("3. Adicionado controle de estado robusto")
        print("4. Função carregarClassificacao otimizada")
        print("\nReinicie o servidor para aplicar as correções.")
    else:
        print("\nERRO: Falha na correção do piscar!")
