#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da nova lógica de atualização via JSON
"""

import sys
import os
sys.path.append('backend')

from ler_ultimos_cinco import ler_ultimos_cinco_serie_a, ler_ultimos_cinco_serie_b
from models.classificacao_db import ClassificacaoDB

def teste_nova_logica():
    print('=== TESTE DA NOVA LÓGICA ===')
    
    # Ler dados dos JSONs
    serie_a_data = ler_ultimos_cinco_serie_a()
    serie_b_data = ler_ultimos_cinco_serie_b()
    
    print(f'Série A: {len(serie_a_data)} times')
    print(f'Série B: {len(serie_b_data)} times')
    
    # Testar atualização no banco
    db = ClassificacaoDB()
    
    # Testar com Flamengo
    flamengo_ultimos = serie_a_data.get('flamengo', '')
    print(f'Flamengo: {flamengo_ultimos}')
    
    # Atualizar no banco
    success = db.atualizar_ultimos_confrontos_serie_a('Flamengo', flamengo_ultimos)
    print(f'Atualização Flamengo: {success}')
    
    # Testar com Palmeiras
    palmeiras_ultimos = serie_a_data.get('palmeiras', '')
    print(f'Palmeiras: {palmeiras_ultimos}')
    
    success = db.atualizar_ultimos_confrontos_serie_a('Palmeiras', palmeiras_ultimos)
    print(f'Atualização Palmeiras: {success}')
    
    print('=== TESTE CONCLUÍDO ===')

if __name__ == "__main__":
    teste_nova_logica()

