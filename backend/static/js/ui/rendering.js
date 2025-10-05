/**
 * FUNÇÕES DE RENDERIZAÇÃO VISUAL
 * Migradas do loteca.html para melhor organização
 * 
 * ⚠️ ATENÇÃO: Estas funções são puramente visuais e não afetam funcionalidades críticas
 */

// FUNÇÃO AUXILIAR PARA DETERMINAR ZONA
function determinarZona(posicao, zona) {
    if (zona) return zona; // Se já tem zona definida, usar ela
    
    // Determinar zona baseada na posição
    if (posicao <= 4) return 'libertadores';
    if (posicao <= 6) return 'pre-libertadores';
    if (posicao <= 12) return 'sul-americana';
    if (posicao >= 17) return 'rebaixamento';
    return '';
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
        const ultimosJogos = time.ultimos.split('').map(resultado => {
            const classe = resultado === 'V' ? 'vitoria' : resultado === 'E' ? 'empate' : 'derrota';
            return `<div class="resultado ${classe}"></div>`;
        }).join('');

        return `
            <tr class="${time.zona}">
                <td>
                    <span class="team-position">${time.pos}</span>
                    <span class="team-name">${time.time}</span>
                </td>
                <td><strong>${time.p}</strong></td>
                <td>${time.j}</td>
                <td>${time.v}</td>
                <td>${time.e}</td>
                <td>${time.d}</td>
                <td>${time.gp}</td>
                <td>${time.gc}</td>
                <td>${time.sg > 0 ? '+' + time.sg : time.sg}</td>
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
