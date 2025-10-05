#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o problema de não carregar tabelas
"""

def fix_table_loading():
    """Corrigir problema de não carregar tabelas"""
    print("Corrigindo problema de nao carregar tabelas...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA: A condição está muito restritiva
    # Vamos simplificar e garantir que sempre carregue
    
    old_showtab_pattern = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Carregar apenas se tabela estiver vazia
                const bodyEl = document.getElementById('classificacaoBody');
                if (bodyEl && bodyEl.children.length === 0) {
                    setTimeout(() => {
                        carregarClassificacao();
                    }, 100);
                }
            }'''
    
    new_showtab_pattern = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Sempre carregar quando a aba é ativada
                setTimeout(() => {
                    carregarClassificacao();
                }, 100);
            }'''
    
    if old_showtab_pattern in content:
        content = content.replace(old_showtab_pattern, new_showtab_pattern)
        print("OK: Condicao de carregamento simplificada")
    else:
        print("AVISO: Padrao showTab nao encontrado")
    
    # PROBLEMA 2: Remover a condição muito restritiva do loading
    old_loading_pattern = '''            // MOSTRAR LOADING APENAS SE TABELA ESTIVER VAZIA
            if (loadingEl && bodyEl && bodyEl.children.length === 0) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido (tabela vazia)');
            } else if (bodyEl && bodyEl.children.length > 0) {
                console.log('📊 [ADMIN] Mantendo dados existentes, sem loading');
            }'''
    
    new_loading_pattern = '''            // MOSTRAR LOADING SEMPRE
            if (loadingEl) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido');
            }
            
            if (bodyEl) {
                bodyEl.innerHTML = '';
                console.log('🧹 [ADMIN] Tabela limpa');
            }'''
    
    if old_loading_pattern in content:
        content = content.replace(old_loading_pattern, new_loading_pattern)
        print("OK: Condicao de loading simplificada")
    else:
        print("AVISO: Padrao de loading nao encontrado")
    
    # PROBLEMA 3: Simplificar o controle de carregamento
    old_control_pattern = '''            // VERIFICAR SE JÁ ESTÁ CARREGANDO
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.carregandoClassificacao = true;'''
    
    new_control_pattern = '''            // Controle simples de carregamento
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, aguardando...');
                setTimeout(() => carregarClassificacao(), 500);
                return;
            }
            window.carregandoClassificacao = true;'''
    
    if old_control_pattern in content:
        content = content.replace(old_control_pattern, new_control_pattern)
        print("OK: Controle de carregamento simplificado")
    else:
        print("AVISO: Padrao de controle nao encontrado")
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao aplicada com sucesso!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DO PROBLEMA DE NAO CARREGAR TABELAS ===")
    
    success = fix_table_loading()
    
    if success:
        print("\nSUCESSO: Correcao aplicada!")
        print("Mudancas:")
        print("1. Sempre carregar quando aba ativada")
        print("2. Loading sempre visivel")
        print("3. Controle de carregamento simplificado")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
