# models/student_balance_staging.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StudentBalanceStaging(models.Model):
    _name = 'ics.student.balance.staging'
    _description = 'Student Balance Staging Table - Raw Import Data'
    _order = 'import_batch desc, id'

    # Import tracking
    import_batch = fields.Char(string='Import Batch', required=True, index=True,
                                help='Batch identifier for grouping imports')
    import_date = fields.Datetime(string='Import Date', default=fields.Datetime.now, required=True)
    imported_by = fields.Many2one('res.users', string='Imported By', default=lambda self: self.env.user)
    row_number = fields.Integer(string='Row #', help='Original row number from Excel file')

    # Migration status - Changed to Selection field for statusbar
    state = fields.Selection([
        ('draft', 'Not Migrated'),
        ('done', 'Migrated'),
    ], string='Status', default='draft', required=True)
    
    # Keep migrated as computed field for backward compatibility
    migrated = fields.Boolean(string='Migrated', compute='_compute_migrated', 
                              store=True, index=True)
    migration_date = fields.Datetime(string='Migration Date')
    migration_log = fields.Text(string='Migration Log')
    student_id = fields.Many2one('ics.student', string='Linked Student',
                                   help='Student created/updated from this record')

    # Raw data fields - flexible text fields to accommodate any data
    # Column 1-20 for flexible import
    col_01 = fields.Char(string='Column 1')
    col_02 = fields.Char(string='Column 2')
    col_03 = fields.Char(string='Column 3')
    col_04 = fields.Char(string='Column 4')
    col_05 = fields.Char(string='Column 5')
    col_06 = fields.Char(string='Column 6')
    col_07 = fields.Char(string='Column 7')
    col_08 = fields.Char(string='Column 8')
    col_09 = fields.Char(string='Column 9')
    col_10 = fields.Char(string='Column 10')
    col_11 = fields.Char(string='Column 11')
    col_12 = fields.Char(string='Column 12')
    col_13 = fields.Char(string='Column 13')
    col_14 = fields.Char(string='Column 14')
    col_15 = fields.Char(string='Column 15')
    col_16 = fields.Char(string='Column 16')
    col_17 = fields.Char(string='Column 17')
    col_18 = fields.Char(string='Column 18')
    col_19 = fields.Char(string='Column 19')
    col_20 = fields.Char(string='Column 20')

    # Additional fields for numeric/text data
    col_21 = fields.Text(string='Column 21')
    col_22 = fields.Text(string='Column 22')
    col_23 = fields.Text(string='Column 23')
    col_24 = fields.Text(string='Column 24')
    col_25 = fields.Text(string='Column 25')

    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('unique_batch_row', 'unique(import_batch, row_number)', 
         'Row number must be unique within each import batch!')
    ]

    @api.depends('state')
    def _compute_migrated(self):
        for record in self:
            record.migrated = (record.state == 'done')

    def name_get(self):
        result = []
        for record in self:
            name = f"Row {record.row_number} - Batch {record.import_batch}"
            if record.col_01:
                name = f"{record.col_01} - {name}"
            result.append((record.id, name))
        return result

    def action_view_student(self):
        self.ensure_one()
        if not self.student_id:
            raise UserError(_('No student linked to this record yet.'))
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
            'student_id': False,
        })