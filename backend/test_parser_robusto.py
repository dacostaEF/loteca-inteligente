#!/usr/bin/env python3
"""
TESTE DO PARSER ROBUSTO DE CSV
==============================

Script para testar o sistema robusto de parsing de CSV
com diferentes formatos de arquivos de confrontos.
"""

import os
import sys
import json
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.csv_parser_robusto import processar_csv_confrontos

def testar_arquivo(caminho_arquivo: str, nome_teste: str):
    """Testar um arquivo específico"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTE: {nome_teste}")
    print(f"📁 Arquivo: {caminho_arquivo}")
    print(f"{'='*60}")
    
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        return False
    
    # Processar arquivo
    sucesso, confrontos, mensagem = processar_csv_confrontos(caminho_arquivo)
    
    print(f"✅ Sucesso: {sucesso}")
    print(f"📊 Mensagem: {mensagem}")
    print(f"📈 Confrontos processados: {len(confrontos)}")
    
    if confrontos:
        print(f"\n📋 Primeiros 3 confrontos:")
        for i, confronto in enumerate(confrontos[:3]):
            print(f"  {i+1}. {confronto['mandante_nome']} vs {confronto['visitante_nome']}")
            print(f"     Data: {confronto['data']}")
            print(f"     Placar: {confronto['placar']}")
            print(f"     Vencedor: {confronto['vencedor']}")
            print(f"     Resultado: {confronto['resultado']}")
            print()
        
        # Estatísticas
        vitorias = sum(1 for c in confrontos if c['resultado'] == 'V')
        empates = sum(1 for c in confrontos if c['resultado'] == 'E')
        derrotas = sum(1 for c in confrontos if c['resultado'] == 'D')
        
        print(f"📊 Estatísticas:")
        print(f"  Vitórias: {vitorias}")
        print(f"  Empates: {empates}")
        print(f"  Derrotas: {derrotas}")
        print(f"  Total: {len(confrontos)}")
    
    return sucesso

def main():
    """Função principal de teste"""
    print("🚀 INICIANDO TESTES DO PARSER ROBUSTO")
    print("="*60)
    
    # Diretório de confrontos
    confrontos_dir = Path("models/Confrontos")
    
    if not confrontos_dir.exists():
        print(f"❌ Diretório de confrontos não encontrado: {confrontos_dir}")
        return
    
    # Lista de arquivos para testar
    arquivos_teste = [
        ("Flamengo_vs_Palmeiras.csv", "Formato Novo - Flamengo vs Palmeiras"),
        ("Corinthians_vs_Atletico-MG.csv", "Formato Antigo - Corinthians vs Atlético-MG"),
        ("Corinthians_vs_Flamengo.csv", "Formato Detalhado - Corinthians vs Flamengo"),
        ("Internacional_vs_Sport.csv", "Formato Novo - Internacional vs Sport"),
        ("Atletico-de-Madrid_vs_Osasuna.csv", "Formato Novo - Atlético de Madrid vs Osasuna")
    ]
    
    resultados = []
    
    for nome_arquivo, nome_teste in arquivos_teste:
        caminho_arquivo = confrontos_dir / nome_arquivo
        sucesso = testar_arquivo(str(caminho_arquivo), nome_teste)
        resultados.append((nome_teste, sucesso))
    
    # Resumo dos resultados
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    sucessos = sum(1 for _, sucesso in resultados if sucesso)
    total = len(resultados)
    
    for nome_teste, sucesso in resultados:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"  {status}: {nome_teste}")
    
    print(f"\n🎯 RESULTADO FINAL: {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("🎉 TODOS OS TESTES PASSARAM! Parser robusto funcionando perfeitamente!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM. Verificar logs para detalhes.")

if __name__ == "__main__":
    main()
