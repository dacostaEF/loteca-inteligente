#!/usr/bin/env python3
"""
Script para atualizar as tabelas AGORA MESMO
"""

import os
import sys
import json
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def atualizar_tabelas_agora():
    """Atualiza as tabelas da Série A e B agora mesmo"""
    
    print("🚀 ATUALIZANDO TABELAS AGORA MESMO...")
    print("=" * 50)
    
    try:
        # Importar o integrador
        from services.classificacao_integrador import ClassificacaoIntegrador
        
        # Criar integrador
        integrador = ClassificacaoIntegrador()
        
        # Atualizar Série A
        print("\n📊 ATUALIZANDO SÉRIE A...")
        serie_a_ok = integrador.atualizar_serie_a_automatica()
        
        if serie_a_ok:
            print("✅ Série A atualizada com sucesso!")
        else:
            print("❌ Erro ao atualizar Série A")
        
        # Atualizar Série B
        print("\n📊 ATUALIZANDO SÉRIE B...")
        serie_b_ok = integrador.atualizar_serie_b_automatica()
        
        if serie_b_ok:
            print("✅ Série B atualizada com sucesso!")
        else:
            print("❌ Erro ao atualizar Série B")
        
        # Resultado final
        print("\n" + "=" * 50)
        if serie_a_ok and serie_b_ok:
            print("🎯 TODAS AS TABELAS ATUALIZADAS COM SUCESSO!")
            print("🌐 Acesse: http://localhost:5000/loteca")
            print("📊 Vá na aba 'Panorama dos Campeonatos'")
        else:
            print("⚠️ ALGUMAS TABELAS FALHARAM")
        
        return serie_a_ok and serie_b_ok
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        return False

if __name__ == "__main__":
    sucesso = atualizar_tabelas_agora()
    
    if sucesso:
        print("\n🎉 PRONTO! As tabelas estão atualizadas!")
    else:
        print("\n💥 ALGO DEU ERRADO! Verifique os erros acima.")

