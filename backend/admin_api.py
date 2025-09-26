#!/usr/bin/env python3
"""
API Backend para Interface Administrativa
Conecta a interface HTML com a Central de Dados SQLite
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
from models.central_dados import CentralDados

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurações
ADMIN_KEY = 'loteca2024admin'  # Chave de administrador
central_dados = CentralDados()

def verificar_auth(request_data):
    """Verificar autenticação do administrador"""
    auth_key = request_data.get('admin_key') or request.headers.get('X-Admin-Key')
    return auth_key == ADMIN_KEY

@app.route('/admin')
def admin_interface():
    """Servir a interface administrativa"""
    try:
        with open('admin_interface.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        logger.error(f"Erro ao servir interface admin: {e}")
        return f"Erro ao carregar interface: {e}", 500

@app.route('/api/admin/auth', methods=['POST'])
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

@app.route('/api/admin/dashboard', methods=['GET'])
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

@app.route('/api/admin/clubes', methods=['GET'])
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

@app.route('/api/admin/clubes', methods=['POST'])
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

@app.route('/api/admin/clubes/<int:clube_id>', methods=['DELETE'])
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

@app.route('/api/admin/estatisticas', methods=['GET'])
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

@app.route('/api/admin/estatisticas', methods=['POST'])
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

@app.route('/api/admin/estatisticas/<int:clube_id>', methods=['DELETE'])
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

@app.route('/api/admin/backup', methods=['GET'])
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

@app.route('/api/admin/restore', methods=['POST'])
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

if __name__ == '__main__':
    print("🚀 Iniciando API Admin do Loteca X-Ray...")
    print(f"🔐 Chave de administrador: {ADMIN_KEY}")
    print("🌐 Interface disponível em: http://127.0.0.1:5001/admin")
    
    app.run(debug=True, port=5001, host='0.0.0.0')
