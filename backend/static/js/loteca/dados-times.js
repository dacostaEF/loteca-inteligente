/**
 * LOTECA X-RAY - Mapeamento de Nomes de Times
 * 
 * Dicionário unificado para normalização de nomes de times brasileiros.
 * Suporta múltiplas variações de nomes (com/sem acentos, abreviações, apelidos).
 * 
 * Uso: const chaveNormalizada = MAPEAMENTO_TIMES_BR[time.toLowerCase().trim()];
 */

const MAPEAMENTO_TIMES_BR = {
    'flamengo/rj': 'flamengo',
    'flamengo': 'flamengo',
    'palmeiras/sp': 'palmeiras', 
    'palmeiras': 'palmeiras',
    'são paulo/sp': 'sao_paulo',
    'sao paulo': 'sao_paulo',
    'são paulo': 'sao_paulo',
    'corinthians/sp': 'corinthians',
    'corinthians': 'corinthians',
    'atletico/mg': 'atletico_mg',
    'atletico mg': 'atletico_mg',
    'atlético-mg': 'atletico_mg',
    'atletico-mg': 'atletico_mg',
    'atlético mineiro/mg': 'atletico_mg',
    'atletico mineiro/mg': 'atletico_mg',
    'atlético mineiro': 'atletico_mg',
    'atletico mineiro': 'atletico_mg',
    'galo': 'atletico_mg',
    'internacional': 'internacional',
    'gremio/rs': 'gremio',
    'gremio': 'gremio',
    'grêmio': 'gremio',
    'cruzeiro/mg': 'cruzeiro',
    'cruzeiro': 'cruzeiro',
    'botafogo/rj': 'botafogo',
    'botafogo': 'botafogo',
    'vasco': 'vasco',
    'vasco da gama': 'vasco',
    'vasco/rj': 'vasco',
    'fluminense': 'fluminense',
    'athletico/pr': 'athletico_pr',
    'athletico-pr': 'athletico_pr',
    'athletico pr': 'athletico_pr',
    'fortaleza/ce': 'fortaleza',
    'fortaleza': 'fortaleza',
    'bahia/ba': 'bahia',
    'bahia': 'bahia',
    'santos': 'santos',
    // ✅ TIMES ADICIONADOS 2025 (TODAS AS VARIAÇÕES - API e CSV!)
    'mirassol': 'mirassol',
    'red bull bragantino': 'red_bull_bragantino',
    'bragantino': 'red_bull_bragantino',
    'ceará': 'ceara',
    'ceara': 'ceara',
    'sport': 'sport',
    'sport recife': 'sport',
    'juventude': 'juventude',
    // OPERÁRIO-PR (todos os formatos!)
    'operário-pr': 'operario_pr',
    'operario-pr': 'operario_pr',
    'operario pr': 'operario_pr',
    'operário': 'operario_pr',
    'operario': 'operario_pr',
    'fantasma': 'operario_pr',
    // VILA NOVA (todos os formatos!)
    'vila nova': 'vila_nova',
    'vila-nova': 'vila_nova',
    'tigre': 'vila_nova',
    // AVAÍ (todos os formatos!)
    'avai': 'avai',
    'avaí': 'avai',
    'avaí fc': 'avai',
    'leão da ilha': 'avai',
    // ATHLETIC-MG (todos os formatos!)
    'athletic-mg': 'athletic_mg',
    'athletic club': 'athletic_mg',
    'athletic mg': 'athletic_mg',
    'athletic': 'athletic_mg',
    'coelho': 'athletic_mg',
    // REMO (todos os formatos!)
    'remo': 'remo',
    'leão azul': 'remo',
    'clube do remo': 'remo',
    // CHAPECOENSE (todos os formatos!)
    'chapecoense': 'chapecoense',
    'chape': 'chapecoense',
    'verdão do oeste': 'chapecoense',
    // VITÓRIA
    'vitoria': 'vitoria',
    'vitória': 'vitoria',
    // GOIÁS
    'goias': 'goias',
    'goiás': 'goias',
    // ATHLETICO-PR (todos os formatos possíveis!)
    'atlhetico': 'athletico_pr',
    'athltetico-pr': 'athletico_pr',
    'athletico paranaense': 'athletico_pr',
    'furacão': 'athletico_pr',
    // VARIAÇÕES ADICIONAIS COM MAIÚSCULAS E BARRAS (usadas nos JSONs)
    'mirassol/sp': 'mirassol',
    'sao paulo/sp': 'sao_paulo',
    'bragantino/sp': 'red_bull_bragantino',
    'red bull bragantino/sp': 'red_bull_bragantino',
    'sport/pe': 'sport',
    'sport recife/pe': 'sport',
    'vitoria/ba': 'vitoria',
    'vitória/ba': 'vitoria',
    'ceara/ce': 'ceara',
    'ceará/ce': 'ceara',
    'internacional/rs': 'internacional',
    'fluminense/rj': 'fluminense',
    'fortaleza/ce': 'fortaleza',
    // TIMES EUROPEUS (Jogos internacionais da Loteca)
    'chelsea': 'chelsea',
    'chelsea/ing': 'chelsea',
    'wolves': 'wolves',
    'wolves/ing': 'wolves',
    'wolverhampton': 'wolves',
    'wolverhampton/ing': 'wolves',
    'parma': 'parma',
    'parma/it': 'parma',
    'milan': 'milan',
    'milan/it': 'milan',
    'ac milan': 'milan',
    'manchester city': 'manchester_city',
    'manchester city/ing': 'manchester_city',
    'man city': 'manchester_city',
    'liverpool': 'liverpool',
    'liverpool/ing': 'liverpool',
    'valencia': 'valencia',
    'valencia/esp': 'valencia',
    'real betis': 'real_betis',
    'real betis/esp': 'real_betis',
    'betis': 'real_betis',
};

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.MAPEAMENTO_TIMES_BR = MAPEAMENTO_TIMES_BR;
}

// Exportar como módulo (se suportado)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MAPEAMENTO_TIMES_BR };
}

