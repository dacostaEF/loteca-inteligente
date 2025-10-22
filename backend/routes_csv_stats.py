#!/usr/bin/env python3
"""
API para servir dados estatísticos do CSV
Integração com a aba "Dados Avançados"
"""

import os
import csv
import json
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

# Blueprint para rotas de estatísticas CSV
csv_stats_bp = Blueprint('csv_stats', __name__)

def load_csv_data():
    """Carregar dados do CSV de estatísticas da Série A"""
    try:
        csv_path = os.path.join('backend', 'estatistica', 'Seria_A_estatisticas_apostas.csv')
        
        if not os.path.exists(csv_path):
            return None
            
        data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Limpar e converter dados
                cleaned_row = {}
                for key, value in row.items():
                    # Remover aspas e espaços extras
                    cleaned_value = value.strip().strip('"')
                    
                    # Converter números
                    if key in ['Posição', 'Jogos', 'Gols Pró', 'Gols Contra', 'Jogos Casa', 
                              'Vitórias Casa', 'Empates Casa', 'Derrotas Casa', 'Gols Pró Casa',
                              'Gols Contra Casa', 'Jogos Fora', 'Vitórias Fora', 'Empates Fora',
                              'Derrotas Fora', 'Gols Pró Fora', 'Gols Contra Fora', 'Pontos Últimos 5']:
                        try:
                            cleaned_row[key] = int(cleaned_value) if cleaned_value else 0
                        except ValueError:
                            cleaned_row[key] = 0
                    
                    # Converter decimais
                    elif key in ['Média Gols Pró', 'Média Gols Contra']:
                        try:
                            cleaned_row[key] = float(cleaned_value) if cleaned_value else 0.0
                        except ValueError:
                            cleaned_row[key] = 0.0
                    
                    # Converter percentuais
                    elif '%' in key:
                        try:
                            cleaned_row[key] = int(cleaned_value) if cleaned_value else 0
                        except ValueError:
                            cleaned_row[key] = 0
                    
                    # Manter strings
                    else:
                        cleaned_row[key] = cleaned_value
                
                data.append(cleaned_row)
        
        return data
        
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return None

@csv_stats_bp.route('/api/csv/serie-a/stats', methods=['GET'])
@cross_origin()
def get_serie_a_stats():
    """Endpoint para obter estatísticas da Série A do CSV"""
    try:
        print("🔍 [CSV-API] Tentando carregar dados do CSV...")
        data = load_csv_data()
        
        if not data:
            print("❌ [CSV-API] Dados não encontrados")
            return jsonify({
                "success": False,
                "error": "Dados não encontrados",
                "data": []
            }), 404
        
        print(f"✅ [CSV-API] {len(data)} times carregados com sucesso")
        return jsonify({
            "success": True,
            "data": data,
            "total": len(data),
            "source": "CSV - Seria_A_estatisticas_apostas.csv"
        })
        
    except Exception as e:
        print(f"❌ [CSV-API] Erro: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erro ao carregar dados: {str(e)}"
        }), 500

@csv_stats_bp.route('/api/csv/test', methods=['GET'])
@cross_origin()
def test_csv_api():
    """Endpoint de teste para verificar se a API está funcionando"""
    return jsonify({
        "success": True,
        "message": "API CSV funcionando!",
        "timestamp": "2025-10-22"
    })

@csv_stats_bp.route('/api/csv/serie-a/team/<team_name>', methods=['GET'])
@cross_origin()
def get_team_stats(team_name):
    """Endpoint para obter estatísticas de um time específico"""
    try:
        data = load_csv_data()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Dados não encontrados"
            }), 404
        
        # Buscar time com diferentes estratégias
        team_data = None
        search_name = team_name.lower().strip()
        
        # Estratégia 1: Busca exata
        for team in data:
            if team['Time'].lower() == search_name:
                team_data = team
                break
        
        # Estratégia 2: Busca parcial (contém)
        if not team_data:
            for team in data:
                if search_name in team['Time'].lower() or team['Time'].lower() in search_name:
                    team_data = team
                    break
        
        # Estratégia 3: Busca por palavras-chave comuns
        if not team_data:
            # Mapear nomes comuns
            name_mappings = {
                'flamengo': 'Flamengo',
                'palmeiras': 'Palmeiras',
                'corinthians': 'Corinthians',
                'sao paulo': 'Sao Paulo',
                'santos': 'Santos',
                'cruzeiro': 'Cruzeiro',
                'atletico mg': 'Atletico Mg',
                'atletico-mg': 'Atletico Mg',
                'botafogo': 'Botafogo',
                'fluminense': 'Fluminense',
                'vasco': 'Vasco',
                'bahia': 'Bahia',
                'gremio': 'Gremio',
                'internacional': 'Internacional',
                'fortaleza': 'Fortaleza',
                'ceara': 'Ceara',
                'athletico': 'Athletico',
                'bragantino': 'Red Bull Bragantino',
                'red bull': 'Red Bull Bragantino',
                'mirassol': 'Mirassol',
                'vitoria': 'Vitoria',
                'juventude': 'Juventude',
                'sport': 'Sport Recife',
                'sport recife': 'Sport Recife'
            }
            
            for key, value in name_mappings.items():
                if key in search_name:
                    for team in data:
                        if team['Time'] == value:
                            team_data = team
                            break
                    if team_data:
                        break
        
        if not team_data:
            return jsonify({
                "success": False,
                "error": f"Time '{team_name}' não encontrado",
                "available_teams": [team['Time'] for team in data[:5]]  # Mostrar primeiros 5 times
            }), 404
        
        return jsonify({
            "success": True,
            "data": team_data,
            "team": team_name,
            "found_as": team_data['Time']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao buscar time: {str(e)}"
        }), 500

@csv_stats_bp.route('/api/csv/serie-a/compare', methods=['POST'])
@cross_origin()
def compare_teams():
    """Endpoint para comparar dois times"""
    try:
        data = request.get_json()
        team1 = data.get('team1')
        team2 = data.get('team2')
        
        if not team1 or not team2:
            return jsonify({
                "success": False,
                "error": "Nomes dos times são obrigatórios"
            }), 400
        
        csv_data = load_csv_data()
        
        if not csv_data:
            return jsonify({
                "success": False,
                "error": "Dados não encontrados"
            }), 404
        
        # Buscar ambos os times
        team1_data = None
        team2_data = None
        
        for team in csv_data:
            if team['Time'].lower() == team1.lower():
                team1_data = team
            elif team['Time'].lower() == team2.lower():
                team2_data = team
        
        if not team1_data:
            return jsonify({
                "success": False,
                "error": f"Time '{team1}' não encontrado"
            }), 404
            
        if not team2_data:
            return jsonify({
                "success": False,
                "error": f"Time '{team2}' não encontrado"
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "team1": team1_data,
                "team2": team2_data,
                "comparison": {
                    "position_diff": team1_data['Posição'] - team2_data['Posição'],
                    "points_diff": team1_data.get('Pontos Últimos 5', 0) - team2_data.get('Pontos Últimos 5', 0),
                    "goals_avg_diff": team1_data['Média Gols Pró'] - team2_data['Média Gols Pró'],
                    "goals_against_avg_diff": team1_data['Média Gols Contra'] - team2_data['Média Gols Contra']
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro na comparação: {str(e)}"
        }), 500
