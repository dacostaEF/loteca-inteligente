#!/usr/bin/env python3
"""
Teste específico para verificar a conversão dos últimos jogos
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auto_classificacao import AutoClassificacao

def testar_conversao_ultimos_jogos():
    """Testa a conversão dos últimos jogos"""
    
    print("🧪 TESTANDO CONVERSÃO DOS ÚLTIMOS JOGOS")
    print("=" * 50)
    
    try:
        # Criar instância
        auto_class = AutoClassificacao()
        
        # Testar conversões específicas
        testes = [
            ("V-V-V-V-D", "🟢-🟢-🟢-🟢-🔴"),
            ("V-E-D-V-V", "🟢-🟡-🔴-🟢-🟢"),
            ("D-E-E-E-V", "🔴-🟡-🟡-🟡-🟢"),
            ("D-E-D-V-V", "🔴-🟡-🔴-🟢-🟢"),
            ("D-D-V-D-V", "🔴-🔴-🟢-🔴-🟢"),
            ("V-D-V-D-V", "🟢-🔴-🟢-🔴-🟢"),
            ("E-V-E-V-D", "🟡-🟢-🟡-🟢-🔴"),
            ("V-D-V-V-V", "🟢-🔴-🟢-🟢-🟢"),
            ("D-V-D-D-D", "🔴-🟢-🔴-🔴-🔴"),
            ("E-E-V-D-D", "🟡-🟡-🟢-🔴-🔴"),
            ("V-E-D-V-D", "🟢-🟡-🔴-🟢-🔴"),
            ("V-D-V-E-D", "🟢-🔴-🟢-🟡-🔴"),
            ("E-E-V-D-V", "🟡-🟡-🟢-🔴-🟢"),
            ("D-D-E-V-E", "🔴-🔴-🟡-🟢-🟡"),
            ("E-D-V-E-E", "🟡-🔴-🟢-🟡-🟡"),
            ("E-E-D-V-D", "🟡-🟡-🔴-🟢-🔴"),
            ("D-V-D-V-V", "🔴-🟢-🔴-🟢-🟢"),
            ("E-D-D-D-V", "🟡-🔴-🔴-🔴-🟢"),
            ("V-D-D-V-D", "🟢-🔴-🔴-🟢-🔴"),
            ("E-D-E-E-D", "🟡-🔴-🟡-🟡-🔴")
        ]
        
        print("\n🔄 Testando conversões individuais:")
        for entrada, esperado in testes:
            resultado = auto_class.converter_ultimos_jogos(entrada)
            status = "✅" if resultado == esperado else "❌"
            print(f"{status} '{entrada}' → '{resultado}' (esperado: '{esperado}')")
        
        # Testar com dados reais
        print("\n📊 Testando com dados reais da tabela:")
        clubes = auto_class.ler_tabela_tradicional_serie_a()
        
        if clubes:
            print(f"\n✅ {len(clubes)} clubes lidos com sucesso!")
            
            # Mostrar últimos jogos dos primeiros 10 clubes
            print("\n🏆 ÚLTIMOS JOGOS DOS PRIMEIROS 10 CLUBES:")
            for clube in clubes[:10]:
                print(f"{clube['posicao']:2d}º {clube['time']:20s} - {clube['ultimos_jogos']}")
                
        else:
            print("❌ Nenhum clube encontrado")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_conversao_ultimos_jogos()


