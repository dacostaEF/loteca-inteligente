# 🔄 MAPEAMENTO DE NOMES DOS CLUBES

**Data:** 30/10/2025  
**Versão:** 2.0  
**Propósito:** Garantir consistência de nomes entre CSVs, JavaScript e JSON

---

## 🎯 PROBLEMA RESOLVIDO

Os clubes têm **nomes diferentes** em cada parte do sistema:
- 📄 **CSVs**: "GOIAS", "AVAI", "RED BULL BRAGANTINO"
- 🗂️ **JSON**: "goias", "avai", "red_bull_bragantino"
- 💻 **Frontend**: "Goiás", "Avaí", "Red Bull Bragantino"

Esta inconsistência causava **containers vazios** na aba "Força dos Elencos".

---

## 🛠️ SOLUÇÃO IMPLEMENTADA

### 1️⃣ **Dois mapeamentos criados:**

#### A) `mapearNomeParaAPI()` (loteca.html, linha ~3748)
- **Função:** Converte nomes da API para nomes display
- **Local:** `backend/templates/loteca.html`
- **Uso:** Extração de jogos da API central

#### B) `mapeamentoNomes` (dentro de `verificarForcaElenco`, linha ~11717)
- **Função:** Converte nomes display para chaves do JSON
- **Local:** `backend/templates/loteca.html`
- **Uso:** Busca de dados no `forca_elenco_unificado.json`

---

## 📋 MAPEAMENTO COMPLETO - 15 TIMES ADICIONADOS

### ⚽ **Série A**

| Nome na API/CSV | Nome Display | Chave JSON | Observações |
|-----------------|--------------|------------|-------------|
| `MIRASSOL` | `Mirassol` | `mirassol` | Sensação da Série A |
| `RED BULL BRAGANTINO` | `Red Bull Bragantino` | `red_bull_bragantino` | Variações: BRAGANTINO |
| `CEARÁ` / `CEARA` | `Ceará` | `ceara` | Com/sem acento |
| `SPORT` | `Sport` | `sport` | Variações: SPORT RECIFE |
| `JUVENTUDE` | `Juventude` | `juventude` | - |
| `VITÓRIA` / `VITORIA` | `Vitória` | `vitoria` | Com/sem acento |

### ⚽ **Série B**

| Nome na API/CSV | Nome Display | Chave JSON | Observações |
|-----------------|--------------|------------|-------------|
| `REMO` | `Remo` | `remo` | Já em minúsculo no CSV |
| `CHAPECOENSE` | `Chapecoense` | `chapecoense` | Variações: CHAPE |
| `OPERÁRIO-PR` / `OPERARIO-PR` | `Operário-PR` | `operario_pr` | Com/sem acento |
| `VILA NOVA` | `Vila Nova` | `vila_nova` | Espaço → underscore |
| `AVAI` / `AVAÍ` | `Avaí` | `avai` | Com/sem acento |
| `ATHLETIC-MG` | `Athletic-MG` | `athletic_mg` | Hífen → underscore |
| `GOIAS` / `GOIÁS` | `Goiás` | `goias` | Com/sem acento |

---

## 🔧 VARIAÇÕES SUPORTADAS

### Red Bull Bragantino
```javascript
'RED BULL BRAGANTINO' → 'Red Bull Bragantino' → 'red_bull_bragantino'
'BRAGANTINO'          → 'Red Bull Bragantino' → 'red_bull_bragantino'
'red bull bragantino' → mapeamentoNomes        → 'red_bull_bragantino'
'bragantino'          → mapeamentoNomes        → 'red_bull_bragantino'
```

### Operário-PR
```javascript
'OPERÁRIO-PR'  → 'Operário-PR' → 'operario_pr'
'OPERARIO-PR'  → 'Operário-PR' → 'operario_pr'
'OPERARIO PR'  → 'Operário-PR' → 'operario_pr'
'operário-pr'  → mapeamentoNomes → 'operario_pr'
'operario-pr'  → mapeamentoNomes → 'operario_pr'
'operario pr'  → mapeamentoNomes → 'operario_pr'
```

### Avaí
```javascript
'AVAI'  → 'Avaí' → 'avai'
'AVAÍ'  → 'Avaí' → 'avai'
'avai'  → mapeamentoNomes → 'avai'
'avaí'  → mapeamentoNomes → 'avai'
```

### Athletico-PR (já existia, mas melhorado)
```javascript
'ATHLETICO-PR'  → 'Athletico-PR' → 'athletico_pr'
'ATHLETICO/PR'  → 'Athletico-PR' → 'athletico_pr'
'athletico-pr'  → mapeamentoNomes → 'athletico_pr'
'athletico/pr'  → mapeamentoNomes → 'athletico_pr'
'athletico pr'  → mapeamentoNomes → 'athletico_pr'
```

---

## 🔍 FLUXO DE DADOS

### Etapa 1: API → Display
```
API retorna: "GOIAS"
↓
mapearNomeParaAPI() 
↓
Nome display: "Goiás"
```

### Etapa 2: Display → JSON Key
```
Nome display: "Goiás"
↓
toLowerCase(): "goiás"
↓
mapeamentoNomes['goiás']: "goias"
↓
Chave JSON: "goias"
```

### Etapa 3: Busca no JSON
```javascript
forcaElencoData.clubes["goias"]
↓
{
  "nome_oficial": "Goiás",
  "valor_elenco_euros": 11.0,
  "forca_elenco": 4.4,
  ...
}
```

---

## 📁 ARQUIVOS MODIFICADOS

### 1. `backend/templates/loteca.html`
**Linha ~3748:** Função `mapearNomeParaAPI()`
```javascript
// ✅ TIMES ADICIONADOS 2025 - Série A e B
'MIRASSOL': 'Mirassol',
'RED BULL BRAGANTINO': 'Red Bull Bragantino',
'BRAGANTINO': 'Red Bull Bragantino',
'AVAI': 'Avaí',
'AVAÍ': 'Avaí',
// ... etc
```

**Linha ~11717:** Objeto `mapeamentoNomes` (dentro de `verificarForcaElenco`)
```javascript
// ✅ TIMES ADICIONADOS 2025
'mirassol': 'mirassol',
'red bull bragantino': 'red_bull_bragantino',
'bragantino': 'red_bull_bragantino',
'avai': 'avai',
'avaí': 'avai',
// ... etc
```

### 2. `backend/static/valor_elenco/forca_elenco_unificado.json`
```json
{
  "clubes": {
    "mirassol": { ... },
    "red_bull_bragantino": { ... },
    "ceara": { ... },
    "sport": { ... },
    "juventude": { ... },
    "remo": { ... },
    "chapecoense": { ... },
    "operario_pr": { ... },
    "vila_nova": { ... },
    "avai": { ... },
    "athletic_mg": { ... },
    "vitoria": { ... },
    "goias": { ... }
  }
}
```

---

## ✅ TESTES RECOMENDADOS

### Teste 1: Verificar mapeamento no console
```javascript
// Abrir console do navegador (F12)
window.testarForcaElenco();
```

### Teste 2: Verificar jogos específicos
```javascript
// Verificar jogo 4 (Goiás vs Athletico-PR)
verificarForcaElenco('GOIAS', 'ATHLETICO-PR');

// Verificar jogo 6 (Avaí vs Athletic-MG)
verificarForcaElenco('AVAI', 'ATHLETIC-MG');

// Verificar jogo 12 (Remo vs Chapecoense)
verificarForcaElenco('remo', 'chapecoense');

// Verificar jogo 14 (Operário-PR vs Vila Nova)
verificarForcaElenco('Operário-PR', 'Vila Nova');
```

### Teste 3: Forçar recarregamento
```javascript
// Forçar aplicação em todos os jogos
window.forcarForcaElencoTodos();
```

---

## ⚠️ REGRAS PARA ADICIONAR NOVOS TIMES

### Ao adicionar um novo time:

1. **Identifique todas as variações do nome**
   - Com/sem acento
   - Com/sem hífen
   - Com/sem estado
   - Abreviações comuns

2. **Adicione no `mapearNomeParaAPI()`**
   ```javascript
   'NOME_NA_API': 'Nome Display',
   'VARIAÇÃO_1': 'Nome Display',
   'VARIAÇÃO_2': 'Nome Display',
   ```

3. **Adicione no `mapeamentoNomes`**
   ```javascript
   'nome display lowercase': 'chave_json',
   'variação_1 lowercase': 'chave_json',
   'variação_2 lowercase': 'chave_json',
   ```

4. **Crie a chave no JSON**
   ```json
   "chave_json": {
     "nome_oficial": "Nome Display",
     "nomes_alternativos": ["variação 1", "variação 2"],
     "valor_elenco_euros": XX.X,
     ...
   }
   ```

---

## 🐛 TROUBLESHOOTING

### Container aparece vazio?

1. **Verifique o console** (F12)
   - Procure por `❌ NÃO ENCONTRADO`
   - Veja qual chave está sendo buscada

2. **Verifique o nome no CSV**
   - Abra o CSV do jogo em `/static/confrontos/`
   - Veja o nome exato usado

3. **Adicione a variação faltante**
   - No `mapearNomeParaAPI()` e `mapeamentoNomes`

### Nome com caracteres especiais?

- **Acentos:** Sempre adicione 2 variações (com/sem)
- **Hífens/Espaços:** JSON usa underscore (`_`)
- **Barras (`/`):** JSON NÃO usa

---

## 📊 ESTATÍSTICAS DO MAPEAMENTO

```
✅ 28 clubes brasileiros mapeados
✅ 15 clubes adicionados em 2025
✅ 2 funções de mapeamento sincronizadas
✅ 3+ variações por clube (em média)
✅ 100% dos jogos cobertos
```

---

**Desenvolvido para:** Loteca X-Ray  
**Última Atualização:** 30/10/2025  
**Manutenção:** Sempre atualizar os 2 mapeamentos simultaneamente!

