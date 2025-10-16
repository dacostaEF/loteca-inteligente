#!/usr/bin/env python3
"""
Script para corrigir URLs quebradas no arquivo loteca.html
"""

import re

def corrigir_urls_quebradas():
    """Corrige todas as URLs quebradas no arquivo loteca.html"""
    
    arquivo = "templates/loteca.html"
    
    try:
        # Ler o arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        print(f"📁 Arquivo lido: {arquivo}")
        print(f"📊 Tamanho original: {len(conteudo)} caracteres")
        
        # Padrão para encontrar URLs quebradas
        # placeholder-team-logo.svg"caminho/arquivo.png"
        padrao_quebrado = r'src="/static/placeholder-team-logo\.svg"[^"]*\.png"'
        
        # Encontrar todas as ocorrências
        ocorrencias = re.findall(padrao_quebrado, conteudo)
        print(f"🔍 URLs quebradas encontradas: {len(ocorrencias)}")
        
        if ocorrencias:
            print("\n📋 URLs quebradas encontradas:")
            for i, url in enumerate(ocorrencias[:10], 1):  # Mostrar apenas as primeiras 10
                print(f"  {i}. {url}")
            
            if len(ocorrencias) > 10:
                print(f"  ... e mais {len(ocorrencias) - 10} URLs")
        
        # Substituir todas as URLs quebradas por placeholder simples
        conteudo_corrigido = re.sub(padrao_quebrado, 'src="/static/placeholder-team-logo.svg"', conteudo)
        
        # Verificar se houve mudanças
        if conteudo != conteudo_corrigido:
            # Salvar o arquivo corrigido
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_corrigido)
            
            print(f"\n✅ Arquivo corrigido com sucesso!")
            print(f"📊 Tamanho final: {len(conteudo_corrigido)} caracteres")
            print(f"🔧 URLs corrigidas: {len(ocorrencias)}")
        else:
            print("\n✅ Nenhuma URL quebrada encontrada!")
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {arquivo}")
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando correção de URLs quebradas...")
    corrigir_urls_quebradas()
    print("🎯 Correção concluída!")

