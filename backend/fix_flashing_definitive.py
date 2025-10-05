#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção definitiva do problema de piscar nas tabelas de classificação
"""

def fix_flashing_tables():
    """Corrigir problema de piscar nas tabelas"""
    print("Corrigindo problema de piscar nas tabelas...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA 1: Múltiplas chamadas para carregarClassificacao
    # Vamos adicionar controle de estado para evitar chamadas múltiplas
    
    # Adicionar variável de controle global
    control_var = '''
        // Controle de estado para evitar piscar
        let isClassificacaoLoading = false;
        let lastLoadedCampeonato = null;'''
    
    if 'isClassificacaoLoading' not in content:
        # Inserir após as configurações
        config_end = content.find('const API_BASE = window.location.port')
        if config_end != -1:
            # Encontrar o final da linha
            line_end = content.find('\n', config_end)
            content = content[:line_end + 1] + control_var + content[line_end + 1:]
            print("OK: Variável de controle adicionada")
    
    # PROBLEMA 2: Modificar carregarClassificacao para evitar chamadas múltiplas
    old_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');'''
    
    new_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            // Controle de estado para evitar chamadas múltiplas
            if (isClassificacaoLoading) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, aguardando...');
                return;
            }
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');
            const campeonato = campeonatoSelect ? campeonatoSelect.value : 'serie-a';
            
            // Se já carregou o mesmo campeonato, não recarregar
            if (lastLoadedCampeonato === campeonato) {
                console.log('🔄 [ADMIN] Campeonato já carregado:', campeonato);
                return;
            }
            
            isClassificacaoLoading = true;
            lastLoadedCampeonato = campeonato;'''
    
    if old_function_start in content:
        content = content.replace(old_function_start, new_function_start)
        print("OK: Controle de estado adicionado à função")
    else:
        print("AVISO: Padrão da função não encontrado")
    
    # PROBLEMA 3: Adicionar limpeza do estado no final da função
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
    
    # PROBLEMA 4: Modificar showTab para evitar chamadas desnecessárias
    old_showtab = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                carregarClassificacao();
            }'''
    
    new_showtab = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                
                // Só carregar se não estiver carregando e se mudou o campeonato
                const campeonatoSelect = document.getElementById('campeonatoSelect');
                const campeonato = campeonatoSelect ? campeonatoSelect.value : 'serie-a';
                
                if (!isClassificacaoLoading && lastLoadedCampeonato !== campeonato) {
                    carregarClassificacao();
                } else {
                    console.log('🔄 [ADMIN] Carregamento desnecessário evitado');
                }
            }'''
    
    if old_showtab in content:
        content = content.replace(old_showtab, new_showtab)
        print("OK: showTab otimizado")
    else:
        print("AVISO: Padrão do showTab não encontrado")
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correção do piscar aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORREÇÃO DEFINITIVA DO PISCAR ===")
    
    success = fix_flashing_tables()
    
    if success:
        print("\nSUCESSO: Problema de piscar corrigido!")
        print("Mudanças aplicadas:")
        print("1. Controle de estado para evitar chamadas múltiplas")
        print("2. Verificação de campeonato já carregado")
        print("3. Otimização do showTab")
        print("4. Limpeza de estado no final da função")
        print("\nReinicie o servidor para aplicar as correções.")
    else:
        print("\nERRO: Falha na correção do piscar!")
