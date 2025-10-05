#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import unicodedata
import re

def normalizar_texto(texto):
    """Normalizar texto removendo acentos e caracteres especiais"""
    if not texto:
        return texto
    
    # Normalizar unicode
    texto = unicodedata.normalize('NFD', texto)
    
    # Remover acentos
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    
    # Substituir caracteres problemáticos
    substituicoes = {
        'Grê': 'Gre',
        'São': 'Sao', 
        'Cea': 'Cea',  # Já está correto
        'Vitória': 'Vitoria',
        'Derrota': 'Derrota',
        'Empate': 'Empate'
    }
    
    for antigo, novo in substituicoes.items():
        texto = texto.replace(antigo, novo)
    
    return texto

def corrigir_csv_clube(caminho_csv):
    """Corrigir um arquivo CSV específico"""
    print(f"Corrigindo: {caminho_csv}")
    
    if not os.path.exists(caminho_csv):
        print(f"  ERRO: Arquivo nao encontrado!")
        return False
    
    # Ler arquivo original
    linhas_originais = []
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        linhas_originais = list(reader)
    
    # Normalizar cada linha
    linhas_corrigidas = []
    for linha in linhas_originais:
        linha_corrigida = [normalizar_texto(campo) for campo in linha]
        linhas_corrigidas.append(linha_corrigida)
    
    # Salvar arquivo corrigido
    with open(caminho_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(linhas_corrigidas)
    
    print(f"  OK: Arquivo corrigido!")
    return True

def corrigir_todos_csvs():
    """Corrigir todos os arquivos CSV dos clubes"""
    print("=== CORRECAO DE CARACTERES ESPECIAIS NOS CSVs ===")
    
    base_dir = "models/Jogos"
    clubes_corrigidos = 0
    clubes_com_erro = 0
    
    # Listar todos os diretórios de clubes
    for item in os.listdir(base_dir):
        clube_dir = os.path.join(base_dir, item)
        if os.path.isdir(clube_dir):
            csv_path = os.path.join(clube_dir, "jogos.csv")
            
            if os.path.exists(csv_path):
                try:
                    if corrigir_csv_clube(csv_path):
                        clubes_corrigidos += 1
                    else:
                        clubes_com_erro += 1
                except Exception as e:
                    print(f"  ERRO ao corrigir {item}: {e}")
                    clubes_com_erro += 1
            else:
                print(f"AVISO: {item} nao tem jogos.csv")
    
    print(f"\nRESUMO:")
    print(f"  Clubes corrigidos: {clubes_corrigidos}")
    print(f"  Clubes com erro: {clubes_com_erro}")
    print(f"  Total processados: {clubes_corrigidos + clubes_com_erro}")

if __name__ == "__main__":
    corrigir_todos_csvs()
