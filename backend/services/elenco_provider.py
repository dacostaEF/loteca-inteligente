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

# ===== OTIMIZAÇÃO: DEBUG MODE =====
# Ativar logs apenas em desenvolvimento (localhost/127.0.0.1)
DEBUG = os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'True'

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
                    categoria = self._calcular_categoria_elenco(valor_mm_euros)
                    
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
                        'rating': self._calcular_rating(valor_total_str, serie),
                        'categoria': categoria  # ✅ NOVO: Categoria A+/A/B/C/D
                    }
                    
        except Exception as e:
            print(f"ERRO: Erro ao processar dados da serie {serie}: {e}")
    
    def _normalizar_nome_clube(self, nome):
        """Normaliza nome do clube para matching"""
        # Mapeamento de nomes - CORRIGIDO PARA MATCH COM FRONTEND
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
    
    def _normalizar_nome_entrada(self, nome_entrada):
        """Normaliza nome de entrada do frontend para matching com CSV"""
        # Mapeamento reverso: frontend -> CSV
        mapeamento_entrada = {
            'PALMEIRAS': 'PALMEIRAS',
            'FLAMENGO': 'FLAMENGO',
            'BOTAFOGO': 'BOTAFOGO',
            'CRUZEIRO': 'CRUZEIRO',
            'CORINTHIANS': 'CORINTHIANS',
            'VASCO': 'VASCO',
            'BAHIA': 'BAHIA',
            'ATLETICO-MG': 'ATLETICO-MG',
            'FLUMINENSE': 'FLUMINENSE',
            'RED BULL BRAGANTINO': 'RED BULL BRAGANTINO',
            'SAO PAULO': 'SAO PAULO',
            'GREMIO': 'GREMIO',
            'INTERNACIONAL': 'INTERNACIONAL',
            'SANTOS': 'SANTOS',
            'FORTALEZA': 'FORTALEZA',
            'SPORT RECIFE': 'SPORT RECIFE',
            'VITORIA': 'VITORIA',
            'CEARA': 'CEARA',
            'JUVENTUDE': 'JUVENTUDE',
            'MIRASSOL': 'MIRASSOL'
        }
        
        return mapeamento_entrada.get(nome_entrada.upper(), nome_entrada.upper())
    
    def _calcular_categoria_elenco(self, valor_mm):
        """
        Calcula CATEGORIA do elenco baseada no valor total em MM Euros
        ✅ SISTEMA DE CATEGORIAS PROFISSIONAL (A+, A, B, C, D)
        
        A+ → SUPERPOTÊNCIAS       (>€800MM)   | Inglaterra, França, Real Madrid
        A  → ELITE                (€300-800MM) | Brasil, Argentina, Bayern
        B  → COMPETITIVOS         (€100-300MM) | Flamengo, Palmeiras, Uruguai
        C  → EM DESENVOLVIMENTO   (€30-100MM)  | Japão, Fortaleza, Bósnia
        D  → BASES SÓLIDAS        (<€30MM)     | Letônia, Série B baixa
        """
        if valor_mm >= 800:
            return 'A+'
        elif valor_mm >= 300:
            return 'A'
        elif valor_mm >= 100:
            return 'B'
        elif valor_mm >= 30:
            return 'C'
        else:
            return 'D'
    
    def _calcular_forca_elenco(self, valor_total_str):
        """
        Calcula categoria e mantém compatibilidade com força numérica legada
        """
        try:
            valor_mm = self._extrair_valor_em_mm_euros(valor_total_str)
            categoria = self._calcular_categoria_elenco(valor_mm)
            
            # Mapear categoria para valor numérico (para compatibilidade)
            mapa_categoria_numero = {
                'A+': 10.0,
                'A': 8.5,
                'B': 7.0,
                'C': 5.0,
                'D': 3.0
            }
            
            return mapa_categoria_numero.get(categoria, 5.0)
            
        except:
            return 5.0  # Fallback: valor médio
    
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
        # ✅ CORRIGIDO: Usar normalização de entrada
        nome_normalizado = self._normalizar_nome_entrada(nome_clube)
        
        # ===== LOGS APENAS EM DEBUG =====
        if DEBUG:
            print(f"🔍 [ELENCO] Buscando clube: '{nome_clube}' -> normalizado: '{nome_normalizado}'")
            print(f"🔍 [ELENCO] Clubes disponíveis: {list(self.dados_elenco.keys())}")
        
        # Tentar match direto
        if nome_normalizado in self.dados_elenco:
            if DEBUG:
                print(f"✅ [ELENCO] Match direto encontrado: {nome_normalizado}")
            return self.dados_elenco[nome_normalizado]
        
        # Tentar match parcial
        for clube_key, dados in self.dados_elenco.items():
            if nome_normalizado in clube_key or clube_key in nome_normalizado:
                if DEBUG:
                    print(f"✅ [ELENCO] Match parcial encontrado: {clube_key}")
                return dados
        
        # ❌ NÃO ENCONTRADO - Retornar erro ao invés de dados padrão
        if DEBUG:
            print(f"❌ [ELENCO] Clube não encontrado: {nome_clube}")
        return None
    
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
