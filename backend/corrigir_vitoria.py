#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv

def corrigir_vitoria_todos_csvs():
    """Corrigir VitA�ria para Vitoria em todos os CSVs"""
    print("=== CORRECAO VITORIA MALFORMADA -> VITORIA ===")
    
    base_dir = "models/Jogos"
    correcoes = 0
    total_alteracoes = 0
    
    # Processar cada CSV
    for item in os.listdir(base_dir):
        clube_dir = os.path.join(base_dir, item)
        if os.path.isdir(clube_dir):
            csv_path = os.path.join(clube_dir, "jogos.csv")
            
            if os.path.exists(csv_path):
                print(f"Corrigindo: {item}")
                
                # Ler arquivo
                linhas = []
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    linhas = list(reader)
                
                # Aplicar correções
                linhas_corrigidas = []
                alteracoes_clube = 0
                
                for linha in linhas:
                    linha_corrigida = []
                    for campo in linha:
                        campo_original = campo
                        # Corrigir VitA�ria para Vitoria
                        campo_corrigido = campo.replace('VitA�ria', 'Vitoria')
                        if campo_original != campo_corrigido:
                            alteracoes_clube += 1
                        linha_corrigida.append(campo_corrigido)
                    linhas_corrigidas.append(linha_corrigida)
                
                # Salvar arquivo corrigido
                with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(linhas_corrigidas)
                
                if alteracoes_clube > 0:
                    print(f"  OK: {item} - {alteracoes_clube} correcoes!")
                    correcoes += 1
                    total_alteracoes += alteracoes_clube
                else:
                    print(f"  OK: {item} - sem correcoes necessarias")
    
    print(f"\nRESUMO:")
    print(f"  Clubes com correcoes: {correcoes}")
    print(f"  Total de alteracoes: {total_alteracoes}")

if __name__ == "__main__":
    corrigir_vitoria_todos_csvs()
