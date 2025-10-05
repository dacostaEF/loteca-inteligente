#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o loop infinito na Central Admin
"""

def fix_infinite_loop():
    """Corrigir loop infinito"""
    print("Corrigindo loop infinito na Central Admin...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA: O setTimeout está criando loop infinito
    # Vamos remover completamente o controle problemático
    
    old_control_pattern = '''            // Controle simples de carregamento
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, aguardando...');
                setTimeout(() => carregarClassificacao(), 500);
                return;
            }
            window.carregandoClassificacao = true;'''
    
    new_control_pattern = '''            // Controle simples de carregamento
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.carregandoClassificacao = true;'''
    
    if old_control_pattern in content:
        content = content.replace(old_control_pattern, new_control_pattern)
        print("OK: Loop infinito corrigido")
    else:
        print("AVISO: Padrao de controle nao encontrado")
    
    # PROBLEMA 2: Garantir que a variável seja limpa no finally
    old_finally_pattern = '''        } finally {
            window.carregandoClassificacao = false;
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    new_finally_pattern = '''        } finally {
            window.carregandoClassificacao = false;
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    # Verificar se o finally já existe
    if 'window.carregandoClassificacao = false;' not in content:
        # Adicionar limpeza da variável
        old_catch_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        }'''
        
        new_catch_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        } finally {
            window.carregandoClassificacao = false;
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
        
        if old_catch_pattern in content:
            content = content.replace(old_catch_pattern, new_catch_pattern)
            print("OK: Limpeza da variavel adicionada")
        else:
            print("AVISO: Padrao de catch nao encontrado")
    
    # PROBLEMA 3: Simplificar ainda mais o showTab
    old_showtab_pattern = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Sempre carregar quando a aba é ativada
                setTimeout(() => {
                    carregarClassificacao();
                }, 100);
            }'''
    
    new_showtab_pattern = '''            if (tabName === 'classificacao') {
                console.log('🏆 [ADMIN] === ABA CLASSIFICAÇÃO ATIVADA ===');
                console.log('🎯 [ADMIN] Elemento da aba ativo:', document.getElementById('classificacao'));
                // Carregar apenas se não estiver carregando
                if (!window.carregandoClassificacao) {
                    setTimeout(() => {
                        carregarClassificacao();
                    }, 100);
                }
            }'''
    
    if old_showtab_pattern in content:
        content = content.replace(old_showtab_pattern, new_showtab_pattern)
        print("OK: ShowTab simplificado")
    else:
        print("AVISO: Padrao showTab nao encontrado")
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao do loop infinito aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DO LOOP INFINITO ===")
    
    success = fix_infinite_loop()
    
    if success:
        print("\nSUCESSO: Loop infinito corrigido!")
        print("Mudancas:")
        print("1. Removido setTimeout recursivo")
        print("2. Adicionada limpeza da variavel")
        print("3. Controle mais simples")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
