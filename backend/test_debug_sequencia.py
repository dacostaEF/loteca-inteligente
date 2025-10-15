#!/usr/bin/env python3
"""
Teste para debugar a sequência e encontrar o problema
"""

def test_debug_sequencia():
    """Debugar a sequência para encontrar o problema"""
    
    print("🔍 DEBUG: Sequência Flamengo vs Palmeiras")
    print("=" * 60)
    
    # Dados reais do CSV Flamengo vs Palmeiras (primeiros 10 confrontos em ordem decrescente)
    confrontos_teste = [
        {'data': '25/05/2025', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Flamengo', 'placar': '0-2'},
        {'data': '8/11/24', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Empate', 'placar': '1-1'},
        {'data': '8/7/24', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Palmeiras', 'placar': '1-0'},
        {'data': '31/07/2024', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Flamengo', 'placar': '2-0'},
        {'data': '21/04/2024', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Empate', 'placar': '0-0'},
        {'data': '11/8/23', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Flamengo', 'placar': '3-0'},
        {'data': '7/8/23', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Empate', 'placar': '1-1'},
        {'data': '28/01/2023', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Palmeiras', 'placar': '4-3'},
        {'data': '21/08/2022', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Empate', 'placar': '1-1'},
        {'data': '20/04/2022', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Empate', 'placar': '0-0'}
    ]
    
    print("📊 ANÁLISE DETALHADA DOS CONFRONTOS:")
    print("-" * 60)
    
    sequencia = ""
    for i, confronto in enumerate(confrontos_teste, 1):
        vencedor = confronto['vencedor'].strip()
        mandante = confronto['mandante'].lower().strip()
        visitante = confronto['visitante'].lower().strip()
        
        print(f"\n🔍 CONFRONTO {i}: {confronto['data']}")
        print(f"   Mandante: {confronto['mandante']}")
        print(f"   Visitante: {confronto['visitante']}")
        print(f"   Vencedor: {vencedor}")
        print(f"   Placar: {confronto['placar']}")
        
        # Lógica de processamento
        if 'empate' in vencedor.lower():
            resultado = 'E'
            print(f"   → EMPATE detectado: {resultado}")
        else:
            # Se o vencedor contém palavras do mandante, time da casa venceu
            palavras_mandante = mandante.split(' ')
            vencedor_contem_mandante = any(palavra in vencedor.lower() for palavra in palavras_mandante if len(palavra) > 2)
            
            if vencedor_contem_mandante:
                resultado = 'V'  # Time da casa venceu
                print(f"   → VITÓRIA DO MANDANTE: {resultado}")
            else:
                resultado = 'D'  # Time visitante venceu
                print(f"   → VITÓRIA DO VISITANTE: {resultado}")
        
        sequencia += resultado + '-'
        print(f"   🎯 Resultado final: {resultado}")
    
    # Remover último hífen
    if sequencia.endswith('-'):
        sequencia = sequencia[:-1]
    
    print(f"\n🎯 SEQUÊNCIA FINAL: {sequencia}")
    
    # Contar resultados
    vitorias = sequencia.count('V')
    empates = sequencia.count('E')
    derrotas = sequencia.count('D')
    
    print(f"\n📈 CONTAGEM:")
    print(f"   V (Vitórias): {vitorias}")
    print(f"   E (Empates): {empates}")
    print(f"   D (Derrotas): {derrotas}")
    print(f"   Total: {vitorias + empates + derrotas}")
    
    # Analisar confronto por confronto
    print(f"\n🔍 ANÁLISE CONFRONTO POR CONFRONTO:")
    print("-" * 60)
    
    vitorias_flamengo = 0
    empates_total = 0
    vitorias_palmeiras = 0
    
    for i, confronto in enumerate(confrontos_teste):
        vencedor = confronto['vencedor'].lower().strip()
        mandante = confronto['mandante'].lower().strip()
        
        if 'empate' in vencedor:
            empates_total += 1
            print(f"Confronto {i+1}: EMPATE")
        else:
            palavras_mandante = mandante.split(' ')
            vencedor_contem_mandante = any(palavra in vencedor for palavra in palavras_mandante if len(palavra) > 2)
            
            if vencedor_contem_mandante:
                # Time da casa venceu
                if 'palmeiras' in mandante:
                    vitorias_palmeiras += 1
                    print(f"Confronto {i+1}: VITÓRIA PALMEIRAS (mandante)")
                else:
                    vitorias_flamengo += 1
                    print(f"Confronto {i+1}: VITÓRIA FLAMENGO (mandante)")
            else:
                # Time visitante venceu
                if 'palmeiras' in mandante:
                    vitorias_flamengo += 1
                    print(f"Confronto {i+1}: VITÓRIA FLAMENGO (visitante)")
                else:
                    vitorias_palmeiras += 1
                    print(f"Confronto {i+1}: VITÓRIA PALMEIRAS (visitante)")
    
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   Vitórias Flamengo: {vitorias_flamengo}")
    print(f"   Empates: {empates_total}")
    print(f"   Vitórias Palmeiras: {vitorias_palmeiras}")
    print(f"   Total: {vitorias_flamengo + empates_total + vitorias_palmeiras}")
    
    resumo = f"{vitorias_flamengo}V-{empates_total}E-{vitorias_palmeiras}D"
    print(f"\n🎯 RESUMO FINAL: {resumo}")
    
    # Verificar se está correto
    if vitorias_flamengo == 3 and empates_total == 5 and vitorias_palmeiras == 2:
        print("✅ RESULTADO CORRETO: 3V-5E-2D")
    else:
        print("❌ RESULTADO INCORRETO!")
        print("   Esperado: 3V-5E-2D")
        print(f"   Obtido: {resumo}")
    
    return vitorias_flamengo == 3 and empates_total == 5 and vitorias_palmeiras == 2

if __name__ == "__main__":
    test_debug_sequencia()
