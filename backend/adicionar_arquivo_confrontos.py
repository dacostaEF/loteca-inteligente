#!/usr/bin/env python3
"""
ADICIONAR ARQUIVO_CONFRONTOS AOS JOGOS
======================================

Script simples para adicionar o campo 'arquivo_confrontos' aos jogos que não têm.
"""

import json
from pathlib import Path

# Mapeamento de jogos para arquivos CSV
mapeamento = {
    1: "Flamengo_vs_Palmeiras.csv",
    2: "Internacional_vs_Sport.csv",
    3: "Corinthians_vs_Atletico-MG.csv",
    4: "Vasco_vs_Cruzeiro.csv",
    5: "Atletico-de-Madrid_vs_Osasuna.csv",
    6: "Atletico-MG_vs_Mirassol.csv",
    7: "Gremio_vs_Vitoria.csv",
    8: "Bahia_vs_Ceara.csv",
    9: "Fortaleza_vs_Juventude.csv",
    10: "Fluminense_vs_Botafogo.csv",
    11: "Criciuma_vs_Paysandu.csv",
    12: "Newcastle_vs_Arsenal.csv",
    13: "Bragantino_vs_Santos.csv",
    14: "Barcelona_vs_Real-Sociedad.csv"
}

def adicionar_campo(jogo_numero):
    """Adicionar campo arquivo_confrontos a um jogo"""
    arquivo = Path(f"models/concurso_1216/analise_rapida/jogo_{jogo_numero}.json")
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    try:
        # Ler arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar se já tem o campo
        if 'arquivo_confrontos' in data['dados']:
            print(f"✅ Jogo {jogo_numero} já tem arquivo_confrontos: {data['dados']['arquivo_confrontos']}")
            return True
        
        # Adicionar campo
        nome_arquivo = mapeamento.get(jogo_numero, f"Jogo_{jogo_numero}.csv")
        data['dados']['arquivo_confrontos'] = nome_arquivo
        
        # Salvar arquivo
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Jogo {jogo_numero} atualizado: {nome_arquivo}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no Jogo {jogo_numero}: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 ADICIONANDO ARQUIVO_CONFRONTOS AOS JOGOS")
    print("="*50)
    
    sucessos = 0
    total = 14
    
    for jogo_numero in range(1, 15):
        if adicionar_campo(jogo_numero):
            sucessos += 1
    
    print(f"\n🎯 RESULTADO: {sucessos}/{total} jogos atualizados com sucesso!")
    
    if sucessos == total:
        print("🎉 TODOS OS JOGOS FORAM ATUALIZADOS!")
    else:
        print("⚠️ ALGUNS JOGOS PRECISAM DE ATENÇÃO.")

if __name__ == "__main__":
    main()
