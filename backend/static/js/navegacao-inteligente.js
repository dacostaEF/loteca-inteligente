/**
 * NAVEGAÇÃO INTELIGENTE ENTRE ABAS
 * Sistema para navegar automaticamente entre Otimizador e Análise Rápida
 */

class NavegacaoInteligente {
    constructor() {
        this.init();
    }

    init() {
        console.log('🚀 [NAVEGAÇÃO] Inicializando navegação inteligente...');
        this.setupEventListeners();
        this.setupHoverEffects();
    }

    setupEventListeners() {
        // Aguardar o carregamento da tabela de otimização
        setTimeout(() => {
            this.attachClickListeners();
        }, 1000);
    }

    attachClickListeners() {
        const optimizationRows = document.querySelectorAll('#optimization-tbody tr');
        
        optimizationRows.forEach((row, index) => {
            // Adicionar data-jogo para identificação
            row.setAttribute('data-jogo', index + 1);
            
            // Adicionar listener de clique
            row.addEventListener('click', (e) => {
                e.preventDefault();
                const jogoNumero = row.getAttribute('data-jogo');
                this.navegarParaAnalise(jogoNumero);
            });

            // Adicionar efeito de hover personalizado
            row.addEventListener('mouseenter', () => {
                this.showHoverEffect(row);
            });

            row.addEventListener('mouseleave', () => {
                this.hideHoverEffect(row);
            });
        });

        console.log(`✅ [NAVEGAÇÃO] ${optimizationRows.length} jogos configurados para navegação`);
    }

    showHoverEffect(row) {
        // Adicionar classe de hover personalizada
        row.classList.add('jogo-hover-active');
        
        // Adicionar tooltip de navegação
        const tooltip = document.createElement('div');
        tooltip.className = 'navegacao-tooltip';
        tooltip.innerHTML = '🔍 Clique para ver análise detalhada';
        row.appendChild(tooltip);
    }

    hideHoverEffect(row) {
        row.classList.remove('jogo-hover-active');
        
        // Remover tooltip
        const tooltip = row.querySelector('.navegacao-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    navegarParaAnalise(jogoNumero) {
        console.log(`🎯 [NAVEGAÇÃO] Navegando para análise do Jogo ${jogoNumero}`);
        
        // 1. Trocar para aba "Análise Rápida"
        this.switchToTab('analise-rapida');
        
        // 2. Aguardar a aba carregar e rolar para o jogo específico
        setTimeout(() => {
            this.scrollToGame(jogoNumero);
            this.highlightGame(jogoNumero);
        }, 500);
    }

    switchToTab(tabId) {
        // Remover active de todas as abas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Esconder todas as abas
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });

        // Ativar aba desejada
        const targetBtn = document.querySelector(`[data-tab="${tabId}"]`);
        const targetContent = document.getElementById(tabId);

        if (targetBtn && targetContent) {
            targetBtn.classList.add('active');
            targetContent.style.display = 'block';
            targetContent.classList.add('tab-transition');
            
            console.log(`✅ [NAVEGAÇÃO] Aba ${tabId} ativada`);
        }
    }

    scrollToGame(jogoNumero) {
        const gameContainer = document.getElementById(`jogo${jogoNumero}-container`);
        
        if (gameContainer) {
            // Aguardar um pouco para a aba carregar completamente
            setTimeout(() => {
                // Rolar suavemente para o jogo
                gameContainer.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                
                console.log(`📍 [NAVEGAÇÃO] Rolando para Jogo ${jogoNumero}`);
            }, 200);
        } else {
            console.warn(`⚠️ [NAVEGAÇÃO] Container do Jogo ${jogoNumero} não encontrado`);
        }
    }

    highlightGame(jogoNumero) {
        const gameContainer = document.getElementById(`jogo${jogoNumero}-container`);
        
        if (gameContainer) {
            // Adicionar efeito de destaque
            gameContainer.classList.add('jogo-destaque-navegacao');
            
            // Remover destaque após 3 segundos
            setTimeout(() => {
                gameContainer.classList.remove('jogo-destaque-navegacao');
            }, 3000);
            
            console.log(`✨ [NAVEGAÇÃO] Jogo ${jogoNumero} destacado`);
        }
    }

    setupHoverEffects() {
        // Adicionar estilos dinâmicos para hover - MESMO ESTILO DA FORÇA DOS ELENCOS
        const style = document.createElement('style');
        style.textContent = `
            .jogo-hover-active {
                transform: scale(1.02) !important;
                box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2) !important;
                border-color: var(--cor-destaque-primaria) !important;
                background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%) !important;
            }
            
            .navegacao-tooltip {
                position: absolute;
                top: -35px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, var(--cor-destaque-primaria) 0%, #7C3AED 100%);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                white-space: nowrap;
                z-index: 1000;
                box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
                animation: fadeIn 0.3s ease;
            }
            
            .jogo-destaque-navegacao {
                animation: highlightPulse 0.5s ease-in-out 3;
                transform: scale(1.02) !important;
                box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
                border-color: var(--cor-destaque-primaria) !important;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateX(-50%) translateY(10px); }
                to { opacity: 1; transform: translateX(-50%) translateY(0); }
            }
            
            @keyframes highlightPulse {
                0%, 100% { transform: scale(1.02); }
                50% { transform: scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.NavegacaoInteligente = new NavegacaoInteligente();
});

// Exportar para uso global
window.NavegacaoInteligente = NavegacaoInteligente;
