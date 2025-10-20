/**
 * Dashboard de Força dos Elencos
 * Sistema independente para evitar conflitos
 */

class DashboardForcaElenco {
    constructor() {
        this.executed = false;
        this.data = {
            top100: [],
            serieA: [],
            serieB: []
        };
        this.init();
    }

    init() {
        console.log('🚀 [DASHBOARD] Inicializando DashboardForcaElenco...');
        
        // Verificar se já foi executado
        if (this.executed) {
            console.log('⚠️ [DASHBOARD] Dashboard já foi executado, pulando...');
            return;
        }

        this.executed = true;
        this.loadData();
    }

    loadData() {
        console.log('📊 [DASHBOARD] Carregando dados...');
        
        // Buscar dados dos elementos HTML
        const top100Data = this.extractDataFromHTML('top100Clubs');
        const serieAData = this.extractDataFromHTML('serieAClubs');
        const serieBData = this.extractDataFromHTML('serieBClubs');

        this.data = {
            top100: top100Data || [],
            serieA: serieAData || [],
            serieB: serieBData || []
        };

        console.log('📊 [DASHBOARD] Dados carregados:');
        console.log('   Top 100:', this.data.top100.length, 'clubes');
        console.log('   Série A:', this.data.serieA.length, 'clubes');
        console.log('   Série B:', this.data.serieB.length, 'clubes');

        this.populateTop100();
        this.initTabs();
    }

    extractDataFromHTML(variableName) {
        try {
            // Buscar script que contém os dados
            const scripts = document.querySelectorAll('script');
            for (let script of scripts) {
                if (script.textContent.includes(variableName)) {
                    // Extrair dados usando regex
                    const regex = new RegExp(`${variableName}\\s*=\\s*(\\[.*?\\])`, 's');
                    const match = script.textContent.match(regex);
                    if (match) {
                        return JSON.parse(match[1]);
                    }
                }
            }
        } catch (error) {
            console.error('❌ [DASHBOARD] Erro ao extrair dados:', error);
        }
        return [];
    }

    populateTop100() {
        console.log('🔍 [DASHBOARD] Preenchendo Top 100...');
        const tbody = document.getElementById('top100Body');
        if (!tbody) {
            console.error('❌ [DASHBOARD] Elemento top100Body não encontrado!');
            return;
        }

        tbody.innerHTML = '';
        this.data.top100.forEach(club => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${club.posicao}</td>
                <td><strong>${club.clube}</strong></td>
                <td>${club.pais}</td>
                <td class="valor-cell">${club.valor}</td>
            `;
            tbody.appendChild(row);
        });
        console.log('✅ [DASHBOARD] Top 100 preenchido com', this.data.top100.length, 'clubes');
    }

    populateSerieA() {
        console.log('🔍 [DASHBOARD] Preenchendo Série A...');
        const tbody = document.getElementById('serieABody');
        if (!tbody) {
            console.error('❌ [DASHBOARD] Elemento serieABody não encontrado!');
            return;
        }

        tbody.innerHTML = '';
        this.data.serieA.forEach(club => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${club.posicao}</td>
                <td><strong>${club.clube}</strong></td>
                <td>${club.plantel}</td>
                <td>${club.idade_media}</td>
                <td>${club.estrangeiros}</td>
                <td class="valor-cell">${club.valor_total}</td>
                <td>${club.posse_bola}</td>
                <td>${club.passes_certos}</td>
                <td>${club.chutes_jogo}</td>
            `;
            tbody.appendChild(row);
        });
        console.log('✅ [DASHBOARD] Série A preenchida com', this.data.serieA.length, 'clubes');
    }

    populateSerieB() {
        console.log('🔍 [DASHBOARD] Preenchendo Série B...');
        const tbody = document.getElementById('serieBBody');
        if (!tbody) {
            console.error('❌ [DASHBOARD] Elemento serieBBody não encontrado!');
            return;
        }

        tbody.innerHTML = '';
        this.data.serieB.forEach(club => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${club.posicao}</td>
                <td><strong>${club.clube}</strong></td>
                <td>${club.plantel}</td>
                <td>${club.idade_media}</td>
                <td>${club.estrangeiros}</td>
                <td class="valor-cell">${club.valor_total}</td>
                <td>${club.posse_bola}</td>
                <td>${club.passes_certos}</td>
                <td>${club.chutes_jogo}</td>
            `;
            tbody.appendChild(row);
        });
        console.log('✅ [DASHBOARD] Série B preenchida com', this.data.serieB.length, 'clubes');
    }

    initTabs() {
        console.log('🚀 [DASHBOARD] Inicializando sistema de abas...');
        
        // Remover listeners antigos se existirem
        if (window.dashboardTabListener) {
            document.removeEventListener('click', window.dashboardTabListener);
        }

        // Criar novo listener com namespace
        window.dashboardTabListener = (e) => {
            if (e.target && e.target.classList.contains('tab-btn') && e.target.closest('.forca-elenco-dashboard')) {
                const targetTab = e.target.getAttribute('data-tab');
                console.log('🔄 [DASHBOARD] Mudando para aba:', targetTab);

                // Remover active de todos
                document.querySelectorAll('.forca-elenco-dashboard .tab-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.forca-elenco-dashboard .tab-content').forEach(content => content.classList.remove('active'));

                // Ativar aba selecionada
                e.target.classList.add('active');
                const targetElement = document.getElementById(targetTab);
                if (targetElement) {
                    targetElement.classList.add('active');
                }

                // Preencher dados da aba ativa
                setTimeout(() => {
                    if (targetTab === 'top100') {
                        this.populateTop100();
                    } else if (targetTab === 'serieA') {
                        this.populateSerieA();
                    } else if (targetTab === 'serieB') {
                        this.populateSerieB();
                    }
                }, 50);
            }
        };

        // Adicionar listener
        document.addEventListener('click', window.dashboardTabListener);
        console.log('✅ [DASHBOARD] Sistema de abas inicializado!');
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Aguardar um pouco para garantir que o HTML foi inserido
    setTimeout(() => {
        if (document.querySelector('.forca-elenco-dashboard')) {
            console.log('🎯 [DASHBOARD] Dashboard encontrado, inicializando...');
            new DashboardForcaElenco();
        }
    }, 200);
});

// Função global para inicialização manual
window.initDashboardForcaElenco = function() {
    console.log('🔄 [DASHBOARD] Inicialização manual...');
    new DashboardForcaElenco();
};
