#!/usr/bin/env python3
"""
Integrador de Classificação Automática
Conecta o sistema automático com o banco de dados existente
"""

import os
import sys
from datetime import datetime
from typing import List, Dict

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.classificacao_db import ClassificacaoDB
from services.auto_classificacao import AutoClassificacao
import logging

logger = logging.getLogger(__name__)

class ClassificacaoIntegrador:
    """
    Integra o sistema automático com o banco de dados
    """
    
    def __init__(self):
        self.auto_class = AutoClassificacao()
        self.db = ClassificacaoDB()
    
    def atualizar_serie_a_automatica(self) -> bool:
        """
        Atualiza a Série A com dados da tabela tradicional CSV
        """
        try:
            logger.info("🔄 Atualizando Série A via tabela tradicional...")
            
            # Processar dados da tabela tradicional
            resultado = self.auto_class.processar_serie_a_tradicional()
            
            if not resultado:
                logger.error("❌ Nenhum dado processado para Série A")
                return False
            
            # Limpar dados antigos da Série A
            self._limpar_serie_a()
            
            # Inserir novos dados
            for clube in resultado:
                self._inserir_clube_serie_a(clube)
            
            logger.info(f"✅ Série A atualizada via tabela tradicional: {len(resultado)} clubes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar Série A: {e}")
            return False
    
    def atualizar_serie_b_automatica(self) -> bool:
        """
        Atualiza a Série B com dados da tabela tradicional CSV
        """
        try:
            logger.info("🔄 Atualizando Série B via tabela tradicional...")
            
            resultado = self.auto_class.processar_serie_b_tradicional()
            
            if not resultado:
                logger.error("❌ Nenhum dado processado para Série B")
                return False
            
            self._limpar_serie_b()
            
            for clube in resultado:
                self._inserir_clube_serie_b(clube)
            
            logger.info(f"✅ Série B atualizada via tabela tradicional: {len(resultado)} clubes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar Série B: {e}")
            return False
    
    def atualizar_serie_c_automatica(self) -> bool:
        """
        Atualiza a Série C com dados da tabela tradicional CSV
        """
        try:
            logger.info("🔄 Atualizando Série C via tabela tradicional...")
            
            resultado = self.auto_class.processar_serie_c_tradicional()
            
            if not resultado:
                logger.error("❌ Nenhum dado processado para Série C")
                return False
            
            # Nota: Série C não tem tabela no banco ainda, apenas processamento
            logger.info(f"✅ Série C processada via tabela tradicional: {len(resultado)} clubes")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar Série C: {e}")
            return False
    
    
    def _limpar_serie_a(self):
        """Limpa dados antigos da Série A"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("DELETE FROM classificacao_serie_a")
                conn.commit()
                logger.info("🗑️ Dados antigos da Série A removidos")
        except Exception as e:
            logger.error(f"Erro ao limpar Série A: {e}")
    
    def _limpar_serie_b(self):
        """Limpa dados antigos da Série B"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("DELETE FROM classificacao_serie_b")
                conn.commit()
                logger.info("🗑️ Dados antigos da Série B removidos")
        except Exception as e:
            logger.error(f"Erro ao limpar Série B: {e}")
    
    def _inserir_clube_serie_a(self, clube: Dict):
        """Insere clube na tabela da Série A"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO classificacao_serie_a (
                        posicao, time, pontos, jogos, vitorias, empates, derrotas,
                        gols_pro, gols_contra, saldo_gols, aproveitamento,
                        ultimos_confrontos, ultimos_jogos, zona, data_atualizacao, rodada, fonte
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clube['posicao'],
                    clube['time'],
                    clube['pontos'],
                    clube['jogos'],
                    clube['vitorias'],
                    clube['empates'],
                    clube['derrotas'],
                    clube['gols_pro'],
                    clube['gols_contra'],
                    clube['saldo_gols'],
                    clube['aproveitamento'],
                    clube.get('ultimos_confrontos', 'N/A'),  # ultimos_confrontos
                    clube.get('ultimos_jogos', 'N/A'),  # ultimos_jogos
                    clube['zona'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # data_atualizacao
                    None,  # rodada (não aplicável)
                    'csv_tradicional'  # fonte
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao inserir {clube['time']} na Série A: {e}")
    
    def _inserir_clube_serie_b(self, clube: Dict):
        """Insere clube na tabela da Série B"""
        try:
            with self.db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO classificacao_serie_b (
                        posicao, time, pontos, jogos, vitorias, empates, derrotas,
                        gols_pro, gols_contra, saldo_gols, aproveitamento,
                        ultimos_confrontos, zona
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clube['posicao'],
                    clube['time'],
                    clube['pontos'],
                    clube['jogos'],
                    clube['vitorias'],
                    clube['empates'],
                    clube['derrotas'],
                    clube['gols_pro'],
                    clube['gols_contra'],
                    clube['saldo_gols'],
                    clube['aproveitamento'],
                    clube.get('ultimos_confrontos', 'N/A'),  # ultimos_confrontos
                    clube['zona']
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao inserir {clube['time']} na Série B: {e}")
    
    def atualizar_todas_series(self) -> Dict:
        """
        Atualiza Série A e B automaticamente
        """
        logger.info("🚀 Iniciando atualização automática de todas as séries...")
        
        resultado = {
            'serie_a': False,
            'serie_b': False,
            'timestamp': datetime.now().isoformat(),
            'erros': []
        }
        
        # Atualizar Série A
        try:
            resultado['serie_a'] = self.atualizar_serie_a_automatica()
        except Exception as e:
            resultado['erros'].append(f"Série A: {str(e)}")
            logger.error(f"Erro na Série A: {e}")
        
        # Atualizar Série B
        try:
            resultado['serie_b'] = self.atualizar_serie_b_automatica()
        except Exception as e:
            resultado['erros'].append(f"Série B: {str(e)}")
            logger.error(f"Erro na Série B: {e}")
        
        # Log do resultado
        if resultado['serie_a'] and resultado['serie_b']:
            logger.info("✅ Todas as séries atualizadas com sucesso!")
        else:
            logger.warning("⚠️ Algumas séries falharam na atualização")
        
        return resultado

# Função principal para uso externo
def executar_atualizacao_automatica():
    """
    Executa a atualização automática de todas as séries
    """
    integrador = ClassificacaoIntegrador()
    return integrador.atualizar_todas_series()

if __name__ == "__main__":
    # Teste do sistema
    resultado = executar_atualizacao_automatica()
    
    print("\n📊 RESULTADO DA ATUALIZAÇÃO:")
    print(f"Série A: {'✅' if resultado['serie_a'] else '❌'}")
    print(f"Série B: {'✅' if resultado['serie_b'] else '❌'}")
    
    if resultado['erros']:
        print("\n❌ ERROS:")
        for erro in resultado['erros']:
            print(f"- {erro}")

