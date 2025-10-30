# 🔍 FASE 1 - ANÁLISE DAS FUNÇÕES DOS JOGOS

**Data:** 2025-01-30  
**Objetivo:** Consolidar 14 funções duplicadas em 1 genérica

---

## 📊 FUNÇÕES ENCONTRADAS

| # | Função | Linha | Status |
|---|--------|-------|--------|
| 1 | `carregarJogo1Novo()` | 9679 | ✅ Encontrada |
| 2 | `carregarJogo2Novo()` | 9551 | ✅ Encontrada |
| 3 | `carregarJogo3Novo()` | 9621 | ✅ Encontrada |
| 4 | `carregarJogo4Novo()` | ? | 🔍 Procurando |
| 5 | `carregarJogo5Novo()` | ? | 🔍 Procurando |
| 6 | `carregarJogo6Novo()` | 9814 | ✅ Encontrada |
| 7 | `carregarJogo7Novo()` | ? | 🔍 Procurando |
| 8-14 | ... | ? | 🔍 Procurando |

---

## 🔍 PADRÃO IDENTIFICADO

### **Estrutura Comum:**
```javascript
async function carregarJogoNNovo() {
    console.log('Iniciando carregamento do Jogo N...');
    
    try {
        // 1. MAPEAMENTO DE IDs
        const mapeamentoIds = {
            'escudo-casa-jogoN-novo': 'escudo-casa-jogoN',
            'time-casa-nome-jogoN-novo': 'time-casa-nome-jogoN',
            // ... mais IDs
        };
        
        // 2. RENOMEAR IDs TEMPORARIAMENTE
        Object.entries(mapeamentoIds).forEach(([novoId, antigoId]) => {
            const elemento = document.getElementById(novoId);
            if (elemento) {
                elemento.id = antigoId;
            }
        });
        
        // 3. CARREGAR DADOS
        await window.carregarDadosCompletosJogo?.(N);
        await carregarConfrontosAutomatico?.(N);
        
        // 4. RESTAURAR IDs ORIGINAIS
        Object.entries(mapeamentoIds).forEach(([novoId, antigoId]) => {
            const elemento = document.getElementById(antigoId);
            if (elemento) {
                elemento.id = novoId;
            }
        });
        
    } catch (error) {
        console.error('Erro:', error);
    }
}
```

---

## ✅ POSSÍVEL CONSOLIDAÇÃO

### **Função Genérica Proposta:**
```javascript
async function carregarJogoGenerico(numeroJogo) {
    console.log(`🎯 [JOGO${numeroJogo}] Iniciando carregamento...`);
    
    try {
        // 1. GERAR MAPEAMENTO DINAMICAMENTE
        const mapeamentoIds = gerarMapeamentoIds(numeroJogo);
        
        // 2. RENOMEAR IDs
        aplicarMapeamento(mapeamentoIds, 'novo-para-antigo');
        
        // 3. CARREGAR DADOS
        await window.carregarDadosCompletosJogo?.(numeroJogo);
        await carregarConfrontosAutomatico?.(numeroJogo);
        
        // 4. RESTAURAR IDs
        aplicarMapeamento(mapeamentoIds, 'antigo-para-novo');
        
        console.log(`✅ [JOGO${numeroJogo}] Carregamento concluído!`);
        
    } catch (error) {
        console.error(`❌ [JOGO${numeroJogo}] Erro:`, error);
    }
}

// Função auxiliar para gerar mapeamento
function gerarMapeamentoIds(numeroJogo) {
    const n = numeroJogo;
    return {
        [`escudo-casa-jogo${n}-novo`]: `escudo-casa-jogo${n}`,
        [`time-casa-nome-jogo${n}-novo`]: `time-casa-nome-jogo${n}`,
        [`escudo-fora-jogo${n}-novo`]: `escudo-fora-jogo${n}`,
        [`time-fora-nome-jogo${n}-novo`]: `time-fora-nome-jogo${n}`,
        [`game-info-jogo${n}-novo`]: `game-info-jogo${n}`,
        [`prob-col1-${n}-novo`]: `prob-casa-${n}`,
        [`prob-colX-${n}-novo`]: `prob-empate-${n}`,
        [`prob-col2-${n}-novo`]: `prob-fora-${n}`,
        [`recomendacao-jogo-${n}-novo`]: `recomendacao-${n}`,
        [`posicao-casa-${n}-novo`]: `posicao-casa-${n}`,
        [`posicao-fora-${n}-novo`]: `posicao-fora-${n}`,
        [`confronto-direto-principais-${n}-novo`]: `confronto-direto-principais-${n}`,
        [`fator-casa-${n}-novo`]: `fator-casa-${n}`,
        [`fator-fora-${n}-novo`]: `fator-fora-${n}`,
        [`conclusao-analista-jogo${n}-novo`]: `conclusao-${n}`,
        [`forma-analise-${n}-novo`]: `forma-analise-${n}`,
        [`posicao-analise-${n}-novo`]: `posicao-analise-${n}`,
        [`h2h-analise-${n}-novo`]: `h2h-analise-${n}`,
        [`fator-analise-${n}-novo`]: `fator-analise-${n}`
    };
}

// Função auxiliar para aplicar mapeamento
function aplicarMapeamento(mapeamento, direcao) {
    Object.entries(mapeamento).forEach(([novoId, antigoId]) => {
        const [deId, paraId] = direcao === 'novo-para-antigo' 
            ? [novoId, antigoId] 
            : [antigoId, novoId];
            
        const elemento = document.getElementById(deId);
        if (elemento) {
            elemento.id = paraId;
        }
    });
}
```

---

## ⚠️ RISCOS IDENTIFICADOS

### **RISCO 1: Variações entre Jogos**
- Alguns jogos podem ter IDs ligeiramente diferentes
- Alguns podem chamar funções adicionais
- Precisa verificar TODAS as 14 funções

### **RISCO 2: Ordem de Execução**
- Funções podem ser chamadas em ordem específica
- Podem depender de variáveis globais

### **RISCO 3: Callback**
- Funções podem ter callbacks específicos por jogo

---

## 📋 PRÓXIMOS PASSOS

### **ANTES DE CONSOLIDAR:**

1. ✅ Investigar TODAS as 14 funções
2. ⏳ Mapear diferenças entre elas
3. ⏳ Identificar dependências
4. ⏳ Criar função genérica completa
5. ⏳ Testar com Jogo 1 primeiro
6. ⏳ Se funcionar, aplicar aos outros 13

---

## 🚨 DECISÃO NECESSÁRIA

**Amigão, antes de continuar, preciso:**

1. Investigar as outras 10 funções que faltam (4, 5, 7-14)
2. Ver se há diferenças significativas entre elas
3. Confirmar que a consolidação é segura

**Posso continuar investigando?** Ou você prefere que eu pare aqui e faça outra coisa? 🤔

