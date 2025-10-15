#!/usr/bin/env python3
"""
Script para corrigir os jogos 9-14 adicionando IDs aos elementos HTML
"""

import re

def corrigir_jogo(numero_jogo, time_casa_antigo, time_fora_antigo, arena_antiga, campeonato_antigo, dia_antigo):
    """Corrige um jogo específico"""
    
    # Padrões para encontrar e substituir
    padroes = [
        # Escudo casa
        (rf'<img src="/static/escudos/[^"]*" \s*alt="{time_casa_antigo}" class="escudo-time"', 
         f'<img id="escudo-casa-jogo{numero_jogo}" src="/static/escudos/[^"]*" alt="{time_casa_antigo}" class="escudo-time"'),
        
        # Nome casa
        (rf'<span>{time_casa_antigo}</span>', 
         f'<span id="nome-casa-jogo{numero_jogo}">{time_casa_antigo}</span>'),
        
        # Escudo fora
        (rf'<img src="/static/escudos/[^"]*" \s*alt="{time_fora_antigo}" class="escudo-time"', 
         f'<img id="escudo-fora-jogo{numero_jogo}" src="/static/escudos/[^"]*" alt="{time_fora_antigo}" class="escudo-time"'),
        
        # Nome fora
        (rf'<span>{time_fora_antigo}</span>', 
         f'<span id="nome-fora-jogo{numero_jogo}">{time_fora_antigo}</span>'),
        
        # Game info
        (rf'<div class="game-info">{arena_antiga} \| {campeonato_antigo} \| {dia_antigo}</div>', 
         f'<div class="game-info" id="game-info-jogo{numero_jogo}">{arena_antiga} | {campeonato_antigo} | {dia_antigo}</div>'),
        
        # Label casa
        (rf'<div class="label">Coluna 1 \({time_casa_antigo}\)</div>', 
         f'<div class="label" id="label-casa-{numero_jogo}">Coluna 1 ({time_casa_antigo})</div>'),
        
        # Label fora
        (rf'<div class="label">Coluna 2 \({time_fora_antigo}\)</div>', 
         f'<div class="label" id="label-fora-{numero_jogo}">Coluna 2 ({time_fora_antigo})</div>'),
    ]
    
    return padroes

# Dados dos jogos 9-14
jogos = [
    {
        'numero': 9,
        'time_casa_antigo': 'BAHIA',
        'time_fora_antigo': 'PALMEIRAS',
        'arena_antiga': 'Arena Fonte Nova',
        'campeonato_antigo': 'Brasileirão Série A',
        'dia_antigo': 'Domingo'
    },
    {
        'numero': 10,
        'time_casa_antigo': 'FLUMINENSE',
        'time_fora_antigo': 'BOTAFOGO',
        'arena_antiga': 'Maracanã',
        'campeonato_antigo': 'Brasileirão Série A',
        'dia_antigo': 'Domingo'
    },
    {
        'numero': 11,
        'time_casa_antigo': 'CRICIÚMA',
        'time_fora_antigo': 'PAYSANDU',
        'arena_antiga': 'Heriberto Hülse',
        'campeonato_antigo': 'Brasileirão Série B',
        'dia_antigo': 'Domingo'
    },
    {
        'numero': 12,
        'time_casa_antigo': 'NEWCASTLE',
        'time_fora_antigo': 'ARSENAL',
        'arena_antiga': 'St. James\' Park',
        'campeonato_antigo': 'Premier League',
        'dia_antigo': 'Domingo'
    },
    {
        'numero': 13,
        'time_casa_antigo': 'BRAGANTINO',
        'time_fora_antigo': 'SANTOS',
        'arena_antiga': 'Nabi Abi Chedid',
        'campeonato_antigo': 'Brasileirão Série A',
        'dia_antigo': 'Domingo'
    },
    {
        'numero': 14,
        'time_casa_antigo': 'BARCELONA',
        'time_fora_antigo': 'REAL SOCIEDAD',
        'arena_antiga': 'Camp Nou',
        'campeonato_antigo': 'La Liga',
        'dia_antigo': 'Domingo'
    }
]

print("Script para corrigir jogos 9-14 criado!")
print("Dados dos jogos:")
for jogo in jogos:
    print(f"Jogo {jogo['numero']}: {jogo['time_casa_antigo']} vs {jogo['time_fora_antigo']}")
