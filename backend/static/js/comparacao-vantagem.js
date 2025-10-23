/**
 * COMPARAÇÃO DE VANTAGENS - FLAMENGO VS PALMEIRAS
 * Sistema de comparação automática para determinar vantagens estatísticas
 */

// Cria o badge de vantagem (amarelo)
function criarBadgeVantagem(texto, classe) {
    const box = document.createElement('div');
    box.className = 'vantagem-badge ' + (classe || 'is-neutro');
    box.innerHTML = `<span>${texto}</span>`;
    return box;
}

// Renderiza vantagem na NOVA ESTRUTURA (limpa antes)
function renderVantagem(targetId, texto, classe) {
    console.log(`🎯 [RENDER] Renderizando vantagem: ${targetId} = ${texto}`);
    
    // Mapear ID da estrutura antiga para nova estrutura
    const novoId = targetId.replace('vencedor-', 'vantagem-');
    const alvo = document.getElementById(novoId);
    
    if (!alvo) {
        console.error(`❌ [RENDER] Elemento ${novoId} não encontrado`);
        return;
    }
    
    console.log(`✅ [RENDER] Elemento ${novoId} encontrado`);
    console.log(`🔍 [RENDER] Conteúdo atual: ${alvo.innerHTML}`);
    
    // Limpar completamente a coluna vantagem
    alvo.innerHTML = '';
    
    // Criar e inserir o badge
    const badge = criarBadgeVantagem(texto, classe);
    alvo.appendChild(badge);
    
    console.log(`✅ [RENDER] Badge inserido na nova estrutura`);
    console.log(`🔍 [RENDER] Conteúdo final: ${alvo.innerHTML}`);
}

// ATUALIZAR VANTAGEM (USANDO RENDER DIRETO)
function atualizarVantagem(id, vencedor, cor) {
    console.log(`🔍 [VANTAGEM] Atualizando vantagem: ${id}`);
    const texto = vencedor; // Removido apenas "Vantagem:"
    
    // Mapear cor para classe
    let classe = 'is-neutro';
    if (cor === 'vermelho') classe = 'is-flamengo';
    if (cor === 'verde') classe = 'is-palmeiras';
    if (cor === 'amarelo') classe = 'is-neutro';
    
    renderVantagem(id, texto, classe);
}


// COMPARAR E DETERMINAR VANTAGEM
function compararEAtualizarVantagem(timeMandante, timeVisitante) {
    console.log('🔍 [COMPARACAO] Comparando dados para determinar vantagens...');
    console.log('🔍 [COMPARACAO] Mandante:', timeMandante.Time);
    console.log('🔍 [COMPARACAO] Visitante:', timeVisitante.Time);
    
    // TESTE: Verificar se os elementos existem
    console.log('🔍 [DEBUG-TESTE] Verificando elementos da tabela...');
    const testeElemento = document.getElementById('vencedor-posicao');
    console.log('🔍 [DEBUG-TESTE] Elemento vencedor-posicao:', testeElemento);
    
    if (testeElemento) {
        console.log('✅ [DEBUG-TESTE] Elemento encontrado!');
        console.log('🔍 [DEBUG-TESTE] Conteúdo atual:', testeElemento.innerHTML);
    } else {
        console.error('❌ [DEBUG-TESTE] Elemento vencedor-posicao NÃO encontrado!');
        console.log('🔍 [DEBUG-TESTE] Tentando buscar todos os elementos com "vencedor"...');
        const todosVencedores = document.querySelectorAll('[id*="vencedor"]');
        console.log('🔍 [DEBUG-TESTE] Elementos encontrados:', todosVencedores.length);
        todosVencedores.forEach((el, index) => {
            console.log(`🔍 [DEBUG-TESTE] ${index + 1}: ${el.id} - ${el.innerHTML}`);
        });
    }
    
    // POSIÇÃO (menor é melhor)
    const mandantePos = parseInt(timeMandante['Posição']);
    const visitantePos = parseInt(timeVisitante['Posição']);
    console.log(`🔍 [POSICAO] ${timeMandante.Time}: ${mandantePos}º, ${timeVisitante.Time}: ${visitantePos}º`);
    
    if (mandantePos < visitantePos) {
        console.log(`✅ [POSICAO] ${timeMandante.Time} tem vantagem (${mandantePos}º < ${visitantePos}º)`);
        atualizarVantagem('vencedor-posicao', timeMandante.Time, 'vermelho');
    } else if (visitantePos < mandantePos) {
        console.log(`✅ [POSICAO] ${timeVisitante.Time} tem vantagem (${visitantePos}º < ${mandantePos}º)`);
        atualizarVantagem('vencedor-posicao', timeVisitante.Time, 'verde');
    } else {
        console.log(`✅ [POSICAO] Empate (${mandantePos}º = ${visitantePos}º)`);
        atualizarVantagem('vencedor-posicao', 'Empate', 'amarelo');
    }

    // GOLS PRÓ (maior é melhor)
    const mandanteGolsPro = parseFloat(timeMandante['Média Gols Pró']);
    const visitanteGolsPro = parseFloat(timeVisitante['Média Gols Pró']);
    console.log(`🔍 [GOLS-PRO] ${timeMandante.Time}: ${mandanteGolsPro}, ${timeVisitante.Time}: ${visitanteGolsPro}`);
    
    if (mandanteGolsPro > visitanteGolsPro) {
        console.log(`✅ [GOLS-PRO] ${timeMandante.Time} tem vantagem (${mandanteGolsPro} > ${visitanteGolsPro})`);
        atualizarVantagem('vencedor-gols-pro', timeMandante.Time, 'vermelho');
    } else if (visitanteGolsPro > mandanteGolsPro) {
        console.log(`✅ [GOLS-PRO] ${timeVisitante.Time} tem vantagem (${visitanteGolsPro} > ${mandanteGolsPro})`);
        atualizarVantagem('vencedor-gols-pro', timeVisitante.Time, 'verde');
    } else {
        console.log(`✅ [GOLS-PRO] Empate (${mandanteGolsPro} = ${visitanteGolsPro})`);
        atualizarVantagem('vencedor-gols-pro', 'Empate', 'amarelo');
    }

    // GOLS CONTRA (menor é melhor)
    const mandanteGolsContra = parseFloat(timeMandante['Média Gols Contra']);
    const visitanteGolsContra = parseFloat(timeVisitante['Média Gols Contra']);
    if (mandanteGolsContra < visitanteGolsContra) {
        atualizarVantagem('vencedor-gols-contra', timeMandante.Time, 'vermelho');
    } else if (visitanteGolsContra < mandanteGolsContra) {
        atualizarVantagem('vencedor-gols-contra', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-gols-contra', 'Empate', 'amarelo');
    }

    // OVER 2.5 (maior é melhor)
    const flaOver25 = parseFloat(timeMandante['Over 2.5']);
    const palOver25 = parseFloat(timeVisitante['Over 2.5']);
    if (flaOver25 > palOver25) {
        atualizarVantagem('vencedor-over25', timeMandante.Time, 'vermelho');
    } else if (palOver25 > flaOver25) {
        atualizarVantagem('vencedor-over25', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-over25', 'Empate', 'amarelo');
    }

    // BTTS (maior é melhor)
    const flaBtts = parseFloat(timeMandante['BTTS']);
    const palBtts = parseFloat(timeVisitante['BTTS']);
    if (flaBtts > palBtts) {
        atualizarVantagem('vencedor-btts', timeMandante.Time, 'vermelho');
    } else if (palBtts > flaBtts) {
        atualizarVantagem('vencedor-btts', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-btts', 'Empate', 'amarelo');
    }

    // CLEAN SHEET (maior é melhor)
    const flaClean = parseFloat(timeMandante['Clean Sheet']);
    const palClean = parseFloat(timeVisitante['Clean Sheet']);
    if (flaClean > palClean) {
        atualizarVantagem('vencedor-clean', timeMandante.Time, 'vermelho');
    } else if (palClean > flaClean) {
        atualizarVantagem('vencedor-clean', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-clean', 'Empate', 'amarelo');
    }

    // GOLS SOFRIDOS TOTAL (menor é melhor)
    const flaGolsSofridos = parseInt(timeMandante['Gols Sofridos Total']);
    const palGolsSofridos = parseInt(timeVisitante['Gols Sofridos Total']);
    if (flaGolsSofridos < palGolsSofridos) {
        atualizarVantagem('vencedor-gols-sofridos', timeMandante.Time, 'vermelho');
    } else if (palGolsSofridos < flaGolsSofridos) {
        atualizarVantagem('vencedor-gols-sofridos', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-gols-sofridos', 'Empate', 'amarelo');
    }

    // PONTOS ÚLTIMOS 5 (maior é melhor)
    const flaPontosUltimos = parseInt(timeMandante['Pontos Últimos 5']);
    const palPontosUltimos = parseInt(timeVisitante['Pontos Últimos 5']);
    if (flaPontosUltimos > palPontosUltimos) {
        atualizarVantagem('vencedor-pontos-ultimos', timeMandante.Time, 'vermelho');
    } else if (palPontosUltimos > flaPontosUltimos) {
        atualizarVantagem('vencedor-pontos-ultimos', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-pontos-ultimos', 'Empate', 'amarelo');
    }

    // CASA - JOGOS (maior é melhor)
    const flaCasaJogos = parseFloat(timeMandante['Casa - Jogos']);
    const palCasaJogos = parseFloat(timeVisitante['Casa - Jogos']);
    if (flaCasaJogos > palCasaJogos) {
        atualizarVantagem('vencedor-casa-jogos', timeMandante.Time, 'vermelho');
    } else if (palCasaJogos > flaCasaJogos) {
        atualizarVantagem('vencedor-casa-jogos', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-casa-jogos', 'Empate', 'amarelo');
    }

    // CASA - GOLS PRÓ (maior é melhor)
    const flaCasaGolsPro = parseFloat(timeMandante['Casa - Gols Pró']);
    const palCasaGolsPro = parseFloat(timeVisitante['Casa - Gols Pró']);
    if (flaCasaGolsPro > palCasaGolsPro) {
        atualizarVantagem('vencedor-casa-gols-pro', timeMandante.Time, 'vermelho');
    } else if (palCasaGolsPro > flaCasaGolsPro) {
        atualizarVantagem('vencedor-casa-gols-pro', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-casa-gols-pro', 'Empate', 'amarelo');
    }

    // CASA - GOLS CONTRA (menor é melhor)
    const flaCasaGolsContra = parseFloat(timeMandante['Casa - Gols Contra']);
    const palCasaGolsContra = parseFloat(timeVisitante['Casa - Gols Contra']);
    if (flaCasaGolsContra < palCasaGolsContra) {
        atualizarVantagem('vencedor-casa-gols-contra', timeMandante.Time, 'vermelho');
    } else if (palCasaGolsContra < flaCasaGolsContra) {
        atualizarVantagem('vencedor-casa-gols-contra', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-casa-gols-contra', 'Empate', 'amarelo');
    }

    // FORA - JOGOS (maior é melhor)
    const flaForaJogos = parseFloat(timeMandante['Fora - Jogos']);
    const palForaJogos = parseFloat(timeVisitante['Fora - Jogos']);
    if (flaForaJogos > palForaJogos) {
        atualizarVantagem('vencedor-fora-jogos', timeMandante.Time, 'vermelho');
    } else if (palForaJogos > flaForaJogos) {
        atualizarVantagem('vencedor-fora-jogos', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-fora-jogos', 'Empate', 'amarelo');
    }

    // FORA - GOLS PRÓ (maior é melhor)
    const flaForaGolsPro = parseFloat(timeMandante['Fora - Gols Pró']);
    const palForaGolsPro = parseFloat(timeVisitante['Fora - Gols Pró']);
    if (flaForaGolsPro > palForaGolsPro) {
        atualizarVantagem('vencedor-fora-gols-pro', timeMandante.Time, 'vermelho');
    } else if (palForaGolsPro > flaForaGolsPro) {
        atualizarVantagem('vencedor-fora-gols-pro', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-fora-gols-pro', 'Empate', 'amarelo');
    }

    // FORA - GOLS CONTRA (menor é melhor)
    const flaForaGolsContra = parseFloat(timeMandante['Fora - Gols Contra']);
    const palForaGolsContra = parseFloat(timeVisitante['Fora - Gols Contra']);
    if (flaForaGolsContra < palForaGolsContra) {
        atualizarVantagem('vencedor-fora-gols-contra', timeMandante.Time, 'vermelho');
    } else if (palForaGolsContra < flaForaGolsContra) {
        atualizarVantagem('vencedor-fora-gols-contra', timeVisitante.Time, 'verde');
    } else {
        atualizarVantagem('vencedor-fora-gols-contra', 'Empate', 'amarelo');
    }

    console.log('✅ [COMPARACAO] Todas as vantagens foram determinadas!');
    
    // PLANO B: Executar correção final após 1 segundo
    setTimeout(() => {
        console.log('🔧 [PLANO-B] Executando correção final...');
        corrigirPosicionamentoBadges();
        
        // TESTE FINAL: Verificar se pelo menos um elemento foi atualizado
        const elementoTeste = document.getElementById('vencedor-posicao');
        if (elementoTeste) {
            console.log('🔍 [TESTE-FINAL] Elemento vencedor-posicao após atualização:', elementoTeste.innerHTML);
        } else {
            console.error('❌ [TESTE-FINAL] Elemento vencedor-posicao não encontrado após atualização!');
        }
    }, 1000);
}

// AVALIAÇÃO AUTOMÁTICA POR PAR DE DADOS
function avaliarParDados(mandanteValor, visitanteValor, categoriaId, tipoComparacao = 'maior', timeMandante, timeVisitante) {
    console.log(`🔍 [AUTO-PAR] ${categoriaId}: ${timeMandante.Time}=${mandanteValor}, ${timeVisitante.Time}=${visitanteValor} (${tipoComparacao})`);
    
    let vencedor, cor;
    
    if (tipoComparacao === 'maior') {
        if (mandanteValor > visitanteValor) {
            vencedor = timeMandante.Time;
            cor = 'vermelho';
        } else if (visitanteValor > mandanteValor) {
            vencedor = timeVisitante.Time;
            cor = 'verde';
        } else {
            vencedor = 'Empate';
            cor = 'amarelo';
        }
    } else if (tipoComparacao === 'menor') {
        if (mandanteValor < visitanteValor) {
            vencedor = timeMandante.Time;
            cor = 'vermelho';
        } else if (visitanteValor < mandanteValor) {
            vencedor = timeVisitante.Time;
            cor = 'verde';
        } else {
            vencedor = 'Empate';
            cor = 'amarelo';
        }
    }
    
    console.log(`✅ [AUTO-PAR] ${categoriaId}: Vantagem=${vencedor} (${cor})`);
    atualizarVantagem(categoriaId, vencedor, cor);
}

// PLANO B: Varredura final para mover badges da coluna errada
function corrigirPosicionamentoBadges() {
    console.log('🔧 [PLANO-B] Iniciando varredura final para corrigir posicionamento...');
    
    document.querySelectorAll('.stat-row').forEach((row, index) => {
        console.log(`🔍 [PLANO-B] Verificando linha ${index + 1}...`);
        
        // Buscar badge na coluna 1 (errado)
        const badge = row.querySelector('.vantagem-badge');
        const destino = row.querySelector('.vencedor-indicator');
        
        if (badge && destino && !destino.contains(badge)) {
            console.log(`🔧 [PLANO-B] Movendo badge da coluna 1 para coluna 4 na linha ${index + 1}`);
            
            // Limpar destino
            destino.innerHTML = '';
            destino.style.cssText = `
                text-align: center;
                padding: 8px;
                vertical-align: middle;
            `;
            
            // Mover badge
            destino.appendChild(badge);
            
            console.log(`✅ [PLANO-B] Badge movido com sucesso!`);
        } else if (badge && destino && destino.contains(badge)) {
            console.log(`✅ [PLANO-B] Badge já está na posição correta na linha ${index + 1}`);
        } else {
            console.log(`🔍 [PLANO-B] Nenhum badge encontrado na linha ${index + 1}`);
        }
    });
    
    console.log('✅ [PLANO-B] Varredura final concluída!');
}

// EXPORTAR FUNÇÕES PARA USO GLOBAL
window.atualizarVantagem = atualizarVantagem;
window.compararEAtualizarVantagem = compararEAtualizarVantagem;
window.avaliarParDados = avaliarParDados;
window.renderVantagem = renderVantagem;
window.corrigirPosicionamentoBadges = corrigirPosicionamentoBadges;
