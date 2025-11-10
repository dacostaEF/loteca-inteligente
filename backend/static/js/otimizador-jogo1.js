// backend/static/js/otimizador-jogo1.js
// Motor de decisão específico (pode ser generalizado). Começamos pelo Jogo 1.

(function(){
  const CHOICES = ['1','X','2'];

  function normalizeTriplet(p1, px, p2) {
    // veio em %?
    if ((p1 + px + p2) > 1.5) { p1/=100; px/=100; p2/=100; }
    const s = p1 + px + p2;
    if (s > 0 && (s < 0.98 || s > 1.02)) { p1/=s; px/=s; p2/=s; }
    return { p1, px, p2 };
  }

  function analisarJogo({ p1, px, p2, fatorCasa = 0.5, fatorVisitante = 0.5, tendenciaEmpates = 0.33 }) {
    // 1) normalização defensiva
    ({ p1, px, p2 } = normalizeTriplet(p1, px, p2));

    // 2) ordenar
    const arr = [{k:'1',v:p1},{k:'X',v:px},{k:'2',v:p2}].sort((a,b)=>b.v-a.v);
    const maxP = arr[0].v, secondP = arr[1].v, gap = maxP - secondP;

    // 3) entropia normalizada (0..1)
    const H = -([p1,px,p2].map(p=> p>0 ? p*Math.log(p) : 0).reduce((a,b)=>a+b,0));
    const Hnorm = H / Math.log(3);

    // 4) classe
    let classe;
    if (maxP >= 0.60 || gap >= 0.20)      classe = 'SECO';
    else if (maxP >= 0.45 || gap >= 0.10) classe = 'DUPLO';
    else                                   classe = 'TRIPLO';

    // 5) sugestão
    let sugestao;
    if (classe === 'SECO') {
      sugestao = arr[0].k;
    } else if (classe === 'DUPLO') {
      const top2 = [arr[0].k, arr[1].k].sort((a,b)=>CHOICES.indexOf(a)-CHOICES.indexOf(b)).join('');
      if ((px === p2) && arr[0].k === '1') {
        if (fatorCasa >= 0.55)             sugestao = '1X';
        else if (fatorVisitante >= 0.55)   sugestao = '12';
        else if (tendenciaEmpates > 0.40)  sugestao = '1X';
        else                               sugestao = '1X';
      } else {
        sugestao = top2;
      }
    } else {
      sugestao = '1X2';
    }

    // 6) cobertura e risco
    const pick = (c) => (c==='1'?p1 : c==='X'?px : p2);
    // ✅ Cálculo correto para duplos (incluindo "12")
    let cobertura;
    if (sugestao === '1X2') cobertura = p1 + px + p2;
    else if (sugestao === '12') cobertura = p1 + p2;
    else if (sugestao === '1X') cobertura = p1 + px;
    else if (sugestao === 'X2') cobertura = px + p2;
    else cobertura = pick(sugestao);  // SECO: apenas uma escolha
    const risco = 1 - cobertura;

    // Para-choque: evitar SECO fraco
    if (classe === 'SECO' && cobertura < 0.55) {
      classe = 'DUPLO';
      const top2 = [arr[0].k, arr[1].k].sort((a,b)=>CHOICES.indexOf(a)-CHOICES.indexOf(b)).join('');
      sugestao = top2;
      // ✅ Recalcular com lógica correta para todos os duplos
      if (sugestao === '1X2') cobertura = p1 + px + p2;
      else if (sugestao === '12') cobertura = p1 + p2;
      else if (sugestao === '1X') cobertura = p1 + px;
      else if (sugestao === 'X2') cobertura = px + p2;
      else cobertura = pick(sugestao);
    }

    // Regra final de desempate: se 1 é o favorito e px == p2, preferir 1X
    if (classe === 'DUPLO' && arr[0].k === '1') {
      const eps = 0.015; // 1.5pp de tolerância
      if (px >= p2 - eps) sugestao = '1X';
      // se px muito menor que p2, mantém top2 calculado antes (pode ser '12')
    }

    // 7) confiança
    let confianca = 'Média';
    if (cobertura >= 0.70) confianca = 'Alta';
    else if (cobertura < 0.50) confianca = 'Baixa';

    return { classe, sugestao, cobertura, risco, confianca, debug:{maxP, secondP, gap, Hnorm, p1, px, p2} };
  }

  async function carregarDadosJogo1() {
    const url = '/api/analise/jogo/1?concurso=concurso_atual';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Falha ao carregar jogo 1');
    const json = await res.json();
    const source = json?.dados || json;

    // Tentar extrair probabilidades e fatores
    const normNum = v => (typeof v === 'string' ? Number(v.replace('%','').replace(',','.')) : Number(v));
    const toUnit = v => (isFinite(v) ? (v>1 ? v/100 : v) : undefined);
    let p1, px, p2;
    function tryAssign(key, val){
      const k = (key||'').toString().toLowerCase();
      const n = toUnit(normNum(val));
      if (n==null || !isFinite(n)) return;
      if (k.includes('coluna1') || k.includes('casa') || k.includes('home') || k.includes('mandante') || k.endsWith('_1') || k.includes('prob_1')) p1 = p1 ?? n;
      else if (k.includes('colunax') || k.includes('empate') || k.includes('draw') || k.endsWith('_x') || k.includes('prob_x')) px = px ?? n;
      else if (k.includes('coluna2') || k.includes('fora') || k.includes('away') || k.includes('visitante') || k.endsWith('_2') || k.includes('prob_2')) p2 = p2 ?? n;
    }
    (function walk(obj){ if(!obj||typeof obj!=='object') return; for(const [k,v] of Object.entries(obj)){ if(v&&typeof v==='object'){ if('valor' in v) tryAssign(k, v.valor); if('prob' in v) tryAssign(k, v.prob); walk(v);} else { if(typeof v==='number'||typeof v==='string') tryAssign(k,v); } } })(source);

    // Fatores (se existirem)
    const fatorCasa = toUnit(normNum(source?.fator_casa ?? source?.fatorCasa ?? 0.5)) ?? 0.5;
    const fatorVisitante = toUnit(normNum(source?.fator_fora ?? source?.fatorVisitante ?? 0.5)) ?? 0.5;
    const tendenciaEmpates = toUnit(normNum(source?.tendencia_empates ?? 0.33)) ?? 0.33;

    return analisarJogo({ p1, px, p2, fatorCasa, fatorVisitante, tendenciaEmpates });
  }

  function aplicarNoOtimizadorJogo1(resultado){
    const row = document.querySelector('tr[data-game="1"]');
    if (!row) return;
    // Atualizar Classificação (badge)
    const badge = row.querySelector('.status-badge');
    if (badge) {
      badge.classList.remove('seco','duplo','triplo');
      const cls = resultado.classe.toLowerCase();
      badge.classList.add(cls);
      badge.textContent = resultado.classe.toUpperCase();
    }
    // Atualizar Sugestão
    const cells = row.querySelectorAll('td');
    if (cells && cells[3]) cells[3].innerHTML = `<strong>${resultado.sugestao}</strong>`;

    // Atualizar Probabilidade usando o módulo principal (mantém o design)
    const p = resultado.debug; // contem p1, px, p2
    if (window.LotecaOtimizador?.setProbabilidade) {
      window.LotecaOtimizador.setProbabilidade(1, p.p1, p.px, p.p2, resultado.sugestao);
    }
  }

  async function init(){
    try {
      const r = await carregarDadosJogo1();
      aplicarNoOtimizadorJogo1(r);
      console.log('[JOGO1] Classificação/Sugestão aplicadas:', r);
    } catch(e){
      console.warn('[JOGO1] Falha ao aplicar análise:', e);
    }
  }

  window.OtimizadorJogo1 = { init, analisarJogo };
})();


