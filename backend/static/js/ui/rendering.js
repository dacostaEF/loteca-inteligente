/**
 * FUNÇÕES DE RENDERIZAÇÃO VISUAL
 * Migradas do loteca.html para melhor organização
 * 
 * ⚠️ ATENÇÃO: Estas funções são puramente visuais e não afetam funcionalidades críticas
 */

// FUNÇÃO AUXILIAR PARA DETERMINAR ZONA
function determinarZona(posicao, zona) {
    if (zona) {
        // Converter zona do backend para classe CSS
        if (zona === 'Libertadores') return 'libertadores';
        if (zona === 'Pré-Libertadores') return 'pre-libertadores';
        if (zona === 'Sul-Americana') return 'sul-americana';
        if (zona === 'Zona de Rebaixamento') return 'rebaixamento';
        if (zona === 'Meio de tabela') return 'meio-tabela';
        return zona.toLowerCase().replace(/\s+/g, '-');
    }
    
    // Determinar zona baseada na posição (baseado na tabela do jornal esportivo)
    if (posicao <= 4) return 'libertadores';      // 1º ao 4º (azul)
    if (posicao <= 6) return 'pre-libertadores';   // 5º ao 6º (azul claro)
    if (posicao <= 12) return 'sul-americana';    // 7º ao 12º (verde)
    if (posicao >= 17) return 'rebaixamento';     // 17º ao 20º (vermelho)
    return 'meio-tabela'; // 13º ao 16º (preto)
}

// RENDERIZAR TABELA DE CLASSIFICAÇÃO (versão simples)
function renderTabelaClassificacao(dados) {
    const header = `
        <table class="brasileirao-table">
            <thead>
                <tr>
                    <th>CLASSIFICAÇÃO</th>
                    <th>P</th>
                    <th>J</th>
                    <th>V</th>
                    <th>E</th>
                    <th>D</th>
                    <th>GP</th>
                    <th>GC</th>
                    <th>SG</th>
                    <th>%</th>
                    <th>ÚLTIMOS</th>
                </tr>
            </thead>
            <tbody>
    `;

    const rows = dados.map(time => {
        // Se os dados já vêm com bolas coloridas, usar diretamente
        let ultimosJogos;
        if (time.ultimos && time.ultimos.includes('🟢')) {
            // Dados já convertidos com bolas coloridas
            ultimosJogos = time.ultimos;
        } else {
            // Converter V-D-E para bolas coloridas
            ultimosJogos = (time.ultimos || '-----').replace(/V/g, '🟢').replace(/D/g, '🔴').replace(/E/g, '🟡');
        }

        // Determinar ícone de variação
        let variacaoIcon = '';
        if (time.variacao === 'subiu') {
            variacaoIcon = '↑';
        } else if (time.variacao === 'desceu') {
            variacaoIcon = '↓';
        } else {
            variacaoIcon = '■';
        }

        return `
            <tr class="${determinarZona(time.pos, time.zona)}">
                <td>
                    <span class="team-position">${time.pos}</span>
                    <span class="variacao-icon">${variacaoIcon}</span>
                    <span class="team-name">${time.time}</span>
                </td>
                <td><strong>${time.p}</strong></td>
                <td>${time.j}</td>
                <td>${time.v}</td>
                <td>${time.e}</td>
                <td>${time.d}</td>
                <td>${time.gp}</td>
                <td>${time.gc}</td>
                <td>${time.sg !== undefined && time.sg !== null ? (time.sg > 0 ? '+' + time.sg : time.sg) : '0'}</td>
                <td>${time.aproveitamento}</td>
                <td>
                    <div class="ultimos-jogos">
                        ${ultimosJogos}
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    const footer = `
            </tbody>
        </table>
        <div class="table-footer">
            <div class="zones-info">
                <h4>🏆 Zonas de Classificação</h4>
                <div class="zones-grid">
                    <div class="zone-item libertadores">
                        <div class="zone-bar"></div>
                        <div class="zone-text">
                            <strong>Libertadores (1º-4º)</strong>
                            <span>Classificação direta para a Copa Libertadores</span>
                        </div>
                    </div>
                    <div class="zone-item pre-libertadores">
                        <div class="zone-bar"></div>
                        <div class="zone-text">
                            <strong>Pré-Libertadores (5º-6º)</strong>
                            <span>Pré-classificação para a Copa Libertadores</span>
                        </div>
                    </div>
                    <div class="zone-item sul-americana">
                        <div class="zone-bar"></div>
                        <div class="zone-text">
                            <strong>Sul-Americana (7º-12º)</strong>
                            <span>Classificação para a Copa Sul-Americana</span>
                        </div>
                    </div>
                    <div class="zone-item meio-tabela">
                        <div class="zone-bar"></div>
                        <div class="zone-text">
                            <strong>Meio de Tabela (13º-16º)</strong>
                            <span>Sem classificação para competições internacionais</span>
                        </div>
                    </div>
                    <div class="zone-item rebaixamento">
                        <div class="zone-bar"></div>
                        <div class="zone-text">
                            <strong>Zona de Rebaixamento (17º-20º)</strong>
                            <span>Rebaixamento para a Série B</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    return header + rows + footer;
}

// RENDERIZAR LINHA DE CLASSIFICAÇÃO (versão editável)
function renderLinhaClassificacao(time, isEditable = false) {
    const zona = determinarZona(time.posicao, time.zona);
    const ultimos = time.ultimos_jogos || 'VVVVV';
    
    return `
        <tr class="team-row zona-${zona}" data-team-id="${time.id}" data-position="${time.posicao}">
            <td class="position">${time.posicao}</td>
            <td class="team-name">
                <div class="team-info">
                    <span class="team-short">${time.time}</span>
                </div>
            </td>
            <td class="points ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="pontos" data-id="${time.id}"` : ''}>${time.pontos}</td>
            <td class="games ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="jogos" data-id="${time.id}"` : ''}>${time.jogos}</td>
            <td class="wins ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="vitorias" data-id="${time.id}"` : ''}>${time.vitorias}</td>
            <td class="draws ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="empates" data-id="${time.id}"` : ''}>${time.empates}</td>
            <td class="losses ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="derrotas" data-id="${time.id}"` : ''}>${time.derrotas}</td>
            <td class="goals-for ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="gols_pro" data-id="${time.id}"` : ''}>${time.gols_pro}</td>
            <td class="goals-against ${isEditable ? 'editable' : ''}" ${isEditable ? `contenteditable="true" data-field="gols_contra" data-id="${time.id}"` : ''}>${time.gols_contra}</td>
            <td class="goal-diff ${time.saldo_gols >= 0 ? 'positive' : 'negative'}">${time.saldo_gols >= 0 ? '+' : ''}${time.saldo_gols}</td>
            <td class="percentage">${time.aproveitamento}%</td>
            <td class="recent-games">
                <div class="games-indicators">
                    ${ultimos.split('').map(resultado => `<span class="game-result ${resultado.toLowerCase()}">${resultado}</span>`).join('')}
                </div>
            </td>
        </tr>
    `;
}

console.log('✅ [RENDERING] Funções de renderização carregadas com sucesso!');
