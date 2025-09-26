#!/usr/bin/env python3
"""
DOWNLOAD DOS ESCUDOS DOS TIMES
Baixa todos os escudos dos clubes do Cartola FC para pasta local
"""

import os
import requests
from services.cartola_provider import clubes
import time

def download_escudos():
    """Baixa todos os escudos dos times do Cartola FC"""
    
    print("🔽 Iniciando download dos escudos...")
    
    # Criar pasta se não existir
    escudos_dir = "static/escudos"
    os.makedirs(escudos_dir, exist_ok=True)
    
    # Buscar todos os clubes
    todos_clubes = clubes()
    print(f"📊 Encontrados {len(todos_clubes)} clubes")
    
    sucessos = 0
    erros = 0
    
    for clube_id, clube_data in todos_clubes.items():
        nome = clube_data.get('nome', f'clube_{clube_id}')
        abrev = clube_data.get('abreviacao', nome[:3]).upper()
        escudos = clube_data.get('escudos', {})
        
        print(f"\n🏟️ Processando: {nome} ({abrev})")
        
        # Criar pasta do clube
        clube_dir = os.path.join(escudos_dir, abrev)
        os.makedirs(clube_dir, exist_ok=True)
        
        # Baixar cada tamanho de escudo
        for tamanho, url in escudos.items():
            if url:
                try:
                    print(f"  📥 Baixando {tamanho}...")
                    
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    # Salvar arquivo
                    filename = f"{tamanho}.png"
                    filepath = os.path.join(clube_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"  ✅ {tamanho} salvo")
                    sucessos += 1
                    
                    # Pausa para não sobrecarregar o servidor
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  ❌ Erro ao baixar {tamanho}: {e}")
                    erros += 1
    
    print(f"\n🎉 Download concluído!")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📁 Escudos salvos em: {escudos_dir}")

if __name__ == "__main__":
    download_escudos()
