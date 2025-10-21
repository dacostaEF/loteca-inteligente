/**
 * QUADRO COMPARATIVO - SISTEMA MODULAR
 * Renderiza quadros comparativos para todos os jogos da Loteca
 * Com efeitos de hover e destaque neon lilás
 */

class QuadroComparativo {
    constructor() {
        this.jogos = [];
        this.estilos = this._criarEstilos();
        this._inicializar();
    }

    /**
     * Criar estilos CSS com efeitos neon lilás
     */
    _criarEstilos() {
        return `
        <style>
        :root {
            --bg: #0f0f13; 
            --panel: #1a1b22; 
            --soft: #151827; 
            --border: #26293a; 
            --muted: #9aa1bd; 
            --text: #e7e8f3;
            --accent: #8b5cf6; 
            --ok: #22c55e; 
            --warn: #f59e0b; 
            --blue: #3b82f6; 
            --bar: #0e1222;
            --neon-lilac: #A855F7;
            --neon-glow: 0 0 20px rgba(168, 85, 247, 0.3);
        }
        
        .quadro-comparativo {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            margin: 18px 0;
            box-shadow: 0 8px 28px rgba(0,0,0,.25);
            max-width: 1200px;
            margin: 0 auto;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .quadro-comparativo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(168, 85, 247, 0.05) 0%, 
                transparent 50%, 
                rgba(0, 227, 140, 0.05) 100%);
            border-radius: 16px;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .quadro-comparativo:hover {
            border-color: var(--neon-lilac);
            box-shadow: 0 8px 28px rgba(0,0,0,.25), var(--neon-glow);
            transform: translateY(-2px);
        }
        
        .quadro-comparativo:hover::before {
            opacity: 1;
        }
        
        .quadro-header {
            display: inline-block;
            margin: -6px 0 12px;
            padding: 6px 14px;
            border-radius: 999px;
            background: #241b3a;
            color: #cbb6ff;
            font: 600 12px/1 Inter, system-ui;
            transition: all 0.3s ease;
        }
        
        .quadro-comparativo:hover .quadro-header {
            background: linear-gradient(135deg, #241b3a, #2d1b4e);
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
        }
        
        .quadro-grid {
            display: grid;
            grid-template-columns: 1fr 220px 1fr;
            gap: 16px;
        }
        
        .quadro-time {
            background: var(--soft);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .quadro-time::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(168, 85, 247, 0.03) 0%, 
                transparent 50%, 
                rgba(0, 227, 140, 0.03) 100%);
            border-radius: 12px;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .quadro-time:hover {
            border-color: var(--neon-lilac);
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.15);
            transform: translateY(-1px);
        }
        
        .quadro-time:hover::before {
            opacity: 1;
        }
        
        .time-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }
        
        .time-crest {
            width: 34px;
            height: 28px;
            border-radius: 8px;
            background: #8b5cf6;
            display: grid;
            place-items: center;
            font-weight: 800;
            color: white;
            transition: all 0.3s ease;
        }
        
        .quadro-time:hover .time-crest {
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
        }
        
        .time-crest--green {
            background: #16a34a;
        }
        
        .quadro-time:hover .time-crest--green {
            box-shadow: 0 0 15px rgba(22, 163, 74, 0.4);
        }
        
        .time-name {
            margin: 0;
            font: 700 14px/1.2 Inter, system-ui;
            color: var(--text);
            letter-spacing: .3px;
        }
        
        .time-chip {
            margin-left: auto;
            font: 600 11px/1 Inter;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #0f1220;
            color: #cbd5e1;
            transition: all 0.3s ease;
        }
        
        .quadro-time:hover .time-chip {
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
        }
        
        .time-chip--elite {
            background: rgba(34,197,94,.12);
            color: #bbf7d0;
            border-color: rgba(34,197,94,.3);
        }
        
        .time-chip--grande {
            background: rgba(59,130,246,.12);
            color: #bfdbfe;
            border-color: rgba(59,130,246,.3);
        }
        
        .time-chip--medio {
            background: rgba(234,179,8,.12);
            color: #fde68a;
            border-color: rgba(234,179,8,.3);
        }
        
        .time-chip--regional {
            background: rgba(156,163,175,.12);
            color: #e5e7eb;
            border-color: rgba(156,163,175,.3);
        }

        .time-kpis {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 12px;
        }
        
        .time-kpi {
            background: #0f1220;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 10px;
            transition: all 0.3s ease;
        }
        
        .quadro-time:hover .time-kpi {
            border-color: rgba(168, 85, 247, 0.3);
            box-shadow: 0 2px 10px rgba(168, 85, 247, 0.1);
        }
        
        .kpi-label {
            display: block;
            color: var(--muted);
            font: 600 11px/1 Inter;
            text-transform: uppercase;
            letter-spacing: .3px;
        }
        
        .kpi-val {
            display: block;
            font: 800 18px/1 Inter;
            color: #fff;
            margin: 6px 0;
        }
        
        .kpi-hint {
            color: var(--muted);
            font: 12px/1.2 Inter;
        }
        
        .forca-bar {
            height: 8px;
            background: var(--bar);
            border: 1px solid var(--border);
            border-radius: 999px;
            overflow: hidden;
        }
        
        .forca-fill {
            display: block;
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #22c55e, #8b5cf6);
            transition: width 0.5s ease;
        }

        .time-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }
        
        .time-stat {
            background: #0f1220;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 8px 10px;
            color: #cfd2e6;
            display: flex;
            justify-content: space-between;
            font: 13px/1.2 Inter;
            transition: all 0.3s ease;
        }
        
        .quadro-time:hover .time-stat {
            border-color: rgba(168, 85, 247, 0.2);
            background: rgba(168, 85, 247, 0.02);
        }
        
        .quadro-vs {
            display: grid;
            grid-template-rows: auto auto auto auto;
            gap: 8px;
            align-content: start;
            justify-items: center;
        }
        
        .vs-ball {
            width: 56px;
            height: 56px;
            border-radius: 999px;
            background: #20173a;
            border: 1px solid var(--border);
            display: grid;
            place-items: center;
            color: #d2c5ff;
            font: 800 16px Inter;
            transition: all 0.3s ease;
        }
        
        .quadro-comparativo:hover .vs-ball {
            background: linear-gradient(135deg, #20173a, #2d1b4e);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
            border-color: var(--neon-lilac);
        }
        
        .vs-insight {
            margin-top: 6px;
            background: #101427;
            border: 1px solid var(--border);
            padding: 6px 10px;
            border-radius: 8px;
            color: #cbd5e1;
            font: 600 12px Inter;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .quadro-comparativo:hover .vs-insight {
            border-color: rgba(168, 85, 247, 0.3);
            background: rgba(168, 85, 247, 0.05);
        }
        
        .vs-delta {
            background: #101427;
            border: 1px solid var(--border);
            padding: 8px 10px;
            border-radius: 8px;
            color: #d1d5e3;
            font: 600 12px Inter;
            display: grid;
            gap: 2px;
            min-width: 160px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .quadro-comparativo:hover .vs-delta {
            border-color: rgba(168, 85, 247, 0.3);
            background: rgba(168, 85, 247, 0.05);
        }
        
        .vs-delta b {
            font: 800 16px/1 Inter;
            color: #fff;
        }

        @media (max-width: 900px) {
            .quadro-grid {
                grid-template-columns: 1fr;
                gap: 12px;
            }
            .quadro-vs {
                order: -1;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: unset;
            }
            .vs-ball {
                justify-self: center;
                grid-column: 1 / -1;
            }
            .time-kpis {
                grid-template-columns: 1fr 1fr;
            }
        }
        </style>
        `;
    }

    /**
     * Inicializar o sistema
     */
    _inicializar() {
        // Injetar estilos
        if (!document.getElementById('quadro-comparativo-styles')) {
            const styleElement = document.createElement('div');
            styleElement.id = 'quadro-comparativo-styles';
            styleElement.innerHTML = this.estilos;
            document.head.appendChild(styleElement);
        }
    }

    /**
     * Renderizar quadro comparativo para um jogo específico
     * @param {Object} dadosJogo - Dados do jogo
     * @param {string} containerId - ID do container onde renderizar
     */
    renderizarQuadro(dadosJogo, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} não encontrado`);
            return;
        }

        const html = this._gerarHTML(dadosJogo);
        container.innerHTML = html;
        
        // Aplicar dados
        this._aplicarDados(dadosJogo);
        
        console.log(`✅ Quadro comparativo renderizado para Jogo ${dadosJogo.numero}`);
    }

    /**
     * Gerar HTML do quadro comparativo
     */
    _gerarHTML(dados) {
        return `
        <section class="quadro-comparativo" id="cmp-jogo${dados.numero}">
            <header class="quadro-header">JOGO ${dados.numero}</header>

            <div class="quadro-grid">
                <!-- Lado A -->
                <article class="quadro-time" id="teamA-jogo${dados.numero}">
                    <div class="time-header">
                        <div class="time-crest">${dados.timeA.sigla}</div>
                        <h3 class="time-name">${dados.timeA.nome}</h3>
                        <span class="time-chip time-chip--${dados.timeA.categoria}" data-role="catA">${dados.timeA.badge}</span>
                    </div>

                    <div class="time-kpis">
                        <div class="time-kpi">
                            <span class="kpi-label">Total</span>
                            <strong class="kpi-val" data-role="plantelA">${dados.timeA.plantel}</strong>
                            <span class="kpi-hint">Nacionais/Estrangeiros: <b data-role="estrA">${dados.timeA.nacionais}/${dados.timeA.estrangeiros}</b></span>
                        </div>
                        <div class="time-kpi">
                            <span class="kpi-label">Força do Elenco</span>
                            <strong class="kpi-val" data-role="forcaA">${dados.timeA.forca}</strong>
                            <div class="forca-bar"><i class="forca-fill" style="width:${(dados.timeA.forca/10)*100}%" data-role="forcaBarA"></i></div>
                        </div>
                        <div class="time-kpi">
                            <span class="kpi-label">Valor Plantel</span>
                            <strong class="kpi-val" data-role="valorA">${dados.timeA.valor}</strong>
                        </div>
                    </div>

                    <div class="time-stats">
                        <div class="time-stat"><span>Idade média</span><b data-role="idadeA">${dados.timeA.idade} anos</b></div>
                        <div class="time-stat"><span>Posse de bola</span><b data-role="posseA">${dados.timeA.posse}</b></div>
                        <div class="time-stat"><span>Passes certos/jogo</span><b data-role="passesA">${dados.timeA.passes}</b></div>
                        <div class="time-stat"><span>Finalizações/jogo</span><b data-role="chutesA">${dados.timeA.chutes}</b></div>
                    </div>
                </article>

                <!-- Resumo VS -->
                <aside class="quadro-vs">
                    <div class="vs-ball">VS</div>
                    <div class="vs-insight" data-role="insight">${dados.insight}</div>
                    <div class="vs-delta">
                        <span>Δ Força</span>
                        <b data-role="deltaForca">${dados.deltaForca}</b>
                    </div>
                    <div class="vs-delta">
                        <span>Δ Valor</span>
                        <b data-role="deltaValor">${dados.deltaValor}</b>
                    </div>
                </aside>

                <!-- Lado B -->
                <article class="quadro-time" id="teamB-jogo${dados.numero}">
                    <div class="time-header">
                        <div class="time-crest time-crest--green">${dados.timeB.sigla}</div>
                        <h3 class="time-name">${dados.timeB.nome}</h3>
                        <span class="time-chip time-chip--${dados.timeB.categoria}" data-role="catB">${dados.timeB.badge}</span>
                    </div>

                    <div class="time-kpis">
                        <div class="time-kpi">
                            <span class="kpi-label">Total</span>
                            <strong class="kpi-val" data-role="plantelB">${dados.timeB.plantel}</strong>
                            <span class="kpi-hint">Nacionais/Estrangeiros: <b data-role="estrB">${dados.timeB.nacionais}/${dados.timeB.estrangeiros}</b></span>
                        </div>
                        <div class="time-kpi">
                            <span class="kpi-label">Força do Elenco</span>
                            <strong class="kpi-val" data-role="forcaB">${dados.timeB.forca}</strong>
                            <div class="forca-bar"><i class="forca-fill" style="width:${(dados.timeB.forca/10)*100}%" data-role="forcaBarB"></i></div>
                        </div>
                        <div class="time-kpi">
                            <span class="kpi-label">Valor Plantel</span>
                            <strong class="kpi-val" data-role="valorB">${dados.timeB.valor}</strong>
                        </div>
                    </div>

                    <div class="time-stats">
                        <div class="time-stat"><span>Idade média</span><b data-role="idadeB">${dados.timeB.idade} anos</b></div>
                        <div class="time-stat"><span>Posse de bola</span><b data-role="posseB">${dados.timeB.posse}</b></div>
                        <div class="time-stat"><span>Passes certos/jogo</span><b data-role="passesB">${dados.timeB.passes}</b></div>
                        <div class="time-stat"><span>Finalizações/jogo</span><b data-role="chutesB">${dados.timeB.chutes}</b></div>
                    </div>
                </article>
            </div>
        </section>
        `;
    }

    /**
     * Aplicar dados dinamicamente
     */
    _aplicarDados(dados) {
        // Dados já estão aplicados no HTML estático
        // Esta função pode ser usada para atualizações dinâmicas futuras
    }

    /**
     * Criar dados de exemplo para um jogo
     * @param {number} numeroJogo - Número do jogo
     * @param {Object} timeA - Dados do time A
     * @param {Object} timeB - Dados do time B
     */
    criarDadosJogo(numeroJogo, timeA, timeB) {
        const deltaForca = (timeB.forca - timeA.forca);
        const deltaValor = timeB.valorNumerico - timeA.valorNumerico;
        
        const insight = Math.abs(deltaForca) < 0.5
            ? 'Confronto equilibrado no plantel'
            : (deltaForca > 0 ? `${timeB.nome} leva vantagem em força` : `${timeA.nome} leva vantagem em força`);

        return {
            numero: numeroJogo,
            timeA: {
                ...timeA,
                categoria: this._determinarCategoria(timeA.forca),
                badge: this._gerarBadge(timeA.forca)
            },
            timeB: {
                ...timeB,
                categoria: this._determinarCategoria(timeB.forca),
                badge: this._gerarBadge(timeB.forca)
            },
            insight: insight,
            deltaForca: `${deltaForca > 0 ? '+' : ''}${deltaForca.toFixed(1)} pts`,
            deltaValor: `€ ${deltaValor.toFixed(2)} mi`
        };
    }

    /**
     * Determinar categoria baseada na força
     */
    _determinarCategoria(forca) {
        if (forca >= 7.0) return 'elite';
        if (forca >= 6.0) return 'grande';
        if (forca >= 4.0) return 'medio';
        return 'regional';
    }

    /**
     * Gerar badge baseado na força
     */
    _gerarBadge(forca) {
        if (forca >= 7.0) return 'Elenco Elite';
        if (forca >= 6.0) return 'Elenco Forte';
        if (forca >= 4.0) return 'Elenco Sólido';
        return 'Elenco em Desenvolvimento';
    }

    /**
     * Renderizar todos os jogos da Loteca
     * @param {Array} dadosJogos - Array com dados de todos os jogos
     */
    renderizarTodosJogos(dadosJogos) {
        dadosJogos.forEach(jogo => {
            const containerId = `quadro-jogo-${jogo.numero}`;
            this.renderizarQuadro(jogo, containerId);
        });
    }
}

// Instância global
window.QuadroComparativo = QuadroComparativo;

// Exemplo de uso:
/*
const quadro = new QuadroComparativo();

// Dados do Jogo 1 - Flamengo vs Palmeiras
const dadosJogo1 = quadro.criarDadosJogo(1, 
    {
        nome: 'FLAMENGO/RJ',
        sigla: 'FLA',
        plantel: 31,
        nacionais: 21,
        estrangeiros: 10,
        idade: 28.4,
        forca: 6.0,
        valor: '€ 195.90 mi',
        valorNumerico: 195.90,
        posse: '62.2%',
        passes: 509,
        chutes: 5.7
    },
    {
        nome: 'PALMEIRAS/SP',
        sigla: 'PAL',
        plantel: 29,
        nacionais: 21,
        estrangeiros: 8,
        idade: 26.3,
        forca: 6.7,
        valor: '€ 212.15 mi',
        valorNumerico: 212.15,
        posse: '52.1%',
        passes: 340,
        chutes: 4.7
    }
);

// Renderizar
quadro.renderizarQuadro(dadosJogo1, 'container-jogo-1');
*/


