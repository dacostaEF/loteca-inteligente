// BOOTSTRAP DE INICIALIZAÇÃO - DOSE 1
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Chamadas oficiais (APIs novas)
    await window.LotecaConfrontos?.carregarConfrontos();
    await window.LotecaFunctions?.preencherTodosOsJogos?.(); // rotina que distribui nos 14 containers
    
    // Chamadas específicas para jogos 1 e 2 (loteca-inline-03.js)
    if (typeof window.carregarDados === 'function') {
      await window.carregarDados(1);
      await window.carregarDados(2);
    }
    
    console.log('[OK] Boot loteca concluído');
  } catch(e) {
    console.error('[ERRO] Boot loteca', e);
  }
});