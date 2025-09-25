#!/usr/bin/env python3
"""
Script para testar o provider da Loteca com dados reais
"""
from services.loteca_provider import get_current_loteca_matches
import json

def test_loteca_data():
    print("🎯 TESTANDO DADOS REAIS DA LOTECA")
    print("=" * 50)
    
    try:
        matches = get_current_loteca_matches()
        print(f"✅ Total de jogos: {len(matches)}")
        print()
        
        # Mostrar primeiros 3 jogos
        for i, match in enumerate(matches[:3], 1):
            print(f"🎮 JOGO {i}: {match['home']} vs {match['away']}")
            print(f"   📊 Probabilidades: Casa={match['prob1']}%, Empate={match['probX']}%, Fora={match['prob2']}%")
            print(f"   🎯 Classificação: {match['classification']} | Sugestão: {match['suggestion']}")
            print(f"   📍 Local: {match.get('stadium', 'N/A')} | Data: {match.get('date', 'N/A')}")
            print(f"   🔍 Fonte: {match.get('data_source', 'N/A')}")
            
            # Mostrar stats se houver
            if 'home_stats' in match and match['home_stats'].get('total_atletas', 0) > 0:
                home_stats = match['home_stats']
                print(f"   🏠 {match['home']}: {home_stats['total_atletas']} atletas, {home_stats['pct_provaveis']}% prováveis, Rating: {home_stats['rating']}")
            
            if 'away_stats' in match and match['away_stats'].get('total_atletas', 0) > 0:
                away_stats = match['away_stats']
                print(f"   ✈️  {match['away']}: {away_stats['total_atletas']} atletas, {away_stats['pct_provaveis']}% prováveis, Rating: {away_stats['rating']}")
            
            print()
        
        # Resumo das fontes de dados
        sources = {}
        for match in matches:
            source = match.get('data_source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("📊 RESUMO DAS FONTES DE DADOS:")
        for source, count in sources.items():
            print(f"   {source}: {count} jogos")
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    test_loteca_data()
