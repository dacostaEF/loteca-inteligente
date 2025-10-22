#!/usr/bin/env python3
"""
Script para atualizar Série C usando tabela tradicional CSV
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.classificacao_integrador import ClassificacaoIntegrador

def atualizar_serie_c():
    """Atualiza Série C via tabela tradicional"""
    
    print("🚀 ATUALIZANDO SÉRIE C VIA TABELA TRADICIONAL")
    print("=" * 50)
    
    try:
        # Criar integrador
        integrador = ClassificacaoIntegrador()
        
        print("\n📊 ATUALIZANDO SÉRIE C...")
        
        # Atualizar Série C
        sucesso = integrador.atualizar_serie_c_automatica()
        
        if sucesso:
            print("✅ Série C atualizada com sucesso via tabela tradicional!")
            print("🌐 Acesse: http://localhost:5000/loteca")
            print("📊 Vá na aba 'Panorama dos Campeonatos'")
            print("\n🎉 PRONTO! Série C atualizada via tabela tradicional!")
        else:
            print("❌ Erro ao atualizar Série C")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    atualizar_serie_c()


