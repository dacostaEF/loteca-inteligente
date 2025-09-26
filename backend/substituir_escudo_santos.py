#!/usr/bin/env python3
"""
SUBSTITUIR ESCUDO DO SANTOS
Substitui o escudo atual do Santos pelo novo, redimensionando para manter o layout
"""

import os
from PIL import Image

def substituir_escudo_santos():
    """Substitui e redimensiona o novo escudo do Santos"""
    
    print("🔄 Substituindo escudo do Santos...")
    
    # Caminhos
    pasta_santos = "static/escudos/SAN_Santos"
    novo_escudo = os.path.join(pasta_santos, "Santos.png")
    
    # Verificar se o novo arquivo existe
    if not os.path.exists(novo_escudo):
        print(f"❌ Arquivo {novo_escudo} não encontrado!")
        return
    
    print(f"✅ Novo escudo encontrado: {novo_escudo}")
    
    try:
        # Abrir a nova imagem
        img = Image.open(novo_escudo)
        print(f"📏 Tamanho original: {img.size}")
        
        # Redimensionar para os tamanhos padrão
        tamanhos = {
            "30x30.png": (30, 30),
            "45x45.png": (45, 45), 
            "60x60.png": (60, 60)
        }
        
        for nome_arquivo, tamanho in tamanhos.items():
            # Redimensionar mantendo qualidade
            img_redimensionada = img.resize(tamanho, Image.Resampling.LANCZOS)
            
            # Salvar substituindo o arquivo antigo
            caminho_destino = os.path.join(pasta_santos, nome_arquivo)
            img_redimensionada.save(caminho_destino, "PNG", optimize=True)
            
            print(f"✅ {nome_arquivo} → {tamanho} salvo")
        
        print(f"\n🎉 Escudo do Santos substituído com sucesso!")
        print(f"📊 Mantido o tamanho visual no layout")
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        print("💡 Certifique-se de ter o Pillow instalado: pip install Pillow")

if __name__ == "__main__":
    substituir_escudo_santos()
