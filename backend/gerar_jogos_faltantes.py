#!/usr/bin/env python3
"""
Script para gerar automaticamente os arquivos JSON dos jogos faltantes (5-14)
com a estrutura corrigida e dados padrão
"""

import json
import os
from datetime import datetime

def gerar_jogo_json(numero, time_casa, time_fora, data_jogo):
    """Gerar arquivo JSON para um jogo específico"""
    
    # Mapear times para escudos
    escudos_map = {
        "INTERNACI0NAL": "/static/escudos/INT_Internacional/Internacional.png",
        "SPORT/PE": "/static/escudos/SPO_Sport/Sport.png",
        "ATLETICO MADRID": "/static/escudos/Atletico_Madrid/atletico_madrid.png",
        "OSASUNA": "/static/escudos/Osasuna/osasuna.png",
        "CRUZEIRO/MG": "/static/escudos/CRU_Cruzeiro/Cruzeiro.png",
        "FORTALEZA/CE": "/static/escudos/FOR_Fortaleza/Fortaleza.png",
        "TOTTENHAM": "/static/escudos/Tottenham/tottenham.png",
        "ASTON VILLA": "/static/escudos/Aston_Villa/aston_villa.png",
        "MIRASSOL/SP": "/static/escudos/MIR_Mirassol/Mirassol.png",
        "SAO PAULO/SP": "/static/escudos/SAO_Sao-Paulo/SaoPaulo.png",
        "CEARA/CE": "/static/escudos/CEA_Ceara/Ceara.png",
        "BOTAFOGO/RJ": "/static/escudos/BOT_Botafogo/Botafogo.png",
        "LIVERPOOL": "/static/escudos/Liverpool/liverpool.png",
        "MANCHESTER UNITED": "/static/escudos/Manchester_United/manchester_united.png",
        "ATALANTA BERGAMAS": "/static/escudos/Atalanta/atalanta.png",
        "LAZIO": "/static/escudos/Lazio/lazio.png",
        "BAHIA/BA": "/static/escudos/BAH_Bahia/Bahia.png",
        "GREMIO/RS": "/static/escudos/GRE_Gremio/Gremio.png",
        "MILAN": "/static/escudos/Milan/milan.png",
        "FIORENTINA": "/static/escudos/Fiorentina/fiorentina.png",
        "GETAFE": "/static/escudos/Getafe/getafe.png",
        "REAL MADRID": "/static/escudos/Real_Madrid/real_madrid.png"
    }
    
    # Dados padrão para todos os jogos
    dados_jogo = {
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
            "dia": data_jogo,
            "escudo_casa": escudos_map.get(time_casa, "/static/escudos/placeholder-team-logo.svg"),
            "escudo_fora": escudos_map.get(time_fora, "/static/escudos/placeholder-team-logo.svg"),
            "probabilidade_casa": "35",
            "probabilidade_empate": "30",
            "probabilidade_fora": "35",
            "recomendacao": f"Recomendação Estatística: Coluna 1 ({time_casa.split('/')[0]}) - Risco Médio",
            "conclusao_analista": f"Confronto equilibrado entre {time_casa.split('/')[0]} e {time_fora.split('/')[0]}. Ambos os times apresentam campanhas similares e características técnicas parecidas. O fator casa será decisivo para determinar o resultado. Recomendação: Análise detalhada necessária.",
            "confrontos_sequence": "E-E-E-E-E-E-E-E-E-E",  # Sequência padrão (todos empates)
            "posicao_casa": "10",
            "posicao_fora": "12",
            "confronto_direto": "3V-4E-3D",  # Resumo padrão equilibrado
            "fator_casa": "50",
            "fator_fora": "50",
            "analise_posicao": "Confronto Equilibrado",
            "analise_posicao_tabelas": "Confronto Equilibrado",
            "analise_confronto_direto": "Confronto Equilibrado",
            "analise_fator_casa": "Confronto Equilibrado",
            "arquivo_confrontos": "",  # Campo para salvar nome do arquivo CSV
            "sincronizado_em": datetime.now().isoformat()
        },
        "admin_key": "loteca2024admin"
    }
    
    return dados_jogo

def main():
    """Função principal para gerar todos os jogos faltantes"""
    
    # Dados dos jogos do concurso 1216 (incluindo jogo 2 que precisa ser corrigido)
    jogos_dados = [
        (2, "INTERNACI0NAL", "SPORT/PE", "Domingo"),  # Jogo 2 corrigido
        (5, "ATLETICO MADRID", "OSASUNA", "Sábado"),
        (6, "CRUZEIRO/MG", "FORTALEZA/CE", "Sábado"),
        (7, "TOTTENHAM", "ASTON VILLA", "Domingo"),
        (8, "MIRASSOL/SP", "SAO PAULO/SP", "Domingo"),
        (9, "CEARA/CE", "BOTAFOGO/RJ", "Domingo"),
        (10, "LIVERPOOL", "MANCHESTER UNITED", "Domingo"),
        (11, "ATALANTA BERGAMAS", "LAZIO", "Domingo"),
        (12, "BAHIA/BA", "GREMIO/RS", "Domingo"),
        (13, "MILAN", "FIORENTINA", "Domingo"),
        (14, "GETAFE", "REAL MADRID", "Domingo")
    ]
    
    # Diretório de destino
    diretorio_destino = "backend/models/concurso_1216/analise_rapida"
    
    print("🚀 GERANDO ARQUIVOS JSON DOS JOGOS FALTANTES...")
    print("=" * 60)
    
    for numero, time_casa, time_fora, data_jogo in jogos_dados:
        print(f"📝 Gerando jogo {numero}: {time_casa} vs {time_fora}")
        
        # Gerar dados do jogo
        dados_jogo = gerar_jogo_json(numero, time_casa, time_fora, data_jogo)
        
        # Nome do arquivo
        nome_arquivo = f"jogo_{numero}.json"
        caminho_arquivo = os.path.join(diretorio_destino, nome_arquivo)
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_arquivo):
            print(f"   🔄 Arquivo {nome_arquivo} já existe, sobrescrevendo...")
        
        # Salvar arquivo
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_jogo, f, indent=2, ensure_ascii=False)
            print(f"   ✅ Arquivo {nome_arquivo} criado com sucesso!")
        except Exception as e:
            print(f"   ❌ Erro ao criar {nome_arquivo}: {e}")
    
    print("\n🎉 PROCESSO CONCLUÍDO!")
    print("📋 Todos os arquivos JSON foram gerados com:")
    print("   ✅ Estrutura corrigida")
    print("   ✅ Dados padrão equilibrados")
    print("   ✅ Sequências padrão (E-E-E-E-E-E-E-E-E-E)")
    print("   ✅ Resumos padrão (3V-4E-3D)")
    print("   ✅ Prontos para personalização na Central Admin")

if __name__ == "__main__":
    main()
