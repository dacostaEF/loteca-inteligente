from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from services.football_api_provider import (
    get_leagues, get_fixtures_by_league, get_odds_by_fixture,
    get_fixture_with_analysis, calculate_probabilities_from_odds,
    health_check as football_health_check, LEAGUES_CONFIG
)

# Blueprint para rotas internacionais
bp_int = Blueprint("internacional", __name__, url_prefix="/api/int")

@bp_int.route("/health", methods=["GET"])
@cross_origin()
def api_health():
    """
    Health check da API internacional
    GET /api/int/health
    """
    try:
        health = football_health_check()
        return jsonify({
            "success": True,
            "data": health
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

@bp_int.route("/leagues", methods=["GET"])
@cross_origin()
def api_leagues():
    """
    Listar ligas disponíveis
    GET /api/int/leagues
    """
    try:
        # Retornar configuração das ligas principais
        leagues_list = []
        for key, config in LEAGUES_CONFIG.items():
            leagues_list.append({
                "key": key,
                "id": config["id"],
                "name": config["name"],
                "country": config["country"]
            })
        
        return jsonify({
            "success": True,
            "total": len(leagues_list),
            "leagues": leagues_list
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "leagues": []
        }), 200

@bp_int.route("/league/<league_key>/fixtures", methods=["GET"])
@cross_origin()
def api_league_fixtures(league_key):
    """
    Buscar fixtures de uma liga específica
    GET /api/int/league/{league_key}/fixtures?days=7
    """
    try:
        # Verificar se a liga existe
        if league_key not in LEAGUES_CONFIG:
            return jsonify({
                "success": False,
                "error": f"Liga '{league_key}' não encontrada",
                "available_leagues": list(LEAGUES_CONFIG.keys())
            }), 404
        
        league_id = LEAGUES_CONFIG[league_key]["id"]
        days_ahead = request.args.get('days', 7, type=int)
        
        # Buscar fixtures
        fixtures = get_fixtures_by_league(league_id, days_ahead)
        
        return jsonify({
            "success": True,
            "league": LEAGUES_CONFIG[league_key],
            "total": len(fixtures),
            "fixtures": fixtures
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "fixtures": []
        }), 200

@bp_int.route("/fixture/<int:fixture_id>/odds", methods=["GET"])
@cross_origin()
def api_fixture_odds(fixture_id):
    """
    Buscar odds de um fixture específico
    GET /api/int/fixture/{fixture_id}/odds
    """
    try:
        odds = get_odds_by_fixture(fixture_id)
        
        if not odds:
            return jsonify({
                "success": False,
                "error": "Odds não encontradas",
                "fixture_id": fixture_id
            }), 404
        
        # Calcular probabilidades
        probabilities = calculate_probabilities_from_odds(odds)
        
        return jsonify({
            "success": True,
            "fixture_id": fixture_id,
            "odds": odds,
            "probabilities": probabilities
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "fixture_id": fixture_id
        }), 200

@bp_int.route("/fixture/<int:fixture_id>/analysis", methods=["GET"])
@cross_origin()
def api_fixture_analysis(fixture_id):
    """
    Análise completa de um fixture (dados + odds + recomendação)
    GET /api/int/fixture/{fixture_id}/analysis
    """
    try:
        analysis = get_fixture_with_analysis(fixture_id)
        
        if not analysis:
            return jsonify({
                "success": False,
                "error": "Fixture não encontrado",
                "fixture_id": fixture_id
            }), 404
        
        return jsonify({
            "success": True,
            "fixture_id": fixture_id,
            "data": analysis
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "fixture_id": fixture_id
        }), 200

@bp_int.route("/fixtures/upcoming", methods=["GET"])
@cross_origin()
def api_upcoming_fixtures():
    """
    Buscar próximos fixtures de todas as ligas principais
    GET /api/int/fixtures/upcoming?days=3
    """
    try:
        days_ahead = request.args.get('days', 3, type=int)
        all_fixtures = []
        
        # Buscar fixtures das principais ligas
        main_leagues = ["premier_league", "champions", "la_liga"]
        
        for league_key in main_leagues:
            try:
                league_id = LEAGUES_CONFIG[league_key]["id"]
                fixtures = get_fixtures_by_league(league_id, days_ahead)
                
                # Adicionar info da liga em cada fixture
                for fixture in fixtures:
                    fixture["league_key"] = league_key
                    fixture["league_config"] = LEAGUES_CONFIG[league_key]
                
                all_fixtures.extend(fixtures)
                
            except Exception as e:
                print(f"[Internacional] Erro ao buscar {league_key}: {e}")
                continue
        
        # Ordenar por data
        all_fixtures.sort(key=lambda x: x["fixture"]["date"])
        
        return jsonify({
            "success": True,
            "total": len(all_fixtures),
            "leagues_searched": main_leagues,
            "fixtures": all_fixtures
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "fixtures": []
        }), 200

@bp_int.route("/recommendations/daily", methods=["GET"])
@cross_origin()
def api_daily_recommendations():
    """
    Recomendações diárias baseadas em análise de fixtures
    GET /api/int/recommendations/daily
    """
    try:
        # Buscar fixtures dos próximos 2 dias
        days_ahead = request.args.get('days', 2, type=int)
        
        recommendations = {
            "secos": [],      # Alta confiança
            "duplos": [],     # Média confiança  
            "triplos": [],    # Baixa confiança/equilibrados
            "summary": {
                "total_games": 0,
                "high_confidence": 0,
                "medium_confidence": 0,
                "low_confidence": 0
            }
        }
        
        # Analisar fixtures das principais ligas
        for league_key in ["premier_league", "champions", "la_liga"]:
            try:
                league_id = LEAGUES_CONFIG[league_key]["id"]
                fixtures = get_fixtures_by_league(league_id, days_ahead)
                
                for fixture in fixtures:
                    fixture_id = fixture["fixture"]["id"]
                    analysis = get_fixture_with_analysis(fixture_id)
                    
                    if analysis and "analysis" in analysis:
                        game_analysis = analysis["analysis"]
                        recommendation = game_analysis.get("recommendation", "triplo")
                        
                        game_info = {
                            "fixture_id": fixture_id,
                            "league": league_key,
                            "teams": fixture["teams"],
                            "date": fixture["fixture"]["date"],
                            "probabilities": analysis.get("probabilities", {}),
                            "confidence": game_analysis.get("confidence", 0),
                            "risk_level": game_analysis.get("risk_level", "alto")
                        }
                        
                        recommendations[f"{recommendation}s"].append(game_info)
                        recommendations["summary"]["total_games"] += 1
                        
                        if recommendation == "seco":
                            recommendations["summary"]["high_confidence"] += 1
                        elif recommendation == "duplo":
                            recommendations["summary"]["medium_confidence"] += 1
                        else:
                            recommendations["summary"]["low_confidence"] += 1
                
            except Exception as e:
                print(f"[Internacional] Erro ao analisar {league_key}: {e}")
                continue
        
        return jsonify({
            "success": True,
            "date": "today",
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "recommendations": {}
        }), 200

# Função para registrar o blueprint
def register_routes(app):
    """Registrar rotas internacionais na aplicação Flask"""
    app.register_blueprint(bp_int)
