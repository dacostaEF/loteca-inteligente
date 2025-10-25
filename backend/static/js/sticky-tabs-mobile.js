// Script para forçar comportamento sticky das abas em mobile
// Solução alternativa para quando CSS sticky não funciona

document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos em mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Elementos
    let tabsContainer = null;
    let isSticky = false;
    let originalTop = 0;
    
    // Função para aplicar sticky via JavaScript
    function applyStickyBehavior() {
        if (!isMobile() || !tabsContainer) return;
        
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const containerTop = tabsContainer.offsetTop;
        
        // Se o container chegou ao topo e ainda não está sticky
        if (scrollTop >= containerTop && !isSticky) {
            tabsContainer.style.position = 'fixed';
            tabsContainer.style.top = '0';
            tabsContainer.style.left = '0';
            tabsContainer.style.right = '0';
            tabsContainer.style.zIndex = '100';
            tabsContainer.style.background = 'linear-gradient(135deg, rgba(18, 16, 26, 0.95) 0%, rgba(30, 27, 41, 0.95) 50%, rgba(18, 16, 26, 0.95) 100%)';
            tabsContainer.style.backdropFilter = 'blur(8px)';
            tabsContainer.style.borderBottom = '1px solid var(--cor-borda)';
            tabsContainer.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            isSticky = true;
        }
        // Se o scroll voltou para cima e está sticky
        else if (scrollTop < originalTop && isSticky) {
            tabsContainer.style.position = '';
            tabsContainer.style.top = '';
            tabsContainer.style.left = '';
            tabsContainer.style.right = '';
            tabsContainer.style.zIndex = '';
            tabsContainer.style.background = '';
            tabsContainer.style.backdropFilter = '';
            tabsContainer.style.borderBottom = '';
            tabsContainer.style.boxShadow = '';
            isSticky = false;
        }
    }
    
    // Função para inicializar
    function initStickyTabs() {
        if (!isMobile()) return;
        
        tabsContainer = document.querySelector('.tabs-container');
        if (!tabsContainer) return;
        
        // Armazenar posição original
        originalTop = tabsContainer.offsetTop;
        
        // Aplicar comportamento sticky
        window.addEventListener('scroll', applyStickyBehavior);
        
        // Aplicar na carga inicial
        applyStickyBehavior();
    }
    
    // Inicializar
    initStickyTabs();
    
    // Reinicializar quando a tela for redimensionada
    window.addEventListener('resize', function() {
        if (isMobile()) {
            initStickyTabs();
        } else {
            // Limpar sticky quando sair do mobile
            if (tabsContainer && isSticky) {
                tabsContainer.style.position = '';
                tabsContainer.style.top = '';
                tabsContainer.style.left = '';
                tabsContainer.style.right = '';
                tabsContainer.style.zIndex = '';
                tabsContainer.style.background = '';
                tabsContainer.style.backdropFilter = '';
                tabsContainer.style.borderBottom = '';
                tabsContainer.style.boxShadow = '';
                isSticky = false;
            }
        }
    });
    
    // Observar mudanças no DOM para detectar quando as abas são carregadas
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && isMobile()) {
                const tabsContainerNew = document.querySelector('.tabs-container');
                if (tabsContainerNew && !tabsContainer) {
                    initStickyTabs();
                }
            }
        });
    });
    
    // Observar mudanças no body
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
