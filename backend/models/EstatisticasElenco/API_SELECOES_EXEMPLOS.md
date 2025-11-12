# 🌍 API de Seleções Nacionais - Exemplos de Uso

## 📋 Endpoints Disponíveis

### 1️⃣ Listar Todas as Seleções
```
GET /api/selecoes/todas
```

**Resposta:**
```json
{
  "success": true,
  "total": 53,
  "selecoes": [
    {
      "posicao": 1,
      "selecao": "Inglaterra",
      "valor_mercado_milhoes": 1410.0,
      "valor_mercado_texto": "€ 1.41 bilhão",
      "continente": "Europa",
      "confederacao": "UEFA"
    },
    ...
  ],
  "fonte": "Transfermarkt 2025"
}
```

---

### 2️⃣ Buscar Seleção Específica
```
GET /api/selecoes/buscar/<nome>
```

**Exemplos:**
- `/api/selecoes/buscar/Brasil`
- `/api/selecoes/buscar/Inglaterra`
- `/api/selecoes/buscar/Bosnia` (normaliza automaticamente)

**Resposta:**
```json
{
  "success": true,
  "selecao": {
    "posicao": 4,
    "selecao": "Brasil",
    "valor_mercado_milhoes": 941.6,
    "valor_mercado_texto": "€ 941.6 milhões",
    "continente": "América do Sul",
    "confederacao": "CONMEBOL"
  },
  "fonte": "Transfermarkt 2025"
}
```

---

### 3️⃣ Comparar Duas Seleções
```
POST /api/selecoes/comparar
Content-Type: application/json

{
  "time_casa": "Brasil",
  "time_fora": "Argentina"
}
```

**Resposta:**
```json
{
  "success": true,
  "time_casa": {
    "posicao": 4,
    "selecao": "Brasil",
    "valor_mercado_milhoes": 941.6,
    ...
  },
  "time_fora": {
    "posicao": 8,
    "selecao": "Argentina",
    "valor_mercado_milhoes": 781.5,
    ...
  },
  "comparacao": {
    "diferenca_valor_milhoes": 160.1,
    "diferenca_percentual": 20.5,
    "favorito": "Brasil",
    "vantagem": "Ligeira Vantagem",
    "valor_casa": 941.6,
    "valor_fora": 781.5
  },
  "fonte": "Transfermarkt 2025"
}
```

---

### 4️⃣ Top N Seleções Mais Valiosas
```
GET /api/selecoes/top/<limite>
```

**Exemplos:**
- `/api/selecoes/top/10` (Top 10)
- `/api/selecoes/top/20` (Top 20)

**Resposta:**
```json
{
  "success": true,
  "total": 10,
  "limite_solicitado": 10,
  "selecoes": [
    {
      "posicao": 1,
      "selecao": "Inglaterra",
      "valor_mercado_milhoes": 1410.0,
      ...
    },
    ...
  ],
  "fonte": "Transfermarkt 2025"
}
```

---

### 5️⃣ Seleções por Confederação
```
GET /api/selecoes/por-confederacao/<confederacao>
```

**Confederações disponíveis:**
- `UEFA` (Europa)
- `CONMEBOL` (América do Sul)
- `CONCACAF` (América do Norte e Central)
- `CAF` (África)
- `AFC` (Ásia)
- `OFC` (Oceania)

**Exemplo:**
```
GET /api/selecoes/por-confederacao/UEFA
```

**Resposta:**
```json
{
  "success": true,
  "confederacao": "UEFA",
  "total": 35,
  "selecoes": [
    {
      "posicao": 1,
      "selecao": "Inglaterra",
      "valor_mercado_milhoes": 1410.0,
      ...
    },
    ...
  ],
  "fonte": "Transfermarkt 2025"
}
```

---

## 🎯 Jogos da Loteca com Seleções

### Jogo 4: Bósnia e Herzegovina vs Romênia
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Bosnia Herzegovina","time_fora":"Romênia"}'
```

### Jogo 5: Suíça vs Suécia
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Suíça","time_fora":"Suécia"}'
```

### Jogo 6: Grécia vs Escócia
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Grécia","time_fora":"Escócia"}'
```

### Jogo 7: Hungria vs Irlanda
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Hungria","time_fora":"Irlanda"}'
```

### Jogo 10: Albânia vs Inglaterra
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Albânia","time_fora":"Inglaterra"}'
```

### Jogo 11: Sérvia vs Letônia
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Sérvia","time_fora":"Letônia"}'
```

### Jogo 12: Itália vs Noruega
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Itália","time_fora":"Noruega"}'
```

### Jogo 14: Ucrânia vs Islândia
```bash
curl -X POST http://localhost:5001/api/selecoes/comparar \
  -H "Content-Type: application/json" \
  -d '{"time_casa":"Ucrânia","time_fora":"Islândia"}'
```

---

## 🔧 Normalização Automática de Nomes

A API normaliza automaticamente variações de nomes:

- `Bosnia` → `Bósnia e Herzegovina`
- `Bosnia Herzegovina` → `Bósnia e Herzegovina`
- `Romenia` → `Romênia`
- `Romania` → `Romênia`
- `Suica` → `Suíça`
- `Suecia` → `Suécia`
- `Grecia` → `Grécia`
- `Escocia` → `Escócia`
- E muitos outros...

---

## 📊 Classificação de Vantagem

A API classifica automaticamente a vantagem entre seleções:

| Diferença % | Classificação |
|------------|---------------|
| < 10% | Muito Equilibrado |
| 10-25% | Ligeira Vantagem |
| 25-50% | Vantagem Moderada |
| 50-100% | Grande Vantagem |
| > 100% | Vantagem Esmagadora |

---

## 🚀 Testando a API

### PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/selecoes/buscar/Brasil" -Method Get
```

### JavaScript (Frontend):
```javascript
async function buscarSelecao(nome) {
    const response = await fetch(`http://localhost:5001/api/selecoes/buscar/${nome}`);
    const data = await response.json();
    console.log(data);
}

buscarSelecao('Brasil');
```

### jQuery (Frontend):
```javascript
$.ajax({
    url: 'http://localhost:5001/api/selecoes/comparar',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        time_casa: 'Brasil',
        time_fora: 'Argentina'
    }),
    success: function(data) {
        console.log(data);
    }
});
```

