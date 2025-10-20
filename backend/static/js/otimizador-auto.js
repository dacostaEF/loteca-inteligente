// backend/static/js/otimizador-auto.js
// Aplica o motor de decisão para todos os 14 jogos, atualizando Classificação, Sugestão e Probabilidades

(function(){
  const CHOICES = ['1','X','2'];

  function normalizeTriplet(p1, px, p2) {
    if ((p1 + px + p2) > 1.5) { p1/=100; px/=100; p2/=100; }
    const s = p1 + px + p2;
    if (s > 0 && (s < 0.98 || s > 1.02)) { p1/=s; px/=s; p2/=s; }
    return { p1, px, p2 };
  }

  function analisarJogoGeneric({ p1, px, p2, fatorCasa = 0.5, fatorVisitante = 0.5, tendenciaEmpates = 0.33 }) {
    ({ p1, px, p2 } = normalizeTriplet(p1, px, p2));
    const arr = [{k:'1',v:p1},{k:'X',v:px},{k:'2',v:p2}].sort((a,b)=>b.v-a.v);
    const maxP = arr[0].v, secondP = arr[1].v, gap = maxP - secondP;
    const H = -([p1,px,p2].map(p=> p>0 ? p*Math.log(p) : 0).reduce((a,b)=>a+b,0));
    const Hnorm = H / Math.log(3);

    let classe;
    if (maxP >= 0.60 || gap >= 0.20)      classe = 'SECO';
    else if (maxP >= 0.45 || gap >= 0.10) classe = 'DUPLO';
    else                                   classe = 'TRIPLO';

    let sugestao;
    if (classe === 'SECO') {
      sugestao = arr[0].k;
    } else if (classe === 'DUPLO') {
      let top2 = [arr[0].k, arr[1].k].sort((a,b)=>CHOICES.indexOf(a)-CHOICES.indexOf(b)).join('');
      // empate px~p2 com 1 favorito → 1X
      const eps = 0.015;
      if (arr[0].k === '1' && (px >= p2 - eps)) top2 = '1X';
      sugestao = top2;
    } else {
      sugestao = '1X2';
    }

    const pick = (c) => (c==='1'?p1 : c==='X'?px : p2);
    let cobertura = sugestao === '1X2' ? (p1+px+p2) : sugestao.split('').reduce((acc,c)=>acc+pick(c),0);
    let risco = 1 - cobertura;

    if (classe === 'SECO' && cobertura < 0.55) {
      classe = 'DUPLO';
      let top2 = [arr[0].k, arr[1].k].sort((a,b)=>CHOICES.indexOf(a)-CHOICES.indexOf(b)).join('');
      if (arr[0].k === '1' && px >= p2 - 0.015) top2 = '1X';
      sugestao = top2;
      cobertura = sugestao === '1X2' ? (p1+px+p2) : sugestao.split('').reduce((acc,c)=>acc+pick(c),0);
      risco = 1 - cobertura;
    }

    let confianca = 'Média';
    if (cobertura >= 0.70) confianca = 'Alta';
    else if (cobertura < 0.50) confianca = 'Baixa';

    return { classe, sugestao, cobertura, risco, confianca, debug:{maxP, secondP, gap, Hnorm, p1, px, p2} };
  }

  function applyToRow(gameId, result){
    const row = document.querySelector(`tr[data-game="${gameId}"]`);
    if (!row) return;
    const badge = row.querySelector('.status-badge');
    if (badge) {
      badge.classList.remove('seco','duplo','triplo');
      badge.classList.add(result.classe.toLowerCase());
      badge.textContent = result.classe.toUpperCase();
    }
    const cells = row.querySelectorAll('td');
    if (cells && cells[3]) cells[3].innerHTML = `<strong>${result.sugestao}</strong>`;
    if (window.LotecaOtimizador?.setProbabilidade) {
      const p = result.debug;
      window.LotecaOtimizador.setProbabilidade(gameId, p.p1, p.px, p.p2, result.sugestao);
    }
  }

  async function fetchProb(gameId) {
    try {
      const res = await fetch(`/api/analise/jogo/${gameId}?concurso=concurso_1216`);
      if (!res.ok) return null;
      const data = await res.json();
      const src = data?.dados || data;
      const normNum = v => (typeof v === 'string' ? Number(v.replace('%','').replace(',','.')) : Number(v));
      const toUnit = v => (isFinite(v) ? (v>1 ? v/100 : v) : undefined);
      let p1, px, p2, fatorCasa, fatorVisitante, tendenciaEmpates;
      function tryAssign(key, val){
        const k = (key||'').toLowerCase();
        const n = toUnit(normNum(val));
        if (n==null || !isFinite(n)) return;
        if (k.includes('coluna1')||k.includes('casa')||k.includes('home')||k.includes('mandante')||k.endsWith('_1')||k.includes('prob_1')) p1 = p1 ?? n;
        else if (k.includes('colunax')||k.includes('empate')||k.includes('draw')||k.endsWith('_x')||k.includes('prob_x')) px = px ?? n;
        else if (k.includes('coluna2')||k.includes('fora')||k.includes('away')||k.includes('visitante')||k.endsWith('_2')||k.includes('prob_2')) p2 = p2 ?? n;
      }
      (function walk(o){ if(!o||typeof o!=='object') return; for(const [k,v] of Object.entries(o)){ if(v&&typeof v==='object'){ if('valor' in v) tryAssign(k,v.valor); if('prob' in v) tryAssign(k,v.prob); walk(v);} else { if(typeof v==='number'||typeof v==='string') tryAssign(k,v);} } })(src);
      fatorCasa = toUnit(normNum(src?.fator_casa ?? src?.fatorCasa ?? 0.5)) ?? 0.5;
      fatorVisitante = toUnit(normNum(src?.fator_fora ?? src?.fatorVisitante ?? 0.5)) ?? 0.5;
      tendenciaEmpates = toUnit(normNum(src?.tendencia_empates ?? 0.33)) ?? 0.33;
      return { p1, px, p2, fatorCasa, fatorVisitante, tendenciaEmpates };
    } catch { return null; }
  }

  async function runAll(){
    for (let id=1; id<=14; id++) {
      const probs = await fetchProb(id);
      if (!probs) continue;
      const result = (window.OtimizadorJogo1?.analisarJogo || analisarJogoGeneric)(probs);
      applyToRow(id, result);
    }
  }

  window.OtimizadorAuto = { runAll };
})();


