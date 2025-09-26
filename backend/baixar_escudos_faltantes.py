#!/usr/bin/env python3
"""
BAIXAR ESCUDOS FALTANTES
Baixa especificamente os escudos dos times que estão incorretos ou faltando
"""

import os
import requests
from services.cartola_provider import clubes
import time

def baixar_escudos_especificos():
    """Baixa escudos específicos que estão faltando ou incorretos"""
    
    print("🔽 Baixando escudos faltantes...")
    
    # IDs específicos que precisamos
    times_corretos = {
        263: "BOT_Botafogo-RJ",      # Botafogo do Rio
        277: "SAN_Santos",           # Santos real  
        282: "CAM_Atletico-MG",      # Atlético-MG
        356: "FOR_Fortaleza"         # Fortaleza que faltou
    }
    
    escudos_dir = "static/escudos"
    todos_clubes = clubes()
    
    for clube_id, nome_pasta in times_corretos.items():
        if clube_id in todos_clubes:
            clube_data = todos_clubes[clube_id]
            nome = clube_data.get('nome_fantasia', f'Time_{clube_id}')
            escudos = clube_data.get('escudos', {})
            
            print(f"\n🏟️ Processando: {nome} → {nome_pasta}")
            
            # Criar pasta
            pasta_path = os.path.join(escudos_dir, nome_pasta)
            os.makedirs(pasta_path, exist_ok=True)
            
            # Baixar cada tamanho
            for tamanho, url in escudos.items():
                if url:
                    try:
                        print(f"  📥 Baixando {tamanho}...")
                        
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        
                        filename = f"{tamanho}.png"
                        filepath = os.path.join(pasta_path, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  ✅ {tamanho} salvo")
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f"  ❌ Erro ao baixar {tamanho}: {e}")
        else:
            print(f"❌ ID {clube_id} não encontrado")
    
    print(f"\n🎉 Download dos escudos faltantes concluído!")

if __name__ == "__main__":
    baixar_escudos_especificos()
