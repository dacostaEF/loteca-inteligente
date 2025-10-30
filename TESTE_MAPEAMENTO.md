# 🧪 TESTE DE MAPEAMENTO - DIAGNÓSTICO

## 📋 INSTRUÇÕES PARA TESTE

### 1️⃣ **Abrir o navegador**
- Acesse: http://localhost:5000
- Vá para a aba: **"Força dos Elencos"**
- Abra o Console (F12)

### 2️⃣ **Colar este código no console:**

```javascript
// TESTE DETALHADO DE MAPEAMENTO
async function testarMapeamentoCompleto() {
    console.log('🧪 ===== TESTE DE MAPEAMENTO COMPLETO =====');
    console.log('');
    
    // 1. Verificar se o JSON foi carregado
    console.log('📊 1. Verificando dados do JSON...');
    if (!forcaElencoData) {
        console.error('❌ forcaElencoData NÃO está carregado!');
        return;
    }
    console.log('✅ forcaElencoData carregado!');
    console.log('📋 Clubes disponíveis:', Object.keys(forcaElencoData.clubes));
    console.log('');
    
    // 2. Extrair jogos da API
    console.log('📊 2. Extraindo jogos da API...');
    const jogos = await extrairJogosDaAba1();
    console.log('✅ Jogos extraídos:', jogos.length);
    console.log('');
    
    // 3. Testar cada jogo problemático
    const jogosTeste = [
        { num: 4, casa: jogos[3]?.timeCasa, fora: jogos[3]?.timeVisitante },
        { num: 6, casa: jogos[5]?.timeCasa, fora: jogos[5]?.timeVisitante },
        { num: 12, casa: jogos[11]?.timeCasa, fora: jogos[11]?.timeVisitante },
        { num: 13, casa: jogos[12]?.timeCasa, fora: jogos[12]?.timeVisitante },
        { num: 14, casa: jogos[13]?.timeCasa, fora: jogos[13]?.timeVisitante }
    ];
    
    console.log('📊 3. Testando jogos problemáticos...');
    console.log('');
    
    jogosTeste.forEach(jogo => {
        console.log(`🎯 JOGO ${jogo.num}: ${jogo.casa} vs ${jogo.fora}`);
        console.log(`   Nome Casa Original: "${jogo.casa}"`);
        console.log(`   Nome Fora Original: "${jogo.fora}"`);
        
        // Testar conversão lowercase
        const casaLower = jogo.casa?.toLowerCase().trim();
        const foraLower = jogo.fora?.toLowerCase().trim();
        console.log(`   Casa (lowercase): "${casaLower}"`);
        console.log(`   Fora (lowercase): "${foraLower}"`);
        
        // Testar verificação
        const resultado = verificarForcaElenco(jogo.casa, jogo.fora);
        console.log(`   Resultado Casa: ${resultado.casa ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
        console.log(`   Resultado Fora: ${resultado.fora ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
        
        if (resultado.casa) {
            console.log(`   ✅ Dados Casa:`, resultado.casa.nome_oficial, `- €${resultado.casa.valor_elenco_euros}M`);
        }
        if (resultado.fora) {
            console.log(`   ✅ Dados Fora:`, resultado.fora.nome_oficial, `- €${resultado.fora.valor_elenco_euros}M`);
        }
        console.log('');
    });
    
    console.log('🧪 ===== FIM DO TESTE =====');
}

// Executar teste
testarMapeamentoCompleto();
```

### 3️⃣ **Copiar e colar aqui os resultados**

Especialmente estas linhas:
- `Nome Casa Original:` 
- `Nome Fora Original:`
- `Casa (lowercase):`
- `Fora (lowercase):`
- `Resultado Casa:` ✅ ou ❌
- `Resultado Fora:` ✅ ou ❌

---

## 🔍 CHECKLIST RÁPIDO

### Jogo 4: Goiás vs Athletico-PR
- [ ] Nome vindo da API: ______________
- [ ] Convertido para: ______________
- [ ] Encontrado no JSON? Sim / Não

### Jogo 6: Avaí vs Athletic-MG
- [ ] Nome vindo da API: ______________
- [ ] Convertido para: ______________
- [ ] Encontrado no JSON? Sim / Não

### Jogo 12: Remo vs Chapecoense
- [ ] Nome vindo da API: ______________
- [ ] Convertido para: ______________
- [ ] Encontrado no JSON? Sim / Não

### Jogo 13: Vasco vs São Paulo
- [ ] Nome vindo da API: ______________
- [ ] Convertido para: ______________
- [ ] Encontrado no JSON? Sim / Não

### Jogo 14: Operário-PR vs Vila Nova
- [ ] Nome vindo da API: ______________
- [ ] Convertido para: ______________
- [ ] Encontrado no JSON? Sim / Não

---

## 📝 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### Problema 1: Nome vem com "/Estado"
**Exemplo:** `"Goiás/GO"` em vez de `"GOIAS"`
**Solução:** Já tratado em `mapearNomeParaAPI()`

### Problema 2: Nome vem em formato diferente
**Exemplo:** `"Vasco da Gama"` em vez de `"Vasco"`
**Solução:** Adicionar variação no mapeamento

### Problema 3: Caracteres especiais
**Exemplo:** `"Operário-PR"` com acento
**Solução:** Já mapeado com/sem acento

### Problema 4: Espaços extras
**Exemplo:** `" Avaí "` com espaços
**Solução:** Já tratado com `.trim()`

---

## 🎯 AÇÃO ESPERADA

Após rodar o teste, vou:
1. ✅ Ver os nomes **exatos** que vêm da API
2. ✅ Identificar quais mapeamentos faltam
3. ✅ Adicionar os mapeamentos corretos
4. ✅ Testar novamente

**Cole os resultados aqui no chat para eu corrigir!** 🔧

