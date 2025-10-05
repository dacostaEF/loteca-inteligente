class CartolaVerificationProvider {
            constructor() {
                this.API_BASE = 'https://api.cartolafc.globo.com';
                this.cache = new Map();
                this.CACHE_TTL = 30 * 60 * 1000; // 30 minutos
            }

            async _get(endpoint) {
                const url = `${this.API_BASE}${endpoint}`;
                const cacheKey = url;
                
                // Verificar cache
                const cached = this.cache.get(cacheKey);
                if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
                    console.log(`[CartolaVerification] Cache hit: ${endpoint}`);
                    return cached.data;
                }

                try {
                    console.log(`[CartolaVerification] Buscando: ${url}`);
                    const response = await fetch(url, {
                        method: 'GET',
                        mode: 'cors',
                        headers: {
                            'Accept': 'application/json',
                        }
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }

                    const data = await response.json();
                    
                    // Armazenar no cache
                    this.cache.set(cacheKey, {
                        data: data,
                        timestamp: Date.now()
                    });

                    console.log(`[CartolaVerification] ✅ Dados obtidos: ${endpoint}`);
                    return data;
                    
                } catch (error) {
                    console.warn(`[CartolaVerification] ❌ Erro ao buscar ${endpoint}:`, error.message);
                    throw error;
                }
            }

            // BUSCAR TODAS AS CLASSIFICAÇÕES DISPONÍVEIS
            async getAvailableClassifications() {
                try {
                    console.log('[CartolaVerification] 🔍 Buscando classificações disponíveis...');
                    
                    // Buscar dados da rodada atual para ver quais campeonatos estão disponíveis
                    const rodadaData = await this._get('/rodadas');
                    const clubesData = await this._get('/clubes');
                    
                    const classifications = [];
                    
                    // Mapear campeonatos disponíveis
                    if (rodadaData && rodadaData.length > 0) {
                        classifications.push({
                            id: 'brasileirao_serie_a',
                            name: 'Brasileirão Série A',
                            type: 'nacional',
                            available: true,
                            lastUpdate: new Date().toISOString()
                        });
                    }
                    
                    // Verificar se há dados de clubes para outros campeonatos
                    if (clubesData && Object.keys(clubesData).length > 0) {
                        classifications.push({
                            id: 'brasileirao_serie_b',
                            name: 'Brasileirão Série B',
                            type: 'nacional',
                            available: true,
                            lastUpdate: new Date().toISOString()
                        });
                    }
                    
                    console.log(`[CartolaVerification] ✅ ${classifications.length} classificações encontradas`);
                    return classifications;
                    
                } catch (error) {
                    console.error('[CartolaVerification] ❌ Erro ao buscar classificações:', error);
                    return [];
                }
            }

            // BUSCAR CLASSIFICAÇÃO ESPECÍFICA
            async getClassification(campeonato) {
                try {
                    console.log(`[CartolaVerification] 📊 Buscando classificação: ${campeonato}`);
                    
                    let endpoint = '';
                    switch(campeonato) {
                        case 'brasileirao_serie_a':
                            endpoint = '/partidas';
                            break;
                        case 'brasileirao_serie_b':
                            endpoint = '/clubes';
                            break;
                        default:
                            throw new Error(`Campeonato não suportado: ${campeonato}`);
                    }
                    
                    const data = await this._get(endpoint);
                    return this._formatClassificationData(data, campeonato);
                    
                } catch (error) {
                    console.error(`[CartolaVerification] ❌ Erro ao buscar ${campeonato}:`, error);
                    return null;
                }
            }

            // FORMATAR DADOS DE CLASSIFICAÇÃO
            _formatClassificationData(data, campeonato) {
                if (campeonato === 'brasileirao_serie_a') {
                    // Processar dados de partidas para criar classificação
                    return this._processPartidasToClassification(data);
                } else if (campeonato === 'brasileirao_serie_b') {
                    // Processar dados de clubes
                    return this._processClubesToClassification(data);
                }
                return data;
            }

            // PROCESSAR PARTIDAS PARA CLASSIFICAÇÃO
            _processPartidasToClassification(partidasData) {
                // Implementar lógica para converter partidas em classificação
                console.log('[CartolaVerification] 📊 Processando partidas para classificação...');
                return {
                    campeonato: 'Brasileirão Série A',
                    rodada: partidasData.length > 0 ? partidasData[0].rodada : 0,
                    classificacao: [], // Será preenchido com lógica de cálculo
                    lastUpdate: new Date().toISOString()
                };
            }

            // PROCESSAR CLUBES PARA CLASSIFICAÇÃO
            _processClubesToClassification(clubesData) {
                console.log('[CartolaVerification] 📊 Processando clubes para classificação...');
                return {
                    campeonato: 'Brasileirão Série B',
                    total_clubes: Object.keys(clubesData).length,
                    clubes: Object.values(clubesData),
                    lastUpdate: new Date().toISOString()
                };
            }
        }

        // PROVIDER CENTRAL ADMIN - DADOS DA CENTRAL ADMIN