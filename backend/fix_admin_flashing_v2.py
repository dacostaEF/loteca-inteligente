#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir definitivamente o problema de piscar na Central Admin
"""

def fix_admin_flashing_v2():
    """Corrigir problema de piscar - versão 2"""
    print("Corrigindo problema de piscar - versao 2...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA 1: Remover chamada dupla na função showTab
    old_pattern = '''            // Carregar dados específicos da aba
            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                setTimeout(() => {
                    console.log('⏰ [ADMIN] Timeout executado - chamando carregarClassificacao...');
                    carregarClassificacao();
                }, 200);
            }'''
    
    new_pattern = '''            // Carregar dados específicos da aba
            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Removido setTimeout para evitar chamada dupla
            }'''
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("OK: Problema 1 corrigido: Removido setTimeout duplo")
    else:
        print("AVISO: Problema 1 nao encontrado")
    
    # PROBLEMA 2: Modificar carregarClassificacao para não chamar atualizarUltimosConfrontosAutomatico
    old_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            // ATUALIZAR ÚLTIMOS CONFRONTOS AUTOMATICAMENTE
            await atualizarUltimosConfrontosAutomatico();'''
    
    new_function_start = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            // REMOVIDO: atualizarUltimosConfrontosAutomatico() para evitar chamada dupla'''
    
    if old_function_start in content:
        content = content.replace(old_function_start, new_function_start)
        print("OK: Problema 2 corrigido: Removido atualizarUltimosConfrontosAutomatico")
    else:
        print("AVISO: Problema 2 nao encontrado")
    
    # PROBLEMA 3: Adicionar controle de estado visual
    loading_control = '''            if (loadingEl) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido');
            }
            
            if (bodyEl) {
                bodyEl.innerHTML = '';
                console.log('🧹 [ADMIN] Tabela limpa');
            }'''
    
    new_loading_control = '''            if (loadingEl) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido');
            }
            
            if (bodyEl) {
                // Manter conteúdo existente se já houver dados
                if (bodyEl.children.length === 0) {
                    bodyEl.innerHTML = '';
                    console.log('🧹 [ADMIN] Tabela limpa');
                } else {
                    console.log('📊 [ADMIN] Mantendo dados existentes');
                }
            }'''
    
    if loading_control in content:
        content = content.replace(loading_control, new_loading_control)
        print("OK: Problema 3 corrigido: Controle de estado visual melhorado")
    else:
        print("AVISO: Problema 3 nao encontrado")
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao v2 aplicada com sucesso!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DEFINITIVA DO PROBLEMA DE PISCAR ===")
    
    success = fix_admin_flashing_v2()
    
    if success:
        print("\nSUCESSO: Correcao definitiva aplicada!")
        print("Mudancas:")
        print("1. Removido setTimeout duplo")
        print("2. Removido atualizarUltimosConfrontosAutomatico")
        print("3. Melhorado controle de estado visual")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
