<?php
require_once '../config/database.php';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

try {
    // ดึงสถิติ
$stats_query = "
    SELECT 
        'total' as type, COUNT(*) as count, 0 as price FROM products
    UNION ALL
    SELECT 
        'available' as type, COUNT(*) as count, 0 as price FROM products WHERE status = 'available'
    UNION ALL
    SELECT 
        'reserved' as type, COUNT(*) as count, 0 as price FROM products WHERE status = 'reserved'
    UNION ALL
    SELECT 
        'sold' as type, COUNT(*) as count, 0 as price FROM products WHERE status = 'sold'
    UNION ALL
    SELECT 
        'total_value' as type, 0 as count, SUM(price) as price FROM products WHERE status = 'available'
";
$stats_stmt = $db->prepare($stats_query);
$stats_stmt->execute();
$stats_raw = $stats_stmt->fetchAll();

$stats = [];
foreach ($stats_raw as $stat) {
    $stats[$stat['type']] = $stat['count'] ?: $stat['price'];
}

    // ดึงคำสั่งซื้อล่าสุด
    $orders_query = "
        SELECT o.*, p.number, p.product_type, p.price, p.network_provider, p.province
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        ORDER BY o.order_date DESC 
        LIMIT 10
    ";
    $orders_stmt = $db->prepare($orders_query);
    $orders_stmt->execute();
    $recent_orders = $orders_stmt->fetchAll();

    // ดึงสินค้าทั้งหมด
    $products_query = "SELECT * FROM products ORDER BY created_at DESC LIMIT 100";
    $products_stmt = $db->prepare($products_query);
    $products_stmt->execute();
    $products = $products_stmt->fetchAll();
    
} catch (PDOException $e) {
    // หากเกิดข้อผิดพลาด ให้ใช้ข้อมูลเริ่มต้น
    $stats = ['total' => 0, 'available' => 0, 'reserved' => 0, 'sold' => 0, 'total_value' => 0];
    $recent_orders = [];
    $products = [];
    error_log("Admin page database error: " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>จัดการสินค้า - เบอร์สวย & ทะเบียนรถ</title>
    
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
        
        .admin-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .stats-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
        }
        
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .stats-total { color: #667eea; }
        .stats-available { color: #28a745; }
        .stats-reserved { color: #ffc107; }
        .stats-sold { color: #dc3545; }
        .stats-value { color: #17a2b8; }
        
        .quick-actions {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .data-table {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .network-badge, .province-badge {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 600;
            color: white;
        }
        
        .network-ais { background: #00a651; }
        .network-dtac { background: #ed1c24; }
        .network-true { background: #ff6600; }
        .province-badge { background: #6f42c1; }
        
        .status-badge {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        
        .status-available { background: #d4edda; color: #155724; }
        .status-reserved { background: #fff3cd; color: #856404; }
        .status-sold { background: #f8d7da; color: #721c24; }
        
        .btn-sm {
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
        }
        
        .table td {
            vertical-align: middle;
        }
        
        .license-plate {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #333;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand" href="../index.php">
                <i class="fas fa-phone-alt text-warning"></i> เบอร์สวย & ทะเบียนรถ
            </a>
            
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="#dashboard">แดชบอร์ด</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#products">จัดการสินค้า</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#orders">คำสั่งซื้อ</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-warning text-dark ml-2" href="../index.php" style="border-radius: 20px;">
                            <i class="fas fa-home"></i> กลับหน้าแรก
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Admin Header -->
    <section class="admin-header">
        <div class="container text-center">
            <h1><i class="fas fa-cogs"></i> ระบบจัดการสินค้า</h1>
            <p class="lead">จัดการเบอร์โทรศัพท์และทะเบียนรถ</p>
        </div>
    </section>

    <!-- Dashboard Stats -->
    <section id="dashboard" class="py-5">
        <div class="container">
            <h2 class="mb-4"><i class="fas fa-chart-bar"></i> สถิติรวม</h2>
            
            <div class="row">
                <div class="col-lg-2 col-md-4 col-sm-6">
                    <div class="stats-card">
                        <div class="stats-number stats-total"><?= $stats['total'] ?? 0 ?></div>
                        <h6>สินค้าทั้งหมด</h6>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-sm-6">
                    <div class="stats-card">
                        <div class="stats-number stats-available"><?= $stats['available'] ?? 0 ?></div>
                        <h6>ว่าง</h6>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-sm-6">
                    <div class="stats-card">
                        <div class="stats-number stats-reserved"><?= $stats['reserved'] ?? 0 ?></div>
                        <h6>จอง</h6>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-sm-6">
                    <div class="stats-card">
                        <div class="stats-number stats-sold"><?= $stats['sold'] ?? 0 ?></div>
                        <h6>ขายแล้ว</h6>
                    </div>
                </div>
                <div class="col-lg-4 col-md-8">
                    <div class="stats-card">
                        <div class="stats-number stats-value">฿<?= number_format($stats['total_value'] ?? 0, 0) ?></div>
                        <h6>มูลค่าสินค้าคงเหลือ</h6>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Quick Actions -->
    <section class="py-3">
        <div class="container">
            <div class="quick-actions">
                <h4><i class="fas fa-bolt"></i> เมนูด่วน</h4>
                <div class="row mt-3">
                    <div class="col-md-3">
                        <button class="btn btn-primary btn-block" data-toggle="modal" data-target="#addProductModal">
                            <i class="fas fa-plus"></i> เพิ่มสินค้าใหม่
                        </button>
                    </div>
                    <div class="col-md-3">
                        <button class="btn btn-success btn-block" onclick="exportData()">
                            <i class="fas fa-download"></i> ส่งออกข้อมูล
                        </button>
                    </div>
                    <div class="col-md-3">
                        <button class="btn btn-info btn-block" onclick="calculateNumerologyAll()">
                            <i class="fas fa-calculator"></i> คำนวณเลขศาสตร์
                        </button>
                    </div>
                    <div class="col-md-3">
                        <button class="btn btn-warning btn-block" onclick="generateReport()">
                            <i class="fas fa-file-alt"></i> สร้างรายงาน
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Recent Orders -->
    <section id="orders" class="py-3">
        <div class="container">
            <div class="data-table">
                <h4><i class="fas fa-shopping-cart"></i> คำสั่งซื้อล่าสุด</h4>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="thead-light">
                            <tr>
                                <th>วันที่</th>
                                <th>สินค้า</th>
                                <th>ลูกค้า</th>
                                <th>เบอร์</th>
                                <th>ราคา</th>
                                <th>สถานะ</th>
                                <th>จัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($recent_orders)): ?>
                                <tr>
                                    <td colspan="7" class="text-center text-muted">ยังไม่มีคำสั่งซื้อ</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($recent_orders as $order): ?>
                                <tr>
                                    <td><?= formatDate($order['order_date']) ?></td>
                                    <td>
                                        <?php if ($order['product_type'] == 'phone'): ?>
                                            <span class="network-badge network-<?= strtolower($order['network_provider']) ?>">
                                                <?= $order['network_provider'] ?>
                                            </span>
                                        <?php else: ?>
                                            <span class="province-badge">
                                                <?= $order['province'] ?>
                                            </span>
                                        <?php endif; ?>
                                        <span class="ml-1 <?= $order['product_type'] == 'license' ? 'license-plate' : '' ?>">
                                            <?= $order['number'] ?>
                                        </span>
                                    </td>
                                    <td><?= $order['customer_name'] ?></td>
                                    <td><?= $order['customer_phone'] ?></td>
                                    <td>฿<?= number_format($order['price'], 0) ?></td>
                                    <td>
                                        <span class="badge badge-<?= $order['order_status'] == 'pending' ? 'warning' : 
                                            ($order['order_status'] == 'confirmed' ? 'success' : 'danger') ?>">
                                            <?= $order['order_status'] == 'pending' ? 'รอดำเนินการ' : 
                                                ($order['order_status'] == 'confirmed' ? 'ยืนยันแล้ว' : 'ยกเลิก') ?>
                                        </span>
                                    </td>
                                    <td>
                                        <div class="btn-group" role="group">
                                            <button class="btn btn-sm btn-outline-primary" onclick="viewOrder(<?= $order['id'] ?>)">
                                                <i class="fas fa-eye"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-success" onclick="confirmOrder(<?= $order['id'] ?>)">
                                                <i class="fas fa-check"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <!-- Products Management -->
    <section id="products" class="py-3">
        <div class="container">
            <div class="data-table">
                <h4><i class="fas fa-boxes"></i> จัดการสินค้า</h4>
                
                <!-- Filters -->
                <div class="row mb-3">
                    <div class="col-md-3">
                        <select class="form-control" id="filterType">
                            <option value="">ประเภทสินค้า</option>
                            <option value="phone">เบอร์โทรศัพท์</option>
                            <option value="license">ทะเบียนรถ</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <select class="form-control" id="filterStatus">
                            <option value="">สถานะ</option>
                            <option value="available">ว่าง</option>
                            <option value="reserved">จอง</option>
                            <option value="sold">ขายแล้ว</option>
                        </select>
                    </div>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="searchNumber" placeholder="ค้นหาเบอร์/ทะเบียน">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary btn-block" onclick="filterProducts()">
                            <i class="fas fa-search"></i> ค้นหา
                        </button>
                    </div>
                </div>
                
                <div class="table-responsive">
                    <table class="table table-hover" id="productsTable">
                        <thead class="thead-light">
                            <tr>
                                <th>ประเภท</th>
                                <th>หมายเลข</th>
                                <th>เครือข่าย/จังหวัด</th>
                                <th>ราคา</th>
                                <th>เลขศาสตร์</th>
                                <th>สถานะ</th>
                                <th>จัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($products as $product): ?>
                            <tr data-type="<?= $product['product_type'] ?>" data-status="<?= $product['status'] ?>" data-number="<?= $product['number'] ?>">
                                <td>
                                    <span class="badge badge-<?= $product['product_type'] == 'phone' ? 'primary' : 'info' ?>">
                                        <?= $product['product_type'] == 'phone' ? 'โทรศัพท์' : 'ทะเบียนรถ' ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="<?= $product['product_type'] == 'license' ? 'license-plate' : '' ?>">
                                        <?= $product['number'] ?>
                                    </span>
                                </td>
                                <td>
                                    <?php if ($product['product_type'] == 'phone'): ?>
                                        <span class="network-badge network-<?= strtolower($product['network_provider']) ?>">
                                            <?= $product['network_provider'] ?>
                                        </span>
                                    <?php else: ?>
                                        <span class="province-badge">
                                            <?= $product['province'] ?>
                                        </span>
                                    <?php endif; ?>
                                </td>
                                <td>฿<?= number_format($product['price'], 0) ?></td>
                                <td>
                                    <strong><?= $product['numerology_sum'] ?></strong>
                                    <br><small class="text-muted"><?= $product['numerology_meaning'] ?></small>
                                </td>
                                <td>
                                    <span class="status-badge status-<?= $product['status'] ?>">
                                        <?= $product['status'] == 'available' ? 'ว่าง' : 
                                            ($product['status'] == 'reserved' ? 'จอง' : 'ขายแล้ว') ?>
                                    </span>
                                </td>
                                <td>
                                    <div class="btn-group" role="group">
                                        <button class="btn btn-sm btn-outline-primary" onclick="editProduct(<?= $product['id'] ?>)">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(<?= $product['id'] ?>)">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <!-- Add Product Modal -->
    <div class="modal fade" id="addProductModal" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">เพิ่มสินค้าใหม่</h5>
                    <button type="button" class="close" data-dismiss="modal">
                        <span>&times;</span>
                    </button>
                </div>
                <form action="add_product.php" method="POST">
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>ประเภทสินค้า <span class="text-danger">*</span></label>
                                    <select name="product_type" class="form-control" required onchange="toggleFields(this.value)">
                                        <option value="">เลือกประเภท</option>
                                        <option value="phone">เบอร์โทรศัพท์</option>
                                        <option value="license">ทะเบียนรถ</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>หมายเลข <span class="text-danger">*</span></label>
                                    <input type="text" name="number" class="form-control" required placeholder="เช่น 081-234-5678 หรือ 8888">
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group" id="networkField" style="display: none;">
                                    <label>เครือข่าย</label>
                                    <select name="network_provider" class="form-control">
                                        <option value="">เลือกเครือข่าย</option>
                                        <option value="AIS">AIS</option>
                                        <option value="DTAC">DTAC</option>
                                        <option value="TRUE">TRUE</option>
                                    </select>
                                </div>
                                <div class="form-group" id="provinceField" style="display: none;">
                                    <label>จังหวัด</label>
                                    <input type="text" name="province" class="form-control" placeholder="เช่น กรุงเทพมหานคร">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>ราคา (บาท) <span class="text-danger">*</span></label>
                                    <input type="number" name="price" class="form-control" required min="0" step="0.01">
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>ผลรวมเลขศาสตร์</label>
                                    <input type="number" name="numerology_sum" class="form-control" readonly>
                                    <small class="text-muted">จะคำนวณอัตโนมัติ</small>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>ความหมายเลขศาสตร์</label>
                                    <input type="text" name="numerology_meaning" class="form-control" readonly>
                                    <small class="text-muted">จะกำหนดอัตโนมัติ</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">ยกเลิก</button>
                        <button type="submit" class="btn btn-primary">บันทึก</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Toggle fields based on product type
        function toggleFields(type) {
            if (type === 'phone') {
                $('#networkField').show();
                $('#provinceField').hide();
                $('select[name="network_provider"]').attr('required', true);
                $('input[name="province"]').attr('required', false);
            } else if (type === 'license') {
                $('#networkField').hide();
                $('#provinceField').show();
                $('select[name="network_provider"]').attr('required', false);
                $('input[name="province"]').attr('required', true);
            } else {
                $('#networkField, #provinceField').hide();
                $('select[name="network_provider"], input[name="province"]').attr('required', false);
            }
        }

        // Calculate numerology
        function calculateNumerology(number) {
            const digits = number.replace(/[^0-9]/g, '');
            let sum = 0;
            
            for (let i = 0; i < digits.length; i++) {
                sum += parseInt(digits[i]);
            }
            
            while (sum > 9 && ![11, 22, 33].includes(sum)) {
                let temp = 0;
                const sumStr = sum.toString();
                for (let i = 0; i < sumStr.length; i++) {
                    temp += parseInt(sumStr[i]);
                }
                sum = temp;
            }
            
            return sum;
        }

        // Get numerology meaning
        function getNumerologyMeaning(sum) {
            const meanings = {
                1: "ความเป็นผู้นำ",
                2: "ความร่วมมือ",
                3: "ความคิดสร้างสรรค์",
                4: "ความมั่นคง",
                5: "ความเสรี",
                6: "ความรับผิดชอบ",
                7: "ปัญญา",
                8: "ความสำเร็จทางวัตถุ",
                9: "ความเมตตา",
                11: "ความเป็นผู้นำทางจิตวิญญาณ",
                22: "ผู้สร้างฝัน",
                33: "ความรักและการเสียสละ",
                42: "ความสำเร็จในการงาน",
                57: "ความรักและความสัมพันธ์",
                64: "ความมั่งคั่งทางการเงิน"
            };
            
            return meanings[sum] || "ความหมายพิเศษ";
        }

        // Auto calculate numerology on number input
        $('input[name="number"]').on('input', function() {
            const number = $(this).val();
            if (number) {
                const sum = calculateNumerology(number);
                const meaning = getNumerologyMeaning(sum);
                
                $('input[name="numerology_sum"]').val(sum);
                $('input[name="numerology_meaning"]').val(meaning);
            }
        });

        // Filter products
        function filterProducts() {
            const type = $('#filterType').val();
            const status = $('#filterStatus').val();
            const search = $('#searchNumber').val().toLowerCase();
            
            $('#productsTable tbody tr').each(function() {
                const row = $(this);
                const rowType = row.data('type');
                const rowStatus = row.data('status');
                const rowNumber = row.data('number').toLowerCase();
                
                let show = true;
                
                if (type && rowType !== type) show = false;
                if (status && rowStatus !== status) show = false;
                if (search && !rowNumber.includes(search)) show = false;
                
                if (show) {
                    row.show();
                } else {
                    row.hide();
                }
            });
        }

        // Edit product
        function editProduct(id) {
            window.location.href = `edit_product.php?id=${id}`;
        }

        // Delete product
        function deleteProduct(id) {
            if (confirm('ต้องการลบสินค้านี้หรือไม่?')) {
                window.location.href = `delete_product.php?id=${id}`;
            }
        }

        // View order
        function viewOrder(id) {
            window.location.href = `view_order.php?id=${id}`;
        }

        // Confirm order
        function confirmOrder(id) {
            if (confirm('ต้องการยืนยันคำสั่งซื้อนี้หรือไม่?')) {
                window.location.href = `confirm_order.php?id=${id}`;
            }
        }

        // Export data
        function exportData() {
            window.location.href = 'export.php';
        }

        // Calculate numerology for all products
        function calculateNumerologyAll() {
            if (confirm('ต้องการคำนวณเลขศาสตร์ใหม่สำหรับสินค้าทั้งหมดหรือไม่?')) {
                // สำหรับการคำนวณเลขศาสตร์ใหม่ทั้งหมด
                $.ajax({
                    url: 'calculate_numerology.php',
                    method: 'POST',
                    beforeSend: function() {
                        $('button[onclick="calculateNumerologyAll()"]').html('<i class="fas fa-spinner fa-spin"></i> กำลังคำนวณ...');
                    },
                    success: function(response) {
                        alert('คำนวณเลขศาสตร์ใหม่เรียบร้อยแล้ว');
                        location.reload();
                    },
                    error: function() {
                        alert('เกิดข้อผิดพลาดในการคำนวณ');
                        $('button[onclick="calculateNumerologyAll()"]').html('<i class="fas fa-calculator"></i> คำนวณเลขศาสตร์');
                    }
                });
            }
        }

        // Generate report
        function generateReport() {
            window.location.href = 'report.php';
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
    </script>
</body>
</html>