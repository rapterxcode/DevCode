from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date, timezone
import random
import os

# Remove existing database file
db_path = 'instance/erp.db'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Existing database removed")
    except:
        print("Could not remove existing database")

# Create new database
with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    
    # Create additional users
    manager = User(
        username='manager',
        email='manager@company.com',
        password_hash=generate_password_hash('manager123'),
        role='manager'
    )
    
    staff = User(
        username='staff',
        email='staff@company.com',
        password_hash=generate_password_hash('staff123'),
        role='user'
    )
    
    db.session.add(manager)
    db.session.add(staff)
    
    # Categories with more variety
    categories_data = [
        ('Electronics', 'Electronic devices and accessories'),
        ('Office Supplies', 'Office equipment and stationery'),
        ('Furniture', 'Office and home furniture'),
        ('Software', 'Software and licenses'),
        ('Hardware', 'Computer hardware and components'),
        ('Books', 'Technical books and manuals'),
        ('Medical', 'Medical equipment and supplies'),
        ('Automotive', 'Auto parts and accessories')
    ]
    
    categories = []
    for name, desc in categories_data:
        cat = Category(name=name, description=desc)
        categories.append(cat)
        db.session.add(cat)
    
    db.session.flush()
    
    # Enhanced Products with Thai Baht prices
    products_data = [
        # Electronics
        ('LAP001', 'Gaming Laptop RTX 4060', 'High-performance gaming laptop with RTX 4060', categories[0].id, 45990.00, 35000.00, 25, 5),
        ('MON001', 'Monitor 27" 4K UHD', '27-inch 4K UHD monitor', categories[0].id, 14990.00, 11000.00, 40, 8),
        ('KEY001', 'Mechanical Keyboard RGB', 'Gaming mechanical keyboard with RGB backlight', categories[0].id, 5490.00, 3500.00, 60, 10),
        ('MOU001', 'Gaming Mouse Wireless', 'Wireless gaming mouse with RGB', categories[0].id, 2790.00, 1800.00, 80, 15),
        ('TAB001', 'Tablet Pro 12.9"', 'Professional 12.9-inch tablet', categories[0].id, 32990.00, 25000.00, 30, 5),
        ('PHO001', 'Smartphone Latest', 'Latest model smartphone', categories[0].id, 28990.00, 22000.00, 45, 10),
        ('SPK001', 'Bluetooth Speaker', 'Portable Bluetooth speaker', categories[0].id, 3990.00, 2500.00, 35, 8),
        ('CAM001', 'Security Camera', 'IP security camera', categories[0].id, 8990.00, 6500.00, 25, 5),
        
        # Office Supplies  
        ('PEN001', 'Blue Pens Pack', 'ปากกาลูกลื่นสีน้ำเงิน 12 ด้าม', categories[1].id, 299.00, 180.00, 200, 50),
        ('PAP001', 'A4 Paper Premium', 'กระดาษ A4 พรีเมี่ยม 500 แผ่น', categories[1].id, 459.00, 290.00, 150, 30),
        ('STA001', 'Heavy Duty Stapler', 'เครื่องเย็บกระดาษหนักพิเศษ', categories[1].id, 890.00, 540.00, 75, 15),
        ('FOL001', 'Manila Folders', 'แฟ้มเอกสารกระดาษแมนิลา 25 ใบ', categories[1].id, 690.00, 430.00, 90, 20),
        ('CAL001', 'Scientific Calculator', 'เครื่องคิดเลขวิทยาศาสตร์', categories[1].id, 1090.00, 720.00, 35, 8),
        ('WHB001', 'Whiteboard Marker', 'ปากกาไวท์บอร์ด 4 สี', categories[1].id, 250.00, 150.00, 120, 25),
        
        # Furniture
        ('CHR001', 'Ergonomic Office Chair', 'เก้าอี้สำนักงานเพื่อสุขภาพพร้อมที่รองหลัง', categories[2].id, 10990.00, 7200.00, 25, 5),
        ('DSK001', 'Height Adjustable Desk', 'โต๊ะทำงานปรับระดับได้', categories[2].id, 21990.00, 14500.00, 15, 3),
        ('CAB001', '4-Drawer Filing Cabinet', 'ตู้เก็บเอกสาร 4 ลิ้นชัก', categories[2].id, 8990.00, 6500.00, 20, 4),
        ('BOO001', '5-Tier Wooden Bookshelf', 'ชั้นหนังสือไม้ 5 ชั้น', categories[2].id, 5490.00, 3600.00, 18, 4),
        ('TAB002', 'Meeting Table', 'โต๊ะประชุม 6 ที่นั่ง', categories[2].id, 15990.00, 12000.00, 8, 2),
        ('SOF001', 'Office Sofa', 'โซฟาสำนักงาน 3 ที่นั่ง', categories[2].id, 18990.00, 14000.00, 5, 1),
        
        # Software
        ('WIN001', 'Windows Pro License', 'ใบอนุญาตไวน์โดว์สโปร', categories[3].id, 7290.00, 5400.00, 50, 10),
        ('OFF001', 'Office Suite License', 'ใบอนุญาตชุดโปรแกรมออฟฟิศ', categories[3].id, 5490.00, 4300.00, 75, 15),
        ('ANT001', 'Antivirus Pro License', 'ใบอนุญาตแอนตี้ไวรัสโปร', categories[3].id, 2190.00, 1440.00, 100, 20),
        ('ADO001', 'Adobe Creative Suite', 'ใบอนุญาต Adobe Creative Suite', categories[3].id, 12990.00, 9500.00, 30, 5),
        ('ACC001', 'Accounting Software', 'ซอฟต์แวร์บัญชี', categories[3].id, 8990.00, 6500.00, 20, 4),
        
        # Hardware
        ('RAM001', 'RAM 16GB DDR4', 'หน่วยความจำ DDR4 16GB', categories[4].id, 3290.00, 2350.00, 45, 10),
        ('SSD001', 'SSD 1TB NVMe', 'ฮาร์ดดิสก์ SSD NVMe ขนาด 1TB', categories[4].id, 4790.00, 3430.00, 35, 8),
        ('GPU001', 'RTX 4070 Graphics Card', 'การ์ดจอ RTX 4070', categories[4].id, 21990.00, 16200.00, 12, 3),
        ('CPU001', 'Processor i7-13700K', 'หน่วยประมวลผล Intel i7-13700K', categories[4].id, 13990.00, 10500.00, 20, 4),
        ('MOB001', 'Motherboard Z790', 'เมนบอร์ด Z790 Chipset', categories[4].id, 8990.00, 6800.00, 15, 3),
        
        # Books
        ('BOK001', 'Python Programming Guide', 'คู่มือการเขียนโปรแกรม Python', categories[5].id, 890.00, 550.00, 50, 10),
        ('BOK002', 'Data Science Handbook', 'คู่มือวิทยาการข้อมูล', categories[5].id, 1290.00, 850.00, 30, 6),
        ('BOK003', 'Network Security Manual', 'คู่มือความปลอดภัยเครือข่าย', categories[5].id, 1590.00, 1000.00, 25, 5),
        
        # Medical
        ('MED001', 'Digital Thermometer', 'เครื่องวัดอุณหภูมิดิจิทัล', categories[6].id, 590.00, 350.00, 100, 20),
        ('MED002', 'Blood Pressure Monitor', 'เครื่องวัดความดันโลหิต', categories[6].id, 2590.00, 1800.00, 40, 8),
        ('MED003', 'First Aid Kit', 'ชุดปฐมพยาบาล', categories[6].id, 1290.00, 850.00, 60, 12),
        
        # Automotive
        ('CAR001', 'Engine Oil 5W-30', 'น้ำมันเครื่องสังเคราะห์ 5W-30', categories[7].id, 890.00, 550.00, 80, 15),
        ('CAR002', 'Car Battery 12V', 'แบตเตอรี่รถยนต์ 12V', categories[7].id, 3990.00, 2800.00, 25, 5),
        ('CAR003', 'Brake Pads Set', 'ผ้าเบรครถยนต์ ชุด', categories[7].id, 1590.00, 1000.00, 40, 8),
        
        # Low stock items (for testing alerts)
        ('LOW001', 'Low Stock Electronics', 'สินค้าอิเล็กทรอนิกส์สต็อกต่ำ', categories[0].id, 3690.00, 2520.00, 2, 10),
        ('LOW002', 'Low Stock Office Item', 'อุปกรณ์สำนักงานสต็อกต่ำ', categories[1].id, 1790.00, 1080.00, 1, 5),
        ('LOW003', 'Critical Stock Furniture', 'เฟอร์นิเจอร์สต็อกวิกฤต', categories[2].id, 7290.00, 5400.00, 0, 5),
    ]
    
    products = []
    for sku, name, desc, cat_id, price, cost, stock, reorder in products_data:
        prod = Product(
            sku=sku,
            name=name,
            description=desc,
            category_id=cat_id,
            unit_price=price,
            cost_price=cost,
            stock_quantity=stock,
            reorder_level=reorder,
            unit_of_measure='pcs',
            is_active=True
        )
        products.append(prod)
        db.session.add(prod)
    
    db.session.flush()
    
    # Enhanced Customers with Thai data
    customers_data = [
        ('บริษัท เทคคอร์ป จำกัด', 'tech@techcorp.co.th', '02-555-0101', '123 ถนนเทคโนโลยี สีลม บางรัก กรุงเทพฯ 10500', 'premium', 350000.00),
        ('ร้านธุรกิจเล็ก', 'contact@smallbiz.co.th', '02-555-0102', '456 ถนนข้าวสาร ราชเทวี กรุงเทพฯ 10400', 'regular', 180000.00),
        ('บริษัท เอ็นเทอร์ไพรส์ โซลูชั่น จำกัด', 'sales@enterprise.co.th', '02-555-0103', '789 ถนนสาทร ปทุมวัน กรุงเทพฯ 10330', 'vip', 900000.00),
        ('สตาร์ทอัพ อินโนเวชั่น', 'hello@startup.co.th', '02-555-0104', '321 ถนนพระราม 4 คลองเตย กรุงเทพฯ 10110', 'premium', 290000.00),
        ('ร้านชุมชนท้องถิ่น', 'info@localstore.co.th', '02-555-0105', '654 ถนนรัชดาภิเษก ห้วยขวาง กรุงเทพฯ 10310', 'regular', 110000.00),
        ('บริษัท โกลบอล คอร์ป จำกัด (มหาชน)', 'purchasing@global.co.th', '02-555-0106', '987 ถนนสุขุมวิท วัฒนา กรุงเทพฯ 10110', 'vip', 1800000.00),
        ('บริษัท มิดไซส์ จำกัด', 'orders@midsize.co.th', '02-555-0107', '147 ถนนพหลโยธิน จตุจักร กรุงเทพฯ 10900', 'premium', 540000.00),
        ('เชนค้าปลีก', 'procurement@retail.co.th', '02-555-0108', '258 ถนนลาดพร้าว วังทองหลาง กรุงเทพฯ 10310', 'vip', 1080000.00),
        ('สถาบันการศึกษา', 'purchasing@edu.ac.th', '02-555-0109', '369 ถนนพญาไท ราชเทวี กรุงเทพฯ 10400', 'regular', 430000.00),
        ('โรงพยาบาลเอกชน', 'supply@healthcare.co.th', '02-555-0110', '741 ถนนเพชรบุรี ราชเทวี กรุงเทพฯ 10400', 'premium', 720000.00),
        ('บริษัท แมนูแฟคเจอริ่ง จำกัด', 'info@manufacturing.co.th', '02-555-0111', '852 ถนนรามอินทรา มีนบุรี กรุงเทพฯ 10510', 'premium', 650000.00),
        ('ร้านอาหารเครือข่าย', 'admin@restaurant.co.th', '02-555-0112', '963 ถนนวิทยุ ลุมพินี กรุงเทพฯ 10330', 'regular', 250000.00)
    ]
    
    customers = []
    for name, email, phone, address, ctype, credit in customers_data:
        cust = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            customer_type=ctype,
            credit_limit=credit
        )
        customers.append(cust)
        db.session.add(cust)
    
    db.session.flush()
    
    # Enhanced Vendors with Thai addresses
    vendors_data = [
        ('บริษัท เทค ซัพพลายเออร์ จำกัด', 'supplier@techsupplier.co.th', '02-555-1001', '100 ถนนสุขุมวิท คลองเตย กรุงเทพฯ 10110', 'คุณสมชาย จิตดี', 'Net 30'),
        ('บริษัท ออฟฟิศ โฮลเซล จำกัด', 'sales@officewholesale.co.th', '02-555-1002', '200 ถนนราชพฤกษ์ บางแค กรุงเทพฯ 10160', 'คุณสมใจ ขายดี', 'Net 15'),
        ('บริษัท เฟอร์นิเจอร์ไดเร็กต์ จำกัด', 'orders@furnituredirect.co.th', '02-555-1003', '300 ถนนรัตนาธิเบศร์ บางกรวย นนทบุรี 11130', 'คุณศิริ ตกแต่ง', 'Net 45'),
        ('บริษัท ซอฟต์แวร์ไลเซนซิ่ง จำกัด', 'licensing@software.co.th', '02-555-1004', '400 ถนนพระราม 9 ห้วยขวาง กรุงเทพฯ 10310', 'คุณอนุชา เทคโน', 'Prepaid'),
        ('บริษัท ฮาร์ดแวร์ดิสทริบิวเตอร์ จำกัด', 'distribution@hardware.co.th', '02-555-1005', '500 ถนนกรุงเทพกรีฑา บางนา กรุงเทพฯ 10260', 'คุณธนา คอมพิว', 'Net 30'),
        ('บริษัท อิเล็กทรอนิกส์โฮลเซล จำกัด', 'wholesale@electronics.co.th', '02-555-1006', '600 ถนนรามคำแหง สะพานสูง กรุงเทพฯ 10240', 'คุณนภา ไฟฟ้า', 'Net 30'),
        ('บริษัท เมดิคัลซัพพลาย จำกัด', 'sales@medsupplies.co.th', '02-555-1007', '700 ถนนวิภาวดีรังสิต ดินแดง กรุงเทพฯ 10400', 'คุณพิมพ์ สุขภาพ', 'Net 60'),
        ('บริษัท ออโต้ปาร์ท จำกัด', 'parts@autoparts.co.th', '02-555-1008', '800 ถนนติวานนท์ ปากเกร็ด นนทบุรี 11120', 'คุณวิชัย ยนต์', 'COD'),
        ('บริษัท บุ๊คดีลเลอร์ จำกัด', 'books@bookdealer.co.th', '02-555-1009', '900 ถนนจรัญสนิทวงศ์ บางพลัด กรุงเทพฯ 10700', 'คุณวรรณา หนังสือ', 'Net 21'),
        ('บริษัท อินดัสเทรียลอิควิปเมนต์ จำกัด', 'sales@industrial.co.th', '02-555-1010', '111 ถนนบางนา-ตราด บางนา กรุงเทพฯ 10260', 'คุณสมศักดิ์ อุตสาห์', 'Net 45')
    ]
    
    vendors = []
    for name, email, phone, address, contact, terms in vendors_data:
        vendor = Vendor(
            name=name,
            email=email,
            phone=phone,
            address=address,
            contact_person=contact,
            payment_terms=terms
        )
        vendors.append(vendor)
        db.session.add(vendor)
    
    db.session.flush()
    
    # Enhanced Departments
    departments_data = [
        ('เทคโนโลยีสารสนเทศ', 'จัดการโครงสร้างพื้นฐาน IT และการพัฒนาซอฟต์แวร์'),
        ('ทรัพยากรบุคคล', 'จัดการความสัมพันธ์พนักงาน การรับสมัคร และสวัสดิการ'),
        ('การเงินและบัญชี', 'จัดการการดำเนินงานทางการเงินและการบัญชี'),
        ('ฝ่ายขายและการตลาด', 'จัดการการขายและแคมเปญการตลาด'),
        ('ฝ่ายปฏิบัติการ', 'จัดการการดำเนินงานประจำวันของธุรกิจ'),
        ('ฝ่ายลูกค้าสัมพันธ์', 'ให้การสนับสนุนและบริการลูกค้า'),
        ('วิจัยและพัฒนา', 'นวัตกรรมและการพัฒนาผลิตภัณฑ์'),
        ('ฝ่ายควบคุมคุณภาพ', 'รับประกันคุณภาพของผลิตภัณฑ์และบริการ'),
        ('ฝ่ายจัดซื้อ', 'จัดการการซื้อและห่วงโซ่อุปทาน'),
        ('ฝ่ายกฎหมาย', 'จัดการกฎหมายและการปฏิบัติตามกฎระเบียบ')
    ]
    
    departments = []
    for name, desc in departments_data:
        dept = Department(name=name, description=desc)
        departments.append(dept)
        db.session.add(dept)
    
    db.session.flush()
    
    # Enhanced Employees with Thai names and extended data
    employees_data = [
        ('EMP001', 'สมชาย', 'ใจดี', 'somchai.jaidee@company.co.th', '081-555-2001', departments[0].id, 'Software Developer', 75000.00),
        ('EMP002', 'สมหญิง', 'รักเรียน', 'somying.rakrian@company.co.th', '081-555-2002', departments[0].id, 'System Administrator', 65000.00),
        ('EMP003', 'นภาพร', 'สุขสันต์', 'napaporn.suksan@company.co.th', '081-555-2003', departments[1].id, 'HR Manager', 85000.00),
        ('EMP004', 'ธนากร', 'เจริญสุข', 'thanakorn.jernsuk@company.co.th', '081-555-2004', departments[2].id, 'Chief Accountant', 90000.00),
        ('EMP005', 'กนิษฐา', 'วิจิตร', 'kanitha.wijit@company.co.th', '081-555-2005', departments[3].id, 'Sales Manager', 95000.00),
        ('EMP006', 'ปรีชา', 'ชาญศิลป์', 'preecha.chansin@company.co.th', '081-555-2006', departments[3].id, 'Marketing Specialist', 55000.00),
        ('EMP007', 'วรรณา', 'มีประสิทธิ์', 'wanna.meeprasit@company.co.th', '081-555-2007', departments[4].id, 'Operations Manager', 80000.00),
        ('EMP008', 'อนันต์', 'บริการดี', 'anan.borikanndee@company.co.th', '081-555-2008', departments[5].id, 'Customer Service Rep', 45000.00),
        ('EMP009', 'ศิริวรรณ', 'นวัตกรรม', 'siriwan.nawatkam@company.co.th', '081-555-2009', departments[6].id, 'Research Scientist', 95000.00),
        ('EMP010', 'จิรายุ', 'ทดสอบ', 'jirayu.todsob@company.co.th', '081-555-2010', departments[7].id, 'QA Specialist', 58000.00),
        ('EMP011', 'สุวิชา', 'เทคโนโลยี', 'suwicha.technology@company.co.th', '081-555-2011', departments[0].id, 'DevOps Engineer', 78000.00),
        ('EMP012', 'มยุรี', 'ดูแลคน', 'mayuree.dulaekons@company.co.th', '081-555-2012', departments[1].id, 'HR Specialist', 52000.00),
        ('EMP013', 'วิชัย', 'การเงิน', 'wichai.karnngern@company.co.th', '081-555-2013', departments[2].id, 'Financial Analyst', 64000.00),
        ('EMP014', 'นันทนา', 'ขายดี', 'nantana.khaidee@company.co.th', '081-555-2014', departments[3].id, 'Sales Representative', 48000.00),
        ('EMP015', 'ธีรพงษ์', 'พอใจลูกค้า', 'theeraphong.pojailuk@company.co.th', '081-555-2015', departments[5].id, 'Customer Success Manager', 62000.00),
        ('EMP016', 'พรรณี', 'จัดซื้อ', 'pannee.jadsue@company.co.th', '081-555-2016', departments[8].id, 'Procurement Specialist', 60000.00),
        ('EMP017', 'สราวุธ', 'กฎหมาย', 'sarawut.godmai@company.co.th', '081-555-2017', departments[9].id, 'Legal Advisor', 75000.00),
        ('EMP018', 'พิมพ์ใจ', 'คุณภาพ', 'pimjai.khunpab@company.co.th', '081-555-2018', departments[7].id, 'Quality Control Manager', 70000.00),
        ('EMP019', 'วีระชัย', 'วิจัย', 'weerachai.wijit@company.co.th', '081-555-2019', departments[6].id, 'R&D Manager', 88000.00),
        ('EMP020', 'สุดารัตน์', 'ปฏิบัติการ', 'sudarat.patibatngan@company.co.th', '081-555-2020', departments[4].id, 'Operations Supervisor', 55000.00)
    ]
    
    employees = []
    for emp_id, fname, lname, email, phone, dept_id, position, salary in employees_data:
        hire_date = datetime.now(timezone.utc) - timedelta(days=random.randint(30, 1095))
        emp = Employee(
            employee_id=emp_id,
            first_name=fname,
            last_name=lname,
            email=email,
            phone=phone,
            department_id=dept_id,
            position=position,
            salary=salary,
            hire_date=hire_date
        )
        employees.append(emp)
        db.session.add(emp)
    
    db.session.flush()
    
    # Update departments with managers
    departments[0].manager_id = employees[0].id  # สมชาย as IT Manager
    departments[1].manager_id = employees[2].id  # นภาพร as HR Manager
    departments[2].manager_id = employees[3].id  # ธนากร as Finance Manager
    departments[3].manager_id = employees[4].id  # กนิษฐา as Sales Manager
    departments[4].manager_id = employees[6].id  # วรรณา as Operations Manager
    departments[5].manager_id = employees[14].id  # ธีรพงษ์ as Customer Service Manager
    departments[6].manager_id = employees[18].id  # วีระชัย as R&D Manager
    departments[7].manager_id = employees[17].id  # พิมพ์ใจ as QC Manager
    departments[8].manager_id = employees[15].id  # พรรณี as Procurement Manager
    departments[9].manager_id = employees[16].id  # สราวุธ as Legal Manager
    
    # Enhanced Sales Orders
    sales_orders = []
    for i in range(25):
        customer = random.choice(customers)
        order_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 180))
        delivery_date = order_date + timedelta(days=random.randint(1, 14))
        
        so = SalesOrder(
            so_number=f"SO{2024}{1000 + i:04d}",
            customer_id=customer.id,
            order_date=order_date,
            delivery_date=delivery_date,
            status=random.choice(['pending', 'confirmed', 'shipped', 'delivered']),
            discount=random.choice([0, 5, 10, 15]),
            notes=f"ใบสั่งขายสำหรับ {customer.name}"
        )
        sales_orders.append(so)
        db.session.add(so)
    
    db.session.flush()
    
    # Sales Order Items
    for so in sales_orders:
        num_items = random.randint(1, 5)
        total_amount = 0
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            
            so_item = SalesOrderItem(
                sales_order_id=so.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.unit_price
            )
            db.session.add(so_item)
            total_amount += quantity * product.unit_price
        
        # Apply discount and tax
        discount_amount = total_amount * (so.discount / 100)
        tax_amount = (total_amount - discount_amount) * 0.07  # 7% VAT
        so.total_amount = total_amount - discount_amount + tax_amount
        so.tax_amount = tax_amount
    
    # Enhanced Purchase Orders
    purchase_orders = []
    for i in range(20):
        vendor = random.choice(vendors)
        order_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 150))
        expected_date = order_date + timedelta(days=random.randint(7, 30))
        
        po = PurchaseOrder(
            po_number=f"PO{2024}{2000 + i:04d}",
            vendor_id=vendor.id,
            order_date=order_date,
            expected_date=expected_date,
            status=random.choice(['pending', 'confirmed', 'received']),
            notes=f"ใบสั่งซื้อจาก {vendor.name}"
        )
        purchase_orders.append(po)
        db.session.add(po)
    
    db.session.flush()
    
    # Purchase Order Items
    for po in purchase_orders:
        num_items = random.randint(1, 4)
        total_amount = 0
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(5, 50)
            unit_price = product.cost_price * random.uniform(0.9, 1.1)
            
            po_item = PurchaseOrderItem(
                purchase_order_id=po.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price
            )
            db.session.add(po_item)
            total_amount += quantity * unit_price
        
        po.total_amount = total_amount
    
    # Enhanced Quotations
    quotations = []
    prepared_by_list = ['สมชาย ใจดี', 'กนิษฐา วิจิตร', 'นันทนา ขายดี', 'ธีรพงษ์ พอใจลูกค้า', 'ปรีชา ชาญศิลป์', 'อนันต์ บริการดี']
    
    for i in range(15):
        customer = random.choice(customers)
        quote_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
        valid_until = quote_date + timedelta(days=30)
        
        quotation = Quotation(
            quote_number=f"QT{2024}{3000 + i:04d}",
            customer_id=customer.id,
            quote_date=quote_date,
            valid_until=valid_until,
            status=random.choice(['draft', 'sent', 'accepted', 'rejected', 'expired']),
            discount=random.choice([0, 5, 10]),
            prepared_by=random.choice(prepared_by_list),
            terms_conditions="เงื่อนไขการชำระเงิน: 30 วัน, การจัดส่ง: FOB, รับประกัน: 1 ปี"
        )
        quotations.append(quotation)
        db.session.add(quotation)
    
    db.session.flush()
    
    # Quotation Items
    for quote in quotations:
        num_items = random.randint(1, 4)
        total_amount = 0
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 8)
            unit_price = product.unit_price * random.uniform(0.95, 1.05)
            
            quote_item = QuotationItem(
                quotation_id=quote.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                description=f"ข้อเสนอสำหรับ {product.name}"
            )
            db.session.add(quote_item)
            total_amount += quantity * unit_price
        
        # Apply discount and tax
        discount_amount = total_amount * (quote.discount / 100)
        tax_amount = (total_amount - discount_amount) * 0.07
        quote.total_amount = total_amount - discount_amount + tax_amount
        quote.tax_amount = tax_amount
    
    # Enhanced Stock Movements
    for i in range(50):
        product = random.choice(products)
        movement_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        
        movement = StockMovement(
            product_id=product.id,
            movement_type=random.choice(['in', 'out', 'adjustment']),
            quantity=random.randint(1, 25),
            reference_type=random.choice(['sale', 'purchase', 'adjustment', 'return', 'transfer']),
            notes=f"การเคลื่อนไหวสต็อกสำหรับ {product.name}",
            created_at=movement_date
        )
        db.session.add(movement)
    
    # Inventory Receives
    inventory_receives = []
    received_by_list = ['พรรณี จัดซื้อ', 'วรรณา มีประสิทธิ์', 'สุดารัตน์ ปฏิบัติการ', 'วิชัย การเงิน', 'จิรายุ ทดสอบ', 'มยุรี ดูแลคน']
    
    for i in range(18):
        vendor = random.choice(vendors)
        receive_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
        
        # Sometimes link to a purchase order
        purchase_order = None
        if random.choice([True, False]) and purchase_orders:
            # Find a purchase order from the same vendor
            vendor_pos = [po for po in purchase_orders if po.vendor_id == vendor.id]
            if vendor_pos:
                purchase_order = random.choice(vendor_pos)
        
        receive = InventoryReceive(
            receive_number=f"RV{2024}{4000 + i:04d}",
            vendor_id=vendor.id,
            purchase_order_id=purchase_order.id if purchase_order else None,
            receive_date=receive_date,
            status=random.choice(['draft', 'confirmed', 'completed']),
            notes=f"รับสินค้าจาก {vendor.name}" + (f" ตาม PO {purchase_order.po_number}" if purchase_order else " (ซื้อตรง)"),
            received_by=random.choice(received_by_list)
        )
        inventory_receives.append(receive)
        db.session.add(receive)
    
    db.session.flush()
    
    # Inventory Receive Items
    used_batch_numbers = set()
    for receive in inventory_receives:
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(10, 100)
            
            # Generate unique batch number
            while True:
                batch_number = f"BT{random.randint(1000, 9999)}"
                if batch_number not in used_batch_numbers:
                    used_batch_numbers.add(batch_number)
                    break
            
            receive_item = InventoryReceiveItem(
                receive_id=receive.id,
                product_id=product.id,
                quantity=quantity,
                unit_cost=product.cost_price,
                batch_number=batch_number,
                expiry_date=datetime.now(timezone.utc).date() + timedelta(days=random.randint(180, 730))
            )
            db.session.add(receive_item)
    
    # Enhanced Accounting Setup
    accounts_data = [
        ('1000', 'เงินสดในมือ', 'asset'),
        ('1100', 'เงินฝากธนาคาร', 'asset'),
        ('1200', 'ลูกหนี้การค้า', 'asset'),
        ('1300', 'สินค้าคงเหลือ', 'asset'),
        ('1400', 'สินทรัพย์หมุนเวียนอื่น', 'asset'),
        ('1500', 'ที่ดิน อาคาร อุปกรณ์', 'asset'),
        ('2000', 'เจ้าหนี้การค้า', 'liability'),
        ('2100', 'หนี้สินหมุนเวียนอื่น', 'liability'),
        ('2200', 'เงินกู้ยืมระยะยาว', 'liability'),
        ('3000', 'ทุนจดทะเบียน', 'equity'),
        ('3100', 'กำไรสะสม', 'equity'),
        ('4000', 'รายได้จากการขาย', 'revenue'),
        ('4100', 'รายได้อื่น', 'revenue'),
        ('5000', 'ต้นทุนขาย', 'expense'),
        ('6000', 'ค่าใช้จ่ายในการขาย', 'expense'),
        ('6100', 'ค่าใช้จ่ายในการบริหาร', 'expense'),
        ('6200', 'ค่าใช้จ่ายทางการเงิน', 'expense')
    ]
    
    for code, name, acc_type in accounts_data:
        balance = 0
        if acc_type == 'asset':
            balance = random.uniform(50000, 500000)
        elif acc_type == 'liability':
            balance = random.uniform(20000, 200000)
        elif acc_type == 'equity':
            balance = random.uniform(100000, 1000000)
        elif acc_type == 'revenue':
            balance = random.uniform(500000, 2000000)
        elif acc_type == 'expense':
            balance = random.uniform(100000, 800000)
            
        account = Account(
            account_code=code,
            account_name=name,
            account_type=acc_type,
            balance=balance
        )
        db.session.add(account)
    
    # Bank Accounts
    bank_names_list = ['บัญชีเงินฝากออมทรัพย์', 'บัญชีเงินฝากกระแสรายวัน', 'บัญชีเงินฝากประจำ', 'บัญชีเครดิตธุรกิจ', 'บัญชีเงินฝากเพื่อธุรกิจ', 'บัญชีเงินฝากออมทรัพย์พิเศษ', 'บัญชีเงินฝากเพื่อการลงทุน', 'บัญชีเงินฝากเพื่อการออม']
    bank_codes_list = ['123-4-56789-0', '987-6-54321-0', '555-1-23456-7', '777-8-98765-4', '111-2-33333-4', '999-9-88888-7', '444-5-66666-8', '888-3-22222-1', '666-7-11111-9', '222-1-99999-3']
    bank_names_bank_list = ['ธนาคารกสิกรไทย', 'ธนาคารไทยพาณิชย์', 'ธนาคารกรุงเทพ', 'ธนาคารกรุงศรีฯ', 'ธนาคารกรุงไทย', 'ธนาคารทหารไทยธนชาต', 'ธนาคารออมสิน', 'ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร', 'ธนาคารกรุงเทพธนาคาร', 'ธนาคารซีไอเอ็มบี ไทย']
    account_types_list = ['savings', 'checking', 'credit']
    
    # Prevent duplicates by using random.sample instead of random.choice
    bank_accounts = []
    used_names = set()
    used_numbers = set()
    used_banks = set()
    
    for i in range(4):
        # Get unique name, number, and bank
        available_names = [name for name in bank_names_list if name not in used_names]
        available_numbers = [num for num in bank_codes_list if num not in used_numbers]
        available_banks = [bank for bank in bank_names_bank_list if bank not in used_banks]
        
        # If we run out of unique options, allow reuse but with different combinations
        if not available_names:
            available_names = bank_names_list
        if not available_numbers:
            available_numbers = bank_codes_list
        if not available_banks:
            available_banks = bank_names_bank_list
            
        name = random.choice(available_names)
        number = random.choice(available_numbers)
        bank = random.choice(available_banks)
        acc_type = random.choice(account_types_list)
        balance = random.uniform(50000, 2000000) if acc_type != 'credit' else random.uniform(-100000, -10000)
        
        # Add to used sets to prevent immediate duplicates
        used_names.add(name)
        used_numbers.add(number)
        used_banks.add(bank)
        
        bank_acc = BankAccount(
            account_name=name,
            account_number=number,
            bank_name=bank,
            account_type=acc_type,
            balance=balance,
            is_active=True
        )
        bank_accounts.append(bank_acc)
        db.session.add(bank_acc)
    
    db.session.flush()
    
    # Bank Transactions
    used_reference_numbers = set()
    for i in range(30):
        bank_account = random.choice(bank_accounts)
        transaction_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        transaction_type = random.choice(['deposit', 'withdrawal', 'transfer'])
        amount = random.uniform(5000, 100000)
        
        if transaction_type == 'withdrawal':
            amount = -amount
        
        # Generate unique reference number
        while True:
            ref_number = f"REF{random.randint(100000, 999999)}"
            if ref_number not in used_reference_numbers:
                used_reference_numbers.add(ref_number)
                break
            
        bank_transaction = BankTransaction(
            bank_account_id=bank_account.id,
            transaction_date=transaction_date,
            transaction_type=transaction_type,
            amount=amount,
            description=f"การทำรายการ{transaction_type} เลขที่ {i+1:04d}",
            reference_number=ref_number,
            balance_after=bank_account.balance + amount
        )
        db.session.add(bank_transaction)
    
    # Attendance Records
    for employee in employees[:10]:  # First 10 employees
        for days_back in range(30):  # Last 30 days
            attendance_date = date.today() - timedelta(days=days_back)
            
            # Skip weekends
            if attendance_date.weekday() >= 5:
                continue
                
            # Random attendance
            if random.random() > 0.95:  # 5% absence rate
                status = 'absent'
                check_in = None
                check_out = None
                hours_worked = 0
            else:
                status = 'present'
                check_in_hour = random.randint(8, 9)
                check_in_minute = random.randint(0, 59)
                check_in = datetime.strptime(f"{check_in_hour}:{check_in_minute}", "%H:%M").time()
                
                check_out_hour = random.randint(17, 19)
                check_out_minute = random.randint(0, 59)
                check_out = datetime.strptime(f"{check_out_hour}:{check_out_minute}", "%H:%M").time()
                
                # Calculate hours worked
                check_in_datetime = datetime.combine(attendance_date, check_in)
                check_out_datetime = datetime.combine(attendance_date, check_out)
                hours_worked = (check_out_datetime - check_in_datetime).seconds / 3600
            
            attendance = Attendance(
                employee_id=employee.id,
                date=attendance_date,
                check_in=check_in,
                check_out=check_out,
                hours_worked=hours_worked,
                status=status
            )
            db.session.add(attendance)
    
    # Payroll Records
    for employee in employees:
        # Create payroll for last 3 months
        for month_back in range(3):
            pay_period_end = date.today().replace(day=1) - timedelta(days=month_back * 30)
            pay_period_start = pay_period_end.replace(day=1)
            
            basic_salary = employee.salary
            overtime_hours = random.uniform(0, 20)
            overtime_rate = basic_salary / 160 * 1.5  # 1.5x normal rate
            allowances = random.uniform(2000, 8000)
            deductions = random.uniform(1000, 3000)
            tax_deduction = basic_salary * 0.05  # 5% tax
            social_security = min(basic_salary * 0.05, 750)  # Max 750 baht
            
            net_salary = basic_salary + (overtime_hours * overtime_rate) + allowances - deductions - tax_deduction - social_security
            
            payroll = Payroll(
                employee_id=employee.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                basic_salary=basic_salary,
                overtime_hours=overtime_hours,
                overtime_rate=overtime_rate,
                allowances=allowances,
                deductions=deductions,
                tax_deduction=tax_deduction,
                social_security=social_security,
                net_salary=net_salary,
                status=random.choice(['draft', 'approved', 'paid']),
                pay_date=pay_period_end + timedelta(days=5) if random.choice([True, False]) else None
            )
            db.session.add(payroll)
    
    # Performance Evaluations
    improvement_areas_list = [
        "พัฒนาทักษะการสื่อสารและการทำงานเป็นทีม",
        "เพิ่มประสิทธิภาพการทำงานและจัดการเวลา",
        "พัฒนาทักษะการนำเสนอและการประชุม",
        "ปรับปรุงการแก้ไขปัญหาและการตัดสินใจ",
        "พัฒนาความคิดสร้างสรรค์และนวัตกรรม",
        "ปรับปรุงการบริการลูกค้าและการจัดการความขัดแย้ง",
        "พัฒนาทักษะการวิเคราะห์ข้อมูลและการรายงาน",
        "ปรับปรุงการทำงานภายใต้ความกดดัน",
        "พัฒนาความรู้ด้านเทคโนโลยีและเครื่องมือใหม่",
        "ปรับปรุงการวางแผนและการจัดลำดับความสำคัญ"
    ]
    
    goals_next_period_list = [
        "เพิ่มประสิทธิภาพการทำงานและพัฒนาทักษะใหม่",
        "รับผิดชอบโครงการใหม่และพัฒนาทีมงาน",
        "ปรับปรุงกระบวนการทำงานและลดต้นทุน",
        "พัฒนาความสัมพันธ์กับลูกค้าและเพิ่มยอดขาย",
        "เรียนรู้เทคโนโลยีใหม่และปรับใช้ในงาน",
        "พัฒนาทักษะการเป็นผู้นำและการจัดการทีม",
        "เพิ่มผลผลิตและคุณภาพการทำงาน",
        "พัฒนาระบบการติดตามและรายงานผล",
        "ปรับปรุงการบริการลูกค้าและความพึงพอใจ",
        "พัฒนาความรู้เฉพาะทางและรับผิดชอบงานที่ซับซ้อนขึ้น"
    ]
    
    for employee in employees[:8]:  # First 8 employees
        evaluation_start = date.today().replace(month=1, day=1)
        evaluation_end = date.today().replace(month=12, day=31)
        
        evaluation = PerformanceEvaluation(
            employee_id=employee.id,
            evaluator_id=employees[2].id if employee.id != employees[2].id else employees[3].id,  # HR Manager or Finance Manager
            evaluation_period_start=evaluation_start,
            evaluation_period_end=evaluation_end,
            overall_rating=random.uniform(3.0, 5.0),
            goals_achievement=random.uniform(3.0, 5.0),
            skills_assessment=random.uniform(3.0, 5.0),
            communication=random.uniform(3.0, 5.0),
            teamwork=random.uniform(3.0, 5.0),
            leadership=random.uniform(2.5, 5.0),
            comments=f"การประเมินผลการปฏิบัติงานของ {employee.first_name} {employee.last_name} สำหรับปี {date.today().year}",
            improvement_areas=random.choice(improvement_areas_list),
            goals_next_period=random.choice(goals_next_period_list),
            status=random.choice(['draft', 'completed', 'approved'])
        )
        db.session.add(evaluation)
    
    # Customer and Vendor Contacts
    contact_types_list = ['call', 'email', 'meeting', 'note', 'visit', 'presentation']
    subjects_list = [
        'ปรึกษาราคาสินค้า',
        'สอบถามสถานะการจัดส่ง',
        'ขอใบเสนอราคาใหม่',
        'รายงานปัญหาสินค้า',
        'นัดหมายประชุม',
        'ต่อรองเงื่อนไขการชำระเงิน',
        'สอบถามสินค้าใหม่',
        'ขอขยายเครดิต',
        'เสนอโปรโมชั่นพิเศษ',
        'ติดตามการชำระเงิน',
        'ขอข้อมูลสินค้าเพิ่มเติม',
        'รายงานความพึงพอใจ',
        'ขอความช่วยเหลือทางเทคนิค',
        'นัดหมายการฝึกอบรม',
        'เสนอแผนการตลาดใหม่'
    ]
    
    sales_team_list = ['กนิษฐา วิจิตร', 'นันทนา ขายดี', 'ธีรพงษ์ พอใจลูกค้า', 'สมชาย ใจดี', 'นภาพร สุขสันต์', 'ธนากร เจริญสุข', 'ปรีชา ชาญศิลป์', 'อนันต์ บริการดี', 'ศิริวรรณ นวัตกรรม', 'มยุรี ดูแลคน']
    procurement_team_list = ['พรรณี จัดซื้อ', 'วรรณา มีประสิทธิ์', 'สุดารัตน์ ปฏิบัติการ', 'ปรีชา ชาญศิลป์', 'อนันต์ บริการดี', 'ศิริวรรณ นวัตกรรม', 'วิชัย การเงิน', 'จิรายุ ทดสอบ', 'สุวิชา เทคโนโลยี', 'ธีรพงษ์ พอใจลูกค้า']
    
    # Customer contacts
    for i in range(20):
        customer = random.choice(customers)
        contact_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        
        contact = CustomerContact(
            customer_id=customer.id,
            contact_type=random.choice(contact_types_list),
            contact_date=contact_date,
            subject=random.choice(subjects_list),
            description=f"รายละเอียดการติดต่อกับ {customer.name}",
            follow_up_date=contact_date + timedelta(days=random.randint(1, 14)) if random.choice([True, False]) else None,
            status=random.choice(['open', 'closed', 'follow_up']),
            created_by=random.choice(sales_team_list)
        )
        db.session.add(contact)
    
    # Vendor contacts
    for i in range(15):
        vendor = random.choice(vendors)
        contact_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        
        contact = VendorContact(
            vendor_id=vendor.id,
            contact_type=random.choice(contact_types_list),
            contact_date=contact_date,
            subject=random.choice(subjects_list),
            description=f"รายละเอียดการติดต่อกับ {vendor.name}",
            follow_up_date=contact_date + timedelta(days=random.randint(1, 14)) if random.choice([True, False]) else None,
            status=random.choice(['open', 'closed', 'follow_up']),
            created_by=random.choice(procurement_team_list)
        )
        db.session.add(contact)
    
    # Sales Tax Invoices
    for i in range(20):
        customer = random.choice(customers)
        sales_order = random.choice(sales_orders)
        invoice_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 120))
        due_date = invoice_date + timedelta(days=30)
        
        total_amount = random.uniform(10000, 100000)
        paid_amount = total_amount if random.random() > 0.3 else random.uniform(0, total_amount * 0.8)
        
        sales_invoice = SalesTaxInvoice(
            invoice_number=f"SI{2024}{5000+i:04d}",
            customer_id=customer.id,
            sales_order_id=sales_order.id,
            invoice_date=invoice_date,
            due_date=due_date,
            total_amount=total_amount,
            tax_amount=total_amount * 0.07,
            paid_amount=paid_amount,
            status='paid' if paid_amount >= total_amount else 'pending',
            notes=f"Sales tax invoice for {customer.name}"
        )
        db.session.add(sales_invoice)
    
    # Purchase Tax Invoices
    for i in range(15):
        vendor = random.choice(vendors)
        purchase_order = random.choice(purchase_orders)
        invoice_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
        due_date = invoice_date + timedelta(days=30)
        
        total_amount = random.uniform(5000, 80000)
        paid_amount = total_amount if random.random() > 0.4 else random.uniform(0, total_amount * 0.7)
        
        purchase_invoice = PurchaseTaxInvoice(
            invoice_number=f"PI{2024}{6000+i:04d}",
            vendor_id=vendor.id,
            purchase_order_id=purchase_order.id,
            invoice_date=invoice_date,
            due_date=due_date,
            total_amount=total_amount,
            tax_amount=total_amount * 0.07,
            paid_amount=paid_amount,
            status='paid' if paid_amount >= total_amount else 'pending',
            notes=f"Purchase tax invoice from {vendor.name}"
        )
        db.session.add(purchase_invoice)
    
    # Stock Count Records
    count_team_list = ['John Smith', 'Jane Wilson', 'Operations Team', 'Inventory Team', 'Warehouse Staff', 'Quality Control Team', 'สมชาย ใจดี', 'นภาพร สุขสันต์', 'พรรณี จัดซื้อ', 'สุดารัตน์ ปฏิบัติการ']
    
    for i in range(15):
        count_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60))
        
        stock_count = StockCount(
            count_number=f"SC{2024}{7000+i:04d}",
            count_date=count_date,
            count_type=random.choice(['full', 'cycle', 'spot']),
            status=random.choice(['draft', 'counting', 'completed']),
            counted_by=random.choice(count_team_list),
            verified_by=random.choice(count_team_list) if random.choice([True, False]) else None,
            notes=f"Stock count #{i+1} for inventory management - {random.choice(['Monthly cycle', 'Annual audit', 'Spot check', 'System reconciliation'])}"
        )
        db.session.add(stock_count)
    
    db.session.flush()
    
    # Stock Count Items
    for stock_count in StockCount.query.all():
        # Select random products for this count, ensuring no duplicates
        num_items = random.randint(5, 15)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        for product in selected_products:
            system_quantity = product.stock_quantity
            counted_quantity = system_quantity + random.randint(-5, 5)
            
            count_item = StockCountItem(
                count_id=stock_count.id,
                product_id=product.id,
                system_quantity=system_quantity,
                counted_quantity=counted_quantity,
                variance=counted_quantity - system_quantity,
                unit_cost=product.cost_price,
                notes=f"Count for {product.name}"
            )
            db.session.add(count_item)
    
    # Inventory Issue Records
    for i in range(10):
        issue_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 45))
        employee = random.choice(employees)
        department = random.choice(departments)
        
        inventory_issue = InventoryIssue(
            issue_number=f"IS{2024}{8000+i:04d}",
            issue_date=issue_date,
            issue_type='internal',
            department_id=department.id,
            employee_id=employee.id,
            status=random.choice(['draft', 'approved', 'issued']),
            notes=f"Inventory issue request from {department.name} department"
        )
        db.session.add(inventory_issue)
    
    db.session.flush()
    
    # Inventory Issue Items
    for issue in InventoryIssue.query.all():
        # Select random products for this issue, ensuring no duplicates
        num_items = random.randint(1, 4)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        for product in selected_products:
            quantity = random.randint(1, 10)
            
            issue_item = InventoryIssueItem(
                issue_id=issue.id,
                product_id=product.id,
                quantity=quantity,
                unit_cost=product.cost_price,
                reason=f"Issue {product.name} to department"
            )
            db.session.add(issue_item)

    db.session.commit()
    print("Enhanced database created successfully with comprehensive English mock data!")
    print(f"""
    ✅ Created comprehensive ERP system with English localization:
    
    📊 Master Data:
    - {len(categories_data)} หมวดหมู่สินค้า
    - {len(products_data)} รายการสินค้า (รวมสินค้าสต็อกต่ำ)
    - {len(customers_data)} ลูกค้า
    - {len(vendors_data)} ผู้ขาย
    - {len(departments_data)} แผนก
    - {len(employees_data)} พนักงาน
    
    🛒 ธุรกรรม:
    - 25 ใบสั่งขาย พร้อมรายการสินค้า
    - 20 ใบสั่งซื้อ พร้อมรายการสินค้า
    - 15 ใบเสนอราคา พร้อมรายการ
    - 12 การรับสินค้าเข้าคลัง
    - 50 การเคลื่อนไหวสต็อก
    
    💰 การเงิน:
    - 17 บัญชีแยกประเภท
    - 4 บัญชีธนาคาร
    - 30 รายการธุรกรรมธนาคาร
    
    👥 ทรัพยากรบุคคล:
    - บันทึกการเข้างาน 30 วันย้อนหลัง
    - เงินเดือน 3 เดือนย้อนหลัง
    - การประเมินผลการปฏิบัติงาน
    
    📞 CRM:
    - 20 การติดต่อลูกค้า
    - 15 การติดต่อผู้ขาย
    
    🔐 ข้อมูลเข้าสู่ระบบ:
    - Admin: admin/admin123
    - Manager: manager/manager123
    - Staff: staff/staff123
    
    🎯 ข้อมูลทั้งหมดเป็นภาษาไทยและใช้สกุลเงินบาท (฿)
    """)