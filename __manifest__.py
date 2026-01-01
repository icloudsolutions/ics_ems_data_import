{
    'name': 'ICS EMS Data Import',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Import legacy data into staging tables for migration to EMS',
    'description': """
ICS Education Management System - Data Import Module
====================================================

This module provides tools to import raw data from Excel files into staging tables,
allowing verification and controlled migration to the EMS system.

Features:
---------
* Import raw Excel data without transformation
* Staging tables with full data visibility
* Column totals and row counts for verification
* Prevent duplicate imports
* Update existing records
* Controlled migration to EMS tables
* Support for repeated imports with updated data

Supported Imports:
------------------
* Student Balance Data
* Fee Structure Data
    """,
    'author': 'ICS - iCloud Solutions',
    'website': 'https://icloudsolutions.sa',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'ics_ems_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/student_balance_staging_views.xml',
        'views/fee_staging_views.xml',
        'wizard/import_student_balance_views.xml',
        'wizard/import_fees_views.xml',
        'wizard/migrate_student_balance_views.xml',
        'wizard/migrate_fees_views.xml',
    ],
    'external_dependencies': {
        'python': ['openpyxl'],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
