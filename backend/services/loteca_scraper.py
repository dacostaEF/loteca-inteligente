#!/usr/bin/env python3
"""
LOTECA X-RAY - SCRAPER AUTOMÁTICO CEF
Sistema de captura automática de jogos da Loteca via scraping
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class LotecaScraper:
    """Scraper para capturar jogos da Loteca do site da CEF"""
    
    def __init__(self):
        self.base_url = "https://loterias.caixa.gov.br"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def get_current_concurso_number(self) -> Optional[int]:
        """Obtém o número do concurso atual"""
        try:
            url = f"{self.base_url}/wps/portal/loterias/landing/loteca"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por padrões que indiquem o número do concurso
            concurso_patterns = [
                r'concurso[:\s]*(\d+)',
                r'(\d{4})',
                r'loteca[:\s]*(\d+)'
            ]
            
            text = soup.get_text().lower()
            for pattern in concurso_patterns:
                match = re.search(pattern, text)
                if match:
                    return int(match.group(1))
            
            # Fallback: tentar extrair de elementos específicos
            concurso_elements = soup.find_all(['span', 'div', 'p'], string=re.compile(r'\d{4}'))
            for element in concurso_elements:
                text = element.get_text().strip()
                if re.match(r'^\d{4}$', text):
                    return int(text)
            
            logger.warning("Não foi possível determinar o número do concurso atual")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter número do concurso: {e}")
            return None
    
    def get_concurso_data(self, concurso_num: int) -> Optional[Dict]:
        """Obtém dados completos de um concurso específico"""
        try:
            # Tentar diferentes URLs possíveis
            urls_to_try = [
                f"{self.base_url}/wps/portal/loterias/landing/loteca/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN-FaqLqB2aIKuKkFhTqABujozURV3EaYjNnPw!!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QPVN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/?timestampAjax=1234567890&concurso={concurso_num}",
                f"{self.base_url}/wps/portal/loterias/landing/loteca/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN-FaqLqB2aIKuKkFhTqABujozURV3EaYjNnPw!!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QPVN93KQ10G1/res/id=buscaResultado/c=cacheLevelPage/=/?timestampAjax=1234567890&concurso={concurso_num}",
                f"{self.base_url}/wps/portal/loterias/landing/loteca/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN-FaqLqB2aIKuKkFhTqABujozURV3EaYjNnPw!!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QPVN93KQ10G1/res/id=buscaResultado/c=cacheLevelPage/=/?timestampAjax=1234567890&concurso={concurso_num}&modalidade=loteca"
            ]
            
            for url in urls_to_try:
                try:
                    logger.info(f"Tentando URL: {url}")
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    # Verificar se a resposta contém dados válidos
                    if self._is_valid_response(response):
                        return self._parse_concurso_data(response, concurso_num)
                    
                except Exception as e:
                    logger.warning(f"Falha na URL {url}: {e}")
                    continue
            
            logger.error(f"Não foi possível obter dados do concurso {concurso_num}")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter dados do concurso {concurso_num}: {e}")
            return None
    
    def _is_valid_response(self, response: requests.Response) -> bool:
        """Verifica se a resposta contém dados válidos"""
        try:
            content = response.text.lower()
            # Verificar se contém indicadores de dados da Loteca
            indicators = ['loteca', 'jogo', 'casa', 'fora', 'coluna 1', 'coluna 2']
            return any(indicator in content for indicator in indicators)
        except:
            return False
    
    def _parse_concurso_data(self, response: requests.Response, concurso_num: int) -> Dict:
        """Extrai dados estruturados da resposta HTML"""
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Estrutura básica do concurso
            concurso_data = {
                "metadados": {
                    "numero": str(concurso_num),
                    "salvo_em": datetime.now().isoformat(),
                    "versao": "2.0",
                    "fonte": "scraper_cef"
                },
                "concurso": {},
                "jogos": [],
                "estatisticas": {}
            }
            
            # Tentar extrair jogos de diferentes formatos
            jogos = self._extract_jogos_from_html(soup)
            if jogos:
                concurso_data["jogos"] = jogos
                logger.info(f"Extraídos {len(jogos)} jogos do concurso {concurso_num}")
            else:
                logger.warning(f"Nenhum jogo encontrado no concurso {concurso_num}")
            
            return concurso_data
            
        except Exception as e:
            logger.error(f"Erro ao processar dados do concurso {concurso_num}: {e}")
            return {}
    
    def _extract_jogos_from_html(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrai lista de jogos do HTML"""
        jogos = []
        
        try:
            # Método 1: Procurar por tabelas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Pular cabeçalho
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:
                        jogo = self._parse_jogo_row(cells)
                        if jogo:
                            jogos.append(jogo)
            
            # Método 2: Procurar por divs com padrões específicos
            if not jogos:
                divs = soup.find_all('div', class_=re.compile(r'jogo|game|match'))
                for div in divs:
                    jogo = self._parse_jogo_div(div)
                    if jogo:
                        jogos.append(jogo)
            
            # Método 3: Procurar por texto estruturado
            if not jogos:
                text_content = soup.get_text()
                jogos = self._extract_jogos_from_text(text_content)
            
            return jogos
            
        except Exception as e:
            logger.error(f"Erro ao extrair jogos do HTML: {e}")
            return []
    
    def _parse_jogo_row(self, cells) -> Optional[Dict]:
        """Processa uma linha de tabela como um jogo"""
        try:
            if len(cells) < 3:
                return None
            
            # Tentar diferentes formatos de células
            numero = self._extract_number(cells[0].get_text())
            time_casa = cells[1].get_text().strip()
            time_fora = cells[2].get_text().strip()
            data = cells[3].get_text().strip() if len(cells) > 3 else "Não informado"
            
            if numero and time_casa and time_fora:
                return {
                    "numero": numero,
                    "time_casa": time_casa,
                    "time_fora": time_fora,
                    "data": data
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao processar linha de jogo: {e}")
            return None
    
    def _parse_jogo_div(self, div) -> Optional[Dict]:
        """Processa uma div como um jogo"""
        try:
            text = div.get_text().strip()
            # Implementar lógica específica baseada no formato encontrado
            return None  # Placeholder
        except:
            return None
    
    def _extract_jogos_from_text(self, text: str) -> List[Dict]:
        """Extrai jogos de texto não estruturado"""
        jogos = []
        try:
            # Implementar regex para extrair jogos do texto
            # Este é um fallback para casos onde o HTML não está estruturado
            pass
        except:
            pass
        return jogos
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Extrai número de um texto"""
        try:
            numbers = re.findall(r'\d+', text)
            return int(numbers[0]) if numbers else None
        except:
            return None
    
    def get_latest_concurso(self) -> Optional[Dict]:
        """Obtém o concurso mais recente disponível"""
        try:
            # Primeiro, tentar obter o número do concurso atual
            current_num = self.get_current_concurso_number()
            if not current_num:
                # Fallback: tentar números recentes
                current_num = 1216  # Último conhecido
            
            # Tentar obter dados do concurso atual
            data = self.get_concurso_data(current_num)
            if data:
                return data
            
            # Se falhar, tentar concursos anteriores
            for i in range(1, 6):  # Tentar até 5 concursos anteriores
                try_num = current_num - i
                data = self.get_concurso_data(try_num)
                if data:
                    logger.info(f"Usando concurso {try_num} (concurso atual {current_num} não disponível)")
                    return data
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter último concurso: {e}")
            return None

def test_scraper():
    """Função de teste para o scraper"""
    scraper = LotecaScraper()
    
    print("🧪 Testando Loteca Scraper...")
    
    # Teste 1: Obter número do concurso atual
    print("\n1. Obtendo número do concurso atual...")
    current_num = scraper.get_current_concurso_number()
    print(f"   Concurso atual: {current_num}")
    
    # Teste 2: Obter dados do último concurso
    print("\n2. Obtendo dados do último concurso...")
    data = scraper.get_latest_concurso()
    if data:
        print(f"   ✅ Sucesso! {len(data.get('jogos', []))} jogos encontrados")
        print(f"   Concurso: {data['metadados']['numero']}")
    else:
        print("   ❌ Falha ao obter dados")
    
    return data

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Executar teste
    test_scraper()

