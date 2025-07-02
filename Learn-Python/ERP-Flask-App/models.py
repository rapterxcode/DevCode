from database import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}>'

# CRM & Customer Management
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    customer_type = db.Column(db.String(20), default='regular')
    credit_limit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    sales_orders = db.relationship('SalesOrder', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

# Vendor Management
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    contact_person = db.Column(db.String(100))
    payment_terms = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    purchase_orders = db.relationship('PurchaseOrder', backref='vendor', lazy=True)

    def __repr__(self):
        return f'<Vendor {self.name}>'

# Inventory Management
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category_ref', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    unit_price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    unit_of_measure = db.Column(db.String(20), default='pcs')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Product {self.name}>'

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)  # 'in', 'out', 'adjustment'
    quantity = db.Column(db.Integer, nullable=False)
    reference_id = db.Column(db.Integer)  # Reference to order/purchase etc
    reference_type = db.Column(db.String(20))  # 'sale', 'purchase', 'adjustment'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    product = db.relationship('Product', backref='stock_movements')

# Purchase Management
class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expected_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, received, cancelled
    total_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy=True, cascade='all, delete-orphan')

class PurchaseOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    received_quantity = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref='purchase_items')

# Sales Management
class SalesOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    so_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    delivery_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    items = db.relationship('SalesOrderItem', backref='sales_order', lazy=True, cascade='all, delete-orphan')

class SalesOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    shipped_quantity = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref='sales_items')

# Accounting & Finance
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_code = db.Column(db.String(20), unique=True, nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)  # asset, liability, equity, revenue, expense
    parent_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    is_active = db.Column(db.Boolean, default=True)
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_number = db.Column(db.String(50), unique=True, nullable=False)
    transaction_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    description = db.Column(db.Text, nullable=False)
    reference_type = db.Column(db.String(20))  # 'sale', 'purchase', 'payment', 'receipt'
    reference_id = db.Column(db.Integer)
    total_amount = db.Column(db.Float, nullable=False)
    entries = db.relationship('TransactionEntry', backref='transaction', lazy=True, cascade='all, delete-orphan')

class TransactionEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    debit_amount = db.Column(db.Float, default=0.0)
    credit_amount = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    account = db.relationship('Account', backref='entries')

# HR Management
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    position = db.Column(db.String(100))
    hire_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    salary = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id', use_alter=True, name='fk_department_manager'))
    employees = db.relationship('Employee', backref='department', lazy=True, 
                               foreign_keys='Employee.department_id')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    hours_worked = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='present')  # present, absent, late, holiday
    employee = db.relationship('Employee', backref='attendance_records')

# Legacy Order models (for backward compatibility)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Float, default=0.0)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

# Enhanced Inventory Management
class InventoryReceive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_number = db.Column(db.String(50), unique=True, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    receive_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, completed
    notes = db.Column(db.Text)
    received_by = db.Column(db.String(100))
    items = db.relationship('InventoryReceiveItem', backref='receive', lazy=True, cascade='all, delete-orphan')
    vendor = db.relationship('Vendor', backref='inventory_receives')
    purchase_order = db.relationship('PurchaseOrder', backref='inventory_receives')

class InventoryReceiveItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_id = db.Column(db.Integer, db.ForeignKey('inventory_receive.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    batch_number = db.Column(db.String(50))
    expiry_date = db.Column(db.Date)
    product = db.relationship('Product', backref='receive_items')

class InventoryIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    issue_type = db.Column(db.String(20), nullable=False)  # 'sale', 'internal', 'adjustment', 'waste'
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, completed
    notes = db.Column(db.Text)
    issued_by = db.Column(db.String(100))
    items = db.relationship('InventoryIssueItem', backref='issue', lazy=True, cascade='all, delete-orphan')
    department = db.relationship('Department', backref='inventory_issues')
    employee = db.relationship('Employee', backref='inventory_issues')

class InventoryIssueItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('inventory_issue.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float)
    reason = db.Column(db.String(100))
    product = db.relationship('Product', backref='issue_items')

class StockCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count_number = db.Column(db.String(50), unique=True, nullable=False)
    count_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    count_type = db.Column(db.String(20), default='full')  # full, cycle, spot
    status = db.Column(db.String(20), default='draft')  # draft, counting, completed, adjusted
    counted_by = db.Column(db.String(100))
    verified_by = db.Column(db.String(100))
    notes = db.Column(db.Text)
    items = db.relationship('StockCountItem', backref='count', lazy=True, cascade='all, delete-orphan')

class StockCountItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count_id = db.Column(db.Integer, db.ForeignKey('stock_count.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    system_quantity = db.Column(db.Integer, default=0)
    counted_quantity = db.Column(db.Integer)
    variance = db.Column(db.Integer, default=0)
    unit_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    product = db.relationship('Product', backref='count_items')

# Enhanced Sales Management
class Quotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    quote_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    valid_until = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, sent, accepted, rejected, expired
    total_amount = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    terms_conditions = db.Column(db.Text)
    prepared_by = db.Column(db.String(100))
    items = db.relationship('QuotationItem', backref='quotation', lazy=True, cascade='all, delete-orphan')
    customer = db.relationship('Customer', backref='quotations')

class QuotationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotation.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    product = db.relationship('Product', backref='quotation_items')

# Tax Invoices
class SalesTaxInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    invoice_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, sent, paid, overdue, cancelled
    subtotal = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    items = db.relationship('SalesTaxInvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    customer = db.relationship('Customer', backref='sales_invoices')
    sales_order = db.relationship('SalesOrder', backref='tax_invoices')

class SalesTaxInvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_tax_invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=7.0)
    description = db.Column(db.Text)
    product = db.relationship('Product', backref='sales_invoice_items')

class PurchaseTaxInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    invoice_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, received, paid, overdue
    subtotal = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    items = db.relationship('PurchaseTaxInvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    vendor = db.relationship('Vendor', backref='purchase_invoices')
    purchase_order = db.relationship('PurchaseOrder', backref='tax_invoices')

class PurchaseTaxInvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('purchase_tax_invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=7.0)
    description = db.Column(db.Text)
    product = db.relationship('Product', backref='purchase_invoice_items')

# CRM Enhancement
class CustomerContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    contact_type = db.Column(db.String(20), nullable=False)  # call, email, meeting, note
    contact_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    subject = db.Column(db.String(200))
    description = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='open')  # open, closed, follow_up
    created_by = db.Column(db.String(100))
    customer = db.relationship('Customer', backref='contacts')

class VendorContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    contact_type = db.Column(db.String(20), nullable=False)  # call, email, meeting, note
    contact_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    subject = db.Column(db.String(200))
    description = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='open')  # open, closed, follow_up
    created_by = db.Column(db.String(100))
    vendor = db.relationship('Vendor', backref='contacts')

# Enhanced Finance Management
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(20), default='checking')  # checking, savings, credit
    balance = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    transactions = db.relationship('BankTransaction', backref='bank_account', lazy=True)

class BankTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, transfer
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    reference_number = db.Column(db.String(50))
    balance_after = db.Column(db.Float)

# Enhanced HR Management
class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)
    basic_salary = db.Column(db.Float, default=0.0)
    overtime_hours = db.Column(db.Float, default=0.0)
    overtime_rate = db.Column(db.Float, default=0.0)
    allowances = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    tax_deduction = db.Column(db.Float, default=0.0)
    social_security = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # draft, approved, paid
    pay_date = db.Column(db.Date)
    employee = db.relationship('Employee', backref='payrolls')

class PerformanceEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    evaluation_period_start = db.Column(db.Date, nullable=False)
    evaluation_period_end = db.Column(db.Date, nullable=False)
    overall_rating = db.Column(db.Float)  # 1-5 scale
    goals_achievement = db.Column(db.Float)
    skills_assessment = db.Column(db.Float)
    communication = db.Column(db.Float)
    teamwork = db.Column(db.Float)
    leadership = db.Column(db.Float)
    comments = db.Column(db.Text)
    improvement_areas = db.Column(db.Text)
    goals_next_period = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, completed, approved
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    employee = db.relationship('Employee', backref='evaluations', foreign_keys=[employee_id])
    evaluator = db.relationship('Employee', backref='evaluations_given', foreign_keys=[evaluator_id])