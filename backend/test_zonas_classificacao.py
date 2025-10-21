#!/usr/bin/env python3
"""
Teste das zonas de classificação baseadas na tabela do jornal esportivo
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auto_classificacao import AutoClassificacao

def testar_zonas_classificacao():
    """Testa as zonas de classificação"""
    
    print("🧪 TESTANDO ZONAS DE CLASSIFICAÇÃO")
    print("=" * 50)
    
    try:
        # Criar instância
        auto_class = AutoClassificacao()
        
        # Testar leitura da tabela tradicional
        print("\n📊 Lendo tabela tradicional...")
        clubes = auto_class.ler_tabela_tradicional_serie_a()
        
        if clubes:
            print(f"✅ {len(clubes)} clubes lidos com sucesso!")
            
            # Mostrar zonas de classificação
            print("\n🏆 ZONAS DE CLASSIFICAÇÃO:")
            print("=" * 60)
            
            for clube in clubes:
                posicao = clube['posicao']
                time = clube['time']
                zona = clube['zona']
                
                # Determinar cor da zona
                if zona == 'Libertadores':
                    cor = "🔵 (azul)"
                elif zona == 'Pré-Libertadores':
                    cor = "🔷 (azul claro)"
                elif zona == 'Sul-Americana':
                    cor = "🟢 (verde)"
                elif zona == 'Zona de Rebaixamento':
                    cor = "🔴 (vermelho)"
                else:
                    cor = "⚫ (preto)"
                
                print(f"{posicao:2d}º {time:20s} - {zona:20s} {cor}")
            
            # Mostrar resumo das zonas
            print("\n📋 RESUMO DAS ZONAS:")
            print("🔵 Libertadores (1º-4º):", [c['time'] for c in clubes if c['zona'] == 'Libertadores'])
            print("🔷 Pré-Libertadores (5º-6º):", [c['time'] for c in clubes if c['zona'] == 'Pré-Libertadores'])
            print("🟢 Sul-Americana (7º-12º):", [c['time'] for c in clubes if c['zona'] == 'Sul-Americana'])
            print("⚫ Meio de tabela (13º-16º):", [c['time'] for c in clubes if c['zona'] == 'Meio de tabela'])
            print("🔴 Zona de Rebaixamento (17º-20º):", [c['time'] for c in clubes if c['zona'] == 'Zona de Rebaixamento'])
                
        else:
            print("❌ Nenhum clube encontrado")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_zonas_classificacao()
