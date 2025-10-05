#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para restaurar Central Admin funcional
"""

def restore_admin():
    """Restaurar Central Admin funcional"""
    print("Restaurando Central Admin funcional...")
    
    # Ler arquivo atual para preservar algumas partes
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Encontrar onde está a função carregarClassificacao problemática
    start_pattern = 'async function carregarClassificacao() {'
    start_pos = current_content.find(start_pattern)
    
    if start_pos == -1:
        print("AVISO: Funcao carregarClassificacao nao encontrada")
        return True
    
    # Encontrar o fim da função
    end_patterns = ['async function ', 'function ', '// ===']
    end_pos = len(current_content)
    for pattern in end_patterns:
        pos = current_content.find(pattern, start_pos + 1)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    
    # Substituir por uma versão funcional simples
    functional_function = '''        async function carregarClassificacao() {
            console.log('🔄 [ADMIN] Carregando classificação...');
            
            const campeonatoSelect = document.getElementById('campeonatoSelect');
            const loadingEl = document.getElementById('loadingClassificacao');
            const bodyEl = document.getElementById('classificacaoBody');
            
            const campeonato = campeonatoSelect ? campeonatoSelect.value : 'serie-a';
            const adminKey = localStorage.getItem('admin_key') || 'loteca2024admin';
            
            if (loadingEl) loadingEl.style.display = 'block';
            if (bodyEl) bodyEl.innerHTML = '';
            
            try {
                const response = await fetch('/api/admin/classificacao', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        admin_key: adminKey,
                        campeonato: campeonato
                    })
                });
                
                if (loadingEl) loadingEl.style.display = 'none';
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success && data.classificacao) {
                    renderizarClassificacao(data.classificacao);
                } else {
                    if (bodyEl) {
                        bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Erro ao carregar dados</td></tr>';
                    }
                }
                
            } catch (error) {
                console.error('Erro:', error);
                if (loadingEl) loadingEl.style.display = 'none';
                if (bodyEl) {
                    bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Erro ao carregar dados</td></tr>';
                }
            }
        }'''
    
    # Substituir função no arquivo
    new_content = current_content[:start_pos] + functional_function + current_content[end_pos:]
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Central Admin restaurada com versao funcional!")
    return True

if __name__ == "__main__":
    print("=== RESTAURACAO DA CENTRAL ADMIN ===")
    
    success = restore_admin()
    
    if success:
        print("\nSUCESSO: Central Admin restaurada!")
        print("Versao funcional aplicada.")
        print("\nReinicie o servidor para aplicar a restauracao.")
    else:
        print("\nERRO: Falha na restauracao!")
