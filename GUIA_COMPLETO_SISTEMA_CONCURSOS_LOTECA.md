# 📚 GUIA COMPLETO - SISTEMA DE CONCURSOS LOTECA X-RAY

**Versão:** 1.0  
**Data:** 29 de Outubro de 2025  
**Autor:** Sistema Loteca X-Ray  

---

## 📑 ÍNDICE

1. [Estrutura do Sistema](#estrutura-do-sistema)
2. [Arquitetura de Arquivos](#arquitetura-de-arquivos)
3. [Componentes Principais](#componentes-principais)
4. [Fluxo de Criação de Novo Concurso](#fluxo-de-criação-de-novo-concurso)
5. [Detalhamento dos Managers](#detalhamento-dos-managers)
6. [Formatos de Arquivo](#formatos-de-arquivo)
7. [Passo a Passo Prático](#passo-a-passo-prático)
8. [Manutenção e Atualização](#manutenção-e-atualização)
9. [Troubleshooting](#troubleshooting)

---

## 1. 📋 ESTRUTURA DO SISTEMA

### 1.1 Visão Geral

O **Loteca X-Ray** é um sistema de análise inteligente de jogos da Loteca que organiza dados em três camadas principais:

1. **CONCURSOS** - Dados específicos de cada concurso da Loteca
2. **CONFRONTOS** - Histórico permanente de confrontos diretos (H2H)
3. **JOGOS** - Estatísticas individuais de cada clube

### 1.2 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────┐
│               SITE CEF (Loteca)                         │
│          https://loterias.caixa.gov.br                  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓ (Scraping ou Manual)
         ┌─────────────────────┐
         │  LotecaScraper      │
         │  loteca_scraper.py  │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │  ConcursoManager    │
         │ Cria pasta/arquivos │
         └──────────┬──────────┘
                    │
       ┌────────────┴────────────┐
       │                         │
       ↓                         ↓
┌──────────────┐         ┌──────────────┐
│ CONFRONTOS   │         │    JOGOS     │
│ (Permanente) │         │ (Por clube)  │
└──────────────┘         └──────────────┘
       │                         │
       └────────────┬────────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │  ANÁLISE RÁPIDA     │
         │  jogo_1.json até    │
         │  jogo_14.json       │
         └─────────────────────┘
```

---

## 2. 🗂️ ARQUITETURA DE ARQUIVOS

### 2.1 Estrutura Completa

```
backend/models/
│
├── concursos/                    ← LOCALIZAÇÃO ANTIGA (compatibilidade)
│   └── concurso_XXXX.json
│
├── concurso_1213/               ← PASTA DE CONCURSO (padrão atual)
│   ├── concurso_1213.json       ← Dados do concurso
│   ├── concurso_loteca_1213.csv ← Jogos em formato CSV
│   ├── 0_AnaliseEstatitica_confrontos.docx
│   └── analise_rapida/          ← Análises individuais
│       ├── jogo_1.json
│       ├── jogo_2.json
│       ├── ...
│       └── jogo_14.json
│
├── concurso_1214/               ← Concurso anterior
├── concurso_1215/               ← Concurso anterior
├── concurso_1216/               ← Concurso atual (exemplo)
│
├── Confrontos/                  ← HISTÓRICO H2H (PERMANENTE)
│   ├── bahia_bragantino.csv
│   ├── ceara_fluminense.csv
│   ├── cruzeiro_vitoria.csv
│   ├── flamengo_sport.csv
│   ├── internacional_atletico-mg.csv
│   └── ... (mais 58 confrontos)
│
├── Jogos/                       ← ESTATÍSTICAS POR CLUBE
│   ├── flamengo/
│   │   └── jogos.csv
│   ├── palmeiras/
│   │   └── jogos.csv
│   ├── sport-recife/
│   │   └── jogos.csv
│   └── ... (um para cada clube)
│
├── concurso_manager.py          ← Gerenciador de concursos
├── confrontos_manager.py        ← Gerenciador de confrontos H2H
└── jogos_manager.py             ← Gerenciador de jogos dos clubes
```

### 2.2 Tipos de Dados

| Tipo | Localização | Permanência | Atualização |
|------|-------------|-------------|-------------|
| **Concursos** | `concurso_XXXX/` | Por concurso | A cada novo concurso |
| **Confrontos** | `Confrontos/` | Permanente | Após cada jogo real |
| **Jogos** | `Jogos/` | Permanente | Após cada jogo real |
| **Análises** | `concurso_XXXX/analise_rapida/` | Por concurso | No momento da criação |

---

## 3. ⚙️ COMPONENTES PRINCIPAIS

### 3.1 ConcursoManager

**Arquivo:** `backend/models/concurso_manager.py`

**Responsabilidades:**
- Criar e gerenciar pastas de concursos
- Salvar e carregar dados de concursos
- Listar todos os concursos disponíveis
- Determinar o próximo número de concurso

**Métodos Principais:**

```python
class ConcursoManager:
    # Salva um novo concurso
    salvar_concurso(numero: str, dados: Dict) -> bool
    
    # Carrega dados de um concurso
    carregar_concurso(numero: str) -> Optional[Dict]
    
    # Lista todos os concursos
    listar_concursos() -> List[Dict]
    
    # Obtém o último concurso
    get_ultimo_concurso() -> Optional[Dict]
    
    # Próximo número disponível
    get_proximo_numero() -> str
    
    # Deleta um concurso
    deletar_concurso(numero: str) -> bool
```

### 3.2 ConfrontosManager

**Arquivo:** `backend/models/confrontos_manager.py`

**Responsabilidades:**
- Gerenciar histórico de confrontos diretos
- Calcular estatísticas H2H (Head-to-Head)
- Analisar tendências de confrontos

**Métodos Principais:**

```python
class ConfrontosManager:
    # Carrega histórico entre dois clubes
    carregar_confrontos(clube1: str, clube2: str) -> List[Dict]
    
    # Analisa confrontos (últimos N jogos)
    analisar_confrontos(clube1: str, clube2: str, ultimos_n: int = 10) -> Dict
    
    # Resumo no formato "3V-5E-2D"
    get_confronto_resumo(clube1: str, clube2: str) -> str
    
    # Lista todos os confrontos disponíveis
    listar_confrontos_disponiveis() -> List[str]
```

**Formato do Resumo:**
- `3V-5E-2D` = 3 Vitórias, 5 Empates, 2 Derrotas (perspectiva do clube 1)

### 3.3 JogosManager

**Arquivo:** `backend/models/jogos_manager.py`

**Responsabilidades:**
- Gerenciar jogos individuais de cada clube
- Calcular estatísticas (PPG, aproveitamento, forma)
- Adicionar/remover/atualizar jogos

**Métodos Principais:**

```python
class JogosManager:
    # Carrega todos os jogos de um clube
    carregar_jogos(clube: str) -> List[Dict]
    
    # Salva jogos de um clube
    salvar_jogos(clube: str, jogos: List[Dict]) -> bool
    
    # Adiciona um novo jogo
    adicionar_jogo(clube: str, jogo: Dict) -> bool
    
    # Calcula estatísticas completas
    calcular_estatisticas(clube: str) -> Dict
    
    # Lista clubes com dados
    listar_clubes_com_jogos() -> List[str]
```

**Estatísticas Calculadas:**
- Total de jogos, vitórias, empates, derrotas
- PPG (Pontos Por Jogo) - Geral, Casa, Fora
- Aproveitamento (%) - Casa e Fora
- Gols marcados/sofridos, saldo de gols
- Clean sheets (jogos sem sofrer gols)
- Sequência atual (ex: "3V" = 3 vitórias seguidas)
- Últimos 5 resultados (ex: "VEVDD")

### 3.4 LotecaScraper

**Arquivo:** `backend/services/loteca_scraper.py`

**Responsabilidades:**
- Capturar dados do site da CEF automaticamente
- Obter número do concurso atual
- Extrair lista de jogos

**Métodos Principais:**

```python
class LotecaScraper:
    # Obtém número do concurso atual
    get_current_concurso_number() -> Optional[int]
    
    # Obtém dados completos do concurso
    get_concurso_data(concurso_num: int) -> Optional[Dict]
```

---

## 4. 🔄 FLUXO DE CRIAÇÃO DE NOVO CONCURSO

### 4.1 Visão Geral do Processo

```
INÍCIO
  │
  ├─→ [1] CAPTURAR JOGOS DO NOVO CONCURSO
  │    ├── Via Scraping (LotecaScraper)
  │    └── OU Manual (CSV)
  │
  ├─→ [2] CRIAR ESTRUTURA DE PASTAS
  │    └── concurso_XXXX/
  │         ├── concurso_XXXX.json
  │         ├── concurso_loteca_XXXX.csv
  │         └── analise_rapida/
  │
  ├─→ [3] PROCESSAR CADA JOGO (1-14)
  │    │
  │    ├─→ [3.1] VERIFICAR CONFRONTO
  │    │    ├── Existe? → Usar CSV existente
  │    │    └── Não existe? → Criar novo CSV
  │    │
  │    ├─→ [3.2] BUSCAR ESTATÍSTICAS
  │    │    ├── Carregar Jogos/{clube}/jogos.csv
  │    │    ├── Calcular posição na tabela
  │    │    ├── Calcular forma recente
  │    │    └── Calcular fator casa/fora
  │    │
  │    └─→ [3.3] GERAR ANÁLISE
  │         └── Criar analise_rapida/jogo_X.json
  │
  ├─→ [4] APÓS JOGOS ACONTECEREM
  │    ├── Atualizar Jogos/{clube}/jogos.csv
  │    └── Atualizar Confrontos/{clube1}_{clube2}.csv
  │
FIM
```

### 4.2 Detalhamento dos Passos

#### PASSO 1: CAPTURAR JOGOS

**Método 1: Scraping Automático**
```python
scraper = LotecaScraper()
numero = scraper.get_current_concurso_number()
dados = scraper.get_concurso_data(numero)
```

**Método 2: Manual (CSV)**
```csv
Jogo,Coluna 1,Coluna 2,Data
1,FLAMENGO/SP,PALMEIRAS/SP,Domingo
2,INTERNACIONAL,SPORT/PE,Domingo
3,CORINTHIANS/SP,ATLETICO/MG,Sábado
...
14,GETAFE,REAL MADRID,Domingo
```

#### PASSO 2: CRIAR ESTRUTURA

**Código Python:**
```python
from backend.models.concurso_manager import concurso_manager

# Preparar dados
dados_concurso = {
    "concurso": {},
    "jogos": [
        {
            "numero": 1,
            "time_casa": "FLAMENGO/SP",
            "time_fora": "PALMEIRAS/SP",
            "data": "Domingo"
        },
        # ... mais 13 jogos
    ],
    "estatisticas": {}
}

# Salvar
sucesso = concurso_manager.salvar_concurso("1217", dados_concurso)
```

**O que acontece:**
1. Sistema cria pasta `backend/models/concurso_1217/`
2. Salva arquivo `concurso_1217.json` com metadados
3. Cria subpasta `analise_rapida/`

#### PASSO 3: PROCESSAR JOGOS

**Para cada jogo (1 a 14):**

```python
from backend.models.confrontos_manager import ConfrontosManager
from backend.models.jogos_manager import jogos_manager

confrontos_mgr = ConfrontosManager()

# 3.1 - Verificar confronto
clube1 = "flamengo"
clube2 = "palmeiras"
confronto_direto = confrontos_mgr.analisar_confrontos(clube1, clube2)

# 3.2 - Buscar estatísticas
stats_flamengo = jogos_manager.calcular_estatisticas(clube1)
stats_palmeiras = jogos_manager.calcular_estatisticas(clube2)

# 3.3 - Gerar análise
analise = {
    "metadados": {
        "jogo_numero": "1",
        "concurso_numero": "1217"
    },
    "dados": {
        "numero": "1",
        "time_casa": "Flamengo/RJ",
        "time_fora": "Palmeiras/SP",
        "posicao_casa": str(stats_flamengo['posicao']),
        "posicao_fora": str(stats_palmeiras['posicao']),
        "confronto_direto": confronto_direto['resumo'],
        "ppg_casa": stats_flamengo['ppg'],
        "ppg_fora": stats_palmeiras['ppg'],
        "ultimos_5_casa": stats_flamengo['ultimos_5_resultados'],
        "ultimos_5_fora": stats_palmeiras['ultimos_5_resultados'],
        # ... mais dados
    }
}

# Salvar em analise_rapida/jogo_1.json
```

#### PASSO 4: ATUALIZAR APÓS JOGOS

**Quando os jogos acontecerem:**

```python
# Adicionar resultado ao histórico do clube
jogo_resultado = {
    'data': '2025-10-29',
    'time_casa': 'Fla',
    'gols_casa': 2,
    'gols_visitante': 1,
    'time_visitante': 'Pal',
    'local': 'Maracanã',
    'resultado': 'V',  # V=Vitória, E=Empate, D=Derrota
    'pontos': 3
}

jogos_manager.adicionar_jogo('flamengo', jogo_resultado)

# Adicionar ao histórico de confrontos
# (Manualmente editar o CSV em Confrontos/flamengo_palmeiras.csv)
```

---

## 5. 📊 FORMATOS DE ARQUIVO

### 5.1 concurso_XXXX.json

```json
{
  "metadados": {
    "numero": "1217",
    "salvo_em": "2025-10-29T15:30:00.000000",
    "versao": "1.0"
  },
  "concurso": {
    "data_sorteio": "2025-11-03",
    "valor_premio": "1000000.00"
  },
  "jogos": [
    {
      "numero": 1,
      "time_casa": "FLAMENGO/SP",
      "time_fora": "PALMEIRAS/SP",
      "data": "Domingo"
    }
  ],
  "estatisticas": {}
}
```

### 5.2 concurso_loteca_XXXX.csv

```csv
Jogo,Coluna 1,Coluna 2,Data
1,FLAMENGO/SP,PALMEIRAS/SP,Domingo
2,INTERNACIONAL,SPORT/PE,Domingo
3,CORINTHIANS/SP,ATLETICO/MG,Sábado
...
```

### 5.3 analise_rapida/jogo_X.json

```json
{
  "metadados": {
    "jogo_numero": "1",
    "concurso_numero": "1217"
  },
  "dados": {
    "numero": "1",
    "time_casa": "Flamengo/RJ",
    "time_fora": "Palmeiras/SP",
    "arena": "Maracanã/RJ",
    "campeonato": "Brasileirão Série A",
    "dia": "Domingo",
    "escudo_casa": "/static/escudos/FLA_Flamengo/Flamengo.png",
    "escudo_fora": "/static/escudos/PAL_Palmeiras/Palmeiras.png",
    "probabilidade_casa": "40",
    "probabilidade_empate": "30",
    "probabilidade_fora": "30",
    "recomendacao": "Recomendação Estatística: Coluna 1 (Flamengo) - Risco Alto",
    "conclusao_analista": "Análise detalhada...",
    "confrontos_sequence": "D-E-V-V-E-V-E-V-E-E",
    "posicao_casa": "2",
    "posicao_fora": "1",
    "confronto_direto": "3V-5E-2D",
    "fator_casa": "60%",
    "fator_fora": "40%",
    "analise_posicao": "Confronto Equilibrado",
    "analise_confronto_direto": "Confronto Equilibrado",
    "analise_fator_casa": "Flamengo Favorito",
    "sincronizado_em": "2025-10-29T16:21:41.661Z"
  },
  "admin_key": "loteca2024admin"
}
```

### 5.4 Confrontos/{clube1}_{clube2}.csv

```csv
Data,Mandante,Placar,Visitante,Vencedor,Rodada,Competição
2021-12-03,Sport,1-1,Flamengo,Empate,R35,Brasileirão 2021
2021-08-15,Flamengo,2-0,Sport,Flamengo,R16,Brasileirão 2021
2021-02-01,Sport,0-3,Flamengo,Flamengo,R33,Brasileirão 2020
...
```

**IMPORTANTE:**
- Nome do arquivo: Sempre em ordem alfabética
- Exemplo: `flamengo_sport.csv` (F antes de S)
- Histórico completo, todos os jogos passados

### 5.5 Jogos/{clube}/jogos.csv

```csv
data,time_casa,gols_casa,gols_visitante,time_visitante,local,resultado,pontos
2024-10-20,Fla,2,1,Pal,Maracanã,V,3
2024-10-13,São,1,1,Fla,Morumbi,E,1
2024-10-06,Fla,3,0,Bot,Maracanã,V,3
...
```

**Campos:**
- `data`: Data do jogo (YYYY-MM-DD)
- `time_casa`: Abreviação do time da casa
- `gols_casa`: Gols marcados pelo time da casa
- `gols_visitante`: Gols marcados pelo visitante
- `time_visitante`: Abreviação do visitante
- `local`: Estádio
- `resultado`: V/E/D (perspectiva do clube)
- `pontos`: 3 (vitória), 1 (empate), 0 (derrota)

---

## 6. 📝 PASSO A PASSO PRÁTICO

### 6.1 Criar Novo Concurso Manualmente

**ETAPA 1: Obter lista de jogos**

Acesse: https://loterias.caixa.gov.br → Loteca

Copie os 14 jogos do próximo concurso.

**ETAPA 2: Criar CSV**

Crie arquivo `concurso_loteca_1217.csv`:

```csv
Jogo,Coluna 1,Coluna 2,Data
1,FLAMENGO/RJ,PALMEIRAS/SP,Domingo
2,INTERNACIONAL/RS,SPORT/PE,Domingo
...
14,GETAFE,REAL MADRID,Domingo
```

**ETAPA 3: Executar script de criação**

```python
import json
import os
from backend.models.concurso_manager import concurso_manager

numero = "1217"

# Preparar jogos
jogos = []
# Ler do CSV e popular lista de jogos

dados = {
    "concurso": {
        "data_sorteio": "2025-11-03"
    },
    "jogos": jogos,
    "estatisticas": {}
}

# Salvar
concurso_manager.salvar_concurso(numero, dados)
```

**ETAPA 4: Gerar análises**

Para cada jogo, criar arquivo JSON com análise completa.

### 6.2 Atualizar Confrontos

**Quando criar novo confronto:**

1. Verificar se já existe: `Confrontos/{clube1}_{clube2}.csv`
2. Se não existe, criar novo arquivo:

```csv
Data,Mandante,Placar,Visitante,Vencedor,Rodada,Competição
```

3. Se existe, adicionar nova linha ao final

**Exemplo de nova linha:**
```csv
2025-10-29,Flamengo,2-1,Palmeiras,Flamengo,R32,Brasileirão 2025
```

### 6.3 Atualizar Jogos dos Clubes

**Após cada jogo real:**

```python
from backend.models.jogos_manager import jogos_manager

# Adicionar jogo ao Flamengo
jogo = {
    'data': '2025-10-29',
    'time_casa': 'Fla',
    'gols_casa': 2,
    'gols_visitante': 1,
    'time_visitante': 'Pal',
    'local': 'Maracanã',
    'resultado': 'V',
    'pontos': 3
}

jogos_manager.adicionar_jogo('flamengo', jogo)

# Adicionar jogo ao Palmeiras (perspectiva invertida)
jogo_palmeiras = {
    'data': '2025-10-29',
    'time_casa': 'Fla',
    'gols_casa': 2,
    'gols_visitante': 1,
    'time_visitante': 'Pal',
    'local': 'Maracanã',
    'resultado': 'D',  # Derrota para o Palmeiras
    'pontos': 0
}

jogos_manager.adicionar_jogo('palmeiras', jogo_palmeiras)
```

---

## 7. 🔧 MANUTENÇÃO E ATUALIZAÇÃO

### 7.1 Ciclo de Vida de um Concurso

```
┌──────────────────────────────────────────────────────┐
│ FASE 1: CRIAÇÃO (Segunda-feira após sorteio)        │
│ - Obter jogos do próximo concurso                   │
│ - Criar estrutura de pastas                         │
│ - Gerar análises preliminares                       │
└──────────────────┬───────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────┐
│ FASE 2: ANÁLISE (Terça a Sexta)                     │
│ - Atualizar estatísticas                            │
│ - Refinar análises                                  │
│ - Adicionar insights                                │
└──────────────────┬───────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────┐
│ FASE 3: JOGOS (Sábado/Domingo)                      │
│ - Acompanhar resultados                             │
└──────────────────┬───────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────┐
│ FASE 4: ATUALIZAÇÃO (Após jogos)                    │
│ - Atualizar Jogos/{clube}/jogos.csv                 │
│ - Atualizar Confrontos/{clube1}_{clube2}.csv        │
│ - Recalcular estatísticas                           │
└──────────────────────────────────────────────────────┘
```

### 7.2 Backup e Versionamento

**Recomendações:**

1. **Backup semanal** da pasta `backend/models/`
2. **Git commit** após criar cada concurso
3. **Manter histórico** de pelo menos 10 concursos
4. **Arquivar** concursos antigos após 3 meses

### 7.3 Limpeza de Dados

**Quando fazer:**
- Remover concursos com mais de 6 meses
- Consolidar confrontos duplicados
- Verificar integridade dos CSVs

**Script de exemplo:**
```python
from backend.models.concurso_manager import concurso_manager

# Listar concursos antigos
concursos = concurso_manager.listar_concursos()
for c in concursos:
    if int(c['numero']) < 1200:  # Concursos muito antigos
        concurso_manager.deletar_concurso(c['numero'])
```

---

## 8. 🆘 TROUBLESHOOTING

### 8.1 Problemas Comuns

#### Problema: Confronto não encontrado

**Sintoma:**
```
Arquivo de confronto não encontrado: Confrontos/flamengo_palmeiras.csv
```

**Solução:**
1. Verificar se o arquivo existe
2. Verificar nomenclatura (ordem alfabética)
3. Criar novo arquivo se necessário

**Comando:**
```python
from backend.models.confrontos_manager import ConfrontosManager
mgr = ConfrontosManager()
confrontos = mgr.listar_confrontos_disponiveis()
print(confrontos)  # Ver quais existem
```

#### Problema: Estatísticas incorretas

**Sintoma:**
- PPG negativo
- Aproveitamento acima de 100%
- Sequência estranha

**Solução:**
1. Verificar formato dos jogos.csv
2. Verificar campo `resultado` (deve ser V/E/D)
3. Verificar campo `pontos` (0/1/3)

**Verificação:**
```python
from backend.models.jogos_manager import jogos_manager

jogos = jogos_manager.carregar_jogos('flamengo')
for j in jogos:
    print(f"{j['data']} - {j['resultado']} - {j['pontos']} pts")
```

#### Problema: Concurso não carrega

**Sintoma:**
```
⚠️ Concurso 1217 não encontrado
```

**Solução:**
1. Verificar se a pasta existe: `backend/models/concurso_1217/`
2. Verificar se o JSON existe dentro da pasta
3. Verificar formato do JSON (sintaxe válida)

**Verificação:**
```python
import os
path = "backend/models/concurso_1217/"
print(f"Pasta existe: {os.path.exists(path)}")
print(f"Conteúdo: {os.listdir(path)}")
```

### 8.2 Validação de Dados

**Script de validação completo:**

```python
#!/usr/bin/env python3
"""Script de validação do sistema"""

from backend.models.concurso_manager import concurso_manager
from backend.models.confrontos_manager import ConfrontosManager
from backend.models.jogos_manager import jogos_manager

def validar_sistema():
    print("🔍 VALIDANDO SISTEMA LOTECA X-RAY")
    print("=" * 50)
    
    # 1. Validar concursos
    print("\n📁 Concursos:")
    concursos = concurso_manager.listar_concursos()
    print(f"   Total: {len(concursos)}")
    for c in concursos[:3]:
        print(f"   - {c['numero']}: {c['total_jogos']} jogos")
    
    # 2. Validar confrontos
    print("\n⚔️ Confrontos:")
    confrontos_mgr = ConfrontosManager()
    confrontos = confrontos_mgr.listar_confrontos_disponiveis()
    print(f"   Total: {len(confrontos)}")
    
    # 3. Validar jogos
    print("\n⚽ Jogos:")
    clubes = jogos_manager.listar_clubes_com_jogos()
    print(f"   Clubes com dados: {len(clubes)}")
    
    print("\n✅ Validação concluída!")

if __name__ == "__main__":
    validar_sistema()
```

### 8.3 Logs e Debug

**Ativar logs detalhados:**

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Locais de log:**
- `ConcursoManager`: Criação/carregamento de concursos
- `ConfrontosManager`: Análise de confrontos
- `JogosManager`: Cálculo de estatísticas
- `LotecaScraper`: Scraping do site CEF

---

## 9. 📊 REFERÊNCIA RÁPIDA

### 9.1 Comandos Úteis

```python
# Criar novo concurso
from backend.models.concurso_manager import concurso_manager
concurso_manager.salvar_concurso("1217", dados)

# Listar concursos
concursos = concurso_manager.listar_concursos()

# Carregar concurso específico
dados = concurso_manager.carregar_concurso("1217")

# Analisar confronto
from backend.models.confrontos_manager import ConfrontosManager
mgr = ConfrontosManager()
analise = mgr.analisar_confrontos("flamengo", "palmeiras")

# Calcular estatísticas de clube
from backend.models.jogos_manager import jogos_manager
stats = jogos_manager.calcular_estatisticas("flamengo")

# Adicionar jogo
jogo = {
    'data': '2025-10-29',
    'time_casa': 'Fla',
    'gols_casa': 2,
    'gols_visitante': 1,
    'time_visitante': 'Pal',
    'local': 'Maracanã',
    'resultado': 'V',
    'pontos': 3
}
jogos_manager.adicionar_jogo("flamengo", jogo)
```

### 9.2 Estrutura de Dados - Resumo

| Tipo | Formato | Localização | Exemplo |
|------|---------|-------------|---------|
| Concurso | JSON | `concurso_XXXX/` | `concurso_1217.json` |
| Lista jogos | CSV | `concurso_XXXX/` | `concurso_loteca_1217.csv` |
| Análise jogo | JSON | `concurso_XXXX/analise_rapida/` | `jogo_1.json` |
| Confronto H2H | CSV | `Confrontos/` | `flamengo_palmeiras.csv` |
| Jogos clube | CSV | `Jogos/{clube}/` | `jogos.csv` |

### 9.3 Fluxo de Dados - Diagrama Simplificado

```
CEF → Scraper → ConcursoManager → [Pasta concurso_XXXX]
                       ↓
                 Para cada jogo:
                       ↓
         ConfrontosManager ← [Confrontos/]
                       ↓
         JogosManager ← [Jogos/{clube}/]
                       ↓
              [analise_rapida/jogo_X.json]
```

---

## 10. 📞 CONTATO E SUPORTE

### 10.1 Documentação Adicional

- **README.md** - Visão geral do projeto
- **CONFIG_APIS.md** - Configuração de APIs
- **DOCUMENTACAO_TECNICA.md** - Detalhes técnicos
- **GUIA_CONFIGURACAO_APIS.md** - Setup de APIs externas

### 10.2 Arquivos de Referência

- `backend/models/concurso_manager.py` - Lógica de concursos
- `backend/models/confrontos_manager.py` - Lógica de confrontos
- `backend/models/jogos_manager.py` - Lógica de jogos
- `backend/services/loteca_scraper.py` - Web scraping

### 10.3 Versão do Sistema

**Versão atual:** 1.0  
**Última atualização:** 29/10/2025  
**Python:** 3.8+  
**Dependências:** requests, BeautifulSoup4, Flask

---

## 📝 CHECKLIST DE NOVO CONCURSO

Use este checklist ao criar um novo concurso:

- [ ] 1. Obter lista de 14 jogos do site CEF
- [ ] 2. Criar arquivo CSV com os jogos
- [ ] 3. Executar script de criação de concurso
- [ ] 4. Verificar se pasta foi criada corretamente
- [ ] 5. Para cada jogo (1-14):
  - [ ] Verificar se confronto H2H existe
  - [ ] Criar confronto se necessário
  - [ ] Gerar análise individual
  - [ ] Verificar escudos dos times
  - [ ] Validar dados gerados
- [ ] 6. Testar API endpoints
- [ ] 7. Fazer backup dos dados
- [ ] 8. Commit no Git

---

## 🎯 CONCLUSÃO

Este guia fornece uma visão completa do **Sistema de Concursos Loteca X-Ray**.

**Principais pontos:**

✅ **Estrutura modular** com managers especializados  
✅ **Dados permanentes** (Confrontos e Jogos)  
✅ **Dados temporários** (Concursos por semana)  
✅ **Análises automáticas** baseadas em estatísticas reais  
✅ **Manutenção simplificada** com scripts auxiliares  

**Para dúvidas:**
- Consultar os arquivos de código-fonte
- Verificar logs do sistema
- Usar scripts de validação

---

**Documento gerado em:** 29 de Outubro de 2025  
**Sistema:** Loteca X-Ray v1.0  
**Autor:** Sistema de Documentação Automática  

---


