#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leitor de Últimos 5 Resultados
Lê os arquivos JSON e retorna dados para integração com o sistema
"""

import json
import os

def ler_ultimos_cinco_serie_a():
    """Lê os últimos 5 resultados da Série A"""
    serie_a_path = "backend/models/Jogos/_serie_a_cinco.json"
    
    if os.path.exists(serie_a_path):
        with open(serie_a_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def ler_ultimos_cinco_serie_b():
    """Lê os últimos 5 resultados da Série B"""
    serie_b_path = "backend/models/Jogos/_serie_b_cinco.json"
    
    if os.path.exists(serie_b_path):
        with open(serie_b_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def gerar_html_chips(resultados):
    """Gera HTML com bolinhas para um time específico"""
    if not resultados:
        return '<div class="chip-container"><span class="chip empate">-</span><span class="chip empate">-</span><span class="chip empate">-</span><span class="chip empate">-</span><span class="chip empate">-</span></div>'
    
    html = '<div class="chip-container">'
    for resultado in resultados:
        if resultado == 'V':
            html += '<span class="chip vitoria">V</span>'
        elif resultado == 'E':
            html += '<span class="chip empate">E</span>'
        elif resultado == 'D':
            html += '<span class="chip derrota">D</span>'
        else:
            html += '<span class="chip empate">-</span>'
    html += '</div>'
    
    return html

def get_ultimos_cinco_por_time(serie, time_nome):
    """Retorna os últimos 5 resultados de um time específico"""
    if serie.lower() == 'a':
        data = ler_ultimos_cinco_serie_a()
    elif serie.lower() == 'b':
        data = ler_ultimos_cinco_serie_b()
    else:
        return ""
    
    # Normalizar nome do time
    time_key = time_nome.lower().replace(' ', '-').replace('_', '-')
    
    return data.get(time_key, "")

if __name__ == "__main__":
    # Teste
    print("=== TESTE DOS ARQUIVOS JSON ===")
    
    serie_a = ler_ultimos_cinco_serie_a()
    print(f"Série A: {len(serie_a)} times")
    for time, resultados in list(serie_a.items())[:3]:
        print(f"  {time}: {resultados}")
    
    print()
    
    serie_b = ler_ultimos_cinco_serie_b()
    print(f"Série B: {len(serie_b)} times")
    for time, resultados in list(serie_b.items())[:3]:
        print(f"  {time}: {resultados}")
    
    print()
    print("=== TESTE HTML CHIPS ===")
    flamengo = get_ultimos_cinco_por_time('a', 'flamengo')
    print(f"Flamengo: {flamengo}")
    print(f"HTML: {gerar_html_chips(flamengo)}")

