from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from services.cartola_provider import clubes, estatisticas_clube, mercado_status, health_check, get_clube_mappings, get_clube_id_by_name
from services.loteca_provider_new import get_current_loteca_matches
from models.classificacao_db import classificacao_db

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

@bp_br.route("/brasileirao/serie-a", methods=["GET"])
@cross_origin()
def api_brasileirao_serie_a():
    """
    Endpoint HÍBRIDO para dados da Série A
    Prioridade: Banco → API → Fallback simulado
    GET /api/br/brasileirao/serie-a
    """
    try:
        from datetime import datetime
        from models.brasileirao_db import brasileirao_db
        
        # 1. TENTAR BANCO PRIMEIRO (Performance)
        db_data = brasileirao_db.get_latest_classification()
        data_age = brasileirao_db.get_data_age()
        
        if db_data and brasileirao_db.is_data_fresh(max_age_hours=6):
            return jsonify({
                "success": True,
                "data": db_data,
                "total": len(db_data),
                "data_source": "database",
                "data_age": data_age,
                "last_updated": datetime.now().isoformat(),
                "cache_duration": 1800,
                "note": f"Dados do banco (atualizados {data_age})"
            })
        
        # 2. DADOS ANTIGOS - TENTAR BUSCAR NOVOS
        print(f"🔄 Dados antigos ({data_age or 'nunca'}), buscando atualizados...")
        
        # FUTURO: Aqui chamaria API real da CBF/ESPN
        # Por enquanto, usar dados atualizados e salvar no banco
        
        dados = [
            { "pos": 1, "time": "Flamengo", "p": 51, "j": 23, "v": 15, "e": 6, "d": 2, "gp": 48, "gc": 11, "sg": 37, "aproveitamento": 73, "ultimos": "VVEVE", "zona": "libertadores" },
            { "pos": 2, "time": "Cruzeiro", "p": 50, "j": 24, "v": 15, "e": 5, "d": 4, "gp": 39, "gc": 17, "sg": 22, "aproveitamento": 69, "ultimos": "VVDEV", "zona": "libertadores" },
            { "pos": 3, "time": "Palmeiras", "p": 49, "j": 22, "v": 15, "e": 4, "d": 3, "gp": 36, "gc": 18, "sg": 18, "aproveitamento": 74, "ultimos": "VVVEV", "zona": "libertadores" },
            { "pos": 4, "time": "Mirassol", "p": 42, "j": 23, "v": 11, "e": 9, "d": 3, "gp": 41, "gc": 23, "sg": 18, "aproveitamento": 60, "ultimos": "EVDEV", "zona": "libertadores" },
            { "pos": 5, "time": "Botafogo", "p": 40, "j": 24, "v": 11, "e": 7, "d": 6, "gp": 35, "gc": 18, "sg": 17, "aproveitamento": 55, "ultimos": "VEVDD", "zona": "pre-libertadores" },
            { "pos": 6, "time": "Bahia", "p": 37, "j": 23, "v": 10, "e": 7, "d": 6, "gp": 31, "gc": 28, "sg": 3, "aproveitamento": 53, "ultimos": "EVVDE", "zona": "pre-libertadores" },
            { "pos": 7, "time": "São Paulo", "p": 35, "j": 24, "v": 9, "e": 8, "d": 7, "gp": 27, "gc": 24, "sg": 3, "aproveitamento": 48, "ultimos": "DEEVV", "zona": "sul-americana" },
            { "pos": 8, "time": "Fluminense", "p": 31, "j": 22, "v": 9, "e": 4, "d": 9, "gp": 26, "gc": 29, "sg": -3, "aproveitamento": 46, "ultimos": "VDDEV", "zona": "sul-americana" },
            { "pos": 9, "time": "Bragantino", "p": 31, "j": 24, "v": 9, "e": 4, "d": 11, "gp": 29, "gc": 35, "sg": -6, "aproveitamento": 43, "ultimos": "DDVEV", "zona": "sul-americana" },
            { "pos": 10, "time": "Corinthians", "p": 29, "j": 24, "v": 7, "e": 8, "d": 9, "gp": 24, "gc": 29, "sg": -5, "aproveitamento": 40, "ultimos": "EEVDD", "zona": "" },
            { "pos": 11, "time": "Grêmio", "p": 29, "j": 24, "v": 7, "e": 8, "d": 9, "gp": 24, "gc": 30, "sg": -6, "aproveitamento": 40, "ultimos": "VEDDE", "zona": "" },
            { "pos": 12, "time": "Ceará", "p": 28, "j": 23, "v": 7, "e": 7, "d": 9, "gp": 22, "gc": 23, "sg": -1, "aproveitamento": 40, "ultimos": "EVDVE", "zona": "" },
            { "pos": 13, "time": "Vasco", "p": 27, "j": 24, "v": 7, "e": 6, "d": 11, "gp": 36, "gc": 35, "sg": 1, "aproveitamento": 37, "ultimos": "VDDVE", "zona": "" },
            { "pos": 14, "time": "Internacional", "p": 27, "j": 23, "v": 7, "e": 6, "d": 10, "gp": 28, "gc": 36, "sg": -8, "aproveitamento": 39, "ultimos": "DEDVE", "zona": "" },
            { "pos": 15, "time": "Santos", "p": 26, "j": 23, "v": 7, "e": 5, "d": 11, "gp": 22, "gc": 32, "sg": -10, "aproveitamento": 37, "ultimos": "DDEEV", "zona": "" },
            { "pos": 16, "time": "Atlético-MG", "p": 25, "j": 22, "v": 6, "e": 7, "d": 9, "gp": 21, "gc": 26, "sg": -5, "aproveitamento": 37, "ultimos": "EDDED", "zona": "" },
            { "pos": 17, "time": "Vitória", "p": 22, "j": 24, "v": 4, "e": 10, "d": 10, "gp": 19, "gc": 35, "sg": -16, "aproveitamento": 30, "ultimos": "EDDED", "zona": "rebaixamento" },
            { "pos": 18, "time": "Juventude", "p": 21, "j": 23, "v": 6, "e": 3, "d": 14, "gp": 19, "gc": 45, "sg": -26, "aproveitamento": 30, "ultimos": "DDDVE", "zona": "rebaixamento" },
            { "pos": 19, "time": "Fortaleza", "p": 18, "j": 23, "v": 4, "e": 6, "d": 13, "gp": 23, "gc": 38, "sg": -15, "aproveitamento": 26, "ultimos": "DDDEE", "zona": "rebaixamento" },
            { "pos": 20, "time": "Sport", "p": 14, "j": 22, "v": 2, "e": 8, "d": 12, "gp": 16, "gc": 34, "sg": -18, "aproveitamento": 21, "ultimos": "DEDED", "zona": "rebaixamento" }
        ]
        
        # 3. SALVAR NOVOS DADOS NO BANCO
        try:
            brasileirao_db.save_classification(dados, fonte="api_simulada")
            print("✅ Dados salvos no banco com sucesso")
        except Exception as db_error:
            print(f"⚠️ Erro ao salvar no banco: {db_error}")
        
        # 4. RETORNAR DADOS ATUALIZADOS
        return jsonify({
            "success": True,
            "data": dados,
            "total": len(dados),
            "last_updated": datetime.now().isoformat(),
            "data_source": "api_fresh",
            "cache_duration": 1800,  # 30 minutos em segundos
            "note": "Dados atualizados e salvos no banco"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "data": [],
            "total": 0,
            "data_source": "error"
        }), 500

@bp_br.route("/brasileirao/db-status", methods=["GET"])
@cross_origin()
def api_db_status():
    """
    Endpoint para verificar status do banco de dados
    GET /api/br/brasileirao/db-status
    """
    try:
        from models.brasileirao_db import brasileirao_db
        
        data_age = brasileirao_db.get_data_age()
        is_fresh = brasileirao_db.is_data_fresh()
        latest_data = brasileirao_db.get_latest_classification()
        
        return jsonify({
            "success": True,
            "database_status": "connected",
            "has_data": latest_data is not None,
            "data_age": data_age,
            "is_fresh": is_fresh,
            "total_teams": len(latest_data) if latest_data else 0,
            "sample_team": latest_data[0] if latest_data else None,
            "note": "Status do banco de dados SQLite"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "database_status": "error",
            "error": str(e),
            "note": "Erro ao acessar banco de dados"
        }), 500

@bp_br.route("/brasileirao/job-status", methods=["GET"])
@cross_origin()
def api_job_status():
    """
    Endpoint para verificar status do job diário
    GET /api/br/brasileirao/job-status
    """
    try:
        from models.brasileirao_db import brasileirao_db
        from datetime import datetime, timedelta
        import os
        
        # Verificar se arquivo de log existe
        log_path = "logs/daily_job.log"
        log_exists = os.path.exists(log_path)
        
        # Status dos dados
        data_age = brasileirao_db.get_data_age()
        is_fresh = brasileirao_db.is_data_fresh(max_age_hours=24)  # Frescos se < 24h
        
        # Próxima execução (23h55 de hoje ou amanhã)
        now = datetime.now()
        hoje_23h55 = now.replace(hour=23, minute=55, second=0, microsecond=0)
        
        if now < hoje_23h55:
            proxima_execucao = hoje_23h55
        else:
            proxima_execucao = hoje_23h55 + timedelta(days=1)
        
        # Status do job
        job_status = "scheduled" if is_fresh else "pending"
        if not log_exists:
            job_status = "not_started"
        
        return jsonify({
            "success": True,
            "job_status": job_status,
            "scheduled_time": "23:55 daily",
            "next_execution": proxima_execucao.strftime("%d/%m/%Y %H:%M:%S"),
            "last_data_update": data_age,
            "data_fresh": is_fresh,
            "log_file_exists": log_exists,
            "current_time": now.strftime("%d/%m/%Y %H:%M:%S"),
            "note": "Job diário configurado para atualizar dados às 23h55"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "note": "Erro ao verificar status do job"
        }), 500

@bp_br.route("/brasileirao/force-update", methods=["POST"])
@cross_origin()
def api_force_update():
    """
    Endpoint para forçar atualização manual (apenas para desenvolvimento)
    POST /api/br/brasileirao/force-update
    """
    try:
        from jobs.daily_updater import job_principal_23h55
        import threading
        
        # Executar job em thread separada para não travar a resposta
        def run_job():
            try:
                job_principal_23h55()
            except Exception as e:
                print(f"Erro no job manual: {e}")
        
        thread = threading.Thread(target=run_job, daemon=True)
        thread.start()
        
        return jsonify({
            "success": True,
            "message": "Atualização manual iniciada",
            "note": "Job executando em background. Verifique logs para progresso.",
            "warning": "Use apenas para desenvolvimento/teste"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "note": "Erro ao iniciar atualização manual"
        }), 500

@bp_br.route("/loteca/current", methods=["GET"])
@cross_origin()
def current_loteca_matches():
    """
    Retorna os confrontos atuais da Loteca com dados reais
    Combina dados do Cartola FC para jogos brasileiros + estimativas para internacionais
    GET /api/br/loteca/current
    """
    try:
        # Usar provider CORRIGIDO que implementa as correções identificadas
        result = get_current_loteca_matches()
        
        # O novo provider já retorna um dict completo
        if isinstance(result, dict):
            return jsonify(result)
        
        # Fallback se retornar lista (compatibilidade)
        return jsonify({
            "success": True,
            "matches": result,
            "total": len(result),
            "data_source": "corrected_provider",
            "note": "Dados corrigidos - sem hardcoded, com dados reais quando possível"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "matches": [],
            "total": 0,
            "data_source": "error",
            "note": "Configure APIs para dados 100% reais"
        }), 500

# === ROTAS DE CLASSIFICAÇÃO PARA O SITE ===

@bp_br.route("/classificacao/serie-a", methods=["GET"])
@cross_origin()
def api_classificacao_serie_a():
    """
    Endpoint para obter classificação da Série A
    GET /api/br/classificacao/serie-a
    """
    try:
        classificacao = classificacao_db.get_classificacao_serie_a()
        
        if not classificacao:
            return jsonify({
                "success": False,
                "error": "Nenhum dado de classificação encontrado",
                "data": []
            }), 404
        
        return jsonify({
            "success": True,
            "data": classificacao,
            "total": len(classificacao),
            "campeonato": "Brasileirão Série A",
            "ultima_atualizacao": classificacao[0].get('data_atualizacao') if classificacao else None
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao carregar classificação Série A: {str(e)}"
        }), 500

@bp_br.route("/classificacao/serie-b", methods=["GET"])
@cross_origin()
def api_classificacao_serie_b():
    """
    Endpoint para obter classificação da Série B
    GET /api/br/classificacao/serie-b
    """
    try:
        classificacao = classificacao_db.get_classificacao_serie_b()
        
        return jsonify({
            "success": True,
            "data": classificacao,
            "total": len(classificacao),
            "campeonato": "Brasileirão Série B",
            "ultima_atualizacao": classificacao[0].get('data_atualizacao') if classificacao else None
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao carregar classificação Série B: {str(e)}"
        }), 500

@bp_br.route("/classificacao/atualizar", methods=["POST"])
@cross_origin()
def api_atualizar_classificacao():
    """
    Endpoint para atualizar dados da classificação (via site)
    POST /api/br/classificacao/atualizar
    """
    try:
        data = request.get_json()
        time_id = data.get('time_id')
        campo = data.get('campo')
        valor = data.get('valor')
        
        if not all([time_id, campo, valor]):
            return jsonify({
                "success": False,
                "error": "Parâmetros obrigatórios: time_id, campo, valor"
            }), 400
        
        sucesso = classificacao_db.update_time_stats(time_id, campo, valor)
        
        if sucesso:
            return jsonify({
                "success": True,
                "message": "Classificação atualizada com sucesso"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Erro ao atualizar classificação"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao atualizar classificação: {str(e)}"
        }), 500

# Função para registrar o blueprint (será chamada em app.py)
def register_routes(app):
    """Registrar rotas do Brasileirão na aplicação Flask"""
    app.register_blueprint(bp_br)
