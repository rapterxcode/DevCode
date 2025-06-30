<?php
require_once 'config/database.php';

$search_results = [];
$search_type = '';
$search_query = '';
$error_message = '';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    $error_message = "ไม่สามารถเชื่อมต่อฐานข้อมูลได้";
}

if ($_GET && !$error_message) {
    $type = sanitize($_GET['type'] ?? '');
    $search_type = $type;
    
    try {
        if ($type == 'phone') {
            $network = sanitize($_GET['network'] ?? '');
            $number = sanitize($_GET['number'] ?? '');
            $search_query = "เบอร์: $number, เครือข่าย: $network";
            
            $query = "SELECT * FROM products WHERE product_type = 'phone'";
            $params = [];
            
            if (!empty($network)) {
                $query .= " AND network_provider = :network";
                $params[':network'] = $network;
            }
            
            if (!empty($number)) {
                $query .= " AND number LIKE :number";
                $params[':number'] = "%$number%";
            }
            
            $query .= " ORDER BY created_at DESC";
            
        } elseif ($type == 'license') {
            $province = sanitize($_GET['province'] ?? '');
            $number = sanitize($_GET['number'] ?? '');
            $search_query = "ทะเบียน: $number, จังหวัด: $province";
            
            $query = "SELECT * FROM products WHERE product_type = 'license'";
            $params = [];
            
            if (!empty($province)) {
                $query .= " AND province = :province";
                $params[':province'] = $province;
            }
            
            if (!empty($number)) {
                $query .= " AND number LIKE :number";
                $params[':number'] = "%$number%";
            }
            
            $query .= " ORDER BY created_at DESC";
            
        } elseif ($type == 'numerology') {
            $numerology = (int)($_GET['numerology'] ?? 0);
            $product_type = sanitize($_GET['product_type'] ?? '');
            $search_query = "เลขศาสตร์: $numerology, ประเภท: $product_type";
            
            $query = "SELECT * FROM products WHERE numerology_sum = :numerology";
            $params = [':numerology' => $numerology];
            
            if (!empty($product_type)) {
                $query .= " AND product_type = :product_type";
                $params[':product_type'] = $product_type;
            }
            
            $query .= " ORDER BY created_at DESC";
        }
        
        if (isset($query)) {
            $stmt = $db->prepare($query);
            $stmt->execute($params);
            $search_results = $stmt->fetchAll();
        }
        
    } catch (PDOException $e) {
        $error_message = "เกิดข้อผิดพลาดในการค้นหา: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ผลการค้นหา - เบอร์สวย & ทะเบียนรถ</title>
    
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
        
        .search-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
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
        
        .network-badge, .province-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
        }
        
        .network-ais { background: #00a651; }
        .network-dtac { background: #ed1c24; }
        .network-true { background: #ff6600; }
        .province-badge { background: #6f42c1; }
        
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
        
        .back-btn {
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand" href="index.php">
                <i class="fas fa-phone-alt text-warning"></i> เบอร์สวย & ทะเบียนรถ
            </a>
            
            <div class="ml-auto">
                <a href="index.php" class="btn btn-warning">
                    <i class="fas fa-home"></i> กลับหน้าแรก
                </a>
            </div>
        </div>
    </nav>

    <!-- Search Header -->
    <section class="search-header">
        <div class="container text-center">
            <h1><i class="fas fa-search"></i> ผลการค้นหา</h1>
            <?php if ($search_query): ?>
                <p class="lead">เงื่อนไขการค้นหา: <?= $search_query ?></p>
            <?php endif; ?>
        </div>
    </section>

    <!-- Search Results -->
    <section class="py-5">
        <div class="container">
            <?php if (isset($error_message)): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                </div>
            <?php endif; ?>
            
            <?php if (empty($search_results) && $_GET): ?>
                <div class="text-center py-5">
                    <i class="fas fa-search fa-5x text-muted mb-3"></i>
                    <h3>ไม่พบสินค้าที่ตรงกับเงื่อนไขการค้นหา</h3>
                    <p class="text-muted">กรุณาลองเปลี่ยนเงื่อนไขการค้นหาใหม่</p>
                    <a href="index.php#search" class="btn btn-primary">
                        <i class="fas fa-search"></i> ค้นหาใหม่
                    </a>
                </div>
            <?php elseif (!empty($search_results)): ?>
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            พบสินค้า <strong><?= count($search_results) ?></strong> รายการ
                            <?php if ($search_type == 'numerology'): ?>
                                <span class="ml-2">
                                    <small>(เลขศาสตร์: <?= $_GET['numerology'] ?> - <?= getNumerologyMeaning($_GET['numerology']) ?>)</small>
                                </span>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <?php foreach ($search_results as $product): ?>
                    <div class="col-lg-4 col-md-6">
                        <div class="card product-card">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center mb-3">
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
                
                <!-- Additional Search -->
                <div class="text-center mt-5">
                    <a href="index.php#search" class="btn btn-outline-primary btn-lg">
                        <i class="fas fa-search"></i> ค้นหาสินค้าอื่น
                    </a>
                </div>
            <?php endif; ?>
        </div>
    </section>

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

        // Auto-close alerts
        setTimeout(function() {
            $('.alert').fadeOut();
        }, 5000);
    </script>
</body>
</html>