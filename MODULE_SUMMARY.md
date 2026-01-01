# ICS EMS Data Import Module - Summary

## Module Information

- **Module Name**: ics_ems_data_import
- **Version**: 19.0.1.0.0
- **Odoo Version**: 19.0
- **Category**: Education
- **Author**: ICS - iCloud Solutions
- **License**: LGPL-3
- **Depends**: base, ics_ems_core
- **External Dependencies**: openpyxl (Python library)

## Module Structure

```
ics_ems_data_import/
│
├── __init__.py                          # Main module initializer
├── __manifest__.py                      # Module manifest
│
├── models/                              # Data models
│   ├── __init__.py
│   ├── student_balance_staging.py       # Student balance staging table
│   └── fee_staging.py                   # Fee staging table
│
├── wizard/                              # Import and migration wizards
│   ├── __init__.py
│   ├── import_student_balance.py        # Import student balance from Excel
│   ├── import_fees.py                   # Import fees from Excel
│   ├── migrate_student_balance.py       # Migrate student balance to EMS
│   └── migrate_fees.py                  # Migrate fees to EMS
│
├── views/                               # XML views
│   ├── menu_views.xml                   # Menu structure
│   ├── student_balance_staging_views.xml # Student balance views
│   ├── fee_staging_views.xml            # Fee staging views
│   └── [wizard views]                   # Wizard form views (4 files)
│
├── security/                            # Access control
│   └── ir.model.access.csv              # Access rights for all models
│
├── static/                              # Static resources
│   └── description/
│       └── index.html                   # Module description page
│
└── Documentation Files
    ├── README.md                        # Complete documentation
    ├── INSTALLATION.md                  # Installation guide
    ├── USAGE_GUIDE.md                   # Quick usage guide
    └── MODULE_SUMMARY.md                # This file
```

## Models Created

### 1. ics.student.balance.staging
**Purpose**: Store raw student balance data from Excel imports

**Key Fields**:
- `import_batch` - Batch identifier
- `row_number` - Original row from Excel
- `col_01` to `col_25` - 25 flexible data columns
- `migrated` - Migration status flag
- `student_id` - Link to migrated student record
- `migration_log` - Detailed migration information

**Constraints**:
- Unique combination of import_batch + row_number

### 2. ics.fee.staging
**Purpose**: Store raw fee data from Excel imports

**Key Fields**:
- `import_batch` - Batch identifier
- `row_number` - Original row from Excel
- `col_01` to `col_30` - 30 flexible data columns
- `migrated` - Migration status flag
- `payslip_id` - Link to migrated payslip record
- `migration_log` - Detailed migration information

**Constraints**:
- Unique combination of import_batch + row_number

### 3. import.student.balance.wizard (Transient)
**Purpose**: Handle Excel file upload and import process

**Features**:
- Binary file upload
- Configurable sheet name
- Skip header rows option
- Update existing records option
- Import statistics and logging

### 4. import.fees.wizard (Transient)
**Purpose**: Handle fee Excel file upload and import

**Features**:
- Same as student balance wizard
- Supports up to 30 columns

### 5. migrate.student.balance.wizard (Transient)
**Purpose**: Migrate staging data to EMS student records

**Features**:
- Column mapping configuration
- Multiple migration modes
- Success/error tracking
- Detailed migration logs

### 6. migrate.fees.wizard (Transient)
**Purpose**: Migrate staging data to EMS payslip records

**Features**:
- Column mapping for fee fields
- Link to existing student records
- Migration status tracking

## Views Created

### Tree Views (List Views)
1. **Student Balance Staging** - Shows all imported balance data with optional columns
2. **Fee Staging** - Shows all imported fee data with optional columns

Both include:
- Color coding (green for migrated, warning for not migrated)
- Row counts
- Import batch grouping
- Date filters

### Form Views
1. **Student Balance Staging Form** - Detailed view of individual records
2. **Fee Staging Form** - Detailed view of fee records

Both include:
- Tabbed interface for columns
- Migration status header
- Action buttons (View linked record, Mark migrated, Reset)
- Import tracking information

### Wizard Views
1. **Import Student Balance** - Upload and configure import
2. **Import Fees** - Upload and configure fee import
3. **Migrate Student Balance** - Configure and execute migration
4. **Migrate Fees** - Configure and execute fee migration

All wizards include:
- Two-step process (configuration → results)
- Detailed logging
- Quick navigation to results

### Search Views
- Filter by migration status
- Filter by import batch
- Group by various fields
- Search in key columns

## Menu Structure

```
Data Import (Root Menu)
│
├── Student Balance
│   ├── Staging Data
│   ├── Import from Excel
│   └── Migrate to EMS
│
└── Fees
    ├── Staging Data
    ├── Import from Excel
    └── Migrate to EMS
```

## Security Groups and Access

### Access Levels

**School Administrator** (group_school_administrator):
- Full CRUD access to all models
- Can import, migrate, and delete data

**School Manager** (group_school_manager):
- Import and migrate data
- Create and update records
- Cannot delete

**School User** (group_school_user):
- Read-only access to staging tables
- Cannot import or migrate

## Key Features

### 1. Raw Data Import
- No transformation during import
- Preserves original data structure
- Flexible column mapping
- Batch identification
- Update existing records

### 2. Data Verification
- Full visibility into imported data
- Column statistics available
- Row count verification
- Import date tracking
- User tracking

### 3. Controlled Migration
- Visual column mapping
- Multiple migration modes
- Duplicate prevention
- Link to source records
- Detailed logging

### 4. Repeatable Process
- Re-import updated data
- Update existing batches
- Reset migration status
- Multiple batch support

## Technical Details

### Database Tables

**Permanent Tables**:
- `ics_student_balance_staging` - Student balance staging
- `ics_fee_staging` - Fee staging

**Transient Tables** (Auto-cleaned):
- `import_student_balance_wizard`
- `import_fees_wizard`
- `migrate_student_balance_wizard`
- `migrate_fees_wizard`

### Python Dependencies

**Required**:
- openpyxl - Excel file reading/writing

**Installation**:
```bash
pip install openpyxl
```

### Supported File Formats

**Excel Files**:
- XLSX format (Excel 2007+)
- Multiple sheets supported
- Data-only values read

## Data Flow

```
Excel File
    ↓
Import Wizard
    ↓
Staging Table (ics.*.staging)
    ↓
Verification & Mapping
    ↓
Migration Wizard
    ↓
EMS Tables (ics.student, ics.student.payslip)
```

## Use Cases

### Primary Use Cases

1. **Initial Data Migration**
   - Import legacy student balance data
   - Import historical fee records
   - One-time bulk migration

2. **Regular Updates**
   - Import updated balance data
   - Import new fee structures
   - Scheduled batch imports

3. **Data Verification**
   - Review imported data before migration
   - Identify data quality issues
   - Validate against EMS records

4. **Error Recovery**
   - Re-import corrected data
   - Reset failed migrations
   - Incremental migration

## Limitations

### Current Limitations

1. **Column Count**:
   - Student Balance: Max 25 columns
   - Fees: Max 30 columns

2. **File Format**:
   - Excel (XLSX) only
   - No CSV support

3. **Data Types**:
   - All data stored as text
   - Type conversion during migration

4. **Editing**:
   - No direct editing in UI
   - Re-import to update

### Workarounds

1. **More Columns Needed**:
   - Split data across multiple imports
   - Or extend model (requires code change)

2. **CSV Files**:
   - Convert to XLSX first
   - Use Excel or LibreOffice

3. **Data Type Issues**:
   - Format correctly in Excel
   - Use migration wizard for conversion

## Future Enhancements

### Planned Features (Not Yet Implemented)

1. CSV import support
2. JSON data import
3. Automated column detection
4. Bulk editing in staging tables
5. Data validation rules
6. Scheduled automatic imports
7. Export staging data back to Excel
8. More sophisticated duplicate detection
9. Data transformation rules
10. Import templates

### Extension Points

The module can be extended by:
- Adding new staging models
- Creating additional wizards
- Implementing custom migration logic
- Adding data transformation rules
- Integrating with external systems

## Installation Checklist

- [ ] Python openpyxl installed
- [ ] ics_ems_core module installed
- [ ] Module copied to addons path
- [ ] Odoo server restarted
- [ ] Apps list updated
- [ ] Module installed via Apps menu
- [ ] Access rights configured
- [ ] Test import performed

## Testing Checklist

- [ ] Import student balance Excel file
- [ ] View staging data
- [ ] Verify row counts
- [ ] Check column data
- [ ] Configure column mapping
- [ ] Migrate to EMS
- [ ] Verify EMS records
- [ ] Test update existing records
- [ ] Test error handling
- [ ] Test reset migration

## Support Resources

### Documentation
- README.md - Complete documentation
- INSTALLATION.md - Installation guide
- USAGE_GUIDE.md - Quick usage guide
- MODULE_SUMMARY.md - This file

### Contact
- Email: support@icloudsolutions.sa
- Website: https://icloudsolutions.sa

### Source Code
- Module files included
- Well-commented code
- Follows Odoo 19 standards

## Version History

### Version 19.0.1.0.0 (Current)
- Initial release
- Student balance import
- Fee import
- Migration wizards
- Full documentation

## Credits

**Developed by**: ICS - iCloud Solutions
**Website**: https://icloudsolutions.sa
**License**: LGPL-3
**Copyright**: © 2026 ICS - iCloud Solutions

---

**Last Updated**: 2026-01-01
**Module Status**: Production Ready
