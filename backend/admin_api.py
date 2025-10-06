#!/usr/bin/env python3
"""
API Backend para Interface Administrativa
Conecta a interface HTML com a Central de Dados SQLite
"""

from flask import Blueprint, request, jsonify, render_template, send_from_directory
from flask_cors import cross_origin
import os
import json
import logging
from datetime import datetime
from models.central_dados import CentralDados
from models.classificacao_db import classificacao_db
from models.jogos_manager import jogos_manager
from models.concurso_manager import concurso_manager
import subprocess
import sys

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar blueprint para admin
bp_admin = Blueprint('admin', __name__)

# Configurações
ADMIN_KEY = 'loteca2024admin'  # Chave de administrador
central_dados = CentralDados()

def verificar_auth(request_data):
    """Verificar autenticação do administrador"""
    auth_key = request_data.get('admin_key') or request.headers.get('X-Admin-Key')
    logger.info(f"🔐 [AUTH] Key recebida: '{auth_key}'")
    logger.info(f"🔐 [AUTH] Key esperada: '{ADMIN_KEY}'")
    logger.info(f"🔐 [AUTH] Tipo recebido: {type(auth_key)}")
    logger.info(f"🔐 [AUTH] Request data: {request_data}")
    resultado = auth_key == ADMIN_KEY
    logger.info(f"🔐 [AUTH] Resultado: {resultado}")
    return resultado

@bp_admin.route('/admin')
def admin_interface():
    """Servir a interface administrativa"""
    try:
        # Caminho correto para o arquivo admin
        admin_path = os.path.join(os.path.dirname(__file__), 'admin_interface.html')
        with open(admin_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        logger.error(f"Erro ao servir interface admin: {e}")
        return f"Erro ao carregar interface: {e}", 500

@bp_admin.route('/api/admin/auth', methods=['POST'])
@cross_origin()
def admin_auth():
    """Autenticar administrador"""
    data = request.get_json()
    key = data.get('key')
    
    if key == ADMIN_KEY:
        return jsonify({
            'success': True,
            'message': 'Autenticação realizada com sucesso'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Chave de acesso inválida'
        }), 401

@bp_admin.route('/api/admin/dashboard', methods=['GET'])
@cross_origin()
def get_dashboard():
    """Obter estatísticas do dashboard"""
    try:
        try:
            stats = central_dados.get_estatisticas_sistema()
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            stats = {'total_clubes': 0, 'ultima_sincronizacao': 'Erro', 'dados_mais_antigos': 'N/A', 'clubes_por_fonte': {}}
        
        # Processar estatísticas para o dashboard
        dashboard_data = {
            'total_clubes': stats.get('total_clubes', 0),
            'clubes_serie_a': 0,
            'clubes_serie_b': 0,
            'ultima_sincronizacao': stats.get('ultima_sincronizacao', 'Nunca'),
            'dados_mais_antigos': stats.get('dados_mais_antigos', 'N/A'),
            'fontes_principais': stats.get('clubes_por_fonte', {}),
            'tamanho_db': _get_db_size()
        }
        
        # Contar clubes por série
        try:
            with central_dados.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM clubes WHERE serie = 'Série A' AND ativo = 1")
                dashboard_data['clubes_serie_a'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM clubes WHERE serie = 'Série B' AND ativo = 1")
                dashboard_data['clubes_serie_b'] = cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Erro ao contar clubes por série: {e}")
            dashboard_data['clubes_serie_a'] = 0
            dashboard_data['clubes_serie_b'] = 0
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter dashboard: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao carregar dashboard'
        }), 500

@bp_admin.route('/api/admin/clubes', methods=['GET'])
@cross_origin()
def get_clubes():
    """Obter lista de todos os clubes"""
    try:
        try:
            with central_dados.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, nome_fantasia, abreviacao, estado, serie, 
                           escudo_60x60, cor_primaria, cor_secundaria, ativo
                    FROM clubes 
                    WHERE ativo = 1
                    ORDER BY nome_fantasia
                """)
                
                clubes = []
                columns = [desc[0] for desc in cursor.description]
                
                for row in cursor.fetchall():
                    clube = dict(zip(columns, row))
                    clubes.append(clube)
        except Exception as e:
            logger.error(f"Erro ao buscar clubes: {e}")
            clubes = []
        
        return jsonify({
            'success': True,
            'data': clubes,
            'total': len(clubes)
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter clubes: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao carregar clubes'
        }), 500

@bp_admin.route('/api/admin/clubes', methods=['POST'])
@cross_origin()
def criar_clube():
    """Criar ou atualizar um clube"""
    data = request.get_json()
    
    if not verificar_auth(data):
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    try:
        # Dados obrigatórios
        if not data.get('nome_fantasia') or not data.get('abreviacao'):
            return jsonify({
                'success': False,
                'message': 'Nome fantasia e abreviação são obrigatórios'
            }), 400
        
        # Preparar dados do clube
        clube_data = {
            'nome_fantasia': data.get('nome_fantasia'),
            'abreviacao': data.get('abreviacao'),
            'estado': data.get('estado'),
            'serie': data.get('serie'),
            'escudo_url': data.get('escudo_url'),
            'escudo_60x60': data.get('escudo_url'),  # Usar mesma URL para todos os tamanhos por enquanto
            'escudo_45x45': data.get('escudo_url'),
            'escudo_30x30': data.get('escudo_url'),
            'cor_primaria': data.get('cor_primaria'),
            'cor_secundaria': data.get('cor_secundaria'),
            'ativo': True
        }
        
        # Se tem ID, é atualização
        if data.get('id'):
            clube_data['id'] = data.get('id')
        
        # Salvar no banco
        clube_id = central_dados.salvar_clube(clube_data, fonte='MANUAL')
        
        return jsonify({
            'success': True,
            'message': 'Clube salvo com sucesso',
            'data': {'id': clube_id}
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar clube: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar clube: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/clubes/<int:clube_id>', methods=['DELETE'])
@cross_origin()
def excluir_clube(clube_id):
    """Excluir um clube (soft delete)"""
    data = request.get_json() or {}
    
    if not verificar_auth(data):
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    try:
        with central_dados.get_connection() as conn:
            cursor = conn.cursor()
            
            # Soft delete - marcar como inativo
            cursor.execute("""
                UPDATE clubes 
                SET ativo = 0, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (clube_id,))
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': 'Clube não encontrado'
                }), 404
            
            conn.commit()
            
            # Log da operação
            central_dados._log_operacao('DELETE', 'clubes', clube_id, usuario='ADMIN')
        
        return jsonify({
            'success': True,
            'message': 'Clube excluído com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao excluir clube: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao excluir clube'
        }), 500

@bp_admin.route('/api/admin/estatisticas', methods=['GET'])
@cross_origin()
def get_estatisticas():
    """Obter todas as estatísticas dos clubes"""
    try:
        try:
            with central_dados.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        s.clube_id,
                        c.nome_fantasia,
                        c.abreviacao,
                        s.total_atletas,
                        s.pct_provaveis,
                        s.media_pontos_elenco,
                        s.preco_medio,
                        s.rating,
                        s.fonte,
                        s.data_atualizacao
                    FROM clube_stats_atuais s
                    JOIN clubes c ON s.clube_id = c.id
                    WHERE c.ativo = 1
                    ORDER BY c.nome_fantasia
                """)
                
                estatisticas = []
                columns = [desc[0] for desc in cursor.description]
                
                for row in cursor.fetchall():
                    stat = dict(zip(columns, row))
                    estatisticas.append(stat)
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            estatisticas = []
        
        return jsonify({
            'success': True,
            'data': estatisticas,
            'total': len(estatisticas)
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao carregar estatísticas'
        }), 500

@bp_admin.route('/api/admin/estatisticas', methods=['POST'])
@cross_origin()
def salvar_estatisticas():
    """Salvar estatísticas de um clube"""
    data = request.get_json()
    
    if not verificar_auth(data):
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    try:
        clube_id = data.get('clube_id')
        if not clube_id:
            return jsonify({
                'success': False,
                'message': 'ID do clube é obrigatório'
            }), 400
        
        # Preparar dados das estatísticas
        stats_data = {
            'clube_id': clube_id,
            'total_atletas': data.get('total_atletas'),
            'pct_provaveis': data.get('pct_provaveis'),
            'media_pontos_elenco': data.get('media_pontos_elenco'),
            'preco_medio': data.get('preco_medio'),
            'rating': data.get('rating'),
            'fonte': data.get('fonte', 'MANUAL'),
            'data_atualizacao': datetime.now().isoformat()
        }
        
        # Remover valores vazios
        stats_data = {k: v for k, v in stats_data.items() if v is not None and v != ''}
        
        with central_dados.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se clube existe
            cursor.execute("SELECT id FROM clubes WHERE id = ? AND ativo = 1", (clube_id,))
            if not cursor.fetchone():
                return jsonify({
                    'success': False,
                    'message': 'Clube não encontrado'
                }), 404
            
            # Inserir ou atualizar estatísticas
            cursor.execute("""
                INSERT OR REPLACE INTO clube_stats_atuais 
                (clube_id, total_atletas, pct_provaveis, media_pontos_elenco, 
                 preco_medio, rating, fonte, data_atualizacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stats_data['clube_id'],
                stats_data.get('total_atletas'),
                stats_data.get('pct_provaveis'),
                stats_data.get('media_pontos_elenco'),
                stats_data.get('preco_medio'),
                stats_data.get('rating'),
                stats_data.get('fonte'),
                stats_data.get('data_atualizacao')
            ))
            
            conn.commit()
            
            # Log da operação
            central_dados._log_operacao('INSERT/UPDATE', 'clube_stats_atuais', clube_id, 
                                      dados=stats_data, usuario='ADMIN')
        
        return jsonify({
            'success': True,
            'message': 'Estatísticas salvas com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar estatísticas: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar estatísticas: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/estatisticas/<int:clube_id>', methods=['DELETE'])
@cross_origin()
def excluir_estatisticas(clube_id):
    """Excluir estatísticas de um clube"""
    data = request.get_json() or {}
    
    if not verificar_auth(data):
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    try:
        with central_dados.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM clube_stats_atuais WHERE clube_id = ?", (clube_id,))
            
            if cursor.rowcount == 0:
                return jsonify({
                    'success': False,
                    'message': 'Estatísticas não encontradas'
                }), 404
            
            conn.commit()
            
            # Log da operação
            central_dados._log_operacao('DELETE', 'clube_stats_atuais', clube_id, usuario='ADMIN')
        
        return jsonify({
            'success': True,
            'message': 'Estatísticas excluídas com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao excluir estatísticas: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao excluir estatísticas'
        }), 500

@bp_admin.route('/api/admin/backup', methods=['GET'])
@cross_origin()
def gerar_backup():
    """Gerar backup completo dos dados"""
    try:
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'clubes': [],
            'estatisticas': [],
            'metadata': central_dados.get_estatisticas_sistema()
        }
        
        with central_dados.get_connection() as conn:
            cursor = conn.cursor()
            
            # Exportar clubes
            cursor.execute("""
                SELECT * FROM clubes WHERE ativo = 1
            """)
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                clube = dict(zip(columns, row))
                backup_data['clubes'].append(clube)
            
            # Exportar estatísticas
            cursor.execute("""
                SELECT * FROM clube_stats_atuais
            """)
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                stat = dict(zip(columns, row))
                backup_data['estatisticas'].append(stat)
        
        return jsonify({
            'success': True,
            'data': backup_data,
            'filename': f'loteca-backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar backup: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro ao gerar backup'
        }), 500

@bp_admin.route('/api/admin/restore', methods=['POST'])
@cross_origin()
def restaurar_backup():
    """Restaurar dados de um backup"""
    data = request.get_json()
    
    if not verificar_auth(data):
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    try:
        backup_data = data.get('backup_data')
        if not backup_data:
            return jsonify({
                'success': False,
                'message': 'Dados de backup não fornecidos'
            }), 400
        
        clubes_restaurados = 0
        stats_restauradas = 0
        
        with central_dados.get_connection() as conn:
            # Restaurar clubes
            for clube in backup_data.get('clubes', []):
                central_dados.salvar_clube(clube, fonte='BACKUP')
                clubes_restaurados += 1
            
            # Restaurar estatísticas
            cursor = conn.cursor()
            for stat in backup_data.get('estatisticas', []):
                cursor.execute("""
                    INSERT OR REPLACE INTO clube_stats_atuais 
                    (clube_id, total_atletas, pct_provaveis, media_pontos_elenco, 
                     preco_medio, rating, fonte, data_atualizacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    stat.get('clube_id'),
                    stat.get('total_atletas'),
                    stat.get('pct_provaveis'),
                    stat.get('media_pontos_elenco'),
                    stat.get('preco_medio'),
                    stat.get('rating'),
                    stat.get('fonte'),
                    stat.get('data_atualizacao')
                ))
                stats_restauradas += 1
            
            conn.commit()
        
        return jsonify({
            'success': True,
            'message': f'Backup restaurado: {clubes_restaurados} clubes, {stats_restauradas} estatísticas'
        })
        
    except Exception as e:
        logger.error(f"Erro ao restaurar backup: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao restaurar backup: {str(e)}'
        }), 500

def _get_db_size():
    """Obter tamanho do banco de dados"""
    try:
        size = os.path.getsize(central_dados.db_path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "N/A"

# === ROTA PARA ESTATÍSTICAS DO DASHBOARD ===

@bp_admin.route('/api/admin/dashboard-stats', methods=['GET'])
@cross_origin()
def get_dashboard_stats():
    """Obter estatísticas para o dashboard da Central Admin"""
    try:
        # Buscar contagens de cada tabela
        stats = classificacao_db.get_tables_info()
        
        # Calcular total de clubes
        total_clubes = (stats.get('serie_a_count', 0) + 
                       stats.get('serie_b_count', 0) + 
                       stats.get('premier_league_count', 0) + 
                       stats.get('la_liga_count', 0) + 
                       stats.get('ligue1_count', 0))
        
        # Buscar última sincronização (mais recente entre todas as tabelas)
        ultima_sync = classificacao_db.get_last_update()
        
        return jsonify({
            'success': True,
            'data': {
                'total_clubes': total_clubes,
                'serie_a': stats.get('serie_a_count', 0),
                'serie_b': stats.get('serie_b_count', 0),
                'premier_league': stats.get('premier_league_count', 0),
                'la_liga': stats.get('la_liga_count', 0),
                'ligue1': stats.get('ligue1_count', 0),
                'ultima_sincronizacao': ultima_sync
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do dashboard: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ROTAS DA CLASSIFICAÇÃO ===

@bp_admin.route('/api/admin/classificacao', methods=['GET', 'POST'])
@cross_origin()
def get_classificacao():
    """Obter classificação de um campeonato"""
    logger.info("🔄 [API] === INICIANDO get_classificacao ===")
    
    # Suportar tanto GET quanto POST
    if request.method == 'GET':
        # Parâmetros via query string
        campeonato = request.args.get('campeonato', 'serie-a')
        admin_key = request.args.get('admin_key', '')
        
        # Verificar auth para GET
        if admin_key != 'loteca2024admin':
            logger.warning("🚫 [API] Auth falhou (GET)")
            return jsonify({
                'success': False,
                'message': 'Acesso negado'
            }), 401
            
        logger.info(f"📥 [API] GET - campeonato: {campeonato}")
    else:
        # POST - dados via JSON
        data = request.get_json()
        logger.info(f"📥 [API] POST - Dados recebidos: {data}")
        
        if not verificar_auth(data):
            logger.warning("🚫 [API] Auth falhou (POST)")
            return jsonify({
                'success': False,
                'message': 'Acesso negado'
            }), 401
            
        campeonato = data.get('campeonato', 'serie-a')
    
    logger.info("✅ [API] Auth OK")
    
    try:
        logger.info(f"🏆 [API] Campeonato solicitado: {campeonato}")
        
        if campeonato == 'serie-a' or campeonato == 'brasileirao-serie-a':
            logger.info("📊 [API] Buscando dados da Série A...")
            classificacao = classificacao_db.get_classificacao_serie_a()
            logger.info(f"📋 [API] Série A retornou {len(classificacao)} registros")
        elif campeonato == 'serie-b':
            logger.info("📊 [API] Buscando dados da Série B...")
            
            # FORÇAR nova instância para debug
            from models.classificacao_db import ClassificacaoDB
            db_fresh = ClassificacaoDB()
            
            # Teste direto no banco
            import sqlite3
            conn = sqlite3.connect("models/tabelas_classificacao.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM classificacao_serie_b")
            count = cursor.fetchone()['total']
            logger.info(f"🔍 [API] Contagem direta: {count}")
            
            cursor.execute("""
                SELECT id, posicao, time, pontos, jogos, vitorias, empates, derrotas,
                       gols_pro, gols_contra, saldo_gols, aproveitamento,
                       ultimos_jogos, zona, created_at, updated_at
                FROM classificacao_serie_b 
                ORDER BY posicao ASC
            """)
            
            rows = cursor.fetchall()
            classificacao = [dict(row) for row in rows]
            
            logger.info(f"📋 [API] Query direta retornou: {len(classificacao)} registros")
            
            if classificacao:
                logger.info(f"🏆 [API] Primeiro time: {classificacao[0]['time']}")
            
            conn.close()
        elif campeonato == 'premier-league':
            logger.info("📊 [API] Buscando dados da Premier League...")
            classificacao = classificacao_db.get_classificacao_premier_league()
            logger.info(f"📋 [API] Premier League retornou {len(classificacao)} registros")
        elif campeonato == 'la-liga':
            logger.info("📊 [API] Buscando dados da La Liga...")
            classificacao = classificacao_db.get_classificacao_la_liga()
            logger.info(f"📋 [API] La Liga retornou {len(classificacao)} registros")
        elif campeonato == 'ligue1':
            logger.info("📊 [API] Buscando dados da Ligue 1...")
            classificacao = classificacao_db.get_classificacao_frances()
            logger.info(f"📋 [API] Ligue 1 retornou {len(classificacao)} registros")
        elif campeonato == 'champions-league':
            logger.info("📊 [API] Buscando dados da Champions League...")
            classificacao = classificacao_db.get_classificacao_champions_league()
            logger.info(f"📋 [API] Champions League retornou {len(classificacao)} registros")
        else:
            logger.warning(f"❌ [API] Campeonato inválido: {campeonato}")
            return jsonify({
                'success': False,
                'message': 'Campeonato inválido'
            }), 400
        
        if classificacao:
            logger.info(f"🏆 [API] Primeiro time: {classificacao[0]}")
        
        response_data = {
            'success': True,
            'classificacao': classificacao,
            'campeonato': campeonato,
            'total': len(classificacao)
        }
        
        logger.info(f"📤 [API] Retornando: success={response_data['success']}, total={response_data['total']}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"💥 [API] Erro ao carregar classificação: {e}")
        import traceback
        logger.error(f"📄 [API] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar classificação: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/classificacao/salvar', methods=['POST'])
@cross_origin()
def salvar_classificacao():
    """Salvar alterações na classificação"""
    data = request.get_json()
    
    if not verificar_auth(data):
        return jsonify({
            'success': False,
            'message': 'Acesso negado'
        }), 401
    
    try:
        updates = data.get('updates', [])
        campeonato = data.get('campeonato', 'serie-a')  # Detectar série
        
        # Determinar série baseada no campeonato
        if campeonato == 'serie-b':
            serie = 'b'
        elif campeonato == 'premier-league':
            serie = 'premier'
        elif campeonato == 'la-liga':
            serie = 'laliga'
        elif campeonato == 'ligue1':
            serie = 'ligue1'
        else:
            serie = 'a'
        
        sucesso = 0
        erros = 0
        
        if serie == 'premier':
            campeonato_nome = "Premier League"
        elif serie == 'laliga':
            campeonato_nome = "La Liga"
        elif serie == 'ligue1':
            campeonato_nome = "Ligue 1"
        else:
            campeonato_nome = f"Série {serie.upper()}"
        logger.info(f"💾 [API] Salvando {len(updates)} alterações no {campeonato_nome}")
        
        for update in updates:
            time_id = update.get('id')
            campo = update.get('field')
            valor = update.get('value')
            
            logger.info(f"📝 [API] Atualizando ID {time_id}: {campo} = {valor}")
            
            if classificacao_db.update_time_stats(time_id, campo, valor, serie):
                sucesso += 1
                logger.info(f"✅ [API] Sucesso: {campo} atualizado")
            else:
                erros += 1
                logger.error(f"❌ [API] Erro ao atualizar {campo}")
        
        return jsonify({
            'success': True,
            'message': f'Classificação atualizada: {sucesso} sucessos, {erros} erros',
            'sucessos': sucesso,
            'erros': erros
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar classificação: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar classificação: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/classificacao/info', methods=['GET'])
@cross_origin()
def get_classificacao_info():
    """Obter informações sobre as tabelas de classificação"""
    try:
        info = classificacao_db.get_tables_info()
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter info classificação: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao obter informações: {str(e)}'
        }), 500

# === ROTAS PARA JOGOS DOS CLUBES ===

@bp_admin.route('/api/admin/jogos/<clube>', methods=['GET'])
@cross_origin()
def get_jogos_clube(clube):
    """Obter jogos de um clube específico"""
    try:
        jogos = jogos_manager.carregar_jogos(clube)
        estatisticas = jogos_manager.calcular_estatisticas(clube)
        
        return jsonify({
            'success': True,
            'data': {
                'jogos': jogos,
                'estatisticas': estatisticas,
                'clube': clube
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter jogos de {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/jogos/<clube>', methods=['POST'])
@cross_origin()
def adicionar_jogo_clube(clube):
    """Adicionar novo jogo para um clube"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['data', 'time_casa', 'gols_casa', 'gols_visitante', 
                          'time_visitante', 'local', 'resultado', 'pontos']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório ausente: {field}'
                }), 400
        
        # Adicionar jogo
        success = jogos_manager.adicionar_jogo(clube, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Jogo adicionado com sucesso para {clube}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao adicionar jogo'
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao adicionar jogo para {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/jogos/<clube>/<int:index>', methods=['PUT'])
@cross_origin()
def atualizar_jogo_clube(clube, index):
    """Atualizar jogo específico de um clube"""
    try:
        data = request.get_json()
        
        success = jogos_manager.atualizar_jogo(clube, index, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Jogo atualizado com sucesso para {clube}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao atualizar jogo ou índice inválido'
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar jogo de {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/jogos/<clube>/<int:index>', methods=['DELETE'])
@cross_origin()
def remover_jogo_clube(clube, index):
    """Remover jogo específico de um clube"""
    try:
        success = jogos_manager.remover_jogo(clube, index)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Jogo removido com sucesso de {clube}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao remover jogo ou índice inválido'
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao remover jogo de {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/jogos', methods=['GET'])
@cross_origin()
def listar_clubes_com_jogos():
    """Listar todos os clubes que têm jogos salvos"""
    try:
        clubes = jogos_manager.listar_clubes_com_jogos()
        
        return jsonify({
            'success': True,
            'data': {
                'clubes': clubes,
                'total': len(clubes)
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar clubes com jogos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/estatisticas-jogos/<clube>', methods=['GET'])
@cross_origin()
def get_estatisticas_jogos_clube(clube):
    """Obter estatísticas calculadas dos jogos de um clube para o dashboard"""
    try:
        estatisticas = jogos_manager.calcular_estatisticas(clube)
        
        return jsonify({
            'success': True,
            'data': estatisticas,
            'clube': clube
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de jogos de {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/estatisticas-editaveis', methods=['POST'])
@cross_origin()
def salvar_estatisticas_editaveis():
    """Salvar estatísticas editáveis de um clube"""
    try:
        data = request.get_json()
        admin_key = data.get('admin_key')
        dados = data.get('dados')
        
        if not admin_key or admin_key != ADMIN_KEY:
            return jsonify({
                'success': False,
                'error': 'Chave de administrador inválida'
            }), 401
            
        if not dados or not dados.get('clube'):
            return jsonify({
                'success': False,
                'error': 'Dados inválidos'
            }), 400
        
        # Salvar em arquivo JSON
        import os
        import json
        
        dados_dir = "backend/models/estatisticas_editaveis"
        os.makedirs(dados_dir, exist_ok=True)
        
        clube_nome = dados['clube'].lower().replace(' ', '_')
        arquivo_path = os.path.join(dados_dir, f"{clube_nome}.json")
        
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Estatísticas editáveis de {dados["clube"]} salvas com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar estatísticas editáveis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp_admin.route('/api/admin/estatisticas-editaveis/<clube>', methods=['GET'])
@cross_origin()
def carregar_estatisticas_editaveis(clube):
    """Carregar estatísticas editáveis salvas de um clube"""
    try:
        import os
        import json
        
        dados_dir = "backend/models/estatisticas_editaveis"
        clube_nome = clube.lower().replace(' ', '_')
        arquivo_path = os.path.join(dados_dir, f"{clube_nome}.json")
        
        if not os.path.exists(arquivo_path):
            return jsonify({
                'success': True,
                'data': None,
                'message': 'Nenhum dado editável salvo para este clube'
            })
        
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        return jsonify({
            'success': True,
            'data': dados
        })
        
    except Exception as e:
        logger.error(f"Erro ao carregar estatísticas editáveis de {clube}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS PARA CONCURSOS DA LOTECA ===

@bp_admin.route('/api/admin/loteca/concursos', methods=['GET'])
@cross_origin()
def listar_concursos():
    """Listar todos os concursos disponíveis"""
    logger.info("📋 [LOTECA] Listando concursos...")
    
    try:
        concursos = concurso_manager.listar_concursos()
        
        return jsonify({
            'success': True,
            'concursos': concursos,
            'total': len(concursos)
        }), 200
        
    except Exception as e:
        logger.error(f"💥 [LOTECA] Erro ao listar concursos: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao listar concursos: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/loteca/concurso/<numero>', methods=['GET'])
@cross_origin()
def carregar_concurso(numero):
    """Carregar um concurso específico"""
    logger.info(f"📂 [LOTECA] Carregando concurso {numero}...")
    
    try:
        dados = concurso_manager.carregar_concurso(numero)
        
        if not dados:
            return jsonify({
                'success': False,
                'message': f'Concurso {numero} não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'concurso': dados
        }), 200
        
    except Exception as e:
        logger.error(f"💥 [LOTECA] Erro ao carregar concurso {numero}: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar concurso: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/loteca/concurso', methods=['POST'])
@cross_origin()
def salvar_concurso():
    """Salvar um concurso"""
    logger.info("💾 [LOTECA] Salvando concurso...")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        numero = data.get('numero')
        if not numero:
            return jsonify({
                'success': False,
                'message': 'Número do concurso não fornecido'
            }), 400
        
        # Salvar concurso
        sucesso = concurso_manager.salvar_concurso(numero, data)
        
        if sucesso:
            return jsonify({
                'success': True,
                'message': f'Concurso {numero} salvo com sucesso!',
                'numero': numero
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Erro ao salvar concurso'
            }), 500
        
    except Exception as e:
        logger.error(f"💥 [LOTECA] Erro ao salvar concurso: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar concurso: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/loteca/ultimo', methods=['GET'])
@cross_origin()
def get_ultimo_concurso():
    """Obter o último concurso"""
    logger.info("🔍 [LOTECA] Buscando último concurso...")
    
    try:
        dados = concurso_manager.get_ultimo_concurso()
        
        if not dados:
            return jsonify({
                'success': False,
                'message': 'Nenhum concurso encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'concurso': dados
        }), 200
        
    except Exception as e:
        logger.error(f"💥 [LOTECA] Erro ao buscar último concurso: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar último concurso: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/loteca/proximo-numero', methods=['GET'])
@cross_origin()
def get_proximo_numero():
    """Obter o próximo número de concurso"""
    logger.info("🔢 [LOTECA] Calculando próximo número...")
    
    try:
        proximo = concurso_manager.get_proximo_numero()
        
        return jsonify({
            'success': True,
            'proximo_numero': proximo
        }), 200
        
    except Exception as e:
        logger.error(f"💥 [LOTECA] Erro ao calcular próximo número: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao calcular próximo número: {str(e)}'
        }), 500

@bp_admin.route('/api/admin/atualizar-ultimos-confrontos', methods=['POST'])
@cross_origin()
def atualizar_ultimos_confrontos():
    """Atualizar últimos confrontos usando arquivos JSON"""
    logger.info("🔄 [JSON-UPDATE] Iniciando atualização via arquivos JSON...")
    
    try:
        # Verificar autenticação
        request_data = request.get_json() or {}
        if not verificar_auth(request_data):
            return jsonify({
                'success': False,
                'message': 'Acesso negado. Chave de administrador inválida.'
            }), 401
        
        # Importar o leitor de JSON
        from ler_ultimos_cinco import ler_ultimos_cinco_serie_a, ler_ultimos_cinco_serie_b
        
        # Ler dados dos arquivos JSON
        serie_a_data = ler_ultimos_cinco_serie_a()
        serie_b_data = ler_ultimos_cinco_serie_b()
        
        logger.info(f"📊 [JSON-UPDATE] Série A: {len(serie_a_data)} times")
        logger.info(f"📊 [JSON-UPDATE] Série B: {len(serie_b_data)} times")
        
        # Atualizar banco de dados
        from models.classificacao_db import ClassificacaoDB
        db = ClassificacaoDB()
        
        # Atualizar Série A
        updated_a = 0
        for time_nome, ultimos in serie_a_data.items():
            # Normalizar nome do time para o banco
            time_banco = time_nome.replace('-', ' ').title()
            if time_banco == 'Sao Paulo':
                time_banco = 'São Paulo'
            elif time_banco == 'Red Bull Bragantino':
                time_banco = 'Bragantino'
            elif time_banco == 'Sport Recife':
                time_banco = 'Sport'
            
            # Atualizar no banco
            success = db.atualizar_ultimos_confrontos_serie_a(time_banco, ultimos)
            if success:
                updated_a += 1
                logger.info(f"✅ [JSON-UPDATE] {time_banco}: {ultimos}")
        
        # Atualizar Série B
        updated_b = 0
        for time_nome, ultimos in serie_b_data.items():
            # Normalizar nome do time para o banco
            time_banco = time_nome.replace('-', ' ').title()
            if time_banco == 'Athletico Pr':
                time_banco = 'Athletico-PR'
            elif time_banco == 'America Mg':
                time_banco = 'América-MG'
            elif time_banco == 'Athletic Mg':
                time_banco = 'Athletic'
            elif time_banco == 'Botafogo Sp':
                time_banco = 'Botafogo SP'
            elif time_banco == 'Amazonas Fc':
                time_banco = 'Amazonas FC'
            elif time_banco == 'Volta Redonda':
                time_banco = 'Volta Redonda'
            
            # Atualizar no banco
            success = db.atualizar_ultimos_confrontos_serie_b(time_banco, ultimos)
            if success:
                updated_b += 1
                logger.info(f"✅ [JSON-UPDATE] {time_banco}: {ultimos}")
        
        logger.info(f"✅ [JSON-UPDATE] Atualização concluída! A: {updated_a}, B: {updated_b}")
        
        return jsonify({
            'success': True,
            'message': f'Últimos confrontos atualizados com sucesso! Série A: {updated_a} times, Série B: {updated_b} times',
            'updated_at': datetime.now().isoformat(),
            'serie_a_updated': updated_a,
            'serie_b_updated': updated_b
        }), 200
            
    except Exception as e:
        logger.error(f"💥 [JSON-UPDATE] Erro geral: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar últimos confrontos: {str(e)}'
        }), 500

# Blueprint integrado ao app principal
# Acesse via: http://localhost:5000/admin
