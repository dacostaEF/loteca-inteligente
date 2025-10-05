#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Automático de Atualização dos Últimos 5 Confrontos
Atualiza automaticamente as tabelas de classificação com os últimos jogos de cada time
"""

import os
import csv
import sqlite3
import unicodedata
import re
from datetime import datetime
from typing import Dict, List, Tuple

class AtualizadorUltimosConfrontos:
    def __init__(self):
        self.jogos_dir = "backend/models/Jogos"
        self.db_path = "backend/models/tabelas_classificacao.db"
        
        # Mapeamento de nomes de times para códigos (baseado nos nomes do banco de dados)
        self.mapeamento_times = {
            # Série A - nomes exatos do banco -> códigos
            "Atlético-MG": "Atl", "Bahia": "Bah", "Botafogo": "Bot", "Bragantino": "Red",
            "Ceará": "Cea", "Corinthians": "Cor", "Cruzeiro": "Cru", "Flamengo": "Fla",
            "Fluminense": "Flu", "Fortaleza": "For", "Grêmio": "Grê", "Internacional": "Int",
            "Juventude": "Juv", "Mirassol": "Mir", "Palmeiras": "Pal", "Santos": "San",
            "São Paulo": "São", "Sport": "Spo", "Vasco": "Vas", "Vitória": "Vit",
            
            # Série B - nomes exatos do banco -> códigos
            "Coritiba": "Cor", "Criciúma": "Cri", "Goiás": "Goi", "Athletico-PR": "Ath",
            "Novorizontino": "Gre", "Cuiabá": "Cui", "Chapecoense": "Cha", "CRB": "Crb",
            "Remo": "Rem", "Atlético-GO": "Atl", "Avaí": "Ava", "Operário": "Ope",
            "Vila Nova": "Vil", "Ferroviária": "Fer", "América-MG": "Ame", "Athletic": "Ath",
            "Volta Redonda": "Vol", "Botafogo SP": "Bot", "Amazonas FC": "Ama", "Paysandu": "Pay"
        }
        
        # Mapeamento de códigos para pastas de arquivos
        self.mapeamento_reverso = {
            "Atl": "atletico-mg", "Bah": "bahia", "Bot": "botafogo", "Red": "red-bull-bragantino",
            "Cea": "ceara", "Cor": "corinthians", "Cru": "cruzeiro", "Fla": "flamengo",
            "Flu": "fluminense", "For": "fortaleza", "Grê": "gremio", "Int": "internacional",
            "Juv": "juventude", "Mir": "mirassol", "Pal": "palmeiras", "San": "santos",
            "São": "sao-paulo", "Spo": "sport-recife", "Vas": "vasco", "Vit": "vitoria",
            "Ama": "amazonas-fc", "Ame": "america-mg", "Ath": "athletico-pr", "Ava": "avai",
            "Cha": "chapecoense", "Crb": "crb-al", "Cri": "criciuma", "Cui": "cuiaba",
            "Fer": "ferroviaria", "Goi": "goias", "Gre": "novohorizontino", "Ope": "operario-pr",
            "Pay": "paysandu", "Rem": "remo", "Vil": "vila-nova", "Vol": "volta-redonda"
        }

    def normalizar_nome(self, nome: str) -> str:
        """Normaliza um nome removendo acentos, convertendo para minúsculo e removendo caracteres especiais"""
        # Remove acentos
        nome_normalizado = unicodedata.normalize('NFD', nome)
        nome_normalizado = ''.join(c for c in nome_normalizado if unicodedata.category(c) != 'Mn')
        
        # Converte para minúsculo
        nome_normalizado = nome_normalizado.lower()
        
        # Remove caracteres especiais e espaços, substitui por hífen
        nome_normalizado = re.sub(r'[^a-z0-9]', '-', nome_normalizado)
        
        # Remove hífens duplicados
        nome_normalizado = re.sub(r'-+', '-', nome_normalizado)
        
        # Remove hífens do início e fim
        nome_normalizado = nome_normalizado.strip('-')
        
        return nome_normalizado

    def encontrar_pasta_arquivo(self, nome_time_banco: str) -> str:
        """Encontra a pasta do arquivo baseada no nome do time no banco de dados"""
        nome_normalizado = self.normalizar_nome(nome_time_banco)
        
        # Lista todas as pastas disponíveis
        pastas_disponiveis = []
        if os.path.exists(self.jogos_dir):
            pastas_disponiveis = [d for d in os.listdir(self.jogos_dir) 
                                if os.path.isdir(os.path.join(self.jogos_dir, d))]
        
        # Procura por correspondência exata
        for pasta in pastas_disponiveis:
            if self.normalizar_nome(pasta) == nome_normalizado:
                return pasta
        
        # Procura por correspondência parcial
        for pasta in pastas_disponiveis:
            if nome_normalizado in self.normalizar_nome(pasta) or self.normalizar_nome(pasta) in nome_normalizado:
                return pasta
        
        return None

    def ler_jogos_time(self, nome_time_banco: str) -> List[Dict]:
        """Lê os jogos de um time específico usando normalização de nomes"""
        # Encontra a pasta do arquivo usando normalização
        nome_pasta = self.encontrar_pasta_arquivo(nome_time_banco)
        
        if not nome_pasta:
            print(f"ERRO: Pasta nao encontrada para {nome_time_banco}")
            return []
        
        arquivo_jogos = os.path.join(self.jogos_dir, nome_pasta, "jogos.csv")
        
        if not os.path.exists(arquivo_jogos):
            print(f"ERRO: Arquivo nao encontrado: {arquivo_jogos}")
            return []
        
        jogos = []
        try:
            with open(arquivo_jogos, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jogos.append(row)
            print(f"OK: {len(jogos)} jogos carregados para {nome_time_banco} (pasta: {nome_pasta})")
            return jogos
        except Exception as e:
            print(f"ERRO ao ler {arquivo_jogos}: {e}")
            return []

    def calcular_ultimos_5_jogos(self, jogos: List[Dict], nome_time_banco: str) -> str:
        """Calcula os últimos 5 jogos de um time e retorna a sequência"""
        if not jogos:
            return "-----"
        
        # Encontra o código do time no mapeamento
        codigo_time = self.mapeamento_times.get(nome_time_banco)
        if not codigo_time:
            print(f"ERRO: Codigo nao encontrado para {nome_time_banco}")
            return "-----"
        
        # Ordena por data (mais antigo primeiro) - CORRIGIDO para usar datetime
        def parse_data(data_str):
            try:
                # Tentar formato DD/MM/YYYY primeiro
                return datetime.strptime(data_str, '%d/%m/%Y')
            except ValueError:
                try:
                    # Tentar formato YYYY-MM-DD
                    return datetime.strptime(data_str, '%Y-%m-%d')
                except ValueError:
                    # Se não conseguir, retornar data muito antiga
                    return datetime(1900, 1, 1)
        
        jogos_ordenados = sorted(jogos, key=lambda x: parse_data(x['Data']), reverse=True)
        
        # Pega os últimos 5 jogos (mais recentes primeiro) e inverte para mostrar mais recente -> mais antigo
        ultimos_5 = jogos_ordenados[:5][::-1]
        
        sequencia = ""
        for jogo in ultimos_5:
            # Primeiro tenta o formato antigo (Resultado_Codigo)
            resultado = jogo.get('Resultado_' + codigo_time, '')
            
            # Se não encontrar, tenta o formato novo (apenas Resultado)
            if not resultado:
                resultado = jogo.get('Resultado', '')
            
            # Se ainda não encontrar, tenta com acentos
            if not resultado and codigo_time == 'Pal':
                resultado = jogo.get('Resultado_Pal', '')
            elif not resultado and codigo_time == 'Grê':
                resultado = jogo.get('Resultado_Grê', '')
            elif not resultado and codigo_time == 'São':
                resultado = jogo.get('Resultado_São', '')
            elif not resultado and codigo_time == 'Cea':
                resultado = jogo.get('Resultado_Cea', '')
            elif not resultado and codigo_time == 'Vit':
                resultado = jogo.get('Resultado_Vit', '')
            
            # Verificar se o time jogou em casa ou fora
            time_casa = jogo.get('Time_Casa', '')
            time_visitante = jogo.get('Time_Visitante', '')
            
            # Determinar se o time jogou em casa
            jogou_em_casa = (time_casa == codigo_time or 
                           (codigo_time == 'Pal' and time_casa == 'Pal') or
                           (codigo_time == 'Grê' and time_casa == 'Grê') or
                           (codigo_time == 'São' and time_casa == 'São') or
                           (codigo_time == 'Cea' and time_casa == 'Cea') or
                           (codigo_time == 'Vit' and time_casa == 'Vit'))
            
            # Se jogou fora de casa, inverter o resultado
            if not jogou_em_casa:
                if resultado in ['Vitória', 'Vitoria', 'V']:
                    resultado = 'Derrota'
                elif resultado in ['Derrota', 'D']:
                    resultado = 'Vitória'
                # Empate continua empate
            
            # Reconhece tanto nomes completos quanto abreviações
            if resultado in ['Vitória', 'Vitoria', 'V']:
                sequencia += "V"
            elif resultado in ['Empate', 'E']:
                sequencia += "E"
            elif resultado in ['Derrota', 'D']:
                sequencia += "D"
            else:
                sequencia += "-"
        
        # Sequencia ja esta na ordem correta (mais recente -> mais antigo)
        
        return sequencia

    def verificar_e_criar_coluna(self, cursor, serie: str):
        """Verifica se a coluna ultimos_confrontos existe e a cria se necessário"""
        try:
            # Verifica se a coluna existe
            cursor.execute(f"PRAGMA table_info(classificacao_{serie.lower().replace(' ', '_')})")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'ultimos_confrontos' not in colunas:
                print(f"Criando coluna 'ultimos_confrontos' na tabela {serie}...")
                cursor.execute(f"ALTER TABLE classificacao_{serie.lower().replace(' ', '_')} ADD COLUMN ultimos_confrontos TEXT DEFAULT '-----'")
                print(f"Coluna 'ultimos_confrontos' criada com sucesso!")
            else:
                print(f"Coluna 'ultimos_confrontos' ja existe na tabela {serie}")
        except Exception as e:
            print(f"ERRO ao verificar/criar coluna: {e}")

    def atualizar_tabela_classificacao(self, serie: str):
        """Atualiza a tabela de classificação de uma série específica"""
        print(f"\nAtualizando {serie}...")
        
        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Verifica e cria a coluna se necessário
            self.verificar_e_criar_coluna(cursor, serie)
            # Busca todos os times da série
            cursor.execute(f"SELECT posicao, time FROM classificacao_{serie.lower().replace(' ', '_')} ORDER BY posicao")
            times = cursor.fetchall()
            
            print(f"Encontrados {len(times)} times na {serie}")
            
            for posicao, nome_time in times:
                # Lê os jogos do time usando normalização
                jogos = self.ler_jogos_time(nome_time)
                
                if not jogos:
                    print(f"AVISO: Nenhum jogo encontrado para {nome_time}")
                    continue
                
                # Calcula os últimos 5 jogos
                ultimos_confrontos = self.calcular_ultimos_5_jogos(jogos, nome_time)
                
                # Atualiza no banco de dados
                cursor.execute(f"""
                    UPDATE classificacao_{serie.lower().replace(' ', '_')} 
                    SET ultimos_confrontos = ? 
                    WHERE time = ?
                """, (ultimos_confrontos, nome_time))
                
                print(f"OK: {posicao}o {nome_time}: {ultimos_confrontos}")
            
            # Salva as alterações
            conn.commit()
            print(f"{serie} atualizada com sucesso!")
            
        except Exception as e:
            print(f"ERRO ao atualizar {serie}: {e}")
            conn.rollback()
        finally:
            conn.close()

    def atualizar_todas_tabelas(self):
        """Atualiza todas as tabelas de classificação"""
        print("Iniciando atualizacao automatica dos Ultimos Confrontos...")
        print(f"Diretorio de jogos: {self.jogos_dir}")
        print(f"Banco de dados: {self.db_path}")
        
        # Verifica se o banco existe
        if not os.path.exists(self.db_path):
            print(f"ERRO: Banco de dados nao encontrado: {self.db_path}")
            return
        
        # Atualiza Série A
        self.atualizar_tabela_classificacao("Serie A")
        
        # Atualiza Série B
        self.atualizar_tabela_classificacao("Serie B")
        
        print("\nAtualizacao completa!")
        print("Todas as tabelas foram atualizadas com os ultimos 5 confrontos!")

    def mostrar_estatisticas(self):
        """Mostra estatísticas dos arquivos de jogos"""
        print("\nESTATISTICAS DOS ARQUIVOS DE JOGOS:")
        print("=" * 50)
        
        total_times = 0
        total_jogos = 0
        
        for codigo, nome_pasta in self.mapeamento_times.items():
            arquivo_jogos = os.path.join(self.jogos_dir, nome_pasta, "jogos.csv")
            
            if os.path.exists(arquivo_jogos):
                try:
                    with open(arquivo_jogos, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        jogos = list(reader)
                    
                    total_times += 1
                    total_jogos += len(jogos)
                    print(f"OK: {codigo:20} ({nome_pasta:3}): {len(jogos):2} jogos")
                except Exception as e:
                    print(f"ERRO: {codigo:20} ({nome_pasta:3}): Erro - {e}")
            else:
                print(f"AVISO: {codigo:20} ({nome_pasta:3}): Arquivo nao encontrado")
        
        print("=" * 50)
        print(f"Total: {total_times} times, {total_jogos} jogos")

def main():
    """Função principal"""
    atualizador = AtualizadorUltimosConfrontos()
    
    print("SISTEMA DE ATUALIZACAO AUTOMATICA DOS ULTIMOS CONFRONTOS")
    print("=" * 60)
    
    # Mostra estatísticas
    atualizador.mostrar_estatisticas()
    
    # Atualiza todas as tabelas
    atualizador.atualizar_todas_tabelas()
    
    print("\nSistema executado com sucesso!")
    print("As tabelas de classificacao agora estao atualizadas!")

if __name__ == "__main__":
    main()
