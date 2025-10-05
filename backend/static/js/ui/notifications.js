// === SISTEMA DE MENSAGENS ===
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
}