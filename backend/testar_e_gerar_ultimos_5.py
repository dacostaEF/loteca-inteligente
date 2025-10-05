#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from datetime import datetime

def testar_e_gerar_ultimos_5():
    """Testar todos os CSVs e gerar os últimos 5 resultados de cada time"""
    print("=== TESTE E GERACAO DOS ULTIMOS 5 RESULTADOS ===")
    
    base_dir = "models/Jogos"
    resultados = {}
    erros = []
    
    # Processar cada CSV
    for item in os.listdir(base_dir):
        clube_dir = os.path.join(base_dir, item)
        if os.path.isdir(clube_dir):
            csv_path = os.path.join(clube_dir, "jogos.csv")
            
            if os.path.exists(csv_path):
                print(f"\nTestando: {item}")
                
                try:
                    # Ler arquivo
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        jogos = list(reader)
                    
                    if not jogos:
                        print(f"  AVISO: {item} - arquivo vazio")
                        continue
                    
                    print(f"  Total de jogos: {len(jogos)}")
                    
                    # Encontrar campo de resultado
                    campos_resultado = [col for col in jogos[0].keys() if 'Resultado' in col]
                    if not campos_resultado:
                        print(f"  ERRO: {item} - nenhum campo Resultado encontrado")
                        erros.append(f"{item}: sem campo Resultado")
                        continue
                    
                    campo_resultado = campos_resultado[0]
                    print(f"  Campo resultado: {campo_resultado}")
                    
                    # ORDENAR POR DATA DECRESCENTE (mais recente primeiro)
                    def parse_data(data_str):
                        try:
                            # Tentar formato DD/MM/YYYY primeiro
                            return datetime.strptime(data_str, '%d/%m/%Y')
                        except ValueError:
                            try:
                                # Tentar formato YYYY-MM-DD
                                return datetime.strptime(data_str, '%Y-%m-%d')
                            except ValueError:
                                # Se não conseguir, retornar data muito antiga
                                return datetime(1900, 1, 1)
                    
                    # Ordenar jogos por data (mais recente primeiro)
                    jogos_ordenados = sorted(jogos, key=lambda x: parse_data(x.get('Data', '01/01/1900')), reverse=True)
                    
                    # Pegar últimos 5 jogos (agora ordenados corretamente)
                    ultimos_5 = jogos_ordenados[:5]
                    
                    print(f"  Datas ordenadas (mais recente primeiro):")
                    for i, jogo in enumerate(jogos_ordenados[:3], 1):  # Mostrar apenas os 3 primeiros
                        data = jogo.get('Data', 'N/A')
                        print(f"    {i}. {data}")
                    
                    # Gerar sequência
                    sequencia = ""
                    for jogo in ultimos_5:
                        resultado = jogo.get(campo_resultado, 'N')
                        
                        # Normalizar resultado
                        if resultado in ['Vitória', 'Vitoria', 'V']:
                            sequencia += "V"
                        elif resultado in ['Empate', 'E']:
                            sequencia += "E"
                        elif resultado in ['Derrota', 'D']:
                            sequencia += "D"
                        else:
                            sequencia += "N"
                    
                    resultados[item] = sequencia
                    print(f"  Sequencia gerada: {sequencia}")
                    
                    # Mostrar detalhes dos últimos 5
                    print(f"  Detalhes dos ultimos 5:")
                    for i, jogo in enumerate(ultimos_5, 1):
                        data = jogo.get('Data', 'N/A')
                        casa = jogo.get('Time_Casa', 'N/A')
                        visitante = jogo.get('Time_Visitante', 'N/A')
                        resultado = jogo.get(campo_resultado, 'N/A')
                        print(f"    {i}. {data} | {casa} x {visitante} | {resultado}")
                    
                except Exception as e:
                    print(f"  ERRO: {item} - {str(e)}")
                    erros.append(f"{item}: {str(e)}")
    
    # Resumo
    print(f"\n=== RESUMO ===")
    print(f"Times processados: {len(resultados)}")
    print(f"Erros encontrados: {len(erros)}")
    
    if erros:
        print(f"\nERROS:")
        for erro in erros:
            print(f"  - {erro}")
    
    # Mostrar todos os resultados
    print(f"\n=== TODOS OS RESULTADOS ===")
    for time, sequencia in sorted(resultados.items()):
        print(f"{time:20s}: {sequencia}")
    
    # Gerar arquivo JSON para atualização
    print(f"\n=== GERANDO ARQUIVO JSON ===")
    
    # Separar Série A e Série B
    serie_a_times = [
        'flamengo', 'palmeiras', 'cruzeiro', 'botafogo', 'mirassol', 'bahia',
        'sao-paulo', 'fluminense', 'red-bull-bragantino', 'gremio', 'ceara',
        'vasco', 'corinthians', 'atletico-mg', 'internacional', 'santos',
        'vitoria', 'juventude', 'fortaleza', 'sport-recife'
    ]
    
    serie_b_times = [
        'coritiba', 'criciuma', 'goias', 'athletico-pr', 'cuiaba', 'chapecoense',
        'crb', 'remo', 'atletico-go', 'avai', 'operario-pr', 'vila-nova',
        'ferroviaria', 'america-mg', 'athletic-mg', 'volta-redonda', 'botafogo-sp',
        'amazonas-fc', 'paysandu'
    ]
    
    serie_a_data = {}
    serie_b_data = {}
    
    for time, sequencia in resultados.items():
        if time in serie_a_times:
            serie_a_data[time] = sequencia
        elif time in serie_b_times:
            serie_b_data[time] = sequencia
    
    # Salvar arquivos JSON
    import json
    
    with open('models/Jogos/_serie_a_cinco.json', 'w', encoding='utf-8') as f:
        json.dump(serie_a_data, f, indent=2, ensure_ascii=False)
    
    with open('models/Jogos/_serie_b_cinco.json', 'w', encoding='utf-8') as f:
        json.dump(serie_b_data, f, indent=2, ensure_ascii=False)
    
    print(f"Arquivo Série A: {len(serie_a_data)} times")
    print(f"Arquivo Série B: {len(serie_b_data)} times")
    print("Arquivos JSON gerados com sucesso!")

if __name__ == "__main__":
    testar_e_gerar_ultimos_5()
