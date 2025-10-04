#!/usr/bin/env python3
"""
Gerenciador de Concursos da Loteca
Sistema de arquivos JSON para armazenar dados dos concursos
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class ConcursoManager:
    """
    Gerenciador de concursos da Loteca
    Armazena dados em arquivos JSON organizados por número do concurso
    """
    
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), 'concursos')
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        """Garante que o diretório de concursos existe"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            logger.info(f"📁 Diretório de concursos criado: {self.base_path}")
    
    def get_concurso_file_path(self, numero: str) -> str:
        """Retorna o caminho do arquivo do concurso"""
        return os.path.join(self.base_path, f"concurso_{numero}.json")
    
    def salvar_concurso(self, numero: str, dados: Dict[str, Any]) -> bool:
        """
        Salva um concurso em arquivo JSON
        
        Args:
            numero: Número do concurso (ex: "1213")
            dados: Dados completos do concurso
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            # Adicionar metadados
            dados_completos = {
                "metadados": {
                    "numero": numero,
                    "salvo_em": datetime.now().isoformat(),
                    "versao": "1.0"
                },
                "concurso": dados.get("concurso", {}),
                "jogos": dados.get("jogos", []),
                "estatisticas": dados.get("estatisticas", {})
            }
            
            # Salvar arquivo
            file_path = self.get_concurso_file_path(numero)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(dados_completos, file, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Concurso {numero} salvo: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar concurso {numero}: {e}")
            return False
    
    def carregar_concurso(self, numero: str) -> Optional[Dict[str, Any]]:
        """
        Carrega um concurso do arquivo JSON
        
        Args:
            numero: Número do concurso
            
        Returns:
            Dict com dados do concurso ou None se não encontrado
        """
        try:
            file_path = self.get_concurso_file_path(numero)
            
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ Concurso {numero} não encontrado: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as file:
                dados = json.load(file)
            
            logger.info(f"📂 Concurso {numero} carregado: {file_path}")
            return dados
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar concurso {numero}: {e}")
            return None
    
    def listar_concursos(self) -> List[Dict[str, Any]]:
        """
        Lista todos os concursos disponíveis
        
        Returns:
            Lista com informações dos concursos
        """
        try:
            concursos = []
            
            if not os.path.exists(self.base_path):
                return concursos
            
            # Buscar arquivos de concurso
            for filename in os.listdir(self.base_path):
                if filename.startswith('concurso_') and filename.endswith('.json'):
                    # Extrair número do concurso
                    numero = filename.replace('concurso_', '').replace('.json', '')
                    
                    # Carregar dados básicos
                    dados = self.carregar_concurso(numero)
                    if dados:
                        concursos.append({
                            "numero": numero,
                            "data_sorteio": dados.get("concurso", {}).get("data_sorteio", ""),
                            "salvo_em": dados.get("metadados", {}).get("salvo_em", ""),
                            "total_jogos": len(dados.get("jogos", []))
                        })
            
            # Ordenar por número (mais recente primeiro)
            concursos.sort(key=lambda x: int(x["numero"]), reverse=True)
            
            logger.info(f"📋 {len(concursos)} concursos encontrados")
            return concursos
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar concursos: {e}")
            return []
    
    def get_ultimo_concurso(self) -> Optional[Dict[str, Any]]:
        """
        Retorna o último concurso (maior número)
        
        Returns:
            Dict com dados do último concurso ou None
        """
        try:
            concursos = self.listar_concursos()
            
            if not concursos:
                logger.info("📭 Nenhum concurso encontrado")
                return None
            
            # Pegar o primeiro (mais recente)
            ultimo_numero = concursos[0]["numero"]
            return self.carregar_concurso(ultimo_numero)
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar último concurso: {e}")
            return None
    
    def get_proximo_numero(self) -> str:
        """
        Retorna o próximo número de concurso disponível
        
        Returns:
            String com o próximo número
        """
        try:
            concursos = self.listar_concursos()
            
            if not concursos:
                return "1213"  # Primeiro concurso
            
            # Pegar o maior número e incrementar
            maior_numero = max(int(c["numero"]) for c in concursos)
            proximo = str(maior_numero + 1)
            
            logger.info(f"🔢 Próximo concurso: {proximo}")
            return proximo
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular próximo número: {e}")
            return "1213"
    
    def deletar_concurso(self, numero: str) -> bool:
        """
        Deleta um concurso
        
        Args:
            numero: Número do concurso
            
        Returns:
            bool: True se deletou com sucesso
        """
        try:
            file_path = self.get_concurso_file_path(numero)
            
            if not os.path.exists(file_path):
                logger.warning(f"⚠️ Concurso {numero} não existe para deletar")
                return False
            
            os.remove(file_path)
            logger.info(f"🗑️ Concurso {numero} deletado: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar concurso {numero}: {e}")
            return False

# Instância global
concurso_manager = ConcursoManager()
