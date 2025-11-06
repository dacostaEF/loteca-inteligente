#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Teste direto da API de Força dos Elencos"""

import os
import sys
import csv
import unicodedata
import json

# Simular a função da API
def testar_api():
    print("🧪 TESTE DIRETO DA API - dados_unificados()")
    print("=" * 60)
    
    # Caminhos dos CSVs
    base_dir = os.path.join(os.path.dirname(__file__), 'models', 'EstatisticasElenco')
    top100_csv = os.path.join(base_dir, 'Valor_Elenco_top_100_clubes_mais_valiosos.csv')
    serie_a_csv = os.path.join(base_dir, 'Valor_Elenco_serie_a_brasileirao.csv')
    serie_b_csv = os.path.join(base_dir, 'Valor_Elenco_serie_b_brasileirao.csv')
    
    print(f"\n📂 CAMINHOS DOS ARQUIVOS:")
    print(f"   Base: {base_dir}")
    print(f"   Top 100: {os.path.exists(top100_csv)} - {top100_csv}")
    print(f"   Série A: {os.path.exists(serie_a_csv)} - {serie_a_csv}")
    print(f"   Série B: {os.path.exists(serie_b_csv)} - {serie_b_csv}")
    
    if not os.path.exists(top100_csv):
        print("\n❌ ERRO: CSV Top 100 não encontrado!")
        return
    
    # Funções auxiliares (copiadas da API)
    def _normalize_headers(d):
        """Normaliza chaves: minúsculas, sem acento, sem % e espaços extras"""
        def normalize_string(s):
            s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
            return s.strip().lower().replace('%','').replace('  ',' ')
        return { normalize_string(k): v for k, v in d.items() }
    
    def normalizar_chave(nome):
        """Converte nome do clube para chave"""
        nome = nome.lower().strip()
        nome = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')
        nome = nome.replace(' ', '_').replace('-', '_')
        return nome
    
    def gerar_variacoes(nome):
        """Gera múltiplas variações de nomes"""
        import re
        variacoes = set()
        nome_lower = nome.lower().strip()
        
        # Remove acentos
        nome_sem_acento = ''.join(c for c in unicodedata.normalize('NFD', nome_lower) if unicodedata.category(c) != 'Mn')
        
        # Variação 1: Nome completo (com underscores)
        variacoes.add(normalizar_chave(nome))
        
        # Variação 2: Nome completo (com espaços)
        nome_com_espacos = nome_sem_acento.replace('-', ' ').replace('/', ' ').replace('_', ' ').strip()
        variacoes.add(nome_com_espacos)
        
        # Variação 3: Nome completo (com hífens)
        nome_com_hifens = nome_sem_acento.replace(' ', '-').replace('/', '-').replace('_', '-').strip()
        variacoes.add(nome_com_hifens)
        
        # Variação 4: Sem sufixos de estado
        nome_sem_estado = re.sub(r'[-/\s](sp|rj|mg|rs|ce|ba|pe|pr|sc|go|df|es|am|pa|mt|ms|al|se|pb|rn|pi|ap|rr|to|ac|ro)$', '', nome_sem_acento, flags=re.IGNORECASE)
        nome_sem_estado = re.sub(r'[-/\s](ing|esp|it|fra|ale|por|bra|brasil|brazil)$', '', nome_sem_estado, flags=re.IGNORECASE).strip()
        if nome_sem_estado and nome_sem_estado != nome_sem_acento:
            variacoes.add(nome_sem_estado)
            variacoes.add(normalizar_chave(nome_sem_estado))
        
        # Variação 5: Primeira palavra
        palavras = re.split(r'[\s\-/]+', nome_sem_acento)
        if palavras and len(palavras[0]) >= 3:
            variacoes.add(palavras[0])
        
        # Variação 6: Última palavra
        if len(palavras) > 1 and len(palavras[-1]) >= 3:
            variacoes.add(palavras[-1])
        
        # Variação 7: Sem separadores
        sem_separadores = nome_sem_acento.replace(' ', '').replace('-', '').replace('/', '')
        if sem_separadores:
            variacoes.add(sem_separadores)
        
        return list(variacoes)
    
    # Ler Top 100
    clubes = {}
    print(f"\n📊 LENDO TOP 100 MUNDIAL...")
    
    try:
        with open(top100_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                r = _normalize_headers(row)
                clube_nome = r.get('clube', '').strip()
                if not clube_nome:
                    continue
                
                count += 1
                variacoes = gerar_variacoes(clube_nome)
                
                # Logar clubes específicos
                if any(termo in clube_nome.lower() for termo in ['atletico', 'manchester', 'liverpool', 'valencia', 'betis']):
                    print(f"   ✅ {clube_nome}")
                    print(f"      Variações: {variacoes[:5]}...")  # Mostrar só as primeiras 5
                
                for chave in variacoes:
                    clubes[chave] = {'nome_oficial': clube_nome, 'fonte': 'Top 100'}
        
        print(f"   📈 Total processado: {count} clubes")
        print(f"   🔑 Total de chaves criadas: {len(clubes)}")
        
    except Exception as e:
        print(f"   ❌ ERRO ao ler Top 100: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Ler Série A
    if os.path.exists(serie_a_csv):
        print(f"\n📊 LENDO SÉRIE A...")
        try:
            with open(serie_a_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    r = _normalize_headers(row)
                    clube_nome = r.get('clube', '').strip()
                    if not clube_nome:
                        continue
                    
                    count += 1
                    variacoes = gerar_variacoes(clube_nome)
                    
                    # Logar Atlético-MG especificamente
                    if 'atletico' in clube_nome.lower():
                        print(f"   ✅ {clube_nome}")
                        print(f"      Variações: {variacoes}")
                    
                    for chave in variacoes:
                        if chave not in clubes:
                            clubes[chave] = {'nome_oficial': clube_nome, 'fonte': 'Série A'}
            
            print(f"   📈 Total processado: {count} clubes")
            
        except Exception as e:
            print(f"   ❌ ERRO ao ler Série A: {e}")
    
    # Teste de busca
    print(f"\n🔍 TESTANDO BUSCAS:")
    testes = [
        "Atlético Mineiro/MG",
        "atletico mineiro",
        "atletico-mg",
        "atletico",
        "MANCHESTER CITY/ING",
        "manchester city",
        "manchester",
        "LIVERPOOL/ING",
        "liverpool",
        "Valencia/ESP",
        "valencia",
        "REAL BETIS/ESP",
        "real betis",
        "betis"
    ]
    
    for teste in testes:
        if teste in clubes:
            print(f"   ✅ '{teste}' → {clubes[teste]['nome_oficial']} ({clubes[teste]['fonte']})")
        else:
            print(f"   ❌ '{teste}' → NÃO ENCONTRADO")
    
    print(f"\n✅ TESTE CONCLUÍDO!")
    print(f"📊 Total de chaves no dicionário: {len(clubes)}")
    
    # Mostrar todas as chaves com "atletico"
    atleticos = [k for k in clubes.keys() if 'atletico' in k]
    if atleticos:
        print(f"\n🔍 Chaves com 'atletico': {atleticos}")

if __name__ == '__main__':
    testar_api()

