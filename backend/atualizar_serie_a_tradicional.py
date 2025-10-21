#!/usr/bin/env python3
"""
Script para atualizar Série A usando tabela tradicional
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def atualizar_serie_a_tradicional():
    """Atualiza Série A usando o CSV da tabela tradicional"""
    
    print("🚀 ATUALIZANDO SÉRIE A VIA TABELA TRADICIONAL")
    print("=" * 50)
    
    try:
        from services.classificacao_integrador import ClassificacaoIntegrador
        
        # Criar integrador
        integrador = ClassificacaoIntegrador()
        
        # Atualizar Série A
        print("\n📊 ATUALIZANDO SÉRIE A...")
        serie_a_ok = integrador.atualizar_serie_a_automatica()
        
        if serie_a_ok:
            print("✅ Série A atualizada com sucesso via tabela tradicional!")
            print("🌐 Acesse: http://localhost:5000/loteca")
            print("📊 Vá na aba 'Panorama dos Campeonatos'")
        else:
            print("❌ Erro ao atualizar Série A")
        
        return serie_a_ok
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = atualizar_serie_a_tradicional()
    
    if sucesso:
        print("\n🎉 PRONTO! Série A atualizada via tabela tradicional!")
    else:
        print("\n💥 ALGO DEU ERRADO! Verifique os erros acima.")
