#!/usr/bin/env python3
"""
Script para testar o job diário localmente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from jobs.daily_updater import executar_job_teste, job_principal_23h55
from models.brasileirao_db import brasileirao_db

def main():
    print("🧪 TESTE DO JOB DIÁRIO LOTECA X-RAY")
    print("=" * 50)
    
    # 1. Status antes do teste
    print("\n1️⃣ STATUS ANTES DO TESTE:")
    data_age = brasileirao_db.get_data_age()
    is_fresh = brasileirao_db.is_data_fresh()
    
    print(f"📊 Idade dos dados: {data_age or 'Nenhum dado'}")
    print(f"🔄 Dados frescos: {is_fresh}")
    
    # 2. Executar job de teste
    print("\n2️⃣ EXECUTANDO JOB DE TESTE:")
    print("-" * 30)
    
    executar_job_teste()
    
    # 3. Status após o teste
    print("\n3️⃣ STATUS APÓS O TESTE:")
    new_age = brasileirao_db.get_data_age()
    new_fresh = brasileirao_db.is_data_fresh()
    latest_data = brasileirao_db.get_latest_classification()
    
    print(f"📊 Nova idade: {new_age or 'Nenhum dado'}")
    print(f"🔄 Agora frescos: {new_fresh}")
    print(f"📈 Times no banco: {len(latest_data) if latest_data else 0}")
    
    if latest_data:
        print("\n🏆 TOP 5 APÓS ATUALIZAÇÃO:")
        for i, team in enumerate(latest_data[:5], 1):
            print(f"   {i}º {team['time']} - {team['p']} pts - {team['ultimos']}")
    
    print("\n✅ TESTE CONCLUÍDO!")
    print("🎯 Para produção: o job rodará automaticamente às 23h55")

if __name__ == "__main__":
    main()
