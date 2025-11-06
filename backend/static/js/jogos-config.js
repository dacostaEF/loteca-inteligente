/**
 * ⚽ CONFIGURAÇÃO ÚNICA DOS JOGOS DA LOTECA
 * 
 * Este arquivo centraliza TODOS os dados dos jogos para evitar duplicação.
 * Usado por:
 * - loteca-functions.js (carregamento de dados)
 * - loteca-confrontos.js (renderização de confrontos)
 * 
 * IMPORTANTE: Ao mudar um jogo, alterar APENAS este arquivo!
 * 
 * Estrutura:
 * - csv: Nome do arquivo CSV com dados históricos
 * - timeCasa: Nome do time da casa (exato como aparece no CSV)
 * - timeFora: Nome do time visitante (exato como aparece no CSV)
 * - escudoCasa: Caminho do escudo do time da casa
 * - escudoFora: Caminho do escudo do time visitante
 */

export const JOGOS_LOTECA = {
    1: {
        csv: 'mirassol_vs_palmeiras.csv',
        timeCasa: 'MIRASSOL',
        timeFora: 'PALMEIRAS',
        escudoCasa: '/static/escudos/MIR_Mirassol/Mirassol.png',
        escudoFora: '/static/escudos/PAL_Palmeiras/Palmeiras.png'
    },
    2: {
        csv: 'Sport_vs_Atletico-MG.csv',
        timeCasa: 'SPORT',
        timeFora: 'ATLETICO-MG',
        escudoCasa: '/static/escudos/SPT_Sport/Sport.png',
        escudoFora: '/static/escudos/CAM_Atletico-MG/Atletico_MG.png'
    },
    3: {
        csv: 'vasco_vs_juventude.csv',
        timeCasa: 'VASCO',
        timeFora: 'JUVENTUDE',
        escudoCasa: '/static/escudos/VAS_Vasco/Vasco.png',
        escudoFora: '/static/escudos/JUV_Juventude/Juventude.PNG'
    },
    4: {
        csv: 'Internacional_vs_bahia.csv',
        timeCasa: 'INTERNACIONAL',
        timeFora: 'BAHIA',
        escudoCasa: '/static/escudos/INT_Internacional/Internacional.png',
        escudoFora: '/static/escudos/BAH_Bahia/Bahia.PNG'
    },
    5: {
        csv: 'Sao_Paulo_vs_bragantino.csv',
        timeCasa: 'SAO PAULO',
        timeFora: 'BRAGANTINO',
        escudoCasa: '/static/escudos/SAP_SaoPaulo/SaoPaulo.png',
        escudoFora: '/static/escudos/RBB_Bragantino/RedBull_Bragantino.png'
    },
    6: {
        csv: 'chelsea_vs_wolves.csv',
        timeCasa: 'CHELSEA',
        timeFora: 'WOLVES',
        escudoCasa: '/static/escudos/Chelsea/Chelsea.png',
        escudoFora: '/static/escudos/Wolverhampton/Wolfes.png'
    },
    7: {
        csv: 'parma_vs_milan.csv',
        timeCasa: 'PARMA',
        timeFora: 'MILAN',
        escudoCasa: '/static/escudos/Parma_IT/Parma.png',
        escudoFora: '/static/escudos/Milan_IT/Milan.png'
    },
    8: {
        csv: 'corinthians_vs_ceara.csv',
        timeCasa: 'CORINTHIANS',
        timeFora: 'CEARA',
        escudoCasa: '/static/escudos/COR_Corinthians/Corinthians.png',
        escudoFora: '/static/escudos/Ceara/ceara.png'
    },
    9: {
        csv: 'vitoria_vs_botafogo-RJ.csv',
        timeCasa: 'VITORIA',
        timeFora: 'BOTAFOGO',
        escudoCasa: '/static/escudos/VIT_Vitoria/Vitoria.png',
        escudoFora: '/static/escudos/Botafogo-RJ/Botafogo_RJ.png'
    },
    10: {
        csv: 'cruzeiro_vs_fluminente.csv',
        timeCasa: 'CRUZEIRO',
        timeFora: 'FLUMINENSE',
        escudoCasa: '/static/escudos/CRU_Cruzeiro/Cruzeiro.png',
        escudoFora: '/static/escudos/FLU_Fluminense/Fluminense.PNG'
    },
    11: {
        csv: 'Mancheter_city_vs_Liverpool.csv',
        timeCasa: 'MANCHESTER CITY',
        timeFora: 'LIVERPOOL',
        escudoCasa: '/static/escudos/Manchester_City/Manchester_City.png',
        escudoFora: '/static/escudos/Liverpool/liverpool.png'
    },
    12: {
        csv: 'Flamengo_vs_santos.csv',
        timeCasa: 'FLAMENGO',
        timeFora: 'SANTOS',
        escudoCasa: '/static/escudos/FLA_Flamengo/Flamengo.png',
        escudoFora: '/static/escudos/SAN_Santos/Santos.png'
    },
    13: {
        csv: 'valencia_real_betis.csv',
        timeCasa: 'VALENCIA',
        timeFora: 'REAL BETIS',
        escudoCasa: '/static/escudos/Valencia/valencia.png',
        escudoFora: '/static/escudos/Real_Betis/Real_Betis.png'
    },
    14: {
        csv: 'fortaleza_vs_gremio.csv',
        timeCasa: 'FORTALEZA',
        timeFora: 'GREMIO',
        escudoCasa: '/static/escudos/FOR_Fortaleza/Fortaleza.png',
        escudoFora: '/static/escudos/GRE_Gremio/Gremio.png'
    }
};

/**
 * Função auxiliar para compatibilidade com código antigo
 * Converte JOGOS_LOTECA para o formato antigo do jogosMap
 */
export function getJogosMapCompat() {
    const jogosMap = {};
    for (const [key, jogo] of Object.entries(JOGOS_LOTECA)) {
        jogosMap[key] = {
            csv: jogo.csv,
            casa: jogo.timeCasa,
            fora: jogo.timeFora
        };
    }
    return jogosMap;
}

