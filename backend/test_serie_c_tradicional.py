#!/usr/bin/env python3
"""
Teste do sistema de Série C via tabela tradicional
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auto_classificacao import AutoClassificacao

def testar_serie_c_tradicional():
    """Testa o sistema completo da Série C"""
    
    print("🧪 TESTANDO SÉRIE C VIA TABELA TRADICIONAL")
    print("=" * 50)
    
    try:
        # Criar instância
        auto_class = AutoClassificacao()
        
        # Testar leitura da tabela tradicional
        print("\n📊 Lendo tabela tradicional Série C...")
        clubes = auto_class.ler_tabela_tradicional_serie_c()
        
        if clubes:
            print(f"✅ {len(clubes)} clubes lidos com sucesso!")
            
            # Separar por grupos
            grupoB = [c for c in clubes if c['grupo'] == 'B']
            grupoC = [c for c in clubes if c['grupo'] == 'C']
            
            print(f"\n🏆 GRUPO B ({len(grupoB)} clubes):")
            for clube in grupoB:
                status = "🔵 SEMI-FINAL" if clube['posicao'] <= 2 else "⚫ Eliminado"
                print(f"{clube['posicao']}º {clube['time']:15s} - {clube['pontos']:2d}pts - {status}")
            
            print(f"\n🏆 GRUPO C ({len(grupoC)} clubes):")
            for clube in grupoC:
                status = "🔵 SEMI-FINAL" if clube['posicao'] <= 2 else "⚫ Eliminado"
                print(f"{clube['posicao']}º {clube['time']:15s} - {clube['pontos']:2d}pts - {status}")
            
            # Mostrar classificados para semi-final
            print(f"\n🏆 CLASSIFICADOS PARA SEMI-FINAL:")
            print(f"Grupo B: {grupoB[0]['time']} (1º) vs {grupoB[1]['time']} (2º)")
            print(f"Grupo C: {grupoC[0]['time']} (1º) vs {grupoC[1]['time']} (2º)")
            
            # Testar processamento
            print(f"\n🔄 Testando processamento...")
            resultado = auto_class.processar_serie_c_tradicional()
            
            if resultado:
                print("✅ Processamento funcionando!")
                print("🌐 Acesse: http://localhost:5000/loteca")
                print("📊 Vá na aba 'Panorama dos Campeonatos'")
            else:
                print("❌ Erro no processamento")
                
        else:
            print("❌ Nenhum clube encontrado")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_serie_c_tradicional()


