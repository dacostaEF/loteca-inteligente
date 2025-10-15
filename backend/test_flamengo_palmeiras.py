#!/usr/bin/env python3
"""
Teste específico para Flamengo vs Palmeiras - verificar se os resultados estão corretos
"""

def test_flamengo_palmeiras():
    """Teste específico para Flamengo vs Palmeiras"""
    
    print("🧪 TESTE: Flamengo vs Palmeiras - Resultados Corretos")
    print("=" * 60)
    
    # Dados reais do CSV Flamengo vs Palmeiras (primeiros 10 confrontos)
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
    
    print("📊 PROCESSANDO CONFRONTOS:")
    print("-" * 60)
    
    # Processar cada confronto
    for i, confronto in enumerate(confrontos_teste, 1):
        vencedor = confronto['vencedor'].strip()
        mandante = confronto['mandante'].lower().strip()
        
        # Lógica de processamento
        if 'empate' in vencedor.lower():
            resultado = 'E'
        else:
            # Se o vencedor contém palavras do mandante, time da casa venceu
            palavras_mandante = mandante.split(' ')
            vencedor_contem_mandante = any(palavra in vencedor.lower() for palavra in palavras_mandante if len(palavra) > 2)
            
            if vencedor_contem_mandante:
                resultado = 'V'  # Time da casa venceu
            else:
                resultado = 'D'  # Time visitante venceu
        
        print(f"Confronto {i}: {confronto['data']} - {confronto['mandante']} vs {confronto['visitante']}")
        print(f"  Placar: {confronto['placar']}")
        print(f"  Vencedor: {vencedor}")
        print(f"  Resultado: {resultado}")
        print()
    
    # Gerar sequência
    sequencia = '-'.join([c['resultado'] for c in confrontos_teste])
    print("🎯 SEQUÊNCIA FINAL:")
    print(f"  {sequencia}")
    print()
    
    # Contar resultados
    vitorias_flamengo = 0
    empates = 0
    vitorias_palmeiras = 0
    
    for confronto in confrontos_teste:
        vencedor = confronto['vencedor'].lower().strip()
        mandante = confronto['mandante'].lower().strip()
        
        if 'empate' in vencedor:
            empates += 1
        else:
            palavras_mandante = mandante.split(' ')
            vencedor_contem_mandante = any(palavra in vencedor for palavra in palavras_mandante if len(palavra) > 2)
            
            if vencedor_contem_mandante:
                # Time da casa venceu
                if 'palmeiras' in mandante:
                    vitorias_palmeiras += 1
                else:
                    vitorias_flamengo += 1
            else:
                # Time visitante venceu
                if 'palmeiras' in mandante:
                    vitorias_flamengo += 1
                else:
                    vitorias_palmeiras += 1
    
    print("📈 ESTATÍSTICAS FINAIS:")
    print(f"  Vitórias Flamengo: {vitorias_flamengo}")
    print(f"  Empates: {empates}")
    print(f"  Vitórias Palmeiras: {vitorias_palmeiras}")
    print(f"  Total: {len(confrontos_teste)} confrontos")
    print()
    
    # Verificar se está correto (baseado na sua expectativa)
    if vitorias_flamengo == 3 and empates == 5 and vitorias_palmeiras == 2:
        print("✅ TESTE PASSOU: Estatísticas corretas!")
        print("🎉 Flamengo vs Palmeiras está funcionando perfeitamente!")
    else:
        print("❌ TESTE FALHOU: Estatísticas incorretas!")
        print("🔧 Verificar lógica de processamento")
    
    return vitorias_flamengo == 3 and empates == 5 and vitorias_palmeiras == 2

if __name__ == "__main__":
    test_flamengo_palmeiras()
