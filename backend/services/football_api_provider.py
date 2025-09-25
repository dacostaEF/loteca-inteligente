import os
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Configurações API-Football
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")  # Chave da API-Football
TIMEOUT = 15
_CACHE = {}

# IDs das principais ligas
LEAGUES_CONFIG = {
    "premier_league": {"id": 39, "name": "Premier League", "country": "England"},
    "la_liga": {"id": 140, "name": "La Liga", "country": "Spain"},  
    "serie_a": {"id": 135, "name": "Serie A", "country": "Italy"},
    "bundesliga": {"id": 78, "name": "Bundesliga", "country": "Germany"},
    "ligue_1": {"id": 61, "name": "Ligue 1", "country": "France"},
    "champions": {"id": 2, "name": "Champions League", "country": "World"},
    "europa": {"id": 3, "name": "Europa League", "country": "World"}
}

def _get_football_api(endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Função interna para fazer requisições à API-Football com cache
    """
    # Cache key baseado no endpoint e parâmetros
    cache_key = (endpoint, tuple(sorted((params or {}).items())))
    cached = _CACHE.get(cache_key)
    
    # Verificar cache (TTL baseado no tipo de dados)
    ttl = get_cache_ttl(endpoint)
    if cached and cached[0] > time.time():
        return cached[1]
    
    # Se não tiver API key, usar dados mock
    if not API_FOOTBALL_KEY:
        print(f"[Football-API] ⚠️ SEM API KEY - Usando dados MOCK para {endpoint}")
        print(f"[Football-API] 🔧 Para dados reais, configure API_FOOTBALL_KEY no Railway")
        mock_data = get_mock_data(endpoint, params)
        # Adicionar flag indicando que são dados mock
        mock_data["_data_source"] = "mock"
        mock_data["_warning"] = "Dados simulados - Configure API_FOOTBALL_KEY para dados reais"
        return mock_data
    
    # Fazer requisição real
    try:
        url = f"{API_FOOTBALL_BASE}{endpoint}"
        headers = {
            "X-RapidAPI-Key": API_FOOTBALL_KEY,
            "X-RapidAPI-Host": "v3.football.api-sports.io"
        }
        
        print(f"[Football-API] GET {url} - Params: {params}")
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        # Adicionar flag indicando dados reais
        data["_data_source"] = "api_football_real"
        data["_timestamp"] = datetime.now().isoformat()
        
        # Armazenar no cache
        _CACHE[cache_key] = (time.time() + ttl, data)
        
        print(f"[Football-API] ✅ DADOS REAIS: {len(data.get('response', []))} itens")
        return data
        
    except Exception as e:
        print(f"[Football-API] ❌ Erro: {e}")
        
        # Usar cache expirado se disponível
        if cached:
            print("[Football-API] 📦 Usando cache expirado")
            return cached[1]
            
        # Fallback para mock data
        print("[Football-API] 🎭 Fallback para dados mock")
        return get_mock_data(endpoint, params)

def get_cache_ttl(endpoint: str) -> int:
    """
    Definir TTL do cache baseado no tipo de dados
    """
    if "fixtures" in endpoint:
        return 30 * 60  # 30 minutos para fixtures
    elif "odds" in endpoint:
        return 10 * 60  # 10 minutos para odds
    elif "teams" in endpoint or "leagues" in endpoint:
        return 24 * 60 * 60  # 24 horas para dados estáticos
    else:
        return 60 * 60  # 1 hora padrão

def get_mock_data(endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Gerar dados mock baseados no endpoint
    """
    if "fixtures" in endpoint:
        return generate_mock_fixtures()
    elif "odds" in endpoint:
        return generate_mock_odds()
    elif "teams" in endpoint:
        return generate_mock_teams()
    elif "leagues" in endpoint:
        return generate_mock_leagues()
    else:
        return {"response": [], "results": 0}

def generate_mock_fixtures() -> Dict[str, Any]:
    """Mock data para fixtures"""
    tomorrow = datetime.now() + timedelta(days=1)
    
    return {
        "response": [
            {
                "fixture": {
                    "id": 1001,
                    "date": tomorrow.isoformat(),
                    "status": {"short": "NS"},
                    "venue": {"name": "Old Trafford", "city": "Manchester"}
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "round": "Regular Season - 10"
                },
                "teams": {
                    "home": {"id": 33, "name": "Manchester United", "logo": ""},
                    "away": {"id": 34, "name": "Newcastle", "logo": ""}
                },
                "goals": {"home": None, "away": None}
            },
            {
                "fixture": {
                    "id": 1002,
                    "date": tomorrow.isoformat(),
                    "status": {"short": "NS"},
                    "venue": {"name": "Anfield", "city": "Liverpool"}
                },
                "league": {
                    "id": 39,
                    "name": "Premier League", 
                    "country": "England",
                    "round": "Regular Season - 10"
                },
                "teams": {
                    "home": {"id": 40, "name": "Liverpool", "logo": ""},
                    "away": {"id": 50, "name": "Manchester City", "logo": ""}
                },
                "goals": {"home": None, "away": None}
            }
        ],
        "results": 2
    }

def generate_mock_odds() -> Dict[str, Any]:
    """Mock data para odds"""
    return {
        "response": [
            {
                "fixture": {"id": 1001},
                "bookmakers": [
                    {
                        "name": "Bet365",
                        "bets": [
                            {
                                "name": "Match Winner",
                                "values": [
                                    {"value": "Home", "odd": "2.10"},
                                    {"value": "Draw", "odd": "3.20"},
                                    {"value": "Away", "odd": "3.50"}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "fixture": {"id": 1002},
                "bookmakers": [
                    {
                        "name": "Bet365",
                        "bets": [
                            {
                                "name": "Match Winner",
                                "values": [
                                    {"value": "Home", "odd": "1.85"},
                                    {"value": "Draw", "odd": "3.40"},
                                    {"value": "Away", "odd": "4.20"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "results": 2
    }

def generate_mock_teams() -> Dict[str, Any]:
    """Mock data para teams"""
    return {
        "response": [
            {"team": {"id": 33, "name": "Manchester United", "country": "England"}},
            {"team": {"id": 34, "name": "Newcastle", "country": "England"}},
            {"team": {"id": 40, "name": "Liverpool", "country": "England"}},
            {"team": {"id": 50, "name": "Manchester City", "country": "England"}}
        ],
        "results": 4
    }

def generate_mock_leagues() -> Dict[str, Any]:
    """Mock data para leagues"""
    return {
        "response": [
            {
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "",
                    "flag": ""
                }
            }
        ],
        "results": 1
    }

# FUNÇÕES PRINCIPAIS DA API

def get_leagues() -> List[Dict[str, Any]]:
    """
    Buscar ligas disponíveis
    """
    try:
        data = _get_football_api("/leagues")
        return data.get("response", [])
    except Exception as e:
        print(f"[Football-API] Erro ao buscar ligas: {e}")
        return []

def get_fixtures_by_league(league_id: int, days_ahead: int = 7) -> List[Dict[str, Any]]:
    """
    Buscar fixtures de uma liga específica
    """
    try:
        # Buscar jogos dos próximos X dias
        from_date = datetime.now().strftime("%Y-%m-%d")
        to_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        params = {
            "league": league_id,
            "from": from_date,
            "to": to_date
        }
        
        data = _get_football_api("/fixtures", params)
        return data.get("response", [])
    except Exception as e:
        print(f"[Football-API] Erro ao buscar fixtures: {e}")
        return []

def get_odds_by_fixture(fixture_id: int) -> Dict[str, Any]:
    """
    Buscar odds de um fixture específico
    """
    try:
        params = {"fixture": fixture_id}
        data = _get_football_api("/odds", params)
        
        response = data.get("response", [])
        if response:
            return response[0]  # Primeiro bookmaker
        return {}
    except Exception as e:
        print(f"[Football-API] Erro ao buscar odds: {e}")
        return {}

def calculate_probabilities_from_odds(odds_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcular probabilidades reais a partir das odds (removendo overround)
    """
    try:
        bookmakers = odds_data.get("bookmakers", [])
        if not bookmakers:
            return {"home": 0.33, "draw": 0.33, "away": 0.34}  # Default equal
        
        # Pegar primeira casa de apostas e primeira aposta (Match Winner)
        bet = bookmakers[0].get("bets", [])
        if not bet:
            return {"home": 0.33, "draw": 0.33, "away": 0.34}
        
        values = bet[0].get("values", [])
        if len(values) < 3:
            return {"home": 0.33, "draw": 0.33, "away": 0.34}
        
        # Extrair odds
        home_odd = float(values[0]["odd"])
        draw_odd = float(values[1]["odd"])
        away_odd = float(values[2]["odd"])
        
        # Converter para probabilidades implícitas
        home_prob = 1 / home_odd
        draw_prob = 1 / draw_odd
        away_prob = 1 / away_odd
        
        # Remover overround (normalizar para 100%)
        total = home_prob + draw_prob + away_prob
        
        return {
            "home": round(home_prob / total, 3),
            "draw": round(draw_prob / total, 3),
            "away": round(away_prob / total, 3)
        }
        
    except Exception as e:
        print(f"[Football-API] Erro ao calcular probabilidades: {e}")
        return {"home": 0.33, "draw": 0.33, "away": 0.34}

def get_fixture_with_analysis(fixture_id: int) -> Dict[str, Any]:
    """
    Buscar fixture completo com odds e análise
    """
    try:
        # Buscar dados básicos do fixture (mock por enquanto)
        fixtures = get_fixtures_by_league(39)  # Premier League
        fixture = next((f for f in fixtures if f["fixture"]["id"] == fixture_id), None)
        
        if not fixture:
            return {}
        
        # Buscar odds
        odds = get_odds_by_fixture(fixture_id)
        
        # Calcular probabilidades
        probabilities = calculate_probabilities_from_odds(odds)
        
        return {
            "fixture": fixture,
            "odds": odds,
            "probabilities": probabilities,
            "analysis": generate_fixture_analysis(fixture, probabilities)
        }
        
    except Exception as e:
        print(f"[Football-API] Erro na análise completa: {e}")
        return {}

def generate_fixture_analysis(fixture: Dict[str, Any], probabilities: Dict[str, float]) -> Dict[str, Any]:
    """
    Gerar análise do fixture baseada nas probabilidades
    """
    home_prob = probabilities.get("home", 0)
    draw_prob = probabilities.get("draw", 0)
    away_prob = probabilities.get("away", 0)
    
    # Determinar favorito
    max_prob = max(home_prob, draw_prob, away_prob)
    
    if max_prob == home_prob:
        favorite = "home"
        confidence = home_prob
    elif max_prob == away_prob:
        favorite = "away"
        confidence = away_prob
    else:
        favorite = "draw"
        confidence = draw_prob
    
    # Determinar recomendação baseada no equilíbrio
    if max_prob > 0.6:
        recommendation = "seco"
        risk_level = "baixo"
    elif max_prob > 0.45:
        recommendation = "duplo"
        risk_level = "medio"
    else:
        recommendation = "triplo"
        risk_level = "alto"
    
    return {
        "favorite": favorite,
        "confidence": round(confidence, 3),
        "recommendation": recommendation,
        "risk_level": risk_level,
        "balance_score": round(1 - max_prob, 3)  # Quanto mais equilibrado, maior o score
    }

# Função utilitária para limpar cache
def clear_cache():
    """Limpar cache de requisições"""
    global _CACHE
    _CACHE = {}
    print("[Football-API] Cache limpo")

# Health check da API
def health_check() -> Dict[str, Any]:
    """
    Verificar status da API
    """
    try:
        # Testar com uma requisição simples
        data = _get_football_api("/leagues", {"id": 39})
        
        return {
            "status": "ok",
            "api_key_configured": bool(API_FOOTBALL_KEY),
            "using_mock": not bool(API_FOOTBALL_KEY),
            "cache_size": len(_CACHE),
            "available_leagues": len(LEAGUES_CONFIG)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "api_key_configured": bool(API_FOOTBALL_KEY),
            "using_mock": True,
            "cache_size": len(_CACHE)
        }
