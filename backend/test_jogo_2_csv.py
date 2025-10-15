#!/usr/bin/env python3
"""
Teste específico para verificar o carregamento do CSV do Jogo 2 (Internacional vs Sport)
"""

import csv
import os
from pathlib import Path

def testar_csv_internacional_sport():
    """Testa o carregamento do CSV Internacional vs Sport"""
    print("🔍 TESTANDO CSV: Internacional vs Sport")
    print("=" * 50)
    
    # Caminho do arquivo CSV
    caminho_csv = Path("models/Confrontos/Internacional_vs_Sport.csv")
    
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
        print("-" * 80)
        
        sequencia = ""
        vitorias_internacional = 0
        empates = 0
        derrotas_internacional = 0
        
        for i, confronto in enumerate(ultimos_10, 1):
            data = confronto.get('Data', 'N/A')
            time_casa = confronto.get('Time da Casa', 'N/A')
            placar = confronto.get('Placar', 'N/A')
            time_visitante = confronto.get('Time Visitante', 'N/A')
            vencedor = confronto.get('Vencedor', 'N/A')
            resultado_internacional = confronto.get('Resultado (Internacional)', 'N/A')
            
            # Determinar resultado para Internacional
            if resultado_internacional == 'Vitória':
                resultado = 'V'
                vitorias_internacional += 1
            elif resultado_internacional == 'Empate':
                resultado = 'E'
                empates += 1
            elif resultado_internacional == 'Derrota':
                resultado = 'D'
                derrotas_internacional += 1
            else:
                resultado = '?'
            
            sequencia += resultado + "-"
            
            print(f"{i:2d}. {data} | {time_casa} {placar} {time_visitante} | {vencedor} | {resultado_internacional} ({resultado})")
        
        # Remover último hífen
        sequencia = sequencia.rstrip('-')
        
        print("\n📊 RESULTADOS CALCULADOS:")
        print(f"🔄 Sequência: {sequencia}")
        print(f"📈 Resumo: {vitorias_internacional}V-{empates}E-{derrotas_internacional}D")
        
        # Verificar se está correto
        sequencia_esperada = "E-V-E-D-V-D-E-E-V-V"
        resumo_esperado = "5V-3E-2D"
        
        print(f"\n✅ VERIFICAÇÃO:")
        print(f"Sequência esperada: {sequencia_esperada}")
        print(f"Sequência calculada: {sequencia}")
        print(f"✅ Sequência correta: {'SIM' if sequencia == sequencia_esperada else 'NÃO'}")
        
        print(f"Resumo esperado: {resumo_esperado}")
        print(f"Resumo calculado: {vitorias_internacional}V-{empates}E-{derrotas_internacional}D")
        print(f"✅ Resumo correto: {'SIM' if f'{vitorias_internacional}V-{empates}E-{derrotas_internacional}D' == resumo_esperado else 'NÃO'}")
        
        return sequencia == sequencia_esperada and f'{vitorias_internacional}V-{empates}E-{derrotas_internacional}D' == resumo_esperado
        
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE DO CSV INTERNACIONAL VS SPORT")
    print("=" * 60)
    
    sucesso = testar_csv_internacional_sport()
    
    if sucesso:
        print("\n🎉 TESTE PASSOU! CSV está correto!")
        print("✅ Dados do Jogo 2 (Internacional vs Sport) estão consistentes!")
    else:
        print("\n❌ TESTE FALHOU! Verificar dados do CSV!")
    
    return sucesso

if __name__ == "__main__":
    main()
