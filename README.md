# ICS EMS Data Import Module

Version: 19.0.1.0.0

## Overview

This Odoo 19 module provides a comprehensive solution for importing legacy data from Excel files into staging tables, with tools for verification and controlled migration to the ICS Education Management System (EMS).

## Features

### Raw Data Import
- Import Excel files without any transformation
- Store data in flexible staging tables with up to 30 columns
- Support for multiple import batches with unique identifiers
- Automatic batch naming with timestamps
- Update existing records or create new ones
- Detailed import logs and error tracking

### Data Verification
- View all imported data in dedicated list views
- Column-by-column data inspection
- Row count tracking
- Import batch grouping
- Filter by migration status

### Controlled Migration
- Map columns to EMS fields using visual wizard
- Multiple migration modes:
  - Create new records only
  - Update existing records only
  - Create and update (smart merge)
- Prevent duplicate data
- Link staging records to migrated EMS records
- Detailed migration logs for troubleshooting

### Repeatable Process
- Import updated data multiple times
- Update existing batches or create new ones
- Reset migration status when needed
- Track migration history

## Installation

### Prerequisites

1. **Python Dependencies**
   ```bash
   pip install openpyxl
   ```

2. **Odoo Dependencies**
   - `ics_ems_core` module must be installed

### Installation Steps

1. Copy the `ics_ems_data_import` folder to your Odoo addons directory
2. Restart Odoo server
3. Update Apps List (Settings → Apps → Update Apps List)
4. Search for "ICS EMS Data Import"
5. Click Install

## Usage

### 1. Import Student Balance Data

**Navigation:** Data Import → Student Balance → Import from Excel

1. Click "Import from Excel" menu
2. Upload your Excel file (e.g., balance_student.xlsx)
3. Configure import settings:
   - **Import Batch Name**: Auto-generated or custom name
   - **Sheet Name**: Excel sheet to import (default: Sheet1)
   - **Skip Header Rows**: Number of header rows (default: 1)
   - **Update Existing**: Enable to update existing batch
4. Click "Import"
5. Review import results:
   - Total rows processed
   - Successfully imported rows
   - Updated rows
   - Errors encountered
6. Click "View Imported Data" to inspect

### 2. View Staging Data

**Navigation:** Data Import → Student Balance → Staging Data

- View all imported raw data
- Filter by import batch
- Filter by migration status
- Inspect individual records
- See import dates and users

### 3. Migrate to EMS

**Navigation:** Data Import → Student Balance → Migrate to EMS

1. Click "Migrate to EMS"
2. Configure migration:
   - **Import Batch**: Select specific batch or migrate all
   - **Migration Mode**: Choose create/update strategy
   - **Column Mapping**:
     - Student Code Column
     - Student Name Column
     - Balance Column
3. Click "Migrate"
4. Review migration results and logs
5. Click "View Migrated Students" to see EMS records

### 4. Import Fee Data

**Navigation:** Data Import → Fees → Import from Excel

Similar process to Student Balance import, but for fee data.

## Data Structure

### Student Balance Staging Table
- **Import Tracking**: batch, date, user, row number
- **Migration Status**: migrated flag, date, log, linked student
- **Data Columns**: 25 flexible columns (col_01 to col_25)
- **Notes**: Additional information field

### Fee Staging Table
- **Import Tracking**: batch, date, user, row number
- **Migration Status**: migrated flag, date, log, linked payslip
- **Data Columns**: 30 flexible columns (col_01 to col_30)
- **Notes**: Additional information field

## Excel File Format

### Expected Structure
- First row: Headers (will be skipped)
- Subsequent rows: Data
- Columns: Up to 25 (balance) or 30 (fees)
- Data types: Text, numbers, dates (all converted to text)

### Example: balance_student.xlsx
```
Student Code | Student Name | Balance | Grade | ...
STU001      | Ahmed Ali    | 1500.00 | 5     | ...
STU002      | Sara Omar    | 2000.00 | 6     | ...
```

### Example: fees.xlsx
```
Student Code | Fee Type     | Amount  | Term  | ...
STU001      | Tuition      | 5000.00 | Fall  | ...
STU002      | Transport    | 1200.00 | Fall  | ...
```

## Workflow

### Standard Import Process

1. **Prepare Excel Files**
   - Organize data in Excel format
   - Ensure consistent column order
   - Include headers in first row

2. **Import to Staging**
   - Upload files using import wizard
   - Verify import results
   - Check for errors

3. **Verify Imported Data**
   - Review staging data in list views
   - Confirm row counts match expectations
   - Inspect sample records

4. **Map Fields**
   - Identify which columns contain which data
   - Configure column mapping in migration wizard

5. **Migrate to EMS**
   - Run migration wizard
   - Review migration logs
   - Verify created/updated records

6. **Handle Errors**
   - Check migration logs for failed records
   - Fix data issues in staging tables
   - Reset migration and retry

### Re-importing Updated Data

1. Enable "Update Existing Records" in import wizard
2. Use same batch name as previous import
3. Updated data will replace old data
4. Reset migration status if needed
5. Re-run migration

## Security

### Access Rights

**School Administrator**
- Full access to all features
- Import, view, migrate, delete

**School Manager**
- Import and migrate data
- View all records
- Cannot delete

**School User**
- View staging data only
- Read-only access

## Troubleshooting

### Import Issues

**Problem**: "openpyxl library required" error
**Solution**: Install openpyxl: `pip install openpyxl`

**Problem**: "Sheet not found" error
**Solution**: Check sheet name in Excel file, update in import wizard

**Problem**: Import batch already exists
**Solution**: Enable "Update Existing Records" or use different batch name

### Migration Issues

**Problem**: Student not found during migration
**Solution**: Create student records first, or verify student code mapping

**Problem**: Duplicate records
**Solution**: Use "Update Only" mode or check for existing records first

**Problem**: Wrong data in columns
**Solution**: Verify column mapping configuration in migration wizard

## Technical Details

### Models

- `ics.student.balance.staging` - Student balance staging table
- `ics.fee.staging` - Fee staging table
- `import.student.balance.wizard` - Import wizard
- `import.fees.wizard` - Fee import wizard
- `migrate.student.balance.wizard` - Migration wizard
- `migrate.fees.wizard` - Fee migration wizard

### Key Methods

**Import Wizards**
- `action_import()` - Process Excel file and create staging records
- `action_view_imported_data()` - Navigate to staging data view

**Staging Models**
- `action_view_student()` / `action_view_payslip()` - View linked EMS records
- `action_mark_migrated()` - Manually mark as migrated
- `action_reset_migration()` - Reset migration status

**Migration Wizards**
- `action_migrate()` - Migrate staging data to EMS
- `action_view_migrated_students()` / `action_view_migrated_payslips()` - View results

## Limitations

- Maximum 25 columns for student balance data
- Maximum 30 columns for fee data
- Excel files only (XLSX format)
- No direct editing of staging data through UI
- Migration requires existing student records for matching

## Future Enhancements

- Support for more data types (CSV, JSON)
- Automated column detection and mapping
- Bulk data editing in staging tables
- Advanced duplicate detection
- Data validation rules
- Scheduled imports
- Export staging data back to Excel

## Support

For issues, questions, or feature requests:
- Email: support@icloudsolutions.sa
- Website: https://icloudsolutions.sa

## License

LGPL-3

## Credits

**Author:** ICS - iCloud Solutions
**Website:** https://icloudsolutions.sa
**Version:** 19.0.1.0.0
