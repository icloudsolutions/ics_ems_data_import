# ICS EMS Data Import - Installation Guide

## Prerequisites

### 1. System Requirements
- Odoo 19.0
- Python 3.10 or higher
- PostgreSQL database

### 2. Required Modules
- `ics_ems_core` - Must be installed first

### 3. Python Dependencies
```bash
pip install openpyxl
```

Or using apt (Debian/Ubuntu):
```bash
apt-get install python3-openpyxl
```

## Installation Steps

### Step 1: Copy Module Files

Copy the `ics_ems_data_import` directory to your Odoo addons path:

```bash
# Option 1: Copy to custom addons directory
cp -r ics_ems_data_import /path/to/odoo/custom-addons/

# Option 2: Copy to default addons directory
cp -r ics_ems_data_import /path/to/odoo/addons/
```

### Step 2: Update Addons Path (if needed)

Edit your Odoo configuration file (`odoo.conf`):

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/odoo/custom-addons
```

### Step 3: Restart Odoo Server

```bash
# If using systemd
sudo systemctl restart odoo

# If running manually
/path/to/odoo-bin -c /path/to/odoo.conf
```

### Step 4: Update Apps List

1. Log in to Odoo as Administrator
2. Go to **Settings** → **Apps**
3. Click **Update Apps List** in the top menu
4. Confirm the update

### Step 5: Install the Module

1. In Apps menu, remove the "Apps" filter
2. Search for "ICS EMS Data Import"
3. Click **Install**
4. Wait for installation to complete

## Verification

After installation, verify the module is working:

1. Check that **Data Import** menu appears in main menu bar
2. Navigate to **Data Import** → **Student Balance** → **Staging Data**
3. Try opening the import wizard

## Post-Installation

### Configure Access Rights

Ensure users have appropriate access:

1. Go to **Settings** → **Users & Companies** → **Users**
2. Edit user and assign groups:
   - **School Administrator** - Full access
   - **School Manager** - Import and migrate
   - **School User** - View only

### Test Import

Test with a sample Excel file:

1. Create a test Excel file with sample data
2. Navigate to **Data Import** → **Student Balance** → **Import from Excel**
3. Upload the file and test import

## Troubleshooting

### Module Not Appearing

**Issue**: Module doesn't appear in Apps list

**Solutions**:
- Verify module is in correct addons directory
- Check Odoo configuration addons_path
- Restart Odoo server
- Update Apps List again
- Check Odoo logs for errors

### Import Errors

**Issue**: "openpyxl not found" error

**Solutions**:
```bash
# Install for system Python
sudo pip3 install openpyxl

# Install with --break-system-packages if needed
sudo pip3 install openpyxl --break-system-packages

# Or install via package manager
sudo apt-get install python3-openpyxl
```

**Issue**: "Module ics_ems_core not found"

**Solutions**:
- Install `ics_ems_core` module first
- Verify it's in the addons path
- Check module dependencies

### Permission Errors

**Issue**: Users cannot access import features

**Solutions**:
- Assign appropriate security groups
- Verify access rights in Security settings
- Check user permissions

## Upgrading

To upgrade to a newer version:

1. Backup your database
2. Replace module files with new version
3. Restart Odoo server
4. Go to **Settings** → **Apps**
5. Search for "ICS EMS Data Import"
6. Click **Upgrade**

## Uninstallation

To uninstall the module:

1. Go to **Settings** → **Apps**
2. Search for "ICS EMS Data Import"
3. Click **Uninstall**
4. Confirm uninstallation

**Warning**: Uninstalling will remove all staging data. Export important data before uninstalling.

## Support

If you encounter issues during installation:

- **Email**: support@icloudsolutions.sa
- **Website**: https://icloudsolutions.sa
- **Documentation**: See README.md in module directory

## Developer Notes

### Module Structure
```
ics_ems_data_import/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── student_balance_staging.py
│   └── fee_staging.py
├── wizard/
│   ├── __init__.py
│   ├── import_student_balance.py
│   ├── import_fees.py
│   ├── migrate_student_balance.py
│   └── migrate_fees.py
├── views/
│   ├── menu_views.xml
│   ├── student_balance_staging_views.xml
│   ├── fee_staging_views.xml
│   └── [wizard views...]
├── security/
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── index.html
└── README.md
```

### Database Tables Created
- `ics_student_balance_staging`
- `ics_fee_staging`
- Various wizard tables (transient)

### External API Dependencies
- openpyxl (Excel file processing)
