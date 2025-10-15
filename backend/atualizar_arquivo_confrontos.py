#!/usr/bin/env python3
"""
Script para atualizar todos os arquivos JSON com o campo arquivo_confrontos
"""

import json
import os
from pathlib import Path

def atualizar_arquivo_json(caminho_arquivo, nome_arquivo_csv=""):
    """Atualiza um arquivo JSON para incluir o campo arquivo_confrontos"""
    try:
        # Ler arquivo JSON
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Verificar se o campo já existe
        if 'dados' in dados and 'arquivo_confrontos' not in dados['dados']:
            # Adicionar campo arquivo_confrontos
            dados['dados']['arquivo_confrontos'] = nome_arquivo_csv
            print(f"✅ Adicionado campo arquivo_confrontos em {caminho_arquivo}")
        else:
            print(f"⚠️ Campo arquivo_confrontos já existe em {caminho_arquivo}")
            return False
        
        # Salvar arquivo atualizado
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Arquivo atualizado: {caminho_arquivo}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar {caminho_arquivo}: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 ATUALIZANDO ARQUIVOS JSON COM CAMPO arquivo_confrontos")
    print("=" * 60)
    
    # Diretório dos arquivos JSON
    diretorio = Path("models/concurso_1216/analise_rapida")
    
    # Mapear jogos para arquivos CSV (quando disponíveis)
    mapeamento_csv = {
        "jogo_1.json": "Flamengo_vs_Palmeiras.csv",
        "jogo_2.json": "",  # Vazio - sem CSV específico
        "jogo_3.json": "Corinthians_vs_Atletico-MG.csv",
        "jogo_4.json": "",  # Vazio - sem CSV específico
        # Outros jogos sem CSV específico
    }
    
    arquivos_atualizados = 0
    
    # Processar todos os arquivos JSON
    for arquivo in diretorio.glob("jogo_*.json"):
        nome_arquivo = arquivo.name
        nome_csv = mapeamento_csv.get(nome_arquivo, "")
        
        print(f"\n📄 Processando: {nome_arquivo}")
        print(f"📁 CSV associado: {nome_csv if nome_csv else 'Nenhum'}")
        
        if atualizar_arquivo_json(arquivo, nome_csv):
            arquivos_atualizados += 1
    
    print(f"\n🎉 PROCESSO CONCLUÍDO!")
    print(f"✅ Arquivos atualizados: {arquivos_atualizados}")
    print(f"📊 Total de arquivos: {len(list(diretorio.glob('jogo_*.json')))}")

if __name__ == "__main__":
    main()
