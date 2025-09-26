#!/usr/bin/env python3
"""Script para testar e verificar a Central de Dados"""

from models.central_dados import CentralDados

def main():
    print("🔍 Verificando Central de Dados...")
    
    db = CentralDados()
    
    # Stats do sistema
    print("\n📊 Estatísticas do Sistema:")
    stats = db.get_estatisticas_sistema()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Exemplo: Flamengo
    print("\n🏆 Exemplo: Flamengo (ID 262)")
    fla_stats = db.obter_stats_clube(262)
    if fla_stats:
        print(f"  Atletas: {fla_stats.get('total_atletas', 'N/A')}")
        print(f"  % Prováveis: {fla_stats.get('pct_provaveis', 0):.1f}%")
        print(f"  Média Pontos: {fla_stats.get('media_pontos_elenco', 0):.2f}")
        print(f"  Preço Médio: C$ {fla_stats.get('preco_medio', 0):.2f}")
        print(f"  Rating: {fla_stats.get('rating', 0):.3f}")
        print(f"  Fonte: {fla_stats.get('fonte', 'N/A')}")
    else:
        print("  ❌ Flamengo não encontrado!")
    
    # Exemplo: Um clube da Série B
    print("\n⚽ Exemplo: Sport (ID 292) - Série B")
    sport_stats = db.obter_stats_clube(292)
    if sport_stats:
        print(f"  Atletas: {sport_stats.get('total_atletas', 'N/A')}")
        print(f"  % Prováveis: {sport_stats.get('pct_provaveis', 0):.1f}%")
        print(f"  Fonte: {sport_stats.get('fonte', 'N/A')}")
    else:
        print("  ❌ Sport não encontrado!")
    
    # Verificar se o banco foi criado
    print(f"\n💾 Banco de dados: {db.db_path}")
    import os
    if os.path.exists(db.db_path):
        size = os.path.getsize(db.db_path)
        print(f"  Tamanho: {size:,} bytes")
    else:
        print("  ❌ Arquivo não encontrado!")
    
    print("\n✅ Verificação concluída!")

if __name__ == "__main__":
    main()
