// Script para forçar quebra de linha após "vs" na coluna Confrontos
// Aplicado em AMBOS os ambientes: mobile e desktop

document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos em ambiente mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Função para aplicar quebra de linha após "vs"
    function applyLineBreakAfterVs() {
        // Aplicar em AMBOS os ambientes (mobile e desktop)
        
        // Buscar todas as células da coluna Confrontos (2ª coluna)
        const confrontoCells = document.querySelectorAll('.page--otimizador-aposta .optimization-table td:nth-child(2)');
        
        confrontoCells.forEach(cell => {
            // Verificar se já foi processado
            if (cell.dataset.processed === 'true') return;
            
            // Obter o texto da célula
            let text = cell.textContent || cell.innerText;
            
            // Verificar se contém "vs" e ainda não foi quebrado
            if (text.includes('vs') && !text.includes('\n')) {
                // Substituir "vs" por "vs\n" para forçar quebra de linha
                text = text.replace(/vs/g, 'vs\n');
                
                // Aplicar o texto com quebra de linha
                cell.textContent = text;
                
                // Marcar como processado
                cell.dataset.processed = 'true';
            }
        });
    }
    
    // Aplicar na carga inicial
    applyLineBreakAfterVs();
    
    // Aplicar quando a tela for redimensionada
    window.addEventListener('resize', function() {
        // Limpar marcações para reprocessar
        const confrontoCells = document.querySelectorAll('.page--otimizador-aposta .optimization-table td:nth-child(2)');
        confrontoCells.forEach(cell => {
            delete cell.dataset.processed;
        });
        applyLineBreakAfterVs();
    });
    
    // Aplicar quando houver mudanças no DOM (caso a tabela seja carregada dinamicamente)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                applyLineBreakAfterVs();
            }
        });
    });
    
    // Observar mudanças na tabela
    const tableContainer = document.querySelector('.page--otimizador-aposta .optimization-table');
    if (tableContainer) {
        observer.observe(tableContainer, {
            childList: true,
            subtree: true
        });
    }
});
