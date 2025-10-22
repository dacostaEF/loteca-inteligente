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
            
            // REMOVER listeners da linha inteira
            // row.addEventListener('click', ...) - REMOVIDO
            
            // CRIAR área específica clicável no canto direito
            this.createNavigationArea(row, index + 1);
        });

        console.log(`✅ [NAVEGAÇÃO] ${optimizationRows.length} jogos configurados para navegação`);
    }

    createNavigationArea(row, jogoNumero) {
        // Encontrar a última célula (canto direito) onde estão estatísticas
        const lastCell = row.querySelector('td:last-child');
        
        if (lastCell) {
            // Criar área clicável específica com tooltip integrado
            const navigationArea = document.createElement('div');
            navigationArea.className = 'analise-navegacao-area';
            navigationArea.setAttribute('data-jogo', jogoNumero);
            navigationArea.innerHTML = '🔍';
            navigationArea.title = 'Clique para ver análise detalhada';
            
            // Adicionar à última célula
            lastCell.appendChild(navigationArea);
            
            // Adicionar listener apenas na área específica
            navigationArea.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation(); // Evitar propagação para a linha
                this.navegarParaAnalise(jogoNumero);
            });
            
            // Adicionar efeito de hover integrado
            navigationArea.addEventListener('mouseenter', () => {
                this.showIntegratedTooltip(navigationArea);
            });
            
            navigationArea.addEventListener('mouseleave', () => {
                this.hideIntegratedTooltip(navigationArea);
            });
            
            console.log(`🎯 [NAVEGAÇÃO] Área específica criada para Jogo ${jogoNumero}`);
        }
    }

    showIntegratedTooltip(area) {
        // Tooltip já é gerenciado pelo CSS ::after
        area.classList.add('tooltip-active');
    }

    hideIntegratedTooltip(area) {
        // Remover classe de tooltip ativo
        area.classList.remove('tooltip-active');
    }

    // Métodos antigos removidos - agora usando área específica

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
        // Estilos agora são gerenciados pelo CSS - área específica
        console.log('✅ [NAVEGAÇÃO] Estilos de hover configurados via CSS');
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.NavegacaoInteligente = new NavegacaoInteligente();
});

// Exportar para uso global
window.NavegacaoInteligente = NavegacaoInteligente;
