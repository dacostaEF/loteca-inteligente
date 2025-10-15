#!/usr/bin/env python3
"""
Teste simples para verificar se a leitura da coluna Vencedor está funcionando
"""

def test_vencedor_simples():
    """Teste simples da coluna Vencedor"""
    
    print("🧪 TESTE SIMPLES: Coluna Vencedor")
    print("=" * 50)
    
    # Dados da sua tabela (primeiros 5 confrontos)
    confrontos_teste = [
        {'data': '25/05/2025', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Flamengo'},
        {'data': '8/11/24', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Empate'},
        {'data': '8/7/24', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Palmeiras'},
        {'data': '31/07/2024', 'mandante': 'Flamengo', 'visitante': 'Palmeiras', 'vencedor': 'Flamengo'},
        {'data': '21/04/2024', 'mandante': 'Palmeiras', 'visitante': 'Flamengo', 'vencedor': 'Empate'}
    ]
    
    print("📊 PROCESSANDO CONFRONTOS:")
    print("-" * 50)
    
    sequencia = ""
    for i, confronto in enumerate(confrontos_teste, 1):
        vencedor = confronto['vencedor'].strip()
        mandante = confronto['mandante'].lower().strip()
        
        # Lógica simplificada
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
        
        print(f"Confronto {i}: {confronto['mandante']} vs {confronto['visitante']}")
        print(f"  Vencedor: {vencedor}")
        print(f"  Resultado: {resultado}")
        print()
        
        sequencia += resultado + '-'
    
    # Remover último hífen
    if sequencia.endswith('-'):
        sequencia = sequencia[:-1]
    
    print("🎯 SEQUÊNCIA FINAL:")
    print(f"  {sequencia}")
    print()
    
    # Verificar se está correto
    sequencia_esperada = "D-E-D-V-E"  # Baseado nos dados
    
    if sequencia == sequencia_esperada:
        print("✅ TESTE PASSOU: Sequência correta!")
        print("🎉 A coluna Vencedor está sendo lida corretamente!")
    else:
        print("❌ TESTE FALHOU: Sequência incorreta!")
        print(f"  Esperado: {sequencia_esperada}")
        print(f"  Obtido: {sequencia}")
    
    return sequencia == sequencia_esperada

if __name__ == "__main__":
    test_vencedor_simples()
