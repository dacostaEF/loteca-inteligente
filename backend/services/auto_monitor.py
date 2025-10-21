#!/usr/bin/env python3
"""
Monitor Automático de Classificação
Monitora mudanças nos CSVs e atualiza automaticamente as tabelas
"""

import os
import time
import hashlib
from datetime import datetime
from typing import Dict, Set
import logging
import threading

from services.classificacao_integrador import ClassificacaoIntegrador

logger = logging.getLogger(__name__)

class AutoMonitor:
    """
    Monitor automático que detecta mudanças nos CSVs e atualiza as tabelas
    """
    
    def __init__(self, check_interval: int = 300):  # 5 minutos
        self.check_interval = check_interval
        self.integrador = ClassificacaoIntegrador()
        self.last_hashes = {}
        self.running = False
        self.monitor_thread = None
        
        # Caminhos para monitorar
        self.serie_a_path = "backend/estatistica/Serie_A"
        self.serie_b_path = "backend/estatistica/Serie_B"
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calcula hash de um arquivo para detectar mudanças"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def get_all_csv_files(self) -> Dict[str, str]:
        """Obtém todos os arquivos CSV e seus hashes"""
        csv_files = {}
        
        # Monitorar Série A
        if os.path.exists(self.serie_a_path):
            for clube_dir in os.listdir(self.serie_a_path):
                clube_path = os.path.join(self.serie_a_path, clube_dir)
                if os.path.isdir(clube_path):
                    csv_path = os.path.join(clube_path, "jogos.csv")
                    if os.path.exists(csv_path):
                        csv_files[csv_path] = self.calculate_file_hash(csv_path)
        
        # Monitorar Série B
        if os.path.exists(self.serie_b_path):
            for clube_dir in os.listdir(self.serie_b_path):
                clube_path = os.path.join(self.serie_b_path, clube_dir)
                if os.path.isdir(clube_path):
                    csv_path = os.path.join(clube_path, "jogos.csv")
                    if os.path.exists(csv_path):
                        csv_files[csv_path] = self.calculate_file_hash(csv_path)
        
        return csv_files
    
    def detect_changes(self) -> bool:
        """Detecta se houve mudanças nos CSVs"""
        current_hashes = self.get_all_csv_files()
        
        # Primeira execução - salvar hashes iniciais
        if not self.last_hashes:
            self.last_hashes = current_hashes
            logger.info("🔍 Monitor iniciado - hashes iniciais salvos")
            return False
        
        # Verificar mudanças
        changes_detected = False
        for file_path, current_hash in current_hashes.items():
            if file_path not in self.last_hashes or self.last_hashes[file_path] != current_hash:
                logger.info(f"📝 Mudança detectada em: {file_path}")
                changes_detected = True
        
        # Atualizar hashes
        self.last_hashes = current_hashes
        
        return changes_detected
    
    def update_classification(self):
        """Atualiza as tabelas de classificação"""
        try:
            logger.info("🔄 Atualização automática iniciada...")
            resultado = self.integrador.atualizar_todas_series()
            
            if resultado['serie_a'] and resultado['serie_b']:
                logger.info("✅ Atualização automática concluída com sucesso!")
            else:
                logger.warning("⚠️ Atualização automática parcial")
                
        except Exception as e:
            logger.error(f"❌ Erro na atualização automática: {e}")
    
    def monitor_loop(self):
        """Loop principal do monitor"""
        logger.info("🚀 Monitor automático iniciado")
        
        while self.running:
            try:
                if self.detect_changes():
                    logger.info("🔄 Mudanças detectadas - iniciando atualização...")
                    self.update_classification()
                else:
                    logger.debug("👀 Nenhuma mudança detectada")
                
                # Aguardar próximo check
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"❌ Erro no monitor: {e}")
                time.sleep(60)  # Aguardar 1 minuto em caso de erro
    
    def start_monitoring(self):
        """Inicia o monitoramento automático"""
        if self.running:
            logger.warning("⚠️ Monitor já está rodando")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("🎯 Monitor automático ATIVADO!")
        logger.info(f"⏰ Verificando mudanças a cada {self.check_interval} segundos")
    
    def stop_monitoring(self):
        """Para o monitoramento automático"""
        if not self.running:
            logger.warning("⚠️ Monitor não está rodando")
            return
        
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        logger.info("🛑 Monitor automático PARADO!")
    
    def force_update(self):
        """Força atualização imediata"""
        logger.info("🔄 Forçando atualização imediata...")
        self.update_classification()
    
    def get_status(self) -> Dict:
        """Retorna status do monitor"""
        return {
            'running': self.running,
            'check_interval': self.check_interval,
            'monitored_files': len(self.last_hashes),
            'last_check': datetime.now().isoformat()
        }

# Instância global do monitor
auto_monitor = AutoMonitor()

def start_auto_monitoring():
    """Inicia o monitoramento automático"""
    auto_monitor.start_monitoring()

def stop_auto_monitoring():
    """Para o monitoramento automático"""
    auto_monitor.stop_monitoring()

def force_auto_update():
    """Força atualização automática"""
    auto_monitor.force_update()

def get_monitor_status():
    """Retorna status do monitor"""
    return auto_monitor.get_status()

if __name__ == "__main__":
    # Teste do monitor
    print("🚀 Iniciando monitor automático...")
    auto_monitor.start_monitoring()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando monitor...")
        auto_monitor.stop_monitoring()

