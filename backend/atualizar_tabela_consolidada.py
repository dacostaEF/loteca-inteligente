#!/usr/bin/env python3
"""
Script Otimizado para Atualizar Classificação
Lê DIRETAMENTE os arquivos consolidados CSV e atualiza o banco

Arquivos lidos:
  - backend/estatistica/Serie_A_tabela_tradicional.csv
  - backend/estatistica/Serie_B_tabela_tradicional.csv

Uso:
  python atualizar_tabela_consolidada.py
  python atualizar_tabela_consolidada.py --serie A
  python atualizar_tabela_consolidada.py --serie B
"""

import os
import sys
import csv
import sqlite3
import argparse
from datetime import datetime

def ler_csv_consolidado(caminho_csv):
    """
    Lê o arquivo CSV consolidado da tabela
    Retorna lista de dicionários com os dados
    """
    print(f"📖 Lendo arquivo: {caminho_csv}")
    
    if not os.path.exists(caminho_csv):
        print(f"❌ ERRO: Arquivo não encontrado: {caminho_csv}")
        return []
    
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            dados = list(reader)
        
        print(f"✅ {len(dados)} times lidos com sucesso!")
        return dados
        
    except Exception as e:
        print(f"❌ ERRO ao ler CSV: {e}")
        return []

def limpar_valor(valor):
    """Remove aspas e espaços extras"""
    if isinstance(valor, str):
        return valor.strip().strip('"').strip()
    return valor

def atualizar_serie_a(db_path, dados):
    """
    Atualiza a tabela classificacao_serie_a no banco
    """
    print(f"\n🔄 Atualizando Série A no banco: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. LIMPAR TABELA EXISTENTE
        print("🗑️  Limpando dados antigos...")
        cursor.execute("DELETE FROM classificacao_serie_a")
        
        # 2. INSERIR NOVOS DADOS
        print("📊 Inserindo novos dados...")
        
        for time in dados:
            # Limpar valores
            posicao = limpar_valor(time.get('Posição', ''))
            nome = limpar_valor(time.get('Time', ''))
            pontos = limpar_valor(time.get('Pontos', '0'))
            jogos = limpar_valor(time.get('Jogos', '0'))
            vitorias = limpar_valor(time.get('Vitórias', '0'))
            empates = limpar_valor(time.get('Empates', '0'))
            derrotas = limpar_valor(time.get('Derrotas', '0'))
            gols_pro = limpar_valor(time.get('Gols Pró', '0'))
            gols_contra = limpar_valor(time.get('Gols Contra', '0'))
            saldo_gols = limpar_valor(time.get('Saldo Gols', '0'))
            aproveitamento = limpar_valor(time.get('Aproveitamento %', '0'))
            ultimos_5 = limpar_valor(time.get('Últimos 5 Jogos', ''))
            
            # Determinar zona (G4, Libertadores, Rebaixamento)
            pos_num = int(posicao)
            if pos_num <= 4:
                zona = 'libertadores-direto'
            elif pos_num <= 6:
                zona = 'libertadores-preliminar'
            elif pos_num <= 12:
                zona = 'sulamericana'
            elif pos_num <= 16:
                zona = 'neutro'
            else:
                zona = 'rebaixamento'
            
            # Inserir no banco
            cursor.execute("""
                INSERT INTO classificacao_serie_a 
                (posicao, time, pontos, jogos, vitorias, empates, derrotas, 
                 gols_pro, gols_contra, saldo_gols, aproveitamento, 
                 ultimos_jogos, zona, data_atualizacao, rodada, fonte)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 28, 'CSV Consolidado')
            """, (
                posicao, nome, pontos, jogos, vitorias, empates, derrotas,
                gols_pro, gols_contra, saldo_gols, aproveitamento,
                ultimos_5, zona
            ))
            
            print(f"  ✅ {posicao}º - {nome} ({pontos} pts)")
        
        # 3. COMMIT
        conn.commit()
        conn.close()
        
        print(f"✅ Série A atualizada com sucesso! ({len(dados)} times)")
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao atualizar Série A: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def atualizar_serie_b(db_path, dados):
    """
    Atualiza a tabela classificacao_serie_b no banco
    """
    print(f"\n🔄 Atualizando Série B no banco: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='classificacao_serie_b'
        """)
        
        if not cursor.fetchone():
            print("⚠️  Tabela classificacao_serie_b não existe. Criando...")
            cursor.execute("""
                CREATE TABLE classificacao_serie_b (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    posicao INTEGER,
                    time TEXT,
                    pontos INTEGER,
                    jogos INTEGER,
                    vitorias INTEGER,
                    empates INTEGER,
                    derrotas INTEGER,
                    gols_pro INTEGER,
                    gols_contra INTEGER,
                    saldo_gols INTEGER,
                    aproveitamento REAL,
                    ultimos_confrontos TEXT,
                    zona TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # 1. LIMPAR TABELA EXISTENTE
        print("🗑️  Limpando dados antigos...")
        cursor.execute("DELETE FROM classificacao_serie_b")
        
        # 2. INSERIR NOVOS DADOS
        print("📊 Inserindo novos dados...")
        
        for time in dados:
            # Limpar valores
            posicao = limpar_valor(time.get('Posição', ''))
            nome = limpar_valor(time.get('Time', ''))
            pontos = limpar_valor(time.get('Pontos', '0'))
            jogos = limpar_valor(time.get('Jogos', '0'))
            vitorias = limpar_valor(time.get('Vitórias', '0'))
            empates = limpar_valor(time.get('Empates', '0'))
            derrotas = limpar_valor(time.get('Derrotas', '0'))
            gols_pro = limpar_valor(time.get('Gols Pró', '0'))
            gols_contra = limpar_valor(time.get('Gols Contra', '0'))
            saldo_gols = limpar_valor(time.get('Saldo Gols', '0'))
            aproveitamento = limpar_valor(time.get('Aproveitamento %', '0'))
            ultimos_5 = limpar_valor(time.get('Últimos 5 Jogos', ''))
            
            # Determinar zona (Acesso, Neutro, Rebaixamento)
            pos_num = int(posicao)
            if pos_num <= 4:
                zona = 'acesso-direto'
            elif pos_num <= 8:
                zona = 'acesso-playoff'
            elif pos_num <= 16:
                zona = 'neutro'
            else:
                zona = 'rebaixamento'
            
            # Inserir no banco
            cursor.execute("""
                INSERT INTO classificacao_serie_b 
                (posicao, time, pontos, jogos, vitorias, empates, derrotas, 
                 gols_pro, gols_contra, saldo_gols, aproveitamento, 
                 ultimos_confrontos, zona, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                posicao, nome, pontos, jogos, vitorias, empates, derrotas,
                gols_pro, gols_contra, saldo_gols, aproveitamento,
                ultimos_5, zona
            ))
            
            print(f"  ✅ {posicao}º - {nome} ({pontos} pts)")
        
        # 3. COMMIT
        conn.commit()
        conn.close()
        
        print(f"✅ Série B atualizada com sucesso! ({len(dados)} times)")
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao atualizar Série B: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Atualizar classificação usando CSV consolidado')
    parser.add_argument('--serie', choices=['A', 'B', 'TODAS'], default='TODAS',
                        help='Série a atualizar (A, B ou TODAS)')
    args = parser.parse_args()
    
    print("=" * 80)
    print("🏆 ATUALIZADOR DE CLASSIFICAÇÃO - MÉTODO CONSOLIDADO")
    print("=" * 80)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🎯 Série: {args.serie}")
    print("=" * 80)
    
    # Caminhos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    estatistica_dir = os.path.join(base_dir, 'estatistica')
    db_path = os.path.join(base_dir, 'models', 'tabelas_classificacao.db')
    
    print(f"\n📂 Diretório base: {base_dir}")
    print(f"📂 Diretório estatísticas: {estatistica_dir}")
    print(f"💾 Banco de dados: {db_path}")
    
    # Verificar se banco existe
    if not os.path.exists(db_path):
        print(f"\n❌ ERRO: Banco de dados não encontrado: {db_path}")
        return False
    
    sucesso = True
    
    # ATUALIZAR SÉRIE A
    if args.serie in ['A', 'TODAS']:
        csv_serie_a = os.path.join(estatistica_dir, 'Serie_A_tabela_tradicional.csv')
        
        if os.path.exists(csv_serie_a):
            print(f"\n{'='*80}")
            print("🇧🇷 PROCESSANDO SÉRIE A")
            print("="*80)
            
            dados_a = ler_csv_consolidado(csv_serie_a)
            
            if dados_a:
                if not atualizar_serie_a(db_path, dados_a):
                    sucesso = False
            else:
                print("❌ Nenhum dado da Série A para processar")
                sucesso = False
        else:
            print(f"\n⚠️  Arquivo Série A não encontrado: {csv_serie_a}")
            if args.serie == 'A':
                sucesso = False
    
    # ATUALIZAR SÉRIE B
    if args.serie in ['B', 'TODAS']:
        csv_serie_b = os.path.join(estatistica_dir, 'Serie_B_tabela_tradicional.csv')
        
        if os.path.exists(csv_serie_b):
            print(f"\n{'='*80}")
            print("🇧🇷 PROCESSANDO SÉRIE B")
            print("="*80)
            
            dados_b = ler_csv_consolidado(csv_serie_b)
            
            if dados_b:
                if not atualizar_serie_b(db_path, dados_b):
                    sucesso = False
            else:
                print("❌ Nenhum dado da Série B para processar")
                sucesso = False
        else:
            print(f"\n⚠️  Arquivo Série B não encontrado: {csv_serie_b}")
            if args.serie == 'B':
                sucesso = False
    
    # RESUMO FINAL
    print("\n" + "="*80)
    if sucesso:
        print("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("❌ ATUALIZAÇÃO CONCLUÍDA COM ERROS")
    print("="*80)
    print(f"📅 Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)
    
    return sucesso

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Atualização cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

