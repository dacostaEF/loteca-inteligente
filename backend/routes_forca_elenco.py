"""
API Dedicada para Força dos Elencos
Dashboard mundial de análise de elencos
"""

from flask import Blueprint, render_template, jsonify, request
import json
import os
import csv
import unicodedata

# ===== OTIMIZAÇÃO: DEBUG MODE =====
# Ativar logs apenas em desenvolvimento (localhost/127.0.0.1)
DEBUG = os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'True'

# Blueprint para a API de força dos elencos
forca_elenco_bp = Blueprint('forca_elenco', __name__, url_prefix='/api/forca-elenco')

def _normalize_headers(d):
    """Normaliza chaves: minúsculas, sem acento, sem % e espaços extras"""
    def normalize_string(s):
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        return s.strip().lower().replace('%','').replace('  ',' ')
    return { normalize_string(k): v for k, v in d.items() }

@forca_elenco_bp.route('/dashboard')
def dashboard():
    """Renderiza o dashboard de força dos elencos"""
    # ===== LOG APENAS EM DEBUG =====
    if DEBUG:
        print("🚀 [API-FORCA-ELENCO] Dashboard solicitado!")
    try:
        # Caminho configurável para os arquivos CSV
        base_dir = os.environ.get('FORCA_ELENCO_CSV_DIR') or os.path.join(os.path.dirname(__file__), 'models', 'EstatisticasElenco')
        top100_csv = os.path.join(base_dir, 'Valor_Elenco_top_100_clubes_mais_valiosos.csv')
        serie_a_csv = os.path.join(base_dir, 'Valor_Elenco_serie_a_brasileirao.csv')
        serie_b_csv = os.path.join(base_dir, 'Valor_Elenco_serie_b_brasileirao.csv')
        
        # Ler dados dos CSVs
        top100_data = []
        serie_a_data = []
        serie_b_data = []
        
        # Ler Top 100 Mundial
        if DEBUG:
            print(f"🔍 Verificando arquivo Top 100: {top100_csv}")
            print(f"📁 Arquivo existe: {os.path.exists(top100_csv)}")
        if os.path.exists(top100_csv):
            with open(top100_csv, 'r', encoding='utf-8-sig') as f:  # utf-8-sig para BOM
                reader = csv.DictReader(f)
                for row in reader:
                    r = _normalize_headers(row)
                    top100_data.append({
                        'posicao': r.get('posicao') or r.get('posição') or '',
                        'clube': r.get('clube', ''),
                        'pais': r.get('pais') or r.get('país') or '',
                        'valor': r.get('valor', '')
                    })
            if DEBUG:
                print(f"✅ Top 100 carregado: {len(top100_data)} clubes")
        
        # Ler Série A
        if DEBUG:
            print(f"🔍 Verificando arquivo Série A: {serie_a_csv}")
            print(f"📁 Arquivo existe: {os.path.exists(serie_a_csv)}")
        if os.path.exists(serie_a_csv):
            with open(serie_a_csv, 'r', encoding='utf-8-sig') as f:  # utf-8-sig para BOM
                reader = csv.DictReader(f)
                for row in reader:
                    r = _normalize_headers(row)
                    serie_a_data.append({
                        'posicao': r.get('posicao') or r.get('posição') or '',
                        'clube': r.get('clube', ''),
                        'plantel': r.get('plantel', ''),
                        'idade_media': r.get('idade media') or r.get('idade média') or '',
                        'estrangeiros': r.get('estrangeiros', ''),
                        'valor_medio': r.get('valor medio') or r.get('valor médio') or '',
                        'valor_total': r.get('valor total') or r.get('valor total') or '',
                        'posse_bola': r.get('posse bola') or r.get('posse bola (%)') or '',
                        'passes_certos': r.get('passes certos') or r.get('passes certos') or '',
                        'chutes_jogo': r.get('chutes/jogo') or r.get('chutes jogo') or ''
                    })
                    # ❌ REMOVIDO: print de cada clube (20 prints!)
            if DEBUG:
                print(f"✅ Série A carregada: {len(serie_a_data)} clubes")
        
        # Ler Série B
        if DEBUG:
            print(f"🔍 Verificando arquivo Série B: {serie_b_csv}")
            print(f"📁 Arquivo existe: {os.path.exists(serie_b_csv)}")
        if os.path.exists(serie_b_csv):
            with open(serie_b_csv, 'r', encoding='utf-8-sig') as f:  # utf-8-sig para BOM
                reader = csv.DictReader(f)
                for row in reader:
                    r = _normalize_headers(row)
                    serie_b_data.append({
                        'posicao': r.get('posicao') or r.get('posição') or '',
                        'clube': r.get('clube', ''),
                        'plantel': r.get('plantel', ''),
                        'idade_media': r.get('idade media') or r.get('idade média') or '',
                        'estrangeiros': r.get('estrangeiros', ''),
                        'valor_medio': r.get('valor medio') or r.get('valor médio') or '',
                        'valor_total': r.get('valor total') or r.get('valor total') or '',
                        'posse_bola': r.get('posse bola') or r.get('posse bola (%)') or '',
                        'passes_certos': r.get('passes certos') or r.get('passes certos') or '',
                        'chutes_jogo': r.get('chutes/jogo') or r.get('chutes jogo') or ''
                    })
                    # ❌ REMOVIDO: print de cada clube (20 prints!)
            if DEBUG:
                print(f"✅ Série B carregada: {len(serie_b_data)} clubes")
        
        if DEBUG:
            print(f"📊 Resumo dos dados carregados:")
            print(f"   Top 100: {len(top100_data)} clubes")
            print(f"   Série A: {len(serie_a_data)} clubes") 
            print(f"   Série B: {len(serie_b_data)} clubes")
        
        # Dados de teste se não conseguir carregar dos CSVs
        if not top100_data and not serie_a_data and not serie_b_data:
            # ⚠️ Print CRÍTICO: Sempre mostrar quando não houver dados
            print("⚠️ [CRÍTICO] Nenhum dado CSV carregado, usando dados de teste...")
            top100_data = [
                {"posicao": "1", "clube": "Real Madrid", "pais": "Espanha", "valor": "€ 1.726 M"},
                {"posicao": "2", "clube": "Manchester City", "pais": "Inglaterra", "valor": "€ 1.538 M"}
            ]
            serie_a_data = [
                {"posicao": "1", "clube": "Palmeiras", "plantel": "29", "idade_media": "26.3", "estrangeiros": "8", "valor_medio": "€ 7.32 mi.", "valor_total": "€ 7.32 mi.", "posse_bola": "52.1%", "passes_certos": "340", "chutes_jogo": "4.7"}
            ]
            serie_b_data = [
                {"posicao": "1", "clube": "Athletico Paranaense", "plantel": "33", "idade_media": "26.5", "estrangeiros": "10", "valor_medio": "€ 1.17 mi.", "valor_total": "€ 1.17 mi.", "posse_bola": "54.8%", "passes_certos": "356", "chutes_jogo": "11.2"}
            ]
        
        if top100_data or serie_a_data or serie_b_data:
            # Criar HTML dinâmico com os dados
            dashboard_html = f"""
            <div class="forca-elenco-dashboard">
                <div class="tabs">
                    <button class="fe-tab-btn active" data-tab="top100">🌍 Top 100 Mundial</button>
                    <button class="fe-tab-btn" data-tab="serieA">🇧🇷 Série A</button>
                    <button class="fe-tab-btn" data-tab="serieB">🇧🇷 Série B</button>
                </div>
                
                <div class="fe-tab-content active" id="top100">
                    <h2>Top 100 Clubes Mundiais</h2>
                    <div class="info-box blue">
                        <p><strong>Resumo:</strong> {len(top100_data)} clubes, valores baseados em gastos com transferências</p>
                        <p><strong>Fonte:</strong> Dados atualizados 2025</p>
                    </div>
                    
                    <div class="table-container">
                        <table id="top100Table" class="serie-a">
                            <thead>
                                <tr>
                                    <th>Posição</th>
                                    <th>Clube</th>
                                    <th>País</th>
                                    <th>Valor</th>
                                </tr>
                            </thead>
                            <tbody id="top100Body">
                                <!-- Dados serão inseridos via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="fe-tab-content" id="serieA">
                    <h2>Série A do Campeonato Brasileiro</h2>
                    <div class="info-box green">
                        <p><strong>Resumo:</strong> {len(serie_a_data)} clubes da Série A com análise detalhada</p>
                        <p><strong>Dados:</strong> Plantel, idade média, estrangeiros, valores e estatísticas</p>
                    </div>
                    
                    <div class="table-container">
                        <table id="serieATable" class="serie-a">
                            <thead>
                                <tr>
                                    <th>Posição</th>
                                    <th>Clube</th>
                                    <th>Plantel</th>
                                    <th>Idade Média</th>
                                    <th>Estrangeiros</th>
                                    <th>Valor Total</th>
                                    <th>Posse Bola</th>
                                    <th>Passes Certos</th>
                                    <th>Chutes/Jogo</th>
                                </tr>
                            </thead>
                            <tbody id="serieABody">
                                <!-- Dados serão inseridos via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="fe-tab-content" id="serieB">
                    <h2>Série B do Campeonato Brasileiro</h2>
                    <div class="info-box yellow">
                        <p><strong>Resumo:</strong> {len(serie_b_data)} clubes da Série B com análise detalhada</p>
                        <p><strong>Dados:</strong> Plantel, idade média, estrangeiros, valores e estatísticas</p>
                    </div>
                    
                    <div class="table-container">
                        <table id="serieBTable" class="serie-b">
                            <thead>
                                <tr>
                                    <th>Posição</th>
                                    <th>Clube</th>
                                    <th>Plantel</th>
                                    <th>Idade Média</th>
                                    <th>Estrangeiros</th>
                                    <th>Valor Total</th>
                                    <th>Posse Bola</th>
                                    <th>Passes Certos</th>
                                    <th>Chutes/Jogo</th>
                                </tr>
                            </thead>
                            <tbody id="serieBBody">
                                <!-- Dados serão inseridos via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Dados compilados do Observatório do Futebol e Transfermarkt.com.br</p>
                </div>
            </div>
            
               <script>
               // ===== TESTE DE EXECUÇÃO =====
               console.log('🚀 [DASHBOARD] Script executando!');
               
               // ===== INJEÇÃO DE DADOS (IDÊNTICA AO TESTE) =====
               window.__TOP100__ = {json.dumps(top100_data, ensure_ascii=False)};
               window.__SERIE_A__ = {json.dumps(serie_a_data, ensure_ascii=False)};
               window.__SERIE_B__ = {json.dumps(serie_b_data, ensure_ascii=False)};
               
               console.log('📊 [DASHBOARD] Dados injetados:');
               console.log('   Top 100:', window.__TOP100__?.length || 0, 'clubes');
               console.log('   Série A:', window.__SERIE_A__?.length || 0, 'clubes');
               console.log('   Série B:', window.__SERIE_B__?.length || 0, 'clubes');
               
               // ===== VERIFICAÇÃO IMEDIATA =====
               console.log('🔍 [DASHBOARD] Verificação imediata:');
               console.log('   window.__TOP100__:', typeof window.__TOP100__, Array.isArray(window.__TOP100__));
               console.log('   window.__SERIE_A__:', typeof window.__SERIE_A__, Array.isArray(window.__SERIE_A__));
               console.log('   window.__SERIE_B__:', typeof window.__SERIE_B__, Array.isArray(window.__SERIE_B__));
               
               // ===== DEBUG DETALHADO =====
               if (window.__TOP100__ && window.__TOP100__.length > 0) {{
                   console.log('✅ Top 100 OK - Primeiro clube:', window.__TOP100__[0]);
               }} else {{
                   console.log('❌ Top 100 VAZIO ou UNDEFINED');
               }}
               
               if (window.__SERIE_A__ && window.__SERIE_A__.length > 0) {{
                   console.log('✅ Série A OK - Primeiro clube:', window.__SERIE_A__[0]);
               }} else {{
                   console.log('❌ Série A VAZIO ou UNDEFINED');
               }}
               
               if (window.__SERIE_B__ && window.__SERIE_B__.length > 0) {{
                   console.log('✅ Série B OK - Primeiro clube:', window.__SERIE_B__[0]);
               }} else {{
                   console.log('❌ Série B VAZIO ou UNDEFINED');
               }}
               </script>
            
               <script>
               // ===== DASHBOARD IDÊNTICO AO TESTE QUE FUNCIONA =====
               (function(){{
                   // ===== util =====
                   const qs = (s, r=document)=>r.querySelector(s);
                   const qsa = (s, r=document)=>[...r.querySelectorAll(s)];

                   function log(...a){{ console.log('[DASHBOARD]', ...a); }}
                   function clear(el){{ while(el && el.firstChild) el.removeChild(el.firstChild); }}

                   function makeRow(cells){{
                       const tr = document.createElement('tr');
                       for (const c of cells){{
                           const td = document.createElement('td');
                           if (c === cells[1]) {{ // Nome do clube em negrito
                               td.innerHTML = `<strong>${{(c ?? '—').toString()}}</strong>`;
                           }} else if (c === cells[cells.length-1] && c && c.toString().includes('€')) {{ // Valor com classe especial
                               td.className = 'valor-cell';
                               td.textContent = (c ?? '—').toString();
                           }} else {{
                               td.textContent = (c ?? '—').toString();
                           }}
                           tr.appendChild(td);
                       }}
                       return tr;
                   }}

                   // Removido RENDERED - sempre renderizar

                   function haveDatasets(){{
                       return Array.isArray(window.__TOP100__) &&
                              Array.isArray(window.__SERIE_A__) &&
                              Array.isArray(window.__SERIE_B__);
                   }}

                   function checkDOM(){{
                       const ok = qs('#top100Body') && qs('#serieABody') && qs('#serieBBody') &&
                                  qs('.fe-tab-btn[data-tab="top100"]') && qs('.fe-tab-btn[data-tab="serieA"]') && qs('.fe-tab-btn[data-tab="serieB"]');
                       if (!ok) console.error('IDs/seletores não encontrados. Confirme: #top100Body, #serieABody, #serieBBody e botões .fe-tab-btn[data-tab].');
                       return ok;
                   }}

                   function renderTop100(){{
                       const tb = qs('#top100Body'); if (!tb) return;
                       clear(tb);
                       for (const r of (window.__TOP100__ || [])){{
                           tb.appendChild(makeRow([r.posicao, r.clube, r.pais, r.valor]));
                       }}
                       log('Top 100 preenchido:', (window.__TOP100__||[]).length);
                   }}

                   function renderSerieA(){{
                       console.log('🎯 [DASHBOARD] Renderizando Série A...');
                       const tb = qs('#serieABody'); 
                       if (!tb) {{
                           console.error('❌ [DASHBOARD] #serieABody não encontrado!');
                           console.log('🔍 [DASHBOARD] Procurando elementos DOM...');
                           console.log('   #serieABody:', document.getElementById('serieABody'));
                           console.log('   .forca-elenco-dashboard:', document.querySelector('.forca-elenco-dashboard'));
                           return;
                       }}
                       console.log('✅ [DASHBOARD] #serieABody encontrado!');
                       console.log('📊 [DASHBOARD] Dados Série A:', window.__SERIE_A__?.length || 0, 'clubes');
                       clear(tb);
                       for (const r of (window.__SERIE_A__ || [])){{
                           console.log('📝 [DASHBOARD] Adicionando linha Série A:', r.clube);
                           tb.appendChild(makeRow([
                               r.posicao, r.clube, r.plantel, r.idade_media, r.estrangeiros,
                               r.valor_total, r.posse_bola, r.passes_certos, r.chutes_jogo
                           ]));
                       }}
                       log('Série A preenchida:', (window.__SERIE_A__||[]).length);
                       console.log('✅ [DASHBOARD] Série A renderizada com sucesso!');
                   }}

                   function renderSerieB(){{
                       console.log('🎯 [DASHBOARD] Renderizando Série B...');
                       const tb = qs('#serieBBody'); 
                       if (!tb) {{
                           console.error('❌ [DASHBOARD] #serieBBody não encontrado!');
                           console.log('🔍 [DASHBOARD] Procurando elementos DOM...');
                           console.log('   #serieBBody:', document.getElementById('serieBBody'));
                           console.log('   .forca-elenco-dashboard:', document.querySelector('.forca-elenco-dashboard'));
                           return;
                       }}
                       console.log('✅ [DASHBOARD] #serieBBody encontrado!');
                       console.log('📊 [DASHBOARD] Dados Série B:', window.__SERIE_B__?.length || 0, 'clubes');
                       clear(tb);
                       for (const r of (window.__SERIE_B__ || [])){{
                           console.log('📝 [DASHBOARD] Adicionando linha Série B:', r.clube);
                           tb.appendChild(makeRow([
                               r.posicao, r.clube, r.plantel, r.idade_media, r.estrangeiros,
                               r.valor_total, r.posse_bola, r.passes_certos, r.chutes_jogo
                           ]));
                       }}
                       log('Série B preenchida:', (window.__SERIE_B__||[]).length);
                       console.log('✅ [DASHBOARD] Série B renderizada com sucesso!');
                   }}

                   function showTab(tab){{
                       console.log('🔄 [DASHBOARD] Mostrando aba:', tab);
                       
                       // Escopo local - apenas dentro do dashboard
                       const root = document.querySelector('#forca-elenco-content');
                       if (!root) {{
                           console.error('❌ [DASHBOARD] Container não encontrado');
                           return;
                       }}
                       
                       // Desativa apenas botões do dashboard
                       root.querySelectorAll('.fe-tab-btn').forEach(b => b.classList.remove('active'));
                       root.querySelector(`[data-tab="${{tab}}"]`)?.classList.add('active');
                       
                       // Esconde/mostra apenas conteúdos do dashboard
                       root.querySelectorAll('.fe-tab-content').forEach(c => {{
                           c.classList.remove('active');
                           c.style.display = 'none';
                       }});
                       const targetTab = root.querySelector('#'+tab);
                       if (targetTab) {{
                           targetTab.classList.add('active');
                           targetTab.style.display = 'block';
                           console.log('👁️ [DASHBOARD] Mostrando:', targetTab.id);
                       }} else {{
                           console.error('❌ [DASHBOARD] Aba não encontrada:', tab);
                       }}
                       
                       // render SEMPRE (não sob demanda)
                       if (tab==='top100') {{
                           console.log('🎯 [DASHBOARD] Renderizando Top 100...');
                           renderTop100();
                       }}
                       if (tab==='serieA') {{
                           console.log('🎯 [DASHBOARD] Renderizando Série A...');
                           renderSerieA();
                       }}
                       if (tab==='serieB') {{
                           console.log('🎯 [DASHBOARD] Renderizando Série B...');
                           renderSerieB();
                       }}
                   }}

                   function bindTabs(){{
                       // Sistema de delegação com escopo local
                       const root = document.querySelector('#forca-elenco-content');
                       if (!root) {{
                           console.error('❌ [DASHBOARD] Container não encontrado para bind');
                           return;
                       }}
                       
                       // Remove listener anterior se existir
                       if (window.dashboardTabListener) {{
                           document.removeEventListener('click', window.dashboardTabListener);
                       }}
                       
                       // Cria novo listener com escopo local
                       window.dashboardTabListener = function (e) {{
                           const btn = e.target.closest('.fe-tab-btn');
                           if (!btn || !root.contains(btn)) return;
                           
                           e.preventDefault();
                           e.stopPropagation();
                           
                           const targetTab = btn.dataset.tab;
                           console.log('🖱️ [DASHBOARD] Clique em:', targetTab);
                           
                           showTab(targetTab);
                       }};
                       
                       document.addEventListener('click', window.dashboardTabListener);
                       console.log('✅ [DASHBOARD] Event listeners configurados com escopo local');
                   }}

                   // ===== boot com espera ativa (IDÊNTICO AO TESTE) =====
                   function boot(attempt=0){{
                       console.log('🔧 [DASHBOARD] Boot executando, tentativa:', attempt);
                       if (!checkDOM()) {{
                           console.error('❌ [DASHBOARD] DOM não encontrado!');
                           return; // IDs errados: aborta já
                       }}
                       if (!haveDatasets()){{
                           if (attempt===0) console.warn('⏳ [DASHBOARD] Aguardando datasets do servidor…');
                           if (attempt > 60) {{ console.error('❌ [DASHBOARD] Dados não chegaram. Verifique injeção das variáveis window.__TOP100__/__SERIE_A__/__SERIE_B__.'); return; }}
                           return setTimeout(()=>boot(attempt+1), 100); // espera até 6s
                       }}
                       console.log('✅ [DASHBOARD] Datasets encontrados!');
                       log('datasets', {{
                           top100: window.__TOP100__?.length||0,
                           serieA: window.__SERIE_A__?.length||0,
                           serieB: window.__SERIE_B__?.length||0
                       }});
                       bindTabs();
                       // primeira render: Top 100
                       console.log('🎯 [DASHBOARD] Renderizando Top 100...');
                       showTab('top100');
                   }}

                   console.log('📝 [DASHBOARD] Adicionando listener DOMContentLoaded...');
                   document.addEventListener('DOMContentLoaded', boot);
                   
                   // ===== TESTE IMEDIATO =====
                   console.log('🧪 [DASHBOARD] Teste imediato...');
                   setTimeout(() => {{
                       console.log('⏰ [DASHBOARD] Teste após 1s...');
                       boot(999); // Forçar execução
                   }}, 1000);
                   
                   // ===== PRESERVAR ABA PRINCIPAL =====
                   function preserveMainTab() {{
                       const mainTab = document.querySelector('[data-tab="forca-elenco"]') || 
                                      document.querySelector('#forca-elenco-tab') ||
                                      document.querySelector('a[href="#forca-elenco"]');
                       if (mainTab) {{
                           mainTab.classList.add('active');
                           console.log('🔒 [DASHBOARD] Aba principal preservada');
                       }}
                   }}
                   
                   // Sistema de escopo local elimina a necessidade de proteção
                   
                   // ===== FUNÇÃO DE DEBUG GLOBAL =====
                   window.debugDashboard = function() {{
                       console.log('🔍 [DEBUG] Verificação completa:');
                       console.log('   window.__TOP100__:', window.__TOP100__);
                       console.log('   window.__SERIE_A__:', window.__SERIE_A__);
                       console.log('   window.__SERIE_B__:', window.__SERIE_B__);
                       console.log('   DOM #top100Body:', document.getElementById('top100Body'));
                       console.log('   DOM #serieABody:', document.getElementById('serieABody'));
                       console.log('   DOM #serieBBody:', document.getElementById('serieBBody'));
                       console.log('   Botões:', document.querySelectorAll('[data-tab]'));
                       
                       // Teste manual de renderização
                       if (window.__TOP100__ && window.__TOP100__.length > 0) {{
                           console.log('🧪 [DEBUG] Testando renderização manual Top 100...');
                           renderTop100();
                       }}
                       
                       if (window.__SERIE_A__ && window.__SERIE_A__.length > 0) {{
                           console.log('🧪 [DEBUG] Testando renderização manual Série A...');
                           renderSerieA();
                       }}
                       
                       if (window.__SERIE_B__ && window.__SERIE_B__.length > 0) {{
                           console.log('🧪 [DEBUG] Testando renderização manual Série B...');
                           renderSerieB();
                       }}
                   }};
                   
                   console.log('🔧 [DASHBOARD] Use window.debugDashboard() para debug manual');
               }})();
               </script>
            """
            
            # Adicionar estilos CSS
            css_styles = """
            <style>
            .forca-elenco-dashboard {
                max-width: 1400px;
                margin: 0 auto;
                background: #1a1a1a;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
                overflow: hidden;
                border: 1px solid #333;
                padding: 20px;
            }
            
            
            .tabs {
                display: flex;
                justify-content: center;
                margin-bottom: 1rem;
                border-bottom: 1px solid #333;
            }
            
            .fe-tab-btn {
                background: #2a2a2a;
                color: #94a3b8;
                border: none;
                padding: 12px 24px;
                margin: 0 5px;
                border-radius: 8px 8px 0 0;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .fe-tab-btn.active {
                background: #A855F7;
                color: white;
            }
            
            .fe-tab-btn:hover {
                background: #7C3AED;
                color: white;
            }
            
            .fe-tab-content {
                display: none;
                padding: 20px;
            }
            
            .fe-tab-content.active {
                display: block;
            }
            
            .tab-content h2 {
                color: #A855F7;
                margin-bottom: 1rem;
                font-size: 1.5rem;
            }
            
            .info-box {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 0.9rem;
                border: 1px solid #333;
            }
            
            .info-box.blue {
                background: #1e3a8a;
                color: #bfdbfe;
                border-color: #3b82f6;
            }
            
            .info-box.green {
                background: #064e3b;
                color: #a7f3d0;
                border-color: #10b981;
            }
            
            .info-box.yellow {
                background: #92400e;
                color: #fde68a;
                border-color: #f59e0b;
            }
            
            .table-container {
                overflow-x: auto;
                overflow-y: auto;
                max-height: 600px;
                border-radius: 8px;
                border: 1px solid #333;
                background: #2a2a2a;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                background: #2a2a2a;
            }
            
            th {
                background: #00E38C;
                color: white;
                padding: 12px 16px;
                text-align: left;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                position: sticky;
                top: 0;
                z-index: 10;
            }
            
            td {
                padding: 12px 16px;
                border-bottom: 1px solid #333;
                font-size: 0.9rem;
                color: #ffffff;
                background: #2a2a2a;
            }
            
            tr:nth-child(even) td {
                background: #1e1e1e;
            }
            
            tr:hover td {
                background: #333 !important;
            }
            
            .valor-cell {
                font-weight: 600;
                color: #00E38C;
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                background: #1e1e1e;
                border-top: 1px solid #333;
                margin-top: 2rem;
            }
            
            .footer p {
                margin: 5px 0;
                color: #94a3b8;
                font-size: 0.9rem;
            }
            </style>
            """
            
            # ===== LOG APENAS EM DEBUG =====
            if DEBUG:
                print("✅ [API-FORCA-ELENCO] HTML gerado com sucesso!")
            return css_styles + dashboard_html
        else:
            # ===== LOG APENAS EM DEBUG =====
            if DEBUG:
                print("❌ [API-FORCA-ELENCO] Nenhum arquivo CSV encontrado")
            return f"<div class='error-message'>Nenhum arquivo CSV encontrado</div>", 500
    
    except Exception as e:
        # ===== LOG APENAS EM DEBUG =====
        if DEBUG:
            print(f"❌ [API-FORCA-ELENCO] Erro: {str(e)}")
        return f"<div class='error-message'>Erro ao carregar dados: {str(e)}</div>", 500

@forca_elenco_bp.route('/dados')
def dados():
    """Retorna dados JSON dos elencos"""
    try:
        elencos_path = os.path.join(os.path.dirname(__file__), 'static', 'valor_elenco', 'elencos_mundiais.json')
        mapeamento_path = os.path.join(os.path.dirname(__file__), 'static', 'valor_elenco', 'mapeamento_clubes.json')
        
        with open(elencos_path, 'r', encoding='utf-8') as f:
            elencos_data = json.load(f)
        
        with open(mapeamento_path, 'r', encoding='utf-8') as f:
            mapeamento_data = json.load(f)
        
        return jsonify({
            'elencos': elencos_data,
            'mapeamento': mapeamento_data,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@forca_elenco_bp.route('/clube/<nome_clube>')
def clube_especifico(nome_clube):
    """Retorna dados de um clube específico"""
    try:
        # Implementar busca por clube específico
        return jsonify({'clube': nome_clube, 'dados': 'em desenvolvimento'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500