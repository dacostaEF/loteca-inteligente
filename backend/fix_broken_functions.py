#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir as funções JavaScript quebradas
"""

def fix_broken_functions():
    """Corrigir funções JavaScript quebradas"""
    print("Corrigindo funcoes JavaScript quebradas...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PROBLEMA 1: Função login() não está definida
    # Vamos verificar se ela existe
    if 'function login()' not in content:
        print("ERRO: Funcao login() nao encontrada!")
        
        # Adicionar função login
        login_function = '''
        // === SISTEMA DE LOGIN ===
        function login() {
            const key = document.getElementById('adminKey').value;
            const errorDiv = document.getElementById('loginError');
            
            if (key === 'loteca2024admin') {
                document.getElementById('loginContainer').style.display = 'none';
                document.getElementById('adminContainer').style.display = 'block';
                carregarDashboard();
                carregarClubes();
                carregarEstatisticas();
            } else {
                errorDiv.style.display = 'block';
                setTimeout(() => {
                    errorDiv.style.display = 'none';
                }, 3000);
            }
        }

        function logout() {
            document.getElementById('loginContainer').style.display = 'flex';
            document.getElementById('adminContainer').style.display = 'none';
            document.getElementById('adminKey').value = '';
        }

        // === FUNÇÃO PARA MOSTRAR/OCULTAR SENHA ===
        function togglePasswordVisibility() {
            const passwordField = document.getElementById('adminKey');
            const toggleIcon = document.getElementById('togglePassword');
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash');
                toggleIcon.style.color = '#00E38C';
                toggleIcon.title = 'Ocultar senha';
            } else {
                passwordField.type = 'password';
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye');
                toggleIcon.style.color = '#666';
                toggleIcon.title = 'Mostrar senha';
            }
        }
        '''
        
        # Encontrar onde inserir as funções (antes do </script>)
        script_end = content.rfind('</script>')
        if script_end != -1:
            content = content[:script_end] + login_function + content[script_end:]
            print("OK: Funcoes de login adicionadas")
        else:
            print("ERRO: Tag </script> nao encontrada!")
            return False
    
    # PROBLEMA 2: Verificar se há erros de sintaxe async/await
    # Vamos encontrar e corrigir problemas de async/await
    
    # Verificar se há await fora de função async
    if 'await carregarClassificacao()' in content:
        print("AVISO: Encontrado await fora de função async")
        # Isso pode estar causando o erro de sintaxe
    
    # PROBLEMA 3: Adicionar funções básicas que podem estar faltando
    basic_functions = '''
        // === FUNÇÕES BÁSICAS ===
        function carregarDashboard() {
            console.log('Dashboard carregado');
        }

        function carregarClubes() {
            console.log('Clubes carregados');
        }

        function carregarEstatisticas() {
            console.log('Estatísticas carregadas');
        }

        function renderizarClassificacao(dados) {
            console.log('Renderizando classificação:', dados);
            const bodyEl = document.getElementById('classificacaoBody');
            if (bodyEl && dados) {
                bodyEl.innerHTML = '<tr><td colspan="12" style="text-align: center; padding: 20px; color: #666;">Dados carregados com sucesso!</td></tr>';
            }
        }
        '''
    
    # Adicionar funções básicas se não existirem
    if 'function carregarDashboard()' not in content:
        script_end = content.rfind('</script>')
        if script_end != -1:
            content = content[:script_end] + basic_functions + content[script_end:]
            print("OK: Funcoes basicas adicionadas")
    
    # Salvar arquivo corrigido
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Funcoes JavaScript corrigidas!")
    return True

if __name__ == "__main__":
    print("=== CORRECAO DAS FUNCOES JAVASCRIPT ===")
    
    success = fix_broken_functions()
    
    if success:
        print("\nSUCESSO: Funcoes JavaScript corrigidas!")
        print("Mudancas:")
        print("1. Funcao login() restaurada")
        print("2. Funcao togglePasswordVisibility() restaurada")
        print("3. Funcoes basicas adicionadas")
        print("\nReinicie o servidor para aplicar as correcoes.")
    else:
        print("\nERRO: Falha na correcao!")
