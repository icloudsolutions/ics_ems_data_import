# models/student_balance_staging.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StudentBalanceStaging(models.Model):
    _name = 'ics.student.balance.staging'
    _description = 'Student Balance Staging Table - Raw Import Data'
    _order = 'import_batch desc, row_number'

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
    student_id = fields.Many2one('ics.student', string='Linked Student')
    parent_id = fields.Many2one('ics.parent', string='Linked Parent')

    # STUDENT INFORMATION (from Excel columns 1-10)
    old_student_id = fields.Char(string='Old Student ID', help='رقم الطالب - Column 2')
    student_name = fields.Char(string='Student Name', help='اسم الطالب - Column 3')
    contract_id = fields.Char(string='Contract ID', help='رقم العقد المالي - Column 4')
    student_national_id = fields.Char(string='Student National ID', help='رقم الهوية/الاقامة لطالب - Column 5')

    # PARENT INFORMATION (columns 6-9)
    old_parent_id = fields.Char(string='Old Parent ID', help='رقم ولي الامر - Column 6')
    parent_name = fields.Char(string='Parent Name', help='أسم ولي الامر - Column 7')
    parent_national_id = fields.Char(string='Parent National ID', help='رقم الهوية/الاقامة لولي الأمر - Column 8')
    parent_mobile = fields.Char(string='Parent Mobile', help='رقم الجوال - Column 9')

    # EMPLOYEE (column 10)
    related_employee = fields.Char(string='Related Employee', help='الموظف المرتبط بالطالب - Column 10')

    # ACADEMIC INFORMATION (columns 11-15)
    school_name = fields.Char(string='School', help='المدرسة - Column 11')
    division_name = fields.Char(string='Division', help='القسم - Column 12')
    grade_name = fields.Char(string='Grade', help='الصف - Column 13')
    grade_branch = fields.Char(string='Grade Branch', help='فرع الصف - Column 14')
    section = fields.Char(string='Section', help='الشعبة - Column 15')

    # TUITION FEES (columns 16-25)
    tuition_term1 = fields.Float(string='Tuition Term 1', help='رسوم دراسية الفصل الأول - Column 16')
    tuition_term2 = fields.Float(string='Tuition Term 2', help='رسوم دراسية الفصل الثاني - Column 17')
    tuition_term3 = fields.Float(string='Tuition Term 3', help='رسوم دراسية الفصل الثالث - Column 18')
    total_tuition = fields.Float(string='Total Tuition', help='الرسوم الدراسية - Column 19')

    discount_term1 = fields.Float(string='Discount Term 1', help='خصم الفصل الاول - Column 20')
    discount_term2 = fields.Float(string='Discount Term 2', help='خصم الفصل الثاني - Column 21')
    discount_term3 = fields.Float(string='Discount Term 3', help='خصم الفصل الثالث - Column 22')
    total_discount = fields.Float(string='Total Discount', help='الخصومات - Column 23')
    discount_percentage = fields.Char(string='Discount %', help='نسبة الخصومات - Column 24')
    net_tuition = fields.Float(string='Net Tuition', help='صافي القسط الدراسي - Column 25')

    # OTHER FEES (columns 26-33)
    other_fees_total = fields.Float(string='Other Fees Total', help='مجموع الرسوم الاخرى - Column 26')
    transport_term1 = fields.Float(string='Transport Term 1', help='رسوم المواصلات الفصل الاول - Column 27')
    transport_term2 = fields.Float(string='Transport Term 2', help='رسوم المواصلات الفصل الثاني - Column 28')
    transport_term3 = fields.Float(string='Transport Term 3', help='رسوم المواصلات الفصل الثالث - Column 29')
    total_transport = fields.Float(string='Total Transport', help='رسوم المواصلات - Column 30')
    refundable_deposit = fields.Float(string='Refundable Deposit', help='التأمينات المسترد - Column 31')
    boarding_fees = fields.Float(string='Boarding Fees', help='السكن الداخلي - Column 32')
    health_insurance = fields.Float(string='Health Insurance', help='التأمين الصحي - Column 33')

    # VAT (columns 34-37)
    vat_term1 = fields.Float(string='VAT Term 1', help='الضريبة المضافة الفصل الاول - Column 34')
    vat_term2 = fields.Float(string='VAT Term 2', help='الضريبة المضافة الفصل الثاني - Column 35')
    vat_term3 = fields.Float(string='VAT Term 3', help='الضريبة المضافة الفصل الثالث - Column 36')
    total_vat = fields.Float(string='Total VAT', help='الضريبة المضافة - Column 37')

    # TOTALS BEFORE DISCOUNT (columns 38-41)
    total_before_discount_term1 = fields.Float(string='Total Before Discount T1', help='Column 38')
    total_before_discount_term2 = fields.Float(string='Total Before Discount T2', help='Column 39')
    total_before_discount_term3 = fields.Float(string='Total Before Discount T3', help='Column 40')
    total_before_discount = fields.Float(string='Total Before Discount', help='اجمالي المطلوب قبل الخصم - Column 41')

    # TOTALS AFTER DISCOUNT (columns 42-45)
    total_after_discount_term1 = fields.Float(string='Total After Discount T1', help='Column 42')
    total_after_discount_term2 = fields.Float(string='Total After Discount T2', help='Column 43')
    total_after_discount_term3 = fields.Float(string='Total After Discount T3', help='Column 44')
    total_after_discount = fields.Float(string='Total After Discount', help='اجمالي بعد الخصم المطلوب - Column 45')

    # PAYMENTS (columns 46-48)
    amount_paid = fields.Float(string='Amount Paid', help='المبلغ المدفوع - Column 46')
    amount_spent = fields.Float(string='Amount Spent', help='المبلغ المصروف - Column 47')
    amount_transferred = fields.Float(string='Amount Transferred', help='المبلغ المحول - Column 48')

    # BALANCES (columns 49-59)
    opening_balance_debit = fields.Float(string='Opening Balance Debit', help='الرصيد الافتتاحي المدين - Column 49')
    opening_balance_credit = fields.Float(string='Opening Balance Credit', help='الرصيد الافتتاحي الدائن - Column 50')
    carried_balance = fields.Float(string='Carried Balance', help='الرصيد المدور - Column 51')
    sales_receivables = fields.Float(string='Sales Receivables', help='مبيعات ذمم - Column 52')

    balance_term1 = fields.Float(string='Balance Term 1', help='رصيد الفصل الأول - Column 53')
    balance_term2 = fields.Float(string='Balance Term 2', help='رصيد الفصل الثاني - Column 54')
    balance_term3 = fields.Float(string='Balance Term 3', help='رصيد الفصل الثالث - Column 55')
    current_year_balance = fields.Float(string='Current Year Balance', help='رصيد العام الحالي - Column 56')

    final_balance_debit = fields.Float(string='Final Balance Debit', help='الرصيد النهائي المدين - Column 57')
    final_balance_credit = fields.Float(string='Final Balance Credit', help='الرصيد النهائي الدائن - Column 58')
    final_balance = fields.Float(string='Final Balance', help='الرصيد النهائي - Column 59')

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
            name = f"{record.student_name or 'Unknown'} ({record.old_student_id or 'No ID'})"
            result.append((record.id, name))
        return result

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
            'student_id': False,
            'parent_id': False,
        })
