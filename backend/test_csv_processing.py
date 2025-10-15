#!/usr/bin/env python3
"""
Teste para verificar o processamento correto do CSV Flamengo vs Palmeiras
"""

import os
import sys

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(__file__))

def test_csv_processing():
    """Testar o processamento do CSV Flamengo vs Palmeiras"""
    
    # Simular dados do CSV Flamengo vs Palmeiras
    csv_data = """Data,Time da Casa,Placar,Time Visitante,Vencedor,Campeonato,Resultado (Flamengo)
25/05/2025,Palmeiras,0-2,Flamengo,Flamengo,Brasileirão 2025,Vitória
8/11/24,Flamengo,1-1,Palmeiras,Empate,Brasileirão 2024,Empate
8/7/24,Palmeiras,1-0,Flamengo,Palmeiras,Copa do Brasil 2024,Derrota
31/07/2024,Flamengo,2-0,Palmeiras,Flamengo,Copa do Brasil 2024,Vitória
21/04/2024,Palmeiras,0-0,Flamengo,Empate,Brasileirão 2024,Empate"""
    
    print("🧪 TESTE: Processamento do CSV Flamengo vs Palmeiras")
    print("=" * 60)
    
    # Processar linha por linha
    linhas = csv_data.strip().split('\n')
    confrontos = []
    
    for i, linha in enumerate(linhas[1:], 1):  # Pular cabeçalho
        partes = linha.split(',')
        if len(partes) >= 5:
            confronto = {
                'data': partes[0].strip(),
                'mandante_nome': partes[1].strip(),
                'placar': partes[2].strip(),
                'visitante_nome': partes[3].strip(),
                'vencedor': partes[4].strip(),
                'resultado': '',
                'campeonato': partes[5].strip() if len(partes) > 5 else '',
                'resultado_time': partes[6].strip() if len(partes) > 6 else ''
            }
            
            # Aplicar lógica de mapeamento
            vencedor_lower = confronto['vencedor'].lower().strip()
            if 'empate' in vencedor_lower:
                confronto['resultado'] = 'E'
            else:
                mandante_lower = confronto['mandante_nome'].lower().strip()
                if vencedor_lower in mandante_lower:
                    confronto['resultado'] = 'V'  # Time da casa venceu
                else:
                    confronto['resultado'] = 'D'  # Time visitante venceu
            
            confrontos.append(confronto)
    
    # Exibir resultados
    print("📊 RESULTADOS DO PROCESSAMENTO:")
    print("-" * 60)
    
    sequencia = ""
    for i, confronto in enumerate(confrontos, 1):
        print(f"Confronto {i}:")
        print(f"  Data: {confronto['data']}")
        print(f"  Mandante: {confronto['mandante_nome']}")
        print(f"  Visitante: {confronto['visitante_nome']}")
        print(f"  Placar: {confronto['placar']}")
        print(f"  Vencedor: {confronto['vencedor']}")
        print(f"  Resultado (V/E/D): {confronto['resultado']}")
        print(f"  Resultado Time: {confronto['resultado_time']}")
        print()
        
        sequencia += confronto['resultado'] + '-'
    
    # Remover último hífen
    if sequencia.endswith('-'):
        sequencia = sequencia[:-1]
    
    print("🎯 SEQUÊNCIA FINAL:")
    print(f"  {sequencia}")
    print()
    
    # Verificar se a sequência está correta
    sequencia_esperada = "D-E-D-V-E"  # Baseado nos dados de teste
    
    if sequencia == sequencia_esperada:
        print("✅ TESTE PASSOU: Sequência está correta!")
    else:
        print("❌ TESTE FALHOU: Sequência incorreta!")
        print(f"  Esperado: {sequencia_esperada}")
        print(f"  Obtido: {sequencia}")
    
    return sequencia == sequencia_esperada

if __name__ == "__main__":
    test_csv_processing()
