<?php
require_once '../config/database.php';

$order = null;
$error_message = '';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

// ดึงข้อมูลคำสั่งซื้อ
if (isset($_GET['id'])) {
    $order_id = (int)$_GET['id'];
    
    try {
        $query = "
            SELECT o.*, p.number, p.product_type, p.price, p.network_provider, p.province, 
                   p.numerology_sum, p.numerology_meaning, p.status as product_status
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            WHERE o.id = :id
        ";
        $stmt = $db->prepare($query);
        $stmt->bindParam(':id', $order_id, PDO::PARAM_INT);
        $stmt->execute();
        $order = $stmt->fetch();
        
        if (!$order) {
            $error_message = "ไม่พบคำสั่งซื้อที่ต้องการ";
        }
    } catch (PDOException $e) {
        $error_message = "เกิดข้อผิดพลาดในการดึงข้อมูลคำสั่งซื้อ";
        error_log("View order error: " . $e->getMessage());
    }
} else {
    $error_message = "ไม่ระบุรหัสคำสั่งซื้อ";
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ดูรายละเอียดคำสั่งซื้อ - จัดการสินค้า</title>
    
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
        
        .order-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .order-details {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .info-section {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin-bottom: 30px;
        }
        
        .product-info {
            background: #e3f2fd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .customer-info {
            background: #f3e5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .order-status {
            background: #e8f5e8;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
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
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .status-pending { background: #fff3cd; color: #856404; }
        .status-confirmed { background: #d4edda; color: #155724; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        
        .product-number {
            font-size: 1.5rem;
            font-weight: 700;
            color: #333;
        }
        
        .license-plate {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 5px 10px;
            border-radius: 5px;
            border: 2px solid #333;
            display: inline-block;
        }
        
        .action-buttons {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
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
            
            <div class="ml-auto">
                <a href="index.php" class="btn btn-warning">
                    <i class="fas fa-arrow-left"></i> กลับหน้าจัดการ
                </a>
            </div>
        </div>
    </nav>

    <!-- Order Header -->
    <section class="order-header">
        <div class="container text-center">
            <h1><i class="fas fa-file-alt"></i> รายละเอียดคำสั่งซื้อ</h1>
            <?php if ($order): ?>
                <p class="lead">คำสั่งซื้อ #<?= $order['id'] ?></p>
            <?php endif; ?>
        </div>
    </section>

    <!-- Order Details -->
    <section class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="order-details">
                        
                        <?php if ($error_message): ?>
                            <div class="alert alert-danger">
                                <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                            </div>
                            
                            <div class="text-center">
                                <a href="index.php" class="btn btn-primary">
                                    <i class="fas fa-arrow-left"></i> กลับหน้าจัดการ
                                </a>
                            </div>
                            
                        <?php else: ?>
                            
                            <!-- Order Status -->
                            <div class="order-status">
                                <div class="row align-items-center">
                                    <div class="col-md-8">
                                        <h5><i class="fas fa-info-circle"></i> สถานะคำสั่งซื้อ</h5>
                                        <span class="status-badge status-<?= $order['order_status'] ?>">
                                            <?= $order['order_status'] == 'pending' ? 'รอดำเนินการ' : 
                                                ($order['order_status'] == 'confirmed' ? 'ยืนยันแล้ว' : 'ยกเลิก') ?>
                                        </span>
                                        <p class="mt-2 mb-0">
                                            <strong>วันที่สั่งซื้อ:</strong> <?= formatDate($order['order_date']) ?>
                                        </p>
                                    </div>
                                    <div class="col-md-4 text-md-right">
                                        <h6>รหัสคำสั่งซื้อ</h6>
                                        <h3 class="text-primary">#<?= $order['id'] ?></h3>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Product Information -->
                            <div class="info-section">
                                <h5><i class="fas fa-shopping-cart"></i> ข้อมูลสินค้า</h5>
                                
                                <div class="product-info">
                                    <div class="row align-items-center">
                                        <div class="col-md-8">
                                            <div class="d-flex align-items-center mb-2">
                                                <?php if ($order['product_type'] == 'phone'): ?>
                                                    <span class="network-badge network-<?= strtolower($order['network_provider']) ?> mr-2">
                                                        <?= $order['network_provider'] ?>
                                                    </span>
                                                    <span class="badge badge-primary">เบอร์โทรศัพท์</span>
                                                <?php else: ?>
                                                    <span class="province-badge mr-2">
                                                        <?= $order['province'] ?>
                                                    </span>
                                                    <span class="badge badge-info">ทะเบียนรถ</span>
                                                <?php endif; ?>
                                            </div>
                                            
                                            <div class="product-number <?= $order['product_type'] == 'license' ? 'license-plate' : '' ?>">
                                                <?= $order['number'] ?>
                                            </div>
                                            
                                            <p class="mb-1">
                                                <strong>เลขศาสตร์:</strong> <?= $order['numerology_sum'] ?> 
                                                (<?= $order['numerology_meaning'] ?>)
                                            </p>
                                            <p class="mb-0">
                                                <strong>สถานะสินค้า:</strong> 
                                                <span class="badge badge-<?= $order['product_status'] == 'available' ? 'success' : 
                                                    ($order['product_status'] == 'reserved' ? 'warning' : 'danger') ?>">
                                                    <?= $order['product_status'] == 'available' ? 'ว่าง' : 
                                                        ($order['product_status'] == 'reserved' ? 'จอง' : 'ขายแล้ว') ?>
                                                </span>
                                            </p>
                                        </div>
                                        <div class="col-md-4 text-md-right">
                                            <div class="h3 text-success mb-0">
                                                ฿<?= number_format($order['price'], 0) ?>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Customer Information -->
                            <div class="info-section">
                                <h5><i class="fas fa-user"></i> ข้อมูลลูกค้า</h5>
                                
                                <div class="customer-info">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>ชื่อ-นามสกุล:</strong> <?= $order['customer_name'] ?></p>
                                            <p><strong>เบอร์โทรศัพท์:</strong> 
                                                <a href="tel:<?= $order['customer_phone'] ?>" class="text-primary">
                                                    <?= $order['customer_phone'] ?>
                                                </a>
                                            </p>
                                        </div>
                                        <div class="col-md-6">
                                            <?php if ($order['customer_email']): ?>
                                                <p><strong>อีเมล:</strong> 
                                                    <a href="mailto:<?= $order['customer_email'] ?>" class="text-primary">
                                                        <?= $order['customer_email'] ?>
                                                    </a>
                                                </p>
                                            <?php else: ?>
                                                <p><strong>อีเมล:</strong> <span class="text-muted">ไม่ระบุ</span></p>
                                            <?php endif; ?>
                                        </div>
                                    </div>
                                    
                                    <?php if ($order['notes']): ?>
                                        <div class="mt-3">
                                            <strong>หมายเหตุ:</strong>
                                            <div class="mt-2 p-3" style="background: #f8f9fa; border-radius: 5px;">
                                                <?= nl2br(htmlspecialchars($order['notes'])) ?>
                                            </div>
                                        </div>
                                    <?php endif; ?>
                                </div>
                            </div>
                            
                            <!-- Action Buttons -->
                            <div class="action-buttons">
                                <h5><i class="fas fa-cogs"></i> การจัดการ</h5>
                                
                                <div class="row">
                                    <div class="col-md-3">
                                        <a href="index.php" class="btn btn-secondary btn-block">
                                            <i class="fas fa-arrow-left"></i> กลับหน้าจัดการ
                                        </a>
                                    </div>
                                    
                                    <?php if ($order['order_status'] == 'pending'): ?>
                                        <div class="col-md-3">
                                            <button class="btn btn-success btn-block" onclick="confirmOrder(<?= $order['id'] ?>)">
                                                <i class="fas fa-check"></i> ยืนยันคำสั่งซื้อ
                                            </button>
                                        </div>
                                        <div class="col-md-3">
                                            <button class="btn btn-danger btn-block" onclick="cancelOrder(<?= $order['id'] ?>)">
                                                <i class="fas fa-times"></i> ยกเลิกคำสั่งซื้อ
                                            </button>
                                        </div>
                                    <?php endif; ?>
                                    
                                    <div class="col-md-3">
                                        <button class="btn btn-info btn-block" onclick="contactCustomer()">
                                            <i class="fas fa-phone"></i> ติดต่อลูกค้า
                                        </button>
                                    </div>
                                </div>
                            </div>
                            
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Confirm order
        function confirmOrder(orderId) {
            if (confirm('ต้องการยืนยันคำสั่งซื้อนี้หรือไม่?')) {
                window.location.href = `confirm_order.php?id=${orderId}`;
            }
        }

        // Cancel order
        function cancelOrder(orderId) {
            const reason = prompt('กรุณาระบุเหตุผลในการยกเลิก:');
            if (reason !== null) {
                window.location.href = `cancel_order.php?id=${orderId}&reason=${encodeURIComponent(reason)}`;
            }
        }

        // Contact customer
        function contactCustomer() {
            const phone = '<?= $order['customer_phone'] ?? '' ?>';
            const email = '<?= $order['customer_email'] ?? '' ?>';
            
            let options = [];
            if (phone) options.push(`โทร: ${phone}`);
            if (email) options.push(`อีเมล: ${email}`);
            
            if (options.length === 0) {
                alert('ไม่มีข้อมูลการติดต่อ');
                return;
            }
            
            const choice = confirm('เลือกช่องทางการติดต่อ:\n' + options.join('\n') + '\n\nกด OK เพื่อโทร หรือ Cancel เพื่อส่งอีเมล');
            
            if (choice && phone) {
                window.open(`tel:${phone}`);
            } else if (!choice && email) {
                const subject = encodeURIComponent(`เรื่อง: คำสั่งซื้อ #<?= $order['id'] ?> - ${<?= $order['product_type'] == 'phone' ? "'เบอร์โทรศัพท์'" : "'ทะเบียนรถ'" ?>} <?= $order['number'] ?>`);
                const body = encodeURIComponent(`เรียน คุณ<?= $order['customer_name'] ?>\n\nเกี่ยวกับคำสั่งซื้อ #<?= $order['id'] ?>\nสินค้า: <?= $order['number'] ?>\nราคา: ฿<?= number_format($order['price'], 0) ?>\n\nขอบคุณครับ`);
                window.open(`mailto:${email}?subject=${subject}&body=${body}`);
            }
        }
    </script>
</body>
</html>