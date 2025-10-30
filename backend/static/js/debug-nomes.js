/**
 * SCRIPT DE DEBUG - NOMES DOS TIMES
 * Copie e cole no console do navegador (F12) para ver os nomes exatos
 */

async function debugNomesTimesCompleto() {
    console.log('🔍 ===== DEBUG COMPLETO - NOMES DOS TIMES =====\n');
    
    try {
        // 1. Carregar dados da API
        const response = await fetch('/api/br/loteca/current');
        const data = await response.json();
        
        if (!data.success || !data.matches) {
            console.error('❌ Erro ao carregar API:', data.error);
            return;
        }
        
        console.log(`✅ ${data.matches.length} jogos carregados\n`);
        
        // 2. Focar nos jogos problemáticos
        const jogosProblem = [3, 5, 11, 12, 13]; // índices: 4, 6, 12, 13, 14
        
        jogosProblem.forEach(index => {
            const jogo = data.matches[index];
            const numeroJogo = index + 1;
            
            console.log(`🎯 JOGO ${numeroJogo}:`);
            console.log(`   Casa ORIGINAL: "${jogo.home_team}"`);
            console.log(`   Casa TIPO: ${typeof jogo.home_team}`);
            console.log(`   Casa LOWERCASE: "${jogo.home_team?.toLowerCase()}"`);
            console.log(`   Fora ORIGINAL: "${jogo.away_team}"`);
            console.log(`   Fora TIPO: ${typeof jogo.away_team}`);
            console.log(`   Fora LOWERCASE: "${jogo.away_team?.toLowerCase()}"`);
            console.log('');
        });
        
        // 3. Testar mapeamentos
        console.log('\n📊 TESTANDO MAPEAMENTOS:\n');
        
        jogosProblem.forEach(index => {
            const jogo = data.matches[index];
            const numeroJogo = index + 1;
            const casa = jogo.home_team;
            const fora = jogo.away_team;
            
            console.log(`🎯 JOGO ${numeroJogo}: ${casa} vs ${fora}`);
            
            // Testar se existe no JSON
            const resultado = verificarForcaElenco(casa, fora);
            
            console.log(`   Casa: ${resultado.casa ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
            console.log(`   Fora: ${resultado.fora ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
            
            if (resultado.casa) {
                console.log(`   ✅ Casa: ${resultado.casa.nome_oficial} - €${resultado.casa.valor_elenco_euros}M`);
            } else {
                console.log(`   ❌ Casa: Nome "${casa}" não mapeado!`);
            }
            
            if (resultado.fora) {
                console.log(`   ✅ Fora: ${resultado.fora.nome_oficial} - €${resultado.fora.valor_elenco_euros}M`);
            } else {
                console.log(`   ❌ Fora: Nome "${fora}" não mapeado!`);
            }
            
            console.log('');
        });
        
        // 4. Listar clubes disponíveis no JSON
        console.log('\n📋 CLUBES DISPONÍVEIS NO JSON:');
        if (forcaElencoData && forcaElencoData.clubes) {
            console.log(Object.keys(forcaElencoData.clubes));
        } else {
            console.log('❌ forcaElencoData não carregado!');
        }
        
    } catch (error) {
        console.error('❌ Erro:', error);
    }
    
    console.log('\n🔍 ===== FIM DO DEBUG =====');
}

// Executar automaticamente
debugNomesTimesCompleto();

