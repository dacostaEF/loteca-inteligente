"""
SISTEMA ROBUSTO DE PARSING DE CSV PARA CONFRONTOS
=================================================

Este módulo implementa um sistema automatizado e robusto para ler arquivos CSV
de confrontos de futebol, independentemente do formato ou estrutura.

Características:
- Detecção automática de formato
- Suporte a múltiplos encodings
- Suporte a múltiplos separadores
- Validação de dados
- Sistema de fallback
- Logging detalhado
"""

import os
import logging
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class CSVParserRobusto:
    """Parser robusto para arquivos CSV de confrontos"""
    
    def __init__(self):
        self.encodings_suportados = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        self.separadores_suportados = [',', ';', '\t', '|']
        self.formatos_reconhecidos = []
        self._inicializar_formatos()
    
    def _inicializar_formatos(self):
        """Inicializar formatos reconhecidos"""
        self.formatos_reconhecidos = [
            {
                'nome': 'Formato Padrão com Resultado',
                'colunas': ['data', 'mandante', 'placar', 'visitante', 'vencedor', 'campeonato', 'resultado'],
                'indices': {'data': 0, 'mandante': 1, 'placar': 2, 'visitante': 3, 'vencedor': 4, 'campeonato': 5, 'resultado': 6},
                'identificador': lambda header: 'resultado' in header.lower() and 'mandante' in header.lower() and len(header.split(',')) == 7
            },
            {
                'nome': 'Formato Antigo - Corinthians',
                'colunas': ['data', 'mandante', 'placar', 'visitante', 'vencedor', 'rodada', 'competicao'],
                'indices': {'data': 0, 'mandante': 1, 'placar': 2, 'visitante': 3, 'vencedor': 4, 'rodada': 5, 'competicao': 6},
                'identificador': lambda header: 'vencedor' in header.lower() and len(header.split(',')) == 7
            },
            {
                'nome': 'Formato Novo - Flamengo vs Palmeiras',
                'colunas': ['data', 'time_casa', 'placar', 'time_visitante', 'vencedor', 'campeonato', 'resultado_time'],
                'indices': {'data': 0, 'mandante': 1, 'placar': 2, 'visitante': 3, 'vencedor': 4, 'campeonato': 5, 'resultado': 6},
                'identificador': lambda header: 'time da casa' in header.lower() and len(header.split(',')) == 7
            },
            {
                'nome': 'Formato Detalhado - Corinthians vs Flamengo',
                'colunas': ['data', 'mandante', 'mandante_nome', 'placar', 'visitante', 'visitante_nome', 'resultado_time', 'rodada', 'competicao'],
                'indices': {'data': 0, 'mandante': 1, 'mandante_nome': 2, 'placar': 3, 'visitante': 4, 'visitante_nome': 5, 'resultado': 6, 'rodada': 7, 'competicao': 8},
                'identificador': lambda header: 'resultado_' in header.lower() and len(header.split(',')) >= 8
            },
            {
                'nome': 'Formato Genérico',
                'colunas': ['data', 'mandante', 'placar', 'visitante', 'vencedor'],
                'indices': {'data': 0, 'mandante': 1, 'placar': 2, 'visitante': 3, 'vencedor': 4},
                'identificador': lambda header: True  # Fallback
            }
        ]
    
    def detectar_formato(self, header: str, num_colunas: int) -> Dict:
        """Detectar automaticamente o formato do CSV"""
        logger.info(f"🔍 [PARSER] Detectando formato - Header: '{header}', Colunas: {num_colunas}")
        
        for formato in self.formatos_reconhecidos:
            try:
                if formato['identificador'](header):
                    logger.info(f"✅ [PARSER] Formato detectado: {formato['nome']}")
                    return formato
            except Exception as e:
                logger.warning(f"⚠️ [PARSER] Erro ao testar formato {formato['nome']}: {e}")
                continue
        
        # Fallback para formato genérico
        logger.info("🔄 [PARSER] Usando formato genérico como fallback")
        return self.formatos_reconhecidos[-1]
    
    def detectar_separador(self, linha: str) -> str:
        """Detectar o separador usado no CSV"""
        for separador in self.separadores_suportados:
            if separador in linha:
                # Verificar se é o separador mais comum
                count = linha.count(separador)
                if count >= 4:  # Pelo menos 5 colunas
                    logger.info(f"✅ [PARSER] Separador detectado: '{separador}' (aparece {count} vezes)")
                    return separador
        
        # Fallback para vírgula
        logger.warning("⚠️ [PARSER] Separador não detectado, usando vírgula como fallback")
        return ','
    
    def normalizar_data(self, data_str: str) -> str:
        """Normalizar formato de data"""
        if not data_str or data_str.strip() == '':
            return ''
        
        data_str = data_str.strip()
        
        # Padrões de data reconhecidos
        padroes_data = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
            r'(\d{1,2})/(\d{1,2})/(\d{2})',   # DD/MM/YY
            r'(\d{4})-(\d{1,2})-(\d{1,2})',   # YYYY-MM-DD
            r'(\d{1,2})-(\d{1,2})-(\d{4})',   # DD-MM-YYYY
        ]
        
        for idx, padrao in enumerate(padroes_data):
            match = re.match(padrao, data_str)
            if match:
                grupos = match.groups()
                if len(grupos) == 3:
                    # CORRIGIDO: Verificar formato específico
                    if idx == 2:  # YYYY-MM-DD (índice 2)
                        ano, mes, dia = grupos
                    elif idx == 3:  # DD-MM-YYYY (índice 3)
                        dia, mes, ano = grupos
                    else:  # DD/MM/YYYY ou DD/MM/YY (índices 0 e 1)
                        dia, mes, ano = grupos
                    
                    # Normalizar ano de 2 dígitos
                    if len(ano) == 2:
                        ano = f"20{ano}" if int(ano) < 50 else f"19{ano}"
                    
                    # Retornar no formato DD/MM/YYYY
                    return f"{dia.zfill(2)}/{mes.zfill(2)}/{ano}"
        
        # Se não conseguiu normalizar, retornar como está
        logger.warning(f"⚠️ [PARSER] Data não normalizada: '{data_str}'")
        return data_str
    
    def determinar_resultado(self, vencedor: str, mandante: str, visitante: str, resultado_direto: str = '') -> str:
        """Determinar resultado V/E/D baseado no vencedor ou resultado direto"""
        
        # Se já tem resultado direto (V/E/D), usar ele
        if resultado_direto and resultado_direto.upper() in ['V', 'E', 'D']:
            return resultado_direto.upper()
        
        # Se não tem vencedor, assumir empate
        if not vencedor or vencedor.strip() == '':
            return 'E'
        
        vencedor_lower = vencedor.lower().strip()
        mandante_lower = mandante.lower().strip()
        visitante_lower = visitante.lower().strip()
        
        # Verificar se é empate
        if any(palavra in vencedor_lower for palavra in ['empate', 'draw', 'tie']):
            return 'E'
        
        # Verificar se o vencedor é o mandante
        palavras_mandante = [palavra for palavra in mandante_lower.split() if len(palavra) > 2]
        if any(palavra in vencedor_lower for palavra in palavras_mandante):
            return 'V'  # Vitória do mandante
        
        # Verificar se o vencedor é o visitante
        palavras_visitante = [palavra for palavra in visitante_lower.split() if len(palavra) > 2]
        if any(palavra in vencedor_lower for palavra in palavras_visitante):
            return 'D'  # Vitória do visitante
        
        # Se não conseguiu determinar, assumir empate
        logger.warning(f"⚠️ [PARSER] Não foi possível determinar resultado para vencedor: '{vencedor}'")
        return 'E'
    
    def validar_confronto(self, confronto: Dict) -> bool:
        """Validar se um confronto tem dados mínimos necessários"""
        campos_obrigatorios = ['data', 'mandante_nome', 'visitante_nome', 'placar']
        
        for campo in campos_obrigatorios:
            if not confronto.get(campo) or confronto[campo].strip() == '':
                logger.warning(f"⚠️ [PARSER] Confronto inválido - campo '{campo}' vazio")
                return False
        
        return True
    
    def processar_linha(self, linha: str, formato: Dict, separador: str, linha_num: int) -> Optional[Dict]:
        """Processar uma linha do CSV"""
        try:
            partes = [parte.strip() for parte in linha.split(separador)]
            
            if len(partes) < 5:
                logger.warning(f"⚠️ [PARSER] Linha {linha_num} ignorada - menos de 5 colunas")
                return None
            
            confronto = {}
            indices = formato['indices']
            
            # Mapear campos baseado no formato detectado
            confronto['data'] = self.normalizar_data(partes[indices.get('data', 0)])
            confronto['mandante_nome'] = partes[indices.get('mandante', 1)]
            confronto['placar'] = partes[indices.get('placar', 2)]
            confronto['visitante_nome'] = partes[indices.get('visitante', 3)]
            
            # Campos opcionais
            confronto['vencedor'] = partes[indices.get('vencedor', 4)] if indices.get('vencedor') is not None and indices.get('vencedor') < len(partes) else ''
            resultado_direto = partes[indices.get('resultado', 6)] if indices.get('resultado') is not None and indices.get('resultado') < len(partes) else ''
            confronto['rodada'] = partes[indices.get('rodada', 5)] if indices.get('rodada') is not None and indices.get('rodada') < len(partes) else ''
            confronto['campeonato'] = partes[indices.get('campeonato', 6)] if indices.get('campeonato') is not None and indices.get('campeonato') < len(partes) else ''
            if not confronto['campeonato']:
                confronto['campeonato'] = partes[indices.get('competicao', 6)] if indices.get('competicao') is not None and indices.get('competicao') < len(partes) else ''
            
            # Determinar resultado V/E/D - PRIORIZAR resultado direto do CSV
            if resultado_direto and resultado_direto.upper() in ['V', 'E', 'D']:
                confronto['resultado'] = resultado_direto.upper()
                logger.info(f"✅ [PARSER] Usando resultado direto do CSV: {resultado_direto.upper()}")
            else:
                confronto['resultado'] = self.determinar_resultado(
                    confronto.get('vencedor', ''),
                    confronto.get('mandante_nome', ''),
                    confronto.get('visitante_nome', ''),
                    ''
                )
                logger.info(f"🔄 [PARSER] Resultado calculado: {confronto['resultado']}")
            
            # Validar confronto
            if not self.validar_confronto(confronto):
                return None
            
            logger.info(f"✅ [PARSER] Linha {linha_num} processada: {confronto['mandante_nome']} vs {confronto['visitante_nome']} = {confronto['resultado']}")
            return confronto
            
        except Exception as e:
            logger.error(f"❌ [PARSER] Erro ao processar linha {linha_num}: {e}")
            return None
    
    def processar_arquivo(self, caminho_arquivo: str) -> Tuple[bool, List[Dict], str]:
        """Processar arquivo CSV completo"""
        logger.info(f"🚀 [PARSER] Iniciando processamento do arquivo: {caminho_arquivo}")
        
        if not os.path.exists(caminho_arquivo):
            return False, [], f"Arquivo não encontrado: {caminho_arquivo}"
        
        confrontos = []
        formato_detectado = None
        separador_detectado = None
        
        # Tentar diferentes encodings
        for encoding in self.encodings_suportados:
            try:
                logger.info(f"🔄 [PARSER] Tentando encoding: {encoding}")
                
                with open(caminho_arquivo, 'r', encoding=encoding) as f:
                    linhas = f.readlines()
                
                if not linhas:
                    logger.warning(f"⚠️ [PARSER] Arquivo vazio com encoding {encoding}")
                    continue
                
                logger.info(f"✅ [PARSER] Arquivo lido com sucesso usando {encoding} - {len(linhas)} linhas")
                
                # Detectar separador na primeira linha
                separador_detectado = self.detectar_separador(linhas[0])
                
                # Detectar formato baseado no cabeçalho
                header = linhas[0].strip()
                num_colunas = len(header.split(separador_detectado))
                formato_detectado = self.detectar_formato(header, num_colunas)
                
                # Processar linhas (pular cabeçalho se necessário)
                inicio = 1 if 'data' in header.lower() else 0
                
                for i, linha in enumerate(linhas[inicio:], start=inicio + 1):
                    linha = linha.strip()
                    if linha:
                        confronto = self.processar_linha(linha, formato_detectado, separador_detectado, i)
                        if confronto:
                            confrontos.append(confronto)
                
                logger.info(f"✅ [PARSER] Processamento concluído com {encoding}")
                logger.info(f"📊 [PARSER] {len(confrontos)} confrontos válidos processados")
                logger.info(f"🎯 [PARSER] Formato usado: {formato_detectado['nome']}")
                logger.info(f"🔧 [PARSER] Separador usado: '{separador_detectado}'")
                
                return True, confrontos, f"Arquivo processado com sucesso usando {encoding}"
                
            except UnicodeDecodeError as e:
                logger.warning(f"⚠️ [PARSER] Encoding {encoding} falhou: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"❌ [PARSER] Erro ao processar arquivo com {encoding}: {str(e)}")
                continue
        
        return False, [], "Nenhum encoding funcionou para o arquivo"

def processar_csv_confrontos(caminho_arquivo: str) -> Tuple[bool, List[Dict], str]:
    """
    Função principal para processar arquivo CSV de confrontos
    
    Args:
        caminho_arquivo: Caminho para o arquivo CSV
        
    Returns:
        Tuple[bool, List[Dict], str]: (sucesso, confrontos, mensagem)
    """
    parser = CSVParserRobusto()
    return parser.processar_arquivo(caminho_arquivo)

# Exemplo de uso
if __name__ == "__main__":
    # Teste com arquivo de exemplo
    caminho_teste = "models/Confrontos/Flamengo_vs_Palmeiras.csv"
    sucesso, confrontos, mensagem = processar_csv_confrontos(caminho_teste)
    
    print(f"Sucesso: {sucesso}")
    print(f"Mensagem: {mensagem}")
    print(f"Confrontos processados: {len(confrontos)}")
    
    if confrontos:
        print("\nPrimeiros 3 confrontos:")
        for i, confronto in enumerate(confrontos[:3]):
            print(f"{i+1}. {confronto['mandante_nome']} vs {confronto['visitante_nome']} - {confronto['resultado']}")
