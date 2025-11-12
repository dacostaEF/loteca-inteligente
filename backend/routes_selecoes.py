"""
API para Seleções Nacionais
Autor: Loteca X-Ray
Data: 2025-01-12

Fornece dados de valor de mercado e estatísticas das seleções nacionais
"""

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import csv
import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Criar Blueprint
bp_selecoes = Blueprint('selecoes', __name__, url_prefix='/api/selecoes')

# Cache para dados das seleções
_cache_selecoes = None

def calcular_categoria_elenco(valor_mm: float) -> str:
    """
    Calcula CATEGORIA do elenco baseada no valor total em MM Euros
    ✅ SISTEMA DE CATEGORIAS PROFISSIONAL (A+, A, B, C, D)
    
    A+ → SUPERPOTÊNCIAS       (>€800MM)   | Inglaterra, França, Real Madrid
    A  → ELITE                (€300-800MM) | Brasil, Argentina, Bayern
    B  → COMPETITIVOS         (€100-300MM) | Flamengo, Palmeiras, Uruguai
    C  → EM DESENVOLVIMENTO   (€30-100MM)  | Japão, Fortaleza, Bósnia
    D  → BASES SÓLIDAS        (<€30MM)     | Letônia, Série B baixa
    """
    if valor_mm >= 800:
        return 'A+'
    elif valor_mm >= 300:
        return 'A'
    elif valor_mm >= 100:
        return 'B'
    elif valor_mm >= 30:
        return 'C'
    else:
        return 'D'

def carregar_dados_selecoes() -> List[Dict]:
    """
    Carrega dados das seleções do CSV
    """
    global _cache_selecoes
    
    if _cache_selecoes is not None:
        return _cache_selecoes
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'models', 'EstatisticasElenco', 'Valor_Elenco_Selecoes_mundo.csv')
        
        if not os.path.exists(csv_path):
            logger.error(f"❌ Arquivo CSV não encontrado: {csv_path}")
            return []
        
        selecoes = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                valor_mm = float(row['Valor_Mercado_Milhoes'])
                categoria = calcular_categoria_elenco(valor_mm)
                
                selecoes.append({
                    'posicao': int(row['Posicao']),
                    'selecao': row['Selecao'],
                    'valor_mercado_milhoes': valor_mm,
                    'valor_mercado_texto': row['Valor_Mercado_Texto'],
                    'continente': row['Continente'],
                    'confederacao': row['Confederacao'],
                    'categoria': categoria  # ✅ NOVO: Categoria A+/A/B/C/D
                })
        
        _cache_selecoes = selecoes
        logger.info(f"✅ Carregadas {len(selecoes)} seleções do CSV")
        return selecoes
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados das seleções: {e}")
        return []


def normalizar_nome_selecao(nome: str) -> str:
    """
    Normaliza o nome da seleção para comparação
    """
    if not nome:
        return ''
    
    # Mapeamento de nomes alternativos
    mapeamento = {
        'bosnia': 'Bósnia e Herzegovina',
        'bosnia herzegovina': 'Bósnia e Herzegovina',
        'bosnia herzegovin': 'Bósnia e Herzegovina',
        'bosnia-herzegovina': 'Bósnia e Herzegovina',
        'bosnia and herzegovina': 'Bósnia e Herzegovina',
        'romenia': 'Romênia',
        'romania': 'Romênia',
        'suica': 'Suíça',
        'switzerland': 'Suíça',
        'suecia': 'Suécia',
        'sweden': 'Suécia',
        'grecia': 'Grécia',
        'greece': 'Grécia',
        'escocia': 'Escócia',
        'scotland': 'Escócia',
        'hungria': 'Hungria',
        'hungary': 'Hungria',
        'irlanda': 'Irlanda',
        'ireland': 'Irlanda',
        'albania': 'Albânia',
        'inglaterra': 'Inglaterra',
        'england': 'Inglaterra',
        'servia': 'Sérvia',
        'serbia': 'Sérvia',
        'letonia': 'Letônia',
        'latvia': 'Letônia',
        'italia': 'Itália',
        'italy': 'Itália',
        'noruega': 'Noruega',
        'norway': 'Noruega',
        'ucrania': 'Ucrânia',
        'ukraine': 'Ucrânia',
        'islandia': 'Islândia',
        'iceland': 'Islândia'
    }
    
    # Normalizar entrada
    nome_norm = nome.lower().strip()
    
    # Tentar mapear
    if nome_norm in mapeamento:
        return mapeamento[nome_norm]
    
    # Retornar capitalizado
    return nome.strip().title()


@bp_selecoes.route('/todas', methods=['GET'])
@cross_origin()
def listar_todas_selecoes():
    """
    Lista todas as seleções disponíveis
    GET /api/selecoes/todas
    
    Response:
    {
        "success": true,
        "total": 53,
        "selecoes": [...]
    }
    """
    try:
        selecoes = carregar_dados_selecoes()
        
        return jsonify({
            "success": True,
            "total": len(selecoes),
            "selecoes": selecoes,
            "fonte": "Transfermarkt 2025"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar seleções: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "selecoes": []
        }), 500


@bp_selecoes.route('/buscar/<nome>', methods=['GET'])
@cross_origin()
def buscar_selecao(nome: str):
    """
    Busca dados de uma seleção específica
    GET /api/selecoes/buscar/<nome>
    
    Exemplo: /api/selecoes/buscar/Brasil
    
    Response:
    {
        "success": true,
        "selecao": {...}
    }
    """
    try:
        selecoes = carregar_dados_selecoes()
        
        # Normalizar nome buscado
        nome_normalizado = normalizar_nome_selecao(nome)
        
        # Buscar por nome exato (case insensitive)
        for selecao in selecoes:
            if selecao['selecao'].lower() == nome_normalizado.lower():
                return jsonify({
                    "success": True,
                    "selecao": selecao,
                    "fonte": "Transfermarkt 2025"
                })
        
        # Buscar por substring
        for selecao in selecoes:
            if nome_normalizado.lower() in selecao['selecao'].lower():
                return jsonify({
                    "success": True,
                    "selecao": selecao,
                    "fonte": "Transfermarkt 2025",
                    "nota": "Match por substring"
                })
        
        return jsonify({
            "success": False,
            "error": f"Seleção '{nome}' não encontrada",
            "selecao": None
        }), 404
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar seleção '{nome}': {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "selecao": None
        }), 500


@bp_selecoes.route('/comparar', methods=['POST'])
@cross_origin()
def comparar_selecoes():
    """
    Compara duas seleções
    POST /api/selecoes/comparar
    
    Body:
    {
        "time_casa": "Brasil",
        "time_fora": "Argentina"
    }
    
    Response:
    {
        "success": true,
        "time_casa": {...},
        "time_fora": {...},
        "comparacao": {
            "diferenca_valor": 160.1,
            "diferenca_percentual": 20.5,
            "favorito": "Brasil",
            "vantagem": "Moderada"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'time_casa' not in data or 'time_fora' not in data:
            return jsonify({
                "success": False,
                "error": "Parâmetros 'time_casa' e 'time_fora' são obrigatórios"
            }), 400
        
        selecoes = carregar_dados_selecoes()
        
        # Normalizar nomes
        nome_casa = normalizar_nome_selecao(data['time_casa'])
        nome_fora = normalizar_nome_selecao(data['time_fora'])
        
        # Buscar seleções
        selecao_casa = None
        selecao_fora = None
        
        for selecao in selecoes:
            if selecao['selecao'].lower() == nome_casa.lower():
                selecao_casa = selecao
            if selecao['selecao'].lower() == nome_fora.lower():
                selecao_fora = selecao
        
        if not selecao_casa or not selecao_fora:
            return jsonify({
                "success": False,
                "error": f"Uma ou ambas as seleções não foram encontradas",
                "time_casa_encontrado": selecao_casa is not None,
                "time_fora_encontrado": selecao_fora is not None
            }), 404
        
        # Calcular comparação
        valor_casa = selecao_casa['valor_mercado_milhoes']
        valor_fora = selecao_fora['valor_mercado_milhoes']
        
        diferenca = abs(valor_casa - valor_fora)
        diferenca_pct = (diferenca / max(valor_casa, valor_fora)) * 100
        
        favorito = selecao_casa['selecao'] if valor_casa > valor_fora else selecao_fora['selecao']
        
        # Classificar vantagem
        if diferenca_pct < 10:
            vantagem = "Muito Equilibrado"
        elif diferenca_pct < 25:
            vantagem = "Ligeira Vantagem"
        elif diferenca_pct < 50:
            vantagem = "Vantagem Moderada"
        elif diferenca_pct < 100:
            vantagem = "Grande Vantagem"
        else:
            vantagem = "Vantagem Esmagadora"
        
        return jsonify({
            "success": True,
            "time_casa": selecao_casa,
            "time_fora": selecao_fora,
            "comparacao": {
                "diferenca_valor_milhoes": round(diferenca, 2),
                "diferenca_percentual": round(diferenca_pct, 2),
                "favorito": favorito,
                "vantagem": vantagem,
                "valor_casa": valor_casa,
                "valor_fora": valor_fora
            },
            "fonte": "Transfermarkt 2025"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao comparar seleções: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@bp_selecoes.route('/top/<int:limite>', methods=['GET'])
@cross_origin()
def top_selecoes(limite: int = 10):
    """
    Retorna as top N seleções mais valiosas
    GET /api/selecoes/top/<limite>
    
    Exemplo: /api/selecoes/top/10
    
    Response:
    {
        "success": true,
        "total": 10,
        "selecoes": [...]
    }
    """
    try:
        selecoes = carregar_dados_selecoes()
        
        # Limitar resultado
        top = selecoes[:min(limite, len(selecoes))]
        
        return jsonify({
            "success": True,
            "total": len(top),
            "limite_solicitado": limite,
            "selecoes": top,
            "fonte": "Transfermarkt 2025"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar top seleções: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "selecoes": []
        }), 500


@bp_selecoes.route('/por-confederacao/<confederacao>', methods=['GET'])
@cross_origin()
def selecoes_por_confederacao(confederacao: str):
    """
    Lista seleções de uma confederação específica
    GET /api/selecoes/por-confederacao/<confederacao>
    
    Confederações: UEFA, CONMEBOL, CONCACAF, CAF, AFC, OFC
    
    Response:
    {
        "success": true,
        "confederacao": "UEFA",
        "total": 35,
        "selecoes": [...]
    }
    """
    try:
        selecoes = carregar_dados_selecoes()
        
        # Filtrar por confederação
        filtradas = [s for s in selecoes if s['confederacao'].upper() == confederacao.upper()]
        
        return jsonify({
            "success": True,
            "confederacao": confederacao.upper(),
            "total": len(filtradas),
            "selecoes": filtradas,
            "fonte": "Transfermarkt 2025"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar seleções da confederação '{confederacao}': {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "selecoes": []
        }), 500

