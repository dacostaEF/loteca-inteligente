import os
import time
import math
import requests
from typing import Dict, List, Optional, Any

# Configurações
API = "https://api.cartolafc.globo.com"
GLB_TOKEN = os.getenv("GLOBO_X_GLB_TOKEN")  # opcional (autenticado)
TIMEOUT = 10
_CACHE = {}

def _get(url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Função interna para fazer requisições HTTP com cache inteligente
    """
    key = ("GET", url, tuple(sorted((params or {}).items())))
    exp_val = _CACHE.get(key)
    
    # Verificar cache válido
    if exp_val and exp_val[0] > time.time():
        return exp_val[1]
    
    # Headers para autenticação (se disponível)
    headers = {"X-GLB-Token": GLB_TOKEN} if GLB_TOKEN else {}
    
    # Log sobre autenticação
    if GLB_TOKEN:
        print(f"[Cartola] ✅ Usando token de autenticação (dados completos)")
    else:
        print(f"[Cartola] ⚠️ SEM TOKEN - Dados podem estar limitados")
        print(f"[Cartola] 🔧 Configure GLOBO_X_GLB_TOKEN para dados completos")
    
    try:
        r = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        
        # Armazenar no cache (TTL 10 min)
        _CACHE[key] = (time.time() + 600, data)
        return data
        
    except requests.exceptions.RequestException as e:
        # Se temos cache expirado, usar como fallback
        if exp_val:
            print(f"[Cartola] Usando cache expirado como fallback para {url}")
            return exp_val[1]
        raise e

def clubes() -> Dict[int, Dict[str, Any]]:
    """
    Buscar todos os clubes do Cartola FC
    Retorna: { "1": {...}, "2": {...} } → mapeia p/ dict int->obj
    """
    try:
        data = _get(f"{API}/clubes")
        return {int(cid): info for cid, info in data.items()}
    except Exception as e:
        print(f"[Cartola] Erro ao buscar clubes: {e}")
        return {}

def atletas_mercado() -> Dict[str, Any]:
    """
    Buscar atletas no mercado do Cartola FC
    Retorna: lista de atletas com chave `clube_id` e `status_id`
    """
    try:
        data = _get(f"{API}/atletas/mercado")
        return data
    except Exception as e:
        print(f"[Cartola] Erro ao buscar atletas: {e}")
        return {"atletas": []}

def mercado_status() -> Dict[str, Any]:
    """
    Buscar status do mercado do Cartola FC
    """
    try:
        return _get(f"{API}/mercado/status")
    except Exception as e:
        print(f"[Cartola] Erro ao buscar status: {e}")
        return {}

def estatisticas_clube(clube_id: int) -> Dict[str, Any]:
    """
    Constrói indicadores do ELENCO a partir dos atletas do clube no mercado.
    
    Args:
        clube_id: ID do clube no Cartola FC
        
    Returns:
        Dict com estatísticas do clube: total_atletas, pct_provaveis, 
        media_pontos_elenco, preco_medio, rating, status
    """
    try:
        d = atletas_mercado()
        atletas = [a for a in d.get("atletas", []) if a.get("clube_id") == clube_id]
        total = len(atletas)
        
        if total == 0:
            return {
                "clube_id": clube_id,
                "total_atletas": 0,
                "pct_provaveis": 0,
                "media_pontos_elenco": None,
                "preco_medio": None,
                "rating": 0,
                "status": "Sem dados"
            }

        # Status prováveis (2,3,7,10,12 = provável/dúvida/etc.)
        # Ajuste conforme mapeamento real do Cartola
        provaveis = [a for a in atletas if a.get("status_id") in (2, 3, 7, 10, 12)]
        pct_prov = round(100 * len(provaveis) / total, 1)

        # Proxy de força do elenco: média ponderada de "pontuação média"
        medias = [a.get("media_num") for a in atletas if a.get("media_num") is not None and a.get("media_num") > 0]
        media_time = round(sum(medias) / len(medias), 2) if medias else None

        # Custo médio (cartoletas)
        precos = [a.get("preco_num") for a in atletas if a.get("preco_num") is not None and a.get("preco_num") > 0]
        preco_medio = round(sum(precos) / len(precos), 2) if precos else None

        # Rating simples 0..1: normaliza média do time
        rating = None
        if medias:
            m = media_time
            # Normalização: assume faixa 0..10; refine depois com histórico
            rating = max(0.0, min(1.0, m / 10.0))
        else:
            rating = 0.0

        return {
            "clube_id": clube_id,
            "total_atletas": total,
            "pct_provaveis": pct_prov,
            "media_pontos_elenco": media_time,
            "preco_medio": preco_medio,
            "rating": rating,
            "status": "Dados reais"
        }

    except Exception as e:
        print(f"[Cartola] Erro ao buscar estatísticas do clube {clube_id}: {e}")
        return {
            "clube_id": clube_id,
            "total_atletas": 0,
            "pct_provaveis": 0,
            "media_pontos_elenco": None,
            "preco_medio": None,
            "rating": 0,
            "status": f"Erro: {str(e)}"
        }

def get_clube_mappings() -> Dict[str, int]:
    """
    Mapeamento de nomes de clubes para IDs do Cartola FC
    """
    return {
        'corinthians': 8,
        'flamengo': 262,
        'fortaleza': 131,
        'sport': 14,
        'juventude': 15,
        'internacional': 4,
        'vasco': 10,
        'cruzeiro': 9,
        'athletico': 3,  # Athletico Paranaense
        'gremio': 1,
        'vitoria': 16,
        'bahia': 2,
        'palmeiras': 7,
        'fluminense': 12,
        'botafogo': 11,
        'criciuma': 17,
        'bragantino': 21,
        'santos': 6
    }

def get_clube_id_by_name(name: str) -> Optional[int]:
    """
    Buscar ID do clube pelo nome
    """
    import re
    mappings = get_clube_mappings()
    normalized_name = re.sub(r'[^a-z]', '', name.lower()).replace('atletico', 'athletico')
    return mappings.get(normalized_name)

# Função utilitária para limpar cache (útil para testes)
def clear_cache():
    """Limpar cache de requisições"""
    global _CACHE
    _CACHE = {}
    print("[Cartola] Cache limpo")

# Função para verificar saúde da API
def health_check() -> Dict[str, Any]:
    """
    Verificar se a API está respondendo
    """
    try:
        status = mercado_status()
        return {
            "status": "ok",
            "api_response": True,
            "rodada_atual": status.get("rodada_atual"),
            "status_mercado": status.get("status_mercado"),
            "cache_size": len(_CACHE)
        }
    except Exception as e:
        return {
            "status": "error",
            "api_response": False,
            "error": str(e),
            "cache_size": len(_CACHE)
        }
