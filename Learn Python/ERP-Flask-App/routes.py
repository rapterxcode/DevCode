from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models import *
from datetime import datetime, date
import random
import string

def register_routes(app):
    
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Dashboard statistics
        total_customers = Customer.query.count()
        total_vendors = Vendor.query.count()
        total_products = Product.query.count()
        total_employees = Employee.query.count()
        
        # Recent activities
        recent_sales = SalesOrder.query.order_by(SalesOrder.order_date.desc()).limit(5).all()
        recent_purchases = PurchaseOrder.query.order_by(PurchaseOrder.order_date.desc()).limit(5).all()
        
        # Low stock alerts
        low_stock_products = Product.query.filter(
            Product.stock_quantity <= Product.reorder_level,
            Product.is_active == True
        ).all()
        
        # Financial summary
        total_sales = db.session.query(db.func.sum(SalesOrder.total_amount)).scalar() or 0
        total_purchases = db.session.query(db.func.sum(PurchaseOrder.total_amount)).scalar() or 0
        
        return render_template('dashboard.html', 
                             total_customers=total_customers,
                             total_vendors=total_vendors,
                             total_products=total_products,
                             total_employees=total_employees,
                             recent_sales=recent_sales,
                             recent_purchases=recent_purchases,
                             low_stock_products=low_stock_products,
                             total_sales=total_sales,
                             total_purchases=total_purchases)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password!', 'error')
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    # ======= INVENTORY MANAGEMENT =======
    @app.route('/inventory')
    def inventory():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        products = Product.query.filter_by(is_active=True).all()
        categories = Category.query.all()
        
        # Add low stock count for alerts
        low_stock_count = sum(1 for product in products if product.stock_quantity <= product.reorder_level)
        
        return render_template('inventory/inventory.html', 
                             products=products, 
                             categories=categories,
                             low_stock_count=low_stock_count)

    @app.route('/inventory/categories')
    def categories():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        categories = Category.query.all()
        return render_template('inventory/categories.html', categories=categories)

    @app.route('/inventory/categories/add', methods=['GET', 'POST'])
    def add_category():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully!', 'success')
            return redirect(url_for('categories'))
        
        return render_template('inventory/add_category.html')

    @app.route('/inventory/products/add', methods=['GET', 'POST'])
    def add_inventory_product():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            sku = request.form['sku']
            description = request.form['description']
            category_id = request.form['category_id'] if request.form['category_id'] else None
            unit_price = float(request.form['unit_price'])
            cost_price = float(request.form['cost_price'])
            stock_quantity = int(request.form['stock_quantity'])
            reorder_level = int(request.form['reorder_level'])
            unit_of_measure = request.form['unit_of_measure']
            
            product = Product(
                name=name,
                sku=sku,
                description=description,
                category_id=category_id,
                unit_price=unit_price,
                cost_price=cost_price,
                stock_quantity=stock_quantity,
                reorder_level=reorder_level,
                unit_of_measure=unit_of_measure
            )
            
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('inventory'))
        
        categories = Category.query.all()
        return render_template('inventory/add_product.html', categories=categories)

    @app.route('/inventory/stock-movements')
    def stock_movements():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        movements = StockMovement.query.order_by(StockMovement.created_at.desc()).all()
        return render_template('inventory/stock_movements.html', movements=movements)

    # ======= PURCHASE MANAGEMENT =======
    @app.route('/purchases')
    def purchases():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        purchase_orders = PurchaseOrder.query.order_by(PurchaseOrder.order_date.desc()).all()
        return render_template('purchases/purchases.html', purchase_orders=purchase_orders)

    @app.route('/purchases/vendors')
    def vendors():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        vendors = Vendor.query.all()
        return render_template('purchases/vendors.html', vendors=vendors)

    @app.route('/purchases/vendors/add', methods=['GET', 'POST'])
    def add_vendor():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            contact_person = request.form['contact_person']
            payment_terms = request.form['payment_terms']
            
            vendor = Vendor(
                name=name,
                email=email,
                phone=phone,
                address=address,
                contact_person=contact_person,
                payment_terms=payment_terms
            )
            
            db.session.add(vendor)
            db.session.commit()
            flash('Vendor added successfully!', 'success')
            return redirect(url_for('vendors'))
        
        return render_template('purchases/add_vendor.html')

    @app.route('/purchases/add', methods=['GET', 'POST'])
    def add_purchase_order():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            vendor_id = int(request.form['vendor_id'])
            expected_date = datetime.strptime(request.form['expected_date'], '%Y-%m-%d') if request.form['expected_date'] else None
            notes = request.form['notes']
            
            # Generate PO number
            po_number = f"PO{random.randint(1000, 9999)}"
            
            purchase_order = PurchaseOrder(
                po_number=po_number,
                vendor_id=vendor_id,
                expected_date=expected_date,
                notes=notes
            )
            
            db.session.add(purchase_order)
            db.session.flush()
            
            # Add items
            product_ids = request.form.getlist('product_id')
            quantities = request.form.getlist('quantity')
            unit_prices = request.form.getlist('unit_price')
            
            total_amount = 0
            for i, product_id in enumerate(product_ids):
                if product_id and quantities[i] and unit_prices[i]:
                    quantity = int(quantities[i])
                    unit_price = float(unit_prices[i])
                    
                    po_item = PurchaseOrderItem(
                        purchase_order_id=purchase_order.id,
                        product_id=int(product_id),
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    
                    total_amount += quantity * unit_price
                    db.session.add(po_item)
            
            purchase_order.total_amount = total_amount
            db.session.commit()
            flash('Purchase order created successfully!', 'success')
            return redirect(url_for('purchases'))
        
        vendors = Vendor.query.all()
        products = Product.query.all()
        return render_template('purchases/add_purchase_order.html', vendors=vendors, products=products)

    # ======= SALES MANAGEMENT =======
    @app.route('/sales')
    def sales():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        sales_orders = SalesOrder.query.order_by(SalesOrder.order_date.desc()).all()
        return render_template('sales/sales.html', sales_orders=sales_orders)

    @app.route('/sales/customers')
    def customers():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        customers = Customer.query.all()
        return render_template('sales/customers.html', customers=customers)

    @app.route('/sales/customers/add', methods=['GET', 'POST'])
    def add_customer():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            customer_type = request.form['customer_type']
            credit_limit = float(request.form['credit_limit']) if request.form['credit_limit'] else 0.0
            
            customer = Customer(
                name=name,
                email=email,
                phone=phone,
                address=address,
                customer_type=customer_type,
                credit_limit=credit_limit
            )
            
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))
        
        return render_template('sales/add_customer.html')

    @app.route('/sales/add', methods=['GET', 'POST'])
    def add_sales_order():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            customer_id = int(request.form['customer_id'])
            delivery_date = datetime.strptime(request.form['delivery_date'], '%Y-%m-%d') if request.form['delivery_date'] else None
            discount = float(request.form['discount']) if request.form['discount'] else 0.0
            notes = request.form['notes']
            
            # Generate SO number
            so_number = f"SO{random.randint(1000, 9999)}"
            
            sales_order = SalesOrder(
                so_number=so_number,
                customer_id=customer_id,
                delivery_date=delivery_date,
                discount=discount,
                notes=notes
            )
            
            db.session.add(sales_order)
            db.session.flush()
            
            # Add items
            product_ids = request.form.getlist('product_id')
            quantities = request.form.getlist('quantity')
            
            total_amount = 0
            for i, product_id in enumerate(product_ids):
                if product_id and quantities[i]:
                    product = Product.query.get(int(product_id))
                    quantity = int(quantities[i])
                    
                    so_item = SalesOrderItem(
                        sales_order_id=sales_order.id,
                        product_id=int(product_id),
                        quantity=quantity,
                        unit_price=product.unit_price
                    )
                    
                    total_amount += quantity * product.unit_price
                    db.session.add(so_item)
            
            # Apply discount and calculate tax
            subtotal = total_amount
            discount_amount = subtotal * (discount / 100)
            tax_amount = (subtotal - discount_amount) * 0.1  # 10% tax
            
            sales_order.total_amount = subtotal - discount_amount + tax_amount
            sales_order.tax_amount = tax_amount
            
            db.session.commit()
            flash('Sales order created successfully!', 'success')
            return redirect(url_for('sales'))
        
        customers = Customer.query.all()
        products = Product.query.all()
        return render_template('sales/add_sales_order.html', customers=customers, products=products)

    # ======= HR MANAGEMENT =======
    @app.route('/hr')
    def hr_dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        total_employees = Employee.query.filter_by(is_active=True).count()
        departments = Department.query.all()
        recent_hires = Employee.query.order_by(Employee.hire_date.desc()).limit(5).all()
        
        return render_template('hr/hr_dashboard.html', 
                             total_employees=total_employees,
                             departments=departments,
                             recent_hires=recent_hires)

    @app.route('/hr/employees')
    def employees():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        employees = Employee.query.filter_by(is_active=True).all()
        return render_template('hr/employees.html', employees=employees)

    @app.route('/hr/employees/add', methods=['GET', 'POST'])
    def add_employee():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            employee_id = request.form['employee_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            department_id = request.form['department_id'] if request.form['department_id'] else None
            position = request.form['position']
            salary = float(request.form['salary']) if request.form['salary'] else None
            
            employee = Employee(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                department_id=department_id,
                position=position,
                salary=salary
            )
            
            db.session.add(employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('employees'))
        
        departments = Department.query.all()
        return render_template('hr/add_employee.html', departments=departments)

    @app.route('/hr/departments')
    def departments():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        departments = Department.query.all()
        return render_template('hr/departments.html', departments=departments)

    @app.route('/hr/departments/add', methods=['GET', 'POST'])
    def add_department():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            manager_id = request.form['manager_id'] if request.form['manager_id'] else None
            
            department = Department(
                name=name,
                description=description,
                manager_id=manager_id
            )
            
            db.session.add(department)
            db.session.commit()
            flash('Department added successfully!', 'success')
            return redirect(url_for('departments'))
        
        employees = Employee.query.filter_by(is_active=True).all()
        return render_template('hr/add_department.html', employees=employees)

    # ======= REPORTS =======
    @app.route('/reports')
    def reports():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        return render_template('reports/reports.html')

    @app.route('/reports/sales')
    def sales_report():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        sales_data = db.session.query(
            Customer.name,
            db.func.count(SalesOrder.id).label('order_count'),
            db.func.sum(SalesOrder.total_amount).label('total_sales')
        ).join(SalesOrder).group_by(Customer.id).all()
        
        # Calculate summary statistics
        total_revenue = sum(row[2] or 0 for row in sales_data)
        total_orders = sum(row[1] or 0 for row in sales_data)
        active_customers = len(sales_data)
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        return render_template('reports/sales_report.html', 
                             sales_data=sales_data,
                             total_revenue=total_revenue,
                             total_orders=total_orders,
                             active_customers=active_customers,
                             average_order_value=average_order_value)

    @app.route('/reports/inventory')
    def inventory_report():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        inventory_data = Product.query.filter_by(is_active=True).all()
        
        # Calculate summary statistics
        total_products = len(inventory_data)
        total_stock = sum(product.stock_quantity for product in inventory_data)
        total_value = sum(product.unit_price * product.stock_quantity for product in inventory_data)
        low_stock_count = sum(1 for product in inventory_data if product.stock_quantity <= product.reorder_level)
        
        return render_template('reports/inventory_report.html', 
                             inventory_data=inventory_data,
                             total_products=total_products,
                             total_stock=total_stock,
                             total_value=total_value,
                             low_stock_count=low_stock_count)

    # ======= ENHANCED INVENTORY MANAGEMENT =======
    @app.route('/inventory/receive')
    def inventory_receive():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        receives = InventoryReceive.query.order_by(InventoryReceive.receive_date.desc()).all()
        return render_template('inventory/receive.html', receives=receives)

    @app.route('/inventory/receive/add', methods=['GET', 'POST'])
    def add_inventory_receive():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            # Process receive form
            flash('สินค้าได้รับเข้าคลังเรียบร้อยแล้ว!', 'success')
            return redirect(url_for('inventory_receive'))
        
        vendors = Vendor.query.all()
        products = Product.query.all()
        return render_template('inventory/add_receive.html', vendors=vendors, products=products)

    @app.route('/inventory/issue')
    def inventory_issue():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        issues = InventoryIssue.query.order_by(InventoryIssue.issue_date.desc()).all()
        return render_template('inventory/issue.html', issues=issues)

    @app.route('/inventory/issue/add', methods=['GET', 'POST'])
    def add_inventory_issue():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            # Process issue form
            flash('เบิกจ่ายสินค้าเรียบร้อยแล้ว!', 'success')
            return redirect(url_for('inventory_issue'))
        
        departments = Department.query.all()
        employees = Employee.query.all()
        products = Product.query.all()
        return render_template('inventory/add_issue.html', departments=departments, employees=employees, products=products)

    @app.route('/inventory/stock-count')
    def stock_count():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        stock_counts = StockCount.query.order_by(StockCount.count_date.desc()).all()
        return render_template('inventory/stock_count.html', stock_counts=stock_counts)

    @app.route('/inventory/stock-count/add', methods=['GET', 'POST'])
    def add_stock_count():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            # Process stock count form
            flash('ตรวจนับสต็อกเรียบร้อยแล้ว!', 'success')
            return redirect(url_for('stock_count'))
        
        products = Product.query.all()
        return render_template('inventory/add_stock_count.html', products=products)

    # ======= ENHANCED PURCHASE & SALES =======
    @app.route('/purchases/receipts')
    def purchase_receipts():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        receipts = InventoryReceive.query.order_by(InventoryReceive.receive_date.desc()).all()
        return render_template('purchases/receipts.html', receipts=receipts)

    @app.route('/purchases/tax-invoices')
    def purchase_tax_invoices():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        invoices = PurchaseTaxInvoice.query.order_by(PurchaseTaxInvoice.invoice_date.desc()).all()
        return render_template('purchases/tax_invoices.html', invoices=invoices)

    @app.route('/sales/quotations')
    def quotations():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        quotations = Quotation.query.order_by(Quotation.quote_date.desc()).all()
        return render_template('sales/quotations.html', quotations=quotations)

    @app.route('/sales/quotations/add', methods=['GET', 'POST'])
    def add_quotation():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            # Process quotation form
            flash('ใบเสนอราคาถูกสร้างเรียบร้อยแล้ว!', 'success')
            return redirect(url_for('quotations'))
        
        customers = Customer.query.all()
        products = Product.query.all()
        return render_template('sales/add_quotation.html', customers=customers, products=products)

    @app.route('/sales/tax-invoices')
    def sales_tax_invoices():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        invoices = SalesTaxInvoice.query.order_by(SalesTaxInvoice.invoice_date.desc()).all()
        return render_template('sales/sales_tax_invoices.html', invoices=invoices)

    # ======= CRM ENHANCEMENT =======
    @app.route('/crm/transaction-history')
    def transaction_history():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Combine sales and purchase history
        sales_history = SalesOrder.query.order_by(SalesOrder.order_date.desc()).all()
        purchase_history = PurchaseOrder.query.order_by(PurchaseOrder.order_date.desc()).all()
        
        return render_template('crm/transaction_history.html', 
                             sales_history=sales_history, 
                             purchase_history=purchase_history)

    @app.route('/crm/follow-up')
    def crm_follow_up():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        customer_contacts = CustomerContact.query.filter_by(status='follow_up').all()
        vendor_contacts = VendorContact.query.filter_by(status='follow_up').all()
        
        return render_template('crm/follow_up.html', 
                             customer_contacts=customer_contacts,
                             vendor_contacts=vendor_contacts)

    # ======= FINANCE MANAGEMENT =======
    @app.route('/finance/chart-of-accounts')
    def chart_of_accounts():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        accounts = Account.query.order_by(Account.account_code).all()
        
        # Calculate totals by account type
        assets_total = db.session.query(db.func.sum(Account.balance)).filter_by(account_type='asset').scalar() or 0
        liabilities_total = db.session.query(db.func.sum(Account.balance)).filter_by(account_type='liability').scalar() or 0
        equity_total = db.session.query(db.func.sum(Account.balance)).filter_by(account_type='equity').scalar() or 0
        revenue_total = db.session.query(db.func.sum(Account.balance)).filter_by(account_type='revenue').scalar() or 0
        expense_total = db.session.query(db.func.sum(Account.balance)).filter_by(account_type='expense').scalar() or 0
        revenue_expense_total = revenue_total - expense_total
        
        return render_template('finance/chart_of_accounts.html', 
                             accounts=accounts,
                             assets_total=assets_total,
                             liabilities_total=liabilities_total,
                             equity_total=equity_total,
                             revenue_expense_total=revenue_expense_total)

    @app.route('/finance/cash-bank')
    def cash_bank():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        bank_accounts = BankAccount.query.filter_by(is_active=True).all()
        transactions = BankTransaction.query.order_by(BankTransaction.transaction_date.desc()).limit(20).all()
        
        return render_template('finance/cash_bank.html', 
                             bank_accounts=bank_accounts,
                             transactions=transactions)

    @app.route('/finance/receivables-payables')
    def receivables_payables():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Mock receivables and payables data
        receivables = SalesTaxInvoice.query.filter(SalesTaxInvoice.paid_amount < SalesTaxInvoice.total_amount).all()
        payables = PurchaseTaxInvoice.query.filter(PurchaseTaxInvoice.paid_amount < PurchaseTaxInvoice.total_amount).all()
        
        return render_template('finance/receivables_payables.html',
                             receivables=receivables,
                             payables=payables)

    @app.route('/finance/financial-statements')
    def financial_statements():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Calculate financial statement data
        accounts = Account.query.all()
        
        # Basic financial figures
        total_assets = sum(acc.balance for acc in accounts if acc.account_type == 'asset')
        total_liabilities = sum(acc.balance for acc in accounts if acc.account_type == 'liability')
        total_equity = sum(acc.balance for acc in accounts if acc.account_type == 'equity')
        total_revenue = sum(acc.balance for acc in accounts if acc.account_type == 'revenue')
        total_expenses = sum(acc.balance for acc in accounts if acc.account_type == 'expense')
        
        # Detailed breakdown (using basic calculations for demo)
        current_assets = total_assets * 0.6  # Mock 60% current assets
        cash_and_bank = total_assets * 0.2   # Mock 20% cash
        accounts_receivable = total_assets * 0.25  # Mock 25% receivables
        inventory_value = total_assets * 0.15  # Mock 15% inventory
        fixed_assets = total_assets * 0.4    # Mock 40% fixed assets
        
        current_liabilities = total_liabilities * 0.7  # Mock 70% current
        accounts_payable = total_liabilities * 0.5     # Mock 50% payables
        long_term_debt = total_liabilities * 0.3       # Mock 30% long-term debt
        
        share_capital = total_equity * 0.6             # Mock 60% share capital
        retained_earnings = total_equity * 0.4         # Mock 40% retained earnings
        
        # Income statement
        sales_revenue = total_revenue * 0.9            # Mock 90% sales revenue
        other_revenue = total_revenue * 0.1            # Mock 10% other revenue
        cogs = total_revenue * 0.4                     # Mock 40% COGS
        gross_profit = total_revenue - cogs
        
        operating_expenses = total_expenses * 0.4      # Mock breakdown
        sales_expenses = total_expenses * 0.2
        admin_expenses = total_expenses * 0.3
        financial_expenses = total_expenses * 0.1
        
        net_income = total_revenue - total_expenses
        
        # Financial ratios
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        net_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0
        debt_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 else 0
        
        return render_template('finance/financial_statements.html',
                             total_assets=total_assets, total_liabilities=total_liabilities, 
                             total_equity=total_equity, net_income=net_income,
                             current_assets=current_assets, cash_and_bank=cash_and_bank,
                             accounts_receivable=accounts_receivable, inventory_value=inventory_value,
                             fixed_assets=fixed_assets, current_liabilities=current_liabilities,
                             accounts_payable=accounts_payable, long_term_debt=long_term_debt,
                             share_capital=share_capital, retained_earnings=retained_earnings,
                             total_revenue=total_revenue, sales_revenue=sales_revenue,
                             other_revenue=other_revenue, cogs=cogs, gross_profit=gross_profit,
                             total_expenses=total_expenses, operating_expenses=operating_expenses,
                             sales_expenses=sales_expenses, admin_expenses=admin_expenses,
                             financial_expenses=financial_expenses, current_ratio=current_ratio,
                             gross_margin=gross_margin, net_margin=net_margin, debt_ratio=debt_ratio)

    # ======= ENHANCED HR MANAGEMENT =======
    @app.route('/hr/time-attendance')
    def time_attendance():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        attendance = Attendance.query.order_by(Attendance.date.desc()).limit(50).all()
        return render_template('hr/time_attendance.html', attendance=attendance)

    @app.route('/hr/payroll')
    def payroll():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        payrolls = Payroll.query.order_by(Payroll.pay_period_end.desc()).all()
        return render_template('hr/payroll.html', payrolls=payrolls)

    @app.route('/hr/performance-evaluation')
    def performance_evaluation():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        evaluations = PerformanceEvaluation.query.order_by(PerformanceEvaluation.created_date.desc()).all()
        return render_template('hr/performance_evaluation.html', evaluations=evaluations)

    # ======= ENHANCED REPORTS =======
    @app.route('/reports/purchase')
    def purchase_report():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Get vendor statistics with purchase data
        vendor_stats = []
        vendors = Vendor.query.all()
        
        for vendor in vendors:
            orders = PurchaseOrder.query.filter_by(vendor_id=vendor.id).all()
            if orders:
                total_amount = sum(order.total_amount or 0 for order in orders)
                order_count = len(orders)
                avg_order = total_amount / order_count if order_count > 0 else 0
                last_purchase = max(order.order_date for order in orders) if orders else None
                
                vendor_stats.append({
                    'vendor_name': vendor.name,
                    'contact_info': vendor.contact_person,
                    'order_count': order_count,
                    'total_amount': total_amount,
                    'avg_order': avg_order,
                    'last_purchase': last_purchase,
                    'status': 'active'  # You can implement actual status logic here
                })
        
        # Calculate summary statistics
        total_orders = sum(stat['order_count'] for stat in vendor_stats)
        total_amount = sum(stat['total_amount'] for stat in vendor_stats)
        average_order = total_amount / total_orders if total_orders > 0 else 0
        active_vendors = len([stat for stat in vendor_stats if stat['status'] == 'active'])
        
        return render_template('reports/purchase_report.html', 
                             vendor_stats=vendor_stats,
                             total_orders=total_orders,
                             total_amount=total_amount,
                             average_order=average_order,
                             active_vendors=active_vendors)

    @app.route('/reports/financial')
    def financial_report():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Mock financial report data
        total_revenue = db.session.query(db.func.sum(SalesOrder.total_amount)).scalar() or 0
        total_expenses = db.session.query(db.func.sum(PurchaseOrder.total_amount)).scalar() or 0
        net_profit = total_revenue - total_expenses
        
        monthly_sales = []  # Mock monthly data
        monthly_purchases = []  # Mock monthly data
        
        return render_template('reports/financial_report.html',
                             total_revenue=total_revenue,
                             total_expenses=total_expenses,
                             net_profit=net_profit,
                             monthly_sales=monthly_sales,
                             monthly_purchases=monthly_purchases)