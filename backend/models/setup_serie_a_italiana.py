#!/usr/bin/env python3
"""
Script para configurar a tabela da Série A Italiana no banco de dados
Execute este script para criar a tabela e inserir dados iniciais
"""

import sqlite3
import os
import sys

def setup_serie_a_italiana():
    """Configurar tabela da Série A Italiana"""
    
    # Caminho do banco de dados
    db_path = "tabelas_classificacao.db"
    
    # Verificar se o banco existe
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados {db_path} não encontrado!")
        print("📁 Procurando em outros locais...")
        
        # Tentar outros caminhos
        possible_paths = [
            "backend/models/tabelas_classificacao.db",
            "models/tabelas_classificacao.db",
            "../tabelas_classificacao.db"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                db_path = path
                print(f"✅ Banco encontrado em: {db_path}")
                break
        else:
            print("❌ Banco de dados não encontrado em nenhum local!")
            return False
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Configurando tabela da Série A Italiana...")
        
        # Ler e executar o script SQL
        sql_file = "create_serie_a_italiana.sql"
        if not os.path.exists(sql_file):
            # Tentar outros caminhos
            possible_sql_paths = [
                "backend/models/create_serie_a_italiana.sql",
                "models/create_serie_a_italiana.sql"
            ]
            
            for path in possible_sql_paths:
                if os.path.exists(path):
                    sql_file = path
                    break
            else:
                print(f"❌ Arquivo SQL {sql_file} não encontrado!")
                return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Executar o script SQL
        cursor.executescript(sql_script)
        
        # Verificar se a tabela foi criada
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='classificacao_serie_a_italiana'
        """)
        
        if cursor.fetchone():
            print("✅ Tabela 'classificacao_serie_a_italiana' criada com sucesso!")
            
            # Verificar quantos times foram inseridos
            cursor.execute("SELECT COUNT(*) FROM classificacao_serie_a_italiana")
            count = cursor.fetchone()[0]
            print(f"📊 {count} times inseridos na tabela")
            
            # Mostrar alguns times
            cursor.execute("SELECT posicao, time FROM classificacao_serie_a_italiana ORDER BY posicao LIMIT 5")
            times = cursor.fetchall()
            print("🏆 Primeiros 5 times:")
            for pos, time in times:
                print(f"   {pos}º - {time}")
            
        else:
            print("❌ Erro ao criar tabela!")
            return False
        
        # Commit e fechar
        conn.commit()
        conn.close()
        
        print("🎉 Configuração da Série A Italiana concluída com sucesso!")
        print("🇮🇹 Agora você pode usar 'Série A Italiana' na Central Admin!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar Série A Italiana: {e}")
        return False

if __name__ == "__main__":
    print("🇮🇹 === CONFIGURADOR DA SÉRIE A ITALIANA ===")
    print("🔧 Este script irá criar a tabela e inserir dados iniciais")
    print()
    
    success = setup_serie_a_italiana()
    
    if success:
        print()
        print("✅ Configuração concluída!")
        print("📋 Próximos passos:")
        print("   1. Inicie o servidor")
        print("   2. Acesse a Central Admin")
        print("   3. Vá para 'Gestão de Classificação'")
        print("   4. Selecione '🇮🇹 Série A Italiana' no dropdown")
        print("   5. Atualize os dados dos times conforme necessário")
    else:
        print()
        print("❌ Configuração falhou!")
        print("🔍 Verifique os logs acima para mais detalhes")
        sys.exit(1)



