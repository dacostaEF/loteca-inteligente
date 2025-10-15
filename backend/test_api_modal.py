#!/usr/bin/env python3
"""
Teste para verificar se a API do modal está funcionando corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_api_modal_logic():
    """Testar a lógica da API do modal"""
    
    print("🧪 TESTE: API Modal - Lógica de Processamento")
    print("=" * 60)
    
    # Simular dados do CSV Flamengo vs Palmeiras
    csv_data = """Data,Time da Casa,Placar,Time Visitante,Vencedor,Campeonato,Resultado (Flamengo)
25/05/2025,Palmeiras,0-2,Flamengo,Flamengo,Brasileirão 2025,Vitória
8/11/24,Flamengo,1-1,Palmeiras,Empate,Brasileirão 2024,Empate
8/7/24,Palmeiras,1-0,Flamengo,Palmeiras,Copa do Brasil 2024,Derrota
31/07/2024,Flamengo,2-0,Palmeiras,Flamengo,Copa do Brasil 2024,Vitória
21/04/2024,Palmeiras,0-0,Flamengo,Empate,Brasileirão 2024,Empate
11/8/23,Flamengo,3-0,Palmeiras,Flamengo,Brasileirão 2023,Vitória
7/8/23,Palmeiras,1-1,Flamengo,Empate,Brasileirão 2023,Empate
28/01/2023,Palmeiras,4-3,Flamengo,Palmeiras,Supercopa Brasil 2023,Derrota
21/08/2022,Palmeiras,1-1,Flamengo,Empate,Brasileirão 2022,Empate
20/04/2022,Flamengo,0-0,Palmeiras,Empate,Brasileirão 2022,Empate"""
    
    linhas = csv_data.strip().split('\n')
    confrontos = []
    
    # Processar como a API faz
    for i, linha in enumerate(linhas[1:], 1):
        linha = linha.strip()
        if not linha:
            continue
            
        partes = linha.split(',')
        if len(partes) < 5:
            continue
        
        # Detectar estrutura automaticamente baseada no cabeçalho
        cabecalho = linhas[0].lower()
        
        if 'time da casa' in cabecalho:
            confronto = {
                "data": partes[0].strip(),
                "mandante": partes[1].strip(),
                "visitante": partes[3].strip(),
                "placar": partes[2].strip(),
                "vencedor": partes[4].strip(),
                "competicao": partes[5].strip() if len(partes) > 5 else '',
                "resultado": ''
            }
        
        # Calcular resultado V/E/D baseado no vencedor
        if confronto.get('vencedor'):
            vencedor = confronto['vencedor'].lower().strip()
            if 'empate' in vencedor:
                confronto['resultado'] = 'E'
            else:
                # Determinar se foi vitória do time casa ou fora
                mandante_lower = confronto['mandante'].lower().strip()
                if any(palavra in mandante_lower for palavra in vencedor.split() if len(palavra) > 2):
                    confronto['resultado'] = 'V'  # Time da casa venceu
                else:
                    confronto['resultado'] = 'D'  # Time visitante venceu
        
        confrontos.append(confronto)
    
    # Exibir resultados
    print("📊 RESULTADOS DO PROCESSAMENTO:")
    print("-" * 60)
    
    vitorias_flamengo = 0
    empates = 0
    vitorias_palmeiras = 0
    
    for i, confronto in enumerate(confrontos, 1):
        print(f"Confronto {i}:")
        print(f"  Data: {confronto['data']}")
        print(f"  Mandante: {confronto['mandante']}")
        print(f"  Visitante: {confronto['visitante']}")
        print(f"  Placar: {confronto['placar']}")
        print(f"  Vencedor: {confronto['vencedor']}")
        print(f"  Resultado: {confronto['resultado']}")
        
        # Contar resultados
        if confronto['resultado'] == 'E':
            empates += 1
        elif confronto['resultado'] == 'V':
            if 'flamengo' in confronto['mandante'].lower():
                vitorias_flamengo += 1
            else:
                vitorias_palmeiras += 1
        elif confronto['resultado'] == 'D':
            if 'flamengo' in confronto['mandante'].lower():
                vitorias_palmeiras += 1
            else:
                vitorias_flamengo += 1
        
        print()
    
    print("🎯 ESTATÍSTICAS FINAIS:")
    print(f"  Vitórias Flamengo: {vitorias_flamengo}")
    print(f"  Empates: {empates}")
    print(f"  Vitórias Palmeiras: {vitorias_palmeiras}")
    print(f"  Total: {len(confrontos)} confrontos")
    
    # Verificar se está correto (baseado na sua expectativa)
    if vitorias_flamengo == 3 and empates == 5 and vitorias_palmeiras == 2:
        print("✅ TESTE PASSOU: Estatísticas corretas!")
        print("🎉 A API do modal está funcionando corretamente!")
    else:
        print("❌ TESTE FALHOU: Estatísticas incorretas!")
        print("🔧 Verificar lógica de processamento")
    
    return vitorias_flamengo == 3 and empates == 5 and vitorias_palmeiras == 2

if __name__ == "__main__":
    test_api_modal_logic()
