/**
 * LOTECA - FUNÇÕES UNIFICADAS
 * Arquivo JavaScript separado para manter o HTML mais leve
 * Contém todas as funções para carregar dados dos jogos
 */

// MAPEAMENTO DOS JOGOS - CSV E TIMES
const jogosMap = {
    1: { csv: 'Flamengo_vs_Palmeiras.csv', casa: 'Flamengo', fora: 'Palmeiras' },
    2: { csv: 'Internacional_vs_Sport.csv', casa: 'Internacional', fora: 'Sport' },
    3: { csv: 'Corinthians_vs_Atletico-MG.csv', casa: 'Corinthians', fora: 'Atletico-MG' },
    4: { csv: 'Roma_vs_Internazionale.csv', casa: 'Roma', fora: 'Internazionale' },
    5: { csv: 'Atletico-Madrid_vs_Osasuna.csv', casa: 'Atletico Madrid', fora: 'Osasuna' },
    6: { csv: 'Cruzeiro_vs_Fortaleza.csv', casa: 'Cruzeiro', fora: 'Fortaleza' },
    7: { csv: 'Tottenham_vs_Aston-Villa.csv', casa: 'Tottenham', fora: 'Aston Villa' },
    8: { csv: 'Mirassol_vs_Sao-Paulo.csv', casa: 'Mirassol', fora: 'Sao_Paulo' },
    9: { csv: 'Ceara_vs_Botafogo-RJ.csv', casa: 'Ceará', fora: 'Botafogo' },
    10: { csv: 'Liverpool_vs_Mancheter-United.csv', casa: 'Liverpool', fora: 'Manchester United' },
    11: { csv: 'Atalanta_vs_Lazio.csv', casa: 'Atalanta', fora: 'Lazio' },
    12: { csv: 'Bahia_vs_Gremio.csv', casa: 'Bahia', fora: 'Gremio' },
    13: { csv: 'Milan_vs_Fiorentina.csv', casa: 'Milan', fora: 'Fiorentina' },
    14: { csv: 'Getafe_vs_Real-Madrid.csv', casa: 'Getafe', fora: 'Real Madrid' }
};

/**
 * FUNÇÃO DE NORMALIZAÇÃO DE TEXTO PARA COMPARAÇÃO DE TIMES
 * Remove acentos, converte para minúsculas e trata variações comuns
 */
function normalizarTexto(texto) {
    if (!texto || typeof texto !== 'string') return '';
    
    return texto
        // Converter para minúsculas
        .toLowerCase()
        // Remover acentos e caracteres especiais
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        // Remover espaços extras
        .trim()
        // Substituir variações comuns
        .replace(/gremio/g, 'gremio')
        .replace(/grêmio/g, 'gremio')
        .replace(/grêmio/g, 'gremio')
        .replace(/sao paulo/g, 'sao_paulo')
        .replace(/são paulo/g, 'sao_paulo')
        .replace(/manchester united/g, 'manchester_united')
        .replace(/manchester-united/g, 'manchester_united')
        .replace(/mancheter-united/g, 'manchester_united')
        .replace(/mancheter united/g, 'manchester_united')
        .replace(/botafogo-rj/g, 'botafogo')
        .replace(/botafogo rj/g, 'botafogo')
        .replace(/sao-paulo/g, 'sao_paulo')
        .replace(/são-paulo/g, 'sao_paulo')
        // Remover caracteres especiais restantes
        .replace(/[^a-z0-9_]/g, '');
}

/**
 * FUNÇÃO PARA COMPARAR TIMES NORMALIZADOS
 * Compara dois nomes de times ignorando acentos, maiúsculas e variações
 */
function compararTimes(time1, time2) {
    const normalizado1 = normalizarTexto(time1);
    const normalizado2 = normalizarTexto(time2);
    
    // console.log(`🔍 [COMPARAÇÃO] "${time1}" → "${normalizado1}" vs "${time2}" → "${normalizado2}"`);
    
    return normalizado1 === normalizado2;
}

/**
 * FUNÇÃO PARA ENCONTRAR TIME CORRESPONDENTE EM LISTA
 * Encontra o time correto mesmo com variações de nome
 */
function encontrarTimeCorrespondente(nomeTime, listaTimes) {
    const normalizado = normalizarTexto(nomeTime);
    
    for (const time of listaTimes) {
        if (compararTimes(nomeTime, time)) {
            // console.log(`✅ [ENCONTROU] "${nomeTime}" corresponde a "${time}"`);
            return time;
        }
    }
    
    console.warn(`⚠️ [NÃO ENCONTRADO] "${nomeTime}" não encontrado na lista:`, listaTimes);
    return nomeTime; // Retorna o nome original se não encontrar
}

// MAPEAMENTO DOS ESCUDOS
const escudosMap = {
    'Flamengo': '/static/escudos/flamengo.png',
    'Palmeiras': '/static/escudos/palmeiras.png',
    'Corinthians': '/static/escudos/corinthians.png',
    'Atletico-MG': '/static/escudos/atletico-mg.png',
    'Bahia': '/static/escudos/BAH_Bahia/Bahia.PNG',
    'Gremio': '/static/escudos/GRE_Gremio/Gremio.png',
    'Atletico Madrid': '/static/escudos/atletico-madrid.png',
    'Osasuna': '/static/escudos/osasuna.png',
    'Barcelona': '/static/escudos/barcelona.png',
    'Real Madrid': '/static/escudos/real-madrid.png',
    'Juventus': '/static/escudos/juventus.png',
    'Inter': '/static/escudos/inter.png',
    'Milan': '/static/escudos/Milan_IT/milan.png',
    'Fiorentina': '/static/escudos/Fiorentina_IT/fiorentina.png',
    'Getafe': '/static/escudos/Getafe/getafe.png',
    'Napoli': '/static/escudos/napoli.png',
    'Roma': '/static/escudos/Roma/Roma.png',
    'Internazionale': '/static/escudos/Internazionale/Internazionale.png',
    'Cruzeiro': '/static/escudos/CRU_Cruzeiro/Cruzeiro.png',
    'Fortaleza': '/static/escudos/FOR_Fortaleza/Fortaleza.png',
    'Tottenham': '/static/escudos/Tottenham/Tottenham.png',
    'Aston Villa': '/static/escudos/Aston_Villa/Aston_Villa.PNG',
    'Mirassol': '/static/escudos/MIR_Mirassol/Mirassol.png',
    'Sao_Paulo': '/static/escudos/SAP_SaoPaulo/SaoPaulo.png',
    'Lazio': '/static/escudos/lazio.png',
    'Liverpool': '/static/escudos/Liverpool/Liverpool.png',
    'Manchester United': '/static/escudos/Manchester_United/Manchester_United.png',
    'Atalanta': '/static/escudos/Atalanta-IT/atalanta.png',
    'Lazio': '/static/escudos/Lazio-IT/lazio.png',
    'Bahia': '/static/escudos/BAH_Bahia/Bahia.PNG',
    'Gremio': '/static/escudos/GRE_Gremio/Gremio.png',
    'Ceará': '/static/escudos/Ceara/Ceara.png',
    'Botafogo': '/static/escudos/Botafogo-RJ/Botafogo_RJ.png'
};

/**
 * FUNÇÃO PRINCIPAL - CARREGAR DADOS COMPLETOS DO JOGO
 * @param {number} numeroJogo - Número do jogo (1-14)
 */
async function carregarDadosCompletosJogo(numeroJogo) {
    // console.log(`🎯 [JOGO${numeroJogo}] Iniciando carregamento completo...`);
    
    try {
        // 1. CARREGAR DADOS DO JSON (ANÁLISE)
        // console.log(`📊 [JOGO${numeroJogo}] Carregando análise JSON...`);
        const response = await fetch(`/api/analise/jogo/${numeroJogo}?concurso=concurso_1216`);
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const dados = await response.json();
        // console.log(`✅ [JOGO${numeroJogo}] Dados JSON carregados:`, dados);
        
        // 2. ATUALIZAR CAMPOS PRINCIPAIS (JSON)
        await atualizarCamposPrincipais(numeroJogo, dados);
        
        // 3. CARREGAR E RENDERIZAR CONFRONTOS (CSV)
        await carregarERenderizarConfrontos(numeroJogo, dados);
        
        // console.log(`🎉 [JOGO${numeroJogo}] Carregamento completo finalizado!`);
        
    } catch (error) {
        console.error(`❌ [JOGO${numeroJogo}] Erro no carregamento:`, error);
        
        // FALLBACK: Usar dados do jogosMap
        const jogoInfo = jogosMap[numeroJogo];
        if (jogoInfo) {
            // console.log(`🔄 [JOGO${numeroJogo}] Usando dados de fallback...`);
            await carregarERenderizarConfrontos(numeroJogo, jogoInfo);
        }
    }
}

/**
 * ATUALIZAR CAMPOS PRINCIPAIS (DADOS DO JSON)
 * @param {number} numeroJogo - Número do jogo
 * @param {object} responseData - Resposta completa da API
 */
async function atualizarCamposPrincipais(numeroJogo, responseData) {
    // console.log(`🔧 [JOGO${numeroJogo}] Atualizando campos principais...`);
    
    // EXTRAIR DADOS DO JSON (SEGUINDO ESTRUTURA DO JOGO 5)
    const dados = responseData.dados || responseData;
    // console.log(`📊 [JOGO${numeroJogo}] Dados extraídos:`, dados);
    
    // MAPEAMENTO DE IDs DINÂMICOS - CORRIGIDO PARA ESTRUTURA REAL DO HTML
    const ids = {
        escudoCasa: `escudo-casa-jogo${numeroJogo}`,
        escudoFora: `escudo-fora-jogo${numeroJogo}`,
        nomeCasa: `time-casa-nome-jogo${numeroJogo}`,
        nomeFora: `time-fora-nome-jogo${numeroJogo}`,
        gameInfo: `game-info-jogo${numeroJogo}`,
        probCasa: `prob-casa-${numeroJogo}`,
        probEmpate: `prob-empate-${numeroJogo}`,
        probFora: `prob-fora-${numeroJogo}`,
        labelCasa: `label-casa-${numeroJogo}`,
        labelFora: `label-fora-${numeroJogo}`,
        recomendacao: `recomendacao-${numeroJogo}`,
        posicaoCasa: `posicao-casa-${numeroJogo}`,
        posicaoFora: `posicao-fora-${numeroJogo}`,
        confrontoDireto: `confronto-direto-principais-${numeroJogo}`,
        fatorCasa: `fator-casa-${numeroJogo}`,
        fatorFora: `fator-fora-${numeroJogo}`,
        conclusaoAnalista: `conclusao-${numeroJogo}`, // CORRIGIDO: era `conclusao-analista-${numeroJogo}`
        formaAnalise: `forma-analise-${numeroJogo}`,
        posicaoAnalise: `posicao-analise-${numeroJogo}`,
        h2hAnalise: `h2h-analise-${numeroJogo}`,
        fatorAnalise: `fator-analise-${numeroJogo}`
    };
    
    // 1. ATUALIZAR ESCUDOS E NOMES DOS TIMES
    console.log(`🔍 [JOGO${numeroJogo}] Buscando elemento: ${ids.escudoCasa}`);
    if (dados.escudo_casa) {
        const escudoCasa = document.getElementById(ids.escudoCasa);
        if (escudoCasa) {
            console.log(`✅ [JOGO${numeroJogo}] Atualizando escudo casa: ${dados.escudo_casa}`);
            escudoCasa.src = dados.escudo_casa;
            escudoCasa.alt = dados.time_casa || 'Time Casa';
        } else {
            console.error(`❌ [JOGO${numeroJogo}] Elemento não encontrado: ${ids.escudoCasa}`);
        }
    }
    
    if (dados.escudo_fora) {
        const escudoFora = document.getElementById(ids.escudoFora);
        if (escudoFora) {
            escudoFora.src = dados.escudo_fora;
            escudoFora.alt = dados.time_fora || 'Time Fora';
        }
    }
    
    if (dados.time_casa) {
        const nomeCasa = document.getElementById(ids.nomeCasa);
        if (nomeCasa) {
            nomeCasa.textContent = dados.time_casa.toUpperCase();
        }
        
        // ATUALIZAR NOME DO TIME CASA NO CABEÇALHO DA TABELA
        const nomeCasaTabela = document.getElementById(`time-casa-nome-${numeroJogo}-novo`);
        if (nomeCasaTabela) {
            nomeCasaTabela.textContent = dados.time_casa.toUpperCase();
            console.log(`✅ [JOGO${numeroJogo}] Nome time casa na tabela: ${dados.time_casa.toUpperCase()}`);
        } else {
            console.warn(`⚠️ [JOGO${numeroJogo}] Elemento não encontrado: time-casa-nome-${numeroJogo}-novo`);
        }
    }
    
    if (dados.time_fora) {
        const nomeFora = document.getElementById(ids.nomeFora);
        if (nomeFora) {
            nomeFora.textContent = dados.time_fora.toUpperCase();
        }
        
        // ATUALIZAR NOME DO TIME FORA NO CABEÇALHO DA TABELA
        const nomeForaTabela = document.getElementById(`time-fora-nome-${numeroJogo}-novo`);
        if (nomeForaTabela) {
            nomeForaTabela.textContent = dados.time_fora.toUpperCase();
            console.log(`✅ [JOGO${numeroJogo}] Nome time fora na tabela: ${dados.time_fora.toUpperCase()}`);
        } else {
            console.warn(`⚠️ [JOGO${numeroJogo}] Elemento não encontrado: time-fora-nome-${numeroJogo}-novo`);
        }
    }
    
    // 2. ATUALIZAR INFORMAÇÕES DO JOGO
    if (dados.arena && dados.campeonato && dados.dia) {
        const gameInfo = document.getElementById(ids.gameInfo);
        if (gameInfo) {
            gameInfo.textContent = `${dados.arena} | ${dados.campeonato} | ${dados.dia}`;
        }
    }
    
    // 3. ATUALIZAR PROBABILIDADES (SEGUINDO ESTRUTURA DO JOGO 5)
    const probCasa = dados.probabilidade_casa || dados.prob_casa;
    const probEmpate = dados.probabilidade_empate || dados.prob_empate;
    const probFora = dados.probabilidade_fora || dados.prob_fora;
    
    if (probCasa) {
        const elementoProbCasa = document.getElementById(ids.probCasa);
        if (elementoProbCasa) {
            elementoProbCasa.classList.remove('loading');
            elementoProbCasa.innerHTML = `<span class="probability-value">${probCasa}</span>`;
        }
    }
    
    if (probEmpate) {
        const elementoProbEmpate = document.getElementById(ids.probEmpate);
        if (elementoProbEmpate) {
            elementoProbEmpate.classList.remove('loading');
            elementoProbEmpate.innerHTML = `<span class="probability-value">${probEmpate}</span>`;
        }
    }
    
    if (probFora) {
        const elementoProbFora = document.getElementById(ids.probFora);
        if (elementoProbFora) {
            elementoProbFora.classList.remove('loading');
            elementoProbFora.innerHTML = `<span class="probability-value">${probFora}</span>`;
        }
    }
    
    // ATUALIZAR OS LABELS DOS TIMES NAS PROBABILIDADES
    if (dados.time_casa) {
        const labelCasa = document.getElementById(ids.labelCasa);
        if (labelCasa) {
            labelCasa.textContent = `Coluna 1 (${dados.time_casa})`;
        }
    }
    
    if (dados.time_fora) {
        const labelFora = document.getElementById(ids.labelFora);
        if (labelFora) {
            labelFora.textContent = `Coluna 2 (${dados.time_fora})`;
        }
    }
    
    // 4. ATUALIZAR RECOMENDAÇÃO
    if (dados.recomendacao) {
        const recomendacao = document.getElementById(ids.recomendacao);
        if (recomendacao) {
            recomendacao.innerHTML = `<strong>${dados.recomendacao}</strong>`;
        }
    }
    
    // 5. ATUALIZAR TABELA DE ANÁLISE
    if (dados.posicao_casa) {
        const posicaoCasa = document.getElementById(ids.posicaoCasa);
        if (posicaoCasa) {
            posicaoCasa.textContent = dados.posicao_casa + '°';
        }
    }
    
    if (dados.posicao_fora) {
        const posicaoFora = document.getElementById(ids.posicaoFora);
        if (posicaoFora) {
            posicaoFora.textContent = dados.posicao_fora + '°';
        }
    }
    
    // 6. ATUALIZAR CONFRONTO DIRETO (COM ESCUDOS) - DADOS REAIS DO JSON
    if (dados.confronto_direto) {
        const confrontoDireto = document.getElementById(ids.confrontoDireto);
        if (confrontoDireto) {
            console.log(`🔍 [JOGO${numeroJogo}] Confronto direto do JSON:`, dados.confronto_direto);
            
            // Parse do formato "8V-0E-2D" - DADOS REAIS
            const match = dados.confronto_direto.match(/(\d+)V-(\d+)E-(\d+)D/);
            if (match) {
                const vitorias = match[1];
                const empates = match[2];
                const derrotas = match[3];
                
                console.log(`📊 [JOGO${numeroJogo}] Parse confronto: ${vitorias}V-${empates}E-${derrotas}D`);
                
                confrontoDireto.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                        <img src="${dados.escudo_casa || '/static/escudos/placeholder.png'}" alt="${dados.time_casa || 'Time Casa'}" style="width: 24px; height: 24px; border-radius: 50%;">
                        <span style="font-weight: bold; color: #ffffff;">${vitorias}V</span>
                        <span style="color: #ffffff; font-weight: bold;">-</span>
                        <span style="color: #ffffff; font-weight: bold;">${empates}E</span>
                        <span style="color: #ffffff; font-weight: bold;">-</span>
                        <span style="font-weight: bold; color: #ffffff;">${derrotas}D</span>
                        <img src="${dados.escudo_fora || '/static/escudos/placeholder.png'}" alt="${dados.time_fora || 'Time Fora'}" style="width: 24px; height: 24px; border-radius: 50%;">
                    </div>
                `;
                console.log(`✅ [JOGO${numeroJogo}] Confronto direto atualizado com dados reais!`);
            }
        }
    }
    
    // 7. ATUALIZAR FATOR CASA
    if (dados.fator_casa) {
        const fatorCasa = document.getElementById(ids.fatorCasa);
        if (fatorCasa) {
            // CORRIGIDO: Não adicionar % se já contém %
            fatorCasa.textContent = dados.fator_casa.includes('%') ? dados.fator_casa : dados.fator_casa + '%';
        }
    }
    
    if (dados.fator_fora) {
        const fatorFora = document.getElementById(ids.fatorFora);
        if (fatorFora) {
            // CORRIGIDO: Não adicionar % se já contém %
            fatorFora.textContent = dados.fator_fora.includes('%') ? dados.fator_fora : dados.fator_fora + '%';
        }
    }
    
    // 8. ATUALIZAR ANÁLISES DA TABELA
    if (dados.analise_posicao) {
        const formaAnalise = document.getElementById(ids.formaAnalise);
        if (formaAnalise) {
            formaAnalise.textContent = dados.analise_posicao;
        }
    }
    
    if (dados.analise_posicao_tabelas) {
        const posicaoAnalise = document.getElementById(ids.posicaoAnalise);
        if (posicaoAnalise) {
            posicaoAnalise.textContent = dados.analise_posicao_tabelas;
        }
    }
    
    if (dados.analise_confronto_direto) {
        const h2hAnalise = document.getElementById(ids.h2hAnalise);
        if (h2hAnalise) {
            h2hAnalise.textContent = dados.analise_confronto_direto;
        }
    }
    
    if (dados.analise_fator_casa) {
        const fatorAnalise = document.getElementById(ids.fatorAnalise);
        if (fatorAnalise) {
            fatorAnalise.textContent = dados.analise_fator_casa;
        }
    }
    
    // 9. ATUALIZAR CONCLUSÃO DO ANALISTA - DADOS REAIS DO JSON
    if (dados.conclusao_analista) {
        const conclusaoAnalista = document.getElementById(ids.conclusaoAnalista);
        if (conclusaoAnalista) {
            console.log(`🔍 [JOGO${numeroJogo}] Conclusão do analista do JSON:`, dados.conclusao_analista.substring(0, 100) + '...');
            conclusaoAnalista.textContent = dados.conclusao_analista;
            console.log(`✅ [JOGO${numeroJogo}] Conclusão do analista atualizada com dados reais!`);
        } else {
            console.error(`❌ [JOGO${numeroJogo}] Elemento conclusao não encontrado com ID:`, ids.conclusaoAnalista);
        }
    } else {
        console.warn(`⚠️ [JOGO${numeroJogo}] Campo conclusao_analista não encontrado nos dados`);
    }
    
    console.log(`✅ [JOGO${numeroJogo}] Campos principais atualizados!`);
}

/**
 * CARREGAR E RENDERIZAR CONFRONTOS (DADOS DO CSV)
 * @param {number} numeroJogo - Número do jogo
 * @param {object} dados - Dados do jogo
 */
async function carregarERenderizarConfrontos(numeroJogo, dados) {
    console.log(`📊 [JOGO${numeroJogo}] Carregando confrontos do CSV...`);
    
    const jogoInfo = jogosMap[numeroJogo];
    if (!jogoInfo) {
        console.error(`❌ [JOGO${numeroJogo}] Jogo não encontrado no mapeamento!`);
        return;
    }
    
    const container = document.getElementById(`confrontos-principais-${numeroJogo}`);
    if (!container) {
        console.error(`❌ [JOGO${numeroJogo}] Container confrontos-principais-${numeroJogo} não encontrado!`);
        return;
    }
    
    try {
        // CARREGAR CSV
        const response = await fetch(`/api/confrontos/${jogoInfo.csv}`);
        if (!response.ok) {
            throw new Error(`Erro ao carregar CSV: ${response.status}`);
        }
        
        const csvText = await response.text();
        const linhas = csvText.split('\n').filter(linha => linha.trim());
        
        console.log(`📊 [JOGO${numeroJogo}] CSV carregado: ${linhas.length} linhas`);
        
        // PROCESSAR DADOS
        const confrontos = [];
        for (let i = 1; i < Math.min(linhas.length, 11); i++) { // Máximo 10 confrontos
            const colunas = linhas[i].split(',');
            if (colunas.length >= 4) {
                const data = colunas[0]?.trim();
                const placar = colunas[1]?.trim();
                const vencedor = colunas[2]?.trim();
                const competicao = colunas[3]?.trim();
                
                // DETERMINAR RESULTADO
                let resultado = 'E'; // Empate por padrão
                if (placar && placar.includes('x')) {
                    const [golsCasa, golsFora] = placar.split('x').map(g => parseInt(g.trim()));
                    if (golsCasa > golsFora) {
                        resultado = 'V';
                    } else if (golsFora > golsCasa) {
                        resultado = 'D';
                    }
                } else if (vencedor && vencedor !== 'Empate') {
                    if (vencedor === jogoInfo.casa) {
                        resultado = 'V';
                    } else if (vencedor === jogoInfo.fora) {
                        resultado = 'D';
                    }
                }
                
                confrontos.push({
                    data: data || 'Data não disponível',
                    placar: placar || 'N/A',
                    resultado: resultado,
                    competicao: competicao || 'Competição não disponível'
                });
            }
        }
        
        // RENDERIZAR HTML
        let htmlConfrontos = '';
        confrontos.forEach((confronto, index) => {
            const corBolinha = confronto.resultado === 'V' ? 'green' : 
                              confronto.resultado === 'D' ? 'red' : 'gray';
            
            htmlConfrontos += `
                <div class="confronto-box">
                    <div class="confronto-data">${confronto.data}</div>
                    <div class="confronto-placar">${confronto.placar}</div>
                    <div class="confronto-resultado ${corBolinha}">${confronto.resultado}</div>
                    <div class="confronto-competicao">${confronto.competicao}</div>
                </div>
            `;
        });
        
        // PREENCHER CONTAINER
        container.innerHTML = htmlConfrontos;
        
        console.log(`✅ [JOGO${numeroJogo}] ${confrontos.length} confrontos renderizados!`);
        
    } catch (error) {
        console.error(`❌ [JOGO${numeroJogo}] Erro ao carregar confrontos:`, error);
        
        // FALLBACK: Dados hardcoded
        const fallbackHtml = `
            <div class="confronto-box">
                <div class="confronto-data">Data não disponível</div>
                <div class="confronto-placar">N/A</div>
                <div class="confronto-resultado gray">E</div>
                <div class="confronto-competicao">Competição não disponível</div>
            </div>
        `;
        
        container.innerHTML = fallbackHtml;
        console.log(`🔄 [JOGO${numeroJogo}] Usando dados de fallback`);
    }
}

/**
 * FUNÇÃO ESPECÍFICA PARA CARREGAR DADOS DO JOGO 5
 * Usa a estrutura específica do jogo_5.json
 */
async function carregarDadosJogo5() {
    console.log('🎯 [JOGO5] Iniciando carregamento específico do JOGO 5...');
    
    try {
        // 1. CARREGAR DADOS DO JSON
        console.log('📊 [JOGO5] Carregando análise JSON...');
        const response = await fetch('/api/analise/jogo/5?concurso=concurso_1216');
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const responseData = await response.json();
        console.log('✅ [JOGO5] Dados JSON carregados:', responseData);
        
        // 2. ATUALIZAR CAMPOS PRINCIPAIS
        await atualizarCamposPrincipais(5, responseData);
        
        // 3. CARREGAR CONFRONTOS DO CSV
        await carregarERenderizarConfrontos(5, responseData);
        
        console.log('🎉 [JOGO5] Carregamento completo finalizado!');
        
    } catch (error) {
        console.error('❌ [JOGO5] Erro no carregamento:', error);
        
        // FALLBACK: Dados hardcoded - DADOS REAIS DO jogo_5.json
        const dadosFallback = {
            dados: {
                time_casa: 'ATLETICO MADRID',
                time_fora: 'OSASUNA',
                arena: 'estádio Riyadh Air Metropolitano - Madri',
                campeonato: 'La Liga',
                dia: 'Sábado',
                escudo_casa: '/static/escudos/Atletico-de-Madrid/atletico-de-madrid.png',
                escudo_fora: '/static/escudos/Osasuna/osasuna.png',
                probabilidade_casa: '80',
                probabilidade_empate: '10',
                probabilidade_fora: '10',
                recomendacao: 'Recomendação Estatística: Coluna 1 (ATLETICO MADRID) - Risco Baixo',
                posicao_casa: '5',
                posicao_fora: '12',
                confronto_direto: '8V-0E-2D', // DADOS REAIS DO JSON
                fator_casa: '90',
                fator_fora: '10',
                analise_posicao: 'Vantagem Atletico de madrid',
                analise_posicao_tabelas: 'Vantagem Atletico de madrid',
                analise_confronto_direto: 'Vantagem Atletico de madrid',
                analise_fator_casa: 'Vantagem Atletico de madrid',
                conclusao_analista: 'O retrospecto recente é avassalador a favor do Atleti. Nos últimos 20 confrontos diretos, o Atlético de Madrid venceu 16 vezes, contra apenas 3 vitórias do Osasuna e 1 único empate. Isso demonstra um desequilíbrio psicológico e técnico muito grande neste duelo.\n\nFase Atual (Tabela de Classificação):\n\nO Atlético de Madrid (5º lugar, 13 Pts) está em melhor condição na tabela, brigando por vaga europeia.\n\nO Osasuna (12º lugar, 10 Pts) está na zona intermediária e, mais importante, vem em péssima fase, com 4 derrotas e 1 empate nos últimos 5 jogos (como visto na coluna "Últimas 5" da tabela).'
            }
        };
        
        await atualizarCamposPrincipais(5, dadosFallback);
        await carregarERenderizarConfrontos(5, dadosFallback);
    }
}


// EXPORTAR FUNÇÕES PARA USO GLOBAL
window.carregarDadosCompletosJogo = carregarDadosCompletosJogo;
window.carregarDadosJogo5 = carregarDadosJogo5;
window.jogosMap = jogosMap;
window.escudosMap = escudosMap;
window.setText = setText;
window.setHTML = setHTML;
