<?php
require_once '../config/database.php';

$success_message = '';
$error_message = '';
$product = null;

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

// ดึงข้อมูลสินค้า
if (isset($_GET['id'])) {
    $product_id = (int)$_GET['id'];
    
    try {
        $query = "SELECT * FROM products WHERE id = :id";
        $stmt = $db->prepare($query);
        $stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
        $stmt->execute();
        $product = $stmt->fetch();
        
        if (!$product) {
            $error_message = "ไม่พบสินค้าที่ต้องการแก้ไข";
        }
    } catch (PDOException $e) {
        $error_message = "เกิดข้อผิดพลาดในการดึงข้อมูลสินค้า";
    }
} else {
    $error_message = "ไม่ระบุรหัสสินค้า";
}

// อัพเดทข้อมูลสินค้า
if ($_POST && $product) {
    $product_type = sanitize($_POST['product_type'] ?? '');
    $number = sanitize($_POST['number'] ?? '');
    $price = (float)($_POST['price'] ?? 0);
    $network_provider = sanitize($_POST['network_provider'] ?? '');
    $province = sanitize($_POST['province'] ?? '');
    $status = sanitize($_POST['status'] ?? 'available');
    $numerology_sum = (int)($_POST['numerology_sum'] ?? 0);
    $numerology_meaning = sanitize($_POST['numerology_meaning'] ?? '');
    
    // ตรวจสอบข้อมูลที่จำเป็น
    if (empty($product_type) || empty($number) || $price <= 0) {
        $error_message = "กรุณากรอกข้อมูลให้ครบถ้วน";
    } else {
        // ตรวจสอบว่าหมายเลขซ้ำหรือไม่ (ยกเว้นสินค้าปัจจุบัน)
        $check_query = "SELECT id FROM products WHERE number = :number AND product_type = :product_type AND id != :current_id";
        $check_stmt = $db->prepare($check_query);
        $check_stmt->bindParam(':number', $number);
        $check_stmt->bindParam(':product_type', $product_type);
        $check_stmt->bindParam(':current_id', $product['id'], PDO::PARAM_INT);
        $check_stmt->execute();
        
        if ($check_stmt->rowCount() > 0) {
            $error_message = "หมายเลขนี้มีอยู่ในระบบแล้ว";
        } else {
            // คำนวณเลขศาสตร์หากไม่ได้ส่งมา
            if (!$numerology_sum) {
                $numerology_sum = calculateNumerology($number);
                $numerology_meaning = getNumerologyMeaning($numerology_sum);
            }
            
            try {
                $query = "UPDATE products SET 
                         product_type = :product_type, 
                         number = :number, 
                         price = :price, 
                         network_provider = :network_provider, 
                         province = :province, 
                         status = :status,
                         numerology_sum = :numerology_sum, 
                         numerology_meaning = :numerology_meaning,
                         updated_at = CURRENT_TIMESTAMP
                         WHERE id = :id";
                
                $stmt = $db->prepare($query);
                
                // Prepare variables for binding
                $network_value = ($product_type == 'phone') ? $network_provider : null;
                $province_value = ($product_type == 'license') ? $province : null;
                
                $stmt->bindParam(':product_type', $product_type);
                $stmt->bindParam(':number', $number);
                $stmt->bindParam(':price', $price);
                $stmt->bindParam(':network_provider', $network_value);
                $stmt->bindParam(':province', $province_value);
                $stmt->bindParam(':status', $status);
                $stmt->bindParam(':numerology_sum', $numerology_sum);
                $stmt->bindParam(':numerology_meaning', $numerology_meaning);
                $stmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
                
                $stmt->execute();
                
                $success_message = "แก้ไขสินค้าเรียบร้อยแล้ว";
                
                // รีเฟรชข้อมูลสินค้า
                $stmt = $db->prepare("SELECT * FROM products WHERE id = :id");
                $stmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
                $stmt->execute();
                $product = $stmt->fetch();
                
            } catch (PDOException $e) {
                $error_message = "เกิดข้อผิดพลาดในการบันทึกข้อมูล: " . $e->getMessage();
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>แก้ไขสินค้า - จัดการสินค้า</title>
    
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
        
        .edit-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .edit-form {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .form-section {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin-bottom: 30px;
        }
        
        .current-product {
            background: #e3f2fd;
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

    <!-- Edit Header -->
    <section class="edit-header">
        <div class="container text-center">
            <h1><i class="fas fa-edit"></i> แก้ไขสินค้า</h1>
            <p class="lead">แก้ไขข้อมูลเบอร์โทรศัพท์หรือทะเบียนรถ</p>
        </div>
    </section>

    <!-- Edit Form -->
    <section class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="edit-form">
                        
                        <?php if ($error_message): ?>
                            <div class="alert alert-danger">
                                <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                            </div>
                            
                            <?php if (!$product): ?>
                                <div class="text-center">
                                    <a href="index.php" class="btn btn-primary">
                                        <i class="fas fa-arrow-left"></i> กลับหน้าจัดการ
                                    </a>
                                </div>
                            <?php endif; ?>
                            
                        <?php endif; ?>
                        
                        <?php if ($success_message): ?>
                            <div class="alert alert-success">
                                <i class="fas fa-check-circle"></i> <?= $success_message ?>
                            </div>
                        <?php endif; ?>
                        
                        <?php if ($product): ?>
                            
                            <!-- Current Product Info -->
                            <div class="current-product">
                                <h5><i class="fas fa-info-circle"></i> ข้อมูลปัจจุบัน</h5>
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
                                            <span class="status-badge status-<?= $product['status'] ?>">
                                                <?= $product['status'] == 'available' ? 'ว่าง' : 
                                                    ($product['status'] == 'reserved' ? 'จอง' : 'ขายแล้ว') ?>
                                            </span>
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
                                        <small class="text-muted">ID: <?= $product['id'] ?></small>
                                    </div>
                                </div>
                            </div>
                            
                            <form method="POST" id="editProductForm">
                                
                                <!-- Basic Information -->
                                <div class="form-section">
                                    <h5><i class="fas fa-edit"></i> แก้ไขข้อมูลพื้นฐาน</h5>
                                    
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>ประเภทสินค้า <span class="text-danger">*</span></label>
                                                <select name="product_type" class="form-control" required onchange="toggleFields(this.value)">
                                                    <option value="phone" <?= $product['product_type'] == 'phone' ? 'selected' : '' ?>>เบอร์โทรศัพท์</option>
                                                    <option value="license" <?= $product['product_type'] == 'license' ? 'selected' : '' ?>>ทะเบียนรถ</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>หมายเลข <span class="text-danger">*</span></label>
                                                <input type="text" name="number" class="form-control" required 
                                                       value="<?= $product['number'] ?>"
                                                       onchange="updateNumerology()">
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-4">
                                            <div class="form-group" id="networkField" <?= $product['product_type'] == 'license' ? 'style="display: none;"' : '' ?>>
                                                <label>เครือข่าย</label>
                                                <select name="network_provider" class="form-control">
                                                    <option value="">เลือกเครือข่าย</option>
                                                    <option value="AIS" <?= $product['network_provider'] == 'AIS' ? 'selected' : '' ?>>AIS</option>
                                                    <option value="DTAC" <?= $product['network_provider'] == 'DTAC' ? 'selected' : '' ?>>DTAC</option>
                                                    <option value="TRUE" <?= $product['network_provider'] == 'TRUE' ? 'selected' : '' ?>>TRUE</option>
                                                </select>
                                            </div>
                                            <div class="form-group" id="provinceField" <?= $product['product_type'] == 'phone' ? 'style="display: none;"' : '' ?>>
                                                <label>จังหวัด</label>
                                                <input type="text" name="province" class="form-control" 
                                                       value="<?= $product['province'] ?? '' ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="form-group">
                                                <label>ราคา (บาท) <span class="text-danger">*</span></label>
                                                <input type="number" name="price" class="form-control" required 
                                                       min="0" step="0.01" 
                                                       value="<?= $product['price'] ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="form-group">
                                                <label>สถานะ</label>
                                                <select name="status" class="form-control">
                                                    <option value="available" <?= $product['status'] == 'available' ? 'selected' : '' ?>>ว่าง</option>
                                                    <option value="reserved" <?= $product['status'] == 'reserved' ? 'selected' : '' ?>>จอง</option>
                                                    <option value="sold" <?= $product['status'] == 'sold' ? 'selected' : '' ?>>ขายแล้ว</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Numerology Information -->
                                <div class="form-section">
                                    <h5><i class="fas fa-calculator"></i> ข้อมูลเลขศาสตร์</h5>
                                    
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>ผลรวมเลขศาสตร์</label>
                                                <input type="number" name="numerology_sum" class="form-control" 
                                                       value="<?= $product['numerology_sum'] ?>" readonly>
                                                <small class="text-muted">จะคำนวณอัตโนมัติจากหมายเลข</small>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>ความหมายเลขศาสตร์</label>
                                                <input type="text" name="numerology_meaning" class="form-control" 
                                                       value="<?= $product['numerology_meaning'] ?>" readonly>
                                                <small class="text-muted">จะกำหนดอัตโนมัติตามผลรวม</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Submit Buttons -->
                                <div class="row mt-4">
                                    <div class="col-md-4">
                                        <a href="index.php" class="btn btn-secondary btn-block">
                                            <i class="fas fa-times"></i> ยกเลิก
                                        </a>
                                    </div>
                                    <div class="col-md-4">
                                        <button type="button" class="btn btn-danger btn-block" onclick="deleteProduct()">
                                            <i class="fas fa-trash"></i> ลบสินค้า
                                        </button>
                                    </div>
                                    <div class="col-md-4">
                                        <button type="submit" class="btn btn-primary btn-block">
                                            <i class="fas fa-save"></i> บันทึกการแก้ไข
                                        </button>
                                    </div>
                                </div>
                            </form>
                            
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

        // Update numerology
        function updateNumerology() {
            const number = $('input[name="number"]').val();
            if (number) {
                const sum = calculateNumerology(number);
                const meaning = getNumerologyMeaning(sum);
                
                $('input[name="numerology_sum"]').val(sum);
                $('input[name="numerology_meaning"]').val(meaning);
            }
        }

        // Auto calculate on number input
        $('input[name="number"]').on('input', updateNumerology);

        // Delete product
        function deleteProduct() {
            if (confirm('ต้องการลบสินค้านี้หรือไม่? การกระทำนี้ไม่สามารถย้อนกลับได้')) {
                window.location.href = `delete_product.php?id=<?= $product['id'] ?>`;
            }
        }

        // Form validation
        $('#editProductForm').on('submit', function(e) {
            const type = $('select[name="product_type"]').val();
            const number = $('input[name="number"]').val().trim();
            const price = parseFloat($('input[name="price"]').val());
            
            if (!type || !number || !price || price <= 0) {
                e.preventDefault();
                alert('กรุณากรอกข้อมูลให้ครบถ้วน');
                return false;
            }
            
            if (type === 'phone' && !$('select[name="network_provider"]').val()) {
                e.preventDefault();
                alert('กรุณาเลือกเครือข่าย');
                return false;
            }
            
            if (type === 'license' && !$('input[name="province"]').val().trim()) {
                e.preventDefault();
                alert('กรุณากรอกจังหวัด');
                return false;
            }
            
            return confirm('ต้องการบันทึกการแก้ไขหรือไม่?');
        });

        // Initialize form
        $(document).ready(function() {
            const currentType = $('select[name="product_type"]').val();
            toggleFields(currentType);
        });
    </script>
</body>
</html>