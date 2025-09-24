# 🎯 Loteca Inteligente - X-Ray Analytics

Sistema avançado de análises para Loteca com dados reais do Cartola FC e APIs internacionais.

## 🚀 Features

### ✅ Implementado:
- 🇧🇷 **Provider Cartola FC** com dados reais dos clubes brasileiros
- 🌍 **Estrutura internacional** (Premier League, La Liga, Champions)
- 📊 **Painel de clubes** com estatísticas em tempo real
- 🎯 **Sistema de recomendações** automáticas (seco/duplo/triplo)
- 🔧 **Diagnóstico completo** do sistema
- 📱 **Interface responsiva** otimizada para mobile

### 🎮 Como usar:
1. Acesse: `https://seu-dominio.railway.app/loteca`
2. Vá para **Aba 2 - Dados Avançados**
3. Veja o **Painel de Clubes** com dados reais
4. Console (F12): `testCartola.diagnosticar()`

## 🏗️ Arquitetura

### Backend (Flask):
- **API Brasileirão:** `/api/br/`
- **API Internacional:** `/api/int/`
- **Frontend:** `/loteca`

### Providers:
- **Cartola FC:** Dados reais dos clubes brasileiros
- **API-Football:** Estrutura para ligas internacionais (mock data)

## 🚀 Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### Via GitHub + Railway:
1. Fork este repositório
2. Conecte ao Railway
3. Deploy automático

## 🧪 Desenvolvimento Local

```bash
# 1. Clonar repo
git clone https://github.com/seu-usuario/loteca-inteligente.git
cd loteca-inteligente

# 2. Instalar dependências
cd backend
pip install -r requirements.txt

# 3. Executar
python app.py

# 4. Acessar
http://127.0.0.1:5000/loteca
```

## 📊 Dados Reais

### Cartola FC (Brasileirão):
- ✅ **Elencos:** Total de atletas, % prováveis
- ✅ **Força:** Média de pontuação dos jogadores
- ✅ **Mercado:** Preços em Cartoletas
- ✅ **Ratings:** Força calculada dos times

### Internacional (Preparado):
- 🌍 **Premier League, La Liga, Champions**
- 🎯 **Odds e probabilidades** calculadas
- 📈 **Recomendações automáticas**

## 🛠️ Stack

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **APIs:** Cartola FC, API-Football (preparado)
- **Deploy:** Railway
- **Cache:** Memory cache com TTL inteligente

## 📱 Mobile First

Interface otimizada para smartphones com:
- **Painel responsivo** de clubes
- **Cards compactos** para análises
- **Touch-friendly** controls

## 🔗 Links

- **Site Principal:** [Loterias Inteligente](https://loteriasinteligente.com.br)
- **Documentação:** Em desenvolvimento
- **Suporte:** Via GitHub Issues

---

**🎯 Desenvolvido para revolucionar as análises de Loteca com dados reais! 🚀**
