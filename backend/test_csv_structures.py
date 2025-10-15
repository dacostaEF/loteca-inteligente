#!/usr/bin/env python3
"""
Teste para verificar a detecção automática das estruturas de CSV
"""

def test_csv_structure_detection():
    """Testar detecção automática de estruturas CSV"""
    
    print("🧪 TESTE: Detecção Automática de Estruturas CSV")
    print("=" * 60)
    
    # Teste 1: CSV Antigo (Corinthians vs Atletico-MG)
    csv_antigo = """Data,mandante,placar, visitante,vencedor,Rodada,Competição
24/5/25,Atlético Mineiro,0-0,Corinthians,Corinthians,R10,Brasileirão 2025"""
    
    print("📊 TESTE 1: CSV Antigo")
    print("-" * 30)
    linhas_antigo = csv_antigo.strip().split('\n')
    partes_antigo = linhas_antigo[1].split(',')
    
    print(f"Cabeçalho: {linhas_antigo[0]}")
    print(f"Partes: {len(partes_antigo)} - {partes_antigo}")
    
    # Detectar estrutura
    if len(partes_antigo) == 7 and 'vencedor' in linhas_antigo[0].lower():
        print("✅ Estrutura 1 detectada: CSV Antigo")
        print(f"  Vencedor na coluna 4: {partes_antigo[4]}")
    else:
        print("❌ Estrutura 1 não detectada")
    
    print()
    
    # Teste 2: CSV Novo (Flamengo vs Palmeiras)
    csv_novo = """Data,Time da Casa,Placar,Time Visitante,Vencedor,Campeonato,Resultado (Flamengo)
25/05/2025,Palmeiras,0-2,Flamengo,Flamengo,Brasileirão 2025,Vitória"""
    
    print("📊 TESTE 2: CSV Novo")
    print("-" * 30)
    linhas_novo = csv_novo.strip().split('\n')
    partes_novo = linhas_novo[1].split(',')
    
    print(f"Cabeçalho: {linhas_novo[0]}")
    print(f"Partes: {len(partes_novo)} - {partes_novo}")
    
    # Detectar estrutura
    if len(partes_novo) == 7 and 'time da casa' in linhas_novo[0].lower():
        print("✅ Estrutura 2 detectada: CSV Novo")
        print(f"  Vencedor na coluna 4: {partes_novo[4]}")
    else:
        print("❌ Estrutura 2 não detectada")
    
    print()
    
    # Teste 3: CSV Diferente (Corinthians vs Flamengo)
    csv_diferente = """data,mandante,mandante_nome,placar,visitante,visitante_nome,resultado_corinthians,rodada,competicao
2025-09-28,Corinthians,Corinthians,1-2,Flamengo,Flamengo,D,R25,Brasileirão 2025"""
    
    print("📊 TESTE 3: CSV Diferente")
    print("-" * 30)
    linhas_diferente = csv_diferente.strip().split('\n')
    partes_diferente = linhas_diferente[1].split(',')
    
    print(f"Cabeçalho: {linhas_diferente[0]}")
    print(f"Partes: {len(partes_diferente)} - {partes_diferente}")
    
    # Detectar estrutura
    if len(partes_diferente) >= 8 and 'resultado_' in linhas_diferente[0].lower():
        print("✅ Estrutura 3 detectada: CSV Diferente")
        print(f"  Resultado na coluna 6: {partes_diferente[6]}")
    else:
        print("❌ Estrutura 3 não detectada")
    
    print()
    
    # Teste de mapeamento de resultados
    print("🎯 TESTE DE MAPEAMENTO DE RESULTADOS")
    print("-" * 40)
    
    # Simular dados do Flamengo vs Palmeiras
    confrontos_teste = [
        {'mandante_nome': 'Palmeiras', 'vencedor': 'Flamengo', 'resultado': ''},
        {'mandante_nome': 'Flamengo', 'vencedor': 'Empate', 'resultado': ''},
        {'mandante_nome': 'Palmeiras', 'vencedor': 'Palmeiras', 'resultado': ''},
        {'mandante_nome': 'Flamengo', 'vencedor': 'Flamengo', 'resultado': ''},
        {'mandante_nome': 'Palmeiras', 'vencedor': 'Empate', 'resultado': ''}
    ]
    
    for i, confronto in enumerate(confrontos_teste, 1):
        vencedor_lower = confronto['vencedor'].lower().strip()
        if 'empate' in vencedor_lower:
            confronto['resultado'] = 'E'
        else:
            mandante_lower = confronto['mandante_nome'].lower().strip()
            if vencedor_lower in mandante_lower:
                confronto['resultado'] = 'V'  # Time da casa venceu
            else:
                confronto['resultado'] = 'D'  # Time visitante venceu
        
        print(f"Confronto {i}: {confronto['mandante_nome']} vs {confronto['vencedor']} → {confronto['resultado']}")
    
    # Gerar sequência
    sequencia = '-'.join([c['resultado'] for c in confrontos_teste])
    print(f"\n🎯 Sequência final: {sequencia}")
    
    # Verificar se está correta
    sequencia_esperada = "D-E-D-V-E"
    if sequencia == sequencia_esperada:
        print("✅ MAPEAMENTO CORRETO!")
    else:
        print(f"❌ MAPEAMENTO INCORRETO! Esperado: {sequencia_esperada}")

if __name__ == "__main__":
    test_csv_structure_detection()
