# ICS EMS Data Import - Complete Field Mapping Guide

## Overview

This document shows the **exact mapping** between:
1. **Excel Columns** (from your legacy system)
2. **Staging Table Fields** (ics.student.balance.staging)
3. **EMS Model Fields** (ics.student, ics.parent, ics.student.payslip)

---

## Student Balance Data (balance_student.xlsx)

### Student Identification

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 2 | رقم الطالب | `old_student_id` | ics.student | - | Used for matching existing students |
| 3 | اسم الطالب | `student_name` | ics.student | `name` | Full name |
| 4 | رقم العقد المالي | `contract_id` | - | - | Contract reference (keep for records) |
| 5 | رقم الهوية/الاقامة لطالب | `student_national_id` | ics.student | `national_id` | **PRIMARY KEY for matching** |

**Student ID Format**: `20250374` (8 digits)
- Format: YYYYNNNN where YYYY = year, NNNN = sequence

**Contract ID Format**: Variable length (e.g., `20256`, `202562`, `2025419`)

### Parent Information

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 6 | رقم ولي الامر | `old_parent_id` | ics.parent | - | Old system reference |
| 7 | أسم ولي الامر | `parent_name` | ics.parent | `name` | Full name |
| 8 | رقم الهوية/الاقامة لولي الأمر | `parent_national_id` | ics.parent | `national_id` | **PRIMARY KEY for matching** |
| 9 | رقم الجوال | `parent_mobile` | ics.parent | `mobile` | Mobile number |

### Employee Relationship

| Excel Column | Arabic Name | Staging Field | Notes |
|--------------|-------------|---------------|-------|
| 10 | الموظف المرتبط بالطالب | `related_employee` | Staff member associated with student (if any) |

### Academic Information

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Mapping Logic |
|--------------|-------------|---------------|-----------|-----------|---------------|
| 11 | المدرسة | `school_name` | ics.school | `name` | Match by name |
| 12 | القسم | `division_name` | ics.division | `name` | Match by name (e.g., "الابتدائي" → Primary) |
| 13 | الصف | `grade_name` | ics.grade | `name` | Match by name (e.g., "الاول" → Grade 1) |
| 14 | فرع الصف | `grade_branch` | - | - | Additional classification |
| 15 | الشعبة | `section` | ics.division | - | Section/Class designation |

**Division Examples**:
- الابتدائي → Primary
- المتوسط → Middle
- الثانوي → Secondary

**Grade Examples**:
- الاول → Grade 1
- الثاني → Grade 2
- etc.

### Tuition Fees

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 16 | رسوم دراسية الفصل الأول | `tuition_term1` | ics.payslip.line | `amount` | Term 1 tuition |
| 17 | رسوم دراسية الفصل الثاني | `tuition_term2` | ics.payslip.line | `amount` | Term 2 tuition |
| 18 | رسوم دراسية الفصل الثالث | `tuition_term3` | ics.payslip.line | `amount` | Term 3 tuition |
| 19 | الرسوم الدراسية | `total_tuition` | ics.student.payslip | `subtotal` | **Total = T1 + T2 + T3** |

### Discounts

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 20 | خصم الفصل الاول | `discount_term1` | ics.payslip.line | `discount_amount` | Term 1 discount |
| 21 | خصم الفصل الثاني | `discount_term2` | ics.payslip.line | `discount_amount` | Term 2 discount |
| 22 | خصم الفصل الثالث | `discount_term3` | ics.payslip.line | `discount_amount` | Term 3 discount |
| 23 | الخصومات | `total_discount` | ics.student.payslip | `discount_amount` | **Total discounts** |
| 24 | نسبة الخصومات | `discount_percentage` | - | - | For reference (e.g., "5.00%") |
| 25 | صافي القسط الدراسي | `net_tuition` | - | - | **Calculated: total_tuition - total_discount** |

### Transportation Fees

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 27 | رسوم المواصلات الفصل الاول | `transport_term1` | ics.payslip.line | `amount` | Term 1 transport |
| 28 | رسوم المواصلات الفصل الثاني | `transport_term2` | ics.payslip.line | `amount` | Term 2 transport |
| 29 | رسوم المواصلات الفصل الثالث | `transport_term3` | ics.payslip.line | `amount` | Term 3 transport |
| 30 | رسوم المواصلات | `total_transport` | - | - | **Total transport fees** |

### Other Fees

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 26 | مجموع الرسوم الاخرى | `other_fees_total` | ics.payslip.line | `amount` | Miscellaneous fees |
| 31 | التأمينات المسترد | `refundable_deposit` | ics.payslip.line | `amount` | Refundable deposit |
| 32 | السكن الداخلي | `boarding_fees` | ics.payslip.line | `amount` | Boarding fees |
| 33 | التأمين الصحي | `health_insurance` | ics.payslip.line | `amount` | Health insurance |

### VAT (Tax)

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 34 | الضريبة المضافة الفصل الاول | `vat_term1` | ics.payslip.line | `tax_amount` | Term 1 VAT |
| 35 | الضريبة المضافة الفصل الثاني | `vat_term2` | ics.payslip.line | `tax_amount` | Term 2 VAT |
| 36 | الضريبة المضافة الفصل الثالث | `vat_term3` | ics.payslip.line | `tax_amount` | Term 3 VAT |
| 37 | الضريبة المضافة | `total_vat` | ics.student.payslip | `tax_amount` | **Total VAT** |

### Totals Before Discount

| Excel Column | Arabic Name | Staging Field | Notes |
|--------------|-------------|---------------|-------|
| 38 | اجمالي المطلوب قبل الخصم الفصل الاول | `total_before_discount_term1` | Term 1 total before discount |
| 39 | اجمالي المطلوب قبل الخصم الفصل الثاني | `total_before_discount_term2` | Term 2 total before discount |
| 40 | اجمالي المطلوب قبل الخصم الفصل الثالث | `total_before_discount_term3` | Term 3 total before discount |
| 41 | اجمالي المطلوب قبل الخصم | `total_before_discount` | **Total before discount** |

### Totals After Discount

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 42 | اجمالي المطلوب بعد الخصم الفصل الاول | `total_after_discount_term1` | - | - | Term 1 after discount |
| 43 | اجمالي المطلوب بعد الخصم الفصل الثاني | `total_after_discount_term2` | - | - | Term 2 after discount |
| 44 | اجمالي المطلوب بعد الخصم الفصل الثالث | `total_after_discount_term3` | - | - | Term 3 after discount |
| 45 | اجمالي بعد الخصم المطلوب | `total_after_discount` | ics.student.payslip | `total` | **FINAL AMOUNT DUE** |

### Payment Information

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 46 | المبلغ المدفوع | `amount_paid` | ics.student.payslip | `paid_amount` | **Total amount paid** |
| 47 | المبلغ المصروف | `amount_spent` | - | - | Amount expensed |
| 48 | المبلغ المحول | `amount_transferred` | - | - | Amount transferred |

### Balance Information

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 49 | الرصيد الافتتاحي المدين | `opening_balance_debit` | - | - | Opening debit balance |
| 50 | الرصيد الافتتاحي الدائن | `opening_balance_credit` | - | - | Opening credit balance |
| 51 | الرصيد المدور | `carried_balance` | - | - | Carried forward balance |
| 52 | مبيعات ذمم | `sales_receivables` | - | - | Sales receivables |
| 53 | رصيد الفصل الأول | `balance_term1` | - | - | Term 1 balance |
| 54 | رصيد الفصل الثاني | `balance_term2` | - | - | Term 2 balance |
| 55 | رصيد الفصل الثالث | `balance_term3` | - | - | Term 3 balance |
| 56 | رصيد العام الحالي | `current_year_balance` | - | - | Current year balance |
| 57 | الرصيد النهائي المدين | `final_balance_debit` | - | - | Final debit balance |
| 58 | الرصيد النهائي الدائن | `final_balance_credit` | - | - | Final credit balance |
| 59 | الرصيد النهائي | `final_balance` | ics.student.payslip | `due_amount` | **OUTSTANDING BALANCE** |

---

## Fee Payment Data (fees.xlsx)

### Payment Record Information

| Excel Column | Arabic Name | Staging Field | EMS Model | EMS Field | Notes |
|--------------|-------------|---------------|-----------|-----------|-------|
| 1 | التسلسل | `sequence_number` | - | - | Sequential number |
| 2 | رقم السند | `receipt_number` | account.payment | `name` | Receipt/voucher number |
| 3 | تاريخ السند | `receipt_date` | account.payment | `date` | Receipt date (Excel serial) |
| 4 | رقم الطالب | `old_student_id` | ics.student | - | **For matching student** |
| 5 | اسم الطالب | `student_name` | ics.student | `name` | Student name (verification) |
| 6 | المبلغ | `amount` | account.payment | `amount` | **Payment amount** |
| 7 | الحالة | `status` | account.payment | `state` | Status (فعال = Active) |
| 8 | أمين الصندوق | `cashier_name` | res.users | `name` | Cashier who received payment |

---

## Migration Logic

### Step 1: Match Existing Records

1. **Find Student**:
   ```python
   student = env['ics.student'].search([
       ('national_id', '=', student_national_id)
   ], limit=1)

   # If not found, try old_student_id match
   if not student:
       student = env['ics.student'].search([
           ('student_id', '=', old_student_id)
       ], limit=1)
   ```

2. **Find Parent**:
   ```python
   parent = env['ics.parent'].search([
       ('national_id', '=', parent_national_id)
   ], limit=1)
   ```

3. **Find School**:
   ```python
   school = env['ics.school'].search([
       ('name', 'ilike', school_name)
   ], limit=1)
   ```

4. **Find Grade**:
   ```python
   grade = env['ics.grade'].search([
       ('name', 'ilike', grade_name),
       ('school_id', '=', school.id)
   ], limit=1)
   ```

### Step 2: Create Missing Records

If student not found, create new:
```python
student_vals = {
    'name': student_name,
    'national_id': student_national_id,
    'school_id': school.id,
    'grade_id': grade.id,
    'academic_year_id': current_academic_year.id,
    # Parse name components from full name
    'first_name': name_parts[0],
    'family_name': name_parts[-1],
    # ... other fields
}
student = env['ics.student'].create(student_vals)
```

If parent not found, create new:
```python
parent_vals = {
    'name': parent_name,
    'national_id': parent_national_id,
    'mobile': parent_mobile,
    'email': f"{parent_national_id}@temp.local",  # Temporary
    'parent_type': 'father',  # Default
}
parent = env['ics.parent'].create(parent_vals)

# Link parent to student
student.write({'parent_ids': [(4, parent.id)]})
```

### Step 3: Create Fee Records (Payslips)

Create payslip with multiple fee lines:
```python
payslip_vals = {
    'student_id': student.id,
    'school_id': school.id,
    'grade_id': grade.id,
    'academic_year_id': academic_year.id,
    'date': fields.Date.today(),
    'line_ids': [
        # Tuition Term 1
        (0, 0, {
            'description': 'Tuition Term 1',
            'amount': tuition_term1,
            'discount_amount': discount_term1,
            'tax_amount': vat_term1,
        }),
        # Tuition Term 2
        (0, 0, {
            'description': 'Tuition Term 2',
            'amount': tuition_term2,
            'discount_amount': discount_term2,
            'tax_amount': vat_term2,
        }),
        # Transportation if > 0
        (0, 0, {
            'description': 'Transportation',
            'amount': total_transport,
        }) if total_transport > 0 else None,
        # Other fees if > 0
        # ... etc
    ],
}
payslip = env['ics.student.payslip'].create(payslip_vals)
```

### Step 4: Record Payments

If amount_paid > 0, create payment record:
```python
payment_vals = {
    'payment_type': 'inbound',
    'partner_id': student.partner_id.id,
    'amount': amount_paid,
    'date': fields.Date.today(),
    'ref': f"Migration - {old_student_id}",
}
payment = env['account.payment'].create(payment_vals)
```

---

## Important Data Considerations

### 1. Student ID Format
- **Old System**: `20250374` (8 digits)
- **Contract ID**: Various formats (`20256`, `202562`, `2025419`)
- **Use national_id as primary matching key** (more reliable)

### 2. Name Parsing
Arabic names typically follow: `[First] [Father] [Grandfather] [Family]`
Example: "ابراهيم احمد ابراهيم ال مسلم"
- first_name: ابراهيم
- father_name: احمد
- grandfather_name: ابراهيم
- family_name: ال مسلم

### 3. Fee Structure
- Tuition divided into 3 terms (semesters)
- Discounts applied per term
- VAT calculated per term
- Final balance = Total - Payments

### 4. Data Validation
Before migration, verify:
- ✅ Student national ID is unique
- ✅ Parent national ID is valid
- ✅ School exists in EMS
- ✅ Grade exists in EMS
- ✅ Amounts are numeric
- ✅ Total calculations match

### 5. Missing Data Handling
- **No parent mobile**: Use placeholder or skip
- **No grade found**: Map to default or prompt user
- **No school found**: Must be created first
- **Invalid amounts**: Set to 0.0 or flag for review

---

## Migration Workflow

### Complete Migration Steps

1. **Pre-Migration**
   - ✅ Install module
   - ✅ Verify schools exist
   - ✅ Verify grades exist
   - ✅ Set current academic year

2. **Import to Staging**
   - Upload balance_student.xlsx
   - Upload fees.xlsx
   - Verify row counts
   - Check sample data

3. **Data Verification**
   - Review staging data
   - Check for duplicates (by national_id)
   - Validate amounts
   - Identify missing schools/grades

4. **Migration Execution**
   - Run automatic migration wizard
   - Review migration log
   - Check created students
   - Check created payslips
   - Verify balances

5. **Post-Migration**
   - Reconcile totals
   - Verify parent-student links
   - Check payment records
   - Generate reports

---

## Field Mapping Summary

### Critical Fields for Migration

**Student Matching** (in order of priority):
1. `student_national_id` → Most reliable
2. `old_student_id` → Secondary match
3. `student_name` → Verification only

**Parent Matching**:
1. `parent_national_id` → Primary key
2. `parent_mobile` → Secondary match
3. `parent_name` → Verification

**Financial Data**:
- `total_after_discount` → Payslip total
- `amount_paid` → Payment amount
- `final_balance` → Outstanding dues

**Academic Data**:
- `school_name` → School lookup
- `division_name` → Division lookup
- `grade_name` → Grade lookup

---

## Quick Reference

### Student Balance: 59 columns
- **Columns 1-15**: Identity & Academic info
- **Columns 16-25**: Tuition & Discounts
- **Columns 26-33**: Other Fees
- **Columns 34-37**: VAT
- **Columns 38-48**: Totals & Payments
- **Columns 49-59**: Balances

### Fees: 8 columns
- **Simple payment records**
- **Link to student by old_student_id**
- **Record payment date and amount**

---

This mapping ensures **100% data preservation** and **intelligent migration** to EMS!
