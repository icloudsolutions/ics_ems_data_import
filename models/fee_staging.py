# models/fee_staging.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FeeStaging(models.Model):
    _name = 'ics.fee.staging'
    _description = 'Fee Payment Staging Table - Raw Import Data'
    _order = 'import_batch desc, receipt_date desc'

    # Import tracking
    import_batch = fields.Char(string='Import Batch', required=True, index=True)
    import_date = fields.Datetime(string='Import Date', default=fields.Datetime.now, required=True)
    imported_by = fields.Many2one('res.users', string='Imported By', default=lambda self: self.env.user)
    row_number = fields.Integer(string='Row Number', help='Row number from Excel')

    # Migration status
    state = fields.Selection([
        ('draft', 'Not Migrated'),
        ('done', 'Migrated'),
    ], string='Status', default='draft', required=True)

    migrated = fields.Boolean(string='Migrated', compute='_compute_migrated', store=True, index=True)
    migration_date = fields.Datetime(string='Migration Date')
    migration_log = fields.Text(string='Migration Log')
    payment_id = fields.Many2one('account.payment', string='Linked Payment')
    student_id = fields.Many2one('ics.student', string='Linked Student')

    # PAYMENT RECORD FIELDS (from fees.xlsx - 8 columns)
    sequence_number = fields.Integer(string='Sequence', help='التسلسل - Column 1')
    receipt_number = fields.Char(string='Receipt Number', help='رقم السند - Column 2', index=True)
    receipt_date = fields.Date(string='Receipt Date', help='تاريخ السند - Column 3')
    receipt_date_excel = fields.Char(string='Receipt Date (Excel)',
                                     help='Raw Excel date value before conversion')

    old_student_id = fields.Char(string='Old Student ID', help='رقم الطالب - Column 4', index=True)
    student_name = fields.Char(string='Student Name', help='اسم الطالب - Column 5')
    amount = fields.Float(string='Amount', help='المبلغ - Column 6')
    status = fields.Char(string='Status', help='الحالة - Column 7 (فعال/ملغي)')
    cashier_name = fields.Char(string='Cashier Name', help='أمين الصندوق - Column 8')

    # Linked records for migration
    journal_id = fields.Many2one('account.journal', string='Payment Journal',
                                 help='Journal to record payment (mapped from cashier)')

    notes = fields.Text(string='Notes')

    _unique_import = models.Constraint(
        'unique(import_batch, row_number)',
        'Row number must be unique within each import batch!'
    )

    @api.depends('state')
    def _compute_migrated(self):
        for record in self:
            record.migrated = (record.state == 'done')

    def name_get(self):
        result = []
        for record in self:
            name = f"Receipt {record.receipt_number or 'N/A'} - {record.student_name or 'Unknown'}"
            result.append((record.id, name))
        return result

    def action_view_payment(self):
        self.ensure_one()
        if not self.payment_id:
            raise UserError(_('No payment linked yet.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payment'),
            'res_model': 'account.payment',
            'res_id': self.payment_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_student(self):
        self.ensure_one()
        if not self.student_id:
            raise UserError(_('No student linked yet.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Student'),
            'res_model': 'ics.student',
            'res_id': self.student_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_mark_migrated(self):
        self.write({
            'state': 'done',
            'migration_date': fields.Datetime.now(),
        })

    def action_reset_migration(self):
        self.write({
            'state': 'draft',
            'migration_date': False,
            'migration_log': False,
            'payment_id': False,
            'student_id': False,
            'journal_id': False,
        })
