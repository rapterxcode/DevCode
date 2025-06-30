<?php
require_once '../config/database.php';

$success_message = '';
$error_message = '';

if ($_POST) {
    $product_type = sanitize($_POST['product_type'] ?? '');
    $number = sanitize($_POST['number'] ?? '');
    $price = (float)($_POST['price'] ?? 0);
    $network_provider = sanitize($_POST['network_provider'] ?? '');
    $province = sanitize($_POST['province'] ?? '');
    $numerology_sum = (int)($_POST['numerology_sum'] ?? 0);
    $numerology_meaning = sanitize($_POST['numerology_meaning'] ?? '');
    
    // ตรวจสอบข้อมูลที่จำเป็น
    if (empty($product_type) || empty($number) || $price <= 0) {
        $error_message = "กรุณากรอกข้อมูลให้ครบถ้วน";
    } else {
        // ตรวจสอบว่าหมายเลขซ้ำหรือไม่
        $check_query = "SELECT id FROM products WHERE number = :number AND product_type = :product_type";
        $check_stmt = $db->prepare($check_query);
        $check_stmt->bindParam(':number', $number);
        $check_stmt->bindParam(':product_type', $product_type);
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
                $query = "INSERT INTO products (product_type, number, price, network_provider, province, numerology_sum, numerology_meaning) 
                         VALUES (:product_type, :number, :price, :network_provider, :province, :numerology_sum, :numerology_meaning)";
                
                $stmt = $db->prepare($query);
                
                // Prepare variables for binding
                $network_value = ($product_type == 'phone') ? $network_provider : null;
                $province_value = ($product_type == 'license') ? $province : null;
                
                $stmt->bindParam(':product_type', $product_type);
                $stmt->bindParam(':number', $number);
                $stmt->bindParam(':price', $price);
                $stmt->bindParam(':network_provider', $network_value);
                $stmt->bindParam(':province', $province_value);
                $stmt->bindParam(':numerology_sum', $numerology_sum);
                $stmt->bindParam(':numerology_meaning', $numerology_meaning);
                
                $stmt->execute();
                
                $success_message = "เพิ่มสินค้าเรียบร้อยแล้ว";
                
                // Redirect กลับไปหน้าจัดการสินค้า
                header("Location: index.php?success=1");
                exit();
                
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
    <title>เพิ่มสินค้าใหม่ - จัดการสินค้า</title>
    
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
        
        .add-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .add-form {
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
        
        .preview-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
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
            margin: 15px 0;
        }
        
        .license-plate {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 10px;
            border-radius: 8px;
            border: 3px solid #333;
            display: inline-block;
        }
        
        .numerology-display {
            background: #e3f2fd;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
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

    <!-- Add Header -->
    <section class="add-header">
        <div class="container text-center">
            <h1><i class="fas fa-plus-circle"></i> เพิ่มสินค้าใหม่</h1>
            <p class="lead">เพิ่มเบอร์โทรศัพท์หรือทะเบียนรถใหม่เข้าสู่ระบบ</p>
        </div>
    </section>

    <!-- Add Form -->
    <section class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="add-form">
                        
                        <?php if ($error_message): ?>
                            <div class="alert alert-danger">
                                <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                            </div>
                        <?php endif; ?>
                        
                        <form method="POST" id="addProductForm">
                            
                            <!-- Basic Information -->
                            <div class="form-section">
                                <h5><i class="fas fa-info-circle"></i> ข้อมูลพื้นฐาน</h5>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label>ประเภทสินค้า <span class="text-danger">*</span></label>
                                            <select name="product_type" class="form-control" required onchange="toggleFields(this.value); updatePreview()">
                                                <option value="">เลือกประเภท</option>
                                                <option value="phone" <?= isset($_POST['product_type']) && $_POST['product_type'] == 'phone' ? 'selected' : '' ?>>เบอร์โทรศัพท์</option>
                                                <option value="license" <?= isset($_POST['product_type']) && $_POST['product_type'] == 'license' ? 'selected' : '' ?>>ทะเบียนรถ</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label>หมายเลข <span class="text-danger">*</span></label>
                                            <input type="text" name="number" class="form-control" required 
                                                   placeholder="เช่น 081-234-5678 หรือ 8888"
                                                   value="<?= $_POST['number'] ?? '' ?>"
                                                   onchange="updatePreview()">
                                            <small class="text-muted">สำหรับเบอร์โทร: รองรับรูปแบบ 081-234-5678 หรือ 0812345678</small>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group" id="networkField" style="display: none;">
                                            <label>เครือข่าย <span class="text-danger">*</span></label>
                                            <select name="network_provider" class="form-control" onchange="updatePreview()">
                                                <option value="">เลือกเครือข่าย</option>
                                                <option value="AIS" <?= isset($_POST['network_provider']) && $_POST['network_provider'] == 'AIS' ? 'selected' : '' ?>>AIS</option>
                                                <option value="DTAC" <?= isset($_POST['network_provider']) && $_POST['network_provider'] == 'DTAC' ? 'selected' : '' ?>>DTAC</option>
                                                <option value="TRUE" <?= isset($_POST['network_provider']) && $_POST['network_provider'] == 'TRUE' ? 'selected' : '' ?>>TRUE</option>
                                            </select>
                                        </div>
                                        <div class="form-group" id="provinceField" style="display: none;">
                                            <label>จังหวัด <span class="text-danger">*</span></label>
                                            <input type="text" name="province" class="form-control" 
                                                   placeholder="เช่น กรุงเทพมหานคร"
                                                   value="<?= $_POST['province'] ?? '' ?>"
                                                   onchange="updatePreview()">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label>ราคา (บาท) <span class="text-danger">*</span></label>
                                            <input type="number" name="price" class="form-control" required 
                                                   min="0" step="0.01" 
                                                   value="<?= $_POST['price'] ?? '' ?>"
                                                   onchange="updatePreview()">
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
                                            <input type="number" name="numerology_sum" class="form-control" readonly>
                                            <small class="text-muted">จะคำนวณอัตโนมัติจากหมายเลข</small>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label>ความหมายเลขศาสตร์</label>
                                            <input type="text" name="numerology_meaning" class="form-control" readonly>
                                            <small class="text-muted">จะกำหนดอัตโนมัติตามผลรวม</small>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="numerology-display" id="numerologyDisplay" style="display: none;">
                                    <h6><i class="fas fa-star"></i> ผลการคำนวณเลขศาสตร์</h6>
                                    <div id="numerologyResult"></div>
                                </div>
                            </div>
                            
                            <!-- Preview -->
                            <div class="preview-box" id="previewBox" style="display: none;">
                                <h5><i class="fas fa-eye"></i> ตัวอย่างการแสดงผล</h5>
                                <div id="productPreview"></div>
                            </div>
                            
                            <!-- Submit Buttons -->
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <a href="index.php" class="btn btn-secondary btn-block">
                                        <i class="fas fa-times"></i> ยกเลิก
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <button type="submit" class="btn btn-primary btn-block">
                                        <i class="fas fa-save"></i> บันทึกสินค้า
                                    </button>
                                </div>
                            </div>
                        </form>
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

        // Update preview
        function updatePreview() {
            const type = $('select[name="product_type"]').val();
            const number = $('input[name="number"]').val();
            const network = $('select[name="network_provider"]').val();
            const province = $('input[name="province"]').val();
            const price = $('input[name="price"]').val();
            
            if (number) {
                // Calculate numerology
                const sum = calculateNumerology(number);
                const meaning = getNumerologyMeaning(sum);
                
                $('input[name="numerology_sum"]').val(sum);
                $('input[name="numerology_meaning"]').val(meaning);
                
                // Show numerology result
                $('#numerologyResult').html(`
                    <div class="row">
                        <div class="col-6">
                            <div class="h4 text-primary">${sum}</div>
                            <small>ผลรวม</small>
                        </div>
                        <div class="col-6">
                            <div class="text-info font-weight-bold">${meaning}</div>
                            <small>ความหมาย</small>
                        </div>
                    </div>
                `);
                $('#numerologyDisplay').show();
                
                // Show preview
                if (type && (network || province) && price) {
                    let badgeHtml = '';
                    let numberHtml = number;
                    
                    if (type === 'phone') {
                        badgeHtml = `<span class="network-badge network-${network.toLowerCase()}">${network}</span>`;
                    } else if (type === 'license') {
                        badgeHtml = `<span class="province-badge">${province}</span>`;
                        numberHtml = `<span class="license-plate">${number}</span>`;
                    }
                    
                    $('#productPreview').html(`
                        <div class="card">
                            <div class="card-body text-center">
                                <div class="mb-2">
                                    ${badgeHtml}
                                    <span class="badge badge-success ml-2">ว่าง</span>
                                </div>
                                <div class="product-number">${numberHtml}</div>
                                <div class="mb-2">
                                    <small>ผลรวม: <strong>${sum}</strong></small><br>
                                    <small class="text-primary">${meaning}</small>
                                </div>
                                <div class="h5 text-success">฿${parseInt(price || 0).toLocaleString()}</div>
                            </div>
                        </div>
                    `);
                    $('#previewBox').show();
                } else {
                    $('#previewBox').hide();
                }
            } else {
                $('#numerologyDisplay, #previewBox').hide();
                $('input[name="numerology_sum"], input[name="numerology_meaning"]').val('');
            }
        }

        // Auto calculate on number input
        $('input[name="number"]').on('input', updatePreview);

        // Initialize form
        $(document).ready(function() {
            const currentType = $('select[name="product_type"]').val();
            if (currentType) {
                toggleFields(currentType);
                updatePreview();
            }
        });

        // Form validation
        $('#addProductForm').on('submit', function(e) {
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
            
            return confirm('ต้องการเพิ่มสินค้านี้หรือไม่?');
        });
    </script>
</body>
</html>