#!/usr/bin/env python3
"""
TESTE DA FASE 1: UNIFICAÇÃO DE MAPEAMENTOS
Valida se todas as abas do site usam o mesmo sistema de clubes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_fase1_unificacao():
    """Testa a unificação de mapeamentos da Fase 1"""
    
    print("🧪 TESTE FASE 1: UNIFICAÇÃO DE MAPEAMENTOS")
    print("=" * 50)
    
    # 1. Testar sistema unificado
    print("\n1️⃣ TESTE DO SISTEMA UNIFICADO:")
    try:
        from services.clubes_unificados import clubes_unificados
        
        # Diagnóstico completo
        relatorio = clubes_unificados.diagnostico_completo()
        print(relatorio)
        
        # Validação
        validacao = clubes_unificados.validar_mapeamento()
        if validacao['valido']:
            print("\n✅ Sistema unificado: VÁLIDO")
        else:
            print("\n❌ Sistema unificado: PROBLEMAS ENCONTRADOS")
            for tipo, items in validacao['duplicatas'].items():
                if items:
                    print(f"   - {tipo}: {items}")
    
    except Exception as e:
        print(f"❌ Erro no sistema unificado: {e}")
        return False
    
    # 2. Testar integração com Cartola Provider
    print("\n2️⃣ TESTE INTEGRAÇÃO CARTOLA PROVIDER:")
    try:
        from services.cartola_provider import get_clube_mappings, get_clube_id_by_name
        
        # Testar mapeamento
        mappings = get_clube_mappings()
        print(f"✅ Mapeamentos carregados: {len(mappings)} clubes")
        
        # Testar buscas específicas
        testes = [
            ('flamengo', 262),
            ('Mengão', 262),
            ('FLA', 262),
            ('palmeiras', 275),
            ('Verdão', 275),
            ('corinthians', 264),
            ('Timão', 264)
        ]
        
        sucessos = 0
        for nome, id_esperado in testes:
            id_obtido = get_clube_id_by_name(nome)
            if id_obtido == id_esperado:
                print(f"   ✅ {nome} → {id_obtido}")
                sucessos += 1
            else:
                print(f"   ❌ {nome} → {id_obtido} (esperado: {id_esperado})")
        
        print(f"\n📊 Testes de busca: {sucessos}/{len(testes)} sucessos")
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False
    
    # 3. Testar compatibilidade com APIs
    print("\n3️⃣ TESTE COMPATIBILIDADE COM APIS:")
    try:
        from services.cartola_provider import health_check, clubes
        
        # Teste básico de conectividade
        health = health_check()
        if health.get('api_response'):
            print("✅ Cartola FC: Conectado")
        else:
            print("⚠️ Cartola FC: Indisponível (normal se sem token)")
        
        # Teste de clubes
        clubes_data = clubes()
        if clubes_data:
            print(f"✅ Dados de clubes: {len(clubes_data)} clubes")
        else:
            print("⚠️ Dados de clubes: Limitados")
            
    except Exception as e:
        print(f"⚠️ APIs indisponíveis: {e}")
    
    # 4. Testar nomes padronizados
    print("\n4️⃣ TESTE PADRONIZAÇÃO DE NOMES:")
    
    # Verificar se todos os times da Série A estão mapeados
    times_serie_a = [
        "Flamengo", "Palmeiras", "Cruzeiro", "Corinthians", "São Paulo",
        "Botafogo", "Fluminense", "Atlético-MG", "Internacional", "Grêmio",
        "Santos", "Vasco", "Bahia", "Ceará", "Fortaleza", "Bragantino",
        "Juventude", "Vitória", "Mirassol", "Sport"
    ]
    
    times_mapeados = 0
    for time in times_serie_a:
        id_clube = get_clube_id_by_name(time)
        if id_clube:
            times_mapeados += 1
            print(f"   ✅ {time}: ID {id_clube}")
        else:
            print(f"   ❌ {time}: NÃO MAPEADO")
    
    print(f"\n📊 Times mapeados: {times_mapeados}/{len(times_serie_a)}")
    
    # 5. Resultado final
    print("\n5️⃣ RESULTADO DA FASE 1:")
    print("-" * 30)
    
    if (validacao['valido'] and 
        sucessos >= len(testes) * 0.8 and  # 80% dos testes
        times_mapeados >= len(times_serie_a) * 0.9):  # 90% dos times
        
        print("🎉 FASE 1: UNIFICAÇÃO DE MAPEAMENTOS - SUCESSO!")
        print("✅ Sistema central funcionando")
        print("✅ Integração com providers OK")
        print("✅ Nomes padronizados")
        print("✅ Compatibilidade mantida")
        print("\n🚀 PRONTO PARA FASE 2!")
        return True
    else:
        print("⚠️ FASE 1: PROBLEMAS IDENTIFICADOS")
        print("🔧 Corrija os erros antes de prosseguir para Fase 2")
        return False

def test_coerencia_entre_abas():
    """Testa se todas as abas usam os mesmos nomes"""
    print("\n🔍 TESTE DE COERÊNCIA ENTRE ABAS:")
    
    # Simular dados das diferentes abas
    aba1_times = ["Flamengo", "Palmeiras", "Corinthians"]  # Da Loteca
    aba2_times = ["flamengo", "palmeiras", "corinthians"]  # Do Squad Health
    aba3_times = ["Flamengo", "Palmeiras", "Corinthians"]  # Do Panorama
    
    from services.clubes_unificados import clubes_unificados
    
    coerencia_total = True
    
    for i, (t1, t2, t3) in enumerate(zip(aba1_times, aba2_times, aba3_times)):
        id1 = clubes_unificados.get_id_cartola(t1)
        id2 = clubes_unificados.get_id_cartola(t2)
        id3 = clubes_unificados.get_id_cartola(t3)
        
        nome_oficial = clubes_unificados.get_nome_oficial(t1)
        
        if id1 == id2 == id3:
            print(f"   ✅ {nome_oficial}: Todas as abas usam ID {id1}")
        else:
            print(f"   ❌ {nome_oficial}: IDs inconsistentes - Aba1:{id1}, Aba2:{id2}, Aba3:{id3}")
            coerencia_total = False
    
    if coerencia_total:
        print("✅ COERÊNCIA TOTAL entre abas!")
    else:
        print("❌ Inconsistências detectadas entre abas")
    
    return coerencia_total

if __name__ == "__main__":
    sucesso_fase1 = test_fase1_unificacao()
    sucesso_coerencia = test_coerencia_entre_abas()
    
    print("\n" + "=" * 50)
    if sucesso_fase1 and sucesso_coerencia:
        print("🎯 FASE 1 CONCLUÍDA COM SUCESSO!")
        print("📝 Avaliação: Sistema unificado implementado e funcionando")
        print("🚀 Pode prosseguir para FASE 2")
    else:
        print("⚠️ FASE 1 PRECISA DE AJUSTES")
        print("🔧 Resolva os problemas antes da Fase 2")
