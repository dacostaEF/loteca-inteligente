# 🚀 LOTECA X-RAY - BACKEND API

Backend Flask para servir dados reais do **Cartola FC** e preparar integração com APIs internacionais.

## 🎯 **FUNCIONALIDADES**

### ✅ **Já Implementado:**
- **Provider Cartola FC** com cache inteligente
- **Rotas RESTful** para clubes e estatísticas
- **CORS configurado** para frontend
- **Tratamento de erros** robusto
- **Health check** da API

### 🔄 **Endpoints Disponíveis:**

```bash
GET /                           # Info da API
GET /api/br/health             # Status da API
GET /api/br/clubes             # Lista todos os clubes
GET /api/br/clube/8/stats      # Estatísticas do clube (ID 8 = Corinthians)
GET /api/br/confronto/corinthians/flamengo  # Comparar dois times
GET /api/br/mercado/status     # Status do mercado Cartola
GET /api/br/mappings           # Mapeamento nome → ID
```

## 🛠️ **INSTALAÇÃO**

```bash
# 1. Navegar para o diretório
cd backend

# 2. Criar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar servidor
python app.py
```

## 🧪 **TESTAR API**

```bash
# Health Check
curl http://127.0.0.1:5000/api/br/health

# Listar clubes
curl http://127.0.0.1:5000/api/br/clubes

# Stats do Corinthians
curl http://127.0.0.1:5000/api/br/clube/8/stats

# Confronto
curl http://127.0.0.1:5000/api/br/confronto/corinthians/flamengo
```

## 📊 **EXEMPLO DE RESPOSTA**

### `GET /api/br/clube/8/stats`
```json
{
  "success": true,
  "clube_id": 8,
  "data": {
    "clube_id": 8,
    "total_atletas": 25,
    "pct_provaveis": 85.2,
    "media_pontos_elenco": 6.45,
    "preco_medio": 12.5,
    "rating": 0.645,
    "status": "Dados reais"
  }
}
```

## 🔗 **INTEGRAÇÃO COM FRONTEND**

Atualizar o `CartolaProvider` no frontend para usar o backend:

```javascript
class CartolaProvider {
    constructor() {
        this.API_BASE = 'http://127.0.0.1:5000/api/br';
    }
    
    async getEstatisticasClube(clubeId) {
        const response = await fetch(`${this.API_BASE}/clube/${clubeId}/stats`);
        const data = await response.json();
        return data.success ? data.data : {};
    }
}
```

## 🌍 **PRÓXIMOS PASSOS**

1. **Teste com frontend** 
2. **Deploy em produção** (Heroku/Vercel)
3. **API internacional** (API-Football)
4. **Cache Redis** para produção
5. **Autenticação** se necessário

---

**🎮 PRONTO PARA USAR! A API ESTÁ SERVINDO DADOS REAIS DO CARTOLA FC! 🔥**
