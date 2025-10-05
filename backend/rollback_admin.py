#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para fazer rollback da Central Admin
"""

def rollback_admin():
    """Fazer rollback da Central Admin"""
    print("Fazendo rollback da Central Admin...")
    
    # Verificar se existe backup
    import os
    if not os.path.exists('backend/admin_interface.html.backup'):
        print("ERRO: Backup nao encontrado!")
        return False
    
    # Restaurar backup
    with open('backend/admin_interface.html.backup', 'r', encoding='utf-8') as f:
        backup_content = f.read()
    
    with open('backend/admin_interface.html', 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    print("Rollback aplicado com sucesso!")
    return True

if __name__ == "__main__":
    print("=== ROLLBACK DA CENTRAL ADMIN ===")
    
    success = rollback_admin()
    
    if success:
        print("\nSUCESSO: Rollback aplicado!")
        print("Central Admin restaurada para versao funcional.")
        print("\nReinicie o servidor para aplicar o rollback.")
    else:
        print("\nERRO: Falha no rollback!")
