from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from services.cartola_provider import clubes, estatisticas_clube, mercado_status, health_check, get_clube_mappings, get_clube_id_by_name

# Blueprint para rotas do Brasileirão
bp_br = Blueprint("br", __name__, url_prefix="/api/br")

@bp_br.route("/clubes", methods=["GET"])
@cross_origin()
def api_clubes():
    """
    Endpoint para listar todos os clubes do Cartola FC
    GET /api/br/clubes
    """
    try:
        data = clubes()
        # Normalizar saída em lista
        out = [
            {
                "id": cid, 
                "nome": v.get("nome", ""), 
                "abreviacao": v.get("abreviacao", ""),
                "escudo": v.get("url_escudo_png", "")
            } 
            for cid, v in data.items()
        ]
        return jsonify({
            "success": True,
            "total": len(out),
            "clubes": out
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "clubes": []
        }), 200

@bp_br.route("/clube/<int:clube_id>/stats", methods=["GET"])
@cross_origin()
def api_clube_stats(clube_id):
    """
    Endpoint para estatísticas de um clube específico
    GET /api/br/clube/{clube_id}/stats
    """
    try:
        stats = estatisticas_clube(clube_id)
        return jsonify({
            "success": True,
            "clube_id": clube_id,
            "data": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "clube_id": clube_id,
            "error": str(e),
            "data": {}
        }), 200

@bp_br.route("/confronto/<string:time_casa>/<string:time_fora>", methods=["GET"])
@cross_origin()
def api_confronto_stats(time_casa, time_fora):
    """
    Endpoint para comparar dois times
    GET /api/br/confronto/{time_casa}/{time_fora}
    """
    try:
        # Buscar IDs dos times
        id_casa = get_clube_id_by_name(time_casa)
        id_fora = get_clube_id_by_name(time_fora)
        
        if not id_casa or not id_fora:
            return jsonify({
                "success": False,
                "error": f"Time(s) não encontrado(s): {time_casa if not id_casa else ''} {time_fora if not id_fora else ''}",
                "times_mapeados": get_clube_mappings()
            }), 404
        
        # Buscar estatísticas
        stats_casa = estatisticas_clube(id_casa)
        stats_fora = estatisticas_clube(id_fora)
        
        # Análise comparativa
        analise = {
            "favorito": None,
            "equilibrio": False,
            "diferenca_rating": 0
        }
        
        if stats_casa.get("rating", 0) > stats_fora.get("rating", 0):
            analise["favorito"] = time_casa
            analise["diferenca_rating"] = round(stats_casa.get("rating", 0) - stats_fora.get("rating", 0), 3)
        elif stats_fora.get("rating", 0) > stats_casa.get("rating", 0):
            analise["favorito"] = time_fora
            analise["diferenca_rating"] = round(stats_fora.get("rating", 0) - stats_casa.get("rating", 0), 3)
        else:
            analise["equilibrio"] = True
        
        # Considerar equilibrado se diferença < 0.1
        if analise["diferenca_rating"] < 0.1:
            analise["equilibrio"] = True
            analise["favorito"] = None
        
        return jsonify({
            "success": True,
            "confronto": f"{time_casa} vs {time_fora}",
            "casa": {
                "nome": time_casa,
                "id": id_casa,
                "stats": stats_casa
            },
            "fora": {
                "nome": time_fora,
                "id": id_fora,
                "stats": stats_fora
            },
            "analise": analise
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "confronto": f"{time_casa} vs {time_fora}"
        }), 200

@bp_br.route("/mercado/status", methods=["GET"])
@cross_origin()
def api_mercado_status():
    """
    Endpoint para status do mercado do Cartola FC
    GET /api/br/mercado/status
    """
    try:
        status = mercado_status()
        return jsonify({
            "success": True,
            "data": status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "data": {}
        }), 200

@bp_br.route("/health", methods=["GET"])
@cross_origin()
def api_health():
    """
    Endpoint para verificar saúde da API
    GET /api/br/health
    """
    try:
        health = health_check()
        return jsonify(health)
    except Exception as e:
        return jsonify({
            "status": "error",
            "api_response": False,
            "error": str(e)
        }), 200

@bp_br.route("/mappings", methods=["GET"])
@cross_origin()
def api_mappings():
    """
    Endpoint para listar mapeamento de nomes para IDs
    GET /api/br/mappings
    """
    try:
        mappings = get_clube_mappings()
        return jsonify({
            "success": True,
            "total": len(mappings),
            "mappings": mappings
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "mappings": {}
        }), 200

# Função para registrar o blueprint (será chamada em app.py)
def register_routes(app):
    """Registrar rotas do Brasileirão na aplicação Flask"""
    app.register_blueprint(bp_br)
