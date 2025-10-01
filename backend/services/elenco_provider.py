#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provedor de dados de elenco dos clubes
Lê dados do planilha_clubes_futebol_final.html e fornece para a API
"""

import os
import re
import json
from pathlib import Path

class ElencoProvider:
    def __init__(self):
        self.dados_elenco = {}
        self.carregar_dados_planilha()
    
    def carregar_dados_planilha(self):
        """Carrega dados do arquivo HTML da planilha"""
        try:
            # Caminho para o arquivo HTML
            html_file = Path(__file__).parent.parent / "models" / "EstatisticasElenco" / "planilha_clubes_futebol_final.html"
            
            if not html_file.exists():
                print(f"AVISO: Arquivo nao encontrado: {html_file}")
                return
            
            # Ler e processar o arquivo HTML
            with open(html_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extrair dados JavaScript das arrays
            self._extrair_dados_javascript(content)
            
            print(f"OK: Dados de elenco carregados: {len(self.dados_elenco)} clubes")
            
        except Exception as e:
            print(f"ERRO: Erro ao carregar dados de elenco: {e}")
    
    def _extrair_dados_javascript(self, content):
        """Extrai dados das arrays JavaScript no HTML"""
        try:
            # Extrair dados da Série A
            serie_a_match = re.search(r'const serieAClubs = \[(.*?)\];', content, re.DOTALL)
            if serie_a_match:
                self._processar_dados_serie(serie_a_match.group(1), 'A')
            
            # Extrair dados da Série B
            serie_b_match = re.search(r'const serieBClubs = \[(.*?)\];', content, re.DOTALL)
            if serie_b_match:
                self._processar_dados_serie(serie_b_match.group(1), 'B')
                
        except Exception as e:
            print(f"ERRO: Erro ao extrair dados JavaScript: {e}")
    
    def _processar_dados_serie(self, dados_texto, serie):
        """Processa dados de uma série específica"""
        try:
            # Usar regex para extrair objetos individuais
            objetos = re.findall(r'\{[^}]+\}', dados_texto)
            
            for obj_str in objetos:
                # Extrair campos usando regex
                clube_match = re.search(r'clube:\s*"([^"]+)"', obj_str)
                valor_total_match = re.search(r'valorTotal:\s*"([^"]+)"', obj_str)
                plantel_match = re.search(r'plantel:\s*(\d+)', obj_str)
                idade_media_match = re.search(r'idadeMedia:\s*([\d.]+)', obj_str)
                estrangeiros_match = re.search(r'estrangeiros:\s*(\d+)', obj_str)
                valor_medio_match = re.search(r'valorMedio:\s*"([^"]+)"', obj_str)
                
                if clube_match:
                    clube_nome = clube_match.group(1)
                    
                    # Normalizar nome do clube
                    clube_normalizado = self._normalizar_nome_clube(clube_nome)
                    
                    valor_total_str = valor_total_match.group(1) if valor_total_match else '€ 0 mi.'
                    valor_mm_euros = self._extrair_valor_em_mm_euros(valor_total_str)
                    
                    self.dados_elenco[clube_normalizado] = {
                        'nome_original': clube_nome,
                        'serie': serie,
                        'valor_total': valor_total_str,
                        'valor_mm_euros': valor_mm_euros,
                        'valor_mm_formatado': f"€ {valor_mm_euros:.1f}MM",
                        'plantel': int(plantel_match.group(1)) if plantel_match else 0,
                        'idade_media': float(idade_media_match.group(1)) if idade_media_match else 0.0,
                        'estrangeiros': int(estrangeiros_match.group(1)) if estrangeiros_match else 0,
                        'valor_medio': valor_medio_match.group(1) if valor_medio_match else '€ 0 mil',
                        'forca_elenco': self._calcular_forca_elenco(valor_total_str),
                        'rating': self._calcular_rating(valor_total_str, serie)
                    }
                    
        except Exception as e:
            print(f"ERRO: Erro ao processar dados da serie {serie}: {e}")
    
    def _normalizar_nome_clube(self, nome):
        """Normaliza nome do clube para matching"""
        # Mapeamento de nomes
        mapeamento = {
            'SE Palmeiras': 'PALMEIRAS',
            'CR Flamengo': 'FLAMENGO', 
            'Botafogo FR': 'BOTAFOGO',
            'Cruzeiro EC': 'CRUZEIRO',
            'SC Corinthians': 'CORINTHIANS',
            'CR Vasco da Gama': 'VASCO',
            'EC Bahia': 'BAHIA',
            'Atlético Mineiro': 'ATLETICO-MG',
            'Fluminense FC': 'FLUMINENSE',
            'RB Bragantino': 'RED BULL BRAGANTINO',
            'São Paulo FC': 'SAO PAULO',
            'Grêmio FBPA': 'GREMIO',
            'SC Internacional': 'INTERNACIONAL',
            'Santos FC': 'SANTOS',
            'Fortaleza EC': 'FORTALEZA',
            'Sport Recife': 'SPORT RECIFE',
            'EC Vitória': 'VITORIA',
            'Ceará SC': 'CEARA',
            'EC Juventude': 'JUVENTUDE',
            'Mirassol FC': 'MIRASSOL'
        }
        
        return mapeamento.get(nome, nome.upper())
    
    def _calcular_forca_elenco(self, valor_total_str):
        """Calcula força do elenco baseada no valor total em MM Euros"""
        try:
            # Extrair valor numérico e converter para MM Euros
            valor_mm = self._extrair_valor_em_mm_euros(valor_total_str)
            
            # Escala de força baseada no valor em MM Euros (0-10)
            if valor_mm >= 200:    # € 200MM+
                return 10.0
            elif valor_mm >= 150:  # € 150-200MM
                return 9.0
            elif valor_mm >= 100:  # € 100-150MM
                return 8.0
            elif valor_mm >= 80:   # € 80-100MM
                return 7.0
            elif valor_mm >= 60:   # € 60-80MM
                return 6.0
            elif valor_mm >= 40:   # € 40-60MM
                return 5.0
            elif valor_mm >= 25:   # € 25-40MM
                return 4.0
            elif valor_mm >= 15:   # € 15-25MM
                return 3.0
            elif valor_mm >= 10:   # € 10-15MM
                return 2.0
            else:                  # < € 10MM
                return 1.0
            
        except:
            return 1.0
    
    def _extrair_valor_em_mm_euros(self, valor_str):
        """Extrai valor e converte para MM Euros (milhões)"""
        try:
            # Padrões possíveis: "€ 212.15 mi.", "€ 1.82 bilhões", etc.
            valor_str = valor_str.lower().replace(',', '.')
            
            # Buscar padrão numérico
            valor_match = re.search(r'€\s*([\d.]+)\s*(mi\.|milhões|bilhões|bi\.)', valor_str)
            
            if valor_match:
                valor = float(valor_match.group(1))
                unidade = valor_match.group(2)
                
                # Converter para MM Euros
                if 'bilhões' in unidade or 'bi.' in unidade:
                    return valor * 1000  # Bilhões para milhões
                elif 'mi.' in unidade or 'milhões' in unidade:
                    return valor  # Já está em milhões
                else:
                    return valor  # Assumir milhões por padrão
            
            # Fallback: tentar extrair apenas número
            numero_match = re.search(r'€\s*([\d.]+)', valor_str)
            if numero_match:
                return float(numero_match.group(1))
            
            return 50.0  # Valor padrão em MM Euros
            
        except Exception as e:
            print(f"AVISO: Erro ao extrair valor: {valor_str} - {e}")
            return 50.0
    
    def _calcular_rating(self, valor_total_str, serie):
        """Calcula rating percentual (0-1) baseado na série"""
        try:
            forca = self._calcular_forca_elenco(valor_total_str)
            
            # Ajustar rating baseado na série
            if serie == 'A':
                # Série A: escala mais alta
                return min(forca / 10.0, 1.0)
            else:
                # Série B: escala mais baixa
                return min(forca / 15.0, 0.7)  # Máximo 70% para Série B
                
        except:
            return 0.1
    
    def obter_dados_clube(self, nome_clube):
        """Obtém dados de um clube específico"""
        nome_normalizado = nome_clube.upper().strip()
        
        # Tentar match direto
        if nome_normalizado in self.dados_elenco:
            return self.dados_elenco[nome_normalizado]
        
        # Tentar match parcial
        for clube_key, dados in self.dados_elenco.items():
            if nome_normalizado in clube_key or clube_key in nome_normalizado:
                return dados
        
        # Retornar dados padrão se não encontrar
        return {
            'nome_original': nome_clube,
            'serie': 'A',
            'valor_total': '€ 50 mi.',
            'valor_mm_euros': 50.0,
            'valor_mm_formatado': '€ 50.0MM',
            'plantel': 30,
            'idade_media': 27.0,
            'estrangeiros': 5,
            'valor_medio': '€ 1.5 mi.',
            'forca_elenco': 5.0,
            'rating': 0.5
        }
    
    def obter_todos_clubes(self):
        """Retorna todos os dados de clubes"""
        return self.dados_elenco
    
    def obter_clubes_por_serie(self, serie):
        """Retorna clubes de uma série específica"""
        return {k: v for k, v in self.dados_elenco.items() if v['serie'] == serie}

# Instância global
elenco_provider = ElencoProvider()

def get_elenco_data(clube_nome):
    """Função helper para obter dados de elenco"""
    return elenco_provider.obter_dados_clube(clube_nome)

def get_all_elenco_data():
    """Função helper para obter todos os dados"""
    return elenco_provider.obter_todos_clubes()
