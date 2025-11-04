/**
 * SISTEMA DE VÍNCULO ESPECÍFICO - CONFRONTOS
 * Vincula apenas os nomes dos confrontos da planilha com os times da Aba 1
 * Mantém o layout da planilha inalterado
 */

class VinculoConfrontos {
  constructor() {
    this.jogosData = {};
    this.init();
  }

  init() {
    console.log('🔄 [VÍNCULO] Inicializando sistema de vínculo de confrontos...');
    this.carregarTodosOsJogos();
  }

  // CARREGAR DADOS DE TODOS OS 14 JOGOS VIA ARQUIVOS JSON
  async carregarTodosOsJogos() {
    console.log('🚀 [VÍNCULO] Carregando dados de todos os 14 jogos via arquivos JSON...');
    
    for (let jogoNum = 1; jogoNum <= 14; jogoNum++) {
      try {
        await this.carregarJogoViaJSON(jogoNum);
      } catch (error) {
        console.warn(`⚠️ [VÍNCULO] Erro ao carregar Jogo ${jogoNum} via JSON:`, error);
        // FALLBACK: Tentar ler diretamente do DOM
        this.carregarJogoViaDOM(jogoNum);
      }
    }
    
    console.log('✅ [VÍNCULO] Dados carregados:', this.jogosData);
    this.atualizarTodasAsColunas();
  }

  // FALLBACK: CARREGAR DADOS DIRETAMENTE DO DOM
  carregarJogoViaDOM(jogoNum) {
    console.log(`🔍 [VÍNCULO] Tentando carregar Jogo ${jogoNum} via DOM...`);
    
    // Tentar diferentes padrões de ID
    const casaElement = document.getElementById(`time-casa-nome-jogo${jogoNum}-novo`) || 
                       document.getElementById(`time-casa-nome-${jogoNum}-novo`) ||
                       document.getElementById(`time-casa-nome-jogo${jogoNum}`) ||
                       document.getElementById(`time-casa-nome-${jogoNum}`);
    
    const foraElement = document.getElementById(`time-fora-nome-jogo${jogoNum}-novo`) || 
                       document.getElementById(`time-fora-nome-${jogoNum}-novo`) ||
                       document.getElementById(`time-fora-nome-jogo${jogoNum}`) ||
                       document.getElementById(`time-fora-nome-${jogoNum}`);
    
    const casa = casaElement?.textContent?.trim() || 'Carregando...';
    const fora = foraElement?.textContent?.trim() || 'Carregando...';
    
    this.jogosData[jogoNum] = { casa, fora };
    console.log(`✅ [VÍNCULO] Jogo ${jogoNum} via DOM: ${casa} vs ${fora}`);
    
    return { casa, fora };
  }

  // CARREGAR DADOS DE UM JOGO ESPECÍFICO VIA ARQUIVO JSON
  async carregarJogoViaJSON(jogoNum) {
    const jsonUrl = `/api/analise/jogo/${jogoNum}?concurso=concurso_1219`;
    console.log(`📡 [VÍNCULO] Carregando Jogo ${jogoNum} via JSON: ${jsonUrl}`);
    
    const response = await fetch(jsonUrl);
    if (!response.ok) {
      throw new Error(`JSON retornou ${response.status}`);
    }
    
    const dados = await response.json();
    console.log(`🔍 [VÍNCULO] Dados JSON recebidos para Jogo ${jogoNum}:`, dados);
    
    // Extrair nomes dos times dos dados JSON (mesma estrutura da Aba 1)
    const casa = dados.dados?.time_casa || dados.time_casa || dados.casa || dados.mandante || 'Carregando...';
    const fora = dados.dados?.time_fora || dados.time_fora || dados.fora || dados.visitante || 'Carregando...';
    
    this.jogosData[jogoNum] = { casa, fora };
    console.log(`✅ [VÍNCULO] Jogo ${jogoNum}: ${casa} vs ${fora}`);
    
    return { casa, fora };
  }

  // ATUALIZAR TODAS AS COLUNAS DE CONFRONTO
  atualizarTodasAsColunas() {
    console.log('🔄 [VÍNCULO] Atualizando todas as colunas de confronto...');
    
    for (let jogoNum = 1; jogoNum <= 14; jogoNum++) {
      this.updateConfrontoColumn(jogoNum);
    }
  }

  // ATUALIZAR APENAS A COLUNA "CONFRONTO" DA PLANILHA
  updateConfrontoColumn(jogoNum) {
    const jogo = this.jogosData[jogoNum];
    if (!jogo) return;

    // PADRONIZAR FORMATAÇÃO PARA MAIÚSCULAS (como Jogos 1-3)
    const casaFormatada = jogo.casa.toUpperCase();
    const foraFormatada = jogo.fora.toUpperCase();
    const confronto = `${casaFormatada} vs ${foraFormatada}`;
    
    // Procurar a linha do jogo na tabela da planilha (múltiplas estratégias)
    let tableRow = document.querySelector(`tr[data-jogo="${jogoNum}"]`);
    
    // Se não encontrar com data-jogo, tentar por posição na tabela
    if (!tableRow) {
      const tbody = document.getElementById('optimization-tbody');
      if (tbody && tbody.children[jogoNum - 1]) {
        tableRow = tbody.children[jogoNum - 1];
      }
    }
    
    // Se ainda não encontrar, tentar por texto do primeiro td
    if (!tableRow) {
      const allRows = document.querySelectorAll('#optimization-tbody tr');
      for (let row of allRows) {
        const firstCell = row.children[0];
        if (firstCell && firstCell.textContent.includes(`Jogo ${jogoNum}`)) {
          tableRow = row;
          break;
        }
      }
    }

    if (!tableRow) {
      console.warn(`❌ [VÍNCULO] Linha do Jogo ${jogoNum} não encontrada na tabela`);
      return;
    }

    // Atualizar APENAS a coluna "Confronto" (2ª coluna)
    const confrontoCell = tableRow.children[1]; // 2ª coluna (índice 1)
    if (confrontoCell) {
      confrontoCell.textContent = confronto;
      console.log(`✅ [VÍNCULO] Jogo ${jogoNum} confronto atualizado: ${confronto}`);
    } else {
      console.warn(`❌ [VÍNCULO] Célula de confronto não encontrada para Jogo ${jogoNum}`);
    }
  }

  // MÉTODO PARA FORÇAR SINCRONIZAÇÃO MANUAL
  forceSync() {
    console.log('🔄 [VÍNCULO] Forçando sincronização manual...');
    this.carregarTodosOsJogos();
  }

  // MÉTODO PARA OBTER DADOS ATUAIS
  getCurrentData() {
    return this.jogosData;
  }

}

// EXPORTAR PARA USO GLOBAL
window.VinculoConfrontos = VinculoConfrontos;

// INICIALIZAÇÃO AUTOMÁTICA QUANDO DOM ESTIVER PRONTO
document.addEventListener('DOMContentLoaded', () => {
  console.log('🔄 [VÍNCULO] DOM carregado, iniciando sistema...');
  
  // Aguardar mais tempo para garantir que todos os dados da Aba 1 estejam carregados
  setTimeout(() => {
    console.log('🚀 [VÍNCULO] Iniciando sistema de vínculo...');
    window.vinculoConfrontos = new VinculoConfrontos();
    console.log('✅ [VÍNCULO] Sistema de vínculo de confrontos ativado!');
  }, 3000); // Aumentado para 3 segundos
});

// FUNÇÃO GLOBAL PARA FORÇAR SINCRONIZAÇÃO MANUAL
window.forcarSincronizacaoConfrontos = function() {
  if (window.vinculoConfrontos) {
    window.vinculoConfrontos.forceSync();
    console.log('🔄 [VÍNCULO] Sincronização manual executada!');
  } else {
    console.warn('❌ [VÍNCULO] Sistema de vínculo não inicializado');
  }
};

// FUNÇÃO PARA TESTAR O SISTEMA MANUALMENTE
window.testarVinculoConfrontos = function() {
  console.log('🧪 [TESTE] Testando sistema de vínculo...');
  
  if (window.vinculoConfrontos) {
    console.log('✅ [TESTE] Sistema inicializado');
    console.log('📊 [TESTE] Dados atuais:', window.vinculoConfrontos.getCurrentData());
    
    // Forçar atualização
    window.vinculoConfrontos.forceSync();
  } else {
    console.error('❌ [TESTE] Sistema não inicializado');
  }
};

// FUNÇÃO PARA INICIALIZAR MANUALMENTE QUANDO A ABA 4 FOR ABERTA
window.inicializarVinculoConfrontos = function() {
  console.log('🎯 [VÍNCULO] Inicialização manual solicitada...');
  
  if (!window.vinculoConfrontos) {
    console.log('🚀 [VÍNCULO] Criando nova instância...');
    window.vinculoConfrontos = new VinculoConfrontos();
  } else {
    console.log('🔄 [VÍNCULO] Forçando sincronização...');
    window.vinculoConfrontos.forceSync();
  }
};


console.log('📁 [VÍNCULO] Arquivo vinculo-confrontos.js carregado com sucesso!');
