from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MigrateFees(models.TransientModel):
    _name = 'migrate.fees.wizard'
    _description = 'Migrate Fees to EMS'

    import_batch = fields.Many2one('ics.fee.staging', string='Import Batch',
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

    fee_type_column = fields.Selection([
        ('col_01', 'Column 1'), ('col_02', 'Column 2'), ('col_03', 'Column 3'),
        ('col_04', 'Column 4'), ('col_05', 'Column 5'), ('col_06', 'Column 6'),
    ], string='Fee Type Column', default='col_02',
       help='Column containing the fee type')

    amount_column = fields.Selection([
        ('col_01', 'Column 1'), ('col_02', 'Column 2'), ('col_03', 'Column 3'),
        ('col_04', 'Column 4'), ('col_05', 'Column 5'), ('col_06', 'Column 6'),
        ('col_07', 'Column 7'), ('col_08', 'Column 8'), ('col_09', 'Column 9'),
        ('col_10', 'Column 10'),
    ], string='Amount Column', default='col_03',
       help='Column containing the fee amount')

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

        staging_records = self.env['ics.fee.staging'].search(domain)

        if not staging_records:
            raise UserError(_('No records found to migrate.'))

        success_count = 0
        error_count = 0
        log_messages = []

        for record in staging_records:
            try:
                # Extract values based on column mapping
                student_code = getattr(record, self.student_code_column, '').strip()
                fee_type = getattr(record, self.fee_type_column, '').strip()
                amount_str = getattr(record, self.amount_column, '0').strip()

                # Validate required fields
                if not student_code:
                    raise ValueError('Student code is empty')

                # Convert amount to float
                try:
                    amount = float(amount_str.replace(',', ''))
                except ValueError:
                    amount = 0.0

                # Find student
                student = self.env['ics.student'].search([
                    ('student_code', '=', student_code),
                ], limit=1)

                if not student:
                    raise ValueError(f'Student not found: {student_code}')

                # Check if payslip exists
                payslip = self.env['ics.student.payslip'].search([
                    ('student_id', '=', student.id),
                    ('state', '=', 'draft'),
                ], limit=1)

                if payslip:
                    if self.migration_mode in ['update_only', 'create_update']:
                        log_messages.append(f"Row {record.row_number}: Found payslip for {student.name}")
                        record.write({
                            'migrated': True,
                            'migration_date': fields.Datetime.now(),
                            'payslip_id': payslip.id,
                            'migration_log': f'Linked to existing payslip: {payslip.reference}',
                        })
                        success_count += 1
                    else:
                        log_messages.append(f"Row {record.row_number}: Payslip exists, skipped")
                else:
                    if self.migration_mode in ['create_only', 'create_update']:
                        log_messages.append(f"Row {record.row_number}: Would create payslip for {student.name}")
                        record.write({
                            'migration_log': f'Ready to create payslip for: {student.name}. Use EMS tools to generate payslips.',
                        })
                        success_count += 1
                    else:
                        log_messages.append(f"Row {record.row_number}: No payslip found, skipped")
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
            'res_model': 'migrate.fees.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_migrated_payslips(self):
        self.ensure_one()
        payslip_ids = self.env['ics.fee.staging'].search([
            ('migrated', '=', True),
            ('payslip_id', '!=', False),
        ]).mapped('payslip_id')

        return {
            'type': 'ir.actions.act_window',
            'name': _('Migrated Payslips'),
            'res_model': 'ics.student.payslip',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', payslip_ids.ids)],
        }
