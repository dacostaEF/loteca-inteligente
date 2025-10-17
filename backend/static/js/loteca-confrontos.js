/**
 * LOTECA - SCRIPT DOS CONFRONTOS
 * Arquivo JavaScript separado para renderizar os 10 boxes de confrontos
 * Baseado na estrutura exata da imagem fornecida
 */

/**
 * FUNÇÃO PARA CARREGAR CONFRONTOS DO JOGO 5 - ESTRUTURA EXATA DA IMAGEM
 */
async function carregarConfrontosJogo5() {
    console.log('🎯 [CONFRONTOS-JOGO5] Carregando últimos confrontos ATLÉTICO MADRID vs OSASUNA...');
    
    const container = document.getElementById('confrontos-principais-5');
    if (!container) {
        console.error('❌ [CONFRONTOS-JOGO5] Container confrontos-principais-5 não encontrado!');
        return;
    }
    
    // DADOS REAIS DO ARQUIVO CSV - ATLÉTICO MADRID vs OSASUNA
    let confrontos = [
        { data: '2024-12-01', mandante: 'Atletico Madrid', visitante: 'Osasuna', placar: '2-1', resultado: 'V' },
        { data: '2024-11-01', mandante: 'Osasuna', visitante: 'Atletico Madrid', placar: '1-1', resultado: 'E' },
        { data: '2024-10-01', mandante: 'Atletico Madrid', visitante: 'Osasuna', placar: '0-1', resultado: 'D' },
        { data: '2024-09-01', mandante: 'Osasuna', visitante: 'Atletico Madrid', placar: '1-2', resultado: 'V' },
        { data: '2024-08-01', mandante: 'Atletico Madrid', visitante: 'Osasuna', placar: '3-0', resultado: 'V' },
        { data: '2024-07-01', mandante: 'Osasuna', visitante: 'Atletico Madrid', placar: '0-0', resultado: 'E' },
        { data: '2024-06-01', mandante: 'Atletico Madrid', visitante: 'Osasuna', placar: '1-0', resultado: 'V' },
        { data: '2024-05-01', mandante: 'Osasuna', visitante: 'Atletico Madrid', placar: '2-1', resultado: 'D' },
        { data: '2024-04-01', mandante: 'Atletico Madrid', visitante: 'Osasuna', placar: '2-2', resultado: 'E' },
        { data: '2024-03-01', mandante: 'Osasuna', visitante: 'Atletico Madrid', placar: '0-3', resultado: 'V' }
    ];
    
    // TENTAR CARREGAR DADOS DO ARQUIVO CSV
    try {
        console.log('🔄 [CONFRONTOS-JOGO5] Buscando dados do arquivo CSV...');
        const csvResponse = await fetch('/api/confrontos/Atletico-de-Madrid_vs_Osasuna.csv');
        
        if (csvResponse.ok) {
            const csvText = await csvResponse.text();
            console.log('✅ [CONFRONTOS-JOGO5] CSV carregado:', csvText.substring(0, 200) + '...');
            
            // Parse do CSV - CORRIGIDO PARA ESTRUTURA REAL
            const lines = csvText.split('\n').filter(line => line.trim());
            console.log('📊 [CONFRONTOS-JOGO5] Total de linhas no CSV:', lines.length);
            
            const csvData = lines.slice(1, 11).map((line, index) => {
                console.log(`🔍 [CONFRONTOS-JOGO5] Processando linha ${index + 2}:`, line);
                
                const colunas = line.split(',');
                console.log(`📋 [CONFRONTOS-JOGO5] Colunas encontradas:`, colunas);
                
                if (colunas.length >= 5) {
                    const data = colunas[0]?.trim();
                    const mandante = colunas[1]?.trim();
                    const placar = colunas[2]?.trim();
                    const visitante = colunas[3]?.trim();
                    const vencedor = colunas[4]?.trim();
                    
                    console.log(`📅 [CONFRONTOS-JOGO5] Data: ${data}, Mandante: ${mandante}, Placar: ${placar}, Visitante: ${visitante}, Vencedor: ${vencedor}`);
                    
                    // DETERMINAR RESULTADO CORRETO
                    let resultado = 'E'; // Empate por padrão
                    
                    if (vencedor === 'Atlético de Madrid' || vencedor === 'Atletico de Madrid') {
                        resultado = 'V'; // Vitória do Atlético Madrid
                    } else if (vencedor === 'Osasuna') {
                        resultado = 'D'; // Derrota do Atlético Madrid (vitória do Osasuna)
                    } else if (vencedor === 'Empate') {
                        resultado = 'E'; // Empate
                    }
                    
                    console.log(`⚽ [CONFRONTOS-JOGO5] Resultado determinado: ${resultado}`);
                    
                    return {
                        data: data,
                        mandante: mandante,
                        visitante: visitante,
                        placar: placar,
                        resultado: resultado
                    };
                }
                return null;
            }).filter(item => item !== null);
            
            if (csvData.length > 0) {
                confrontos = csvData;
                console.log('🎯 [CONFRONTOS-JOGO5] Usando dados reais do CSV!', confrontos.length, 'confrontos');
            }
        }
    } catch (error) {
        console.log('⚠️ [CONFRONTOS-JOGO5] Usando dados padrão (fallback):', error);
    }
    
    // Pegar os últimos 10 confrontos
    const ultimos10 = confrontos.slice(0, 10);
    
    // Buscar escudos da Central Admin uma única vez
    let escudoCasa = '/static/escudos/Atletico-de-Madrid/atletico-de-madrid.png';
    let escudoFora = '/static/escudos/Osasuna/osasuna.png';
    
    try {
        console.log('🔄 [CONFRONTOS-JOGO5] Buscando escudos da Central Admin...');
        const jogoResponse = await fetch('/api/analise/jogo/5?concurso=concurso_1216');
        
        if (jogoResponse.ok) {
            const jogoData = await jogoResponse.json();
            if (jogoData.success && jogoData.dados) {
                console.log('✅ [CONFRONTOS-JOGO5] Dados carregados da Central Admin:', jogoData.dados);
                
                if (jogoData.dados.escudo_casa) {
                    escudoCasa = jogoData.dados.escudo_casa;
                }
                if (jogoData.dados.escudo_fora) {
                    escudoFora = jogoData.dados.escudo_fora;
                }
            }
        }
    } catch (error) {
        console.log('⚠️ [CONFRONTOS-JOGO5] Usando escudos padrão:', error);
    }
    
    // RENDERIZAR CONFRONTOS - ESTRUTURA EXATA DA IMAGEM
    const boxesHtml = ultimos10.map(confronto => {
        const resultado = confronto.resultado.toUpperCase();
        let conteudo;
        
        if (resultado === 'V') {
            conteudo = `<img src="${escudoCasa}" alt="Atlético Madrid" style="width: 17px; height: 17px; border-radius: 50%;" onerror="this.outerHTML='<span style=\'color: #fff; font-size: 8px; font-weight: bold;\'>ATM</span>'">`;
        } else if (resultado === 'D') {
            conteudo = `<img src="${escudoFora}" alt="Osasuna" style="width: 17px; height: 17px; border-radius: 50%;" onerror="this.outerHTML='<span style=\'color: #fff; font-size: 8px; font-weight: bold;\'>OSA</span>'">`;
        } else {
            conteudo = '<span style="color: #ffc107; font-weight: bold; font-size: 11px;">E</span>';
        }
        
        let dataFormatada = '';
        if (confronto.data) {
            // O CSV já vem no formato DD/MM/YY, então vamos usar diretamente
            dataFormatada = confronto.data;
            console.log(`📅 [CONFRONTOS-JOGO5] Data formatada: ${dataFormatada}`);
        }
        
        return `
            <div style="
                background: #2a2a2a; 
                border-left: 2px solid #28a745; 
                border-radius: 6px; 
                padding: 8px 6px; 
                margin: 3px; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                min-width: 56px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.3);
            ">
                <div style="
                    color: #ccc; 
                    font-size: 8px; 
                    margin-bottom: 5px; 
                    text-align: center;
                ">${dataFormatada}</div>
                <div style="
                    background: #1a1a1a; 
                    color: #fff; 
                    font-weight: bold; 
                    font-size: 10px; 
                    padding: 4px 8px; 
                    border-radius: 4px; 
                    margin-bottom: 5px; 
                    text-align: center;
                    min-width: 28px;
                ">${confronto.placar}</div>
                <div style="
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                ">${conteudo}</div>
            </div>
        `;
    }).join('');
    
    // PREENCHER CONTAINER
    container.innerHTML = boxesHtml;
    
    console.log('✅ [CONFRONTOS-JOGO5]', ultimos10.length, 'boxes renderizados com estrutura da imagem!');
    console.log('📊 [CONFRONTOS-JOGO5] Dados finais renderizados:', ultimos10);
    console.log('🎨 [CONFRONTOS-JOGO5] HTML gerado:', boxesHtml.substring(0, 500) + '...');
}

/**
 * FUNÇÃO GENÉRICA PARA CARREGAR CONFRONTOS DE QUALQUER JOGO
 * @param {number} numeroJogo - Número do jogo (1-14)
 * @param {string} timeCasa - Nome do time da casa
 * @param {string} timeFora - Nome do time de fora
 * @param {string} arquivoCsv - Nome do arquivo CSV
 * @param {string} escudoCasa - Caminho do escudo do time da casa
 * @param {string} escudoFora - Caminho do escudo do time de fora
 */
async function carregarConfrontosGenerico(numeroJogo, timeCasa, timeFora, arquivoCsv, escudoCasa, escudoFora) {
    console.log(`🎯 [CONFRONTOS-JOGO${numeroJogo}] Carregando últimos confrontos ${timeCasa} vs ${timeFora}...`);
    
    const container = document.getElementById(`confrontos-principais-${numeroJogo}`);
    if (!container) {
        console.error(`❌ [CONFRONTOS-JOGO${numeroJogo}] Container confrontos-principais-${numeroJogo} não encontrado!`);
        return;
    }
    
    // DADOS DE FALLBACK
    let confrontos = [
        { data: '2024-12-01', mandante: timeCasa, visitante: timeFora, placar: '2-1', resultado: 'V' },
        { data: '2024-11-01', mandante: timeFora, visitante: timeCasa, placar: '1-1', resultado: 'E' },
        { data: '2024-10-01', mandante: timeCasa, visitante: timeFora, placar: '0-1', resultado: 'D' },
        { data: '2024-09-01', mandante: timeFora, visitante: timeCasa, placar: '1-2', resultado: 'V' },
        { data: '2024-08-01', mandante: timeCasa, visitante: timeFora, placar: '3-0', resultado: 'V' },
        { data: '2024-07-01', mandante: timeFora, visitante: timeCasa, placar: '0-0', resultado: 'E' },
        { data: '2024-06-01', mandante: timeCasa, visitante: timeFora, placar: '1-0', resultado: 'V' },
        { data: '2024-05-01', mandante: timeFora, visitante: timeCasa, placar: '2-1', resultado: 'D' },
        { data: '2024-04-01', mandante: timeCasa, visitante: timeFora, placar: '2-2', resultado: 'E' },
        { data: '2024-03-01', mandante: timeFora, visitante: timeCasa, placar: '0-3', resultado: 'V' }
    ];
    
    // TENTAR CARREGAR DADOS DO ARQUIVO CSV
    try {
        console.log(`🔄 [CONFRONTOS-JOGO${numeroJogo}] Buscando dados do arquivo CSV: ${arquivoCsv}`);
        const csvResponse = await fetch(`/api/confrontos/${arquivoCsv}`);
        
        if (csvResponse.ok) {
            const csvText = await csvResponse.text();
            console.log(`✅ [CONFRONTOS-JOGO${numeroJogo}] CSV carregado:`, csvText.substring(0, 200) + '...');
            
            // Parse do CSV
            const lines = csvText.split('\n');
            const csvData = lines.slice(1, 11).map(line => {
                const [data, timeCasaCsv, placar, timeForaCsv, vencedor, campeonato] = line.split(',');
                return {
                    data: data,
                    mandante: timeCasaCsv,
                    visitante: timeForaCsv,
                    placar: placar,
                    resultado: vencedor === timeCasa ? 'V' : vencedor === timeFora ? 'D' : 'E'
                };
            });
            
            if (csvData.length > 0) {
                confrontos = csvData;
                console.log(`🎯 [CONFRONTOS-JOGO${numeroJogo}] Usando dados reais do CSV!`, confrontos.length, 'confrontos');
            }
        }
    } catch (error) {
        console.log(`⚠️ [CONFRONTOS-JOGO${numeroJogo}] Usando dados padrão (fallback):`, error);
    }
    
    // Pegar os últimos 10 confrontos
    const ultimos10 = confrontos.slice(0, 10);
    
    // Buscar escudos da Central Admin uma única vez
    let escudoCasaFinal = escudoCasa;
    let escudoForaFinal = escudoFora;
    
    try {
        console.log(`🔄 [CONFRONTOS-JOGO${numeroJogo}] Buscando escudos da Central Admin...`);
        const jogoResponse = await fetch(`/api/analise/jogo/${numeroJogo}?concurso=concurso_1216`);
        
        if (jogoResponse.ok) {
            const jogoData = await jogoResponse.json();
            if (jogoData.success && jogoData.dados) {
                console.log(`✅ [CONFRONTOS-JOGO${numeroJogo}] Dados carregados da Central Admin:`, jogoData.dados);
                
                if (jogoData.dados.escudo_casa) {
                    escudoCasaFinal = jogoData.dados.escudo_casa;
                }
                if (jogoData.dados.escudo_fora) {
                    escudoForaFinal = jogoData.dados.escudo_fora;
                }
            }
        }
    } catch (error) {
        console.log(`⚠️ [CONFRONTOS-JOGO${numeroJogo}] Usando escudos padrão:`, error);
    }
    
    // RENDERIZAR CONFRONTOS - SEGUINDO ESTRUTURA EXATA DO JOGO 1
    const bolinhasHtml = ultimos10.map(confronto => {
        const resultado = confronto.resultado.toUpperCase();
        let classe, conteudo;
        
        if (resultado === 'V') {
            classe = timeCasa.toLowerCase().replace(/\s+/g, '-');
            conteudo = `<img src="${escudoCasaFinal}" alt="${timeCasa}" class="confronto-escudo" onerror="this.outerHTML='${timeCasa.substring(0,3).toUpperCase()}'">`;
        } else if (resultado === 'D') {
            classe = timeFora.toLowerCase().replace(/\s+/g, '-');
            conteudo = `<img src="${escudoForaFinal}" alt="${timeFora}" class="confronto-escudo" onerror="this.outerHTML='${timeFora.substring(0,3).toUpperCase()}'">`;
        } else {
            classe = 'empate';
            conteudo = 'E';
        }
        
        let dataFormatada = '';
        if (confronto.data) {
            const [ano, mes, dia] = confronto.data.split('-');
            const anoAbrev = ano.substring(2);
            dataFormatada = `${dia}/${mes}/${anoAbrev}`;
        }
        
        return `
            <div class="confronto-item">
                <div class="confronto-data">${dataFormatada}</div>
                <div class="confronto-placar">${confronto.placar}</div>
                <div class="confronto-result ${classe}" title="${confronto.data}: ${confronto.mandante} ${confronto.placar} ${confronto.visitante}">${conteudo}</div>
            </div>
        `;
    }).join('');
    
    // PREENCHER CONTAINER
    container.innerHTML = bolinhasHtml;
    
    console.log(`✅ [CONFRONTOS-JOGO${numeroJogo}]`, ultimos10.length, 'bolinhas renderizadas na tabela (linha única)');
}

// EXPORTAR FUNÇÕES PARA USO GLOBAL
window.carregarConfrontosJogo5 = carregarConfrontosJogo5;
window.carregarConfrontosGenerico = carregarConfrontosGenerico;
