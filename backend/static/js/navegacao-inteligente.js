/**
 * NAVEGAÇÃO INTELIGENTE ENTRE ABAS
 * Sistema para navegar automaticamente entre Otimizador e Análise Rápida
 */

class NavegacaoInteligente {
    constructor() {
        this.init();
    }

    init() {
        // Log crítico - sempre mantido
        window.log.navigation('Inicializando navegação inteligente...');
        this.setupEventListeners();
        this.setupHoverEffects();
    }

    setupEventListeners() {
        // Aguardar o carregamento da tabela de otimização
        setTimeout(() => {
            this.attachClickListeners();
        }, 2000); // Aumentar tempo de espera
        
        // Tentar novamente após mais tempo para garantir que todas as linhas estejam carregadas
        setTimeout(() => {
            this.attachClickListeners();
        }, 5000);
        
        // Verificação final para garantir que todos os jogos tenham a funcionalidade
        setTimeout(() => {
            this.verifyAllGamesHaveNavigation();
        }, 8000);
    }

    verifyAllGamesHaveNavigation() {
        const optimizationRows = document.querySelectorAll('#optimization-tbody tr');
        let missingNavigation = 0;
        
        optimizationRows.forEach((row, index) => {
            const jogoNumero = index + 1;
            const hasNavigation = row.querySelector('.analise-navegacao-area');
            
            if (!hasNavigation) {
                console.warn(`⚠️ [VERIFICAÇÃO] Jogo ${jogoNumero} não tem área de navegação - criando...`);
                this.createNavigationArea(row, jogoNumero);
                missingNavigation++;
            }
        });
        
        if (missingNavigation > 0) {
            // Log crítico - jogos sem navegação
            window.log.warning(`${missingNavigation} jogos tiveram navegação adicionada`);
        } else {
            // Log de sucesso - apenas em desenvolvimento
            window.log.debug(`Todos os ${optimizationRows.length} jogos têm navegação configurada`);
        }
    }

    attachClickListeners() {
        const optimizationRows = document.querySelectorAll('#optimization-tbody tr');
        
        // Log de debug - apenas em desenvolvimento
        window.log.debug(`Encontradas ${optimizationRows.length} linhas na tabela`);
        
        optimizationRows.forEach((row, index) => {
            const jogoNumero = index + 1;
            
            // Adicionar data-jogo para identificação
            row.setAttribute('data-jogo', jogoNumero);
            
            // Verificar se já existe área de navegação
            const existingArea = row.querySelector('.analise-navegacao-area');
            if (existingArea) {
                // Log de debug - apenas em desenvolvimento
                window.log.debug(`Área já existe para Jogo ${jogoNumero}`);
                return; // Pular se já existe
            }
            
            // CRIAR área específica clicável no canto direito
            this.createNavigationArea(row, jogoNumero);
        });

        // Log crítico - sempre mantido
        window.log.navigation(`${optimizationRows.length} jogos configurados para navegação`);
    }

    createNavigationArea(row, jogoNumero) {
        // Encontrar a última célula (canto direito) onde estão estatísticas
        const lastCell = row.querySelector('td:last-child');
        
        if (lastCell) {
            // Verificar se já existe área de navegação nesta célula
            const existingArea = lastCell.querySelector('.analise-navegacao-area');
            if (existingArea) {
                console.log(`⚠️ [NAVEGAÇÃO] Área já existe na célula do Jogo ${jogoNumero}`);
                return;
            }
            
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
        } else {
            console.warn(`⚠️ [NAVEGAÇÃO] Última célula não encontrada para Jogo ${jogoNumero}`);
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
        
        // 1. Salvar o jogo atual para retorno
        this.jogoAtual = jogoNumero;
        
        // 2. Trocar para aba "Análise Rápida"
        this.switchToTab('analise-rapida');
        
        // 3. Aguardar a aba carregar e rolar para o jogo específico
        setTimeout(() => {
            this.scrollToGame(jogoNumero);
            this.highlightGame(jogoNumero);
            
            // 4. Mostrar botão de retorno
            this.showRetornoButton();
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
            // Adicionar efeito de destaque - MESMO ESTILO DA FORÇA DOS ELENCOS
            gameContainer.classList.add('destaque-navegacao');
            
            // Remover destaque após 3 segundos
            setTimeout(() => {
                gameContainer.classList.remove('destaque-navegacao');
            }, 3000);
            
            // Log crítico - sempre mantido
            window.log.navigation(`Jogo ${jogoNumero} destacado na Análise Rápida`);
        }
    }

    setupHoverEffects() {
        // Estilos agora são gerenciados pelo CSS - área específica
        window.log.debug('Estilos de hover configurados via CSS');
    }

    showRetornoButton() {
        // Criar botão de retorno se não existir
        if (!this.retornoButton) {
            this.createRetornoButton();
        }
        
        // Mostrar botão com animação
        setTimeout(() => {
            this.retornoButton.classList.add('show');
            console.log(`🔄 [RETORNO] Botão de retorno mostrado para Jogo ${this.jogoAtual}`);
        }, 300);
    }

    createRetornoButton() {
        // Encontrar o container do jogo específico
        const gameContainer = document.getElementById(`jogo${this.jogoAtual}-container`);
        
        if (!gameContainer) {
            console.warn(`⚠️ [RETORNO] Container do Jogo ${this.jogoAtual} não encontrado`);
            return;
        }
        
        // Criar botão de retorno
        this.retornoButton = document.createElement('button');
        this.retornoButton.className = 'retorno-otimizador-btn';
        this.retornoButton.innerHTML = `
            <span class="icon">←</span>
            Voltar ao Otimizador
        `;
        
        // Adicionar listener de clique
        this.retornoButton.addEventListener('click', () => {
            this.retornarAoOtimizador();
        });
        
        // Adicionar ao container do jogo específico
        gameContainer.appendChild(this.retornoButton);
        
        console.log(`🔄 [RETORNO] Botão de retorno criado no container do Jogo ${this.jogoAtual}`);
    }

    retornarAoOtimizador() {
        if (this.jogoAtual) {
            console.log(`🔄 [RETORNO] Retornando ao Jogo ${this.jogoAtual} no Otimizador`);
            
            // 1. Trocar para aba Otimizador
            this.switchToTab('otimizador-aposta');
            
            // 2. Aguardar e rolar para o jogo específico
            setTimeout(() => {
                this.scrollToGameOtimizador(this.jogoAtual);
                this.highlightGameOtimizador(this.jogoAtual);
                
                // 3. Esconder botão de retorno
                this.hideRetornoButton();
            }, 300);
        }
    }

    scrollToGameOtimizador(jogoNumero) {
        const gameRow = document.querySelector(`#optimization-tbody tr[data-jogo="${jogoNumero}"]`);
        
        if (gameRow) {
            gameRow.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            
            console.log(`📍 [RETORNO] Rolando para Jogo ${jogoNumero} no Otimizador`);
        }
    }

    highlightGameOtimizador(jogoNumero) {
        const gameRow = document.querySelector(`#optimization-tbody tr[data-jogo="${jogoNumero}"]`);
        
        if (gameRow) {
            // Adicionar efeito de destaque - MESMO ESTILO DA FORÇA DOS ELENCOS
            gameRow.classList.add('jogo-destaque-retorno');
            
            // Remover destaque após 3 segundos
            setTimeout(() => {
                gameRow.classList.remove('jogo-destaque-retorno');
            }, 3000);
            
            // Log crítico - sempre mantido
            window.log.navigation(`Jogo ${jogoNumero} destacado no Otimizador`);
        }
    }

    hideRetornoButton() {
        if (this.retornoButton) {
            this.retornoButton.classList.remove('show');
            
            // Remover botão após animação
            setTimeout(() => {
                if (this.retornoButton && this.retornoButton.parentNode) {
                    this.retornoButton.parentNode.removeChild(this.retornoButton);
                    this.retornoButton = null;
                }
            }, 300);
            
            console.log(`🔄 [RETORNO] Botão de retorno escondido do Jogo ${this.jogoAtual}`);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.NavegacaoInteligente = new NavegacaoInteligente();
});

// Exportar para uso global
window.NavegacaoInteligente = NavegacaoInteligente;
