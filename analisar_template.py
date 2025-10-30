#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise do template loteca.html
"""

import re
from collections import Counter
import sys
import io

# Forçar UTF-8 no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analisar_template():
    with open('backend/templates/loteca.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    total_linhas = len(content.split('\n'))
    
    print("="*70)
    print("ANÁLISE DO TEMPLATE LOTECA.HTML")
    print("="*70)
    
    # 1. ESTATÍSTICAS BÁSICAS
    print(f"\n📊 ESTATÍSTICAS BÁSICAS:")
    print(f"   Total de linhas: {total_linhas:,}")
    print(f"   Tamanho: {len(content) / 1024 / 1024:.2f} MB")
    
    # 2. TAGS SCRIPT
    script_tags = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    script_externos = re.findall(r'<script[^>]*src="([^"]+)"', content)
    
    print(f"\n📜 TAGS <script>:")
    print(f"   Scripts inline: {len(script_tags)}")
    print(f"   Scripts externos: {len(script_externos)}")
    
    print(f"\n   Scripts externos carregados:")
    for script in script_externos:
        print(f"      • {script}")
    
    # 3. FUNÇÕES JAVASCRIPT
    # Procurar por: function nome(), const nome = function(), etc.
    funcoes_function = re.findall(r'\bfunction\s+(\w+)\s*\(', content)
    funcoes_const = re.findall(r'\bconst\s+(\w+)\s*=\s*(?:function|async\s+function|\()', content)
    funcoes_let = re.findall(r'\blet\s+(\w+)\s*=\s*(?:function|async\s+function|\()', content)
    funcoes_var = re.findall(r'\bvar\s+(\w+)\s*=\s*(?:function|async\s+function|\()', content)
    
    todas_funcoes = funcoes_function + funcoes_const + funcoes_let + funcoes_var
    
    print(f"\n⚙️ FUNÇÕES JAVASCRIPT:")
    print(f"   Total encontradas: {len(todas_funcoes)}")
    print(f"   Únicas: {len(set(todas_funcoes))}")
    print(f"   Duplicadas: {len(todas_funcoes) - len(set(todas_funcoes))}")
    
    # Contar duplicações
    counter = Counter(todas_funcoes)
    duplicadas = {func: count for func, count in counter.items() if count > 1}
    
    if duplicadas:
        print(f"\n   Funções duplicadas:")
        for func, count in sorted(duplicadas.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"      • {func}: {count}x")
    
    # 4. PADRÕES SUSPEITOS
    print(f"\n🔍 PADRÕES SUSPEITOS:")
    
    # Funções OLD ou REMOVIDA
    funcoes_old = re.findall(r'function\s+(\w*(?:OLD|REMOVIDA|DEPRECATED)\w*)', content, re.IGNORECASE)
    print(f"   Funções OLD/REMOVIDA: {len(funcoes_old)}")
    if funcoes_old:
        for func in funcoes_old[:5]:
            print(f"      • {func}")
    
    # Código comentado (comentários grandes)
    comentarios_grandes = re.findall(r'<!--[\s\S]{100,}?-->', content)
    print(f"   Comentários grandes (>100 chars): {len(comentarios_grandes)}")
    
    # Funções carregarJogo1, carregarJogo2, etc
    funcoes_jogo = re.findall(r'function\s+(carregarJogo\d+\w*)', content)
    print(f"   Funções carregarJogoN: {len(funcoes_jogo)}")
    if funcoes_jogo:
        print(f"      Exemplo: {', '.join(funcoes_jogo[:5])}")
    
    # 5. LINHAS DE CÓDIGO VS HTML
    linhas = content.split('\n')
    linhas_js = 0
    linhas_html = 0
    dentro_script = False
    
    for linha in linhas:
        if '<script' in linha:
            dentro_script = True
        elif '</script>' in linha:
            dentro_script = False
        elif dentro_script:
            linhas_js += 1
        else:
            linhas_html += 1
    
    print(f"\n📈 DISTRIBUIÇÃO DO CÓDIGO:")
    print(f"   Linhas JavaScript: {linhas_js:,} ({linhas_js/total_linhas*100:.1f}%)")
    print(f"   Linhas HTML: {linhas_html:,} ({linhas_html/total_linhas*100:.1f}%)")
    
    # 6. DEPENDÊNCIAS
    print(f"\n🔗 DEPENDÊNCIAS:")
    fetch_calls = re.findall(r'fetch\([\'"]([^\'"]+)', content)
    apis_unicas = set(fetch_calls)
    print(f"   Chamadas fetch(): {len(fetch_calls)}")
    print(f"   APIs únicas: {len(apis_unicas)}")
    if apis_unicas:
        print(f"   APIs:")
        for api in sorted(list(apis_unicas))[:10]:
            print(f"      • {api}")
    
    print("\n" + "="*70)
    print("✅ ANÁLISE CONCLUÍDA")
    print("="*70)

if __name__ == "__main__":
    analisar_template()

