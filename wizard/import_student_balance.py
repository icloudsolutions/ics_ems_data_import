import base64
import io
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

try:
    import openpyxl
except ImportError:
    openpyxl = None


class ImportStudentBalance(models.TransientModel):
    _name = 'import.student.balance.wizard'
    _description = 'Import Student Balance from Excel'

    excel_file = fields.Binary(string='Excel File', required=True,
                                help='Upload the student balance Excel file')
    filename = fields.Char(string='Filename')
    import_batch = fields.Char(string='Import Batch Name',
                                 default=lambda self: f"BALANCE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                                 required=True,
                                 help='Unique identifier for this import batch')
    sheet_name = fields.Char(string='Sheet Name', default='Sheet1',
                               help='Name of the Excel sheet to import (leave empty for first sheet)')
    skip_header_rows = fields.Integer(string='Skip Header Rows', default=1,
                                       help='Number of header rows to skip')
    update_existing = fields.Boolean(string='Update Existing Records',
                                      help='Update records if batch already exists, otherwise create new')

    # Summary fields
    total_rows = fields.Integer(string='Total Rows', readonly=True)
    imported_rows = fields.Integer(string='Imported Rows', readonly=True)
    updated_rows = fields.Integer(string='Updated Rows', readonly=True)
    error_count = fields.Integer(string='Errors', readonly=True)
    import_log = fields.Text(string='Import Log', readonly=True)

    def action_import(self):
        self.ensure_one()

        if not openpyxl:
            raise UserError(_('The Python library "openpyxl" is required. Please install it: pip install openpyxl'))

        if not self.excel_file:
            raise UserError(_('Please upload an Excel file.'))

        # Decode the file
        try:
            file_data = base64.b64decode(self.excel_file)
            workbook = openpyxl.load_workbook(io.BytesIO(file_data), data_only=True)
        except Exception as e:
            raise UserError(_('Error reading Excel file: %s') % str(e))

        # Get the sheet
        if self.sheet_name:
            if self.sheet_name in workbook.sheetnames:
                sheet = workbook[self.sheet_name]
            else:
                raise UserError(_('Sheet "%s" not found. Available sheets: %s') %
                              (self.sheet_name, ', '.join(workbook.sheetnames)))
        else:
            sheet = workbook.active

        # Check if batch exists
        existing_batch = self.env['ics.student.balance.staging'].search([
            ('import_batch', '=', self.import_batch)
        ], limit=1)

        if existing_batch and not self.update_existing:
            raise UserError(_('Import batch "%s" already exists. Enable "Update Existing Records" or use a different batch name.') % self.import_batch)

        # Process rows
        staging_obj = self.env['ics.student.balance.staging']
        imported_count = 0
        updated_count = 0
        error_count = 0
        log_messages = []

        for row_idx, row in enumerate(sheet.iter_rows(min_row=self.skip_header_rows + 1), start=self.skip_header_rows + 1):
            try:
                # Extract cell values
                values = {}
                for col_idx, cell in enumerate(row[:25], start=1):  # Max 25 columns
                    col_field = f'col_{col_idx:02d}'
                    cell_value = cell.value

                    # Convert to string, handling different types
                    if cell_value is not None:
                        if isinstance(cell_value, (int, float)):
                            values[col_field] = str(cell_value)
                        elif isinstance(cell_value, datetime):
                            values[col_field] = cell_value.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            values[col_field] = str(cell_value)
                    else:
                        values[col_field] = ''

                # Skip empty rows
                if not any(values.values()):
                    continue

                values.update({
                    'import_batch': self.import_batch,
                    'row_number': row_idx,
                    'import_date': fields.Datetime.now(),
                    'imported_by': self.env.user.id,
                })

                # Check if record exists
                existing = staging_obj.search([
                    ('import_batch', '=', self.import_batch),
                    ('row_number', '=', row_idx)
                ], limit=1)

                if existing and self.update_existing:
                    existing.write(values)
                    updated_count += 1
                else:
                    staging_obj.create(values)
                    imported_count += 1

            except Exception as e:
                error_count += 1
                log_messages.append(f"Row {row_idx}: {str(e)}")

        # Update wizard with results
        self.write({
            'total_rows': sheet.max_row - self.skip_header_rows,
            'imported_rows': imported_count,
            'updated_rows': updated_count,
            'error_count': error_count,
            'import_log': '\n'.join(log_messages) if log_messages else 'Import completed successfully!',
        })

        # Show results
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import Results'),
            'res_model': 'import.student.balance.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {'show_results': True},
        }

    def action_view_imported_data(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Imported Student Balance Data'),
            'res_model': 'ics.student.balance.staging',
            'view_mode': 'tree,form',
            'domain': [('import_batch', '=', self.import_batch)],
            'context': {'default_import_batch': self.import_batch},
        }
