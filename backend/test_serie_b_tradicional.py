#!/usr/bin/env python3
"""
Teste do sistema de Série B via tabela tradicional
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auto_classificacao import AutoClassificacao
from services.classificacao_integrador import ClassificacaoIntegrador

def testar_serie_b_tradicional():
    """Testa o sistema completo da Série B"""
    
    print("🧪 TESTANDO SÉRIE B VIA TABELA TRADICIONAL")
    print("=" * 50)
    
    try:
        # Criar instância
        auto_class = AutoClassificacao()
        
        # Testar leitura da tabela tradicional
        print("\n📊 Lendo tabela tradicional Série B...")
        clubes = auto_class.ler_tabela_tradicional_serie_b()
        
        if clubes:
            print(f"✅ {len(clubes)} clubes lidos com sucesso!")
            
            # Mostrar TOP 5
            print("\n🏆 TOP 5 SÉRIE B:")
            for i, clube in enumerate(clubes[:5], 1):
                print(f"{i}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")
            
            # Mostrar todos os clubes
            print(f"\n📋 TODOS OS {len(clubes)} CLUBES:")
            for clube in clubes:
                print(f"{clube['posicao']:2d}º {clube['time']:20s} - {clube['pontos']:2d}pts - {clube['jogos']:2d}J - {clube['vitorias']:2d}V-{clube['empates']:2d}E-{clube['derrotas']:2d}D - {clube['gols_pro']:2d}GP-{clube['gols_contra']:2d}GC - {clube['zona']}")
            
            # Testar integração completa
            print("\n🔄 Testando integração completa...")
            integrador = ClassificacaoIntegrador()
            sucesso = integrador.atualizar_serie_b_automatica()
            
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
    testar_serie_b_tradicional()

