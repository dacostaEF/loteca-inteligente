#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Encontrar await problemático
"""

def find_await_problems():
    """Encontrar await problemático"""
    print("Procurando await problemático...")
    
    with open('backend/admin_interface.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== PROCURANDO AWAIT PROBLEMATICO ===")
    
    # Procurar por await que não está dentro de função async
    for i, line in enumerate(lines):
        if 'await ' in line:
            # Verificar se está dentro de uma função async
            is_inside_async = False
            
            # Procurar para trás até encontrar uma função
            for j in range(i-1, max(0, i-100), -1):
                if 'async function' in lines[j]:
                    is_inside_async = True
                    break
                elif 'function ' in lines[j] and 'async function' not in lines[j]:
                    break
            
            if not is_inside_async:
                print(f"ERRO na linha {i+1}: {line.strip()}")
                
                # Mostrar contexto
                print("Contexto:")
                for k in range(max(0, i-3), min(len(lines), i+4)):
                    marker = ">>> " if k == i else "    "
                    print(f"{marker}{k+1}: {lines[k].strip()}")
                print()

if __name__ == "__main__":
    find_await_problems()
