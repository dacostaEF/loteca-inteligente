#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE INVESTIGACAO - BANCOS DUPLICADOS
Apenas LEITURA, nao modifica nada!
"""

import sqlite3
import os
from datetime import datetime
import sys
import io

# Forcar UTF-8 no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def bytes_to_mb(bytes_size):
    """Converte bytes para MB"""
    return round(bytes_size / (1024 * 1024), 2)

def investigar_banco(db_path):
    """Investiga conteúdo de um banco de dados"""
    print(f"\n{'='*70}")
    print(f"📊 INVESTIGANDO: {db_path}")
    print(f"{'='*70}")
    
    # Verificar se existe
    if not os.path.exists(db_path):
        print("❌ ARQUIVO NÃO EXISTE!")
        return None
    
    # Informações do arquivo
    stats = os.stat(db_path)
    print(f"\n📦 Tamanho: {bytes_to_mb(stats.st_size)} MB ({stats.st_size} bytes)")
    print(f"📅 Última modificação: {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Criado em: {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar e investigar
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📋 Tabelas encontradas ({len(tabelas)}):")
        for tabela in tabelas:
            print(f"   • {tabela}")
        
        # Investigar cada tabela
        dados_tabelas = {}
        for tabela in tabelas:
            try:
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                total = cursor.fetchone()[0]
                
                # Pegar primeiro e último registro (se existir)
                primeiro = None
                ultimo = None
                data_atualizacao = None
                
                if total > 0:
                    cursor.execute(f"SELECT * FROM {tabela} LIMIT 1")
                    primeiro = dict(cursor.fetchone())
                    
                    cursor.execute(f"SELECT * FROM {tabela} ORDER BY rowid DESC LIMIT 1")
                    ultimo = dict(cursor.fetchone())
                    
                    # Tentar pegar data de atualização (se tiver)
                    colunas = [desc[0] for desc in cursor.description]
                    if 'data_atualizacao' in colunas:
                        cursor.execute(f"SELECT data_atualizacao FROM {tabela} ORDER BY data_atualizacao DESC LIMIT 1")
                        result = cursor.fetchone()
                        if result and result[0]:
                            data_atualizacao = result[0]
                    elif 'updated_at' in colunas:
                        cursor.execute(f"SELECT updated_at FROM {tabela} ORDER BY updated_at DESC LIMIT 1")
                        result = cursor.fetchone()
                        if result and result[0]:
                            data_atualizacao = result[0]
                
                dados_tabelas[tabela] = {
                    'total': total,
                    'primeiro': primeiro,
                    'ultimo': ultimo,
                    'data_atualizacao': data_atualizacao
                }
                
                print(f"\n   🔹 {tabela}:")
                print(f"      Registros: {total}")
                if data_atualizacao:
                    print(f"      Última atualização: {data_atualizacao}")
                
                # Mostrar exemplo do último registro (primeiras 3 colunas)
                if ultimo:
                    exemplo = list(ultimo.items())[:3]
                    print(f"      Exemplo: {dict(exemplo)}")
                    
            except Exception as e:
                print(f"   ❌ Erro ao ler {tabela}: {e}")
        
        conn.close()
        
        return {
            'arquivo': db_path,
            'tamanho_mb': bytes_to_mb(stats.st_size),
            'tamanho_bytes': stats.st_size,
            'modificado': datetime.fromtimestamp(stats.st_mtime),
            'criado': datetime.fromtimestamp(stats.st_ctime),
            'tabelas': dados_tabelas
        }
        
    except Exception as e:
        print(f"❌ ERRO ao abrir banco: {e}")
        return None

def comparar_bancos(banco1, banco2):
    """Compara 2 bancos e mostra diferenças"""
    print(f"\n{'='*70}")
    print("🔍 COMPARAÇÃO ENTRE OS 2 BANCOS")
    print(f"{'='*70}")
    
    if not banco1 or not banco2:
        print("❌ Um dos bancos não pôde ser investigado!")
        return
    
    # Comparar tamanhos
    print(f"\n📦 TAMANHO:")
    print(f"   Banco 1 (correto):  {banco1['tamanho_mb']} MB")
    print(f"   Banco 2 (duplicado): {banco2['tamanho_mb']} MB")
    
    if banco1['tamanho_bytes'] > banco2['tamanho_bytes']:
        diff = banco1['tamanho_bytes'] - banco2['tamanho_bytes']
        print(f"   ✅ Banco 1 é MAIOR (+{bytes_to_mb(diff)} MB)")
    elif banco2['tamanho_bytes'] > banco1['tamanho_bytes']:
        diff = banco2['tamanho_bytes'] - banco1['tamanho_bytes']
        print(f"   ⚠️ Banco 2 é MAIOR (+{bytes_to_mb(diff)} MB)")
    else:
        print(f"   ℹ️ Tamanhos IGUAIS")
    
    # Comparar datas
    print(f"\n📅 ÚLTIMA MODIFICAÇÃO:")
    print(f"   Banco 1 (correto):  {banco1['modificado'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Banco 2 (duplicado): {banco2['modificado'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    if banco1['modificado'] > banco2['modificado']:
        print(f"   ✅ Banco 1 é MAIS RECENTE")
    elif banco2['modificado'] > banco1['modificado']:
        print(f"   ⚠️ Banco 2 é MAIS RECENTE")
    else:
        print(f"   ℹ️ Mesma data")
    
    # Comparar tabelas
    print(f"\n📋 TABELAS:")
    tabelas1 = set(banco1['tabelas'].keys())
    tabelas2 = set(banco2['tabelas'].keys())
    
    comuns = tabelas1 & tabelas2
    so_banco1 = tabelas1 - tabelas2
    so_banco2 = tabelas2 - tabelas1
    
    print(f"   Tabelas em comum: {len(comuns)}")
    if so_banco1:
        print(f"   ⚠️ Só no Banco 1: {', '.join(so_banco1)}")
    if so_banco2:
        print(f"   ⚠️ Só no Banco 2: {', '.join(so_banco2)}")
    
    # Comparar registros nas tabelas comuns
    print(f"\n📊 REGISTROS NAS TABELAS COMUNS:")
    for tabela in sorted(comuns):
        total1 = banco1['tabelas'][tabela]['total']
        total2 = banco2['tabelas'][tabela]['total']
        
        status = "✅" if total1 >= total2 else "⚠️"
        print(f"   {status} {tabela}:")
        print(f"      Banco 1: {total1} registros")
        print(f"      Banco 2: {total2} registros")
        
        if total1 != total2:
            diff = abs(total1 - total2)
            print(f"      Diferença: {diff} registros")
    
    # RECOMENDAÇÃO FINAL
    print(f"\n{'='*70}")
    print("🎯 RECOMENDAÇÃO:")
    print(f"{'='*70}")
    
    banco1_melhor = (
        banco1['tamanho_bytes'] >= banco2['tamanho_bytes'] and
        banco1['modificado'] >= banco2['modificado']
    )
    
    if banco1_melhor:
        print("""
✅ O BANCO CORRETO (backend/models/tabelas_classificacao.db) está:
   • Mais recente ou igual
   • Com mais dados ou igual
   
   👉 SEGURO DELETAR o banco duplicado (backend/tabelas_classificacao.db)
        """)
    else:
        print("""
⚠️ O BANCO DUPLICADO (backend/tabelas_classificacao.db) está:
   • Mais recente OU
   • Com mais dados
   
   👉 CUIDADO! Pode ter dados importantes. 
      Recomendo COPIAR dados do duplicado para o correto antes de deletar!
        """)

if __name__ == "__main__":
    print("\n🔍 INVESTIGAÇÃO DE BANCOS DUPLICADOS")
    print("="*70)
    
    # Caminhos dos bancos
    banco_correto = "backend/models/tabelas_classificacao.db"
    banco_duplicado = "backend/tabelas_classificacao.db"
    
    # Investigar ambos
    dados_correto = investigar_banco(banco_correto)
    dados_duplicado = investigar_banco(banco_duplicado)
    
    # Comparar
    if dados_correto and dados_duplicado:
        comparar_bancos(dados_correto, dados_duplicado)
    
    print(f"\n{'='*70}")
    print("✅ INVESTIGAÇÃO CONCLUÍDA!")
    print("="*70)

