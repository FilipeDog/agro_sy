#!/usr/bin/env python3
"""
Script to update imports from old structure to new structure
"""

import os
import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_MAPPINGS = {
    # Database imports
    r'from cattle_management\.database\.db_manager import': 'from agrogestor.core.database.db_manager import',
    r'from cattle_management\.database\.migrate_database import': 'from agrogestor.core.database.migrate_database import',
    r'import cattle_management\.database\.db_manager': 'import agrogestor.core.database.db_manager',

    # Utils imports
    r'from cattle_management\.utils\.validators import': 'from agrogestor.utils.validators import',
    r'from cattle_management\.utils\.logger import': 'from agrogestor.utils.logger import',
    r'from cattle_management\.utils\.calculator import': 'from agrogestor.utils.calculator import',
    r'from cattle_management\.utils\.theme_manager import': 'from agrogestor.utils.theme_manager import',
    r'from cattle_management\.utils\.backup_manager import': 'from agrogestor.utils.backup_manager import',
    r'from cattle_management\.utils\.excel_importer import': 'from agrogestor.utils.excel_importer import',
    r'from cattle_management\.utils\.ui_helpers import': 'from agrogestor.utils.ui_helpers import',

    # Cattle UI imports
    r'from cattle_management\.ui\.animals_register import': 'from agrogestor.modules.cattle.animals_register import',
    r'from cattle_management\.ui\.weight_control import': 'from agrogestor.modules.cattle.weight_control import',
    r'from cattle_management\.ui\.inseminations import': 'from agrogestor.modules.cattle.inseminations import',
    r'from cattle_management\.ui\.applications import': 'from agrogestor.modules.cattle.applications import',

    # Agriculture UI imports
    r'from cattle_management\.ui\.talhoes_register import': 'from agrogestor.modules.agriculture.talhoes_register import',
    r'from cattle_management\.ui\.tratos_culturais import': 'from agrogestor.modules.agriculture.tratos_culturais import',
    r'from cattle_management\.ui\.colheitas_banana import': 'from agrogestor.modules.agriculture.colheitas_banana import',

    # Financial UI imports
    r'from cattle_management\.ui\.expenses import': 'from agrogestor.modules.financial.expenses import',
    r'from cattle_management\.ui\.revenues import': 'from agrogestor.modules.financial.revenues import',
    r'from cattle_management\.ui\.bank_accounts import': 'from agrogestor.modules.financial.bank_accounts import',
    r'from cattle_management\.ui\.financial_dashboard import': 'from agrogestor.modules.financial.financial_dashboard import',
    r'from cattle_management\.ui\.cash_flow_projection import': 'from agrogestor.modules.financial.cash_flow_projection import',

    # People UI imports
    r'from cattle_management\.ui\.employees_register import': 'from agrogestor.modules.people.employees_register import',
    r'from cattle_management\.ui\.users_management import': 'from agrogestor.modules.people.users_management import',
    r'from cattle_management\.ui\.clients_register import': 'from agrogestor.modules.people.clients_register import',
    r'from cattle_management\.ui\.suppliers_register import': 'from agrogestor.modules.people.suppliers_register import',

    # Inventory UI imports
    r'from cattle_management\.ui\.inventory import': 'from agrogestor.modules.inventory.inventory import',

    # Main UI imports
    r'from cattle_management\.ui\.login import': 'from agrogestor.ui.login import',
    r'from cattle_management\.ui\.main_window import': 'from agrogestor.ui.main_window import',

    # Dashboards
    r'from cattle_management\.ui\.welcome_screen import': 'from agrogestor.ui.dashboards.welcome_screen import',
    r'from cattle_management\.ui\.dashboard import': 'from agrogestor.ui.dashboards.dashboard import',
    r'from cattle_management\.ui\.dashboard_banana import': 'from agrogestor.ui.dashboards.dashboard_banana import',

    # Reports
    r'from cattle_management\.ui\.reports_window import': 'from agrogestor.ui.reports.reports_window import',

    # Shared UI
    r'from cattle_management\.ui\.generic_register import': 'from agrogestor.ui.shared.generic_register import',
    r'from cattle_management\.ui\.global_search import': 'from agrogestor.ui.shared.global_search import',
    r'from cattle_management\.ui\.alerts_reminders import': 'from agrogestor.ui.shared.alerts_reminders import',
}

def update_imports_in_file(file_path):
    """Update imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply all mappings
        for old_pattern, new_import in IMPORT_MAPPINGS.items():
            content = re.sub(old_pattern, new_import, content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to update all Python files"""
    agrogestor_dir = Path('/home/user/agro_sy/agrogestor')

    if not agrogestor_dir.exists():
        print(f"Directory {agrogestor_dir} not found!")
        return

    # Find all Python files
    python_files = list(agrogestor_dir.rglob('*.py'))

    print(f"Found {len(python_files)} Python files")

    updated_count = 0
    for file_path in python_files:
        if update_imports_in_file(file_path):
            print(f"Updated: {file_path.relative_to(agrogestor_dir)}")
            updated_count += 1

    print(f"\nTotal files updated: {updated_count}/{len(python_files)}")

if __name__ == '__main__':
    main()
