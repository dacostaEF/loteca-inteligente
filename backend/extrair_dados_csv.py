"""
Script para extrair dados do HTML original e criar CSV
"""

import re
import csv
import json

def extrair_dados_html():
    """Extrai dados do HTML original e cria CSV"""
    
    # Ler HTML original
    with open('static/valor_elenco/planilha_clubes_futebol_final.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extrair array top100Clubs
    pattern = r'const top100Clubs = \[(.*?)\];'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if not match:
        print("❌ Array top100Clubs não encontrado")
        return
    
    clubs_data = match.group(1)
    
    # Converter para lista Python
    clubs_list = []
    
    # Processar cada linha do array
    lines = clubs_data.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('{') and line.endswith('},'):
            # Extrair dados da linha
            # Formato: { posicao: 1, clube: "Real Madrid", pais: "Espanha", valor: "€ 1.726 M" },
            
            # Usar regex para extrair valores
            pos_match = re.search(r'posicao:\s*(\d+)', line)
            clube_match = re.search(r'clube:\s*"([^"]+)"', line)
            pais_match = re.search(r'pais:\s*"([^"]+)"', line)
            valor_match = re.search(r'valor:\s*"([^"]+)"', line)
            
            if pos_match and clube_match and pais_match and valor_match:
                club = {
                    'posicao': int(pos_match.group(1)),
                    'clube': clube_match.group(1),
                    'pais': pais_match.group(1),
                    'valor': valor_match.group(1)
                }
                clubs_list.append(club)
    
    print(f"✅ Extraídos {len(clubs_list)} clubes")
    
    # Salvar como CSV
    with open('static/valor_elenco/top100_clubes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['posicao', 'clube', 'pais', 'valor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for club in clubs_list:
            writer.writerow(club)
    
    print("✅ CSV criado: static/valor_elenco/top100_clubes.csv")
    
    # Salvar como JSON também
    with open('static/valor_elenco/top100_clubes.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(clubs_list, jsonfile, ensure_ascii=False, indent=2)
    
    print("✅ JSON criado: static/valor_elenco/top100_clubes.json")
    
    return clubs_list

if __name__ == "__main__":
    extrair_dados_html()
