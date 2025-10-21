#!/usr/bin/env python3
"""
Script para atualizar as tabelas lendo os CSVs atualizados
"""

import os
import csv
import sqlite3
from datetime import datetime

def mapear_nome_clube(nome_pasta):
    """Mapeia nomes das pastas para nomes dos clubes"""
    mapeamento = {
        'flamengo': 'Flamengo',
        'palmeiras': 'Palmeiras', 
        'corinthians': 'Corinthians',
        'sao-paulo': 'São Paulo',
        'botafogo': 'Botafogo',
        'fluminense': 'Fluminense',
        'cruzeiro': 'Cruzeiro',
        'atletico-mg': 'Atlético-MG',
        'bahia': 'Bahia',
        'ceara': 'Ceará',
        'fortaleza': 'Fortaleza',
        'gremio': 'Grêmio',
        'internacional': 'Internacional',
        'juventude': 'Juventude',
        'mirassol': 'Mirassol',
        'red-bull-bragantino': 'Red Bull Bragantino',
        'santos': 'Santos',
        'sport-recife': 'Sport',
        'vasco': 'Vasco',
        'vitoria': 'Vitória'
    }
    return mapeamento.get(nome_pasta.lower(), nome_pasta.title())

def ler_csv_clube(caminho_csv):
    """Lê CSV de um clube e calcula estatísticas"""
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            jogos = list(reader)
        
        if not jogos:
            return None
        
        # Pegar dados do último jogo
        ultimo_jogo = jogos[0]
        
        # Calcular estatísticas
        pontos = int(ultimo_jogo['Pontos_Acumulados'])
        jogos_disputados = len(jogos)
        
        # Contar vitórias, empates, derrotas
        vitorias = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Vitoria')
        empates = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Empate')
        derrotas = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Derrota')
        
        # Calcular gols
        gols_pro = 0
        gols_contra = 0
        
        for jogo in jogos:
            time_casa = jogo['Time_Casa']
            time_visitante = jogo['Time_Visitante']
            
            nome_clube = os.path.basename(os.path.dirname(caminho_csv))
            nome_clube_mapeado = mapear_nome_clube(nome_clube)
            
            if time_casa == nome_clube_mapeado:
                gols_pro += int(jogo['Gols_Casa'])
                gols_contra += int(jogo['Gols_Visitante'])
            elif time_visitante == nome_clube_mapeado:
                gols_pro += int(jogo['Gols_Visitante'])
                gols_contra += int(jogo['Gols_Casa'])
        
        saldo_gols = gols_pro - gols_contra
        aproveitamento = (pontos / (jogos_disputados * 3)) * 100 if jogos_disputados > 0 else 0
        
        return {
            'time': nome_clube_mapeado,
            'pontos': pontos,
            'jogos': jogos_disputados,
            'vitorias': vitorias,
            'empates': empates,
            'derrotas': derrotas,
            'gols_pro': gols_pro,
            'gols_contra': gols_contra,
            'saldo_gols': saldo_gols,
            'aproveitamento': round(aproveitamento, 1)
        }
        
    except Exception as e:
        print(f"❌ Erro ao ler {caminho_csv}: {e}")
        return None

def processar_serie(serie_path, serie_nome):
    """Processa todos os clubes de uma série"""
    print(f"📊 Processando {serie_nome}...")
    
    clubes = []
    
    if not os.path.exists(serie_path):
        print(f"❌ Pasta {serie_path} não encontrada!")
        return clubes
    
    # Listar todas as pastas de clubes
    for pasta_clube in os.listdir(serie_path):
        pasta_completa = os.path.join(serie_path, pasta_clube)
        
        if os.path.isdir(pasta_completa):
            csv_path = os.path.join(pasta_completa, "jogos.csv")
            
            if os.path.exists(csv_path):
                print(f"  📁 Processando {pasta_clube}...")
                dados_clube = ler_csv_clube(csv_path)
                
                if dados_clube:
                    clubes.append(dados_clube)
                else:
                    print(f"    ❌ Falha ao processar {pasta_clube}")
    
    # Ordenar por classificação
    clubes_ordenados = sorted(clubes, key=lambda x: (
        -x['pontos'],
        -x['saldo_gols'],
        -x['gols_pro']
    ))
    
    # Adicionar posição e zona
    for i, clube in enumerate(clubes_ordenados, 1):
        clube['posicao'] = i
        if 1 <= i <= 6:
            clube['zona'] = 'Libertadores'
        elif 7 <= i <= 12:
            clube['zona'] = 'Sul-Americana'
        elif 17 <= i <= 20:
            clube['zona'] = 'Zona de Rebaixamento'
        else:
            clube['zona'] = 'Meio de tabela'
    
    print(f"✅ {serie_nome}: {len(clubes_ordenados)} clubes processados")
    return clubes_ordenados

def atualizar_banco(serie_a, serie_b):
    """Atualiza o banco de dados"""
    print("\n💾 Atualizando banco de dados...")
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect('backend/models/tabelas_classificacao.db')
        cursor = conn.cursor()
        
        # Limpar Série A
        cursor.execute("DELETE FROM classificacao_serie_a")
        print("🗑️ Dados antigos da Série A removidos")
        
        # Inserir Série A
        for clube in serie_a:
            cursor.execute("""
                INSERT INTO classificacao_serie_a (
                    posicao, time, pontos, jogos, vitorias, empates, derrotas,
                    gols_pro, gols_contra, saldo_gols, aproveitamento,
                    ultimos_confrontos, zona, data_atualizacao, rodada, fonte
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clube['posicao'], clube['time'], clube['pontos'], clube['jogos'],
                clube['vitorias'], clube['empates'], clube['derrotas'],
                clube['gols_pro'], clube['gols_contra'], clube['saldo_gols'],
                clube['aproveitamento'], '', clube['zona'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, 'csv_automatico'
            ))
        
        print(f"✅ Série A: {len(serie_a)} clubes inseridos")
        
        # Limpar Série B
        cursor.execute("DELETE FROM classificacao_serie_b")
        print("🗑️ Dados antigos da Série B removidos")
        
        # Inserir Série B
        for clube in serie_b:
            cursor.execute("""
                INSERT INTO classificacao_serie_b (
                    posicao, time, pontos, jogos, vitorias, empates, derrotas,
                    gols_pro, gols_contra, saldo_gols, aproveitamento,
                    ultimos_confrontos, zona, data_atualizacao, rodada, fonte
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clube['posicao'], clube['time'], clube['pontos'], clube['jogos'],
                clube['vitorias'], clube['empates'], clube['derrotas'],
                clube['gols_pro'], clube['gols_contra'], clube['saldo_gols'],
                clube['aproveitamento'], '', clube['zona'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, 'csv_automatico'
            ))
        
        print(f"✅ Série B: {len(serie_b)} clubes inseridos")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 ATUALIZANDO TABELAS DOS CSVs ATUALIZADOS")
    print("=" * 50)
    
    # Processar Série A
    serie_a = processar_serie("backend/estatistica/Serie_A", "Série A")
    
    # Processar Série B  
    serie_b = processar_serie("backend/estatistica/Serie_B", "Série B")
    
    if not serie_a and not serie_b:
        print("❌ Nenhum dado processado!")
        return
    
    # Mostrar preview
    print("\n🏆 PREVIEW SÉRIE A - TOP 5:")
    for clube in serie_a[:5]:
        print(f"{clube['posicao']}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")
    
    print("\n🥈 PREVIEW SÉRIE B - TOP 5:")
    for clube in serie_b[:5]:
        print(f"{clube['posicao']}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")
    
    # Atualizar banco
    if atualizar_banco(serie_a, serie_b):
        print("\n🎉 TABELAS ATUALIZADAS COM SUCESSO!")
        print("🌐 Acesse: http://localhost:5000/loteca")
        print("📊 Vá na aba 'Panorama dos Campeonatos'")
    else:
        print("\n💥 ERRO AO ATUALIZAR BANCO!")

if __name__ == "__main__":
    main()

