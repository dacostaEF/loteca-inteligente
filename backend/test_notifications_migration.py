#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testar migração do Sistema de Mensagens
"""

def test_notifications_migration():
    """Testar se a migração funcionou"""
    print("Testando migração do Sistema de Mensagens...")
    
    # Verificar se arquivo externo existe
    import os
    if os.path.exists('backend/static/js/ui/notifications.js'):
        print("OK: Arquivo externo existe: notifications.js")
        
        # Verificar conteúdo do arquivo
        with open('backend/static/js/ui/notifications.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'function mostrarSucesso' in content:
            print("OK: Função mostrarSucesso encontrada")
        else:
            print("ERRO: Função mostrarSucesso não encontrada")
            
        if 'function mostrarErro' in content:
            print("OK: Função mostrarErro encontrada")
        else:
            print("ERRO: Função mostrarErro não encontrada")
            
        if 'function mostrarNotificacao' in content:
            print("OK: Função mostrarNotificacao encontrada")
        else:
            print("ERRO: Função mostrarNotificacao não encontrada")
    else:
        print("ERRO: Arquivo externo não existe")
        return False
    
    # Verificar se referência foi adicionada ao HTML
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'notifications.js' in html_content:
        print("OK: Referência externa encontrada no HTML")
    else:
        print("ERRO: Referência externa não encontrada no HTML")
        return False
    
    # Verificar se funções foram removidas do HTML
    if 'function mostrarSucesso' not in html_content:
        print("OK: Funções removidas do HTML")
    else:
        print("ERRO: Funções ainda estão no HTML")
        return False
    
    print("\nMIGRAÇÃO TESTADA COM SUCESSO!")
    return True

if __name__ == "__main__":
    print("=== TESTE DA MIGRAÇÃO ===")
    
    success = test_notifications_migration()
    
    if success:
        print("\nSUCESSO: Migração funcionando!")
        print("Próximo passo: Testar no navegador")
    else:
        print("\nERRO: Migração com problemas!")
