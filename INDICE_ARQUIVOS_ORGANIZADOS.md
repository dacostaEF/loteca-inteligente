# 📂 ÍNDICE COMPLETO DE ARQUIVOS - LOTECA X-RAY

## 🎯 ARQUIVOS DE ENTRADA (Entry Points)

```
📄 railway_entry.py ..................... Entrada Railway (produção)
📄 wsgi.py .............................. Entrada WSGI (produção)
📄 backend/app.py ....................... Aplicação Flask principal
```

---

## ⚙️ CONFIGURAÇÃO

```
📄 requirements.txt ..................... Dependências Python
📄 Procfile ............................. Config Railway
📄 railway.json ......................... Config Railway
📄 .gitignore (se existir) .............. Arquivos ignorados
```

---

## 🔧 SCRIPTS DE ATUALIZAÇÃO (⚠️ DUPLICADOS)

```
🔴 DUPLICADOS - CONSOLIDAR EM 1:

📄 atualizar_do_csv.py .................. 242 linhas (raiz)
📄 atualizar_tabelas_agora.py ........... 243 linhas (raiz)
📄 atualizar_tabelas_csv.py ............. 242 linhas (raiz)
📄 backend/atualizar_agora.py ........... 68 linhas (backend)
📄 backend/atualizar_manual.py .......... 242 linhas (backend)

📄 backend/atualizar_serie_a_tradicional.py
📄 backend/atualizar_serie_b_tradicional.py
📄 backend/atualizar_serie_c_tradicional.py
```

---

## 🌐 ROTAS/APIS (Backend)

```
📄 backend/app.py ....................... Aplicação principal
📄 backend/routes_brasileirao.py ........ API Brasileirão ⚠️ Imports quebrados!
📄 backend/routes_internacionais.py ..... API Ligas Internacionais
📄 backend/routes_forca_elenco.py ....... API Força de Elenco
📄 backend/routes_auto_classificacao.py . API Classificação Automática
📄 backend/routes_csv_stats.py .......... API Estatísticas CSV
📄 backend/admin_api.py ................. API Interface Admin
```

---

## 🗄️ MODELOS/MANAGERS (Backend)

```
📁 backend/models/

DATABASE HELPERS:
📄 backend/models/__init__.py
📄 backend/models/brasileirao_db.py ..... Database Brasileirão
📄 backend/models/central_dados.py ...... Database Central
📄 backend/models/classificacao_db.py ... Database Classificação

MANAGERS:
📄 backend/models/concurso_manager.py ... Gerencia concursos Loteca
📄 backend/models/confrontos_manager.py . Gerencia confrontos
📄 backend/models/jogos_manager.py ...... Gerencia jogos

OUTROS:
📄 backend/models/create_serie_a_italiana.sql
```

---

## 💾 BANCOS DE DADOS (SQLite)

```
⚠️ POSSÍVEL DUPLICAÇÃO:

📦 backend/models/brasileirao.db
📦 backend/models/central_dados.db
📦 backend/models/tabelas_classificacao.db ... ✅ CORRETO
📦 backend/tabelas_classificacao.db .......... ❓ DUPLICADO?
```

---

## 🔌 SERVIÇOS (Backend)

```
📁 backend/services/

📄 auto_classificacao.py ................ Classificação automática
📄 auto_monitor.py ...................... Monitor automático
📄 cartola_provider.py .................. Provider API Cartola FC
📄 classificacao_integrador.py .......... Integrador de classificação
📄 clubes_unificados.py ................. Clubes unificados
📄 csv_parser_robusto.py ................ Parser CSV robusto
📄 elenco_provider.py ................... Provider dados de elenco
📄 loteca_scraper.py .................... Scraper dados Loteca
```

---

## 🧪 TESTES (Backend)

```
📄 backend/test_serie_a_tradicional.py
📄 backend/test_serie_b_tradicional.py
📄 backend/test_serie_c_tradicional.py
📄 backend/test_ultimos_jogos.py
📄 backend/test_zonas_classificacao.py
```

---

## 🎨 FRONTEND - TEMPLATES HTML

```
📁 backend/templates/

📄 loteca.html .......................... 13.402 linhas! 🔥
📄 admin_interface.html ................. Interface Admin

🗑️ POSSIVELMENTE NÃO USADOS:
📄 exemplo-quadros-comparativos.html
📄 integracao-exemplo.html
📄 quadro_comparativo_jogo1.html
📄 loteca.zip ........................... ❓ Por que tem um ZIP aqui?
```

---

## 🎨 FRONTEND - CSS

```
📁 backend/static/css/

📄 loteca.css ........................... Estilos principais
📄 melhorias-abas.css ................... Melhorias UI abas
```

---

## 🎨 FRONTEND - JAVASCRIPT

```
📁 backend/static/js/

PRINCIPAIS:
📄 loteca-functions.js .................. Funções unificadas
📄 loteca-confrontos.js ................. Carregamento confrontos
📄 loteca-otimizador.js ................. Otimizador de apostas
📄 quadro-comparativo.js ................ Quadros comparativos
📄 dashboard-forca-elenco.js ............ Dashboard força elenco
📄 confrontos-break.js .................. Break de confrontos
📄 comparacao-vantagem.js ............... Comparação vantagem
📄 integracao-quadros.js ................ Integração quadros
📄 navegacao-inteligente.js ............. Navegação inteligente
📄 otimizador-auto.js ................... Otimizador automático
📄 otimizador-jogo1.js .................. Otimizador jogo 1
📄 sticky-tabs-mobile.js ................ Tabs sticky mobile
📄 vinculo-confrontos.js ................ Vínculo confrontos
📄 log-manager.js ....................... Gerenciador de logs

SUBPASTAS:
📁 js/ui/
  📄 notifications.js ................... Notificações UI
  📄 rendering.js ....................... Renderização UI

📁 js/inline/ (3 arquivos)
  📄 loteca-inline-01.js
  📄 loteca-inline-03.js
  📄 loteca-inline-04.js

📁 js/analysis/ (vazia ou com conteúdo?)
📁 js/data/ (vazia ou com conteúdo?)

⚠️ PROBLEMA CONHECIDO:
  loteca-functions.js e loteca-confrontos.js têm 
  MAPEAMENTO DUPLICADO dos jogos (memória ID: 10488994)
```

---

## 🖼️ IMAGENS/RECURSOS ESTÁTICOS

```
📁 backend/static/

LOGOS:
📄 Logo_loteraisinteligente.png
📄 Logo_loteraisinteligente_preto.png
📄 Favicon_LI.png
📄 favicon.ico
📄 placeholder-team-logo.svg

ESCUDOS:
📁 escudos/ ............................ 146 arquivos
  ├── COR_Corinthians/Corinthians.png
  ├── FLA_Flamengo/Flamengo.png
  ├── PAL_Palmeiras/Palmeiras.png
  └── ... (121 .png + 25 .PNG) ......... ⚠️ Inconsistente

DADOS JSON:
📁 valor_elenco/
  📄 elencos_mundiais.json
  📄 forca_elenco_unificado.json
  📄 mapeamento_clubes.json
```

---

## 📊 DADOS - ESTATÍSTICAS

```
📁 backend/estatistica/

TABELAS GERAIS:
📄 estatisticas_brasileirao_2025-10-21.csv
📄 Serie_A_tabela_tradicional.csv
📄 Serie_B_tabela_tradicional.csv
📄 Serie_C_tabela_tradicional.csv
📄 Seria_A_estatisticas_apostas.csv ....... ⚠️ "Seria" ou "Serie"?
📄 Serie_B_estatisticas_apostas.csv

INTERNACIONAIS:
📄 La_Liga_tabela_tradicional.csv
📄 Ligue1_tabela_tradicional.csv
📄 Premier_League_tabela_tradicional.csv

SÉRIE A (por time):
📁 Serie_A/
  ├── flamengo/jogos.csv
  ├── palmeiras/jogos.csv
  ├── corinthians/jogos.csv
  └── ... (20 times)

SÉRIE B (por time):
📁 Serie_B/
  ├── santos/jogos.csv
  ├── sport-recife/jogos.csv
  └── ... (20 times)

SÉRIE C (por time):
📁 Serie_C/
  ├── guarani/jogos.csv
  ├── ponte_preta/jogos.csv
  └── stats_csv_reader_Brasileirao_original.html

🧪 ARQUIVOS DE TESTE/DESENVOLVIMENTO:
📄 stats_csv_reader_Brasileirao.html
```

---

## 📊 DADOS - JOGOS

```
📁 backend/models/Jogos/

DADOS POR TIME (41 times):
📁 [time]/jogos.csv

EXEMPLOS:
  ├── flamengo/jogos.csv
  ├── palmeiras/jogos.csv
  ├── santos/jogos.csv
  └── ...

ARQUIVOS ESPECIAIS:
📄 _serie_a_cinco.json
📄 _serie_b_cinco.json
📄 pastas.json

🧪 ARQUIVOS DE TESTE/DEV:
📄 EstatisticaClubes_SeriaA_fotMob.html
📄 Gera_csv_e_tabelas.html

📝 DOCUMENTAÇÃO:
📄 RANKING_CLUBES_ANALISE.md
📄 RANKING_FINAL_ATUALIZADO_Serie_A.md

⚠️ OBSERVAÇÃO: Há duplicação com backend/estatistica/Serie_X/
```

---

## 🎲 DADOS - CONCURSOS LOTECA

```
📁 backend/models/

CONCURSOS INDIVIDUAIS:
📁 concurso_1213/ (vazio?)
📁 concurso_1214/ (vazio?)
📁 concurso_1215/
  ├── concurso_loteca_1215.csv
  └── analise_rapida/
      ├── jogo_1.json
      ├── jogo_2.json
      └── ...

📁 concurso_1216/
  ├── concurso_loteca_1216.csv
  ├── concurso_1216.json
  ├── 0_AnaliseEstatitica_confrontos.docx
  └── analise_rapida/
      ├── jogo_1.json ... jogo_14.json

📁 concurso_1218/
  ├── concurso_loteca_1218.csv
  └── concurso_1218.json

CONCURSOS CONSOLIDADOS:
📁 concursos/
  ├── concurso_1213.json
  ├── concurso_1214.json
  ├── concurso_1215.json
  └── concurso_1216.json

⚠️ OBSERVAÇÃO: Dados em 2 lugares (pasta individual + consolidado)
```

---

## ⚔️ DADOS - CONFRONTOS

```
📁 backend/models/Confrontos/

CONFRONTOS ATUAIS (25 arquivos):
📄 corinthians_gremio.csv
📄 santos_fortaleza.csv
📄 cruzeiro_vitoria.csv
📄 ... (confrontos brasileiros)

CONFRONTOS INTERNACIONAIS:
📄 Atalanta_vs_Lazio.csv
📄 Atletico-de-Madrid_vs_Osasuna.csv
📄 Liverpool_vs_Mancheter-United.csv
📄 Roma_vs_internazionale.csv
📄 Tottenham_vs_Aston-Villa.csv

HISTÓRICO:
📁 historico/ (38 arquivos CSV)

TOTAL: 63 arquivos CSV de confrontos
```

---

## 📊 DADOS - VALOR DE ELENCO

```
📁 backend/models/EstatisticasElenco/

📄 Valor_Elenco_serie_a_brasileirao.csv
📄 Valor_Elenco_serie_b_brasileirao.csv
📄 Valor_Elenco_top_100_clubes_mais_valiosos.csv

🧪 ARQUIVOS HTML (DEV):
📄 planilha_clubes_futebol_final.html
📄 planilha_clubes_futebol_Versãooriginal.html
```

---

## 📚 DOCUMENTAÇÃO

```
RAIZ:
📄 README.md ............................ Documentação principal
📄 CHECKLIST_AVALIACAO.md
📄 CONFIG_APIS.md
📄 DOCUMENTACAO_TECNICA.md
📄 ESTRUTURA_ABA_ANALISE_RAPIDA_ADMIN.md
📄 GUIA_COMPLETO_SISTEMA_CONCURSOS_LOTECA.md
📄 GUIA_CONFIGURACAO_APIS.md
📄 MAPEAMENTO_COMPLETO_PAGINAS_LOTECA.md
📄 RESPOSTA_DESENVOLVEDOR.md
📄 RESUMO_EXECUTIVO.md

BACKEND:
📄 backend/README.md
📄 backend/CORRECAO_DADOS_CSV.md
📄 backend/CORRECAO_DADOS_RENDERIZADOS.md

📝 TOTAL: 15 arquivos de documentação
```

---

## 🗑️ ARQUIVOS LEGADOS/NÃO USADOS

```
📁 antigos/
  ├── Logo_loteraisinteligente.png
  └── templates/
      └── Logo_loteraisinteligente.png

⚠️ VERIFICAR SE PODE SER DELETADO
```

---

## 📊 RESUMO ESTATÍSTICO

```
TOTAL DE ARQUIVOS POR TIPO:

Python (.py):          ~45 arquivos
JavaScript (.js):      19 arquivos
Markdown (.md):        15 arquivos
HTML (.html):          ~10 arquivos
CSV (.csv):            ~150+ arquivos
JSON (.json):          ~30 arquivos
SQLite (.db):          4 arquivos
PNG/Imagens:           ~150 arquivos
Outros:                ~10 arquivos

TAMANHO DOS ARQUIVOS:

Maior arquivo:         loteca.html (13.402 linhas!)
Duplicações críticas:  5 scripts Python quase idênticos
Código morto:          ~10 arquivos HTML de teste
```

---

## 🎯 ARQUIVOS COM PROBLEMAS IDENTIFICADOS

```
🔴 CRÍTICO:
  • backend/routes_brasileirao.py ....... Imports quebrados
  • atualizar_*.py (5 arquivos) ......... Duplicados
  • backend/tabelas_classificacao.db .... Duplicado?

🟠 IMPORTANTE:
  • backend/templates/loteca.html ....... 13.402 linhas
  • loteca-functions.js ................. Mapeamento duplicado
  • loteca-confrontos.js ................ Mapeamento duplicado
  • escudos/*.PNG ....................... Extensões inconsistentes

🟡 MELHORIAS:
  • railway_entry.py + wsgi.py .......... Setup duplicado
  • Múltiplos logos ..................... 5 cópias
  • Arquivos de teste HTML .............. Não usados?
  • Pasta antigos/ ...................... Lixo?
```

---

**FIM DO ÍNDICE**

Este índice foi gerado pela análise completa do projeto.
Veja mais detalhes em:
- `RELATORIO_ANALISE_CODIGO_COMPLETO.md`
- `RESUMO_PROBLEMAS_VISUAL.md`

