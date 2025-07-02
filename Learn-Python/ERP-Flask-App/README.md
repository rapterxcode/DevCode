# 🏢 ERP Flask Application / ระบบ ERP ด้วย Flask

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-orange.svg)](https://sqlalchemy.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)

A comprehensive Enterprise Resource Planning (ERP) system built with Python Flask, featuring modern responsive UI and complete business management capabilities.

ระบบการวางแผนทรัพยากรองค์กร (ERP) ที่ครอบคลุม พัฒนาด้วย Python Flask พร้อมส่วนติดต่อผู้ใช้ที่ทันสมัยและความสามารถในการจัดการธุรกิจที่สมบูรณ์

## 📋 Table of Contents / สารบัญ

- [🎯 Overview / ภาพรวม](#-overview--ภาพรวม)
- [✨ Features / ฟีเจอร์](#-features--ฟีเจอร์)
- [🚀 Installation / การติดตั้ง](#-installation--การติดตั้ง)
- [📖 Usage / วิธีการใช้งาน](#-usage--วิธีการใช้งาน)
- [🏗️ Project Structure / โครงสร้างโครงการ](#%EF%B8%8F-project-structure--โครงสร้างโครงการ)
- [🛠️ Development Guide / คู่มือการพัฒนา](#%EF%B8%8F-development-guide--คู่มือการพัฒนา)
- [📋 Menu Functions / ฟังก์ชันเมนูต่างๆ](#-menu-functions--ฟังก์ชันเมนูต่างๆ)
- [💾 Database Models / โมเดลฐานข้อมูล](#-database-models--โมเดลฐานข้อมูล)
- [🔧 Configuration / การตั้งค่า](#-configuration--การตั้งค่า)
- [🚨 Troubleshooting / การแก้ไขปัญหา](#-troubleshooting--การแก้ไขปัญหา)

## 🎯 Overview / ภาพรวม

This ERP system is designed to streamline business operations with integrated modules for inventory management, sales, purchasing, human resources, customer relationship management, and financial accounting. Built with modern web technologies and responsive design.

ระบบ ERP นี้ออกแบบมาเพื่อปรับปรุงการดำเนินงานทางธุรกิจด้วยโมดูลที่รวมเข้าด้วยกันสำหรับการจัดการสินค้าคงคลัง การขาย การจัดซื้อ ทรัพยากรบุคคล การจัดการลูกค้า และการบัญชีการเงิน

### 🎨 Key Highlights / จุดเด่นหลัก

- **Modern UI/UX** - Bootstrap 5 with responsive design / ส่วนติดต่อผู้ใช้ทันสมัยด้วย Bootstrap 5
- **Multi-language Support** - Thai and English interface / รองรับภาษาไทยและอังกฤษ
- **Real-time Dashboard** - Live business metrics / แดชบอร์ดแบบเรียลไทม์
- **Mobile Responsive** - Works on all devices / ใช้งานได้บนทุกอุปกรณ์
- **Modular Architecture** - Easy to extend / สถาปัตยกรรมแบบโมดูลาร์

## ✨ Features / ฟีเจอร์

### 📦 Inventory Management / การจัดการคลังสินค้า
- ✅ **Product Management** / การจัดการสินค้า
  - Product database with SKU tracking / ฐานข้อมูลสินค้าพร้อมการติดตาม SKU
  - Category management / การจัดการหมวดหมู่
  - Multi-unit pricing / การกำหนดราคาหลายหน่วย
  
- ✅ **Stock Control** / การควบคุมสต็อก
  - Real-time stock tracking / การติดตามสต็อกแบบเรียลไทม์
  - Low stock alerts / การแจ้งเตือนสินค้าใกล้หมด
  - Stock movement history / ประวัติการเคลื่อนไหวสต็อก

- ✅ **Warehouse Operations** / การดำเนินงานคลังสินค้า
  - Goods receiving / การรับสินค้า
  - Stock issue management / การจัดการเบิกจ่ายสินค้า
  - Physical stock counting / การตรวจนับสต็อกจริง
  - Batch/lot tracking / การติดตามล็อต/ชุด

### 🛒 Purchase & Sales / การซื้อและขาย

#### Purchase Management / การจัดการการซื้อ
- ✅ **Purchase Orders** / ใบสั่งซื้อ
  - Create and track purchase orders / สร้างและติดตามใบสั่งซื้อ
  - Multi-vendor support / รองรับผู้ขายหลายราย
  - Approval workflow / ขั้นตอนการอนุมัติ

- ✅ **Vendor Management** / การจัดการผู้ขาย
  - Vendor database / ฐานข้อมูลผู้ขาย
  - Payment terms tracking / การติดตามเงื่อนไขการชำระเงิน
  - Performance analytics / การวิเคราะห์ประสิทธิภาพ

#### Sales Management / การจัดการการขาย
- ✅ **Sales Orders** / ใบสั่งขาย
  - Order processing / การประมวลผลคำสั่งซื้อ
  - Customer order tracking / การติดตามคำสั่งซื้อของลูกค้า
  - Delivery management / การจัดการการส่งมอบ

- ✅ **Quotation System** / ระบบใบเสนอราคา
  - Professional quotations / ใบเสนอราคาระดับมืออาชีพ
  - Quote to order conversion / การแปลงใบเสนอราคาเป็นคำสั่งซื้อ
  - Validity tracking / การติดตามความใช้ได้

### 👥 Customer Relationship Management (CRM)
- ✅ **Customer Database** / ฐานข้อมูลลูกค้า
  - Complete customer profiles / โปรไฟล์ลูกค้าที่สมบูรณ์
  - Credit limit management / การจัดการวงเงินเครดิต
  - Transaction history / ประวัติการทำธุรกรรม

- ✅ **Follow-up Management** / การจัดการติดตาม
  - Contact scheduling / การจัดตารางติดต่อ
  - Activity tracking / การติดตามกิจกรรม
  - Customer interaction history / ประวัติการติดต่อกับลูกค้า

### 💰 Finance & Accounting / การเงินและบัญชี
- ✅ **Chart of Accounts** / ผังบัญชี
  - Hierarchical account structure / โครงสร้างบัญชีแบบลำดับชั้น
  - Account balance tracking / การติดตามยอดคงเหลือบัญชี
  - Account type management / การจัดการประเภทบัญชี

- ✅ **Cash & Bank Management** / การจัดการเงินสดและธนาคาร
  - Multiple bank accounts / บัญชีธนาคารหลายบัญชี
  - Transaction recording / การบันทึกรายการ
  - Bank reconciliation / การกระทบยอดธนาคาร

- ✅ **Accounts Receivable & Payable** / ลูกหนี้และเจ้าหนี้
  - Outstanding invoice tracking / การติดตามใบแจ้งหนี้ค้างชำระ
  - Payment scheduling / การจัดตารางการชำระเงิน
  - Aging analysis / การวิเคราะห์อายุหนี้

- ✅ **Financial Statements** / งบการเงิน
  - Balance sheet / งบดุล
  - Income statement / งบกำไรขาดทุน
  - Financial ratios / อัตราส่วนทางการเงิน

### 👨‍💼 Human Resources / ทรัพยากรบุคคล
- ✅ **Employee Management** / การจัดการพนักงาน
  - Employee database / ฐานข้อมูลพนักงาน
  - Department assignments / การมอบหมายแผนก
  - Position tracking / การติดตามตำแหน่ง

- ✅ **Time & Attendance** / เวลาและการเข้างาน
  - Check-in/out tracking / การติดตามเข้า-ออกงาน
  - Working hours calculation / การคำนวณชั่วโมงทำงาน
  - Attendance reports / รายงานการเข้างาน

- ✅ **Payroll Management** / การจัดการเงินเดือน
  - Salary processing / การประมวลผลเงินเดือน
  - Deductions and allowances / การหักและเบี้ยเลี้ยง
  - Payslip generation / การสร้างสลิปเงินเดือน

- ✅ **Performance Evaluation** / การประเมินผลงาน
  - 360-degree evaluations / การประเมิน 360 องศา
  - Goal tracking / การติดตามเป้าหมาย
  - Performance analytics / การวิเคราะห์ผลงาน

### 📊 Reports & Analytics / รายงานและการวิเคราะห์
- ✅ **Sales Reports** / รายงานการขาย
  - Sales performance analysis / การวิเคราะห์ประสิทธิภาพการขาย
  - Customer analytics / การวิเคราะห์ลูกค้า
  - Product performance / ประสิทธิภาพสินค้า

- ✅ **Purchase Reports** / รายงานการซื้อ
  - Vendor performance / ประสิทธิภาพผู้ขาย
  - Cost analysis / การวิเคราะห์ต้นทุน
  - Purchase trends / แนวโน้มการซื้อ

- ✅ **Inventory Reports** / รายงานสินค้าคงคลัง
  - Stock valuation / การประเมินค่าสต็อก
  - Movement analysis / การวิเคราะห์การเคลื่อนไหว
  - ABC analysis / การวิเคราะห์ ABC

- ✅ **Financial Reports** / รายงานการเงิน
  - Profit & loss / กำไรขาดทุน
  - Cash flow / กระแสเงินสด
  - Financial ratios / อัตราส่วนทางการเงิน

## 🚀 Installation / การติดตั้ง

### Prerequisites / ข้อกำหนดเบื้องต้น

Before installing, ensure you have the following installed on your system:
ก่อนติดตั้ง ตรวจสอบให้แน่ใจว่าคุณมีสิ่งต่อไปนี้ติดตั้งในระบบของคุณ:

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads/)

### Step-by-Step Installation / ขั้นตอนการติดตั้งทีละขั้น

#### 1. Clone the Repository / โคลนที่เก็บโค้ด
```bash
git clone https://github.com/your-username/ERP-Flask-App.git
cd ERP-Flask-App
```

#### 2. Create Virtual Environment / สร้าง Virtual Environment
```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies / ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Initialize Database / เริ่มต้นฐานข้อมูล
```bash
# Create database with sample data
python reset_enhanced_db.py
```

#### 5. Run the Application / รันแอปพลิเคชัน
```bash
python app.py
```

#### 6. Access the Application / เข้าถึงแอปพลิเคชัน
Open your web browser and navigate to: `http://localhost:5000`
เปิดเว็บเบราว์เซอร์และไปที่: `http://localhost:5000`

## 🔑 Default Login Credentials / ข้อมูลการเข้าสู่ระบบเริ่มต้น

| Role / บทบาท | Username | Password | Access Level / ระดับการเข้าถึง |
|---------------|----------|----------|---------------------------|
| **Administrator** | `admin` | `admin123` | Full system access / เข้าถึงระบบทั้งหมด |
| **Manager** | `manager` | `manager123` | Management functions / ฟังก์ชันการจัดการ |
| **Staff** | `staff` | `staff123` | Basic operations / การดำเนินงานพื้นฐาน |

## 📖 Usage / วิธีการใช้งาน

### Getting Started / เริ่มต้นใช้งาน

#### 1. Login / การเข้าสู่ระบบ
1. Navigate to `http://localhost:5000`
2. Enter your username and password / ใส่ชื่อผู้ใช้และรหัสผ่าน
3. Click "Login" to access the system / คลิก "Login" เพื่อเข้าสู่ระบบ

#### 2. Dashboard Overview / ภาพรวมแดชบอร์ด
After logging in, you'll see the main dashboard with:
หลังจากเข้าสู่ระบบ คุณจะเห็นแดชบอร์ดหลักที่มี:

- **Key Performance Indicators (KPIs)** / ตัวชี้วัดหลัก
- **Recent Activities** / กิจกรรมล่าสุด
- **Low Stock Alerts** / การแจ้งเตือนสินค้าใกล้หมด
- **Financial Summary** / สรุปทางการเงิน

#### 3. Navigation / การนำทาง
- **Sidebar Menu** - Use the collapsible left sidebar to navigate between modules
  เมนูด้านข้าง - ใช้แถบด้านซ้ายที่ยุบได้เพื่อนำทางระหว่างโมดูล

- **Breadcrumb Navigation** - Track your current location within the system
  การนำทางแบบ Breadcrumb - ติดตามตำแหน่งปัจจุบันของคุณในระบบ

- **Quick Actions** - Access frequently used functions via toolbar buttons
  การดำเนินการด่วน - เข้าถึงฟังก์ชันที่ใช้บ่อยผ่านปุ่มแถบเครื่องมือ

### Basic Operations / การดำเนินงานพื้นฐาน

#### Adding New Records / การเพิ่มข้อมูลใหม่
1. Navigate to the desired module / ไปยังโมดูลที่ต้องการ
2. Click the "Add" or "New" button / คลิกปุ่ม "Add" หรือ "New"
3. Fill in the required fields / กรอกข้อมูลในช่องที่จำเป็น
4. Click "Save" to create the record / คลิก "Save" เพื่อสร้างข้อมูล

#### Viewing and Editing Records / การดูและแก้ไขข้อมูล
1. Browse the list of records in table format / เรียกดูรายการข้อมูลในรูปแบบตาราง
2. Click on a record to view details / คลิกที่ข้อมูลเพื่อดูรายละเอียด
3. Use "Edit" button to modify information / ใช้ปุ่ม "Edit" เพื่อแก้ไขข้อมูล
4. Save changes when done / บันทึกการเปลี่ยนแปลงเมื่อเสร็จสิ้น

#### Generating Reports / การสร้างรายงาน
1. Go to the Reports module / ไปที่โมดูลรายงาน
2. Select the type of report needed / เลือกประเภทรายงานที่ต้องการ
3. Set date ranges and filters / ตั้งค่าช่วงวันที่และตัวกรอง
4. Click "Generate" to create the report / คลิก "Generate" เพื่อสร้างรายงาน

## 🏗️ Project Structure / โครงสร้างโครงการ

```
ERP-Flask-App/
├── 📄 app.py                          # Main application entry point / จุดเข้าแอปพลิเคชันหลัก
├── 🗄️ database.py                     # Database configuration / การตั้งค่าฐานข้อมูล
├── 📊 models.py                       # Database models (40+ models) / โมเดลฐานข้อมูล (40+ โมเดล)
├── 🛤️ routes.py                       # URL routes and business logic / เส้นทาง URL และตรรกะทางธุรกิจ
├── 🔄 reset_enhanced_db.py           # Database initialization with sample data / เริ่มต้นฐานข้อมูลพร้อมข้อมูลตัวอย่าง
├── 📋 requirements.txt               # Python dependencies / dependencies ของ Python
├── 📖 README.md                      # Project documentation / เอกสารโครงการ
│
├── 📁 instance/                      # Instance-specific configuration / การตั้งค่าเฉพาะอินสแตนซ์
│   └── 🗄️ erp.db                    # SQLite database file / ไฟล์ฐานข้อมูล SQLite
│
├── 📁 static/                        # Static assets / ทรัพยากรแบบคงที่
│   ├── 🎨 css/                       # Custom stylesheets / สไตล์ชีตแบบกำหนดเอง
│   ├── 📜 js/                        # JavaScript files / ไฟล์ JavaScript
│   └── 🖼️ images/                   # Image assets / ทรัพยากรรูปภาพ
│
└── 📁 templates/                     # Jinja2 HTML templates / เทมเพลต HTML ของ Jinja2
    ├── 🏠 base.html                  # Base template with navigation / เทมเพลตพื้นฐานพร้อมการนำทาง
    ├── 📊 dashboard.html             # Main dashboard / แดชบอร์ดหลัก
    ├── 🔐 login.html                 # Login page / หน้าเข้าสู่ระบบ
    │
    ├── 📦 inventory/                 # Inventory management templates / เทมเพลตการจัดการสินค้าคงคลัง
    │   ├── inventory.html            # Product listing / รายการสินค้า
    │   ├── categories.html           # Category management / การจัดการหมวดหมู่
    │   ├── stock_movements.html      # Stock movement tracking / การติดตามการเคลื่อนไหวสต็อก
    │   ├── receive.html              # Goods receiving / การรับสินค้า
    │   ├── issue.html                # Stock issuance / การเบิกจ่ายสต็อก
    │   └── stock_count.html          # Physical counting / การตรวจนับจริง
    │
    ├── 🛒 purchases/                 # Purchase management templates / เทมเพลตการจัดการการซื้อ
    │   ├── purchases.html            # Purchase orders / ใบสั่งซื้อ
    │   ├── vendors.html              # Vendor management / การจัดการผู้ขาย
    │   ├── receipts.html             # Purchase receipts / ใบรับสินค้า
    │   └── tax_invoices.html         # Tax invoices / ใบกำกับภาษี
    │
    ├── 💼 sales/                     # Sales management templates / เทมเพลตการจัดการการขาย
    │   ├── sales.html                # Sales orders / ใบสั่งขาย
    │   ├── customers.html            # Customer management / การจัดการลูกค้า
    │   ├── quotations.html           # Quotation management / การจัดการใบเสนอราคา
    │   └── sales_tax_invoices.html   # Sales tax invoices / ใบกำกับภาษีขาย
    │
    ├── 👥 crm/                       # CRM templates / เทมเพลต CRM
    │   ├── transaction_history.html  # Transaction tracking / การติดตามธุรกรรม
    │   └── follow_up.html            # Follow-up management / การจัดการติดตาม
    │
    ├── 💰 finance/                   # Finance templates / เทมเพลตการเงิน
    │   ├── chart_of_accounts.html    # Chart of accounts / ผังบัญชี
    │   ├── cash_bank.html            # Cash & bank management / การจัดการเงินสดและธนาคาร
    │   ├── receivables_payables.html # A/R & A/P management / การจัดการลูกหนี้และเจ้าหนี้
    │   └── financial_statements.html # Financial statements / งบการเงิน
    │
    ├── 👨‍💼 hr/                        # HR templates / เทมเพลต HR
    │   ├── employees.html            # Employee management / การจัดการพนักงาน
    │   ├── departments.html          # Department management / การจัดการแผนก
    │   ├── time_attendance.html      # Time & attendance / เวลาและการเข้างาน
    │   ├── payroll.html              # Payroll management / การจัดการเงินเดือน
    │   └── performance_evaluation.html # Performance reviews / การประเมินผลงาน
    │
    └── 📊 reports/                   # Report templates / เทมเพลตรายงาน
        ├── sales_report.html         # Sales analytics / การวิเคราะห์การขาย
        ├── purchase_report.html      # Purchase analytics / การวิเคราะห์การซื้อ
        ├── inventory_report.html     # Inventory analytics / การวิเคราะห์สินค้าคงคลัง
        └── financial_report.html     # Financial analytics / การวิเคราะห์การเงิน
```

## 🛠️ Development Guide / คู่มือการพัฒนา

### Architecture Overview / ภาพรวมสถาปัตยกรรม

The application follows the **MVC (Model-View-Controller)** pattern:
แอปพลิเคชันใช้รูปแบบ **MVC (Model-View-Controller)**:

- **Models** (`models.py`) - Database entities and relationships / เอนทิตีฐานข้อมูลและความสัมพันธ์
- **Views** (`templates/`) - User interface templates / เทมเพลตส่วนติดต่อผู้ใช้
- **Controllers** (`routes.py`) - Business logic and request handling / ตรรกะทางธุรกิจและการจัดการคำขอ

### Adding New Features / การเพิ่มฟีเจอร์ใหม่

#### 1. Create Database Model / สร้างโมเดลฐานข้อมูล

```python
# In models.py
class NewFeature(db.Model):
    __tablename__ = 'new_feature'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    items = db.relationship('NewFeatureItem', backref='feature', lazy=True)
    
    def __repr__(self):
        return f'<NewFeature {self.name}>'
```

#### 2. Add Routes / เพิ่มเส้นทาง

```python
# In routes.py
@app.route('/new-feature')
def new_feature_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    features = NewFeature.query.filter_by(is_active=True).all()
    return render_template('new_feature/list.html', features=features)

@app.route('/new-feature/add', methods=['GET', 'POST'])
def add_new_feature():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        feature = NewFeature(name=name, description=description)
        db.session.add(feature)
        db.session.commit()
        
        flash('Feature added successfully!', 'success')
        return redirect(url_for('new_feature_list'))
    
    return render_template('new_feature/add.html')
```

#### 3. Create Templates / สร้างเทมเพลต

```html
<!-- templates/new_feature/list.html -->
{% extends "base.html" %}

{% block title %}New Features - ERP System{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h3 mb-0">New Features</h1>
    <a href="{{ url_for('add_new_feature') }}" class="btn btn-primary">
        <i class="fas fa-plus me-2"></i>Add Feature
    </a>
</div>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for feature in features %}
                    <tr>
                        <td>{{ feature.name }}</td>
                        <td>{{ feature.description or 'No description' }}</td>
                        <td>{{ feature.created_at.strftime('%d/%m/%Y') }}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary">Edit</button>
                            <button class="btn btn-sm btn-outline-info">View</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

#### 4. Update Navigation / อัปเดตการนำทาง

```html
<!-- In templates/base.html -->
<li class="nav-item">
    <a class="nav-link collapsed" href="#" data-bs-toggle="collapse" 
       data-bs-target="#newFeatureSubmenu" aria-expanded="false">
        <i class="fas fa-star"></i>
        <span>New Features</span>
        <i class="fas fa-caret-down ms-auto"></i>
    </a>
    <div class="collapse" id="newFeatureSubmenu">
        <ul class="nav flex-column ms-3">
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('new_feature_list') }}">
                    <i class="fas fa-list"></i> List Features
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('add_new_feature') }}">
                    <i class="fas fa-plus"></i> Add Feature
                </a>
            </li>
        </ul>
    </div>
</li>
```

### Database Migration / การย้ายฐานข้อมูล

When adding new models or modifying existing ones:
เมื่อเพิ่มโมเดลใหม่หรือแก้ไขโมเดลที่มีอยู่:

```bash
# Backup current database
cp instance/erp.db instance/erp_backup.db

# Reset database with new schema
python reset_enhanced_db.py
```

### Code Standards / มาตรฐานโค้ด

#### Python Code Style / รูปแบบโค้ด Python
- Follow **PEP 8** guidelines / ปฏิบัติตามแนวทาง PEP 8
- Use descriptive variable names / ใช้ชื่อตัวแปรที่อธิบายได้
- Add docstrings for functions / เพิ่ม docstring สำหรับฟังก์ชัน
- Keep functions under 50 lines / ให้ฟังก์ชันสั้นกว่า 50 บรรทัด

#### Template Standards / มาตรฐานเทมเพลต
- Use consistent Bootstrap classes / ใช้คลาส Bootstrap อย่างสม่ำเสมอ
- Add ARIA labels for accessibility / เพิ่มป้ายกำกับ ARIA เพื่อการเข้าถึง
- Include Thai and English text / รวมข้อความภาษาไทยและอังกฤษ
- Maintain responsive design / รักษาการออกแบบที่ตอบสนอง

#### Database Standards / มาตรฐานฐานข้อมูล
- Use meaningful table names / ใช้ชื่อตารางที่มีความหมาย
- Add appropriate indexes / เพิ่มดัชนีที่เหมาะสม
- Define foreign key relationships / กำหนดความสัมพันธ์คีย์ต่างประเทศ
- Include created_at timestamps / รวมเวลาแสตมป์ created_at

## 📋 Menu Functions / ฟังก์ชันเมนูต่างๆ

### 📦 Inventory Module / โมดูลคลังสินค้า

#### Product Management / การจัดการสินค้า
- **Route**: `/inventory`
- **Function**: `inventory()`
- **Template**: `templates/inventory/inventory.html`

**Features / ฟีเจอร์:**
- ✅ View all products with pagination / ดูสินค้าทั้งหมดแบบแบ่งหน้า
- ✅ Filter by category and status / กรองตามหมวดหมู่และสถานะ
- ✅ Search by name or SKU / ค้นหาตามชื่อหรือ SKU
- ✅ Low stock alerts / การแจ้งเตือนสินค้าใกล้หมด
- ✅ Bulk operations / การดำเนินการกลุ่ม

**Usage Example / ตัวอย่างการใช้งาน:**
```python
# Get products with low stock
low_stock_products = Product.query.filter(
    Product.stock_quantity <= Product.reorder_level,
    Product.is_active == True
).all()
```

#### Categories Management / การจัดการหมวดหมู่
- **Route**: `/inventory/categories`
- **Function**: `categories()`
- **Template**: `templates/inventory/categories.html`

**Features / ฟีเจอร์:**
- ✅ Create/Edit/Delete categories / สร้าง/แก้ไข/ลบหมวดหมู่
- ✅ Category hierarchy support / รองรับลำดับชั้นหมวดหมู่
- ✅ Product count per category / จำนวนสินค้าต่อหมวดหมู่

#### Stock Movements / การเคลื่อนไหวสต็อก
- **Route**: `/inventory/stock-movements`
- **Function**: `stock_movements()`
- **Template**: `templates/inventory/stock_movements.html`

**Features / ฟีเจอร์:**
- ✅ Track all stock changes / ติดตามการเปลี่ยนแปลงสต็อกทั้งหมด
- ✅ Movement types: IN, OUT, ADJUSTMENT / ประเภทการเคลื่อนไหว: เข้า, ออก, ปรับปรุง
- ✅ Reference tracking / การติดตามอ้างอิง
- ✅ Date range filtering / การกรองช่วงวันที่

#### Inventory Receive / การรับสินค้าเข้าคลัง
- **Route**: `/inventory/receive`
- **Function**: `inventory_receive()`
- **Template**: `templates/inventory/receive.html`

**Features / ฟีเจอร์:**
- ✅ Receive goods from vendors / รับสินค้าจากผู้ขาย
- ✅ Link to purchase orders / เชื่อมโยงกับใบสั่งซื้อ
- ✅ Batch/lot tracking / การติดตามล็อต/ชุด
- ✅ Quality inspection notes / บันทึกการตรวจสอบคุณภาพ

#### Inventory Issue / การเบิกจ่ายสินค้า
- **Route**: `/inventory/issue`
- **Function**: `inventory_issue()`
- **Template**: `templates/inventory/issue.html`

**Features / ฟีเจอร์:**
- ✅ Issue goods to departments / เบิกสินค้าให้แผนก
- ✅ Multiple issue types / ประเภทการเบิกหลายแบบ
- ✅ Employee assignment / การมอบหมายพนักงาน
- ✅ Return management / การจัดการของคืน

#### Stock Count / การตรวจนับสต็อก
- **Route**: `/inventory/stock-count`
- **Function**: `stock_count()`
- **Template**: `templates/inventory/stock_count.html`

**Features / ฟีเจอร์:**
- ✅ Physical stock counting / การนับสต็อกจริง
- ✅ Count types: Full, Cycle, Spot / ประเภทการนับ: เต็ม, วงจร, จุด
- ✅ Variance analysis / การวิเคราะห์ความแตกต่าง
- ✅ Adjustment processing / การประมวลผลการปรับปรุง

### 🛒 Purchase Module / โมดูลการจัดซื้อ

#### Purchase Orders / ใบสั่งซื้อ
- **Route**: `/purchases`
- **Function**: `purchases()`
- **Template**: `templates/purchases/purchases.html`

**Features / ฟีเจอร์:**
- ✅ Create multi-item purchase orders / สร้างใบสั่งซื้อหลายรายการ
- ✅ Order status tracking / การติดตามสถานะคำสั่งซื้อ
- ✅ Approval workflow / ขั้นตอนการอนุมัติ
- ✅ Expected delivery dates / วันที่คาดว่าจะส่งมอบ

#### Vendor Management / การจัดการผู้ขาย
- **Route**: `/purchases/vendors`
- **Function**: `vendors()`
- **Template**: `templates/purchases/vendors.html`

**Features / ฟีเจอร์:**
- ✅ Comprehensive vendor database / ฐานข้อมูลผู้ขายที่ครอบคลุม
- ✅ Payment terms management / การจัดการเงื่อนไขการชำระเงิน
- ✅ Contact person tracking / การติดตามบุคคลติดต่อ
- ✅ Performance analytics / การวิเคราะห์ประสิทธิภาพ

#### Purchase Receipts / ใบรับสินค้า
- **Route**: `/purchases/receipts`
- **Function**: `purchase_receipts()`
- **Template**: `templates/purchases/receipts.html`

**Features / ฟีเจอร์:**
- ✅ Goods receiving documentation / เอกสารการรับสินค้า
- ✅ Quality inspection records / บันทึกการตรวจสอบคุณภาพ
- ✅ Partial delivery support / รองรับการส่งมอบบางส่วน
- ✅ Discrepancy reporting / การรายงานความผิดปกติ

### 💼 Sales Module / โมดูลการขาย

#### Sales Orders / ใบสั่งขาย
- **Route**: `/sales`
- **Function**: `sales()`
- **Template**: `templates/sales/sales.html`

**Features / ฟีเจอร์:**
- ✅ Multi-item sales orders / ใบสั่งขายหลายรายการ
- ✅ Customer order processing / การประมวลผลคำสั่งซื้อของลูกค้า
- ✅ Discount management / การจัดการส่วนลด
- ✅ Tax calculation / การคำนวณภาษี
- ✅ Delivery scheduling / การจัดตารางการส่งมอบ

#### Customer Management / การจัดการลูกค้า
- **Route**: `/sales/customers`
- **Function**: `customers()`
- **Template**: `templates/sales/customers.html`

**Features / ฟีเจอร์:**
- ✅ Complete customer profiles / โปรไฟล์ลูกค้าที่สมบูรณ์
- ✅ Credit limit tracking / การติดตามวงเงินเครดิต
- ✅ Customer type classification / การจำแนกประเภทลูกค้า
- ✅ Sales history / ประวัติการขาย

#### Quotations / ใบเสนอราคา
- **Route**: `/sales/quotations`
- **Function**: `quotations()`
- **Template**: `templates/sales/quotations.html`

**Features / ฟีเจอร์:**
- ✅ Professional quotation generation / การสร้างใบเสนอราคาระดับมืออาชีพ
- ✅ Quote validity tracking / การติดตามความใช้ได้ของใบเสนอราคา
- ✅ Terms and conditions / ข้อตกลงและเงื่อนไข
- ✅ Quote to order conversion / การแปลงใบเสนอราคาเป็นคำสั่งซื้อ

### 👥 CRM Module / โมดูล CRM

#### Transaction History / ประวัติการทำธุรกรรม
- **Route**: `/crm/transaction-history`
- **Function**: `transaction_history()`
- **Template**: `templates/crm/transaction_history.html`

**Features / ฟีเจอร์:**
- ✅ Complete transaction timeline / ไทม์ไลน์ธุรกรรมที่สมบูรณ์
- ✅ Customer interaction history / ประวัติการติดต่อกับลูกค้า
- ✅ Sales pipeline tracking / การติดตามช่องทางการขาย
- ✅ Activity logging / การบันทึกกิจกรรม

#### Follow-up Management / การจัดการติดตาม
- **Route**: `/crm/follow-up`
- **Function**: `crm_follow_up()`
- **Template**: `templates/crm/follow_up.html`

**Features / ฟีเจอร์:**
- ✅ Scheduled follow-up activities / กิจกรรมติดตามที่กำหนดเวลา
- ✅ Reminder system / ระบบแจ้งเตือน
- ✅ Contact logging / การบันทึกการติดต่อ
- ✅ Opportunity tracking / การติดตามโอกาส

### 💰 Finance Module / โมดูลการเงิน

#### Chart of Accounts / ผังบัญชี
- **Route**: `/finance/chart-of-accounts`
- **Function**: `chart_of_accounts()`
- **Template**: `templates/finance/chart_of_accounts.html`

**Features / ฟีเจอร์:**
- ✅ Hierarchical account structure / โครงสร้างบัญชีแบบลำดับชั้น
- ✅ Account type classification / การจำแนกประเภทบัญชี
- ✅ Balance tracking / การติดตามยอดคงเหลือ
- ✅ Financial summary / สรุปทางการเงิน

#### Cash & Bank Management / การจัดการเงินสดและธนาคาร
- **Route**: `/finance/cash-bank`
- **Function**: `cash_bank()`
- **Template**: `templates/finance/cash_bank.html`

**Features / ฟีเจอร์:**
- ✅ Multiple bank account support / รองรับบัญชีธนาคารหลายบัญชี
- ✅ Transaction recording / การบันทึกรายการ
- ✅ Balance reconciliation / การกระทบยอดยอดคงเหลือ
- ✅ Cash flow tracking / การติดตามกระแสเงินสด

### 👨‍💼 HR Module / โมดูลทรัพยากรบุคคล

#### Employee Management / การจัดการพนักงาน
- **Route**: `/hr/employees`
- **Function**: `employees()`
- **Template**: `templates/hr/employees.html`

**Features / ฟีเจอร์:**
- ✅ Comprehensive employee records / บันทึกพนักงานที่ครอบคลุม
- ✅ Department assignments / การมอบหมายแผนก
- ✅ Position hierarchy / ลำดับชั้นตำแหน่ง
- ✅ Employment history / ประวัติการทำงาน

#### Time & Attendance / เวลาและการเข้างาน
- **Route**: `/hr/time-attendance`
- **Function**: `time_attendance()`
- **Template**: `templates/hr/time_attendance.html`

**Features / ฟีเจอร์:**
- ✅ Check-in/out tracking / การติดตามเข้า-ออกงาน
- ✅ Working hours calculation / การคำนวณชั่วโมงทำงาน
- ✅ Overtime management / การจัดการชั่วโมงล่วงเวลา
- ✅ Attendance analytics / การวิเคราะห์การเข้างาน

#### Payroll Management / การจัดการเงินเดือน
- **Route**: `/hr/payroll`
- **Function**: `payroll()`
- **Template**: `templates/hr/payroll.html`

**Features / ฟีเจอร์:**
- ✅ Automated salary calculation / การคำนวณเงินเดือนอัตโนมัติ
- ✅ Deductions and allowances / การหักและเบี้ยเลี้ยง
- ✅ Tax computation / การคำนวณภาษี
- ✅ Payslip generation / การสร้างสลิปเงินเดือน

### 📊 Reports Module / โมดูลรายงาน

#### Sales Reports / รายงานการขาย
- **Route**: `/reports/sales`
- **Function**: `sales_report()`
- **Template**: `templates/reports/sales_report.html`

**Features / ฟีเจอร์:**
- ✅ Sales performance analysis / การวิเคราะห์ประสิทธิภาพการขาย
- ✅ Customer analytics / การวิเคราะห์ลูกค้า
- ✅ Product performance / ประสิทธิภาพสินค้า
- ✅ Revenue trends / แนวโน้มรายได้

#### Purchase Reports / รายงานการซื้อ
- **Route**: `/reports/purchase`
- **Function**: `purchase_report()`
- **Template**: `templates/reports/purchase_report.html`

**Features / ฟีเจอร์:**
- ✅ Vendor performance analysis / การวิเคราะห์ประสิทธิภาพผู้ขาย
- ✅ Cost analysis / การวิเคราะห์ต้นทุน
- ✅ Purchase trends / แนวโน้มการซื้อ
- ✅ Savings opportunities / โอกาสประหยัด

## 💾 Database Models / โมเดลฐานข้อมูล

### Core Models / โมเดลหลัก

#### User Authentication / การรับรองตัตนผู้ใช้
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

#### Product Management / การจัดการสินค้า
```python
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
```

### Relationship Patterns / รูปแบบความสัมพันธ์

#### One-to-Many Relationships / ความสัมพันธ์หนึ่งต่อกลุ่ม
```python
# Customer → Sales Orders
class Customer(db.Model):
    # ... fields ...
    sales_orders = db.relationship('SalesOrder', backref='customer', lazy=True)

class SalesOrder(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # ... other fields ...
```

#### Many-to-Many Relationships / ความสัมพันธ์กลุ่มต่อกลุ่ม
```python
# Products ↔ Purchase Orders (through PurchaseOrderItem)
class PurchaseOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
```

#### Self-referencing Relationships / ความสัมพันธ์อ้างอิงตนเอง
```python
# Account hierarchy
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    # ... other fields ...
```

### Database Schema Overview / ภาพรวมโครงสร้างฐานข้อมูล

The database contains **40+ interconnected tables** organized into logical modules:
ฐานข้อมูลมี**ตารางที่เชื่อมโยงกันมากกว่า 40 ตาราง** จัดระเบียบเป็นโมดูลตรรกะ:

1. **Authentication** (2 tables) / การรับรองตัวตน (2 ตาราง)
2. **Inventory** (8 tables) / สินค้าคงคลัง (8 ตาราง)
3. **Sales** (6 tables) / การขาย (6 ตาราง)
4. **Purchases** (6 tables) / การซื้อ (6 ตาราง)
5. **Finance** (8 tables) / การเงิน (8 ตาราง)
6. **HR** (6 tables) / ทรัพยากรบุคคล (6 ตาราง)
7. **CRM** (4 tables) / CRM (4 ตาราง)

## 🔧 Configuration / การตั้งค่า

### Environment Variables / ตัวแปรสภาพแวดล้อม

Create a `.env` file in the project root:
สร้างไฟล์ `.env` ในรูทโครงการ:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-super-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///instance/erp.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Application Settings
APP_NAME=ERP Flask Application
APP_VERSION=1.0.0
DEFAULT_LANGUAGE=en
TIMEZONE=Asia/Bangkok

# Security Settings
SESSION_TIMEOUT=3600
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS=5
```

### Database Configuration / การตั้งค่าฐานข้อมูล

```python
# database.py
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/erp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
```

### Application Settings / การตั้งค่าแอปพลิเคชัน

```python
# app.py
app.config.update(
    # Security
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    
    # File uploads
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    UPLOAD_FOLDER='static/uploads',
    
    # Internationalization
    LANGUAGES=['en', 'th'],
    BABEL_DEFAULT_LOCALE='en',
    BABEL_DEFAULT_TIMEZONE='Asia/Bangkok'
)
```

## 🚨 Troubleshooting / การแก้ไขปัญหา

### Common Issues / ปัญหาที่พบบ่อย

#### 1. Template Not Found Errors
```
jinja2.exceptions.TemplateNotFound: template_name.html
```

**Solution / วิธีแก้ไข:**
```bash
# Check if template file exists
ls templates/module_name/template_name.html

# If missing, create the template file
mkdir -p templates/module_name
touch templates/module_name/template_name.html
```

#### 2. Database Connection Issues
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked
```

**Solution / วิธีแก้ไข:**
```bash
# Stop the application
# Delete the database file
rm instance/erp.db

# Recreate the database
python reset_enhanced_db.py
```

#### 3. Import Errors
```
ModuleNotFoundError: No module named 'flask'
```

**Solution / วิธีแก้ไข:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. Permission Denied Errors
```
PermissionError: [Errno 13] Permission denied: 'instance/erp.db'
```

**Solution / วิธีแก้ไข:**
```bash
# Check directory permissions
ls -la instance/

# Fix permissions
chmod 755 instance/
chmod 644 instance/erp.db
```

#### 5. Port Already in Use
```
OSError: [Errno 98] Address already in use
```

**Solution / วิธีแก้ไข:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <process_id>

# Or use a different port
python app.py --port 5001
```

### Debug Mode / โหมดดีบัก

Enable debug mode for development:
เปิดใช้โหมดดีบักสำหรับการพัฒนา:

```python
# app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Logging / การบันทึกล็อก

Add logging for troubleshooting:
เพิ่มการบันทึกล็อกสำหรับการแก้ไขปัญหา:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

## 🚀 Production Deployment / การติดตั้งใช้งานจริง

### Using Gunicorn / การใช้ Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker / การใช้ Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Environment Variables for Production / ตัวแปรสภาพแวดล้อมสำหรับการใช้งานจริง
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=your-production-database-url
```

## 🤝 Contributing / การมีส่วนร่วม

### How to Contribute / วิธีการมีส่วนร่วม

1. **Fork the repository** / แยกที่เก็บโค้ด
2. **Create a feature branch** / สร้างแบรนช์ฟีเจอร์
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** / ทำการเปลี่ยนแปลง
4. **Test thoroughly** / ทดสอบอย่างละเอียด
5. **Commit your changes** / คอมมิตการเปลี่ยนแปลง
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch** / พุชไปยังแบรนช์
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** / เปิด Pull Request

### Code Review Process / กระบวนการตรวจสอบโค้ด

- All code must pass existing tests / โค้ดทั้งหมดต้องผ่านการทดสอบที่มีอยู่
- New features must include tests / ฟีเจอร์ใหม่ต้องมีการทดสอบ
- Follow the established code style / ปฏิบัติตามรูปแบบโค้ดที่กำหนด
- Update documentation as needed / อัปเดตเอกสารตามความจำเป็น

## 📄 License / ใบอนุญาต

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

โครงการนี้อยู่ภายใต้ **ใบอนุญาต MIT** - ดูรายละเอียดในไฟล์ [LICENSE](LICENSE)

## 🙏 Acknowledgments / กิตติกรรมประกาศ

- **Flask Framework** - Web framework foundation / รากฐานเว็บเฟรมเวิร์ก
- **Bootstrap** - UI component library / ไลบรารีคอมโพเนนต์ UI
- **SQLAlchemy** - Database ORM / ORM ฐานข้อมูล
- **Font Awesome** - Icon library / ไลบรารีไอคอน
- **Jinja2** - Template engine / เครื่องมือเทมเพลต

## 📞 Support / การสนับสนุน

For support and questions:
สำหรับการสนับสนุนและคำถาม:

- 📧 **Email**: support@erp-flask.com
- 📋 **Issues**: [GitHub Issues](https://github.com/your-username/ERP-Flask-App/issues)
- 📖 **Documentation**: [Project Wiki](https://github.com/your-username/ERP-Flask-App/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/ERP-Flask-App/discussions)

---

<div align="center">

**Made with ❤️ in Thailand / สร้างด้วย ❤️ ในประเทศไทย**

[![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com)

**Happy Coding! / เขียนโค้ดให้สนุก!** 🚀

</div>