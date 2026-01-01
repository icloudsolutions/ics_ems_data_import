# ICS EMS Data Import - Quick Usage Guide

## Quick Start

### 1. Import Student Balance Data

**Step-by-step:**

1. Navigate to **Data Import** → **Student Balance** → **Import from Excel**

2. In the wizard:
   - Click **Choose File** and select your Excel file
   - Leave default settings for first import:
     - Sheet Name: Sheet1
     - Skip Header Rows: 1
   - Batch name is auto-generated (e.g., BALANCE_20260101_120000)
   - Click **Import**

3. Review results:
   - Check total rows imported
   - Review any errors in the log
   - Click **View Imported Data** to see staging table

4. Verify in staging table:
   - All rows are visible
   - Columns are properly populated
   - Row numbers match Excel file

### 2. Map and Migrate Data

**After importing:**

1. Navigate to **Data Import** → **Student Balance** → **Migrate to EMS**

2. Configure migration:
   - **Import Batch**: Leave empty to migrate all, or select specific batch
   - **Migration Mode**: Choose "Create New and Update Existing"
   - **Column Mapping**:
     - Student Code Column: Select column containing student ID
     - Student Name Column: Select column with student name
     - Balance Column: Select column with balance amount
   - Click **Migrate**

3. Review migration results:
   - Check success count
   - Review migration log for errors
   - Click **View Migrated Students** to see EMS records

### 3. Re-import Updated Data

**When you have updated data:**

1. Navigate to **Data Import** → **Student Balance** → **Import from Excel**

2. Configure for update:
   - Select the same Excel file (with updates)
   - Enter the **same batch name** as before
   - Enable **Update Existing Records**
   - Click **Import**

3. Result: Existing records will be updated with new data

4. If you need to re-migrate:
   - Find the records in staging table
   - Use **Reset Migration** button to clear migration status
   - Run migration wizard again

## Common Scenarios

### Scenario 1: First Time Import

```
Goal: Import student balance data for the first time

Steps:
1. Prepare Excel: balance_student.xlsx with columns:
   - Student Code | Student Name | Balance | Grade | ...

2. Import to staging:
   - Use default batch name
   - Don't enable "Update Existing"

3. Verify data in staging table

4. Migrate to EMS with column mapping

Result: New student records or updated balances
```

### Scenario 2: Update Existing Data

```
Goal: Import updated balance data for same students

Steps:
1. Prepare updated Excel with same structure

2. Import with:
   - Same batch name as before
   - Enable "Update Existing Records"

3. Existing staging records are updated

4. Reset migration if needed and re-migrate

Result: Updated balances in EMS
```

### Scenario 3: Multiple Batches

```
Goal: Keep separate imports for different purposes

Steps:
1. First import:
   - Batch name: BALANCE_JANUARY

2. Second import:
   - Batch name: BALANCE_FEBRUARY

3. View and migrate each batch separately

Result: Organized imports by batch
```

### Scenario 4: Handling Errors

```
Goal: Fix import or migration errors

For Import Errors:
1. Check import log for error details
2. Fix Excel file
3. Re-import with "Update Existing" enabled

For Migration Errors:
1. Check migration log
2. Create missing student records if needed
3. Fix column mapping if wrong
4. Use "Reset Migration" on failed records
5. Re-run migration

Result: Clean data in EMS
```

## Tips and Best Practices

### Before Import

✅ **DO:**
- Keep headers in first row of Excel
- Use consistent column order
- Test with small file first
- Backup database before large imports

❌ **DON'T:**
- Mix data types in columns
- Leave empty columns between data
- Use special characters in batch names

### During Import

✅ **DO:**
- Review import results carefully
- Check error logs
- Verify row counts
- Inspect sample records

❌ **DON'T:**
- Import without verifying first
- Ignore error messages
- Skip data verification step

### During Migration

✅ **DO:**
- Map columns correctly
- Start with "Create New and Update Existing" mode
- Review migration logs
- Check migrated records in EMS

❌ **DON'T:**
- Migrate without checking staging data
- Ignore failed migrations
- Use wrong column mapping

## Column Mapping Guide

### Student Balance Columns

Typical mapping:
- **Column 1** → Student Code/ID
- **Column 2** → Student Name
- **Column 3** → Balance Amount
- **Column 4** → Grade/Class
- **Column 5** → Academic Year

Adjust based on your Excel structure.

### Fee Columns

Typical mapping:
- **Column 1** → Student Code
- **Column 2** → Fee Type
- **Column 3** → Amount
- **Column 4** → Term/Period
- **Column 5** → Due Date

## Keyboard Shortcuts

- **Alt + Home** → Go to main menu
- **Ctrl + K** → Open command palette
- **Ctrl + F** → Search in current view

## Troubleshooting Quick Fixes

### "No records to migrate"
**Fix**: Make sure records in staging table are not already marked as "Migrated". Use "Not Migrated" filter.

### "Student not found"
**Fix**: Create student record in EMS first, or check student code mapping.

### "Batch already exists"
**Fix**: Enable "Update Existing Records" or change batch name.

### "Wrong data in columns"
**Fix**: Verify column mapping in migration wizard matches your Excel structure.

## Getting Help

### Documentation
- Full README: See README.md in module folder
- Installation: See INSTALLATION.md

### Support
- Email: support@icloudsolutions.sa
- Website: https://icloudsolutions.sa

### Debug Mode
Enable developer mode for more details:
1. Go to Settings
2. Activate Developer Mode
3. See technical details in forms

## Video Tutorials (Planned)

Coming soon:
- Basic Import Workflow
- Advanced Column Mapping
- Handling Large Datasets
- Error Resolution

Check our website for updates!
