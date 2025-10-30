#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para verificar todas as importações
"""

print("=" * 60)
print("VERIFICAÇÃO COMPLETA DE IMPLEMENTAÇÃO")
print("=" * 60)
print()

errors = []
success = []

# Teste 1: Importar global_search
print("1. Testando global_search.py...")
try:
    from cattle_management.ui.global_search import GlobalSearch
    success.append("✓ global_search.py - GlobalSearch importado")
except Exception as e:
    errors.append(f"✗ global_search.py - ERRO: {str(e)}")

# Teste 2: Importar financial_dashboard
print("2. Testando financial_dashboard.py...")
try:
    from cattle_management.ui.financial_dashboard import FinancialDashboard
    success.append("✓ financial_dashboard.py - FinancialDashboard importado")
except Exception as e:
    errors.append(f"✗ financial_dashboard.py - ERRO: {str(e)}")

# Teste 3: Importar alerts_reminders
print("3. Testando alerts_reminders.py...")
try:
    from cattle_management.ui.alerts_reminders import AlertsReminders
    success.append("✓ alerts_reminders.py - AlertsReminders importado")
except Exception as e:
    errors.append(f"✗ alerts_reminders.py - ERRO: {str(e)}")

# Teste 4: Importar cash_flow_projection
print("4. Testando cash_flow_projection.py...")
try:
    from cattle_management.ui.cash_flow_projection import CashFlowProjection
    success.append("✓ cash_flow_projection.py - CashFlowProjection importado")
except Exception as e:
    errors.append(f"✗ cash_flow_projection.py - ERRO: {str(e)}")

# Teste 5: Importar main_window e verificar métodos
print("5. Testando main_window.py...")
try:
    from cattle_management.ui.main_window import MainWindow

    # Verificar se métodos existem
    methods_to_check = [
        'open_global_search',
        'open_financial_dashboard',
        'open_alerts',
        'open_cash_flow',
        'setup_keyboard_shortcuts'
    ]

    for method in methods_to_check:
        if hasattr(MainWindow, method):
            success.append(f"✓ main_window.py - Método {method}() existe")
        else:
            errors.append(f"✗ main_window.py - Método {method}() NÃO EXISTE")

except Exception as e:
    errors.append(f"✗ main_window.py - ERRO: {str(e)}")

print()
print("=" * 60)
print("RESULTADOS")
print("=" * 60)
print()

if success:
    print("✅ SUCESSOS:")
    for s in success:
        print(f"  {s}")
    print()

if errors:
    print("❌ ERROS:")
    for e in errors:
        print(f"  {e}")
    print()
else:
    print("🎉 NENHUM ERRO ENCONTRADO!")
    print()

print("=" * 60)
print(f"Total de Verificações: {len(success) + len(errors)}")
print(f"Sucessos: {len(success)}")
print(f"Erros: {len(errors)}")
print("=" * 60)

# Exit code
import sys
sys.exit(0 if len(errors) == 0 else 1)
