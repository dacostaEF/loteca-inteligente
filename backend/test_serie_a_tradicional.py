#!/usr/bin/env python3
"""
Teste do novo sistema de leitura da tabela tradicional
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auto_classificacao import AutoClassificacao
from services.classificacao_integrador import ClassificacaoIntegrador

def testar_serie_a_tradicional():
    """Testa a leitura da tabela tradicional"""
    
    print("🧪 TESTANDO SÉRIE A VIA TABELA TRADICIONAL")
    print("=" * 50)
    
    try:
        # Criar instância
        auto_class = AutoClassificacao()
        
        # Testar leitura da tabela tradicional
        print("\n📊 Lendo tabela tradicional...")
        clubes = auto_class.ler_tabela_tradicional_serie_a()
        
        if clubes:
            print(f"✅ {len(clubes)} clubes lidos com sucesso!")
            
            # Mostrar top 5
            print("\n🏆 TOP 5 SÉRIE A:")
            for clube in clubes[:5]:
                print(f"{clube['posicao']}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")
            
            # Mostrar todos os clubes
            print("\n📋 TODOS OS CLUBES:")
            for clube in clubes:
                print(f"{clube['posicao']:2d}º {clube['time']:20s} - {clube['pontos']:2d}pts - {clube['jogos']:2d}J - {clube['vitorias']:2d}V-{clube['empates']:2d}E-{clube['derrotas']:2d}D - {clube['gols_pro']:2d}GP-{clube['gols_contra']:2d}GC - {clube['zona']}")
            
            # Testar integração completa
            print("\n🔄 Testando integração completa...")
            integrador = ClassificacaoIntegrador()
            sucesso = integrador.atualizar_serie_a_automatica()
            
            if sucesso:
                print("✅ Integração completa funcionando!")
                print("🌐 Acesse: http://localhost:5000/loteca")
                print("📊 Vá na aba 'Panorama dos Campeonatos'")
            else:
                print("❌ Erro na integração")
                
        else:
            print("❌ Nenhum clube encontrado")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_serie_a_tradicional()


