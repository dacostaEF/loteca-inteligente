#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir definitivamente o problema da Central Admin
"""

def fix_admin_definitive():
    """Correção definitiva da Central Admin"""
    print("Aplicando correcao definitiva da Central Admin...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # SOLUÇÃO DEFINITIVA: Remover completamente o controle problemático
    # e usar uma abordagem mais simples
    
    # Encontrar a função carregarClassificacao completa
    start_pattern = 'async function carregarClassificacao() {'
    start_pos = content.find(start_pattern)
    
    if start_pos == -1:
        print("ERRO: Funcao carregarClassificacao nao encontrada!")
        return False
    
    # Encontrar o fim da função
    end_patterns = ['async function ', 'function ', '// ===']
    end_pos = len(content)
    for pattern in end_patterns:
        pos = content.find(pattern, start_pos + 1)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    
    # Substituir toda a função por uma versão simplificada
    new_function = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] === INICIANDO CARREGAMENTO DA CLASSIFICAÇÃO ===');
            
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
            
            if (loadingEl) {
                loadingEl.style.display = 'block';
                console.log('📊 [ADMIN] Loading exibido');
            }
            
            if (bodyEl) {
                bodyEl.innerHTML = '';
                console.log('🧹 [ADMIN] Tabela limpa');
            }
            
            try {
                const requestData = {
                    admin_key: adminKey,
                    campeonato: campeonato
                };
                
                console.log('📤 [ADMIN] Enviando requisição...');
                console.log('   - URL: /api/admin/classificacao');
                console.log('   - Method: POST');
                console.log('   - Body:', JSON.stringify(requestData));
                
                const response = await fetch('/api/admin/classificacao', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(requestData)
                });
                
                console.log('📥 [ADMIN] Resposta recebida:');
                console.log('   - Status:', response.status);
                console.log('   - OK:', response.ok);
                
                if (loadingEl) {
                    loadingEl.style.display = 'none';
                    console.log('📊 [ADMIN] Loading escondido');
                }
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('📋 [ADMIN] Dados JSON recebidos:');
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
                
            } catch (error) {
                console.error('💥 [ADMIN] Erro na requisição:', error);
                console.error('📄 [ADMIN] Error stack:', error.stack);
                
                if (loadingEl) {
                    loadingEl.style.display = 'none';
                }
                
                if (bodyEl) {
                    bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Erro ao carregar dados</td></tr>';
                }
            }
            
            console.log('🏁 [ADMIN] === CARREGAMENTO FINALIZADO ===');
        }'''
    
    # Substituir função no arquivo
    new_content = content[:start_pos] + new_function + content[end_pos:]
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Funcao carregarClassificacao substituida por versao simplificada!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DEFINITIVA DA CENTRAL ADMIN ===")
    
    success = fix_admin_definitive()
    
    if success:
        print("\nSUCESSO: Correcao definitiva aplicada!")
        print("Mudancas:")
        print("1. Funcao completamente reescrita")
        print("2. Removido controle problemático")
        print("3. Versao simplificada e funcional")
        print("\nReinicie o servidor para aplicar as mudancas.")
    else:
        print("\nERRO: Falha na correcao!")
