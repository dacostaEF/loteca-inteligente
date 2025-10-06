import sqlite3
import os

def criar_tabela_champions_league():
    """Cria a tabela da Champions League no banco de dados"""
    
    db_path = "backend/models/tabelas_classificacao.db"
    if not os.path.exists(db_path):
        print(f"ERRO: Banco de dados nao encontrado: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criar tabela da Champions League
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classificacao_champions_league (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                posicao INTEGER NOT NULL,
                clube VARCHAR(100) NOT NULL,
                pais VARCHAR(50) NOT NULL,
                grupo VARCHAR(5),
                pts INTEGER NOT NULL,
                pj INTEGER NOT NULL,
                vit INTEGER NOT NULL,
                e INTEGER NOT NULL,
                der INTEGER NOT NULL,
                gm INTEGER NOT NULL,
                gc INTEGER NOT NULL,
                sg INTEGER NOT NULL,
                ultimas_5 VARCHAR(10),
                fase VARCHAR(50) DEFAULT 'grupos',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Inserir dados de exemplo (alguns times famosos)
        dados_exemplo = [
            {
                'posicao': 1, 'clube': 'Real Madrid', 'pais': 'Espanha', 'grupo': 'A',
                'pts': 15, 'pj': 6, 'vit': 5, 'e': 0, 'der': 1,
                'gm': 18, 'gc': 6, 'sg': 12, 'ultimas_5': 'VVVDV', 'fase': 'oitavas'
            },
            {
                'posicao': 2, 'clube': 'Manchester City', 'pais': 'Inglaterra', 'grupo': 'A',
                'pts': 12, 'pj': 6, 'vit': 4, 'e': 0, 'der': 2,
                'gm': 15, 'gc': 8, 'sg': 7, 'ultimas_5': 'VVDDV', 'fase': 'oitavas'
            },
            {
                'posicao': 3, 'clube': 'Bayern Munich', 'pais': 'Alemanha', 'grupo': 'B',
                'pts': 15, 'pj': 6, 'vit': 5, 'e': 0, 'der': 1,
                'gm': 16, 'gc': 5, 'sg': 11, 'ultimas_5': 'VVVVD', 'fase': 'oitavas'
            },
            {
                'posicao': 4, 'clube': 'PSG', 'pais': 'França', 'grupo': 'B',
                'pts': 10, 'pj': 6, 'vit': 3, 'e': 1, 'der': 2,
                'gm': 12, 'gc': 9, 'sg': 3, 'ultimas_5': 'VEDVV', 'fase': 'oitavas'
            },
            {
                'posicao': 5, 'clube': 'Barcelona', 'pais': 'Espanha', 'grupo': 'C',
                'pts': 13, 'pj': 6, 'vit': 4, 'e': 1, 'der': 1,
                'gm': 14, 'gc': 7, 'sg': 7, 'ultimas_5': 'VVEDV', 'fase': 'oitavas'
            },
            {
                'posicao': 6, 'clube': 'Arsenal', 'pais': 'Inglaterra', 'grupo': 'C',
                'pts': 11, 'pj': 6, 'vit': 3, 'e': 2, 'der': 1,
                'gm': 11, 'gc': 6, 'sg': 5, 'ultimas_5': 'VEEDV', 'fase': 'oitavas'
            },
            {
                'posicao': 7, 'clube': 'Inter Milan', 'pais': 'Itália', 'grupo': 'D',
                'pts': 14, 'pj': 6, 'vit': 4, 'e': 2, 'der': 0,
                'gm': 13, 'gc': 4, 'sg': 9, 'ultimas_5': 'VVEEV', 'fase': 'oitavas'
            },
            {
                'posicao': 8, 'clube': 'Atletico Madrid', 'pais': 'Espanha', 'grupo': 'D',
                'pts': 9, 'pj': 6, 'vit': 2, 'e': 3, 'der': 1,
                'gm': 8, 'gc': 6, 'sg': 2, 'ultimas_5': 'EEVDV', 'fase': 'oitavas'
            }
        ]
        
        # Limpar dados antigos
        cursor.execute("DELETE FROM classificacao_champions_league")
        print("Dados antigos da Champions League removidos")
        
        # Inserir dados de exemplo
        for time in dados_exemplo:
            cursor.execute("""
                INSERT INTO classificacao_champions_league 
                (posicao, clube, pais, grupo, pts, pj, vit, e, der, gm, gc, sg, ultimas_5, fase)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                time['posicao'], time['clube'], time['pais'], time['grupo'],
                time['pts'], time['pj'], time['vit'], time['e'], time['der'],
                time['gm'], time['gc'], time['sg'], time['ultimas_5'], time['fase']
            ))
        
        conn.commit()
        print(f"Champions League criada com sucesso! {len(dados_exemplo)} times inseridos")
        
        # Mostrar alguns dados para verificação
        cursor.execute("SELECT posicao, clube, pais, grupo, pts, ultimas_5 FROM classificacao_champions_league ORDER BY posicao LIMIT 5")
        top5 = cursor.fetchall()
        
        print("\nTOP 5 CHAMPIONS LEAGUE:")
        print("=" * 60)
        for pos, clube, pais, grupo, pts, ultimos in top5:
            print(f"{pos}º {clube} ({pais}) - Grupo {grupo}: {pts} pts - Últimos: {ultimos}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERRO ao criar Champions League: {e}")
        return False

if __name__ == "__main__":
    print("=== CRIACAO DA TABELA CHAMPIONS LEAGUE ===")
    print("Criando tabela e inserindo dados de exemplo...")
    print()
    
    if criar_tabela_champions_league():
        print("\nSUCESSO: Champions League criada!")
        print("Próximos passos:")
        print("1. Adicionar aba na Central Admin")
        print("2. Criar API endpoint")
        print("3. Integrar na página do usuário")
        print("4. Criar modal explicativo")
    else:
        print("\nERRO: Falha na criacao!")
