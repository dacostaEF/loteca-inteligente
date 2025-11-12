"""
Script para Calcular Estatísticas de Seleções a partir dos CSVs de Confrontos
Autor: Loteca X-Ray
Data: 2025-01-12

Calcula estatísticas baseadas nos jogos históricos dos CSVs
"""

import csv
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

# Mapeamento dos 8 jogos de seleções
JOGOS_SELECOES = {
    4: {'casa': 'BOSNIA HERZEGOVINA', 'fora': 'ROMÊNIA', 'csv': 'BosniaHerzogovina_vs_Romenia.csv'},
    5: {'casa': 'SUICA', 'fora': 'SUECIA', 'csv': 'Suica_vs_Suecia.csv'},
    6: {'casa': 'GRECIA', 'fora': 'ESCOCIA', 'csv': 'Escocia_vs_Grecia.csv'},
    7: {'casa': 'HUNGRIA', 'fora': 'IRLANDA', 'csv': 'Irlanda_vs_Hungria.csv'},
    10: {'casa': 'ALBANIA', 'fora': 'INGLATERRA', 'csv': 'Albania_vs_Inglaterra.csv'},
    11: {'casa': 'SERVIA', 'fora': 'LETONIA', 'csv': 'Servia_vs_Letonia.csv'},
    12: {'casa': 'ITALIA', 'fora': 'NORUEGA', 'csv': 'Italia_vs_Noruega.csv'},
    14: {'casa': 'UCRANIA', 'fora': 'ISLANDIA', 'csv': 'Islandia_vs_Ucrania.csv'}
}

def normalizar_nome(nome: str) -> str:
    """Normaliza nome para comparação"""
    return nome.upper().strip().replace('Â', 'A').replace('Ê', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')

def extrair_placar(placar_str: str) -> Tuple[int, int]:
    """
    Extrai gols de um placar
    Ex: "4-1" -> (4, 1)
        "2-1 (Pro.)" -> (2, 1)
    """
    try:
        # Remover texto extra (Pro.), espaços, etc
        placar_limpo = placar_str.split('(')[0].strip()
        gols = placar_limpo.split('-')
        return int(gols[0]), int(gols[1])
    except:
        return 0, 0

def calcular_resultado(gols_pro: int, gols_contra: int) -> str:
    """V, E ou D"""
    if gols_pro > gols_contra:
        return 'V'
    elif gols_pro < gols_contra:
        return 'D'
    else:
        return 'E'

def calcular_pontos(resultado: str) -> int:
    """3 pontos vitória, 1 empate, 0 derrota"""
    return {'V': 3, 'E': 1, 'D': 0}.get(resultado, 0)

def processar_csv_confrontos(csv_path: str, nome_time: str) -> Dict:
    """
    Processa CSV de confrontos e calcula estatísticas para um time específico
    """
    print(f"\nProcessando: {nome_time}")
    print(f"CSV: {os.path.basename(csv_path)}")
    
    if not os.path.exists(csv_path):
        print(f"ERRO: Arquivo nao encontrado: {csv_path}")
        return None
    
    nome_norm = normalizar_nome(nome_time)
    
    # Dados gerais
    jogos_total = []
    jogos_casa = []
    jogos_fora = []
    
    print(f"  Lendo CSV...")
    
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mandante = normalizar_nome(row.get('mandante', ''))
            visitante = normalizar_nome(row.get('visitante', ''))
            placar = row.get('placar', '0-0')
            
            gols_mandante, gols_visitante = extrair_placar(placar)
            
            # Verificar se é o nosso time como mandante ou visitante
            if nome_norm in mandante or mandante in nome_norm:
                # Nosso time jogou em casa
                gols_pro = gols_mandante
                gols_contra = gols_visitante
                resultado = calcular_resultado(gols_pro, gols_contra)
                jogos_casa.append({
                    'gols_pro': gols_pro,
                    'gols_contra': gols_contra,
                    'resultado': resultado,
                    'pontos': calcular_pontos(resultado)
                })
                jogos_total.append(jogos_casa[-1])
                
            elif nome_norm in visitante or visitante in nome_norm:
                # Nosso time jogou fora
                gols_pro = gols_visitante
                gols_contra = gols_mandante
                resultado = calcular_resultado(gols_pro, gols_contra)
                jogos_fora.append({
                    'gols_pro': gols_pro,
                    'gols_contra': gols_contra,
                    'resultado': resultado,
                    'pontos': calcular_pontos(resultado)
                })
                jogos_total.append(jogos_fora[-1])
    
    # Calcular estatísticas GERAIS
    total_jogos = len(jogos_total)
    if total_jogos == 0:
        print(f"AVISO: Nenhum jogo encontrado para {nome_time}")
        return None
    
    total_gols_pro = sum(j['gols_pro'] for j in jogos_total)
    total_gols_contra = sum(j['gols_contra'] for j in jogos_total)
    media_gols_pro = round(total_gols_pro / total_jogos, 2)
    media_gols_contra = round(total_gols_contra / total_jogos, 2)
    
    # Over 2.5 (total de gols >= 3)
    jogos_over25 = sum(1 for j in jogos_total if (j['gols_pro'] + j['gols_contra']) >= 3)
    over25_pct = round((jogos_over25 / total_jogos) * 100, 1)
    
    # BTTS (ambos marcaram)
    jogos_btts = sum(1 for j in jogos_total if j['gols_pro'] > 0 and j['gols_contra'] > 0)
    btts_pct = round((jogos_btts / total_jogos) * 100, 1)
    
    # Clean Sheets (não sofreu gols)
    jogos_clean = sum(1 for j in jogos_total if j['gols_contra'] == 0)
    clean_pct = round((jogos_clean / total_jogos) * 100, 1)
    
    # Últimos 5 jogos (mais recentes)
    ultimos_5 = jogos_total[-5:]  # Pega os últimos 5
    sequencia_ultimos5 = ''.join([j['resultado'] for j in ultimos_5])
    pontos_ultimos5 = sum(j['pontos'] for j in ultimos_5)
    
    # Calcular estatísticas CASA
    total_jogos_casa = len(jogos_casa)
    if total_jogos_casa > 0:
        total_gols_pro_casa = sum(j['gols_pro'] for j in jogos_casa)
        total_gols_contra_casa = sum(j['gols_contra'] for j in jogos_casa)
        pontos_casa = sum(j['pontos'] for j in jogos_casa)
        aproveitamento_casa = round((pontos_casa / (total_jogos_casa * 3)) * 100, 1)
    else:
        total_gols_pro_casa = 0
        total_gols_contra_casa = 0
        aproveitamento_casa = 0.0
    
    # Calcular estatísticas FORA
    total_jogos_fora = len(jogos_fora)
    if total_jogos_fora > 0:
        total_gols_pro_fora = sum(j['gols_pro'] for j in jogos_fora)
        total_gols_contra_fora = sum(j['gols_contra'] for j in jogos_fora)
        pontos_fora = sum(j['pontos'] for j in jogos_fora)
        aproveitamento_fora = round((pontos_fora / (total_jogos_fora * 3)) * 100, 1)
    else:
        total_gols_pro_fora = 0
        total_gols_contra_fora = 0
        aproveitamento_fora = 0.0
    
    estatisticas = {
        'Time': nome_time,
        'Posição': 0,  # ⚠️ Usuário preencherá
        'Jogos': total_jogos,
        'Gols Pró': total_gols_pro,
        'Gols Contra': total_gols_contra,
        'Média Gols Pró': media_gols_pro,
        'Média Gols Contra': media_gols_contra,
        'Over 2.5 %': over25_pct,
        'BTTS Sim %': btts_pct,
        'Clean Sheets %': clean_pct,
        'Últimos 5 Jogos': sequencia_ultimos5,
        'Pontos Últimos 5': pontos_ultimos5,
        'Jogos Casa': total_jogos_casa,
        'Aproveitamento Casa %': aproveitamento_casa,
        'Gols Pró Casa': total_gols_pro_casa,
        'Gols Contra Casa': total_gols_contra_casa,
        'Jogos Fora': total_jogos_fora,
        'Aproveitamento Fora %': aproveitamento_fora,
        'Gols Pró Fora': total_gols_pro_fora,
        'Gols Contra Fora': total_gols_contra_fora,
        'Fonte': 'Calculado a partir de jogos históricos',
        'Status': 'Dados Parciais - Posição a preencher'
    }
    
    print(f"OK {nome_time}: {total_jogos} jogos analisados")
    print(f"   Media Gols: {media_gols_pro} pro / {media_gols_contra} contra")
    print(f"   Casa: {total_jogos_casa} jogos ({aproveitamento_casa}%)")
    print(f"   Fora: {total_jogos_fora} jogos ({aproveitamento_fora}%)")
    
    return estatisticas

def main():
    """Processar todos os jogos de seleções"""
    print("="*60)
    print("CALCULADOR DE ESTATISTICAS DE SELECOES")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    confrontos_dir = os.path.join(base_dir, 'models', 'confrontos')
    output_dir = os.path.join(base_dir, 'models', 'EstatisticasElenco')
    
    # Coletar todas as estatísticas
    todas_estatisticas = []
    selecoes_processadas = set()
    
    for jogo_num, info in sorted(JOGOS_SELECOES.items()):
        print(f"\n{'='*60}")
        print(f"JOGO {jogo_num}: {info['casa']} vs {info['fora']}")
        print(f"{'='*60}")
        
        csv_path = os.path.join(confrontos_dir, info['csv'])
        
        # Processar time da casa (se ainda não processado)
        if info['casa'] not in selecoes_processadas:
            stats_casa = processar_csv_confrontos(csv_path, info['casa'])
            if stats_casa:
                todas_estatisticas.append(stats_casa)
                selecoes_processadas.add(info['casa'])
        
        # Processar time de fora (se ainda não processado)
        if info['fora'] not in selecoes_processadas:
            stats_fora = processar_csv_confrontos(csv_path, info['fora'])
            if stats_fora:
                todas_estatisticas.append(stats_fora)
                selecoes_processadas.add(info['fora'])
    
    # Salvar em JSON
    output_json = os.path.join(output_dir, 'Estatisticas_Selecoes_Calculadas.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(todas_estatisticas, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"CONCLUIDO!")
    print(f"{'='*60}")
    print(f"Total de selecoes processadas: {len(todas_estatisticas)}")
    print(f"Arquivo salvo: {output_json}")
    print(f"\nATENCAO:")
    print(f"   - Campo 'Posicao' esta em 0 (voce deve preencher)")
    print(f"   - Estatisticas baseadas apenas em jogos historicos dos CSVs")
    print(f"   - Voce pode complementar com dados da internet")
    
    # Salvar também em CSV para fácil edição
    output_csv = os.path.join(output_dir, 'Estatisticas_Selecoes_Calculadas.csv')
    if todas_estatisticas:
        with open(output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=todas_estatisticas[0].keys())
            writer.writeheader()
            writer.writerows(todas_estatisticas)
        print(f"CSV salvo: {output_csv}")
    
    print(f"\n{'='*60}\n")

if __name__ == '__main__':
    main()

