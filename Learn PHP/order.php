<?php
require_once 'config/database.php';

$success_message = '';
$error_message = '';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    $error_message = "ไม่สามารถเชื่อมต่อฐานข้อมูลได้";
}

if ($_POST && !$error_message) {
    $product_id = (int)($_POST['product_id'] ?? 0);
    $customer_name = sanitize($_POST['customer_name'] ?? '');
    $customer_phone = sanitize($_POST['customer_phone'] ?? '');
    $customer_email = sanitize($_POST['customer_email'] ?? '');
    $notes = sanitize($_POST['notes'] ?? '');
    
    // ตรวจสอบข้อมูลที่จำเป็น
    if (empty($product_id) || empty($customer_name) || empty($customer_phone)) {
        $error_message = "กรุณากรอกข้อมูลให้ครบถ้วน";
    } else {
        try {
            // ตรวจสอบว่าสินค้ายังคงว่างอยู่หรือไม่
            $check_query = "SELECT * FROM products WHERE id = :id AND status = 'available'";
            $check_stmt = $db->prepare($check_query);
            $check_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
            $check_stmt->execute();
            
            $product = $check_stmt->fetch();
            
            if (!$product) {
                $error_message = "สินค้าไม่พร้อมให้บริการหรือถูกจองแล้ว";
            } else {
                // เริ่ม transaction
                $db->beginTransaction();
                
                // เพิ่มคำสั่งซื้อ
                $order_query = "INSERT INTO orders (product_id, customer_name, customer_phone, customer_email, notes) 
                              VALUES (:product_id, :customer_name, :customer_phone, :customer_email, :notes)";
                $order_stmt = $db->prepare($order_query);
                $order_stmt->bindParam(':product_id', $product_id, PDO::PARAM_INT);
                $order_stmt->bindParam(':customer_name', $customer_name);
                $order_stmt->bindParam(':customer_phone', $customer_phone);
                $order_stmt->bindParam(':customer_email', $customer_email);
                $order_stmt->bindParam(':notes', $notes);
                $order_stmt->execute();
                
                // อัพเดทสถานะสินค้าเป็น reserved
                $update_query = "UPDATE products SET status = 'reserved', updated_at = CURRENT_TIMESTAMP WHERE id = :id";
                $update_stmt = $db->prepare($update_query);
                $update_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
                $update_stmt->execute();
                
                // ยืนยัน transaction
                $db->commit();
                
                $success_message = "ส่งคำสั่งซื้อเรียบร้อยแล้ว! เจ้าหน้าที่จะติดต่อกลับภายใน 24 ชั่วโมง";
                
                // ส่งอีเมลแจ้งเตือน (ถ้ามี email server)
                // sendOrderNotification($product, $customer_name, $customer_phone, $customer_email);
                
            }
        } catch (PDOException $e) {
            if ($db->inTransaction()) {
                $db->rollBack();
            }
            $error_message = "เกิดข้อผิดพลาดในการบันทึกข้อมูล: " . $e->getMessage();
            error_log("Order error: " . $e->getMessage());
        }
    }
}

// ดึงข้อมูลสินค้าหากมี product_id
$product = null;
if (isset($_GET['id']) && $db) {
    $product_id = (int)$_GET['id'];
    
    try {
        $query = "SELECT * FROM products WHERE id = :id";
        $stmt = $db->prepare($query);
        $stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
        $stmt->execute();
        $product = $stmt->fetch();
    } catch (PDOException $e) {
        $error_message = "ไม่สามารถดึงข้อมูลสินค้าได้";
        error_log("Product fetch error: " . $e->getMessage());
    }
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>สั่งซื้อสินค้า - เบอร์สวย & ทะเบียนรถ</title>
    
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
        
        .order-form {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .product-summary {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
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
        
        .product-number {
            font-size: 2rem;
            font-weight: 700;
            color: #333;
        }
        
        .license-plate {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 10px;
            border-radius: 8px;
            border: 3px solid #333;
            display: inline-block;
        }
        
        .success-animation {
            text-align: center;
            padding: 50px 0;
        }
        
        .success-icon {
            font-size: 5rem;
            color: #28a745;
            margin-bottom: 20px;
            animation: bounceIn 1s;
        }
        
        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
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

    <!-- Order Header -->
    <section class="order-header">
        <div class="container text-center">
            <?php if ($success_message): ?>
                <h1><i class="fas fa-check-circle"></i> สั่งซื้อสำเร็จ</h1>
                <p class="lead">ขอบคุณสำหรับการสั่งซื้อ</p>
            <?php else: ?>
                <h1><i class="fas fa-shopping-cart"></i> สั่งซื้อสินค้า</h1>
                <p class="lead">กรอกข้อมูลเพื่อสั่งซื้อสินค้า</p>
            <?php endif; ?>
        </div>
    </section>

    <!-- Order Content -->
    <section class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="order-form">
                        
                        <?php if ($success_message): ?>
                            <div class="success-animation">
                                <div class="success-icon">
                                    <i class="fas fa-check-circle"></i>
                                </div>
                                <div class="alert alert-success">
                                    <h4 class="alert-heading">สำเร็จ!</h4>
                                    <p><?= $success_message ?></p>
                                    <hr>
                                    <p class="mb-0">
                                        <i class="fas fa-info-circle"></i>
                                        หมายเลขอ้างอิง: #<?= date('Ymd') . str_pad(rand(1, 9999), 4, '0', STR_PAD_LEFT) ?>
                                    </p>
                                </div>
                                
                                <div class="mt-4">
                                    <a href="index.php" class="btn btn-primary btn-lg mr-2">
                                        <i class="fas fa-home"></i> กลับหน้าแรก
                                    </a>
                                    <a href="index.php#products" class="btn btn-outline-primary btn-lg">
                                        <i class="fas fa-shopping-cart"></i> ดูสินค้าอื่น
                                    </a>
                                </div>
                            </div>
                            
                        <?php else: ?>
                            
                            <?php if ($error_message): ?>
                                <div class="alert alert-danger">
                                    <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                                </div>
                            <?php endif; ?>
                            
                            <?php if ($product): ?>
                                <div class="product-summary">
                                    <h5><i class="fas fa-info-circle"></i> ข้อมูลสินค้า</h5>
                                    <div class="row align-items-center">
                                        <div class="col-md-8">
                                            <div class="d-flex align-items-center mb-2">
                                                <?php if ($product['product_type'] == 'phone'): ?>
                                                    <span class="network-badge network-<?= strtolower($product['network_provider']) ?> mr-2">
                                                        <?= $product['network_provider'] ?>
                                                    </span>
                                                <?php else: ?>
                                                    <span class="province-badge mr-2">
                                                        <?= $product['province'] ?>
                                                    </span>
                                                <?php endif; ?>
                                                <span class="badge badge-success">ว่าง</span>
                                            </div>
                                            
                                            <div class="product-number <?= $product['product_type'] == 'license' ? 'license-plate' : '' ?>">
                                                <?= $product['number'] ?>
                                            </div>
                                            
                                            <p class="mb-1">
                                                <strong>เลขศาสตร์:</strong> <?= $product['numerology_sum'] ?> 
                                                (<?= $product['numerology_meaning'] ?>)
                                            </p>
                                        </div>
                                        <div class="col-md-4 text-md-right">
                                            <div class="h3 text-success mb-0">
                                                ฿<?= number_format($product['price'], 0) ?>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <form method="POST">
                                    <input type="hidden" name="product_id" value="<?= $product['id'] ?>">
                                    
                                    <h5><i class="fas fa-user"></i> ข้อมูลผู้สั่งซื้อ</h5>
                                    
                                    <div class="form-group">
                                        <label for="customer_name">ชื่อ-นามสกุล <span class="text-danger">*</span></label>
                                        <input type="text" name="customer_name" id="customer_name" class="form-control" required>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="customer_phone">เบอร์โทรศัพท์ <span class="text-danger">*</span></label>
                                        <input type="tel" name="customer_phone" id="customer_phone" class="form-control" required>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="customer_email">อีเมล</label>
                                        <input type="email" name="customer_email" id="customer_email" class="form-control">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="notes">หมายเหตุ</label>
                                        <textarea name="notes" id="notes" class="form-control" rows="3" placeholder="ข้อมูลเพิ่มเติม หรือ ข้อความถึงเจ้าหน้าที่"></textarea>
                                    </div>
                                    
                                    <div class="alert alert-info">
                                        <i class="fas fa-info-circle"></i>
                                        <strong>หมายเหตุ:</strong> เจ้าหน้าที่จะติดต่อกลับภายใน 24 ชั่วโมง เพื่อยืนยันการสั่งซื้อและรายละเอียดการชำระเงิน
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-6">
                                            <a href="index.php" class="btn btn-secondary btn-block">
                                                <i class="fas fa-arrow-left"></i> ยกเลิก
                                            </a>
                                        </div>
                                        <div class="col-md-6">
                                            <button type="submit" class="btn btn-primary btn-block">
                                                <i class="fas fa-check"></i> ยืนยันการสั่งซื้อ
                                            </button>
                                        </div>
                                    </div>
                                </form>
                                
                            <?php else: ?>
                                <div class="text-center py-5">
                                    <i class="fas fa-exclamation-triangle fa-5x text-warning mb-3"></i>
                                    <h3>ไม่พบข้อมูลสินค้า</h3>
                                    <p class="text-muted">สินค้าที่คุณต้องการอาจถูกขายไปแล้วหรือไม่มีอยู่ในระบบ</p>
                                    <a href="index.php" class="btn btn-primary">
                                        <i class="fas fa-home"></i> กลับหน้าแรก
                                    </a>
                                </div>
                            <?php endif; ?>
                            
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
        // Form validation
        $('form').on('submit', function(e) {
            const name = $('#customer_name').val().trim();
            const phone = $('#customer_phone').val().trim();
            
            if (!name || !phone) {
                e.preventDefault();
                alert('กรุณากรอกชื่อและเบอร์โทรศัพท์');
                return false;
            }
            
            // ตรวจสอบรูปแบบเบอร์โทร
            const phonePattern = /^[0-9]{9,10}$/;
            if (!phonePattern.test(phone.replace(/-/g, ''))) {
                e.preventDefault();
                alert('กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง');
                return false;
            }
            
            // ยืนยันการสั่งซื้อ
            return confirm('ยืนยันการสั่งซื้อสินค้านี้หรือไม่?');
        });

        // Auto format phone number
        $('#customer_phone').on('input', function() {
            let value = $(this).val().replace(/[^0-9]/g, '');
            if (value.length > 3 && value.length <= 6) {
                value = value.substring(0, 3) + '-' + value.substring(3);
            } else if (value.length > 6) {
                value = value.substring(0, 3) + '-' + value.substring(3, 6) + '-' + value.substring(6, 10);
            }
            $(this).val(value);
        });
    </script>
</body>
</html>