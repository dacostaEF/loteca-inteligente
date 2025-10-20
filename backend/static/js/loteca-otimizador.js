// backend/static/js/loteca-otimizador.js
// Controla cliques e totais da Aba 5 sem depender de inline scripts

window.LotecaOtimizador = (function () {
  const VALOR_UNIDADE = 4.00; // valor mínimo oficial

  // Lookup oficial (Duplos, Triplos) -> {apostas, valor}
  const LOOKUP_VALIDO = new Map([
    [[0,0].toString(), {apostas:1,   valor:4}],
    [[1,0].toString(), {apostas:2,   valor:4}],
    [[2,0].toString(), {apostas:4,   valor:8}],
    [[3,0].toString(), {apostas:8,   valor:16}],
    [[4,0].toString(), {apostas:16,  valor:32}],
    [[5,0].toString(), {apostas:32,  valor:64}],
    [[6,0].toString(), {apostas:64,  valor:128}],
    [[7,0].toString(), {apostas:128, valor:256}],
    [[8,0].toString(), {apostas:256, valor:512}],
    [[9,0].toString(), {apostas:512, valor:1024}],
    [[0,1].toString(), {apostas:3,   valor:6}],
    [[1,1].toString(), {apostas:6,   valor:12}],
    [[2,1].toString(), {apostas:12,  valor:24}],
    [[3,1].toString(), {apostas:24,  valor:48}],
    [[4,1].toString(), {apostas:48,  valor:96}],
    [[5,1].toString(), {apostas:96,  valor:192}],
    [[6,1].toString(), {apostas:192, valor:384}],
    [[7,1].toString(), {apostas:384, valor:768}],
    [[8,1].toString(), {apostas:768, valor:1536}],
    [[0,2].toString(), {apostas:9,   valor:18}],
    [[1,2].toString(), {apostas:18,  valor:36}],
    [[2,2].toString(), {apostas:36,  valor:72}],
    [[3,2].toString(), {apostas:72,  valor:144}],
    [[4,2].toString(), {apostas:144, valor:288}],
    [[5,2].toString(), {apostas:288, valor:576}],
    [[6,2].toString(), {apostas:576, valor:1152}],
    [[0,3].toString(), {apostas:27,  valor:54}],
    [[1,3].toString(), {apostas:54,  valor:108}],
    [[2,3].toString(), {apostas:108, valor:216}],
    [[3,3].toString(), {apostas:216, valor:432}],
    [[4,3].toString(), {apostas:432, valor:864}],
    [[5,3].toString(), {apostas:864, valor:1728}],
    [[0,4].toString(), {apostas:81,  valor:162}],
    [[1,4].toString(), {apostas:162, valor:324}],
    [[2,4].toString(), {apostas:324, valor:648}],
    [[3,4].toString(), {apostas:648, valor:1296}],
    [[0,5].toString(), {apostas:243, valor:486}],
    [[1,5].toString(), {apostas:486, valor:972}],
    [[0,6].toString(), {apostas:729, valor:1458}],
  ]);

  const SELECOES = Array.from({ length: 14 }, () => null);

  const mapChoiceToArray = (choice) => {
    if (choice === '1X2') return ['1','X','2'];
    if (choice === '1X') return ['1','X'];
    if (choice === 'X2') return ['X','2'];
    return [choice];
  };

  function classePorChoice(choice){
    const len = mapChoiceToArray(choice).length;
    if (len === 3) return 'triple';
    if (len === 2) return 'double';
    return 'single';
  }

  function contarDuplosTriplos() {
    let D=0,T=0;
    for (const it of SELECOES) {
      if (!it) continue;
      if (it.kind === 'double') D++;
      else if (it.kind === 'triple') T++;
    }
    return {D,T};
  }

  function validarCombo(D,T){
    return LOOKUP_VALIDO.has([D,T].toString());
  }

  function calcularApostasEValor(D,T){
    return LOOKUP_VALIDO.get([D,T].toString()) || {apostas:1, valor:VALOR_UNIDADE};
  }

  function atualizarPainel(sel){
    const {D,T} = contarDuplosTriplos();
    const {apostas, valor} = calcularApostasEValor(D,T);
    const set = (q,v)=>{ const el=document.querySelector(q); if(el) el.textContent = typeof v==='number'?String(v):v; };
    set(sel.duplos, D);
    set(sel.triplos, T);
    set(sel.apostas, apostas);
    set(sel.valor, `R$ ${valor.toFixed(2).replace('.',',')}`);
  }

  function setActiveButtons($linha, choice){
    $linha.querySelectorAll('[data-choice]').forEach(btn=>{
      const on = btn.dataset.choice === choice;
      btn.classList.toggle('active', on);
      btn.classList.toggle('is-active', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      // Aplicar estilo inline para vencer qualquer regra mais forte
      if (on) {
        btn.style.background = 'linear-gradient(135deg, #A855F7 0%, #7C3AED 100%)';
        btn.style.borderColor = '#A855F7';
        btn.style.color = '#ffffff';
        btn.style.boxShadow = '0 2px 8px rgba(168,85,247,.3)';
        btn.style.transform = 'scale(1.03)';
      } else {
        // estado desligado volta para o padrão escuro
        btn.style.background = '#2d2d2d';
        btn.style.borderColor = '#444';
        btn.style.color = '#ffffff';
        btn.style.boxShadow = '';
        btn.style.transform = '';
      }
    });
  }

  function tryUpdateSelecao(idx, choice, painelSelectors){
    const prev = SELECOES[idx];
    SELECOES[idx] = { kind: classePorChoice(choice), value: choice };
    const {D,T} = contarDuplosTriplos();
    if (!validarCombo(D,T)) { SELECOES[idx] = prev; return {ok:false}; }
    atualizarPainel(painelSelectors); return {ok:true};
  }

  function bindClicks(rootSelector, painelSelectors){
    const $root = document.querySelector(rootSelector);
    if (!$root) { console.warn('[LotecaOtimizador] root não encontrado:', rootSelector); }

    // Captura global (funciona mesmo se o botão não estiver diretamente dentro do root)
    document.addEventListener('click', (ev)=>{
      const btn = ev.target.closest('[data-choice]');
      if (!btn) return;
      const $linha = btn.closest('[data-jogo], tr[data-game]');
      if (!$linha) return;
      const idx = Number($linha.getAttribute('data-jogo') || $linha.getAttribute('data-game')) - 1;
      if (!(idx >= 0 && idx < 14)) return;
      const choice = btn.dataset.choice;
      const {ok} = tryUpdateSelecao(idx, choice, painelSelectors);
      if (ok) setActiveButtons($linha, choice);
    }, { capture: true });
    atualizarPainel(painelSelectors);
  }

  function init({ root='#optimization-tbody', painelSelectors={ duplos:'#user-duplos', triplos:'#user-triplos', apostas:'#user-apostas', valor:'#user-valor' } }={}){
    // Garantir estilo visual do ativo
    try {
      const styleId = 'loteca-optimizer-styles';
      if (!document.getElementById(styleId)) {
        const st = document.createElement('style');
        st.id = styleId;
        st.textContent = `
          .choice-btn.active, .choice-btn.is-active { 
            background: linear-gradient(135deg, #A855F7 0%, #7C3AED 100%) !important;
            border-color: #A855F7 !important;
            color: #fff !important;
            box-shadow: 0 2px 8px rgba(168,85,247,.3) !important;
            transform: scale(1.03) !important;
          }
        `;
        document.head.appendChild(st);
      }
    } catch {}
    bindClicks(root, painelSelectors);
  }

  return { init, _state: SELECOES };
})();


