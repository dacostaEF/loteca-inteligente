#!/usr/bin/env python3
"""
Rotas para Automação de Classificação
API endpoints para atualização automática das tabelas
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
import os
import sys

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.classificacao_integrador import ClassificacaoIntegrador
from services.auto_classificacao import AutoClassificacao
from services.auto_monitor import get_monitor_status, force_auto_update, start_auto_monitoring, stop_auto_monitoring

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar blueprint
bp_auto = Blueprint('auto_classificacao', __name__)

@bp_auto.route('/api/auto/classificacao/atualizar', methods=['POST'])
@cross_origin()
def atualizar_classificacao_automatica():
    """
    Atualiza Série A e B automaticamente lendo os CSVs
    POST /api/auto/classificacao/atualizar
    """
    try:
        logger.info("🔄 Iniciando atualização automática via API...")
        
        # Executar atualização automática
        integrador = ClassificacaoIntegrador()
        resultado = integrador.atualizar_todas_series()
        
        # Preparar resposta
        response = {
            'success': True,
            'message': 'Atualização automática executada',
            'resultado': resultado,
            'timestamp': resultado['timestamp']
        }
        
        # Adicionar estatísticas
        if resultado['serie_a'] and resultado['serie_b']:
            response['status'] = 'completo'
            response['message'] = 'Série A e B atualizadas com sucesso'
        elif resultado['serie_a'] or resultado['serie_b']:
            response['status'] = 'parcial'
            response['message'] = 'Apenas algumas séries foram atualizadas'
        else:
            response['status'] = 'erro'
            response['message'] = 'Falha na atualização das séries'
        
        logger.info(f"✅ Atualização concluída: {response['status']}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Erro na atualização automática: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro na atualização automática: {str(e)}',
            'status': 'erro'
        }), 500

@bp_auto.route('/api/auto/classificacao/status', methods=['GET'])
@cross_origin()
def status_classificacao():
    """
    Verifica o status das tabelas de classificação
    GET /api/auto/classificacao/status
    """
    try:
        from models.classificacao_db import ClassificacaoDB
        
        db = ClassificacaoDB()
        
        # Verificar Série A
        serie_a = db.get_classificacao_serie_a()
        
        # Verificar Série B
        serie_b = db.get_classificacao_serie_b()
        
        # Verificar se há dados dos CSVs
        auto_class = AutoClassificacao()
        
        # Contar CSVs disponíveis
        csvs_serie_a = 0
        csvs_serie_b = 0
        
        if os.path.exists(auto_class.serie_a_path):
            csvs_serie_a = len([f for f in os.listdir(auto_class.serie_a_path) 
                               if os.path.isdir(os.path.join(auto_class.serie_a_path, f))])
        
        if os.path.exists(auto_class.serie_b_path):
            csvs_serie_b = len([f for f in os.listdir(auto_class.serie_b_path) 
                               if os.path.isdir(os.path.join(auto_class.serie_b_path, f))])
        
        return jsonify({
            'success': True,
            'status': {
                'serie_a': {
                    'banco_registros': len(serie_a),
                    'csvs_disponiveis': csvs_serie_a,
                    'atualizado': len(serie_a) > 0
                },
                'serie_b': {
                    'banco_registros': len(serie_b),
                    'csvs_disponiveis': csvs_serie_b,
                    'atualizado': len(serie_b) > 0
                },
                'csvs_total': csvs_serie_a + csvs_serie_b
            }
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao verificar status: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/preview', methods=['GET'])
@cross_origin()
def preview_classificacao():
    """
    Preview dos dados que seriam gerados (sem salvar no banco)
    GET /api/auto/classificacao/preview
    """
    try:
        logger.info("👀 Gerando preview da classificação...")
        
        # Processar dados sem salvar
        auto_class = AutoClassificacao()
        resultado = auto_class.processar_todas_series()
        
        # Preparar preview
        preview = {
            'success': True,
            'message': 'Preview gerado com sucesso',
            'preview': {
                'serie_a': {
                    'total_clubes': len(resultado['serie_a']),
                    'top_5': resultado['serie_a'][:5],
                    'zonas': {
                        'libertadores': [c for c in resultado['serie_a'] if c['zona'] == 'Libertadores'],
                        'sul_americana': [c for c in resultado['serie_a'] if c['zona'] == 'Sul-Americana'],
                        'rebaixamento': [c for c in resultado['serie_a'] if c['zona'] == 'Zona de Rebaixamento']
                    }
                },
                'serie_b': {
                    'total_clubes': len(resultado['serie_b']),
                    'top_5': resultado['serie_b'][:5],
                    'zonas': {
                        'acesso': [c for c in resultado['serie_b'] if c['zona'] == 'Acesso'],
                        'rebaixamento': [c for c in resultado['serie_b'] if c['zona'] == 'Zona de Rebaixamento']
                    }
                }
            },
            'timestamp': resultado['timestamp']
        }
        
        logger.info("✅ Preview gerado com sucesso")
        return jsonify(preview), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar preview: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro ao gerar preview: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/forcar-atualizacao', methods=['POST'])
@cross_origin()
def forcar_atualizacao():
    """
    Força atualização mesmo se os dados já estiverem atualizados
    POST /api/auto/classificacao/forcar-atualizacao
    """
    try:
        logger.info("🔄 Forçando atualização automática...")
        
        # Executar atualização forçada
        integrador = ClassificacaoIntegrador()
        resultado = integrador.atualizar_todas_series()
        
        return jsonify({
            'success': True,
            'message': 'Atualização forçada executada com sucesso',
            'resultado': resultado,
            'forcado': True
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro na atualização forçada: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro na atualização forçada: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/monitor/status', methods=['GET'])
@cross_origin()
def monitor_status():
    """
    Verifica status do monitor automático
    GET /api/auto/classificacao/monitor/status
    """
    try:
        status = get_monitor_status()
        return jsonify({
            'success': True,
            'monitor': status
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao verificar status do monitor: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/monitor/start', methods=['POST'])
@cross_origin()
def start_monitor():
    """
    Inicia o monitor automático
    POST /api/auto/classificacao/monitor/start
    """
    try:
        start_auto_monitoring()
        return jsonify({
            'success': True,
            'message': 'Monitor automático iniciado com sucesso'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao iniciar monitor: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/monitor/stop', methods=['POST'])
@cross_origin()
def stop_monitor():
    """
    Para o monitor automático
    POST /api/auto/classificacao/monitor/stop
    """
    try:
        stop_auto_monitoring()
        return jsonify({
            'success': True,
            'message': 'Monitor automático parado com sucesso'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao parar monitor: {str(e)}'
        }), 500

@bp_auto.route('/api/auto/classificacao/monitor/force-update', methods=['POST'])
@cross_origin()
def force_monitor_update():
    """
    Força atualização imediata via monitor
    POST /api/auto/classificacao/monitor/force-update
    """
    try:
        force_auto_update()
        return jsonify({
            'success': True,
            'message': 'Atualização forçada executada com sucesso'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro na atualização forçada: {str(e)}'
        }), 500
