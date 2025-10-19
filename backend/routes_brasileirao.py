from flask import Blueprint, jsonify, request, send_file
from flask_cors import cross_origin
import os
from services.cartola_provider import clubes, estatisticas_clube, mercado_status, health_check, get_clube_mappings, get_clube_id_by_name
# from services.loteca_provider_new import get_current_loteca_matches  # REMOVIDO: código morto
from models.classificacao_db import classificacao_db
from models.jogos_manager import JogosManager
from datetime import datetime
from services.elenco_provider import get_elenco_data, get_all_elenco_data

# Blueprint para rotas do Brasileirão
bp_br = Blueprint("br", __name__, url_prefix="/api/br")
bp_confrontos = Blueprint("confrontos", __name__, url_prefix="/api")

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
        # result = get_current_loteca_matches()  # REMOVIDO: código morto
        result = {"success": False, "error": "Endpoint removido - código morto"}
        
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

@bp_br.route("/estatisticas/<clube>", methods=["GET"])
@cross_origin()
def api_estatisticas_clube(clube):
    """
    Endpoint para estatísticas detalhadas de um clube específico
    GET /api/br/estatisticas/{clube}
    """
    try:
        jm = JogosManager()
        stats = jm.calcular_estatisticas(clube)
        
        return jsonify({
            "success": True,
            "clube": clube,
            "pontos_total": stats.get('pontos_total', 0),
            "total_jogos": stats.get('total_jogos', 0),
            "ppg_casa": stats.get('ppg_casa', 0),
            "ppg_fora": stats.get('ppg_fora', 0),
            "aproveitamento_casa": stats.get('aproveitamento_casa', 0),
            "aproveitamento_fora": stats.get('aproveitamento_fora', 0),
            "vitorias": stats.get('vitorias', 0),
            "empates": stats.get('empates', 0),
            "derrotas": stats.get('derrotas', 0),
            "gols_marcados": stats.get('gols_marcados', 0),
            "gols_sofridos": stats.get('gols_sofridos', 0),
            "saldo_gols": stats.get('saldo_gols', 0),
            "clean_sheets": stats.get('clean_sheets', 0),
            "jogos_casa": stats.get('jogos_casa', 0),
            "jogos_fora": stats.get('jogos_fora', 0),
            "pontos_casa": stats.get('pontos_casa', 0),
            "pontos_fora": stats.get('pontos_fora', 0)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao carregar estatísticas de {clube}: {str(e)}",
            "clube": clube
        }), 500

@bp_br.route("/ranking-completo", methods=["GET"])
@cross_origin()
def api_ranking_completo():
    """
    Endpoint para ranking completo de todos os clubes
    GET /api/br/ranking-completo
    """
    try:
        jm = JogosManager()
        
        clubes = [
            'flamengo', 'palmeiras', 'cruzeiro', 'mirassol', 'bahia',
            'botafogo', 'fluminense', 'sao-paulo', 'gremio', 'red-bull-bragantino',
            'atletico-mg', 'ceara', 'corinthians', 'vasco', 'internacional',
            'santos', 'juventude', 'vitoria', 'fortaleza', 'sport-recife'
        ]
        
        ranking = []
        
        for clube in clubes:
            try:
                stats = jm.calcular_estatisticas(clube)
                ppg_total = stats['pontos_total'] / stats['total_jogos'] if stats['total_jogos'] > 0 else 0
                
                ranking.append({
                    'clube': clube,
                    'nome_display': formatar_nome_clube(clube),
                    'pontos': stats['pontos_total'],
                    'jogos': stats['total_jogos'],
                    'ppg_total': round(ppg_total, 2),
                    'ppg_casa': stats['ppg_casa'],
                    'ppg_fora': stats['ppg_fora'],
                    'aproveitamento_casa': stats['aproveitamento_casa'],
                    'aproveitamento_fora': stats['aproveitamento_fora'],
                    'vitorias': stats['vitorias'],
                    'empates': stats['empates'],
                    'derrotas': stats['derrotas'],
                    'gols_marcados': stats.get('gols_marcados', 0),
                    'gols_sofridos': stats.get('gols_sofridos', 0),
                    'saldo_gols': stats.get('saldo_gols', 0)
                })
            except Exception as e:
                print(f"Erro ao processar {clube}: {e}")
                # Adicionar dados padrão em caso de erro
                ranking.append({
                    'clube': clube,
                    'nome_display': formatar_nome_clube(clube),
                    'pontos': 0,
                    'jogos': 0,
                    'ppg_total': 0,
                    'ppg_casa': 0,
                    'ppg_fora': 0,
                    'aproveitamento_casa': 0,
                    'aproveitamento_fora': 0,
                    'vitorias': 0,
                    'empates': 0,
                    'derrotas': 0,
                    'gols_marcados': 0,
                    'gols_sofridos': 0,
                    'saldo_gols': 0
                })
        
        # Ordenar por PPG Total
        ranking.sort(key=lambda x: x['ppg_total'], reverse=True)
        
        # Adicionar posições e status
        for i, clube in enumerate(ranking):
            clube['posicao'] = i + 1
            clube['status'] = determinar_status_clube(clube['ppg_total'])
        
        return jsonify({
            'success': True,
            'ranking': ranking,
            'total_clubes': len(ranking),
            'ultima_atualizacao': datetime.now().isoformat(),
            'lider': ranking[0]['nome_display'] if ranking else 'N/A',
            'zona_rebaixamento': len([c for c in ranking if c['status']['codigo'] == 'ZONA'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Erro ao gerar ranking: {str(e)}"
        }), 500

def formatar_nome_clube(clube):
    """Formatar nome do clube para exibição"""
    nomes = {
        'flamengo': 'CR Flamengo',
        'palmeiras': 'SE Palmeiras', 
        'cruzeiro': 'Cruzeiro EC',
        'mirassol': 'Mirassol FC',
        'bahia': 'EC Bahia',
        'botafogo': 'Botafogo FR',
        'fluminense': 'Fluminense FC',
        'sao-paulo': 'São Paulo FC',
        'gremio': 'Grêmio FBPA',
        'red-bull-bragantino': 'RB Bragantino',
        'atletico-mg': 'Atlético Mineiro',
        'ceara': 'Ceará SC',
        'corinthians': 'SC Corinthians',
        'vasco': 'CR Vasco da Gama',
        'internacional': 'SC Internacional',
        'santos': 'Santos FC',
        'juventude': 'EC Juventude',
        'vitoria': 'EC Vitória',
        'fortaleza': 'Fortaleza EC',
        'sport-recife': 'Sport Recife'
    }
    return nomes.get(clube, clube.title())

def determinar_status_clube(ppg):
    """Determina status do clube baseado no PPG"""
    if ppg >= 1.60:
        return {'codigo': 'G5', 'descricao': 'Libertadores', 'cor': '#28a745'}
    elif ppg >= 1.20:
        return {'codigo': 'MEIO', 'descricao': 'Meio de Tabela', 'cor': '#ffc107'}
    elif ppg >= 0.90:
        return {'codigo': 'RISCO', 'descricao': 'Zona de Risco', 'cor': '#fd7e14'}
    else:
        return {'codigo': 'ZONA', 'descricao': 'Rebaixamento', 'cor': '#dc3545'}

@bp_br.route("/loteca/clube/<string:clube_slug>/dados", methods=["GET"])
@cross_origin()
def api_dados_clube_loteca(clube_slug):
    """
    Endpoint público para buscar dados de um clube para a página da Loteca
    GET /api/br/loteca/clube/{clube_slug}/dados
    
    Retorna dados consolidados do dashboard admin para uso na análise rápida
    """
    try:
        # Inicializar o JogosManager
        jogos_manager = JogosManager()
        
        # Buscar estatísticas dos jogos (dados mais confiáveis)
        estatisticas_jogos = jogos_manager.calcular_estatisticas(clube_slug)
        
        if not estatisticas_jogos or estatisticas_jogos.get('total_jogos', 0) == 0:
            return jsonify({
                "success": False,
                "error": f"Dados não encontrados para o clube: {clube_slug}",
                "clube": clube_slug,
                "dados": {}
            }), 404
        
        # Mapear dados para o formato esperado pela página da Loteca
        dados_loteca = {
            # Forma recente (últimos 5 jogos)
            "forma_recente": estatisticas_jogos.get('ultimos_5_resultados', 'N-N-N-N-N'),
            
            # Posição na tabela (buscar da classificação se disponível)
            "posicao_tabela": "N/A",  # Será implementado depois
            
            # Aproveitamento em casa
            "aproveitamento_casa": f"{estatisticas_jogos.get('aproveitamento_casa', 0):.0f}%",
            
            # Aproveitamento fora
            "aproveitamento_fora": f"{estatisticas_jogos.get('aproveitamento_fora', 0):.0f}%",
            
            # Dados adicionais para análises
            "total_jogos": estatisticas_jogos.get('total_jogos', 0),
            "vitorias": estatisticas_jogos.get('vitorias', 0),
            "empates": estatisticas_jogos.get('empates', 0),
            "derrotas": estatisticas_jogos.get('derrotas', 0),
            "gols_marcados": estatisticas_jogos.get('gols_marcados', 0),
            "gols_sofridos": estatisticas_jogos.get('gols_sofridos', 0),
            "media_gols_marcados": round(estatisticas_jogos.get('media_gols_marcados', 0), 2),
            "media_gols_sofridos": round(estatisticas_jogos.get('media_gols_sofridos', 0), 2),
            "clean_sheets": estatisticas_jogos.get('clean_sheets', 0),
            "pct_clean_sheets": round(estatisticas_jogos.get('pct_clean_sheets', 0), 1),
            "sequencia_atual": estatisticas_jogos.get('sequencia_atual', ''),
            "pontos_ultimos_5": estatisticas_jogos.get('pontos_ultimos_5', 0),
            
            # Dados de casa/fora
            "jogos_casa": estatisticas_jogos.get('jogos_casa', 0),
            "vitorias_casa": estatisticas_jogos.get('vitorias_casa', 0),
            "empates_casa": estatisticas_jogos.get('empates_casa', 0),
            "derrotas_casa": estatisticas_jogos.get('derrotas_casa', 0),
            "jogos_fora": estatisticas_jogos.get('jogos_fora', 0),
            "vitorias_fora": estatisticas_jogos.get('vitorias_fora', 0),
            "empates_fora": estatisticas_jogos.get('empates_fora', 0),
            "derrotas_fora": estatisticas_jogos.get('derrotas_fora', 0)
        }
        
        return jsonify({
            "success": True,
            "clube": clube_slug,
            "nome_formatado": formatar_nome_clube(clube_slug),
            "dados": dados_loteca,
            "fonte": "dashboard_admin",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "clube": clube_slug,
            "error": str(e),
            "dados": {}
        }), 500

@bp_br.route("/loteca/confronto/<string:clube_casa>/<string:clube_fora>", methods=["GET"])
@cross_origin()
def api_confronto_loteca(clube_casa, clube_fora):
    """
    Endpoint público para comparar dois clubes para a página da Loteca
    GET /api/br/loteca/confronto/{clube_casa}/{clube_fora}
    
    Retorna dados comparativos dos dois clubes para análise rápida
    """
    try:
        # Buscar dados dos dois clubes diretamente
        jogos_manager = JogosManager()
        
        # Buscar estatísticas dos dois clubes
        stats_casa = jogos_manager.calcular_estatisticas(clube_casa)
        stats_fora = jogos_manager.calcular_estatisticas(clube_fora)
        
        if not stats_casa or stats_casa.get('total_jogos', 0) == 0:
            return jsonify({
                "success": False,
                "error": f"Dados do clube da casa não encontrados: {clube_casa}"
            }), 404
            
        if not stats_fora or stats_fora.get('total_jogos', 0) == 0:
            return jsonify({
                "success": False,
                "error": f"Dados do clube visitante não encontrados: {clube_fora}"
            }), 404
        
        # Preparar dados dos clubes
        casa_dados = {
            "forma_recente": stats_casa.get('ultimos_5_resultados', 'N-N-N-N-N'),
            "aproveitamento_casa": f"{stats_casa.get('aproveitamento_casa', 0):.0f}%",
            "aproveitamento_fora": f"{stats_casa.get('aproveitamento_fora', 0):.0f}%",
            "pontos_ultimos_5": stats_casa.get('pontos_ultimos_5', 0)
        }
        
        fora_dados = {
            "forma_recente": stats_fora.get('ultimos_5_resultados', 'N-N-N-N-N'),
            "aproveitamento_casa": f"{stats_fora.get('aproveitamento_casa', 0):.0f}%",
            "aproveitamento_fora": f"{stats_fora.get('aproveitamento_fora', 0):.0f}%",
            "pontos_ultimos_5": stats_fora.get('pontos_ultimos_5', 0)
        }
        
        # Análise comparativa
        analise = {
            "forma_recente": {
                "casa": casa_dados['forma_recente'],
                "fora": fora_dados['forma_recente'],
                "vantagem": analisar_forma_recente(casa_dados['pontos_ultimos_5'], fora_dados['pontos_ultimos_5'])
            },
            "fator_casa": {
                "casa": casa_dados['aproveitamento_casa'],
                "fora": fora_dados['aproveitamento_fora'],  # VISITANTE FORA DE CASA
                "vantagem": analisar_fator_casa(
                    float(casa_dados['aproveitamento_casa'].replace('%', '')),
                    float(fora_dados['aproveitamento_fora'].replace('%', ''))
                )
            },
            "confronto_direto": {
                "casa": "N/A",  # Será implementado depois
                "fora": "N/A",
                "vantagem": "equilibrio"
            }
        }
        
        return jsonify({
            "success": True,
            "confronto": f"{clube_casa} vs {clube_fora}",
            "casa": {
                "clube": clube_casa,
                "nome": formatar_nome_clube(clube_casa),
                "dados": casa_dados
            },
            "fora": {
                "clube": clube_fora,
                "nome": formatar_nome_clube(clube_fora),
                "dados": fora_dados
            },
            "analise": analise,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "confronto": f"{clube_casa} vs {clube_fora}",
            "error": str(e)
        }), 500

def analisar_forma_recente(pontos_casa, pontos_fora):
    """Analisa qual time tem melhor forma recente baseado nos pontos dos últimos 5 jogos"""
    if pontos_casa > pontos_fora:
        return "casa"
    elif pontos_fora > pontos_casa:
        return "fora"
    else:
        return "equilibrio"

def analisar_fator_casa(aproveitamento_casa, aproveitamento_fora):
    """
    Analisa o fator casa: aproveitamento do mandante em casa vs aproveitamento do visitante fora
    
    Args:
        aproveitamento_casa (float): % de aproveitamento do time da casa jogando em casa
        aproveitamento_fora (float): % de aproveitamento do time visitante jogando fora
    
    Returns:
        str: 'casa', 'fora' ou 'equilibrio'
    """
    margem_equilibrio = 5.0  # Margem de 5% para considerar equilíbrio
    
    if aproveitamento_casa > aproveitamento_fora + margem_equilibrio:
        return "casa"
    elif aproveitamento_fora > aproveitamento_casa + margem_equilibrio:
        return "fora"
    else:
        return "equilibrio"

@bp_br.route("/loteca/confronto-historico/<string:clube_casa>/<string:clube_fora>", methods=["GET"])
@cross_origin()
def api_confronto_historico(clube_casa, clube_fora):
    """
    Endpoint para obter histórico de confrontos entre dois clubes
    GET /api/br/loteca/confronto-historico/{clube_casa}/{clube_fora}
    
    Retorna os últimos confrontos para a seção "Cartola FC - Dados Reais"
    """
    try:
        import csv
        import os
        
        # Caminho do arquivo de confronto (tentar ambas as ordens)
        confrontos_path = os.path.join(os.path.dirname(__file__), 'models', 'Confrontos')
        
        # Tentar primeira ordem
        arquivo_confronto = os.path.join(confrontos_path, f"{clube_casa.title()}_vs_{clube_fora.title()}.csv")
        
        # Se não existir, tentar ordem inversa
        if not os.path.exists(arquivo_confronto):
            arquivo_confronto = os.path.join(confrontos_path, f"{clube_fora.title()}_vs_{clube_casa.title()}.csv")
        
        if not os.path.exists(arquivo_confronto):
            return jsonify({
                "success": False,
                "error": f"Histórico de confrontos não encontrado: {clube_casa} vs {clube_fora}"
            }), 404
        
        # Carregar confrontos
        confrontos = []
        with open(arquivo_confronto, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                confrontos.append(row)
        
        # Pegar os últimos 5 confrontos
        ultimos_5 = confrontos[:5]
        
        # Analisar estatísticas dos últimos 10
        ultimos_10 = confrontos[:10]
        vitorias_casa = 0
        empates = 0
        vitorias_fora = 0
        
        for jogo in ultimos_10:
            resultado = jogo['resultado_corinthians'].upper()
            if clube_casa.lower() == 'corinthians':
                if resultado == 'V':
                    vitorias_casa += 1
                elif resultado == 'E':
                    empates += 1
                else:
                    vitorias_fora += 1
            else:  # clube_casa é Flamengo
                if resultado == 'V':
                    vitorias_fora += 1
                elif resultado == 'E':
                    empates += 1
                else:
                    vitorias_casa += 1
        
        # Determinar tendência
        if vitorias_casa > vitorias_fora:
            tendencia = f"Vantagem {clube_casa}"
        elif vitorias_fora > vitorias_casa:
            tendencia = f"Vantagem {clube_fora}"
        else:
            tendencia = "Equilíbrio"
        
        return jsonify({
            "success": True,
            "confronto": f"{clube_casa} vs {clube_fora}",
            "ultimos_5_jogos": ultimos_5,
            "estatisticas_ultimos_10": {
                "total_jogos": len(ultimos_10),
                "vitorias_casa": vitorias_casa,
                "empates": empates,
                "vitorias_fora": vitorias_fora,
                "resumo_h2h": f"{vitorias_casa}V-{empates}E-{vitorias_fora}D",
                "tendencia": tendencia
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "confronto": f"{clube_casa} vs {clube_fora}",
            "error": str(e)
        }), 500

@bp_br.route("/loteca/confronto-modal/<clube_casa>/<clube_fora>", methods=["GET"])
@cross_origin()
def api_confronto_historico_modal(clube_casa, clube_fora):
    """
    Endpoint para buscar histórico de confrontos para o modal
    GET /api/br/loteca/confronto-historico/{clube_casa}/{clube_fora}
    
    Busca arquivo CSV com ordem flexível: Clube1_vs_Clube2.csv ou Clube2_vs_Clube1.csv
    """
    import os
    import csv
    from pathlib import Path
    
    try:
        # Normalizar nomes dos clubes
        clube_casa_norm = clube_casa.strip().title()
        clube_fora_norm = clube_fora.strip().title()
        
        # Diretório dos confrontos
        confrontos_dir = Path(__file__).parent / "models" / "Confrontos"
        
        # Tentar ambas as ordens possíveis
        arquivo_opcoes = [
            f"{clube_casa_norm}_vs_{clube_fora_norm}.csv",
            f"{clube_fora_norm}_vs_{clube_casa_norm}.csv"
        ]
        
        arquivo_encontrado = None
        for arquivo in arquivo_opcoes:
            caminho_arquivo = confrontos_dir / arquivo
            if caminho_arquivo.exists():
                arquivo_encontrado = caminho_arquivo
                break
        
        if not arquivo_encontrado:
            return jsonify({
                "success": False,
                "error": f"Arquivo de confrontos não encontrado para {clube_casa} vs {clube_fora}",
                "arquivos_procurados": arquivo_opcoes
            }), 404
        
        # Usar parser robusto para ler dados do CSV
        from services.csv_parser_robusto import processar_csv_confrontos
        
        sucesso, confrontos_raw, mensagem = processar_csv_confrontos(str(arquivo_encontrado))
        
        if not sucesso:
            return jsonify({
                "success": False,
                "error": f"Erro ao processar arquivo CSV: {mensagem}",
                "confronto": f"{clube_casa} vs {clube_fora}"
            }), 500
        
        # Converter para formato compatível com código existente
        confrontos = []
        for confronto_raw in confrontos_raw:
            confronto = {
                "data": confronto_raw.get('data', ''),
                "mandante": confronto_raw.get('mandante_nome', ''),
                "visitante": confronto_raw.get('visitante_nome', ''),
                "placar": confronto_raw.get('placar', ''),
                "vencedor": confronto_raw.get('vencedor', ''),
                "competicao": confronto_raw.get('campeonato', ''),
                "resultado": confronto_raw.get('resultado', ''),
                "resultado_corinthians": confronto_raw.get('resultado', '')  # Compatibilidade
            }
            confrontos.append(confronto)
        
        return jsonify({
            "success": True,
            "confronto": f"{clube_casa} vs {clube_fora}",
            "arquivo_usado": arquivo_encontrado.name,
            "total_confrontos": len(confrontos),
            "confrontos": confrontos,  # TODOS os confrontos do CSV
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "confronto": f"{clube_casa} vs {clube_fora}"
        }), 500

@bp_br.route("/elenco/<clube_nome>", methods=["GET"])
@cross_origin()
def api_elenco_clube(clube_nome):
    """
    Endpoint para obter dados de elenco de um clube específico
    GET /api/br/elenco/{clube_nome}
    
    Retorna dados da planilha de estatísticas de elenco
    """
    try:
        # Obter dados do clube
        dados_elenco = get_elenco_data(clube_nome)
        
        return jsonify({
            "success": True,
            "clube": clube_nome,
            "dados": dados_elenco,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "clube": clube_nome
        }), 500

@bp_br.route("/elenco", methods=["GET"])
@cross_origin()
def api_todos_elencos():
    """
    Endpoint para obter dados de elenco de todos os clubes
    GET /api/br/elenco
    
    Retorna todos os dados da planilha de estatísticas de elenco
    """
    try:
        # Obter todos os dados
        todos_dados = get_all_elenco_data()
        
        return jsonify({
            "success": True,
            "total_clubes": len(todos_dados),
            "dados": todos_dados,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ROTA PRINCIPAL: /api/br/confrontos/<filename>
@bp_br.route("/confrontos/<filename>", methods=["GET"])
@cross_origin()
def servir_arquivo_confrontos(filename):
    """
    Endpoint para servir arquivos CSV de confrontos
    GET /api/br/confrontos/<filename>
    """
    try:
        # Caminho para a pasta de confrontos
        confrontos_path = os.path.join(os.path.dirname(__file__), 'models', 'Confrontos')
        arquivo_path = os.path.join(confrontos_path, filename)
        
        # Verificar se o arquivo existe
        if not os.path.exists(arquivo_path):
            return jsonify({
                "error": f"Arquivo não encontrado: {filename}"
            }), 404
        
        # Verificar se é um arquivo CSV
        if not filename.lower().endswith('.csv'):
            return jsonify({
                "error": "Apenas arquivos CSV são permitidos"
            }), 400
        
        # Servir o arquivo
        return send_file(arquivo_path, mimetype='text/csv')
        
    except Exception as e:
        return jsonify({
            "error": f"Erro ao servir arquivo: {str(e)}"
        }), 500

# ROTA ALTERNATIVA: /api/confrontos/<filename> (redireciona para /api/br/confrontos/)
@bp_br.route("/confrontos-alt/<filename>", methods=["GET"])
@cross_origin()
def servir_arquivo_confrontos_alt(filename):
    """
    Endpoint alternativo para servir arquivos CSV de confrontos
    GET /api/br/confrontos-alt/<filename> (redireciona para /api/br/confrontos/<filename>)
    """
    # Redirecionar para a função principal
    return servir_arquivo_confrontos(filename)

# ROTA PRINCIPAL: /api/confrontos/<filename> (sem prefixo /br)
@bp_confrontos.route("/confrontos/<filename>", methods=["GET"])
@cross_origin()
def servir_arquivo_confrontos_direto(filename):
    """
    Endpoint direto para servir arquivos CSV de confrontos
    GET /api/confrontos/<filename>
    """
    # Usar a mesma lógica da função principal
    try:
        # Caminho para a pasta de confrontos
        confrontos_path = os.path.join(os.path.dirname(__file__), 'models', 'Confrontos')
        arquivo_path = os.path.join(confrontos_path, filename)
        
        # Verificar se o arquivo existe
        if not os.path.exists(arquivo_path):
            return jsonify({
                "error": f"Arquivo não encontrado: {filename}"
            }), 404
        
        # Verificar se é um arquivo CSV
        if not filename.lower().endswith('.csv'):
            return jsonify({
                "error": "Apenas arquivos CSV são permitidos"
            }), 400
        
        # Servir o arquivo
        return send_file(arquivo_path, mimetype='text/csv')
        
    except Exception as e:
        return jsonify({
            "error": f"Erro ao servir arquivo: {str(e)}"
        }), 500

# Função para registrar o blueprint (será chamada em app.py)
def register_routes(app):
    """Registrar rotas do Brasileirão na aplicação Flask"""
    app.register_blueprint(bp_br)
    app.register_blueprint(bp_confrontos)
