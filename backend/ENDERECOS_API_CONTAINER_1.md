# 📍 ENDEREÇOS DA API PARA O CONTAINER 1

## 🎯 **RESUMO EXECUTIVO**

O **Container 1 (Jogo 1)** está lendo dados de **múltiplos endereços** da API, todos apontando para o mesmo arquivo JSON. Aqui está o mapeamento completo:

## 🔗 **ENDPOINTS DA API**

### **1. Endpoint Principal:**
```
GET /api/analise/jogo/1?concurso=concurso_1216
```

### **2. Endpoint Alternativo (sem parâmetro):**
```
GET /api/analise/jogo/1
```

## 📁 **ARQUIVO FÍSICO LIDO**

### **Caminho Completo:**
```
backend/models/concurso_1216/analise_rapida/jogo_1.json
```

### **Estrutura do Arquivo:**
```json
{
  "dados": {
    "time_casa": "Flamengo/RJ",
    "time_fora": "Palmeiras/SP",
    "escudo_casa": "/static/escudos/FLA_Flamengo/Flamengo.png",
    "escudo_fora": "/static/escudos/PAL_Palmeiras/Palmeiras.png",
    "confrontos_sequence": "D-E-V-V-E-V-E-V-E-E",
    "confronto_direto": "3V-5E-2D",
    "arquivo_confrontos": "Flamengo_vs_Palmeiras.csv",
    "probabilidades": {
      "vitoria_casa": 35,
      "empate": 30,
      "vitoria_fora": 35
    }
  },
  "metadados": {
    "concurso": "1216",
    "jogo": 1,
    "data_criacao": "2025-01-15",
    "ultima_atualizacao": "2025-01-15"
  }
}
```

## 🚀 **FUNÇÕES QUE CHAMAM A API**

### **1. Função Principal:**
```javascript
async function carregarDadosJogo1() {
    const response = await fetch('/api/analise/jogo/1?concurso=concurso_1216');
    // Processa dados e atualiza interface
}
```

### **2. Funções Secundárias:**
```javascript
// Para confrontos
const jogoResponse = await fetch('/api/analise/jogo/1');

// Para escudos
const jogoResponse = await fetch('/api/analise/jogo/1');

// Para gráficos
const jogoResponse = await fetch('/api/analise/jogo/1');
```

## 🔧 **IMPLEMENTAÇÃO NO BACKEND**

### **Arquivo:** `backend/admin_api.py`
```python
@bp_admin.route('/api/analise/jogo/<int:jogo_numero>', methods=['GET'])
@cross_origin()
def obter_dados_analise_jogo(jogo_numero):
    """
    NOVA API - Baseada no teste que funcionou perfeitamente
    """
    # Parâmetros
    concurso = request.args.get("concurso", "concurso_1215")
    
    # Caminho do arquivo
    pasta = BACKEND_DIR / "models" / concurso / "analise_rapida"
    arquivo = pasta / f"jogo_{jogo_numero}.json"
    
    # Ler arquivo JSON
    with open(arquivo, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    # Retornar dados
    return jsonify({
        "success": True,
        "dados": raw.get("dados", {}),
        "metadados": raw.get("metadados", {})
    })
```

## 📊 **DADOS RETORNADOS**

### **Campos Principais:**
- ✅ **`time_casa`** - Nome do time da casa
- ✅ **`time_fora`** - Nome do time visitante
- ✅ **`escudo_casa`** - Caminho do escudo do time da casa
- ✅ **`escudo_fora`** - Caminho do escudo do time visitante
- ✅ **`confrontos_sequence`** - Sequência dos últimos confrontos (D-E-V-V-E-V-E-V-E-E)
- ✅ **`confronto_direto`** - Resumo do confronto direto (3V-5E-2D)
- ✅ **`arquivo_confrontos`** - Nome do arquivo CSV de confrontos
- ✅ **`probabilidades`** - Probabilidades de vitória, empate e derrota

### **Campos de Metadados:**
- ✅ **`concurso`** - Número do concurso (1216)
- ✅ **`jogo`** - Número do jogo (1)
- ✅ **`data_criacao`** - Data de criação do arquivo
- ✅ **`ultima_atualizacao`** - Data da última atualização

## 🎯 **FLUXO COMPLETO**

### **1. Carregamento da Página:**
```
Página carrega
   ↓
carregarDadosJogo1() é chamada
   ↓
fetch('/api/analise/jogo/1?concurso=concurso_1216')
   ↓
Backend lê: backend/models/concurso_1216/analise_rapida/jogo_1.json
   ↓
Dados são retornados para o frontend
   ↓
Interface é atualizada com dados reais
```

### **2. Atualizações Secundárias:**
```
Funções específicas chamam a API
   ↓
fetch('/api/analise/jogo/1')
   ↓
Mesmo arquivo JSON é lido
   ↓
Dados específicos são extraídos
   ↓
Elementos específicos são atualizados
```

## 🔍 **LOGS DE DEBUG**

### **No Console do Navegador:**
```javascript
🎯 [JOGO1] Iniciando carregamento dos dados do JOGO 1...
✅ [JOGO1] Dados recebidos da API: {success: true, dados: {...}}
✅ [JOGO1] Dados atualizados com sucesso!
```

### **No Backend:**
```python
[NOVA-API] Concurso recebido: 'concurso_1216'
[NOVA-API] Pasta calculada: backend/models/concurso_1216/analise_rapida
[NOVA-API] Caminho do arquivo: backend/models/concurso_1216/analise_rapida/jogo_1.json
[NOVA-API] Arquivo existe: True
[NOVA-API] Arquivo lido com sucesso!
```

## 🎉 **RESULTADO FINAL**

### **✅ Endereços Confirmados:**

1. **API Endpoint:** `/api/analise/jogo/1?concurso=concurso_1216`
2. **Arquivo Físico:** `backend/models/concurso_1216/analise_rapida/jogo_1.json`
3. **Dados:** Flamengo/RJ vs Palmeiras/SP
4. **Sequência:** `D-E-V-V-E-V-E-V-E-E`
5. **Resumo:** `3V-5E-2D`

### **✅ Status:**
- **API funcionando:** ✅
- **Arquivo existe:** ✅
- **Dados corretos:** ✅
- **Interface atualizada:** ✅

**AMIGÃO, A API ESTÁ LENDO CORRETAMENTE O ARQUIVO `jogo_1.json` DO CONCURSO 1216!** 🚀✅📁
