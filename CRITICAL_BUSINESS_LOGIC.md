# ICS EMS - Critical Business Logic & Fields

## Overview

This document describes **CRITICAL business fields** that were added to ensure proper student registration, financial tracking, and data migration from the legacy system.

---

## 🎯 Critical Fields Added

### 1. Legacy System Tracking (ics.student)

#### `old_student_id` - Old System Student ID
- **Type**: Char (indexed)
- **Format**: `20250374` (8 digits: YYYY + NNNN)
- **Purpose**:
  - Match students from legacy system
  - Allow users to search by old ID
  - Link to other legacy data tables
- **Example**: `20250374` = 2025 (year) + 0374 (sequence)
- **Usage**:
  ```python
  # Search by old ID
  student = env['ics.student'].search([
      ('old_student_id', '=', '20250374')
  ])
  ```

#### `old_contract_id` - Old Contract ID
- **Type**: Char (indexed)
- **Format**: Variable (`20256`, `202562`, `2025419`)
- **Purpose**:
  - Link to financial records in legacy system
  - Match payment receipts
  - Reference contract documents
- **Usage**:
  ```python
  # Find student by contract
  student = env['ics.student'].search([
      ('old_contract_id', '=', '2025419')
  ])
  ```

---

### 2. Student Classification (ics.student)

#### `student_type` - Student Type
- **Type**: Selection (required)
- **Values**:
  1. `new` - **New Student** (first time enrollment)
  2. `continuing` - **Continuing Student** (same school, grade promotion)
  3. `transfer_internal` - **Transfer from Al-Tahtheeb School** (different branch)
  4. `transfer_external` - **Transfer from External School** (outside Al-Tahtheeb)

- **Purpose**:
  - Determine admission workflow
  - Check if opening balance exists
  - Apply appropriate registration rules
  - Track student origin

- **Business Rules**:
  | Type | Opening Balance Check | Document Requirements | Admission Test |
  |------|----------------------|----------------------|----------------|
  | New | ❌ No | Full documents | ✅ Yes |
  | Continuing | ✅ **MUST CHECK** | Minimal | ❌ No |
  | Transfer Internal | ✅ **MUST CHECK** | Minimal | ❌ No |
  | Transfer External | ⚠️ Check if exists | Full documents | ✅ Yes |

- **Usage in Admission**:
  ```python
  if application.student_type == 'new':
      # New student - no opening balance
      # Require full admission test
      pass
  elif application.student_type == 'continuing':
      # CRITICAL: Check opening balance before registration
      existing_student = search_by_national_id()
      if existing_student.opening_balance > 0:
          raise Error('Must clear opening balance first!')
  elif application.student_type == 'transfer_internal':
      # Transfer from another Al-Tahtheeb school
      # CRITICAL: Check opening balance
      existing_student = search_by_old_student_id()
      if existing_student.opening_balance > 0:
          raise Error('Must clear balance from previous school!')
  ```

---

### 3. Opening Balance Tracking (ics.student)

#### `opening_balance` - Opening Balance (الرصيد الافتتاحي)
- **Type**: Monetary (tracked)
- **Currency**: Company default currency
- **Purpose**: **MOST CRITICAL FIELD!**
  - Track unpaid amounts from **previous academic years**
  - **BLOCK REGISTRATION** if balance exists
  - Ensure parents clear all dues before new enrollment
  - Import departure balance from legacy system

- **Business Rules**:
  ```
  ⚠️ CRITICAL RULE:
  IF opening_balance > 0 AND NOT balance_cleared:
      → BLOCK new academic year registration
      → BLOCK certificates issuance
      → BLOCK portal access (optional)
      → REQUIRE payment before proceeding
  ```

- **When Set**:
  1. **Data Migration**: Import from `balance_student.xlsx` column 59 (final_balance)
  2. **Year End**: Carry forward unpaid fees to next year
  3. **Manual Adjustment**: By finance staff

- **Example Scenario**:
  ```
  Student: Ahmad (National ID: 1194245021)
  Academic Year 2023-2024:
    - Total Fees: 20,000 SAR
    - Paid: 13,000 SAR
    - Balance: 7,000 SAR (unpaid)

  Year End Process:
    - Carry 7,000 SAR → opening_balance for 2024-2025
    - Ahmad applies for 2024-2025
    - System checks: opening_balance = 7,000 SAR > 0
    - BLOCK registration until parent pays 7,000 SAR
  ```

- **Usage**:
  ```python
  # Check before registration
  if student.opening_balance > 0 and not student.balance_cleared:
      raise UserError(
          f'Cannot register! Outstanding balance from previous years: '
          f'{student.opening_balance} SAR. '
          f'Please clear balance before registration.'
      )
  ```

#### `opening_balance_notes` - Opening Balance Notes
- **Type**: Text
- **Purpose**:
  - Explain source of opening balance
  - Record migration details
  - Note payment arrangements

- **Example**:
  ```
  "Migrated from legacy system: Final balance for 2023-2024 academic year.
   Original student ID: 20250374
   Original contract ID: 2025419
   Includes: Term 2 and Term 3 unpaid tuition."
  ```

#### `balance_cleared` - Balance Cleared Flag
- **Type**: Boolean (tracked)
- **Purpose**:
  - Mark opening balance as fully paid
  - Enable registration for new year
  - Track payment compliance

- **Business Logic**:
  ```python
  # When payment received for opening balance
  if payment_covers_opening_balance():
      student.write({
          'opening_balance': 0.0,
          'balance_cleared': True,
          'balance_cleared_date': fields.Date.today()
      })
      # Now student can register for new year
  ```

#### `balance_cleared_date` - Balance Cleared Date
- **Type**: Date (tracked)
- **Purpose**: Record when balance was cleared

---

## 🔄 Admission & Registration Workflow

### New Student Workflow
```
1. Submit Application (student_type = 'new')
   ├─ Collect documents
   ├─ Schedule admission test
   ├─ Conduct interview
   └─ ✅ No opening balance check

2. Accept Application
   └─ Create student record (opening_balance = 0)

3. Register for Academic Year
   └─ Generate fee invoices
```

### Continuing Student Workflow
```
1. Submit Application (student_type = 'continuing')
   └─ System finds existing student by national_id

2. CHECK OPENING BALANCE ⚠️ CRITICAL
   ├─ IF opening_balance > 0:
   │  ├─ Show outstanding amount
   │  ├─ BLOCK registration
   │  ├─ Notify parent: "Must clear 7,000 SAR before registration"
   │  └─ Wait for payment
   └─ IF opening_balance = 0 OR balance_cleared = True:
      └─ ✅ Allow registration

3. After Payment (if needed)
   ├─ Record payment
   ├─ Update: opening_balance = 0, balance_cleared = True
   └─ Enable registration

4. Register for New Academic Year
   ├─ Update grade (promotion)
   └─ Generate new fee invoices
```

### Transfer Student (Internal) Workflow
```
1. Submit Application (student_type = 'transfer_internal')
   └─ Transfer from another Al-Tahtheeb school

2. FIND EXISTING RECORD
   ├─ Search by national_id
   └─ Search by old_student_id

3. CHECK OPENING BALANCE ⚠️ CRITICAL
   └─ Same as continuing student

4. Transfer Student Record
   ├─ Update school_id
   ├─ Clear opening balance requirement
   └─ Assign to new grade
```

### Transfer Student (External) Workflow
```
1. Submit Application (student_type = 'transfer_external')
   ├─ From outside school
   └─ May or may not have existing record

2. Check if student was previously enrolled
   └─ Search by national_id

3. IF Found (was Al-Tahtheeb student before):
   └─ CHECK OPENING BALANCE ⚠️

4. IF Not Found:
   └─ Treat as new student
   └─ opening_balance = 0
```

---

## 💰 Opening Balance in Admission Application

### Enhanced Outstanding Dues Check

The `_compute_outstanding_dues()` method now checks **THREE sources**:

#### 1. Student's Own Opening Balance
```python
# For continuing/transfer students
if student_type in ['continuing', 'transfer']:
    existing_student = search_by_national_id()
    if existing_student.opening_balance > 0:
        total_outstanding += existing_student.opening_balance
```

#### 2. Current Unpaid Fees
```python
# Unpaid fees from current year
unpaid_fees = search_unpaid_payslips()
total_outstanding += sum(unpaid_fees.due_amount)
```

#### 3. Parent's Other Children Opening Balance
```python
# Check siblings' opening balances
siblings = parent.student_ids
siblings_with_opening_balance = siblings.filtered(
    lambda s: s.opening_balance > 0
)
total_outstanding += sum(siblings.opening_balance)
```

### Registration Block Logic
```python
if application.has_outstanding_dues:
    if application.outstanding_amount > 0:
        raise UserError(
            f'Cannot complete registration!\n\n'
            f'Outstanding dues: {application.outstanding_amount} SAR\n\n'
            f'This includes:\n'
            f'- Opening balance from previous years\n'
            f'- Unpaid fees from current year\n'
            f'- Unpaid fees from siblings\n\n'
            f'Please clear all outstanding dues before registration.'
        )
```

---

## 📊 Fee Payment Tracking (ics.fee.staging)

### Fee Payment Fields (fees.xlsx - 8 columns)

#### `receipt_number` - Receipt Number (رقم السند)
- Format: `20247007`, `20247008`
- Purpose: Unique payment receipt identifier

#### `receipt_date` - Receipt Date (تاريخ السند)
- Excel serial date converted to Odoo date
- Purpose: Payment transaction date

#### `old_student_id` - Old Student ID (رقم الطالب)
- Match student for payment
- Link to `ics.student.old_student_id`

#### `amount` - Payment Amount (المبلغ)
- Payment amount received
- Currency: SAR (default)

#### `status` - Status (الحالة)
- Values: `فعال` (Active) or `ملغي` (Cancelled)
- Only import active payments

#### `cashier_name` - Cashier Name (أمين الصندوق)
- Name of cashier who received payment
- **MAP TO**: `journal_id` (account.journal)

#### `journal_id` - Payment Journal
- **NEW FIELD**: Link to accounting journal
- **Mapping Logic**:
  ```python
  # Find or create journal for cashier
  journal = env['account.journal'].search([
      ('name', 'ilike', cashier_name),
      ('type', '=', 'cash')
  ], limit=1)

  if not journal:
      # Create journal for cashier
      journal = env['account.journal'].create({
          'name': f'Cash - {cashier_name}',
          'type': 'cash',
          'code': generate_code(cashier_name),
      })

  fee_staging.journal_id = journal.id
  ```

---

## 🔍 Search & Matching Logic

### Student Matching Priority

When importing or searching for students:

1. **PRIMARY**: `national_id` (most reliable)
   ```python
   student = search([('national_id', '=', '1194245021')])
   ```

2. **SECONDARY**: `old_student_id` (legacy system)
   ```python
   if not student:
       student = search([('old_student_id', '=', '20250374')])
   ```

3. **TERTIARY**: `student_id` (new EMS ID)
   ```python
   if not student:
       student = search([('student_id', '=', 'STU/2025/0374')])
   ```

4. **LAST RESORT**: `old_contract_id` + `name`
   ```python
   if not student:
       student = search([
           ('old_contract_id', '=', '2025419'),
           ('name', 'ilike', student_name)
       ])
   ```

---

## ⚠️ Critical Business Rules Summary

### ✅ MUST DO

1. **Always check opening_balance** before registration for:
   - Continuing students
   - Transfer students (internal)
   - Transfer students (external, if previously enrolled)

2. **Block registration** if:
   - `opening_balance > 0` AND `NOT balance_cleared`
   - `has_outstanding_dues = True`
   - `outstanding_amount > 0`

3. **Preserve legacy IDs**:
   - Always set `old_student_id` during migration
   - Always set `old_contract_id` during migration
   - Index both fields for fast searching

4. **Track student type**:
   - Set correct `student_type` on admission
   - Use type to determine workflow
   - Apply appropriate checks per type

5. **Record opening balance notes**:
   - Explain source of balance
   - Record migration details
   - Document payment arrangements

### ❌ NEVER DO

1. **Never allow registration** with unpaid opening balance
2. **Never delete** old_student_id or old_contract_id
3. **Never change** student_type after creation (unless correcting error)
4. **Never clear** opening_balance without actual payment
5. **Never ignore** outstanding dues in admission

---

## 📋 Migration Checklist

When migrating from legacy system:

- [ ] Import all students with `old_student_id`
- [ ] Import all students with `old_contract_id`
- [ ] Calculate and set `opening_balance` from final_balance
- [ ] Set `opening_balance_notes` with migration details
- [ ] Set correct `student_type` based on history
- [ ] Import all fee payments with `receipt_number`
- [ ] Map cashier names to journals
- [ ] Verify opening balances match legacy system
- [ ] Test registration workflow with opening balance
- [ ] Verify blocking logic works correctly

---

## 🎓 Examples

### Example 1: New Student (No Opening Balance)
```python
# New student - first time enrollment
student = env['ics.student'].create({
    'name': 'Ahmad Mohammed',
    'national_id': '1234567890',
    'student_type': 'new',
    'opening_balance': 0.0,  # New student, no previous balance
    'old_student_id': False,  # No old ID
    'old_contract_id': False,  # No old contract
})
# Registration: ✅ Allowed immediately
```

### Example 2: Continuing Student (With Opening Balance)
```python
# Student from previous year with unpaid fees
student = env['ics.student'].search([
    ('old_student_id', '=', '20250374')
])

# Check opening balance
if student.opening_balance > 0:
    print(f'Outstanding: {student.opening_balance} SAR')
    print('Must clear before registration!')
    # Registration: ❌ BLOCKED

# After payment
payment = record_payment(amount=student.opening_balance)
student.write({
    'opening_balance': 0.0,
    'balance_cleared': True,
    'balance_cleared_date': today(),
})
# Registration: ✅ Now allowed
```

### Example 3: Transfer Student (Check Opening Balance)
```python
# Student transferring from another Al-Tahtheeb school
application = env['ics.admission.application'].create({
    'student_type': 'transfer_internal',
    'national_id': '1194245021',
    'previous_school': 'Al-Tahtheeb Khobar',
})

# System automatically checks
outstanding_dues = application._compute_outstanding_dues()
if application.has_outstanding_dues:
    # Show message to parent
    message = (
        f'Outstanding dues detected: {application.outstanding_amount} SAR\n'
        f'Please clear all dues before completing registration.'
    )
    # Registration: ❌ BLOCKED until payment
```

---

**This business logic ensures financial compliance and prevents registration with unpaid dues!**
