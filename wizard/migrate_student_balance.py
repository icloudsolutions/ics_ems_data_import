from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MigrateStudentBalance(models.TransientModel):
    _name = 'migrate.student.balance.wizard'
    _description = 'Migrate Student Balance to EMS'

    import_batch = fields.Many2one('ics.student.balance.staging', string='Import Batch',
                                     domain="[('migrated', '=', False)]",
                                     help='Select records from a specific batch')
    migration_mode = fields.Selection([
        ('create_only', 'Create New Only'),
        ('update_only', 'Update Existing Only'),
        ('create_update', 'Create New and Update Existing'),
    ], string='Migration Mode', default='create_update', required=True)

    # Field mapping configuration
    student_code_column = fields.Selection([
        ('col_01', 'Column 1'), ('col_02', 'Column 2'), ('col_03', 'Column 3'),
        ('col_04', 'Column 4'), ('col_05', 'Column 5'),
    ], string='Student Code Column', default='col_01',
       help='Column containing the student code/ID')

    student_name_column = fields.Selection([
        ('col_01', 'Column 1'), ('col_02', 'Column 2'), ('col_03', 'Column 3'),
        ('col_04', 'Column 4'), ('col_05', 'Column 5'),
    ], string='Student Name Column', default='col_02',
       help='Column containing the student name')

    balance_column = fields.Selection([
        ('col_01', 'Column 1'), ('col_02', 'Column 2'), ('col_03', 'Column 3'),
        ('col_04', 'Column 4'), ('col_05', 'Column 5'), ('col_06', 'Column 6'),
        ('col_07', 'Column 7'), ('col_08', 'Column 8'), ('col_09', 'Column 9'),
        ('col_10', 'Column 10'),
    ], string='Balance Column', default='col_03',
       help='Column containing the balance amount')

    # Results
    success_count = fields.Integer(string='Success', readonly=True)
    error_count = fields.Integer(string='Errors', readonly=True)
    migration_log = fields.Text(string='Migration Log', readonly=True)

    def action_migrate(self):
        self.ensure_one()

        # Get records to migrate
        if self.import_batch:
            domain = [('import_batch', '=', self.import_batch.import_batch), ('migrated', '=', False)]
        else:
            domain = [('migrated', '=', False)]

        staging_records = self.env['ics.student.balance.staging'].search(domain)

        if not staging_records:
            raise UserError(_('No records found to migrate.'))

        success_count = 0
        error_count = 0
        log_messages = []

        for record in staging_records:
            try:
                # Extract values based on column mapping
                student_code = getattr(record, self.student_code_column, '').strip()
                student_name = getattr(record, self.student_name_column, '').strip()
                balance_str = getattr(record, self.balance_column, '0').strip()

                # Validate required fields
                if not student_code:
                    raise ValueError('Student code is empty')

                # Convert balance to float
                try:
                    balance = float(balance_str.replace(',', ''))
                except ValueError:
                    balance = 0.0

                # Find or create student
                student = self.env['ics.student'].search([
                    '|',
                    ('student_code', '=', student_code),
                    ('name', '=', student_name),
                ], limit=1)

                if student:
                    if self.migration_mode in ['update_only', 'create_update']:
                        # Update student record if needed
                        log_messages.append(f"Row {record.row_number}: Found student {student.name} (ID: {student.id})")
                        record.write({
                            'migrated': True,
                            'migration_date': fields.Datetime.now(),
                            'student_id': student.id,
                            'migration_log': f'Linked to existing student: {student.name}',
                        })
                        success_count += 1
                    else:
                        log_messages.append(f"Row {record.row_number}: Student exists, skipped (create_only mode)")
                else:
                    if self.migration_mode in ['create_only', 'create_update']:
                        # Note: This is a simplified example
                        # In practice, you would need more complete student data
                        log_messages.append(f"Row {record.row_number}: Student not found - {student_code}")
                        record.write({
                            'migration_log': f'Student not found: {student_code}. Please create student first or provide complete data.',
                        })
                        error_count += 1
                    else:
                        log_messages.append(f"Row {record.row_number}: Student not found, skipped (update_only mode)")
                        error_count += 1

            except Exception as e:
                error_count += 1
                log_messages.append(f"Row {record.row_number}: ERROR - {str(e)}")
                record.write({
                    'migration_log': f'Migration failed: {str(e)}',
                })

        # Update wizard with results
        self.write({
            'success_count': success_count,
            'error_count': error_count,
            'migration_log': '\n'.join(log_messages),
        })

        return {
            'type': 'ir.actions.act_window',
            'name': _('Migration Results'),
            'res_model': 'migrate.student.balance.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_migrated_students(self):
        self.ensure_one()
        student_ids = self.env['ics.student.balance.staging'].search([
            ('migrated', '=', True),
            ('student_id', '!=', False),
        ]).mapped('student_id')

        return {
            'type': 'ir.actions.act_window',
            'name': _('Migrated Students'),
            'res_model': 'ics.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', student_ids.ids)],
        }
