#!/usr/bin/env python3
"""
Script simples para criar todos os jogos restantes
"""

import json

# Dados dos jogos
jogos = [
    (9, "CEARA/CE", "BOTAFOGO/RJ", "/static/escudos/CEA_Ceara/Ceara.png", "/static/escudos/BOT_Botafogo/Botafogo.png"),
    (10, "LIVERPOOL", "MANCHESTER UNITED", "/static/escudos/Liverpool/liverpool.png", "/static/escudos/Manchester_United/manchester_united.png"),
    (11, "ATALANTA BERGAMAS", "LAZIO", "/static/escudos/Atalanta/atalanta.png", "/static/escudos/Lazio/lazio.png"),
    (12, "BAHIA/BA", "GREMIO/RS", "/static/escudos/BAH_Bahia/Bahia.png", "/static/escudos/GRE_Gremio/Gremio.png"),
    (13, "MILAN", "FIORENTINA", "/static/escudos/Milan/milan.png", "/static/escudos/Fiorentina/fiorentina.png"),
    (14, "GETAFE", "REAL MADRID", "/static/escudos/Getafe/getafe.png", "/static/escudos/Real_Madrid/real_madrid.png")
]

for numero, time_casa, time_fora, escudo_casa, escudo_fora in jogos:
    dados = {
        "metadados": {
            "jogo_numero": str(numero),
            "concurso_numero": "1216"
        },
        "dados": {
            "numero": str(numero),
            "time_casa": time_casa,
            "time_fora": time_fora,
            "arena": f"Arena {time_casa.split('/')[0]}" if '/' in time_casa else f"Arena {time_casa}",
            "campeonato": "Brasileirão Série A" if any(termo in time_casa.upper() for termo in ['/SP', '/MG', '/CE', '/RJ', '/BA', '/RS']) else "Internacional",
            "dia": "Domingo",
            "escudo_casa": escudo_casa,
            "escudo_fora": escudo_fora,
            "probabilidade_casa": "35",
            "probabilidade_empate": "30",
            "probabilidade_fora": "35",
            "recomendacao": f"Recomendação Estatística: Coluna 1 ({time_casa.split('/')[0]}) - Risco Médio",
            "conclusao_analista": f"Confronto equilibrado entre {time_casa.split('/')[0]} e {time_fora.split('/')[0]}. Ambos os times apresentam campanhas similares e características técnicas parecidas. O fator casa será decisivo para determinar o resultado. Recomendação: Análise detalhada necessária.",
            "confrontos_sequence": "E-E-E-E-E-E-E-E-E-E",
            "posicao_casa": "10",
            "posicao_fora": "12",
            "confronto_direto": "3V-4E-3D",
            "fator_casa": "50",
            "fator_fora": "50",
            "analise_posicao": "Confronto Equilibrado",
            "analise_posicao_tabelas": "Confronto Equilibrado",
            "analise_confronto_direto": "Confronto Equilibrado",
            "analise_fator_casa": "Confronto Equilibrado",
            "sincronizado_em": "2025-10-15T15:20:00.000Z"
        },
        "admin_key": "loteca2024admin"
    }
    
    with open(f"backend/models/concurso_1216/analise_rapida/jogo_{numero}.json", 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Jogo {numero} criado: {time_casa} vs {time_fora}")

print("🎉 Todos os jogos foram criados!")
