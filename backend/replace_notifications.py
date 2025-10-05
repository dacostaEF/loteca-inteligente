#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remover funções de notificações do HTML e adicionar referência externa
"""

def replace_notifications_with_reference():
    """Substituir funções por referência externa"""
    print("Substituindo funções por referência externa...")
    
    # Ler arquivo admin_interface.html
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Funções de mensagens para remover
    notifications_functions = '''        // === SISTEMA DE MENSAGENS ===
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
    
    # Referência externa
    external_reference = '''        <!-- Sistema de Mensagens (externo) -->
        <script src="{{ url_for('static', filename='js/ui/notifications.js') }}"></script>'''
    
    # Remover funções e adicionar referência
    if notifications_functions in content:
        content = content.replace(notifications_functions, external_reference)
        print("OK: Funções de notificações removidas e referência adicionada")
    else:
        print("AVISO: Funções de notificações não encontradas")
        return False
    
    # Salvar arquivo modificado
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Substituição aplicada!")
    return True

if __name__ == "__main__":
    print("=== SUBSTITUIÇÃO POR REFERÊNCIA EXTERNA ===")
    
    success = replace_notifications_with_reference()
    
    if success:
        print("\nSUCESSO: Referência externa adicionada!")
        print("Funções movidas para: backend/static/js/ui/notifications.js")
    else:
        print("\nERRO: Falha na substituição!")
