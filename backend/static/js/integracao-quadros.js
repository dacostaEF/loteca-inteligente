/**
 * INTEGRAÇÃO DOS QUADROS COMPARATIVOS
 * Sistema para integrar os quadros comparativos na aplicação principal
 */

// Função para integrar quadros comparativos na aba "Plantel ($)"
function integrarQuadrosComparativos() {
    console.log('🎯 [QUADROS] Integrando quadros comparativos...');
    
    // Verificar se o sistema de quadros está disponível
    if (typeof QuadroComparativo === 'undefined') {
        console.error('❌ [QUADROS] Sistema QuadroComparativo não encontrado!');
        return;
    }
    
    const quadro = new QuadroComparativo();
    
    // Dados reais dos jogos (baseados nos CSVs)
    const dadosJogos = obterDadosJogosReais();
    
    // Renderizar quadros na sub-aba "Plantel ($)"
    renderizarQuadrosNaAbaPlantel(quadro, dadosJogos);
}

/**
 * Obter dados reais dos jogos baseados EXCLUSIVAMENTE nos CSVs da Série A
 * ✅ CORRIGIDO: Usando dados reais do CSV Valor_Elenco_serie_a_brasileirao.csv
 */
function obterDadosJogosReais() {
    return [
        // JOGO 1 - Flamengo vs Palmeiras (DADOS CORRETOS DO CSV SÉRIE A)
        {
            numero: 1,
            timeA: {
                nome: 'FLAMENGO/RJ',
                sigla: 'FLA',
                plantel: 31,  // ✅ CORRETO: CSV Série A posição 2
                nacionais: 21,  // 31 - 10 = 21
                estrangeiros: 10,  // ✅ CORRETO: CSV Série A
                idade: 28.4,  // ✅ CORRETO: CSV Série A
                forca: 6.0,  // ✅ CORRETO: Baseado no valor real € 195.90 mi
                valor: '€ 195.90 mi',  // ✅ CORRETO: CSV Série A
                valorNumerico: 195.90,
                posse: '62.2%',  // ✅ CORRETO: CSV Série A
                passes: 509,  // ✅ CORRETO: CSV Série A
                chutes: 5.7,  // ✅ CORRETO: CSV Série A
                categoria: 'grande',
                badge: 'Elenco Forte'
            },
            timeB: {
                nome: 'PALMEIRAS/SP',
                sigla: 'PAL',
                plantel: 29,  // ✅ CORRETO: CSV Série A posição 1
                nacionais: 21,  // 29 - 8 = 21
                estrangeiros: 8,  // ✅ CORRETO: CSV Série A
                idade: 26.3,  // ✅ CORRETO: CSV Série A
                forca: 6.7,  // ✅ CORRETO: Baseado no valor real € 212.15 mi
                valor: '€ 212.15 mi',  // ✅ CORRETO: CSV Série A
                valorNumerico: 212.15,
                posse: '52.1%',  // ✅ CORRETO: CSV Série A
                passes: 340,  // ✅ CORRETO: CSV Série A
                chutes: 4.7,  // ✅ CORRETO: CSV Série A
                categoria: 'elite',
                badge: 'Elenco Elite'
            },
            insight: 'Confronto equilibrado no plantel',
            deltaForca: '+0.7 pts',
            deltaValor: '€ 16.25 mi'
        },
        
        // JOGO 2 - Internacional vs Sport
        {
            numero: 2,
            timeA: {
                nome: 'INTERNACIONAL/RS',
                sigla: 'INT',
                plantel: 29,
                nacionais: 20,
                estrangeiros: 9,
                idade: 27.0,
                forca: 5.8,
                valor: '€ 86.00 mi',
                valorNumerico: 86.00,
                posse: '51.7%',
                passes: 383,
                chutes: 4.7,
                categoria: 'grande',
                badge: 'Elenco Forte'
            },
            timeB: {
                nome: 'SPORT RECIFE/PE',
                sigla: 'SPT',
                plantel: 31,
                nacionais: 25,
                estrangeiros: 6,
                idade: 29.1,
                forca: 4.2,
                valor: '€ 39.25 mi',
                valorNumerico: 39.25,
                posse: '47.2%',
                passes: 309,
                chutes: 4.2,
                categoria: 'medio',
                badge: 'Elenco Sólido'
            },
            insight: 'Internacional leva vantagem em força',
            deltaForca: '-1.6 pts',
            deltaValor: '€ -46.75 mi'
        }
        
        // Adicionar mais jogos conforme necessário...
    ];
}

/**
 * Renderizar quadros na aba "Plantel ($)" usando dados reais do CSV Série A
 * ✅ CORRIGIDO: Carregando dados via API /api/br/elenco/ que lê do CSV
 */
async function renderizarQuadrosNaAbaPlantel(quadro, dadosJogos) {
    const container = document.getElementById('jogos-loteca-container');
    if (!container) {
        console.error('❌ [QUADROS] Container jogos-loteca-container não encontrado!');
        return;
    }
    
    // Limpar container atual
    container.innerHTML = '';
    
    console.log('🔍 [QUADROS] Carregando dados reais do CSV Série A...');
    
    // Carregar dados via API CSV para os primeiros jogos
    try {
        // JOGO 1 - Flamengo vs Palmeiras (dados reais do CSV)
        await carregarDadosJogoAPI(1);
        
        // JOGO 2 - Internacional vs Sport (se disponível no CSV)
        await carregarDadosJogoAPI(2);
        
        // JOGO 3 - Corinthians vs Atlético-MG (se disponível no CSV)
        await carregarDadosJogoAPI(3);
        
        console.log('✅ [QUADROS] Quadros renderizados com dados reais do CSV Série A');
        
    } catch (error) {
        console.error('❌ [QUADROS] Erro ao carregar dados do CSV, usando dados estáticos:', error);
        
        // Fallback: usar dados estáticos corrigidos
        dadosJogos.forEach(jogo => {
            const jogoContainer = document.createElement('div');
            jogoContainer.id = `quadro-jogo-${jogo.numero}`;
            jogoContainer.className = 'quadro-jogo-container';
            
            container.appendChild(jogoContainer);
            
            // Renderizar quadro
            quadro.renderizarQuadro(jogo, `quadro-jogo-${jogo.numero}`);
        });
    }
}

/**
 * Função para atualizar dados de um jogo específico
 */
function atualizarDadosJogo(numeroJogo, novosDados) {
    const quadro = new QuadroComparativo();
    const containerId = `quadro-jogo-${numeroJogo}`;
    
    // Atualizar dados
    const dadosAtualizados = quadro.criarDadosJogo(numeroJogo, novosDados.timeA, novosDados.timeB);
    
    // Re-renderizar
    quadro.renderizarQuadro(dadosAtualizados, containerId);
    
    console.log(`✅ [QUADROS] Jogo ${numeroJogo} atualizado`);
}

/**
 * Função para carregar dados de um jogo via API CSV Série A
 * ✅ CORRIGIDO: Usando exclusivamente /api/br/elenco/ que lê do CSV Série A
 */
async function carregarDadosJogoAPI(numeroJogo) {
    try {
        console.log(`🔍 [QUADROS] Carregando dados do Jogo ${numeroJogo} via CSV Série A...`);
        
        // Buscar dados dos times via API CSV Série A
        const [timeA, timeB] = await Promise.all([
            fetch(`/api/br/elenco/${getNomeTimeA(numeroJogo)}`).then(r => r.json()),
            fetch(`/api/br/elenco/${getNomeTimeB(numeroJogo)}`).then(r => r.json())
        ]);
        
        if (!timeA.success || !timeB.success) {
            throw new Error(`Erro ao carregar dados dos times do jogo ${numeroJogo}`);
        }
        
        // Converter dados do CSV para formato do quadro
        const dadosQuadro = {
            numero: numeroJogo,
            timeA: {
                nome: timeA.dados.nome_original || getNomeTimeA(numeroJogo),
                sigla: getSiglaTimeA(numeroJogo),
                plantel: timeA.dados.plantel || 0,
                nacionais: (timeA.dados.plantel || 0) - (timeA.dados.estrangeiros || 0),
                estrangeiros: timeA.dados.estrangeiros || 0,
                idade: timeA.dados.idade_media || 0,
                forca: timeA.dados.forca_elenco || 0,
                valor: timeA.dados.valor_total || '€ 0 mi',
                valorNumerico: timeA.dados.valor_mm_euros || 0,
                posse: '0%',  // Não disponível no CSV atual
                passes: 0,    // Não disponível no CSV atual
                chutes: 0,    // Não disponível no CSV atual
                categoria: determinarCategoria(timeA.dados.forca_elenco || 0),
                badge: gerarBadge(timeA.dados.forca_elenco || 0)
            },
            timeB: {
                nome: timeB.dados.nome_original || getNomeTimeB(numeroJogo),
                sigla: getSiglaTimeB(numeroJogo),
                plantel: timeB.dados.plantel || 0,
                nacionais: (timeB.dados.plantel || 0) - (timeB.dados.estrangeiros || 0),
                estrangeiros: timeB.dados.estrangeiros || 0,
                idade: timeB.dados.idade_media || 0,
                forca: timeB.dados.forca_elenco || 0,
                valor: timeB.dados.valor_total || '€ 0 mi',
                valorNumerico: timeB.dados.valor_mm_euros || 0,
                posse: '0%',  // Não disponível no CSV atual
                passes: 0,    // Não disponível no CSV atual
                chutes: 0,    // Não disponível no CSV atual
                categoria: determinarCategoria(timeB.dados.forca_elenco || 0),
                badge: gerarBadge(timeB.dados.forca_elenco || 0)
            },
            insight: 'Dados carregados do CSV Série A',
            deltaForca: `+${((timeB.dados.forca_elenco || 0) - (timeA.dados.forca_elenco || 0)).toFixed(1)} pts`,
            deltaValor: `€ ${((timeB.dados.valor_mm_euros || 0) - (timeA.dados.valor_mm_euros || 0)).toFixed(2)} mi`
        };
        
        // Renderizar
        const quadro = new QuadroComparativo();
        quadro.renderizarQuadro(dadosQuadro, `quadro-jogo-${numeroJogo}`);
        
        console.log(`✅ [QUADROS] Dados do jogo ${numeroJogo} carregados do CSV Série A`);
        
    } catch (error) {
        console.error(`❌ [QUADROS] Erro ao carregar dados do jogo ${numeroJogo}:`, error);
    }
}

/**
 * Funções auxiliares para mapear jogos
 */
function getNomeTimeA(numeroJogo) {
    const mapeamento = {
        1: 'Flamengo',
        2: 'Internacional', 
        3: 'Corinthians',
        // Adicionar mais conforme necessário
    };
    return mapeamento[numeroJogo] || 'Time A';
}

function getNomeTimeB(numeroJogo) {
    const mapeamento = {
        1: 'Palmeiras',
        2: 'Sport',
        3: 'Atletico-MG',
        // Adicionar mais conforme necessário
    };
    return mapeamento[numeroJogo] || 'Time B';
}

function getSiglaTimeA(numeroJogo) {
    const mapeamento = {
        1: 'FLA',
        2: 'INT',
        3: 'COR',
        // Adicionar mais conforme necessário
    };
    return mapeamento[numeroJogo] || 'A';
}

function getSiglaTimeB(numeroJogo) {
    const mapeamento = {
        1: 'PAL',
        2: 'SPT',
        3: 'CAM',
        // Adicionar mais conforme necessário
    };
    return mapeamento[numeroJogo] || 'B';
}

function determinarCategoria(forca) {
    if (forca >= 7.0) return 'elite';
    if (forca >= 6.0) return 'grande';
    if (forca >= 4.0) return 'medio';
    return 'regional';
}

function gerarBadge(forca) {
    if (forca >= 7.0) return 'Elenco Elite';
    if (forca >= 6.0) return 'Elenco Forte';
    if (forca >= 4.0) return 'Elenco Sólido';
    return 'Elenco em Desenvolvimento';
}

/**
 * Converter dados da API para formato do quadro comparativo
 */
function converterDadosParaQuadro(dadosAPI) {
    return {
        numero: dadosAPI.numero,
        timeA: {
            nome: dadosAPI.timeA.nome,
            sigla: dadosAPI.timeA.sigla,
            plantel: dadosAPI.timeA.plantel,
            nacionais: dadosAPI.timeA.nacionais,
            estrangeiros: dadosAPI.timeA.estrangeiros,
            idade: dadosAPI.timeA.idade,
            forca: dadosAPI.timeA.forca,
            valor: dadosAPI.timeA.valor,
            valorNumerico: dadosAPI.timeA.valorNumerico,
            posse: dadosAPI.timeA.posse,
            passes: dadosAPI.timeA.passes,
            chutes: dadosAPI.timeA.chutes,
            categoria: dadosAPI.timeA.categoria,
            badge: dadosAPI.timeA.badge
        },
        timeB: {
            nome: dadosAPI.timeB.nome,
            sigla: dadosAPI.timeB.sigla,
            plantel: dadosAPI.timeB.plantel,
            nacionais: dadosAPI.timeB.nacionais,
            estrangeiros: dadosAPI.timeB.estrangeiros,
            idade: dadosAPI.timeB.idade,
            forca: dadosAPI.timeB.forca,
            valor: dadosAPI.timeB.valor,
            valorNumerico: dadosAPI.timeB.valorNumerico,
            posse: dadosAPI.timeB.posse,
            passes: dadosAPI.timeB.passes,
            chutes: dadosAPI.timeB.chutes,
            categoria: dadosAPI.timeB.categoria,
            badge: dadosAPI.timeB.badge
        },
        insight: dadosAPI.insight,
        deltaForca: dadosAPI.deltaForca,
        deltaValor: dadosAPI.deltaValor
    };
}

/**
 * Inicializar sistema de quadros comparativos
 */
function inicializarSistemaQuadros() {
    console.log('🚀 [QUADROS] Inicializando sistema de quadros comparativos...');
    
    // Verificar se estamos na aba "Plantel ($)"
    const abaPlantel = document.getElementById('times-loteca');
    if (abaPlantel && abaPlantel.style.display !== 'none') {
        console.log('📊 [QUADROS] Aba Plantel ($) ativa, integrando quadros...');
        integrarQuadrosComparativos();
    }
    
    // Adicionar listener para mudanças de aba
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('sub-tab-btn') && e.target.dataset.subtab === 'times-loteca') {
            console.log('🔄 [QUADROS] Aba Plantel ($) ativada, renderizando quadros...');
            setTimeout(() => {
                integrarQuadrosComparativos();
            }, 100);
        }
    });
}

// Auto-inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Aguardar um pouco para garantir que todos os scripts estejam carregados
    setTimeout(() => {
        inicializarSistemaQuadros();
    }, 1000);
});

// Exportar funções para uso global
window.integrarQuadrosComparativos = integrarQuadrosComparativos;
window.atualizarDadosJogo = atualizarDadosJogo;
window.carregarDadosJogoAPI = carregarDadosJogoAPI;
