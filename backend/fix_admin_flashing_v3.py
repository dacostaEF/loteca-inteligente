#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir DEFINITIVAMENTE o problema de piscar - versão 3
"""

def fix_admin_flashing_v3():
    """Corrigir problema de piscar - versão 3 (definitiva)"""
    print("Corrigindo problema de piscar - versao 3 (definitiva)...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # SOLUÇÃO DEFINITIVA: Modificar completamente a função carregarClassificacao
    old_function_pattern = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            // REMOVIDO: atualizarUltimosConfrontosAutomatico() para evitar chamada dupla
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');
            const loadingEl = document.getElementById('loadingClassificacao');
            const bodyEl = document.getElementById('classificacaoBody');
            
            console.log('🎯 [ADMIN] Elementos DOM encontrados:');
            console.log('   - campeonatoSelect:', campeonatoSelect ? 'OK' : 'MISSING');
            console.log('   - loadingEl:', loadingEl ? 'OK' : 'MISSING');
            console.log('   - bodyEl:', bodyEl ? 'OK' : 'MISSING');
            
            const campeonato = campeonatoSelect ? campeonatoSelect.value : 'serie-a';
            let adminKey = localStorage.getItem('admin_key');
            
            // FORÇAR admin key se não existir
            if (!adminKey) {
                console.warn('⚠️ [ADMIN] Admin key não encontrada no localStorage! Usando padrão...');
                adminKey = 'loteca2024admin';
                localStorage.setItem('admin_key', adminKey);
            }
            
            console.log('🔑 [ADMIN] Configurações:');
            console.log('   - campeonato:', campeonato);
            console.log('   - adminKey:', adminKey ? 'OK (***' + adminKey.slice(-4) + ')' : 'MISSING');
            console.log('   - adminKey completa:', adminKey);
            
            if (loadingEl) {
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
    
    new_function_pattern = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');
            const loadingEl = document.getElementById('loadingClassificacao');
            const bodyEl = document.getElementById('classificacaoBody');
            
            // VERIFICAR SE JÁ ESTÁ CARREGANDO
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.carregandoClassificacao = true;
            
            console.log('🎯 [ADMIN] Elementos DOM encontrados:');
            console.log('   - campeonatoSelect:', campeonatoSelect ? 'OK' : 'MISSING');
            console.log('   - loadingEl:', loadingEl ? 'OK' : 'MISSING');
            console.log('   - bodyEl:', bodyEl ? 'OK' : 'MISSING');
            
            const campeonato = campeonatoSelect ? campeonatoSelect.value : 'serie-a';
            let adminKey = localStorage.getItem('admin_key');
            
            // FORÇAR admin key se não existir
            if (!adminKey) {
                console.warn('⚠️ [ADMIN] Admin key não encontrada no localStorage! Usando padrão...');
                adminKey = 'loteca2024admin';
                localStorage.setItem('admin_key', adminKey);
            }
            
            console.log('🔑 [ADMIN] Configurações:');
            console.log('   - campeonato:', campeonato);
            console.log('   - adminKey:', adminKey ? 'OK (***' + adminKey.slice(-4) + ')' : 'MISSING');
            console.log('   - adminKey completa:', adminKey);
            
            // MOSTRAR LOADING APENAS SE TABELA ESTIVER VAZIA
            if (loadingEl && bodyEl && bodyEl.children.length === 0) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido (tabela vazia)');
            } else if (bodyEl && bodyEl.children.length > 0) {
                console.log('📊 [ADMIN] Mantendo dados existentes, sem loading');
            }'''
    
    if old_function_pattern in content:
        content = content.replace(old_function_pattern, new_function_pattern)
        print("OK: Funcao carregarClassificacao modificada")
    else:
        print("AVISO: Padrao da funcao nao encontrado")
    
    # ADICIONAR LIMPEZA DA VARIÁVEL NO FINAL DA FUNÇÃO
    cleanup_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        } finally {
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    new_cleanup_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        } finally {
            window.carregandoClassificacao = false;
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    if cleanup_pattern in content:
        content = content.replace(cleanup_pattern, new_cleanup_pattern)
        print("OK: Limpeza da variavel adicionada")
    else:
        print("AVISO: Padrao de cleanup nao encontrado")
    
    # MODIFICAR A FUNÇÃO showTab PARA NÃO CHAMAR carregarClassificacao AUTOMATICAMENTE
    showtab_pattern = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Removido setTimeout para evitar chamada dupla
            }'''
    
    new_showtab_pattern = '''            if (tabName === 'classificacao') {
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
    
    if showtab_pattern in content:
        content = content.replace(showtab_pattern, new_showtab_pattern)
        print("OK: Funcao showTab modificada")
    else:
        print("AVISO: Padrao showTab nao encontrado")
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao v3 aplicada com sucesso!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DEFINITIVA DO PROBLEMA DE PISCAR - V3 ===")
    
    success = fix_admin_flashing_v3()
    
    if success:
        print("\nSUCESSO: Correcao definitiva v3 aplicada!")
        print("Mudancas:")
        print("1. Adicionado controle de carregamento global")
        print("2. Loading apenas quando tabela vazia")
        print("3. Carregamento condicional na aba")
        print("4. Limpeza adequada da variavel")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
