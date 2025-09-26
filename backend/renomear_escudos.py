#!/usr/bin/env python3
"""
RENOMEAR ESCUDOS PARA IDENTIFICAÇÃO FÁCIL
Renomeia as pastas dos escudos de códigos para formato: CODIGO_Nome-do-Time
"""

import os
import shutil
from services.cartola_provider import clubes

def identificar_e_renomear_escudos():
    """Renomeia as pastas dos escudos para facilitar identificação"""
    
    print("🔄 Iniciando renomeação dos escudos...")
    
    escudos_dir = "static/escudos"
    
    # Buscar todos os clubes do Cartola FC
    todos_clubes = clubes()
    print(f"📊 {len(todos_clubes)} clubes encontrados no Cartola FC")
    
    # Criar mapeamento código -> nome
    codigo_para_nome = {}
    for clube_id, clube_data in todos_clubes.items():
        abrev = clube_data.get('abreviacao', '').upper()
        nome = clube_data.get('nome', '').replace(' ', '-')
        nome_fantasia = clube_data.get('nome_fantasia', '').replace(' ', '-')
        
        # Usar nome_fantasia se disponível, senão nome
        nome_final = nome_fantasia if nome_fantasia else nome
        
        if abrev and nome_final:
            codigo_para_nome[abrev] = nome_final
            print(f"📋 {abrev} → {nome_final}")
    
    print(f"\n🎯 Mapeamento criado para {len(codigo_para_nome)} times")
    
    # Listar pastas atuais
    if not os.path.exists(escudos_dir):
        print(f"❌ Pasta {escudos_dir} não encontrada!")
        return
    
    pastas_atuais = [d for d in os.listdir(escudos_dir) 
                     if os.path.isdir(os.path.join(escudos_dir, d))]
    
    print(f"\n📁 {len(pastas_atuais)} pastas encontradas:")
    
    renamed_count = 0
    not_found_count = 0
    
    for pasta in sorted(pastas_atuais):
        pasta_path = os.path.join(escudos_dir, pasta)
        
        if pasta in codigo_para_nome:
            # Renomear pasta
            novo_nome = f"{pasta}_{codigo_para_nome[pasta]}"
            novo_path = os.path.join(escudos_dir, novo_nome)
            
            try:
                if not os.path.exists(novo_path):
                    shutil.move(pasta_path, novo_path)
                    print(f"✅ {pasta} → {novo_nome}")
                    renamed_count += 1
                else:
                    print(f"⚠️ {novo_nome} já existe, pulando...")
            except Exception as e:
                print(f"❌ Erro ao renomear {pasta}: {e}")
                
        else:
            print(f"❓ {pasta} - time não identificado")
            not_found_count += 1
    
    print(f"\n🎉 Renomeação concluída!")
    print(f"✅ Renomeados: {renamed_count}")
    print(f"❓ Não identificados: {not_found_count}")
    
    # Mostrar times não identificados para investigação manual
    if not_found_count > 0:
        print(f"\n🔍 Times não identificados:")
        for pasta in sorted(pastas_atuais):
            if pasta not in codigo_para_nome:
                print(f"   - {pasta}")

if __name__ == "__main__":
    identificar_e_renomear_escudos()
