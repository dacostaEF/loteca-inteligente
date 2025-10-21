#!/usr/bin/env python3
"""
Sistema de Automação de Classificação
Lê CSVs da pasta estatistica/ e atualiza automaticamente as tabelas de classificação
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Tuple
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoClassificacao:
    """
    Sistema automático para gerar classificação das Séries A e B
    """
    
    def __init__(self, base_path: str = "estatistica"):
        self.base_path = base_path
        self.serie_a_path = os.path.join(base_path, "Serie_A")
        self.serie_b_path = os.path.join(base_path, "Serie_B")
        
        # Zonas de classificação baseadas na tabela do jornal esportivo
        self.zonas_serie_a = {
            "Libertadores": (1, 4),      # 1º ao 4º (azul)
            "Pré-Libertadores": (5, 6),   # 5º ao 6º (azul claro)
            "Sul-Americana": (7, 12),    # 7º ao 12º (verde)
            "Zona de Rebaixamento": (17, 20)  # 17º ao 20º (vermelho)
        }
        
        self.zonas_serie_b = {
            "Acesso": (1, 4),            # 1º ao 4º (azul)
            "Meio de tabela": (5, 16),   # 5º ao 16º (cinza)
            "Zona de Rebaixamento": (17, 20)  # 17º ao 20º (vermelho)
        }
        
        self.zonas_serie_c = {
            "Semi-final": (1, 2),        # 1º ao 2º (azul) - Classificados para semi-final
            "Eliminados": (3, 4)         # 3º ao 4º (cinza) - Eliminados
        }
    
    def converter_ultimos_jogos(self, ultimos_jogos: str) -> str:
        """
        Converte os últimos jogos de formato V-D-E para bolas coloridas
        V = 🟢 (vitória), D = 🔴 (derrota), E = 🟡 (empate)
        """
        if not ultimos_jogos:
            return ""
        
        # Converter cada resultado para bola colorida
        resultado = ultimos_jogos.replace('V', '🟢').replace('D', '🔴').replace('E', '🟡')
        
        # Garantir que temos exatamente 5 bolas (pegar apenas os últimos 5)
        bolas = resultado.split('-')
        if len(bolas) > 5:
            bolas = bolas[-5:]  # Pegar apenas os últimos 5
        
        return '-'.join(bolas)
    
    def determinar_variacao_posicao(self, posicao: int) -> str:
        """
        Determina a variação de posição baseada na tabela do jornal esportivo
        Por enquanto, simula variações baseadas na posição atual
        """
        # Simular variações baseadas na posição (em um sistema real, 
        # isso viria de dados históricos ou comparação com rodada anterior)
        if posicao <= 3:
            return 'subiu'  # Times no topo tendem a subir
        elif posicao <= 6:
            return 'manteve'  # Times na zona de classificação tendem a manter
        elif posicao <= 12:
            return 'desceu'  # Times no meio tendem a descer
        elif posicao <= 16:
            return 'manteve'  # Times no meio de tabela tendem a manter
        else:
            return 'desceu'  # Times na zona de rebaixamento tendem a descer
    
    def ler_csv_clube(self, caminho_csv: str) -> Dict:
        """
        Lê CSV de um clube e calcula estatísticas
        """
        try:
            with open(caminho_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                jogos = list(reader)
            
            if not jogos:
                return None
            
            # Pegar dados do último jogo (mais atualizado)
            ultimo_jogo = jogos[0]
            
            # Calcular estatísticas
            pontos = int(ultimo_jogo['Pontos_Acumulados'])
            jogos_disputados = len(jogos)
            
            # Contar vitórias, empates, derrotas
            vitorias = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Vitoria')
            empates = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Empate')
            derrotas = sum(1 for jogo in jogos if jogo['Resultado_Sao'] == 'Derrota')
            
            # Calcular gols pró e contra
            gols_pro = 0
            gols_contra = 0
            
            for jogo in jogos:
                # Determinar se o clube jogou em casa ou fora
                time_casa = jogo['Time_Casa']
                time_visitante = jogo['Time_Visitante']
                
                # Extrair nome do clube do caminho (última pasta)
                nome_clube = os.path.basename(os.path.dirname(caminho_csv))
                
                # Mapear nomes dos CSVs para nomes dos clubes
                nome_clube_mapeado = self.mapear_nome_clube(nome_clube)
                
                if time_casa == nome_clube_mapeado:
                    # Jogou em casa
                    gols_pro += int(jogo['Gols_Casa'])
                    gols_contra += int(jogo['Gols_Visitante'])
                elif time_visitante == nome_clube_mapeado:
                    # Jogou fora
                    gols_pro += int(jogo['Gols_Visitante'])
                    gols_contra += int(jogo['Gols_Casa'])
            
            saldo_gols = gols_pro - gols_contra
            aproveitamento = (pontos / (jogos_disputados * 3)) * 100 if jogos_disputados > 0 else 0
            
            return {
                'time': self.mapear_nome_clube(os.path.basename(os.path.dirname(caminho_csv))),
                'pontos': pontos,
                'jogos': jogos_disputados,
                'vitorias': vitorias,
                'empates': empates,
                'derrotas': derrotas,
                'gols_pro': gols_pro,
                'gols_contra': gols_contra,
                'saldo_gols': saldo_gols,
                'aproveitamento': round(aproveitamento, 1),
                'ultima_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'fonte': 'csv_automatico'
            }
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV {caminho_csv}: {e}")
            return None
    
    def mapear_nome_clube(self, nome_pasta: str) -> str:
        """
        Mapeia nomes das pastas para nomes dos clubes
        """
        mapeamento = {
            'flamengo': 'Flamengo',
            'palmeiras': 'Palmeiras',
            'corinthians': 'Corinthians',
            'sao-paulo': 'São Paulo',
            'botafogo': 'Botafogo',
            'fluminense': 'Fluminense',
            'cruzeiro': 'Cruzeiro',
            'atletico-mg': 'Atlético-MG',
            'bahia': 'Bahia',
            'ceara': 'Ceará',
            'fortaleza': 'Fortaleza',
            'gremio': 'Grêmio',
            'internacional': 'Internacional',
            'juventude': 'Juventude',
            'mirassol': 'Mirassol',
            'red-bull-bragantino': 'Red Bull Bragantino',
            'santos': 'Santos',
            'sport-recife': 'Sport',
            'vasco': 'Vasco',
            'vitoria': 'Vitória',
            'america-mg': 'América-MG',
            'athletico-pr': 'Athletico-PR',
            'atletico-go': 'Atlético-GO',
            'avai': 'Avaí',
            'botafogo-sp': 'Botafogo-SP',
            'chapecoense': 'Chapecoense',
            'coritiba': 'Coritiba',
            'crb': 'CRB',
            'criciuma': 'Criciúma',
            'cuiaba': 'Cuiabá',
            'ferroviaria': 'Ferroviária',
            'goias': 'Goiás',
            'novohorizontino': 'Novorizontino',
            'operario-pr': 'Operário-PR',
            'paysandu': 'Paysandu',
            'remo': 'Remo',
            'vila-nova': 'Vila Nova',
            'volta-redonda': 'Volta Redonda'
        }
        
        return mapeamento.get(nome_pasta.lower(), nome_pasta.title())
    
    def processar_serie(self, serie_path: str, serie_nome: str) -> List[Dict]:
        """
        Processa todos os clubes de uma série
        """
        logger.info(f"Processando {serie_nome}...")
        
        clubes = []
        
        if not os.path.exists(serie_path):
            logger.error(f"Pasta {serie_path} não encontrada!")
            return clubes
        
        # Listar todas as pastas de clubes
        for pasta_clube in os.listdir(serie_path):
            pasta_completa = os.path.join(serie_path, pasta_clube)
            
            if os.path.isdir(pasta_completa):
                csv_path = os.path.join(pasta_completa, "jogos.csv")
                
                if os.path.exists(csv_path):
                    logger.info(f"Processando {pasta_clube}...")
                    dados_clube = self.ler_csv_clube(csv_path)
                    
                    if dados_clube:
                        clubes.append(dados_clube)
                    else:
                        logger.warning(f"Falha ao processar {pasta_clube}")
                else:
                    logger.warning(f"CSV não encontrado para {pasta_clube}")
        
        # Ordenar por classificação (pontos, saldo, gols pró)
        clubes_ordenados = sorted(clubes, key=lambda x: (
            -x['pontos'],      # Mais pontos primeiro
            -x['saldo_gols'],  # Melhor saldo
            -x['gols_pro']     # Mais gols pró
        ))
        
        # Adicionar posição e zona
        for i, clube in enumerate(clubes_ordenados, 1):
            clube['posicao'] = i
            clube['zona'] = self.determinar_zona(i, serie_nome)
        
        logger.info(f"{serie_nome}: {len(clubes_ordenados)} clubes processados")
        return clubes_ordenados
    
    def determinar_zona(self, posicao: int, serie: str) -> str:
        """
        Determina a zona de classificação baseada na posição
        """
        if serie == "Série A":
            if 1 <= posicao <= 6:
                return "Libertadores"
            elif 7 <= posicao <= 12:
                return "Sul-Americana"
            elif 17 <= posicao <= 20:
                return "Zona de Rebaixamento"
            else:
                return "Meio de tabela"
        
        elif serie == "Série B":
            if 1 <= posicao <= 4:
                return "Acesso"
            elif 17 <= posicao <= 20:
                return "Zona de Rebaixamento"
            else:
                return "Meio de tabela"
        
        return "Meio de tabela"
    
    def processar_todas_series(self) -> Dict:
        """
        Processa Série A e B automaticamente
        """
        logger.info("🚀 Iniciando processamento automático das séries...")
        
        resultado = {
            'serie_a': [],
            'serie_b': [],
            'timestamp': datetime.now().isoformat(),
            'total_clubes': 0
        }
        
        # Processar Série A
        serie_a = self.processar_serie(self.serie_a_path, "Série A")
        resultado['serie_a'] = serie_a
        
        # Processar Série B
        serie_b = self.processar_serie(self.serie_b_path, "Série B")
        resultado['serie_b'] = serie_b
        
        resultado['total_clubes'] = len(serie_a) + len(serie_b)
        
        logger.info(f"✅ Processamento concluído: {len(serie_a)} Série A + {len(serie_b)} Série B")
        
        return resultado

    def ler_tabela_tradicional_serie_a(self) -> List[Dict]:
        """
        Lê diretamente do arquivo Serie_A_tabela_tradicional.csv
        """
        try:
            csv_path = os.path.join(self.base_path, "Serie_A_tabela_tradicional.csv")
            # Debug: mostrar caminho
            logger.info(f"🔍 Procurando arquivo em: {csv_path}")
            logger.info(f"🔍 Arquivo existe: {os.path.exists(csv_path)}")
            
            if not os.path.exists(csv_path):
                logger.error(f"❌ Arquivo não encontrado: {csv_path}")
                return []
            
            clubes = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Mapear campos do CSV para formato interno
                    clube = {
                        'time': row['Time'].strip('"'),
                        'pontos': int(row['Pontos']),
                        'jogos': int(row['Jogos']),
                        'vitorias': int(row['Vitórias']),
                        'empates': int(row['Empates']),
                        'derrotas': int(row['Derrotas']),
                        'gols_pro': int(row['Gols Pró']),
                        'gols_contra': int(row['Gols Contra']),
                        'saldo_gols': int(row['Saldo Gols']),
                        'aproveitamento': float(row['Aproveitamento %']),
                        'ultimos_jogos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'ultimos_confrontos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'posicao': int(row['Posição']),
                        'variacao': self.determinar_variacao_posicao(int(row['Posição']))
                    }
                    
                    # Determinar zona baseada na tabela do jornal esportivo
                    posicao = clube['posicao']
                    if 1 <= posicao <= 4:
                        clube['zona'] = 'Libertadores'
                    elif 5 <= posicao <= 6:
                        clube['zona'] = 'Pré-Libertadores'
                    elif 7 <= posicao <= 12:
                        clube['zona'] = 'Sul-Americana'
                    elif 17 <= posicao <= 20:
                        clube['zona'] = 'Zona de Rebaixamento'
                    else:
                        clube['zona'] = 'Meio de tabela'
                    
                    clubes.append(clube)
            
            logger.info(f"✅ Série A lida do CSV tradicional: {len(clubes)} clubes")
            return clubes
            
        except Exception as e:
            logger.error(f"❌ Erro ao ler tabela tradicional: {e}")
            return []
    
    def ler_tabela_tradicional_serie_b(self) -> List[Dict]:
        """
        Lê diretamente do arquivo Serir_B_tabela_tradicional.csv
        """
        try:
            csv_path = os.path.join(self.base_path, "Serir_B_tabela_tradicional.csv")
            logger.info(f"🔍 Procurando arquivo Série B em: {csv_path}")
            logger.info(f"🔍 Arquivo existe: {os.path.exists(csv_path)}")
            
            if not os.path.exists(csv_path):
                logger.error(f"❌ Arquivo não encontrado: {csv_path}")
                return []
            
            clubes = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    clube = {
                        'time': row['Time'].strip('"'),
                        'pontos': int(row['Pontos']),
                        'jogos': int(row['Jogos']),
                        'vitorias': int(row['Vitórias']),
                        'empates': int(row['Empates']),
                        'derrotas': int(row['Derrotas']),
                        'gols_pro': int(row['Gols Pró']),
                        'gols_contra': int(row['Gols Contra']),
                        'saldo_gols': int(row['Saldo Gols']),
                        'aproveitamento': float(row['Aproveitamento %']),
                        'ultimos_jogos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'ultimos_confrontos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'posicao': int(row['Posição']),
                        'variacao': self.determinar_variacao_posicao(int(row['Posição']))
                    }
                    
                    # Determinar zona baseada na posição da Série B
                    posicao = clube['posicao']
                    if 1 <= posicao <= 4:
                        clube['zona'] = 'Acesso'
                    elif 17 <= posicao <= 20:
                        clube['zona'] = 'Zona de Rebaixamento'
                    else:
                        clube['zona'] = 'Meio de tabela'
                    
                    clubes.append(clube)
            
            logger.info(f"✅ Série B lida do CSV tradicional: {len(clubes)} clubes")
            return clubes
            
        except Exception as e:
            logger.error(f"❌ Erro ao ler tabela tradicional Série B: {e}")
            return []
    
    def ler_tabela_tradicional_serie_c(self) -> List[Dict]:
        """
        Lê diretamente do arquivo Serie_C_tabela_tradicional.csv
        """
        try:
            csv_path = os.path.join(self.base_path, "Serie_C_tabela_tradicional.csv")
            logger.info(f"🔍 Procurando arquivo Série C em: {csv_path}")
            logger.info(f"🔍 Arquivo existe: {os.path.exists(csv_path)}")
            
            if not os.path.exists(csv_path):
                logger.error(f"❌ Arquivo não encontrado: {csv_path}")
                return []
            
            clubes = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    clube = {
                        'time': row['Time'].strip('"'),
                        'grupo': row['Grupo'].strip('"'),
                        'pontos': int(row['Pontos']),
                        'jogos': int(row['Jogos']),
                        'vitorias': int(row['Vitórias']),
                        'empates': int(row['Empates']),
                        'derrotas': int(row['Derrotas']),
                        'gols_pro': int(row['Gols Pró']),
                        'gols_contra': int(row['Gols Contra']),
                        'saldo_gols': int(row['Saldo Gols']),
                        'aproveitamento': float(row['Aproveitamento %']),
                        'ultimos_jogos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'ultimos_confrontos': self.converter_ultimos_jogos(row['Últimos 5 Jogos'].strip('"')),
                        'posicao': int(row['Posição']),
                        'variacao': self.determinar_variacao_posicao(int(row['Posição']))
                    }
                    
                    # Determinar zona baseada na posição da Série C
                    posicao = clube['posicao']
                    if 1 <= posicao <= 2:
                        clube['zona'] = 'Semi-final'
                    else:
                        clube['zona'] = 'Eliminados'
                    
                    clubes.append(clube)
            
            logger.info(f"✅ Série C lida do CSV tradicional: {len(clubes)} clubes")
            return clubes
            
        except Exception as e:
            logger.error(f"❌ Erro ao ler tabela tradicional Série C: {e}")
            return []

    def processar_serie_a_tradicional(self) -> List[Dict]:
        """
        Processa Série A usando o arquivo de tabela tradicional
        """
        try:
            logger.info("📊 Processando Série A via tabela tradicional...")
            
            # Ler dados do CSV tradicional
            clubes = self.ler_tabela_tradicional_serie_a()
            
            if not clubes:
                logger.error("❌ Nenhum clube encontrado na tabela tradicional")
                return []
            
            # Ordenar por posição (já vem ordenado do CSV)
            clubes_ordenados = sorted(clubes, key=lambda x: x['posicao'])
            
            logger.info(f"✅ Série A processada: {len(clubes_ordenados)} clubes")
            return clubes_ordenados
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Série A tradicional: {e}")
            return []
    
    def processar_serie_b_tradicional(self) -> List[Dict]:
        """
        Processa Série B usando o arquivo de tabela tradicional
        """
        try:
            logger.info("📊 Processando Série B via tabela tradicional...")
            
            clubes = self.ler_tabela_tradicional_serie_b()
            
            if not clubes:
                logger.error("❌ Nenhum clube encontrado na tabela tradicional Série B")
                return []
            
            clubes_ordenados = sorted(clubes, key=lambda x: x['posicao'])
            
            logger.info(f"✅ Série B processada: {len(clubes_ordenados)} clubes")
            return clubes_ordenados
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Série B tradicional: {e}")
            return []
    
    def processar_serie_c_tradicional(self) -> List[Dict]:
        """
        Processa Série C usando o arquivo de tabela tradicional
        """
        try:
            logger.info("📊 Processando Série C via tabela tradicional...")
            
            clubes = self.ler_tabela_tradicional_serie_c()
            
            if not clubes:
                logger.error("❌ Nenhum clube encontrado na tabela tradicional Série C")
                return []
            
            # Ordenar por grupo e depois por posição
            clubes_ordenados = sorted(clubes, key=lambda x: (x['grupo'], x['posicao']))
            
            logger.info(f"✅ Série C processada: {len(clubes_ordenados)} clubes")
            return clubes_ordenados
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Série C tradicional: {e}")
            return []

# Função principal para uso externo
def gerar_classificacao_automatica():
    """
    Função principal para gerar classificação automaticamente
    """
    auto_class = AutoClassificacao()
    return auto_class.processar_todas_series()

if __name__ == "__main__":
    # Teste do sistema
    resultado = gerar_classificacao_automatica()
    
    print("\n🏆 SÉRIE A - TOP 5:")
    for clube in resultado['serie_a'][:5]:
        print(f"{clube['posicao']}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")
    
    print("\n🥈 SÉRIE B - TOP 5:")
    for clube in resultado['serie_b'][:5]:
        print(f"{clube['posicao']}º {clube['time']} - {clube['pontos']}pts ({clube['zona']})")

