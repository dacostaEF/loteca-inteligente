#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Últimos 5 Resultados
Lê os arquivos JSON e gera HTML com bolinhas coloridas
"""

import json
import os

def gerar_html_ultimos_cinco():
    """Gera HTML com os últimos 5 resultados em formato de bolinhas"""
    
    # Caminhos dos arquivos
    serie_a_path = "backend/models/Jogos/_serie_a_cinco.json"
    serie_b_path = "backend/models/Jogos/_serie_b_cinco.json"
    
    # Ler Série A
    serie_a_data = {}
    if os.path.exists(serie_a_path):
        with open(serie_a_path, 'r', encoding='utf-8') as f:
            serie_a_data = json.load(f)
    
    # Ler Série B
    serie_b_data = {}
    if os.path.exists(serie_b_path):
        with open(serie_b_path, 'r', encoding='utf-8') as f:
            serie_b_data = json.load(f)
    
    # Gerar HTML
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Últimos 5 Resultados - Séries A e B</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .serie {
            background: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .serie h2 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .times-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .time-item {
            display: flex;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        
        .time-nome {
            font-weight: bold;
            margin-right: 15px;
            min-width: 120px;
            color: #333;
        }
        
        .chip-container {
            display: flex;
            gap: 5px;
            align-items: center;
        }
        
        .chip {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #000;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .chip.vitoria {
            background-color: #2ecc71;
        }
        
        .chip.empate {
            background-color: #bdc3c7;
        }
        
        .chip.derrota {
            background-color: #e74c3c;
        }
        
        .legenda {
            background: #e9ecef;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .legenda h3 {
            margin-top: 0;
            color: #495057;
        }
        
        .legenda-item {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Últimos 5 Resultados - Brasileirão</h1>
        
        <div class="serie">
            <h2>🥇 Série A</h2>
            <div class="times-grid">
"""
    
    # Adicionar times da Série A
    for time, resultados in serie_a_data.items():
        html += f"""
                <div class="time-item">
                    <div class="time-nome">{time.replace('-', ' ').title()}</div>
                    <div class="chip-container">
"""
        for resultado in resultados:
            if resultado == 'V':
                html += '<span class="chip vitoria">V</span>'
            elif resultado == 'E':
                html += '<span class="chip empate">E</span>'
            elif resultado == 'D':
                html += '<span class="chip derrota">D</span>'
            else:
                html += '<span class="chip empate">-</span>'
        
        html += """
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="serie">
            <h2>🥈 Série B</h2>
            <div class="times-grid">
"""
    
    # Adicionar times da Série B
    for time, resultados in serie_b_data.items():
        html += f"""
                <div class="time-item">
                    <div class="time-nome">{time.replace('-', ' ').title()}</div>
                    <div class="chip-container">
"""
        for resultado in resultados:
            if resultado == 'V':
                html += '<span class="chip vitoria">V</span>'
            elif resultado == 'E':
                html += '<span class="chip empate">E</span>'
            elif resultado == 'D':
                html += '<span class="chip derrota">D</span>'
            else:
                html += '<span class="chip empate">-</span>'
        
        html += """
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="legenda">
            <h3>📋 Legenda</h3>
            <div class="legenda-item">
                <span class="chip vitoria">V</span> Vitória
            </div>
            <div class="legenda-item">
                <span class="chip empate">E</span> Empate
            </div>
            <div class="legenda-item">
                <span class="chip derrota">D</span> Derrota
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    html = gerar_html_ultimos_cinco()
    
    # Salvar arquivo HTML
    with open("ultimos_cinco_resultados.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("HTML gerado com sucesso!")
    print("Arquivo: ultimos_cinco_resultados.html")
    print("Abra no navegador para visualizar")
