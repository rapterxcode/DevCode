<?php
require_once 'config/database.php';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("Cannot connect to database");
}

try {
    // ดึงข้อมูลสินค้าทั้งหมด
    $query = "SELECT * FROM products ORDER BY created_at DESC LIMIT 20";
    $stmt = $db->prepare($query);
    $stmt->execute();
    $products = $stmt->fetchAll();

    // ดึงสถิติสินค้า (แบบ manual เนื่องจาก view อาจยังไม่มี)
    $stats_query = "
        SELECT 
            'phone' as product_type,
            COUNT(*) as total_products,
            COUNT(CASE WHEN status = 'available' THEN 1 END) as available_count,
            COUNT(CASE WHEN status = 'reserved' THEN 1 END) as reserved_count,
            COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold_count,
            AVG(price) as average_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM products WHERE product_type = 'phone'
        UNION ALL
        SELECT 
            'license' as product_type,
            COUNT(*) as total_products,
            COUNT(CASE WHEN status = 'available' THEN 1 END) as available_count,
            COUNT(CASE WHEN status = 'reserved' THEN 1 END) as reserved_count,
            COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold_count,
            AVG(price) as average_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM products WHERE product_type = 'license'
    ";
    $stats_stmt = $db->prepare($stats_query);
    $stats_stmt->execute();
    $stats = $stats_stmt->fetchAll();
    
} catch (PDOException $e) {
    // หากเกิดข้อผิดพลาด ให้ใช้ข้อมูลเริ่มต้น
    $products = [];
    $stats = [
        ['product_type' => 'phone', 'total_products' => 0, 'available_count' => 0, 'reserved_count' => 0, 'sold_count' => 0],
        ['product_type' => 'license', 'total_products' => 0, 'available_count' => 0, 'reserved_count' => 0, 'sold_count' => 0]
    ];
    error_log("Database error in index.php: " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เบอร์สวย & ทะเบียนรถ - ศูนย์รวมเบอร์มงคล</title>
    
    <!-- Bootstrap 4 CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            font-family: 'Kanit', sans-serif; 
            background-color: #f8f9fa;
        }
        
        .navbar-brand { 
            font-weight: 600; 
            font-size: 1.5rem;
        }
        
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 0;
            margin-top: -56px;
            padding-top: 156px;
        }
        
        .hero-section h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .hero-section p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .btn-hero {
            padding: 12px 30px;
            font-size: 1.1rem;
            border-radius: 25px;
            margin: 0 10px;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            font-size: 2.5rem;
            font-weight: 600;
            color: #333;
        }
        
        .product-card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            margin-bottom: 30px;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
        }
        
        .product-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .network-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
        }
        
        .network-ais { background: #00a651; }
        .network-dtac { background: #ed1c24; }
        .network-true { background: #ff6600; }
        .province-badge { 
            background: #6f42c1; 
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status-available { background: #d4edda; color: #155724; }
        .status-reserved { background: #fff3cd; color: #856404; }
        .status-sold { background: #f8d7da; color: #721c24; }
        
        .product-number {
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin: 20px 0;
            color: #333;
        }
        
        .license-plate {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 10px;
            border-radius: 8px;
            border: 3px solid #333;
            display: inline-block;
            min-width: 120px;
        }
        
        .numerology-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: center;
        }
        
        .numerology-meaning {
            color: #667eea;
            font-weight: 600;
        }
        
        .product-price {
            font-size: 1.5rem;
            font-weight: 700;
            color: #28a745;
            text-align: center;
            margin: 20px 0;
        }
        
        .search-tabs .nav-link {
            border-radius: 25px 25px 0 0;
            border: none;
            color: #666;
            font-weight: 500;
        }
        
        .search-tabs .nav-link.active {
            background: #667eea;
            color: white;
        }
        
        .contact-item {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .contact-item i {
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .stats-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            padding: 50px 0 20px;
        }
        
        .footer h5 {
            color: #ffd700;
            margin-bottom: 20px;
        }
        
        .footer a {
            color: #bdc3c7;
            text-decoration: none;
        }
        
        .footer a:hover {
            color: #ffd700;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-phone-alt text-warning"></i> เบอร์สวย & ทะเบียนรถ
            </a>
            
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">หน้าแรก</a></li>
                    <li class="nav-item"><a class="nav-link" href="#products">สินค้า</a></li>
                    <li class="nav-item"><a class="nav-link" href="#search">ค้นหา</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">ติดต่อเรา</a></li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-warning text-dark ml-2" href="admin/" style="border-radius: 20px;">
                            <i class="fas fa-cog"></i> จัดการสินค้า
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero-section">
        <div class="container text-center">
            <h1>ศูนย์รวมเบอร์มงคล & ทะเบียนรถสวย</h1>
            <p>เลือกเบอร์โทรศัพท์และทะเบียนรถที่เหมาะกับดวงชะตาของคุณ</p>
            <div>
                <a href="#products" class="btn btn-warning btn-hero">
                    <i class="fas fa-shopping-cart"></i> ดูสินค้า
                </a>
                <a href="#search" class="btn btn-outline-light btn-hero">
                    <i class="fas fa-search"></i> ค้นหาเบอร์
                </a>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="py-5" style="background: white;">
        <div class="container">
            <div class="row">
                <?php foreach ($stats as $stat): ?>
                <div class="col-md-6 col-lg-3">
                    <div class="stats-card">
                        <div class="stats-number"><?= $stat['total_products'] ?></div>
                        <h6><?= $stat['product_type'] == 'phone' ? 'เบอร์โทรศัพท์' : 'ทะเบียนรถ' ?></h6>
                        <small class="text-muted">
                            ว่าง: <?= $stat['available_count'] ?> | 
                            จอง: <?= $stat['reserved_count'] ?> | 
                            ขายแล้ว: <?= $stat['sold_count'] ?>
                        </small>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Search Section -->
    <section id="search" class="py-5" style="background: #f8f9fa;">
        <div class="container">
            <h2 class="section-title">ค้นหาเบอร์และทะเบียน</h2>
            
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card">
                        <div class="card-body">
                            <ul class="nav nav-tabs search-tabs" role="tablist">
                                <li class="nav-item">
                                    <a class="nav-link active" data-toggle="tab" href="#search-number">ค้นหาเบอร์</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" data-toggle="tab" href="#search-license">ค้นหาทะเบียน</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" data-toggle="tab" href="#search-numerology">ค้นหาตามเลขศาสตร์</a>
                                </li>
                            </ul>
                            
                            <div class="tab-content pt-4">
                                <!-- ค้นหาเบอร์ -->
                                <div class="tab-pane active" id="search-number">
                                    <form action="search.php" method="GET">
                                        <input type="hidden" name="type" value="phone">
                                        <div class="row">
                                            <div class="col-md-4">
                                                <select name="network" class="form-control">
                                                    <option value="">เลือกเครือข่าย</option>
                                                    <option value="AIS">AIS</option>
                                                    <option value="DTAC">DTAC</option>
                                                    <option value="TRUE">TRUE</option>
                                                </select>
                                            </div>
                                            <div class="col-md-5">
                                                <input type="text" name="number" class="form-control" placeholder="ป้อนเบอร์ที่ต้องการ">
                                            </div>
                                            <div class="col-md-3">
                                                <button type="submit" class="btn btn-primary btn-block">
                                                    <i class="fas fa-search"></i> ค้นหา
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                
                                <!-- ค้นหาทะเบียน -->
                                <div class="tab-pane" id="search-license">
                                    <form action="search.php" method="GET">
                                        <input type="hidden" name="type" value="license">
                                        <div class="row">
                                            <div class="col-md-4">
                                                <select name="province" class="form-control">
                                                    <option value="">เลือกจังหวัด</option>
                                                    <option value="กรุงเทพมหานคร">กรุงเทพมหานคร</option>
                                                    <option value="ชลบุรี">ชลบุรี</option>
                                                    <option value="เชียงใหม่">เชียงใหม่</option>
                                                    <option value="ภูเก็ต">ภูเก็ต</option>
                                                    <option value="ขอนแก่น">ขอนแก่น</option>
                                                </select>
                                            </div>
                                            <div class="col-md-5">
                                                <input type="text" name="number" class="form-control" placeholder="ป้อนทะเบียนที่ต้องการ">
                                            </div>
                                            <div class="col-md-3">
                                                <button type="submit" class="btn btn-primary btn-block">
                                                    <i class="fas fa-search"></i> ค้นหา
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                
                                <!-- ค้นหาตามเลขศาสตร์ -->
                                <div class="tab-pane" id="search-numerology">
                                    <form action="search.php" method="GET">
                                        <input type="hidden" name="type" value="numerology">
                                        <div class="row">
                                            <div class="col-md-4">
                                                <select name="product_type" class="form-control">
                                                    <option value="">ประเภท</option>
                                                    <option value="phone">เบอร์โทรศัพท์</option>
                                                    <option value="license">ทะเบียนรถ</option>
                                                </select>
                                            </div>
                                            <div class="col-md-5">
                                                <input type="number" name="numerology" class="form-control" placeholder="ผลรวมที่ต้องการ (เช่น 42, 64, 57)">
                                            </div>
                                            <div class="col-md-3">
                                                <button type="submit" class="btn btn-success btn-block">
                                                    <i class="fas fa-calculator"></i> คำนวณ
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                    
                                    <div class="mt-3 p-3" style="background: #e3f2fd; border-radius: 8px;">
                                        <small class="text-info">
                                            <i class="fas fa-info-circle"></i>
                                            <strong>ตัวอย่างความหมาย:</strong>
                                            42: ความสำเร็จในการงาน | 
                                            64: ความมั่งคั่งทางการเงิน | 
                                            57: ความรักและความสัมพันธ์
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Products Section -->
    <section id="products" class="py-5">
        <div class="container">
            <h2 class="section-title">สินค้าแนะนำ</h2>
            
            <!-- Filter Buttons -->
            <div class="text-center mb-4">
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-primary active" onclick="filterProducts('all')">ทั้งหมด</button>
                    <button type="button" class="btn btn-outline-primary" onclick="filterProducts('phone')">เบอร์โทรศัพท์</button>
                    <button type="button" class="btn btn-outline-primary" onclick="filterProducts('license')">ทะเบียนรถ</button>
                </div>
            </div>
            
            <div class="row" id="products-grid">
                <?php foreach ($products as $product): ?>
                <div class="col-lg-4 col-md-6 product-item" data-type="<?= $product['product_type'] ?>">
                    <div class="card product-card">
                        <div class="card-body">
                            <div class="product-header">
                                <div>
                                    <?php if ($product['product_type'] == 'phone'): ?>
                                        <span class="network-badge network-<?= strtolower($product['network_provider']) ?>">
                                            <?= $product['network_provider'] ?>
                                        </span>
                                    <?php else: ?>
                                        <span class="province-badge">
                                            <?= $product['province'] ?>
                                        </span>
                                    <?php endif; ?>
                                </div>
                                <span class="status-badge status-<?= $product['status'] ?>">
                                    <?= $product['status'] == 'available' ? 'ว่าง' : 
                                        ($product['status'] == 'reserved' ? 'จอง' : 'ขายแล้ว') ?>
                                </span>
                            </div>
                            
                            <div class="product-number <?= $product['product_type'] == 'license' ? 'license-plate' : '' ?>">
                                <?= $product['number'] ?>
                            </div>
                            
                            <div class="numerology-box">
                                <div>ผลรวม: <strong><?= $product['numerology_sum'] ?></strong></div>
                                <div class="numerology-meaning"><?= $product['numerology_meaning'] ?></div>
                            </div>
                            
                            <div class="product-price">฿<?= number_format($product['price'], 0) ?></div>
                            
                            <?php if ($product['status'] == 'available'): ?>
                                <button class="btn btn-primary btn-block" onclick="orderProduct(<?= $product['id'] ?>)">
                                    <i class="fas fa-shopping-cart"></i> 
                                    สั่งซื้อ<?= $product['product_type'] == 'phone' ? 'เบอร์โปรด' : 'ทะเบียน' ?>
                                </button>
                            <?php else: ?>
                                <button class="btn btn-secondary btn-block" disabled>
                                    <?= $product['status'] == 'reserved' ? 'จองแล้ว' : 'ขายแล้ว' ?>
                                </button>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-5" style="background: #f8f9fa;">
        <div class="container">
            <h2 class="section-title">ติดต่อเรา</h2>
            
            <div class="row">
                <div class="col-lg-6">
                    <div class="contact-item">
                        <div class="text-center">
                            <i class="fas fa-phone"></i>
                            <h5>โทรศัพท์</h5>
                            <p class="mb-0">081-234-5678</p>
                        </div>
                    </div>
                    
                    <div class="contact-item">
                        <div class="text-center">
                            <i class="fas fa-envelope"></i>
                            <h5>อีเมล</h5>
                            <p class="mb-0">info@phonebeauty.com</p>
                        </div>
                    </div>
                    
                    <div class="contact-item">
                        <div class="text-center">
                            <i class="fab fa-line"></i>
                            <h5>LINE ID</h5>
                            <p class="mb-0">@phonebeauty</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-6">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">ส่งข้อความถึงเรา</h5>
                            <form action="contact.php" method="POST">
                                <div class="form-group">
                                    <input type="text" name="name" class="form-control" placeholder="ชื่อ-นามสกุล" required>
                                </div>
                                <div class="form-group">
                                    <input type="tel" name="phone" class="form-control" placeholder="เบอร์โทรศัพท์" required>
                                </div>
                                <div class="form-group">
                                    <input type="email" name="email" class="form-control" placeholder="อีเมล">
                                </div>
                                <div class="form-group">
                                    <textarea name="message" class="form-control" rows="4" placeholder="ข้อความ" required></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block">
                                    <i class="fas fa-paper-plane"></i> ส่งข้อความ
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4">
                    <h5>เบอร์สวย & ทะเบียนรถ</h5>
                    <p>ศูนย์รวมเบอร์มงคลและทะเบียนรถสวยคุณภาพ</p>
                </div>
                <div class="col-lg-2">
                    <h5>บริการ</h5>
                    <ul class="list-unstyled">
                        <li><a href="#products">เบอร์โทรศัพท์</a></li>
                        <li><a href="#products">ทะเบียนรถ</a></li>
                        <li><a href="#search">คำนวณเลขศาสตร์</a></li>
                    </ul>
                </div>
                <div class="col-lg-3">
                    <h5>ติดต่อ</h5>
                    <p><i class="fas fa-phone mr-2"></i> 081-234-5678</p>
                    <p><i class="fas fa-envelope mr-2"></i> info@phonebeauty.com</p>
                </div>
                <div class="col-lg-3">
                    <h5>ตามติดเรา</h5>
                    <div>
                        <a href="#" class="mr-3"><i class="fab fa-facebook-f fa-2x"></i></a>
                        <a href="#" class="mr-3"><i class="fab fa-line fa-2x"></i></a>
                        <a href="#"><i class="fab fa-instagram fa-2x"></i></a>
                    </div>
                </div>
            </div>
            <hr>
            <div class="text-center">
                <p>&copy; 2024 เบอร์สวย & ทะเบียนรถ. สงวนลิขสิทธิ์.</p>
            </div>
        </div>
    </footer>

    <!-- Order Modal -->
    <div class="modal fade" id="orderModal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">สั่งซื้อสินค้า</h5>
                    <button type="button" class="close" data-dismiss="modal">
                        <span>&times;</span>
                    </button>
                </div>
                <form action="order.php" method="POST">
                    <div class="modal-body">
                        <input type="hidden" name="product_id" id="order_product_id">
                        <div id="product_details"></div>
                        
                        <div class="form-group">
                            <label>ชื่อ-นามสกุล <span class="text-danger">*</span></label>
                            <input type="text" name="customer_name" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label>เบอร์โทรศัพท์ <span class="text-danger">*</span></label>
                            <input type="tel" name="customer_phone" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label>อีเมล</label>
                            <input type="email" name="customer_email" class="form-control">
                        </div>
                        <div class="form-group">
                            <label>หมายเหตุ</label>
                            <textarea name="notes" class="form-control" rows="3"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">ยกเลิก</button>
                        <button type="submit" class="btn btn-primary">ยืนยันการสั่งซื้อ</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Filter products
        function filterProducts(type) {
            $('.btn-group .btn').removeClass('active');
            $(`button[onclick="filterProducts('${type}')"]`).addClass('active');
            
            if (type === 'all') {
                $('.product-item').show();
            } else {
                $('.product-item').hide();
                $(`.product-item[data-type="${type}"]`).show();
            }
        }

        // Order product
        function orderProduct(productId) {
            $.ajax({
                url: 'get_product.php',
                method: 'GET',
                data: { id: productId },
                dataType: 'json',
                success: function(product) {
                    $('#order_product_id').val(productId);
                    
                    const productType = product.product_type === 'phone' ? 'เบอร์โทรศัพท์' : 'ทะเบียนรถ';
                    const network = product.network_provider || product.province;
                    
                    $('#product_details').html(`
                        <div class="alert alert-info">
                            <h6><strong>${productType}: ${product.number}</strong></h6>
                            <p class="mb-1">เครือข่าย/จังหวัด: ${network}</p>
                            <p class="mb-1">ราคา: ฿${parseInt(product.price).toLocaleString()}</p>
                            <p class="mb-0">เลขศาสตร์: ${product.numerology_sum} (${product.numerology_meaning})</p>
                        </div>
                    `);
                    
                    $('#orderModal').modal('show');
                },
                error: function() {
                    alert('เกิดข้อผิดพลาดในการโหลดข้อมูลสินค้า');
                }
            });
        }

        // Smooth scrolling
        $('a[href^="#"]').on('click', function(event) {
            var target = $(this.getAttribute('href'));
            if (target.length) {
                event.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 70
                }, 1000);
            }
        });

        // Auto-close alerts
        setTimeout(function() {
            $('.alert').fadeOut();
        }, 5000);
    </script>
</body>
</html>