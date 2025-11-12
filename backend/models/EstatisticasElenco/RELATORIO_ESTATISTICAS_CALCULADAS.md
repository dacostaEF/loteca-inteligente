# 📊 RELATÓRIO - ESTATÍSTICAS CALCULADAS DAS SELEÇÕES

**Data:** 2025-01-12  
**Script:** `backend/scripts/calcular_estatisticas_selecoes.py`  
**Fonte:** CSVs de confrontos históricos

---

## ✅ SELEÇÕES COM DADOS CALCULADOS (10/16):

| # | Seleção | Jogos | Média Gols Pró | Média Gols Contra | Status |
|---|---------|-------|----------------|-------------------|--------|
| 1 | **INGLATERRA** | 7 | 3.00 | 0.14 | ✅ Excelente |
| 2 | **HUNGRIA** | 15 | 1.87 | 1.47 | ✅ Bom |
| 3 | **IRLANDA** | 15 | 1.47 | 1.87 | ✅ Bom |
| 4 | **NORUEGA** | 16 | 0.88 | 1.12 | ✅ Excelente |
| 5 | **UCRÂNIA** | 6 | 1.67 | 1.33 | ⚠️ Poucos jogos |
| 6 | **ISLÂNDIA** | 6 | 1.33 | 1.67 | ⚠️ Poucos jogos |
| 7 | **ESCÓCIA** | 5 | 1.00 | 1.00 | ⚠️ Poucos jogos |
| 8 | **ALBÂNIA** | 7 | 0.14 | 3.00 | ✅ Bom |
| 9 | **SÉRVIA** | 1 | 1.00 | 0.00 | ❌ Muito poucos jogos |
| 10 | **LETÔNIA** | 1 | 0.00 | 1.00 | ❌ Muito poucos jogos |

---

## ❌ SELEÇÕES SEM DADOS (6/16):

| # | Seleção | Motivo | Solução |
|---|---------|--------|---------|
| 1 | **BÓSNIA HERZEGOVINA** | Nome nos CSVs: "Bósnia-Herzegovina" (com hífen e acentos) | Adicionar manualmente |
| 2 | **ROMÊNIA** | Nome nos CSVs: "Romênia" (com ê) | Adicionar manualmente |
| 3 | **SUÍÇA** | Nome nos CSVs: "Suíça" (com acentos) | Adicionar manualmente |
| 4 | **SUÉCIA** | Nome nos CSVs: "Suécia" (com acentos) | Adicionar manualmente |
| 5 | **GRÉCIA** | Nome nos CSVs: "Grécia" (com acentos) | Adicionar manualmente |
| 6 | **ITÁLIA** | Nome nos CSVs: "Itália" (com acentos) | Adicionar manualmente |

---

## 📊 ESTATÍSTICAS GERADAS PARA CADA SELEÇÃO:

### **GERAL:**
- ✅ Jogos (total)
- ✅ Gols Pró (total)
- ✅ Gols Contra (total)
- ✅ Média Gols Pró
- ✅ Média Gols Contra
- ✅ Over 2.5 % (jogos com 3+ gols)
- ✅ BTTS Sim % (ambos marcaram)
- ✅ Clean Sheets % (sem sofrer gols)

### **FORMA:**
- ✅ Últimos 5 Jogos (sequência: VVEVD)
- ✅ Pontos Últimos 5

### **CASA:**
- ✅ Jogos Casa
- ✅ Aproveitamento Casa %
- ✅ Gols Pró Casa
- ✅ Gols Contra Casa

### **FORA:**
- ✅ Jogos Fora
- ✅ Aproveitamento Fora %
- ✅ Gols Pró Fora
- ✅ Gols Contra Fora

---

## ⚠️ CAMPOS A PREENCHER MANUALMENTE:

### 1. **Posição** (em todos):
Atualmente está como `0`. Você precisa preencher com:
- Posição no grupo das Eliminatórias
- Ou Ranking FIFA

**Onde buscar:**
- UEFA.com (para grupos das Eliminatórias)
- FIFA.com (para ranking mundial)

---

## 🔧 COMO COMPLETAR OS DADOS:

### **OPÇÃO 1: Editar o CSV gerado**
Arquivo: `Estatisticas_Selecoes_Calculadas.csv`

1. Abrir no Excel/Google Sheets
2. Preencher campo "Posição" para as 10 seleções
3. Adicionar manualmente as 6 seleções faltantes
4. Salvar

### **OPÇÃO 2: Editar o JSON gerado**
Arquivo: `Estatisticas_Selecoes_Calculadas.json`

1. Abrir no editor de texto
2. Preencher `"Posição": 0` para as 10 seleções
3. Copiar e adaptar blocos para as 6 seleções faltantes
4. Salvar

---

## 📝 EXEMPLO DE DADOS A BUSCAR NA INTERNET:

### **Para Bósnia Herzegovina:**
```json
{
  "Time": "BOSNIA HERZEGOVINA",
  "Posição": 2,  // ← BUSCAR NO UEFA.COM (Grupo H)
  "Jogos": 10,  // ← BUSCAR quantos jogos na temporada
  "Média Gols Pró": 1.20,  // ← CALCULAR ou buscar
  "Média Gols Contra": 1.10,
  ...
}
```

**Fontes recomendadas:**
- **UEFA.com** - Estatísticas oficiais das Eliminatórias
- **Transfermarkt.com** - Estatísticas de seleções
- **Flashscore.com** - Estatísticas detalhadas
- **Sofascore.com** - Estatísticas e forma recente

---

## 🎯 PRÓXIMOS PASSOS:

1. ✅ **FEITO:** Cálculo automático de 10 seleções
2. ⏳ **PENDENTE:** Preencher campo "Posição" (você)
3. ⏳ **PENDENTE:** Adicionar 6 seleções faltantes (você)
4. ⏳ **FUTURO:** Integrar com API de Dados Avançados
5. ⏳ **FUTURO:** Testar na interface

---

## 💡 OBSERVAÇÕES:

### **Seleções com poucos dados históricos:**
- **Sérvia** (1 jogo): Dados insuficientes
- **Letônia** (1 jogo): Dados insuficientes
- **Escócia** (5 jogos): Razoável
- **Ucrânia** (6 jogos): Razoável
- **Islândia** (6 jogos): Razoável

**Recomendação:** Buscar dados adicionais na internet para estas seleções.

### **Seleções com bons dados históricos:**
- **Inglaterra** (7 jogos): Excelente
- **Noruega** (16 jogos): Excelente
- **Hungria** (15 jogos): Excelente
- **Irlanda** (15 jogos): Excelente

---

## 📂 ARQUIVOS GERADOS:

1. **`Estatisticas_Selecoes_Calculadas.json`**  
   Formato: JSON para APIs  
   Uso: Backend / APIs

2. **`Estatisticas_Selecoes_Calculadas.csv`**  
   Formato: CSV para edição fácil  
   Uso: Excel / Google Sheets

3. **`RELATORIO_ESTATISTICAS_CALCULADAS.md`** (este arquivo)  
   Formato: Markdown para documentação  
   Uso: Referência / Documentação

---

**🚀 Status:** Dados parcialmente completos - Pronto para complementação manual!

