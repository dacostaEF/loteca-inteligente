#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o problema da variável não ser limpa
"""

def fix_variable_cleanup():
    """Corrigir limpeza da variável de controle"""
    print("Corrigindo limpeza da variavel de controle...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA: A variável não está sendo limpa corretamente
    # Vamos encontrar onde ela deveria ser limpa e garantir que seja
    
    # Primeiro, vamos verificar se existe o finally
    if 'window.carregandoClassificacao = false;' not in content:
        print("ERRO: Limpeza da variavel nao encontrada!")
        
        # Adicionar limpeza no final da função
        old_end_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        }'''
        
        new_end_pattern = '''        } catch (error) {
            console.error('💥 [ADMIN] Erro na requisição:', error);
            console.error('📄 [ADMIN] Error stack:', error.stack);
        } finally {
            window.carregandoClassificacao = false;
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
        
        if old_end_pattern in content:
            content = content.replace(old_end_pattern, new_end_pattern)
            print("OK: Limpeza da variavel adicionada")
        else:
            print("AVISO: Padrao de catch nao encontrado")
    
    # PROBLEMA 2: Adicionar limpeza também no sucesso
    success_pattern = '''                console.log('📋 [ADMIN] Dados JSON recebidos:');
                console.log('   - success:', data.success);
                console.log('   - total:', data.total);
                console.log('   - campeonato:', data.campeonato);
                
                if (data.success && data.classificacao) {
                    console.log('✅ [ADMIN] Dados válidos recebidos!');
                    renderizarClassificacao(data.classificacao);
                } else {
                    console.warn('⚠️ [ADMIN] Dados inválidos ou vazios');
                    if (bodyEl) {
                        bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Erro ao carregar dados</td></tr>';
                    }
                }'''
    
    new_success_pattern = '''                console.log('📋 [ADMIN] Dados JSON recebidos:');
                console.log('   - success:', data.success);
                console.log('   - total:', data.total);
                console.log('   - campeonato:', data.campeonato);
                
                if (data.success && data.classificacao) {
                    console.log('✅ [ADMIN] Dados válidos recebidos!');
                    renderizarClassificacao(data.classificacao);
                } else {
                    console.warn('⚠️ [ADMIN] Dados inválidos ou vazios');
                    if (bodyEl) {
                        bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Erro ao carregar dados</td></tr>';
                    }
                }
                
                // Limpar variável de controle após sucesso
                window.carregandoClassificacao = false;'''
    
    if success_pattern in content:
        content = content.replace(success_pattern, new_success_pattern)
        print("OK: Limpeza adicionada no sucesso")
    else:
        print("AVISO: Padrao de sucesso nao encontrado")
    
    # PROBLEMA 3: Simplificar ainda mais o controle
    old_control_pattern = '''            // Controle simples de carregamento
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.carregandoClassificacao = true;'''
    
    new_control_pattern = '''            // Controle simples de carregamento
            if (window.carregandoClassificacao) {
                console.log('🔄 [ADMIN] Carregamento já em andamento, ignorando...');
                return;
            }
            window.carregandoClassificacao = true;
            console.log('🔄 [ADMIN] Iniciando carregamento...');'''
    
    if old_control_pattern in content:
        content = content.replace(old_control_pattern, new_control_pattern)
        print("OK: Controle melhorado")
    else:
        print("AVISO: Padrao de controle nao encontrado")
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Correcao da limpeza da variavel aplicada!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DA LIMPEZA DA VARIAVEL ===")
    
    success = fix_variable_cleanup()
    
    if success:
        print("\nSUCESSO: Limpeza da variavel corrigida!")
        print("Mudancas:")
        print("1. Limpeza no finally")
        print("2. Limpeza no sucesso")
        print("3. Log melhorado")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
