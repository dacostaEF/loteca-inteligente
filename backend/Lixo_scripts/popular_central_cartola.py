#!/usr/bin/env python3
"""
POPULAR CENTRAL DE DADOS COM CARTOLA FC
Script para extrair os 68 clubes do Cartola FC e popular a Central de Dados
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.central_dados import CentralDados
from services.cartola_provider import clubes, estatisticas_clube
import logging

logger = logging.getLogger(__name__)

# MAPEAMENTO MANUAL PARA CLASSIFICAÇÃO
CLASSIFICACAO_SERIES = {
    # SÉRIE A 2025 (20 clubes)
    'serie_a': {
        262: 'FLA',  # Flamengo
        264: 'COR',  # Corinthians  
        275: 'PAL',  # Palmeiras
        276: 'SAO',  # São Paulo
        266: 'FLU',  # Fluminense
        263: 'BOT',  # Botafogo
        267: 'VAS',  # Vasco
        265: 'BAH',  # Bahia
        285: 'INT',  # Internacional
        284: 'GRE',  # Grêmio
        282: 'CAM',  # Atlético Mineiro
        283: 'CRU',  # Cruzeiro
        287: 'VIT',  # Vitória
        293: 'CAP',  # Athletico-PR
        356: 'FOR',  # Fortaleza
        354: 'CEA',  # Ceará
        280: 'RBB',  # Red Bull Bragantino
        288: 'CRI',  # Criciúma
        286: 'JUV',  # Juventude
        277: 'SAN',  # Santos
    },
    
    # SÉRIE B 2025 (estimativa com clubes conhecidos)
    'serie_b': {
        292: 'SPT',  # Sport
        309: 'BRA',  # Brasiliense
        314: 'AVA',  # Avaí
        315: 'CHA',  # Chapecoense
        340: 'CRB',  # CRB
        341: 'CSA',  # CSA
        290: 'GOI',  # Goiás
        343: 'NAU',  # Náutico
        289: 'PAR',  # Paraná
        291: 'PAY',  # Paysandu
        303: 'PON',  # Ponte Preta
        306: 'SAN',  # Santa Cruz
        344: 'STC',  # Santa Catarina
        350: 'ABC',  # ABC
        351: 'AME',  # América-RN
        362: 'MOT',  # Moto Club
        363: 'SAM',  # Sampaio Corrêa
        364: 'REM',  # Remo
        373: 'ACG',  # Atlético-GO
        375: 'VIL',  # Vila Nova
    }
}

# MAPEAMENTO DE ESTADOS (baseado em conhecimento dos clubes)
ESTADOS_CLUBES = {
    # RIO DE JANEIRO
    262: 'RJ',  # Flamengo
    266: 'RJ',  # Fluminense
    263: 'RJ',  # Botafogo
    267: 'RJ',  # Vasco
    
    # SÃO PAULO  
    264: 'SP',  # Corinthians
    275: 'SP',  # Palmeiras
    276: 'SP',  # São Paulo
    277: 'SP',  # Santos
    280: 'SP',  # Red Bull Bragantino
    303: 'SP',  # Ponte Preta
    
    # MINAS GERAIS
    282: 'MG',  # Atlético Mineiro
    283: 'MG',  # Cruzeiro
    
    # RIO GRANDE DO SUL
    285: 'RS',  # Internacional
    284: 'RS',  # Grêmio
    286: 'RS',  # Juventude
    
    # BAHIA
    265: 'BA',  # Bahia
    287: 'BA',  # Vitória
    
    # PARANÁ
    293: 'PR',  # Athletico-PR
    289: 'PR',  # Paraná
    
    # CEARÁ
    356: 'CE',  # Fortaleza
    354: 'CE',  # Ceará
    363: 'CE',  # Sampaio Corrêa
    
    # SANTA CATARINA
    314: 'SC',  # Avaí
    315: 'SC',  # Chapecoense
    344: 'SC',  # Santa Catarina
    317: 'SC',  # Joinville
    
    # GOIÁS
    290: 'GO',  # Goiás
    373: 'GO',  # Atlético-GO
    375: 'GO',  # Vila Nova
    
    # PERNAMBUCO
    292: 'PE',  # Sport
    343: 'PE',  # Náutico
    306: 'PE',  # Santa Cruz
    
    # ALAGOAS
    340: 'AL',  # CRB
    341: 'AL',  # CSA
    342: 'AL',  # ASA
    
    # PARÁ
    291: 'PA',  # Paysandu
    364: 'PA',  # Remo
    
    # RIO GRANDE DO NORTE
    350: 'RN',  # ABC
    351: 'RN',  # América-RN
    
    # MARANHÃO
    362: 'MA',  # Moto Club
    
    # DISTRITO FEDERAL
    309: 'DF',  # Brasiliense
    
    # PARAÍBA
    1349: 'PB',  # Ipatinga (se for da Paraíba)
    
    # SERGIPE
    288: 'SE',  # Criciúma (verificar)
}

def detectar_serie(clube_id: int) -> str:
    """Detectar série do clube baseado no mapeamento"""
    if clube_id in CLASSIFICACAO_SERIES['serie_a']:
        return 'A'
    elif clube_id in CLASSIFICACAO_SERIES['serie_b']:
        return 'B'
    else:
        return 'REGIONAL'

def detectar_estado(clube_id: int) -> str:
    """Detectar estado do clube"""
    return ESTADOS_CLUBES.get(clube_id, 'UNKNOWN')

def extrair_cores_do_escudo(escudo_urls: dict) -> tuple:
    """
    Extrair cores baseado no nome do clube (simplificado)
    Em uma implementação completa, isso seria análise de imagem
    """
    # Cores básicas conhecidas (simplificado)
    cores_conhecidas = {
        'FLA': ('#E60026', '#000000'),  # Vermelho e preto
        'COR': ('#000000', '#FFFFFF'),  # Preto e branco
        'PAL': ('#1E4D2B', '#FFFFFF'),  # Verde e branco
        'SAO': ('#FF0000', '#000000'),  # Vermelho e preto
        'FLU': ('#800020', '#FFFFFF'),  # Grená e branco
        'BOT': ('#000000', '#FFFFFF'),  # Preto e branco
        'VAS': ('#000000', '#FFFFFF'),  # Preto e branco
        'BAH': ('#0066CC', '#FF0000'),  # Azul e vermelho
        'INT': ('#CC0000', '#FFFFFF'),  # Vermelho e branco
        'GRE': ('#007AC1', '#000000'),  # Azul e preto
    }
    
    return ('#FFFFFF', '#000000')  # Padrão

def popular_central_com_cartola():
    """Função principal para popular a central com dados do Cartola"""
    
    print("🏗️ Inicializando Central de Dados...")
    central = CentralDados()
    central.popular_dados_iniciais()
    
    print("📡 Buscando dados do Cartola FC...")
    try:
        clubes_cartola = clubes()
        print(f"✅ Encontrados {len(clubes_cartola)} clubes no Cartola FC")
    except Exception as e:
        print(f"❌ Erro ao buscar clubes do Cartola: {e}")
        return
    
    print("🏗️ Processando e classificando clubes...")
    clubes_processados = 0
    
    for clube_id, dados_brutos in clubes_cartola.items():
        try:
            # Detectar classificação
            serie = detectar_serie(clube_id)
            estado = detectar_estado(clube_id)
            
            # Extrair URLs dos escudos
            escudos = dados_brutos.get('escudos', {})
            
            # Buscar estatísticas do clube
            print(f"📊 Buscando stats do clube {dados_brutos.get('nome', 'UNKNOWN')} (ID: {clube_id})...")
            try:
                stats = estatisticas_clube(clube_id)
            except Exception as e:
                print(f"⚠️ Erro ao buscar stats do clube {clube_id}: {e}")
                stats = {}
            
            # Preparar dados para a central
            dados_clube = {
                'id': clube_id,
                'nome': dados_brutos.get('nome', ''),
                'nome_completo': dados_brutos.get('nome_fantasia', ''),
                'abreviacao': dados_brutos.get('abreviacao', ''),
                'apelido': dados_brutos.get('apelido', ''),
                'estado': estado,
                'escudo_url': escudos.get('60x60', ''),
                'escudo_30x30': escudos.get('30x30', ''),
                'escudo_45x45': escudos.get('45x45', ''),
                'escudo_60x60': escudos.get('60x60', ''),
                'stats': stats
            }
            
            # Salvar na central
            central.salvar_clube(dados_clube, fonte='CARTOLA')
            
            # Associar ao campeonato adequado
            if serie in ['A', 'B']:
                campeonato_id = 1 if serie == 'A' else 2  # Série A ou B
                try:
                    with central.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT OR IGNORE INTO clube_campeonatos
                            (clube_id, campeonato_id, temporada)
                            VALUES (?, ?, 2025)
                        """, (clube_id, campeonato_id))
                        conn.commit()
                except Exception as e:
                    print(f"⚠️ Erro ao associar clube {clube_id} ao campeonato: {e}")
            
            clubes_processados += 1
            print(f"✅ {dados_clube['nome']} (Série {serie}, {estado}) - processado")
            
        except Exception as e:
            print(f"❌ Erro ao processar clube {clube_id}: {e}")
            continue
    
    print(f"\n🎉 Processamento concluído!")
    print(f"📊 {clubes_processados} clubes salvos na Central de Dados")
    
    # Mostrar estatísticas finais
    stats = central.get_estatisticas_sistema()
    print(f"\n📈 Estatísticas do Sistema:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Mostrar distribuição por série
    with central.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nome, cc.campeonato_id, camp.nome as campeonato
            FROM clubes c
            LEFT JOIN clube_campeonatos cc ON c.id = cc.clube_id  
            LEFT JOIN campeonatos camp ON cc.campeonato_id = camp.id
            WHERE cc.temporada = 2025 OR cc.temporada IS NULL
            ORDER BY cc.campeonato_id, c.nome
        """)
        
        results = cursor.fetchall()
        
        print(f"\n🏆 Distribuição por Série:")
        serie_a = [r for r in results if r[1] == 1]
        serie_b = [r for r in results if r[1] == 2]
        regionais = [r for r in results if r[1] is None]
        
        print(f"  Série A: {len(serie_a)} clubes")
        print(f"  Série B: {len(serie_b)} clubes") 
        print(f"  Regionais: {len(regionais)} clubes")

if __name__ == "__main__":
    popular_central_com_cartola()

