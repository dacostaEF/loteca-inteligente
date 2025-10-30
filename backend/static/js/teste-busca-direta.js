/**
 * TESTE DIRETO DE BUSCA NO JSON
 * Cole no console (F12) para diagnosticar
 */

console.log('🔍 ===== TESTE DE BUSCA DIRETA NO JSON =====\n');

// 1. Verificar se o JSON está carregado
if (!forcaElencoData) {
    console.error('❌ forcaElencoData NÃO carregado!');
} else {
    console.log('✅ forcaElencoData carregado!');
    console.log('📋 Clubes disponíveis:', Object.keys(forcaElencoData.clubes));
    console.log('');
}

// 2. Testar busca direta pelos 7 clubes problemáticos
const clubesProblema = [
    { nome: 'Athletico-PR', chaveEsperada: 'athletico_pr' },
    { nome: 'Avaí', chaveEsperada: 'avai' },
    { nome: 'Athletic-MG', chaveEsperada: 'athletic_mg' },
    { nome: 'Remo', chaveEsperada: 'remo' },
    { nome: 'Chapecoense', chaveEsperada: 'chapecoense' },
    { nome: 'Operário-PR', chaveEsperada: 'operario_pr' },
    { nome: 'Vila Nova', chaveEsperada: 'vila_nova' }
];

console.log('🧪 TESTANDO BUSCA DIRETA:\n');

clubesProblema.forEach(clube => {
    console.log(`🎯 ${clube.nome}`);
    
    // Testar busca direta no JSON
    const encontradoDireto = forcaElencoData.clubes[clube.chaveEsperada];
    console.log(`   Busca direta [${clube.chaveEsperada}]: ${encontradoDireto ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
    
    if (encontradoDireto) {
        console.log(`   ✅ Dados: ${encontradoDireto.nome_oficial} - €${encontradoDireto.valor_elenco_euros}M`);
    }
    
    // Testar através da função verificarForcaElenco
    const resultado = verificarForcaElenco(clube.nome, clube.nome);
    console.log(`   Função verificarForcaElenco: ${resultado.casa ? '✅ ENCONTRADO' : '❌ NÃO ENCONTRADO'}`);
    
    if (!resultado.casa) {
        // Debug do mapeamento
        const nomeLower = clube.nome.toLowerCase().trim();
        console.log(`   🔍 Nome lowercase: "${nomeLower}"`);
        
        // Tentar ver se existe no mapeamento
        console.log(`   🔍 Testando mapeamento...`);
        
        // Simular o que a função faz
        const mapeamentoTeste = {
            'athletico-pr': 'athletico_pr',
            'avaí': 'avai',
            'athletic-mg': 'athletic_mg',
            'remo': 'remo',
            'chapecoense': 'chapecoense',
            'operário-pr': 'operario_pr',
            'vila nova': 'vila_nova'
        };
        
        const chave = mapeamentoTeste[nomeLower];
        console.log(`   🔍 Chave do mapeamento teste: "${chave || 'NÃO ENCONTRADO'}"`);
    }
    
    console.log('');
});

console.log('🔍 ===== FIM DO TESTE =====');

