#!/usr/bin/env python3
"""
Teste específico para verificar o carregamento do CSV Atlético de Madrid vs Osasuna
"""

import csv
import os
from pathlib import Path

def testar_csv_atletico_osasuna():
    """Testa o carregamento do CSV Atlético de Madrid vs Osasuna"""
    print("🔍 TESTANDO CSV: Atlético de Madrid vs Osasuna")
    print("=" * 60)
    
    # Caminho do arquivo CSV
    caminho_csv = Path("models/Confrontos/Atletico-de-Madrid_vs_Osasuna.csv")
    
    if not caminho_csv.exists():
        print(f"❌ Arquivo não encontrado: {caminho_csv}")
        return False
    
    print(f"✅ Arquivo encontrado: {caminho_csv}")
    
    # Ler arquivo CSV
    confrontos = []
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                confrontos.append(row)
        
        print(f"📊 Total de confrontos encontrados: {len(confrontos)}")
        
        # Pegar últimos 10 confrontos
        ultimos_10 = confrontos[:10]
        
        print("\n📋 ÚLTIMOS 10 CONFRONTOS:")
        print("-" * 100)
        
        sequencia = ""
        vitorias_atletico = 0
        empates = 0
        derrotas_atletico = 0
        
        for i, confronto in enumerate(ultimos_10, 1):
            data = confronto.get('Data', 'N/A')
            mandante = confronto.get('mandante', 'N/A')
            placar = confronto.get('placar', 'N/A')
            visitante = confronto.get(' visitante', 'N/A').strip()
            vencedor = confronto.get('vencedor', 'N/A')
            
            # Determinar resultado para Atlético de Madrid
            if vencedor == 'Atlético de Madrid':
                resultado = 'V'
                vitorias_atletico += 1
            elif vencedor == 'Empate':
                resultado = 'E'
                empates += 1
            else:  # Osasuna venceu
                resultado = 'D'
                derrotas_atletico += 1
            
            sequencia += resultado + "-"
            
            print(f"{i:2d}. {data} | {mandante} {placar} {visitante} | Vencedor: {vencedor} | Resultado Atlético: {resultado}")
        
        # Remover último hífen
        sequencia = sequencia.rstrip('-')
        
        print("\n📊 RESULTADOS CALCULADOS:")
        print(f"🔄 Sequência: {sequencia}")
        print(f"📈 Resumo: {vitorias_atletico}V-{empates}E-{derrotas_atletico}D")
        
        # Verificar se está correto
        sequencia_esperada = "D-V-D-V-V-V-V-V-V-V"
        resumo_esperado = "9V-0E-1D"
        
        print(f"\n✅ VERIFICAÇÃO:")
        print(f"Sequência esperada: {sequencia_esperada}")
        print(f"Sequência calculada: {sequencia}")
        print(f"✅ Sequência correta: {'SIM' if sequencia == sequencia_esperada else 'NÃO'}")
        
        print(f"Resumo esperado: {resumo_esperado}")
        print(f"Resumo calculado: {vitorias_atletico}V-{empates}E-{derrotas_atletico}D")
        print(f"✅ Resumo correto: {'SIM' if f'{vitorias_atletico}V-{empates}E-{derrotas_atletico}D' == resumo_esperado else 'NÃO'}")
        
        return sequencia == sequencia_esperada and f'{vitorias_atletico}V-{empates}E-{derrotas_atletico}D' == resumo_esperado
        
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE DO CSV ATLÉTICO DE MADRID VS OSASUNA")
    print("=" * 70)
    
    sucesso = testar_csv_atletico_osasuna()
    
    if sucesso:
        print("\n🎉 TESTE PASSOU! CSV está correto!")
        print("✅ Dados do Jogo 5 (Atlético de Madrid vs Osasuna) estão consistentes!")
    else:
        print("\n❌ TESTE FALHOU! Verificar dados do CSV!")
    
    return sucesso

if __name__ == "__main__":
    main()
