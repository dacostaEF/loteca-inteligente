# 🗺️ MAPEAMENTO COMPLETO - PÁGINAS DO LOTECA X-RAY

**Concurso Atual:** 1216  
**Arquivo Principal:** `backend/templates/loteca.html` (13.377 linhas)  
**Data:** 29 de Outubro de 2025

---

## 📊 ESTRUTURA GERAL DO SITE

### **Arquivo Principal**
```
backend/templates/loteca.html
├── Header (linha 74-81)
│   └── <h1>Concurso 1216</h1> ← HARDCODED
├── Sistema de Abas (linha 84-102)
└── Scripts JS Externos
    ├── loteca-functions.js
    ├── loteca-confrontos.js
    ├── confrontos-break.js
    └── sticky-tabs-mobile.js
```

---

## 🎯 AS 5 ABAS PRINCIPAIS

### **1. OTIMIZADOR DE APOSTA** 
**ID:** `otimizador-aposta`  
**Linha:** 105-193  
**Status:** ✅ Ativa por padrão

#### **Fonte de Dados:**
```javascript
// LINHA 11507-11530
async function carregarDadosJogos() {
    // PRIORIDADE 1: API
    const response = await fetch('/api/br/loteca/current');
    
    // PRIORIDADE 2: Fallback hardcoded
    gamesData = generateFallbackData();
}
```

#### **API Usada:**
- **Endpoint:** `/api/br/loteca/current`
- **Retorno:** Lista de 14 jogos com probabilidades

#### **Dados Exibidos:**
- ✅ Confrontos (times casa vs fora)
- ✅ Classificação na tabela
- ✅ Sugestão da IA
- ✅ Probabilidades (Col1, X, Col2)
- ✅ Contador de duplos/triplos

---

### **2. ANÁLISE RÁPIDA**
**ID:** `analise-rapida`  
**Linha:** 194-891  
**Status:** ✅ Funcional

#### **Fonte de Dados:**
```javascript
// LINHA 130-163 (loteca-functions.js)
async function carregarDadosCompletosJogo(numeroJogo) {
    // 1. CARREGAR DADOS DO JSON
    const response = await fetch(`/api/analise/jogo/${numeroJogo}?concurso=concurso_1216`);
    
    // 2. ATUALIZAR CAMPOS PRINCIPAIS
    await atualizarCamposPrincipais(numeroJogo, dados);
    
    // 3. CARREGAR E RENDERIZAR CONFRONTOS
    await carregarERenderizarConfrontos(numeroJogo, dados);
}
```

#### **APIs Usadas:**
1. **Análise do Jogo:**
   - **Endpoint:** `/api/analise/jogo/{numeroJogo}?concurso=concurso_1216`
   - **Backend:** `admin_api.py` linha 1681-1715
   - **Arquivo:** `models/concurso_1216/analise_rapida/jogo_X.json`

2. **Confrontos H2H:**
   - **Endpoint:** `/api/br/confrontos/{arquivo}.csv`
   - **Arquivo:** `models/Confrontos/{time1}_{time2}.csv`

#### **Dados Exibidos:**
- ✅ Nomes dos times
- ✅ Escudos
- ✅ Probabilidades (Casa, Empate, Fora)
- ✅ Posição na tabela
- ✅ Confronto direto (ex: 3V-5E-2D)
- ✅ Histórico H2H (últimos 10 jogos)
- ✅ Análise do analista
- ✅ Recomendação

#### **Estrutura JSON Esperada:**
```json
{
  "dados": {
    "time_casa": "Flamengo/RJ",
    "time_fora": "Palmeiras/SP",
    "escudo_casa": "/static/escudos/FLA_Flamengo/Flamengo.png",
    "escudo_fora": "/static/escudos/PAL_Palmeiras/Palmeiras.png",
    "probabilidade_casa": "40",
    "probabilidade_empate": "30",
    "probabilidade_fora": "30",
    "posicao_casa": "2",
    "posicao_fora": "1",
    "confronto_direto": "3V-5E-2D",
    "confrontos_sequence": "V-E-D-V-E",
    "fator_casa": "60%",
    "fator_fora": "40%",
    "recomendacao": "Coluna 1 (Flamengo) - Risco Médio",
    "conclusao_analista": "Análise detalhada..."
  }
}
```

#### **Mapeamento de Jogos (Concurso 1216):**
```javascript
// loteca-functions.js linha 8-23
const jogosMap = {
    1: { csv: 'Flamengo_vs_Palmeiras.csv', casa: 'Flamengo', fora: 'Palmeiras' },
    2: { csv: 'Internacional_vs_Sport.csv', casa: 'Internacional', fora: 'Sport' },
    3: { csv: 'Corinthians_vs_Atletico-MG.csv', casa: 'Corinthians', fora: 'Atletico-MG' },
    4: { csv: 'Roma_vs_Internazionale.csv', casa: 'Roma', fora: 'Internazionale' },
    5: { csv: 'Atletico-Madrid_vs_Osasuna.csv', casa: 'Atletico Madrid', fora: 'Osasuna' },
    6: { csv: 'Cruzeiro_vs_Fortaleza.csv', casa: 'Cruzeiro', fora: 'Fortaleza' },
    7: { csv: 'Tottenham_vs_Aston-Villa.csv', casa: 'Tottenham', fora: 'Aston Villa' },
    8: { csv: 'Mirassol_vs_Sao-Paulo.csv', casa: 'Mirassol', fora: 'Sao_Paulo' },
    9: { csv: 'Ceara_vs_Botafogo-RJ.csv', casa: 'Ceará', fora: 'Botafogo' },
    10: { csv: 'Liverpool_vs_Mancheter-United.csv', casa: 'Liverpool', fora: 'Manchester United' },
    11: { csv: 'Atalanta_vs_Lazio.csv', casa: 'Atalanta', fora: 'Lazio' },
    12: { csv: 'Bahia_vs_Gremio.csv', casa: 'Bahia', fora: 'Gremio' },
    13: { csv: 'Milan_vs_Fiorentina.csv', casa: 'Milan', fora: 'Fiorentina' },
    14: { csv: 'Getafe_vs_Real-Madrid.csv', casa: 'Getafe', fora: 'Real Madrid' }
};
```

---

### **3. FORÇA DOS ELENCOS**
**ID:** `forca-elenco`  
**Linha:** 892-978  
**Status:** ✅ Funcional

#### **Fonte de Dados:**
```javascript
// LINHA 6050-6083
async function loadElencoData(data) {
    // BUSCAR IDs DOS CLUBES
    const homeId = centralAdminProvider.getClubIdByName(data.home.name);
    const awayId = centralAdminProvider.getClubIdByName(data.away.name);
    
    // BUSCAR ESTATÍSTICAS REAIS
    const [homeStats, awayStats] = await Promise.all([
        centralAdminProvider.getEstatisticasClube(homeId),
        centralAdminProvider.getEstatisticasClube(awayId)
    ]);
}
```

#### **APIs Usadas:**
1. **Lista de Clubes:**
   - **Endpoint:** `/api/br/clubes`
   - **Retorno:** Lista com ID e nome de todos os clubes

2. **Estatísticas do Clube:**
   - **Endpoint:** `/api/br/clube/{id}/stats`
   - **Retorno:** Dados do Cartola FC
     - Total de atletas
     - Preço médio
     - Rating do elenco
     - Performance

#### **Dados Exibidos:**
- ✅ Rating do elenco (0-100%)
- ✅ Preço médio dos jogadores (Cartoletas)
- ✅ Total de atletas
- ✅ Badges de qualidade
- ✅ Comparação visual entre elencos

#### **Integração Cartola FC:**
```
API Cartola → services/cartola_provider.py
              ↓
      Backend (admin_api.py)
              ↓
        Frontend (loteca.html)
              ↓
    Renderização dos badges
```

---

### **4. DADOS AVANÇADOS**
**ID:** `dados-avancados`  
**Linha:** 979-1359  
**Status:** ✅ Funcional

#### **Fonte de Dados:**
Usa a **mesma API** da aba "Análise Rápida":
```javascript
// Linha 12303-12334
async function carregarDados(jogo) {
    const url = `/api/analise/jogo/${jogo}?concurso=concurso_1216`;
    const resp = await fetch(url);
    const api = await resp.json();
}
```

#### **Dados Exibidos:**
- ✅ Estatísticas detalhadas por jogo
- ✅ Forma recente dos times
- ✅ Desempenho casa vs fora
- ✅ Gols marcados/sofridos
- ✅ Sequências (vitórias/derrotas)
- ✅ Aproveitamento (%)

---

### **5. PANORAMA DOS CAMPEONATOS**
**ID:** `panorama-campeonatos`  
**Linha:** 1360-1715  
**Status:** ✅ Funcional

#### **Fonte de Dados:**
```javascript
// Carrega dados de classificação dos campeonatos
// Via API de classificação automática
```

#### **APIs Usadas:**
- **Endpoint:** `/api/auto/classificacao/{campeonato}`
- **Campeonatos:** Brasileirão Série A, B, C + Internacionais

#### **Dados Exibidos:**
- ✅ Tabela de classificação
- ✅ Pontos, vitórias, empates, derrotas
- ✅ Saldo de gols
- ✅ Aproveitamento
- ✅ Zonas (Libertadores, Rebaixamento, etc.)

---

## 🔄 FLUXO COMPLETO DE CARREGAMENTO

### **Inicialização (DOMContentLoaded)**
```javascript
// LINHA 11105-11130
document.addEventListener('DOMContentLoaded', function() {
    // 1. CARREGAR DADOS DOS JOGOS
    carregarDadosJogos();
    
    // 2. INICIALIZAR ABAS
    initializeTabs();
    
    // 3. CARREGAR DADOS REAIS
    loadRealLotecaData();
    
    // 4. CARREGAMENTO AUTOMÁTICO DOS JOGOS
    setTimeout(async () => {
        for (let i = 1; i <= 14; i++) {
            await carregarDadosCompletosJogo(i);
        }
    }, 500);
});
```

---

## 📂 ESTRUTURA DE ARQUIVOS DO CONCURSO 1216

### **No Servidor (Backend)**
```
backend/models/concurso_1216/
├── concurso_1216.json              ← Metadados do concurso
├── concurso_loteca_1216.csv        ← Lista dos 14 jogos
└── analise_rapida/                 ← Análises individuais
    ├── jogo_1.json
    ├── jogo_2.json
    ├── jogo_3.json
    ├── jogo_4.json
    ├── jogo_5.json
    ├── jogo_6.json
    ├── jogo_7.json
    ├── jogo_8.json
    ├── jogo_9.json
    ├── jogo_10.json
    ├── jogo_11.json
    ├── jogo_12.json
    ├── jogo_13.json
    └── jogo_14.json
```

### **Confrontos (Permanentes)**
```
backend/models/Confrontos/
├── flamengo_palmeiras.csv
├── internacional_sport.csv
├── corinthians_atletico-mg.csv
├── bahia_gremio.csv
├── ceara_botafogo.csv
├── cruzeiro_fortaleza.csv
├── mirassol_sao-paulo.csv
└── ... (mais 55 confrontos)
```

### **Estatísticas dos Clubes**
```
backend/models/Jogos/
├── flamengo/
│   └── jogos.csv               ← Histórico de jogos
├── palmeiras/
│   └── jogos.csv
├── internacional/
│   └── jogos.csv
└── ... (um para cada clube)
```

---

## 🌐 ENDPOINTS DA API

### **1. Análise do Jogo**
```
GET /api/analise/jogo/{numeroJogo}?concurso=concurso_1216
```
**Backend:** `admin_api.py` linha 1681-1715  
**Retorna:** Dados completos do jogo (JSON)

### **2. Confrontos H2H**
```
GET /api/br/confrontos/{arquivo}.csv
```
**Retorna:** Histórico de confrontos (CSV)

### **3. Loteca Atual**
```
GET /api/br/loteca/current
```
**Retorna:** Lista de 14 jogos do concurso atual

### **4. Lista de Clubes**
```
GET /api/br/clubes
```
**Retorna:** Todos os clubes com IDs do Cartola FC

### **5. Estatísticas do Clube**
```
GET /api/br/clube/{id}/stats
```
**Retorna:** Estatísticas do Cartola FC

### **6. Classificação**
```
GET /api/auto/classificacao/{campeonato}
```
**Retorna:** Tabela de classificação atualizada

---

## ⚙️ SCRIPTS JAVASCRIPT

### **loteca-functions.js** (Principal)
- `carregarDadosCompletosJogo(numeroJogo)` - Carrega tudo do jogo
- `atualizarCamposPrincipais()` - Atualiza campos visuais
- `carregarERenderizarConfrontos()` - Renderiza confrontos
- `jogosMap` - Mapeamento dos 14 jogos
- `escudosMap` - Mapeamento dos escudos

### **loteca-confrontos.js**
- `carregarConfrontosAutomatico(numeroJogo)` - Carrega H2H
- `renderizarConfrontosJogo()` - Renderiza na tela
- Parsing de CSV de confrontos

### **confrontos-break.js**
- Detalhamento adicional de confrontos
- Análises específicas

### **sticky-tabs-mobile.js**
- Comportamento das abas em mobile
- Scroll e navegação

---

## 🎨 CSS

### **loteca.css** (Principal)
```
static/css/loteca.css
├── Layout geral
├── Sistema de abas
├── Cards dos jogos
├── Tabelas
├── Badges
├── Responsividade mobile
└── Animações
```

---

## 🔍 COMO CADA ABA CARREGA OS DADOS

### **Fluxo Detalhado: ABA "ANÁLISE RÁPIDA"**

```
USUÁRIO CLICA NO JOGO 1
        ↓
onChange do select (HTML linha 2295)
        ↓
carregarDadosJogo() (linha 3024)
        ↓
carregarDadosCompletosJogo(1) (loteca-functions.js linha 130)
        ↓
┌───────────────────────────────────────┐
│ 1. BUSCAR JSON DO SERVIDOR            │
│    fetch('/api/analise/jogo/1?...') │
│    ↓                                  │
│    admin_api.py linha 1681            │
│    ↓                                  │
│    Lê: models/concurso_1216/          │
│         analise_rapida/jogo_1.json    │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ 2. ATUALIZAR CAMPOS NA TELA           │
│    atualizarCamposPrincipais()        │
│    ↓                                  │
│    - Nomes dos times                  │
│    - Escudos                          │
│    - Probabilidades                   │
│    - Posições                         │
│    - Análises                         │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ 3. CARREGAR CONFRONTOS H2H            │
│    carregarERenderizarConfrontos()    │
│    ↓                                  │
│    fetch('/api/br/confrontos/         │
│           Flamengo_vs_Palmeiras.csv') │
│    ↓                                  │
│    Lê: models/Confrontos/             │
│         flamengo_palmeiras.csv        │
│    ↓                                  │
│    - Parse do CSV                     │
│    - Últimos 10 jogos                 │
│    - Vencedor de cada jogo            │
│    - Renderização visual              │
└───────────┬───────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ 4. RENDERIZAÇÃO COMPLETA              │
│    ✅ Todos os dados na tela          │
└───────────────────────────────────────┘
```

---

## 📊 DADOS QUE CADA ABA PRECISA

| Aba | JSON Análise | CSV Confrontos | API Cartola | API Classificação |
|-----|--------------|----------------|-------------|-------------------|
| **Otimizador** | ✅ | ❌ | ❌ | ✅ (posições) |
| **Análise Rápida** | ✅ | ✅ | ❌ | ❌ |
| **Força Elencos** | ✅ | ❌ | ✅ | ❌ |
| **Dados Avançados** | ✅ | ✅ | ❌ | ❌ |
| **Panorama** | ❌ | ❌ | ❌ | ✅ |

---

## 🚨 PONTOS CRÍTICOS PARA TROCAR DE CONCURSO

### **O que precisa mudar do 1216 para 1218:**

1. **HTML (loteca.html linha 79)**
```html
<!-- ANTES -->
<h1>Concurso 1216</h1>

<!-- DEPOIS -->
<h1>Concurso 1218</h1>
```

2. **JavaScript (loteca-functions.js linha 136)**
```javascript
// ANTES
const response = await fetch(`/api/analise/jogo/${numeroJogo}?concurso=concurso_1216`);

// DEPOIS
const response = await fetch(`/api/analise/jogo/${numeroJogo}?concurso=concurso_1218`);
```

3. **JavaScript (loteca.html linha 12305)**
```javascript
// ANTES
const url = `/api/analise/jogo/${jogo}?concurso=concurso_1216`;

// DEPOIS
const url = `/api/analise/jogo/${jogo}?concurso=concurso_1218`;
```

4. **Mapeamento dos Jogos (loteca-functions.js linha 8-23)**
```javascript
// ATUALIZAR com os novos jogos do concurso 1218
const jogosMap = {
    1: { csv: 'Corinthians_vs_Gremio.csv', casa: 'Corinthians', fora: 'Gremio' },
    2: { csv: 'Santos_vs_Fortaleza.csv', casa: 'Santos', fora: 'Fortaleza' },
    // ... resto dos jogos
};
```

5. **Criar arquivos no servidor:**
```
backend/models/concurso_1218/
├── concurso_1218.json
├── concurso_loteca_1218.csv
└── analise_rapida/
    ├── jogo_1.json   ← CRIAR
    ├── jogo_2.json   ← CRIAR
    └── ... (até 14)
```

---

## 📝 CHECKLIST PARA MUDAR CONCURSO

- [ ] 1. Criar pasta `concurso_1218/`
- [ ] 2. Criar `concurso_1218.json` com metadados
- [ ] 3. Criar `concurso_loteca_1218.csv` com os 14 jogos
- [ ] 4. Criar pasta `analise_rapida/`
- [ ] 5. Gerar 14 arquivos `jogo_X.json`
- [ ] 6. Verificar confrontos H2H existem
- [ ] 7. Criar confrontos novos se necessário
- [ ] 8. Atualizar número do concurso no HTML (linha 79)
- [ ] 9. Atualizar parâmetro `concurso` nos scripts JS (2 lugares)
- [ ] 10. Atualizar `jogosMap` com novos confrontos
- [ ] 11. Testar cada aba
- [ ] 12. Validar carregamento dos dados

---

## 🎯 CONCLUSÃO

O site está **100% funcional** para o concurso 1216 porque:

✅ **Todos os arquivos JSON existem** (`analise_rapida/jogo_X.json`)  
✅ **Todos os confrontos H2H existem** (`Confrontos/*.csv`)  
✅ **APIs estão configuradas** corretamente  
✅ **Scripts JS estão apontando** para `concurso_1216`  

Para funcionar no concurso 1218, basta **replicar essa estrutura** e **atualizar as referências**!

---

**Documento gerado em:** 29/10/2025  
**Sistema:** Loteca X-Ray v1.0  
**Concurso Atual:** 1216


