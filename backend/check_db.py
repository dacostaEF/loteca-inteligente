#!/usr/bin/env python3
import sqlite3
import os

db_path = 'models/tabelas_classificacao.db'

if os.path.exists(db_path):
    print(f"✅ Banco encontrado: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"📊 Tabelas encontradas: {tables}")
    
    # Verificar conteúdo das tabelas principais
    for table in tables:
        if 'classificacao' in table.lower():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📋 {table}: {count} registros")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                rows = cursor.fetchall()
                print(f"   Primeiros registros: {rows[:2]}")
    
    conn.close()
else:
    print(f"❌ Banco não encontrado: {db_path}")
