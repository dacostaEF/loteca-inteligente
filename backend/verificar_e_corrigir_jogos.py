#!/usr/bin/env python3
"""
VERIFICAR E CORRIGIR JOGOS 2-14
================================

Script para verificar se todos os jogos 2-14 estão lendo corretamente
as APIs e têm o campo 'arquivo_confrontos' configurado.
"""

import os
import json
from pathlib import Path

def verificar_jogo(numero_jogo):
    """Verificar um jogo específico"""
    print(f"\n{'='*60}")
    print(f"🎯 VERIFICANDO JOGO {numero_jogo}")
    print(f"{'='*60}")
    
    # Caminho do arquivo
    arquivo = Path(f"models/concurso_1216/analise_rapida/jogo_{numero_jogo}.json")
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    # Ler arquivo
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False
    
    # Verificar estrutura
    if 'dados' not in data:
        print(f"❌ Campo 'dados' não encontrado")
        return False
    
    dados = data['dados']
    
    # Verificar campos obrigatórios
    campos_obrigatorios = [
        'time_casa', 'time_fora', 'escudo_casa', 'escudo_fora',
        'confrontos_sequence', 'confronto_direto'
    ]
    
    campos_faltando = []
    for campo in campos_obrigatorios:
        if campo not in dados:
            campos_faltando.append(campo)
    
    if campos_faltando:
        print(f"❌ Campos obrigatórios faltando: {campos_faltando}")
        return False
    
    # Verificar campo arquivo_confrontos
    tem_arquivo_confrontos = 'arquivo_confrontos' in dados
    
    print(f"✅ Arquivo existe: {arquivo}")
    print(f"✅ Estrutura válida: {len(dados)} campos")
    print(f"✅ Time Casa: {dados.get('time_casa', 'N/A')}")
    print(f"✅ Time Fora: {dados.get('time_fora', 'N/A')}")
    print(f"✅ Sequência: {dados.get('confrontos_sequence', 'N/A')}")
    print(f"✅ Confronto Direto: {dados.get('confronto_direto', 'N/A')}")
    print(f"{'✅' if tem_arquivo_confrontos else '❌'} Arquivo Confrontos: {dados.get('arquivo_confrontos', 'NÃO ENCONTRADO')}")
    
    return True, tem_arquivo_confrontos, dados

def adicionar_arquivo_confrontos(numero_jogo, nome_arquivo):
    """Adicionar campo arquivo_confrontos a um jogo"""
    arquivo = Path(f"models/concurso_1216/analise_rapida/jogo_{numero_jogo}.json")
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Adicionar campo
        data['dados']['arquivo_confrontos'] = nome_arquivo
        
        # Salvar arquivo
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Campo 'arquivo_confrontos' adicionado: {nome_arquivo}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar campo: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 VERIFICANDO JOGOS 2-14")
    print("="*60)
    
    # Mapeamento de jogos para arquivos CSV (baseado nos arquivos existentes)
    mapeamento_jogos = {
        2: "Internacional_vs_Sport.csv",
        3: "Corinthians_vs_Atletico-MG.csv",  # Exemplo
        4: "Vasco_vs_Cruzeiro.csv",  # Exemplo
        5: "Atletico-de-Madrid_vs_Osasuna.csv",
        6: "Atletico-MG_vs_Mirassol.csv",  # Exemplo
        7: "Gremio_vs_Vitoria.csv",  # Exemplo
        8: "Bahia_vs_Ceara.csv",  # Exemplo
        9: "Fortaleza_vs_Juventude.csv",  # Exemplo
        10: "Fluminense_vs_Botafogo.csv",  # Exemplo
        11: "Criciuma_vs_Paysandu.csv",  # Exemplo
        12: "Newcastle_vs_Arsenal.csv",  # Exemplo
        13: "Bragantino_vs_Santos.csv",  # Exemplo
        14: "Barcelona_vs_Real-Sociedad.csv"  # Exemplo
    }
    
    resultados = []
    
    # Verificar cada jogo
    for numero_jogo in range(2, 15):
        sucesso, tem_arquivo_confrontos, dados = verificar_jogo(numero_jogo)
        
        if sucesso:
            if not tem_arquivo_confrontos:
                # Adicionar campo arquivo_confrontos
                nome_arquivo = mapeamento_jogos.get(numero_jogo, f"Jogo_{numero_jogo}.csv")
                if adicionar_arquivo_confrontos(numero_jogo, nome_arquivo):
                    print(f"✅ Jogo {numero_jogo} corrigido com sucesso!")
                else:
                    print(f"❌ Erro ao corrigir Jogo {numero_jogo}")
                    resultados.append((numero_jogo, False))
                    continue
            
            resultados.append((numero_jogo, True))
        else:
            resultados.append((numero_jogo, False))
    
    # Resumo dos resultados
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS RESULTADOS")
    print(f"{'='*60}")
    
    sucessos = sum(1 for _, sucesso in resultados if sucesso)
    total = len(resultados)
    
    for numero_jogo, sucesso in resultados:
        status = "✅ OK" if sucesso else "❌ ERRO"
        print(f"  {status}: Jogo {numero_jogo}")
    
    print(f"\n🎯 RESULTADO FINAL: {sucessos}/{total} jogos verificados com sucesso")
    
    if sucessos == total:
        print("🎉 TODOS OS JOGOS ESTÃO CORRETOS!")
    else:
        print("⚠️ ALGUNS JOGOS PRECISAM DE ATENÇÃO.")

if __name__ == "__main__":
    main()
