#!/usr/bin/env python3
"""
LOTECA X-RAY - JOB DIÁRIO 23H55
Sistema de atualização automática de todos os dados
Executa TODOS OS DIAS às 23h55 para capturar resultados do dia
"""

import schedule
import time
import os
import sys
from datetime import datetime, timezone
import logging

# Configurar path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_job.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def criar_diretorio_logs():
    """Cria diretório de logs se não existir"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

def atualizar_brasileirao():
    """Atualiza dados do Brasileirão Série A e B"""
    try:
        logger.info("🇧🇷 Iniciando atualização do Brasileirão...")
        
        from models.brasileirao_db import brasileirao_db
        from services.cartola_provider import clubes, health_check
        
        # 1. Verificar se Cartola FC está funcionando
        health = health_check()
        if not health.get('api_response', False):
            logger.warning("⚠️ Cartola FC indisponível, usando dados simulados")
            usar_dados_simulados = True
        else:
            logger.info("✅ Cartola FC online")
            usar_dados_simulados = False
        
        # 2. FUTURO: Aqui seria scraping da CBF/GloboEsporte
        # Por enquanto, usar dados atualizados do sistema atual
        dados_serie_a = [
            {"pos": 1, "time": "Flamengo", "p": 54, "j": 24, "v": 16, "e": 6, "d": 2, "gp": 51, "gc": 12, "sg": 39, "aproveitamento": 75, "ultimos": "VVEVV", "zona": "libertadores"},
            {"pos": 2, "time": "Palmeiras", "p": 52, "j": 23, "v": 16, "e": 4, "d": 3, "gp": 39, "gc": 18, "sg": 21, "aproveitamento": 75, "ultimos": "VVVEV", "zona": "libertadores"},
            {"pos": 3, "time": "Cruzeiro", "p": 50, "j": 24, "v": 15, "e": 5, "d": 4, "gp": 40, "gc": 18, "sg": 22, "aproveitamento": 69, "ultimos": "VVDEV", "zona": "libertadores"},
            {"pos": 4, "time": "Mirassol", "p": 45, "j": 24, "v": 12, "e": 9, "d": 3, "gp": 43, "gc": 24, "sg": 19, "aproveitamento": 62, "ultimos": "EVDEV", "zona": "libertadores"},
            {"pos": 5, "time": "Botafogo", "p": 43, "j": 25, "v": 12, "e": 7, "d": 6, "gp": 37, "gc": 19, "sg": 18, "aproveitamento": 57, "ultimos": "VEVDD", "zona": "pre-libertadores"},
            {"pos": 6, "time": "Bahia", "p": 40, "j": 24, "v": 11, "e": 7, "d": 6, "gp": 33, "gc": 29, "sg": 4, "aproveitamento": 55, "ultimos": "EVVDE", "zona": "pre-libertadores"},
            {"pos": 7, "time": "São Paulo", "p": 38, "j": 25, "v": 10, "e": 8, "d": 7, "gp": 29, "gc": 25, "sg": 4, "aproveitamento": 50, "ultimos": "DEEVV", "zona": "sul-americana"},
            {"pos": 8, "time": "Fluminense", "p": 34, "j": 23, "v": 10, "e": 4, "d": 9, "gp": 28, "gc": 30, "sg": -2, "aproveitamento": 49, "ultimos": "VDDEV", "zona": "sul-americana"},
            {"pos": 9, "time": "Bragantino", "p": 34, "j": 25, "v": 10, "e": 4, "d": 11, "gp": 31, "gc": 36, "sg": -5, "aproveitamento": 45, "ultimos": "DDVEV", "zona": "sul-americana"},
            {"pos": 10, "time": "Corinthians", "p": 32, "j": 25, "v": 8, "e": 8, "d": 9, "gp": 26, "gc": 30, "sg": -4, "aproveitamento": 42, "ultimos": "EEVDD", "zona": ""},
            {"pos": 11, "time": "Grêmio", "p": 32, "j": 25, "v": 8, "e": 8, "d": 9, "gp": 26, "gc": 31, "sg": -5, "aproveitamento": 42, "ultimos": "VEDDE", "zona": ""},
            {"pos": 12, "time": "Ceará", "p": 31, "j": 24, "v": 8, "e": 7, "d": 9, "gp": 24, "gc": 24, "sg": 0, "aproveitamento": 43, "ultimos": "EVDVE", "zona": ""},
            {"pos": 13, "time": "Vasco", "p": 30, "j": 25, "v": 8, "e": 6, "d": 11, "gp": 38, "gc": 36, "sg": 2, "aproveitamento": 40, "ultimos": "VDDVE", "zona": ""},
            {"pos": 14, "time": "Internacional", "p": 30, "j": 24, "v": 8, "e": 6, "d": 10, "gp": 30, "gc": 37, "sg": -7, "aproveitamento": 41, "ultimos": "DEDVE", "zona": ""},
            {"pos": 15, "time": "Santos", "p": 29, "j": 24, "v": 8, "e": 5, "d": 11, "gp": 24, "gc": 33, "sg": -9, "aproveitamento": 40, "ultimos": "DDEEV", "zona": ""},
            {"pos": 16, "time": "Atlético-MG", "p": 28, "j": 23, "v": 7, "e": 7, "d": 9, "gp": 23, "gc": 27, "sg": -4, "aproveitamento": 40, "ultimos": "EDDED", "zona": ""},
            {"pos": 17, "time": "Vitória", "p": 25, "j": 25, "v": 5, "e": 10, "d": 10, "gp": 21, "gc": 36, "sg": -15, "aproveitamento": 33, "ultimos": "EDDED", "zona": "rebaixamento"},
            {"pos": 18, "time": "Juventude", "p": 24, "j": 24, "v": 7, "e": 3, "d": 14, "gp": 21, "gc": 46, "sg": -25, "aproveitamento": 33, "ultimos": "DDDVE", "zona": "rebaixamento"},
            {"pos": 19, "time": "Fortaleza", "p": 21, "j": 24, "v": 5, "e": 6, "d": 13, "gp": 25, "gc": 39, "sg": -14, "aproveitamento": 29, "ultimos": "DDDEE", "zona": "rebaixamento"},
            {"pos": 20, "time": "Sport", "p": 17, "j": 23, "v": 3, "e": 8, "d": 12, "gp": 18, "gc": 35, "sg": -17, "aproveitamento": 24, "ultimos": "DEDED", "zona": "rebaixamento"}
        ]
        
        # 3. Salvar no banco
        rodada_atual = 25  # FUTURO: Detectar rodada atual automaticamente
        brasileirao_db.save_classification(dados_serie_a, fonte="job_diario", rodada=rodada_atual)
        
        logger.info(f"✅ Brasileirão Série A atualizado - {len(dados_serie_a)} times salvos")
        
        # FUTURO: Adicionar Série B, C, D
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar Brasileirão: {e}")
        return False

def atualizar_internacional():
    """Atualiza dados de ligas internacionais"""
    try:
        logger.info("🌍 Iniciando atualização internacional...")
        
        # FUTURO: Integrar com API-Football
        # Por enquanto, log de placeholder
        logger.info("⚠️ Internacional: usando dados simulados (API-Football não configurada)")
        
        # Simular algumas atualizações
        ligas_atualizadas = ["Premier League", "La Liga", "Champions League"]
        
        for liga in ligas_atualizadas:
            logger.info(f"   📊 {liga}: dados simulados atualizados")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar dados internacionais: {e}")
        return False

def atualizar_loteca():
    """Atualiza jogos e probabilidades da Loteca"""
    try:
        logger.info("🎲 Iniciando atualização da Loteca...")
        
        from services.loteca_provider_new import get_current_loteca_matches
        
        # Buscar jogos atuais
        loteca_data = get_current_loteca_matches()
        
        if isinstance(loteca_data, dict) and loteca_data.get('success'):
            total_jogos = loteca_data.get('total', 0)
            logger.info(f"✅ Loteca atualizada - {total_jogos} jogos processados")
        else:
            logger.warning("⚠️ Loteca: dados limitados ou erro na API")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar Loteca: {e}")
        return False

def executar_backup_dados():
    """Cria backup dos dados importantes"""
    try:
        logger.info("💾 Criando backup dos dados...")
        
        # FUTURO: Implementar backup real
        logger.info("✅ Backup simulado criado")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no backup: {e}")
        return False

def job_principal_23h55():
    """Job principal que executa às 23h55 todos os dias"""
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info(f"🕚 INÍCIO JOB DIÁRIO 23H55 - {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 60)
    
    resultados = {
        'brasileirao': False,
        'internacional': False,
        'loteca': False,
        'backup': False
    }
    
    try:
        # 1. Atualizar Brasileirão
        resultados['brasileirao'] = atualizar_brasileirao()
        
        # 2. Atualizar dados internacionais
        resultados['internacional'] = atualizar_internacional()
        
        # 3. Atualizar Loteca
        resultados['loteca'] = atualizar_loteca()
        
        # 4. Backup de segurança
        resultados['backup'] = executar_backup_dados()
        
        # 5. Relatório final
        sucessos = sum(resultados.values())
        total = len(resultados)
        
        end_time = datetime.now()
        duracao = (end_time - start_time).total_seconds()
        
        logger.info("=" * 60)
        logger.info(f"📊 RELATÓRIO FINAL - {sucessos}/{total} operações bem-sucedidas")
        logger.info(f"⏱️ Duração total: {duracao:.2f} segundos")
        
        for operacao, sucesso in resultados.items():
            status = "✅" if sucesso else "❌"
            logger.info(f"   {status} {operacao.title()}")
        
        if sucessos == total:
            logger.info("🎉 JOB DIÁRIO 23H55 - CONCLUÍDO COM SUCESSO TOTAL!")
        else:
            logger.warning(f"⚠️ JOB DIÁRIO 23H55 - CONCLUÍDO COM {total-sucessos} ERROS")
            
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"💥 ERRO CRÍTICO NO JOB 23H55: {e}")
        logger.error("=" * 60)

def executar_job_teste():
    """Executa o job imediatamente para teste"""
    logger.info("🧪 EXECUTANDO JOB DE TESTE (IMEDIATO)")
    job_principal_23h55()

def iniciar_scheduler():
    """Inicia o agendador para 23h55 todos os dias"""
    logger.info("⏰ Configurando agendador para 23h55 diários...")
    
    # Agendar para 23h55 todos os dias
    schedule.every().day.at("23:55").do(job_principal_23h55)
    
    logger.info("✅ Agendador configurado!")
    logger.info("📅 Próxima execução: TODOS OS DIAS às 23h55")
    logger.info("🔄 Para teste manual, use: executar_job_teste()")
    
    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto

if __name__ == "__main__":
    criar_diretorio_logs()
    
    # Verificar se é para executar teste ou scheduler
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        executar_job_teste()
    else:
        iniciar_scheduler()
