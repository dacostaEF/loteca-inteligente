from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import logging
from datetime import datetime

# Blueprint para rotas das ligas internacionais
bp_int = Blueprint("int", __name__, url_prefix="/api/int")

# Configuração de logging
logger = logging.getLogger(__name__)

# DADOS SIMULADOS PARA LIGAS INTERNACIONAIS

def get_premier_league_data():
    """Dados simulados da Premier League"""
    return [
        {"pos": 1, "time": "Manchester City", "p": 28, "j": 12, "v": 9, "e": 1, "d": 2, "gp": 32, "gc": 12, "sg": 20, "aproveitamento": 78, "ultimos": "VVVEV", "zona": "champions"},
        {"pos": 2, "time": "Arsenal", "p": 27, "j": 12, "v": 8, "e": 3, "d": 1, "gp": 26, "gc": 10, "sg": 16, "aproveitamento": 75, "ultimos": "VVVVE", "zona": "champions"},
        {"pos": 3, "time": "Liverpool", "p": 25, "j": 12, "v": 7, "e": 4, "d": 1, "gp": 28, "gc": 11, "sg": 17, "aproveitamento": 69, "ultimos": "VVEVV", "zona": "champions"},
        {"pos": 4, "time": "Tottenham", "p": 23, "j": 12, "v": 7, "e": 2, "d": 3, "gp": 25, "gc": 17, "sg": 8, "aproveitamento": 64, "ultimos": "VVEDV", "zona": "champions"},
        {"pos": 5, "time": "Aston Villa", "p": 22, "j": 12, "v": 6, "e": 4, "d": 2, "gp": 24, "gc": 16, "sg": 8, "aproveitamento": 61, "ultimos": "VEVVV", "zona": "europa"},
        {"pos": 6, "time": "Newcastle", "p": 20, "j": 12, "v": 6, "e": 2, "d": 4, "gp": 22, "gc": 18, "sg": 4, "aproveitamento": 56, "ultimos": "VVEDD", "zona": "europa"},
        {"pos": 7, "time": "Manchester United", "p": 19, "j": 12, "v": 6, "e": 1, "d": 5, "gp": 18, "gc": 20, "sg": -2, "aproveitamento": 53, "ultimos": "VEDVV", "zona": "europa"},
        {"pos": 8, "time": "Brighton", "p": 18, "j": 12, "v": 5, "e": 3, "d": 4, "gp": 20, "gc": 19, "sg": 1, "aproveitamento": 50, "ultimos": "EDVVE", "zona": ""},
        {"pos": 9, "time": "West Ham", "p": 17, "j": 12, "v": 5, "e": 2, "d": 5, "gp": 19, "gc": 21, "sg": -2, "aproveitamento": 47, "ultimos": "VEDED", "zona": ""},
        {"pos": 10, "time": "Chelsea", "p": 16, "j": 12, "v": 4, "e": 4, "d": 4, "gp": 16, "gc": 15, "sg": 1, "aproveitamento": 44, "ultimos": "EEVVD", "zona": ""},
        {"pos": 11, "time": "Wolves", "p": 15, "j": 12, "v": 4, "e": 3, "d": 5, "gp": 17, "gc": 20, "sg": -3, "aproveitamento": 42, "ultimos": "DVEED", "zona": ""},
        {"pos": 12, "time": "Brentford", "p": 14, "j": 12, "v": 4, "e": 2, "d": 6, "gp": 18, "gc": 22, "sg": -4, "aproveitamento": 39, "ultimos": "EDDVE", "zona": ""},
        {"pos": 13, "time": "Crystal Palace", "p": 13, "j": 12, "v": 3, "e": 4, "d": 5, "gp": 14, "gc": 18, "sg": -4, "aproveitamento": 36, "ultimos": "EDEVD", "zona": ""},
        {"pos": 14, "time": "Fulham", "p": 12, "j": 12, "v": 3, "e": 3, "d": 6, "gp": 15, "gc": 21, "sg": -6, "aproveitamento": 33, "ultimos": "DEDVE", "zona": ""},
        {"pos": 15, "time": "Everton", "p": 11, "j": 12, "v": 3, "e": 2, "d": 7, "gp": 12, "gc": 20, "sg": -8, "aproveitamento": 31, "ultimos": "DDVED", "zona": ""},
        {"pos": 16, "time": "Nottingham Forest", "p": 10, "j": 12, "v": 2, "e": 4, "d": 6, "gp": 13, "gc": 19, "sg": -6, "aproveitamento": 28, "ultimos": "EDDED", "zona": ""},
        {"pos": 17, "time": "Luton Town", "p": 8, "j": 12, "v": 2, "e": 2, "d": 8, "gp": 10, "gc": 24, "sg": -14, "aproveitamento": 22, "ultimos": "DDDED", "zona": "rebaixamento"},
        {"pos": 18, "time": "Sheffield United", "p": 6, "j": 12, "v": 1, "e": 3, "d": 8, "gp": 8, "gc": 25, "sg": -17, "aproveitamento": 17, "ultimos": "DDDDE", "zona": "rebaixamento"},
        {"pos": 19, "time": "Burnley", "p": 5, "j": 12, "v": 1, "e": 2, "d": 9, "gp": 9, "gc": 26, "sg": -17, "aproveitamento": 14, "ultimos": "DDDDD", "zona": "rebaixamento"},
        {"pos": 20, "time": "Bournemouth", "p": 4, "j": 12, "v": 1, "e": 1, "d": 10, "gp": 7, "gc": 28, "sg": -21, "aproveitamento": 11, "ultimos": "DDDDD", "zona": "rebaixamento"}
    ]

def get_la_liga_data():
    """Dados simulados da La Liga"""
    return [
        {"pos": 1, "time": "Real Madrid", "p": 32, "j": 13, "v": 10, "e": 2, "d": 1, "gp": 28, "gc": 8, "sg": 20, "aproveitamento": 82, "ultimos": "VVVVV", "zona": "champions"},
        {"pos": 2, "time": "Barcelona", "p": 28, "j": 13, "v": 8, "e": 4, "d": 1, "gp": 26, "gc": 12, "sg": 14, "aproveitamento": 72, "ultimos": "VVVEV", "zona": "champions"},
        {"pos": 3, "time": "Atlético Madrid", "p": 26, "j": 13, "v": 8, "e": 2, "d": 3, "gp": 24, "gc": 14, "sg": 10, "aproveitamento": 67, "ultimos": "VVEDV", "zona": "champions"},
        {"pos": 4, "time": "Girona", "p": 25, "j": 13, "v": 7, "e": 4, "d": 2, "gp": 22, "gc": 15, "sg": 7, "aproveitamento": 64, "ultimos": "VEVVV", "zona": "champions"},
        {"pos": 5, "time": "Real Sociedad", "p": 23, "j": 13, "v": 7, "e": 2, "d": 4, "gp": 20, "gc": 16, "sg": 4, "aproveitamento": 59, "ultimos": "VVEDD", "zona": "europa"},
        {"pos": 6, "time": "Athletic Bilbao", "p": 21, "j": 13, "v": 6, "e": 3, "d": 4, "gp": 19, "gc": 17, "sg": 2, "aproveitamento": 54, "ultimos": "VEDVV", "zona": "europa"},
        {"pos": 7, "time": "Real Betis", "p": 20, "j": 13, "v": 6, "e": 2, "d": 5, "gp": 18, "gc": 19, "sg": -1, "aproveitamento": 51, "ultimos": "EDVVE", "zona": "europa"},
        {"pos": 8, "time": "Valencia", "p": 19, "j": 13, "v": 5, "e": 4, "d": 4, "gp": 17, "gc": 18, "sg": -1, "aproveitamento": 49, "ultimos": "VEDED", "zona": ""},
        {"pos": 9, "time": "Villarreal", "p": 18, "j": 13, "v": 5, "e": 3, "d": 5, "gp": 16, "gc": 20, "sg": -4, "aproveitamento": 46, "ultimos": "EEVVD", "zona": ""},
        {"pos": 10, "time": "Getafe", "p": 17, "j": 13, "v": 5, "e": 2, "d": 6, "gp": 15, "gc": 21, "sg": -6, "aproveitamento": 44, "ultimos": "DVEED", "zona": ""},
        {"pos": 11, "time": "Osasuna", "p": 16, "j": 13, "v": 4, "e": 4, "d": 5, "gp": 14, "gc": 19, "sg": -5, "aproveitamento": 41, "ultimos": "EDDVE", "zona": ""},
        {"pos": 12, "time": "Sevilla", "p": 15, "j": 13, "v": 4, "e": 3, "d": 6, "gp": 16, "gc": 22, "sg": -6, "aproveitamento": 38, "ultimos": "EDEVD", "zona": ""},
        {"pos": 13, "time": "Las Palmas", "p": 14, "j": 13, "v": 4, "e": 2, "d": 7, "gp": 13, "gc": 20, "sg": -7, "aproveitamento": 36, "ultimos": "DEDVE", "zona": ""},
        {"pos": 14, "time": "Celta Vigo", "p": 13, "j": 13, "v": 3, "e": 4, "d": 6, "gp": 12, "gc": 19, "sg": -7, "aproveitamento": 33, "ultimos": "DDVED", "zona": ""},
        {"pos": 15, "time": "Mallorca", "p": 12, "j": 13, "v": 3, "e": 3, "d": 7, "gp": 11, "gc": 21, "sg": -10, "aproveitamento": 31, "ultimos": "EDDED", "zona": ""},
        {"pos": 16, "time": "Rayo Vallecano", "p": 11, "j": 13, "v": 2, "e": 5, "d": 6, "gp": 10, "gc": 18, "sg": -8, "aproveitamento": 28, "ultimos": "DDDDE", "zona": ""},
        {"pos": 17, "time": "Cádiz", "p": 10, "j": 13, "v": 2, "e": 4, "d": 7, "gp": 9, "gc": 22, "sg": -13, "aproveitamento": 26, "ultimos": "DDDDD", "zona": "rebaixamento"},
        {"pos": 18, "time": "Almería", "p": 8, "j": 13, "v": 1, "e": 5, "d": 7, "gp": 8, "gc": 24, "sg": -16, "aproveitamento": 21, "ultimos": "DDDDD", "zona": "rebaixamento"},
        {"pos": 19, "time": "Granada", "p": 6, "j": 13, "v": 1, "e": 3, "d": 9, "gp": 7, "gc": 26, "sg": -19, "aproveitamento": 15, "ultimos": "DDDDD", "zona": "rebaixamento"},
        {"pos": 20, "time": "Alavés", "p": 5, "j": 13, "v": 1, "e": 2, "d": 10, "gp": 6, "gc": 28, "sg": -22, "aproveitamento": 13, "ultimos": "DDDDD", "zona": "rebaixamento"}
    ]

def get_ligue1_data():
    """Dados simulados da Ligue 1"""
    return [
        {"pos": 1, "time": "Paris Saint-Germain", "p": 30, "j": 12, "v": 9, "e": 3, "d": 0, "gp": 28, "gc": 8, "sg": 20, "aproveitamento": 83, "ultimos": "VVVVV", "zona": "champions"},
        {"pos": 2, "time": "Nice", "p": 26, "j": 12, "v": 8, "e": 2, "d": 2, "gp": 20, "gc": 10, "sg": 10, "aproveitamento": 72, "ultimos": "VVVEV", "zona": "champions"},
        {"pos": 3, "time": "Monaco", "p": 24, "j": 12, "v": 7, "e": 3, "d": 2, "gp": 22, "gc": 14, "sg": 8, "aproveitamento": 67, "ultimos": "VVEDV", "zona": "champions"},
        {"pos": 4, "time": "Lille", "p": 22, "j": 12, "v": 6, "e": 4, "d": 2, "gp": 19, "gc": 15, "sg": 4, "aproveitamento": 61, "ultimos": "VEVVV", "zona": "champions"},
        {"pos": 5, "time": "Lens", "p": 21, "j": 12, "v": 6, "e": 3, "d": 3, "gp": 18, "gc": 16, "sg": 2, "aproveitamento": 58, "ultimos": "VVEDD", "zona": "europa"},
        {"pos": 6, "time": "Marseille", "p": 20, "j": 12, "v": 6, "e": 2, "d": 4, "gp": 17, "gc": 18, "sg": -1, "aproveitamento": 56, "ultimos": "VEDVV", "zona": "europa"},
        {"pos": 7, "time": "Rennes", "p": 19, "j": 12, "v": 5, "e": 4, "d": 3, "gp": 16, "gc": 17, "sg": -1, "aproveitamento": 53, "ultimos": "EDVVE", "zona": "europa"},
        {"pos": 8, "time": "Reims", "p": 18, "j": 12, "v": 5, "e": 3, "d": 4, "gp": 15, "gc": 18, "sg": -3, "aproveitamento": 50, "ultimos": "VEDED", "zona": ""},
        {"pos": 9, "time": "Lyon", "p": 17, "j": 12, "v": 5, "e": 2, "d": 5, "gp": 14, "gc": 19, "sg": -5, "aproveitamento": 47, "ultimos": "EEVVD", "zona": ""},
        {"pos": 10, "time": "Montpellier", "p": 16, "j": 12, "v": 4, "e": 4, "d": 4, "gp": 13, "gc": 16, "sg": -3, "aproveitamento": 44, "ultimos": "DVEED", "zona": ""},
        {"pos": 11, "time": "Toulouse", "p": 15, "j": 12, "v": 4, "e": 3, "d": 5, "gp": 12, "gc": 17, "sg": -5, "aproveitamento": 42, "ultimos": "EDDVE", "zona": ""},
        {"pos": 12, "time": "Nantes", "p": 14, "j": 12, "v": 4, "e": 2, "d": 6, "gp": 11, "gc": 18, "sg": -7, "aproveitamento": 39, "ultimos": "EDEVD", "zona": ""},
        {"pos": 13, "time": "Brest", "p": 13, "j": 12, "v": 3, "e": 4, "d": 5, "gp": 10, "gc": 16, "sg": -6, "aproveitamento": 36, "ultimos": "DEDVE", "zona": ""},
        {"pos": 14, "time": "Strasbourg", "p": 12, "j": 12, "v": 3, "e": 3, "d": 6, "gp": 9, "gc": 18, "sg": -9, "aproveitamento": 33, "ultimos": "DDVED", "zona": ""},
        {"pos": 15, "time": "Lorient", "p": 11, "j": 12, "v": 3, "e": 2, "d": 7, "gp": 8, "gc": 20, "sg": -12, "aproveitamento": 31, "ultimos": "EDDED", "zona": ""},
        {"pos": 16, "time": "Metz", "p": 10, "j": 12, "v": 2, "e": 4, "d": 6, "gp": 7, "gc": 19, "sg": -12, "aproveitamento": 28, "ultimos": "DDDDE", "zona": ""},
        {"pos": 17, "time": "Le Havre", "p": 9, "j": 12, "v": 2, "e": 3, "d": 7, "gp": 6, "gc": 21, "sg": -15, "aproveitamento": 25, "ultimos": "DDDDD", "zona": "rebaixamento"},
        {"pos": 18, "time": "Clermont", "p": 7, "j": 12, "v": 1, "e": 4, "d": 7, "gp": 5, "gc": 22, "sg": -17, "aproveitamento": 19, "ultimos": "DDDDD", "zona": "rebaixamento"}
    ]

def get_champions_league_data():
    """Dados simulados da Champions League (Grupos)"""
    return [
        # GRUPO A
        {"pos": 1, "time": "Bayern Munich", "grupo": "A", "p": 12, "j": 4, "v": 4, "e": 0, "d": 0, "gp": 8, "gc": 2, "sg": 6, "aproveitamento": 100, "ultimos": "VVVV", "zona": "oitavas"},
        {"pos": 2, "time": "Manchester United", "grupo": "A", "p": 6, "j": 4, "v": 2, "e": 0, "d": 2, "gp": 5, "gc": 6, "sg": -1, "aproveitamento": 50, "ultimos": "VVDD", "zona": "oitavas"},
        {"pos": 3, "time": "Galatasaray", "grupo": "A", "p": 3, "j": 4, "v": 1, "e": 0, "d": 3, "gp": 3, "gc": 7, "sg": -4, "aproveitamento": 25, "ultimos": "DDVD", "zona": "europa"},
        {"pos": 4, "time": "Copenhagen", "grupo": "A", "p": 0, "j": 4, "v": 0, "e": 0, "d": 4, "gp": 1, "gc": 3, "sg": -2, "aproveitamento": 0, "ultimos": "DDDD", "zona": "eliminado"},
        
        # GRUPO B
        {"pos": 1, "time": "Arsenal", "grupo": "B", "p": 9, "j": 4, "v": 3, "e": 0, "d": 1, "gp": 7, "gc": 3, "sg": 4, "aproveitamento": 75, "ultimos": "VVVD", "zona": "oitavas"},
        {"pos": 2, "time": "PSV Eindhoven", "grupo": "B", "p": 6, "j": 4, "v": 2, "e": 0, "d": 2, "gp": 5, "gc": 5, "sg": 0, "aproveitamento": 50, "ultimos": "VDDV", "zona": "oitavas"},
        {"pos": 3, "time": "Lens", "grupo": "B", "p": 3, "j": 4, "v": 1, "e": 0, "d": 3, "gp": 3, "gc": 6, "sg": -3, "aproveitamento": 25, "ultimos": "DDVD", "zona": "europa"},
        {"pos": 4, "time": "Sevilla", "grupo": "B", "p": 0, "j": 4, "v": 0, "e": 0, "d": 4, "gp": 2, "gc": 3, "sg": -1, "aproveitamento": 0, "ultimos": "DDDD", "zona": "eliminado"},
        
        # GRUPO C
        {"pos": 1, "time": "Real Madrid", "grupo": "C", "p": 12, "j": 4, "v": 4, "e": 0, "d": 0, "gp": 9, "gc": 1, "sg": 8, "aproveitamento": 100, "ultimos": "VVVV", "zona": "oitavas"},
        {"pos": 2, "time": "Napoli", "grupo": "C", "p": 6, "j": 4, "v": 2, "e": 0, "d": 2, "gp": 4, "gc": 5, "sg": -1, "aproveitamento": 50, "ultimos": "VVDD", "zona": "oitavas"},
        {"pos": 3, "time": "Braga", "grupo": "C", "p": 3, "j": 4, "v": 1, "e": 0, "d": 3, "gp": 2, "gc": 6, "sg": -4, "aproveitamento": 25, "ultimos": "DDVD", "zona": "europa"},
        {"pos": 4, "time": "Union Berlin", "grupo": "C", "p": 0, "j": 4, "v": 0, "e": 0, "d": 4, "gp": 1, "gc": 4, "sg": -3, "aproveitamento": 0, "ultimos": "DDDD", "zona": "eliminado"},
        
        # GRUPO D
        {"pos": 1, "time": "Inter Milan", "grupo": "D", "p": 10, "j": 4, "v": 3, "e": 1, "d": 0, "gp": 6, "gc": 2, "sg": 4, "aproveitamento": 83, "ultimos": "VVVE", "zona": "oitavas"},
        {"pos": 2, "time": "Real Sociedad", "grupo": "D", "p": 7, "j": 4, "v": 2, "e": 1, "d": 1, "gp": 4, "gc": 3, "sg": 1, "aproveitamento": 58, "ultimos": "VVEV", "zona": "oitavas"},
        {"pos": 3, "time": "Salzburg", "grupo": "D", "p": 3, "j": 4, "v": 1, "e": 0, "d": 3, "gp": 3, "gc": 5, "sg": -2, "aproveitamento": 25, "ultimos": "DDVD", "zona": "europa"},
        {"pos": 4, "time": "Benfica", "grupo": "D", "p": 0, "j": 4, "v": 0, "e": 0, "d": 4, "gp": 1, "gc": 4, "sg": -3, "aproveitamento": 0, "ultimos": "DDDD", "zona": "eliminado"}
    ]

# ROTAS DA API

@bp_int.route("/health", methods=["GET"])
@cross_origin()
def health_check():
    """Health check para APIs internacionais"""
    return jsonify({
        "status": "online",
        "service": "International Leagues API",
        "timestamp": datetime.now().isoformat(),
        "leagues": ["premier-league", "la-liga", "ligue1", "champions-league"]
    })

@bp_int.route("/leagues", methods=["GET"])
@cross_origin()
def get_leagues():
    """Lista todas as ligas internacionais disponíveis"""
    return jsonify({
        "success": True,
        "leagues": [
            {
                "id": "premier-league",
                "name": "Premier League",
                "country": "England",
                "flag": "⚽",
                "teams": 20
            },
            {
                "id": "la-liga",
                "name": "La Liga",
                "country": "Spain", 
                "flag": "🇪🇸",
                "teams": 20
            },
            {
                "id": "ligue1",
                "name": "Ligue 1",
                "country": "France",
                "flag": "🇫🇷", 
                "teams": 18
            },
            {
                "id": "champions-league",
                "name": "Champions League",
                "country": "Europe",
                "flag": "🏆",
                "teams": 32
            }
        ]
    })

@bp_int.route("/classificacao/<league>", methods=["GET"])
@cross_origin()
def get_classificacao(league):
    """Endpoint para obter classificação de liga internacional específica"""
    try:
        logger.info(f"🌍 Buscando classificação: {league}")
        
        # Para Premier League, usar dados do CSV
        if league == "premier-league":
            from services.auto_classificacao import AutoClassificacao
            auto_class = AutoClassificacao()
            dados = auto_class.processar_premier_league_tradicional()
            
            if not dados:
                return jsonify({
                    "success": False,
                    "error": "Nenhum dado encontrado para Premier League"
                }), 404
            
            return jsonify({
                "success": True,
                "data": dados,
                "total": len(dados),
                "league": "Premier League",
                "last_updated": datetime.now().isoformat(),
                "source": "csv_tradicional"
            })
        
        # Para La Liga, usar dados do CSV
        if league == "la-liga":
            from services.auto_classificacao import AutoClassificacao
            auto_class = AutoClassificacao()
            dados = auto_class.processar_la_liga_tradicional()
            
            if not dados:
                return jsonify({
                    "success": False,
                    "error": "Nenhum dado encontrado para La Liga"
                }), 404
            
            return jsonify({
                "success": True,
                "data": dados,
                "total": len(dados),
                "league": "La Liga",
                "last_updated": datetime.now().isoformat(),
                "source": "csv_tradicional"
            })
        
        # Para Ligue 1, usar dados do CSV
        if league == "ligue1":
            from services.auto_classificacao import AutoClassificacao
            auto_class = AutoClassificacao()
            dados = auto_class.processar_ligue1_tradicional()
            
            if not dados:
                return jsonify({
                    "success": False,
                    "error": "Nenhum dado encontrado para Ligue 1"
                }), 404
            
            return jsonify({
                "success": True,
                "data": dados,
                "total": len(dados),
                "league": "Ligue 1",
                "last_updated": datetime.now().isoformat(),
                "source": "csv_tradicional"
            })
        
        # Para outras ligas, usar dados simulados (temporário)
        league_functions = {
            "champions-league": get_champions_league_data
        }
        
        if league not in league_functions:
            return jsonify({
                "success": False,
                "error": f"Liga '{league}' não encontrada",
                "available_leagues": ["premier-league", "la-liga", "ligue1", "champions-league"]
            }), 404
        
        # Obter dados da liga
        dados = league_functions[league]()
        
        # Mapear nomes das ligas
        league_names = {
            "la-liga": "La Liga", 
            "ligue1": "Ligue 1",
            "champions-league": "Champions League"
        }
        
        return jsonify({
            "success": True,
            "data": dados,
            "total": len(dados),
            "league": league_names[league],
            "last_updated": datetime.now().isoformat(),
            "source": "simulated_data"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar classificação {league}: {e}")
        return jsonify({
            "success": False,
            "error": f"Erro ao carregar classificação {league}: {str(e)}"
        }), 500

@bp_int.route("/fixtures/<league>", methods=["GET"])
@cross_origin()
def get_fixtures(league):
    """Endpoint para obter próximos jogos de uma liga"""
    try:
        # Por enquanto, retornar dados simulados
        fixtures = [
            {
                "home_team": "Manchester City",
                "away_team": "Arsenal", 
                "date": "2024-01-15",
                "time": "17:30",
                "venue": "Etihad Stadium"
            }
        ]
        
        return jsonify({
            "success": True,
            "fixtures": fixtures,
            "league": league,
            "total": len(fixtures)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao buscar fixtures {league}: {str(e)}"
        }), 500
