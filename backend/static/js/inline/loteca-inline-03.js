// CARREGAMENTO DE DADOS DOS JOGOS - API INTEGRATION
(async function(){
  async function carregarDados(jogo){
    const url = `/api/analise/jogo/${jogo}?concurso=concurso_1216`; // ajuste o 1216 se necessário
    const resp = await fetch(url);
    if (!resp.ok) { console.error('HTTP', resp.status, url); return; }
    const api = await resp.json();
    const raw = (api && api.dados && api.dados.dados) || api || {};
    const src = raw.dados_publicos || raw.dados || raw;
    if (!src.probabilidades) {
      const col1 = src.probabilidade_casa ?? null;
      const colX = src.probabilidade_empate ?? null;
      const col2 = src.probabilidade_fora ?? null;
      if (col1 != null || colX != null || col2 != null) src.probabilidades = { col1, colX, col2 };
    }
    if (jogo === 1) preencherJogo1Com(src);
    if (jogo === 2) preencherJogo2Com(src);
  }

  function putPct(id, v){
    const el = document.getElementById(id);
    if (!el || !el.classList) return;
    el.classList.remove('loading');
    if (v == null || v === '') return;
    el.innerHTML = `<span class="probability-value">${String(v).replace('%','')}%</span>`;
  }
  // Funções setText e setHTML movidas para loteca-functions.js (implementação oficial)
  // IMPLEMENTAÇÃO TEMPORÁRIA PARA COMPATIBILIDADE
  function setText(id, text = '') {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }
  
  function setHTML(id, html = '') {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
  }

  // ==== JOGO 1 ====
  function preencherJogo1Com(src){
    setText('time-casa-nome', (src.time_casa||'').toUpperCase());
    setText('time-fora-nome', (src.time_fora||'').toUpperCase());
    // JOGO 1 REMOVIDO - PULAR ATUALIZAÇÃO
    // setText('time-casa-nome-jogo1', (src.time_casa||'').toUpperCase());
    // setText('time-fora-nome-jogo1', (src.time_fora||'').toUpperCase());
    const escCasa = null; // document.getElementById('escudo-casa-jogo1');
    const escFora = null; // document.getElementById('escudo-fora-jogo1');
    if (escCasa && src.escudo_casa) escCasa.src = src.escudo_casa;
    if (escFora && src.escudo_fora) escFora.src = src.escudo_fora;

    const info1 = document.querySelector('#analise-rapida .game-card:nth-of-type(1) .game-info');
    if (info1) info1.textContent = `${src.arena||''} | ${src.campeonato||''} | ${src.dia||''}`;

    const p = src.probabilidades || {};
    putPct('prob-col1', p.col1 ?? src.probabilidade_casa);
    putPct('prob-colX', p.colX ?? src.probabilidade_empate);
    putPct('prob-col2', p.col2 ?? src.probabilidade_fora);

    if (src.recomendacao) setHTML('recomendacao-jogo-1', `<strong>${src.recomendacao}</strong>`);
    if (src.conclusao_analista) setText('conclusao-analista-jogo1', src.conclusao_analista||'');

    setText('posicao-casa', src.posicao_casa ? `${src.posicao_casa}°` : '');
    setText('posicao-fora', src.posicao_fora ? `${src.posicao_fora}°` : '');
    setText('fator-casa',  src.fator_casa||'');
    setText('fator-fora',  src.fator_fora||'');

    if (src.confronto_direto) {
      const h2hEl = document.getElementById('confronto-direto-principais');
      if (h2hEl) h2hEl.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem; justify-content: center;">
          <img src="${src.escudo_casa||''}" alt="${src.time_casa||''}" style="width:24px;height:24px;">
          <span>${src.confronto_direto}</span>
          <img src="${src.escudo_fora||''}" alt="${src.time_fora||''}" style="width:24px;height:24px;">
        </div>`;
    }
    const h2hAnal = document.getElementById('h2h-analise-1');
    const posAnal = document.getElementById('posicao-analise-1');
    const fatAnal = document.getElementById('fator-analise-1');
    if (h2hAnal) h2hAnal.innerHTML = src.analise_confronto_direto || '';
    if (posAnal) posAnal.textContent = src.analise_posicao || '';
    if (fatAnal) fatAnal.innerHTML = src.analise_fator_casa || '';
  }

  // ==== JOGO 2 ====
  function preencherJogo2Com(src){
    setText('time-casa-nome-2', (src.time_casa||'').toUpperCase());
    setText('time-fora-nome-2', (src.time_fora||'').toUpperCase());
    const escCasa2 = document.getElementById('escudo-casa-jogo2');
    const escFora2 = document.getElementById('escudo-fora-jogo2');
    if (escCasa2 && src.escudo_casa) escCasa2.src = src.escudo_casa;
    if (escFora2 && src.escudo_fora) escFora2.src = src.escudo_fora;

    const info2 = document.querySelector('#analise-rapida .game-card:nth-of-type(2) .game-info');
    if (info2) info2.textContent = `${src.arena||''} | ${src.campeonato||''} | ${src.dia||''}`;

    const p2 = src.probabilidades || {};
    putPct('prob-col1-2', p2.col1 ?? src.probabilidade_casa);
    putPct('prob-colX-2', p2.colX ?? src.probabilidade_empate);
    putPct('prob-col2-2', p2.col2 ?? src.probabilidade_fora);

    if (src.recomendacao) setHTML('recomendacao-jogo-2', `<strong>${src.recomendacao}</strong>`);
    if (src.conclusao_analista) setText('conclusao-analista-2', src.conclusao_analista||'');

    setText('posicao-casa-2', src.posicao_casa ? `${src.posicao_casa}°` : '');
    setText('posicao-fora-2', src.posicao_fora ? `${src.posicao_fora}°` : '');
    setText('fator-casa-2',  src.fator_casa||'');
    setText('fator-fora-2',  src.fator_fora||'');

    if (src.confronto_direto) {
      const h2hEl2 = document.getElementById('confronto-direto-principais-2');
      if (h2hEl2) h2hEl2.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem; justify-content: center;">
          <img src="${src.escudo_casa||''}" alt="${src.time_casa||''}" style="width:24px;height:24px;">
          <span>${src.confronto_direto}</span>
          <img src="${src.escudo_fora||''}" alt="${src.time_fora||''}" style="width:24px;height:24px;">
        </div>`;
    }
    const h2hAnal = document.getElementById('h2h-analise-2');
    const posAnal = document.getElementById('posicao-analise-2');
    const fatAnal = document.getElementById('fator-analise-2');
    if (h2hAnal) h2hAnal.innerHTML = src.analise_confronto_direto || '';
    if (posAnal) posAnal.textContent = src.analise_posicao || '';
    if (fatAnal) fatAnal.innerHTML = src.analise_fator_casa || '';
  }

  // DOMContentLoaded removido - usando bootstrap do loteca-inline-04.js
  // carregarDados(1) e carregarDados(2) serão chamados pelo bootstrap
  
  // EXPORTAR FUNÇÃO PARA WINDOW
  window.carregarDados = carregarDados;
})();