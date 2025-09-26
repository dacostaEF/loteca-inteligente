#!/usr/bin/env python3
"""
CORRIGIR CAMINHOS DOS ESCUDOS
Atualiza todos os caminhos hard-coded dos escudos no HTML
"""

import re

def corrigir_caminhos_escudos():
    """Corrige todos os caminhos dos escudos no arquivo HTML"""
    
    # Mapeamento dos caminhos antigos para novos
    mapeamento = {
        '/static/escudos/JUV/45x45.png': '/static/escudos/JUV_Juventude/45x45.png',
        '/static/escudos/INT/45x45.png': '/static/escudos/INT_Internacional/45x45.png',
        '/static/escudos/VAS/45x45.png': '/static/escudos/VAS_Vasco/45x45.png',
        '/static/escudos/CRU/45x45.png': '/static/escudos/CRU_Cruzeiro/45x45.png',
        '/static/escudos/CAP/45x45.png': '/static/escudos/CAP_Athlético-PR/45x45.png',
        '/static/escudos/OPE/45x45.png': '/static/escudos/OPE_Operário-PR/45x45.png',
        '/static/escudos/CAM/45x45.png': '/static/escudos/CAM_Atletico-MG/45x45.png',
        '/static/escudos/MIR/45x45.png': '/static/escudos/MIR_Mirassol/45x45.png',
        '/static/escudos/GRE/45x45.png': '/static/escudos/GRE_Grêmio/45x45.png',
        '/static/escudos/VIT/45x45.png': '/static/escudos/VIT_Vitória/45x45.png',
        '/static/escudos/BAH/45x45.png': '/static/escudos/BAH_Bahia/45x45.png',
        '/static/escudos/PAL/45x45.png': '/static/escudos/PAL_Palmeiras/45x45.png',
        '/static/escudos/FLU/45x45.png': '/static/escudos/FLU_Fluminense/45x45.png',
        '/static/escudos/BOT/45x45.png': '/static/escudos/BOT_Botafogo-RJ/45x45.png',
        '/static/escudos/CRI/45x45.png': '/static/escudos/CRI_Criciúma/45x45.png',
        '/static/escudos/PAY/45x45.png': '/static/escudos/PAY_Paysandu/45x45.png',
        '/static/escudos/RBB/45x45.png': '/static/escudos/RBB_Bragantino/45x45.png',
        '/static/escudos/SAN/45x45.png': '/static/escudos/SAN_Santos/45x45.png'
    }
    
    print("🔧 Corrigindo caminhos dos escudos...")
    
    # Ler arquivo HTML
    html_file = "templates/loteca.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    alteracoes = 0
    
    # Aplicar correções
    for caminho_antigo, caminho_novo in mapeamento.items():
        if caminho_antigo in conteudo:
            conteudo = conteudo.replace(caminho_antigo, caminho_novo)
            alteracoes += 1
            print(f"✅ {caminho_antigo} → {caminho_novo}")
    
    # Salvar arquivo corrigido
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"\n🎉 Correção concluída!")
    print(f"✅ {alteracoes} caminhos corrigidos")

if __name__ == "__main__":
    corrigir_caminhos_escudos()
