#!/usr/bin/env python3
"""Script para visualizar dados da Central de Dados"""

import sqlite3
import os
from tabulate import tabulate

def visualizar_central():
    db_path = os.path.join("models", "central_dados.db")
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
    
    print(f"📊 Visualizando Central de Dados: {db_path}")
    print(f"💾 Tamanho: {os.path.getsize(db_path):,} bytes\n")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Estatísticas gerais
        print("📈 ESTATÍSTICAS GERAIS:")
        cursor.execute("SELECT COUNT(*) FROM clubes WHERE ativo = 1")
        total_clubes = cursor.fetchone()[0]
        print(f"  Total de clubes: {total_clubes}")
        
        cursor.execute("SELECT COUNT(*) FROM clube_stats_atuais")
        total_stats = cursor.fetchone()[0]
        print(f"  Estatísticas salvas: {total_stats}")
        
        # 2. Clubes por série
        print("\n🏆 CLUBES POR SÉRIE:")
        cursor.execute("""
            SELECT serie, COUNT(*) as total 
            FROM clubes 
            WHERE ativo = 1 
            GROUP BY serie 
            ORDER BY total DESC
        """)
        series = cursor.fetchall()
        for serie, count in series:
            print(f"  {serie}: {count} clubes")
        
        # 3. Exemplos de clubes (primeiros 10)
        print("\n⚽ EXEMPLOS DE CLUBES (primeiros 10):")
        cursor.execute("""
            SELECT c.id, c.abreviacao, c.nome_fantasia, c.estado, c.serie,
                   s.total_atletas, s.pct_provaveis, s.media_pontos_elenco
            FROM clubes c
            LEFT JOIN clube_stats_atuais s ON c.id = s.clube_id
            WHERE c.ativo = 1
            ORDER BY c.id
            LIMIT 10
        """)
        
        clubes = cursor.fetchall()
        headers = ["ID", "Sigla", "Nome", "UF", "Série", "Atletas", "% Prov", "Média"]
        
        # Formatar dados para exibição
        dados_formatados = []
        for clube in clubes:
            id_, sigla, nome, uf, serie, atletas, pct_prov, media = clube
            dados_formatados.append([
                id_,
                sigla or "N/A",
                (nome[:20] + "...") if nome and len(nome) > 20 else (nome or "N/A"),
                uf or "?",
                serie or "?",
                atletas or "-",
                f"{pct_prov:.1f}%" if pct_prov else "-",
                f"{media:.2f}" if media else "-"
            ])
        
        print(tabulate(dados_formatados, headers=headers, tablefmt="grid"))
        
        # 4. Clubes com mais dados
        print("\n🔝 TOP 5 CLUBES COM MAIS ATLETAS:")
        cursor.execute("""
            SELECT c.abreviacao, c.nome_fantasia, s.total_atletas, s.pct_provaveis
            FROM clubes c
            JOIN clube_stats_atuais s ON c.id = s.clube_id
            WHERE s.total_atletas IS NOT NULL
            ORDER BY s.total_atletas DESC
            LIMIT 5
        """)
        
        top_clubes = cursor.fetchall()
        for sigla, nome, atletas, pct_prov in top_clubes:
            print(f"  {sigla}: {atletas} atletas ({pct_prov:.1f}% prováveis) - {nome}")
        
        # 5. Verificar se há escudos salvos
        print("\n🛡️ ESCUDOS DISPONÍVEIS:")
        cursor.execute("""
            SELECT COUNT(*) FROM clubes 
            WHERE escudo_60x60 IS NOT NULL AND escudo_60x60 != ''
        """)
        escudos_60 = cursor.fetchone()[0]
        print(f"  Escudos 60x60: {escudos_60} clubes")
        
        cursor.execute("""
            SELECT COUNT(*) FROM clubes 
            WHERE escudo_45x45 IS NOT NULL AND escudo_45x45 != ''
        """)
        escudos_45 = cursor.fetchone()[0]
        print(f"  Escudos 45x45: {escudos_45} clubes")
        
        cursor.execute("""
            SELECT COUNT(*) FROM clubes 
            WHERE escudo_30x30 IS NOT NULL AND escudo_30x30 != ''
        """)
        escudos_30 = cursor.fetchone()[0]
        print(f"  Escudos 30x30: {escudos_30} clubes")

if __name__ == "__main__":
    try:
        visualizar_central()
    except ImportError:
        print("⚠️ Para uma visualização melhor, instale: pip install tabulate")
        print("Executando versão simplificada...\n")
        
        # Versão simples sem tabulate
        import sqlite3
        import os
        
        db_path = os.path.join("models", "central_dados.db")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clubes WHERE ativo = 1")
            print(f"Total de clubes: {cursor.fetchone()[0]}")
            
            cursor.execute("""
                SELECT c.abreviacao, c.nome_fantasia, s.total_atletas
                FROM clubes c
                LEFT JOIN clube_stats_atuais s ON c.id = s.clube_id
                WHERE c.ativo = 1
                LIMIT 5
            """)
            
            print("\nPrimeiros 5 clubes:")
            for sigla, nome, atletas in cursor.fetchall():
                print(f"  {sigla}: {nome} ({atletas or 0} atletas)")
