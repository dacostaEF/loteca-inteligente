#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrair Sistema de Mensagens para arquivo externo
"""

def extract_notifications():
    """Extrair funções de notificações"""
    print("Extraindo Sistema de Mensagens...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Funções de mensagens para extrair
    notifications_code = '''// === SISTEMA DE MENSAGENS ===
function mostrarSucesso(mensagem) {
    mostrarNotificacao(`✅ ${mensagem}`, 'success');
}

function mostrarErro(mensagem) {
    mostrarNotificacao(`❌ ${mensagem}`, 'error');
}

function mostrarNotificacao(mensagem, tipo = 'info') {
    // Remover notificações anteriores
    const notificacoesExistentes = document.querySelectorAll('.notification');
    notificacoesExistentes.forEach(n => n.remove());
    
    // Criar nova notificação
    const notification = document.createElement('div');
    notification.className = `notification ${tipo}`;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span>${mensagem}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; font-size: 18px; cursor: pointer; padding: 0; margin-left: 10px;">×</button>
        </div>
    `;
    
    // Adicionar ao body
    document.body.appendChild(notification);
    
    // Mostrar com animação
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}'''
    
    # Criar diretório se não existir
    import os
    os.makedirs('backend/static/js/ui', exist_ok=True)
    
    # Salvar arquivo de notificações
    with open('backend/static/js/ui/notifications.js', 'w', encoding='utf-8') as f:
        f.write(notifications_code)
    
    print("Arquivo notifications.js criado!")
    return True

if __name__ == "__main__":
    print("=== EXTRAÇÃO DO SISTEMA DE MENSAGENS ===")
    
    success = extract_notifications()
    
    if success:
        print("\nSUCESSO: Sistema de mensagens extraído!")
        print("Arquivo: backend/static/js/ui/notifications.js")
    else:
        print("\nERRO: Falha na extração!")
