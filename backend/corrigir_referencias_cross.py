#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv

def corrigir_referencias_cross():
    """Corrigir referências cruzadas entre clubes"""
    print("=== CORRECAO DE REFERENCIAS CRUZADAS ===")
    
    base_dir = "models/Jogos"
    correcoes = 0
    
    # Mapeamento de correções
    mapeamento = {
        'Grê': 'Gre',  # Grêmio
        'São': 'Sao',  # São Paulo
        'Vitória': 'Vitoria',
        'Derrota': 'Derrota',
        'Empate': 'Empate'
    }
    
    # Processar cada CSV
    for item in os.listdir(base_dir):
        clube_dir = os.path.join(base_dir, item)
        if os.path.isdir(clube_dir):
            csv_path = os.path.join(clube_dir, "jogos.csv")
            
            if os.path.exists(csv_path):
                print(f"Corrigindo referencias em: {item}")
                
                # Ler arquivo
                linhas = []
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    linhas = list(reader)
                
                # Aplicar correções
                linhas_corrigidas = []
                for linha in linhas:
                    linha_corrigida = []
                    for campo in linha:
                        campo_corrigido = campo
                        for antigo, novo in mapeamento.items():
                            campo_corrigido = campo_corrigido.replace(antigo, novo)
                        linha_corrigida.append(campo_corrigido)
                    linhas_corrigidas.append(linha_corrigida)
                
                # Salvar arquivo corrigido
                with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(linhas_corrigidas)
                
                correcoes += 1
                print(f"  OK: {item} corrigido!")
    
    print(f"\nRESUMO: {correcoes} arquivos corrigidos!")

if __name__ == "__main__":
    corrigir_referencias_cross()
