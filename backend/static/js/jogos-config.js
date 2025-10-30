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
        csv: 'corinthians_gremio.csv',
        timeCasa: 'CORINTHIANS',
        timeFora: 'GREMIO',
        escudoCasa: '/static/escudos/COR_Corinthians/Corinthians.png',
        escudoFora: '/static/escudos/GRE_Gremio/Gremio.png'
    },
    2: {
        csv: 'santos_fortaleza.csv',
        timeCasa: 'SANTOS',
        timeFora: 'FORTALEZA',
        escudoCasa: '/static/escudos/SAN_Santos/Santos.png',
        escudoFora: '/static/escudos/FOR_Fortaleza/Fortaleza.png'
    },
    3: {
        csv: 'cruzeiro_vitoria.csv',
        timeCasa: 'CRUZEIRO',
        timeFora: 'VITORIA',
        escudoCasa: '/static/escudos/CRU_Cruzeiro/Cruzeiro.png',
        escudoFora: '/static/escudos/VIT_Vitoria/Vitoria.png'
    },
    4: {
        csv: 'goias_athletico-pr.csv',
        timeCasa: 'GOIAS',
        timeFora: 'ATHLETICO-PR',
        escudoCasa: '/static/escudos/GOI_Goias/Goias.png',
        escudoFora: '/static/escudos/Athletico-PR/Athletico_PR.png'
    },
    5: {
        csv: 'mirassol_botafogo.csv',
        timeCasa: 'MIRASSOL',
        timeFora: 'BOTAFOGO',
        escudoCasa: '/static/escudos/MIR_Mirassol/Mirassol.png',
        escudoFora: '/static/escudos/Botafogo-RJ/Botafogo_RJ.png'
    },
    6: {
        csv: 'avai_athetic-mg.csv',
        timeCasa: 'AVAI',
        timeFora: 'ATHLETIC-MG',
        escudoCasa: '/static/escudos/Avaí/Avaí.PNG',
        escudoFora: '/static/escudos/Athletic-MG/Athletic-MG.PNG'
    },
    7: {
        csv: 'flamengo_sport.csv',
        timeCasa: 'FLAMENGO',
        timeFora: 'SPORT',
        escudoCasa: '/static/escudos/FLA_Flamengo/Flamengo.png',
        escudoFora: '/static/escudos/SPT_Sport/Sport.png'
    },
    8: {
        csv: 'bahia_bragantino.csv',
        timeCasa: 'BAHIA',
        timeFora: 'RED BULL BRAGANTINO',
        escudoCasa: '/static/escudos/BAH_Bahia/Bahia.PNG',
        escudoFora: '/static/escudos/RBB_Bragantino/RedBull_Bragantino.png'
    },
    9: {
        csv: 'ceara_fluminense.csv',
        timeCasa: 'Ceará',
        timeFora: 'Fluminense',
        escudoCasa: '/static/escudos/Ceara/ceara.png',
        escudoFora: '/static/escudos/FLU_Fluminense/Fluminense.PNG'
    },
    10: {
        csv: 'juventude_palmeiras.csv',
        timeCasa: 'Juventude',
        timeFora: 'Palmeiras',
        escudoCasa: '/static/escudos/JUV_Juventude/Juventude.PNG',
        escudoFora: '/static/escudos/PAL_Palmeiras/Palmeiras.png'
    },
    11: {
        csv: 'internacional_atletico-mg.csv',
        timeCasa: 'Internacional',
        timeFora: 'Atlético-MG',
        escudoCasa: '/static/escudos/INT_Internacional/Internacional.png',
        escudoFora: '/static/escudos/CAM_Atletico-MG/Atletico_MG.png'
    },
    12: {
        csv: 'remo_chapecoense.csv',
        timeCasa: 'remo',
        timeFora: 'chapecoense',
        escudoCasa: '/static/escudos/Remo/Remo.PNG',
        escudoFora: '/static/escudos/Chapecoense/Chapecoense.PNG'
    },
    13: {
        csv: 'vasco_sao_paulo.csv',
        timeCasa: 'Vasco',
        timeFora: 'São Paulo',
        escudoCasa: '/static/escudos/VAS_Vasco/Vasco.png',
        escudoFora: '/static/escudos/SAP_SaoPaulo/SaoPaulo.png'
    },
    14: {
        csv: 'operario-pr_vilanova.csv',
        timeCasa: 'Operário-PR',
        timeFora: 'Vila Nova',
        escudoCasa: '/static/escudos/OPE_Operario-PR/Operario_PR.PNG',
        escudoFora: '/static/escudos/Vila_Nova/Vila_Nova.PNG'
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

