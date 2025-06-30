<?php
require_once 'config/database.php';

$success_message = '';
$error_message = '';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    $error_message = "ไม่สามารถเชื่อมต่อฐานข้อมูลได้";
}

if ($_POST && !$error_message) {
    $name = sanitize($_POST['name'] ?? '');
    $phone = sanitize($_POST['phone'] ?? '');
    $email = sanitize($_POST['email'] ?? '');
    $message = sanitize($_POST['message'] ?? '');
    
    // ตรวจสอบข้อมูลที่จำเป็น
    if (empty($name) || empty($phone) || empty($message)) {
        $error_message = "กรุณากรอกข้อมูลให้ครบถ้วน";
    } else {
        try {
            $query = "INSERT INTO contacts (name, phone, email, message) VALUES (:name, :phone, :email, :message)";
            $stmt = $db->prepare($query);
            $stmt->bindParam(':name', $name);
            $stmt->bindParam(':phone', $phone);
            $stmt->bindParam(':email', $email);
            $stmt->bindParam(':message', $message);
            
            $stmt->execute();
            
            $success_message = "ส่งข้อความเรียบร้อยแล้ว เจ้าหน้าที่จะติดต่อกลับโดยเร็ว";
            
            // ส่งอีเมลแจ้งเตือน (ถ้ามี email server)
            // sendContactNotification($name, $phone, $email, $message);
            
        } catch (PDOException $e) {
            $error_message = "เกิดข้อผิดพลาดในการส่งข้อความ กรุณาลองใหม่อีกครั้ง";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ติดต่อเรา - เบอร์สวย & ทะเบียนรถ</title>
    
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
        
        .contact-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .contact-form-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .contact-item {
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }
        
        .contact-item:hover {
            transform: translateY(-5px);
        }
        
        .contact-item i {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .contact-item h5 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .contact-item p {
            color: #666;
            margin: 0;
            font-size: 1.1rem;
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
        
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
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

    <!-- Contact Header -->
    <section class="contact-header">
        <div class="container text-center">
            <h1><i class="fas fa-envelope"></i> ติดต่อเรา</h1>
            <p class="lead">เราพร้อมให้บริการและตอบข้อสงสัยของคุณ</p>
        </div>
    </section>

    <!-- Contact Information -->
    <section class="py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-3 col-md-6">
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <h5>โทรศัพท์</h5>
                        <p>081-234-5678</p>
                        <small class="text-muted">จันทร์-เสาร์ 9:00-18:00</small>
                    </div>
                </div>
                
                <div class="col-lg-3 col-md-6">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <h5>อีเมล</h5>
                        <p>info@phonebeauty.com</p>
                        <small class="text-muted">ตอบกลับภายใน 24 ชม.</small>
                    </div>
                </div>
                
                <div class="col-lg-3 col-md-6">
                    <div class="contact-item">
                        <i class="fab fa-line"></i>
                        <h5>LINE Official</h5>
                        <p>@phonebeauty</p>
                        <small class="text-muted">แชทได้ตลอด 24 ชม.</small>
                    </div>
                </div>
                
                <div class="col-lg-3 col-md-6">
                    <div class="contact-item">
                        <i class="fab fa-facebook"></i>
                        <h5>Facebook</h5>
                        <p>เบอร์สวย & ทะเบียนรถ</p>
                        <small class="text-muted">ติดตามข่าวสารใหม่</small>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Form -->
    <section class="py-3">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="contact-form-section">
                        
                        <?php if ($success_message): ?>
                            <div class="success-animation">
                                <div class="success-icon">
                                    <i class="fas fa-check-circle"></i>
                                </div>
                                <div class="alert alert-success">
                                    <h4 class="alert-heading">ส่งข้อความสำเร็จ!</h4>
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
                                        <i class="fas fa-shopping-cart"></i> ดูสินค้า
                                    </a>
                                </div>
                            </div>
                            
                        <?php else: ?>
                            
                            <h4><i class="fas fa-paper-plane"></i> ส่งข้อความถึงเรา</h4>
                            <p class="text-muted">กรอกข้อมูลด้านล่างและเราจะติดต่อกลับโดยเร็ว</p>
                            
                            <?php if ($error_message): ?>
                                <div class="alert alert-danger">
                                    <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                                </div>
                            <?php endif; ?>
                            
                            <form method="POST" id="contactForm">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="name">ชื่อ-นามสกุล <span class="text-danger">*</span></label>
                                            <input type="text" name="name" id="name" class="form-control" required
                                                   value="<?= $_POST['name'] ?? '' ?>" placeholder="กรอกชื่อ-นามสกุล">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="phone">เบอร์โทรศัพท์ <span class="text-danger">*</span></label>
                                            <input type="tel" name="phone" id="phone" class="form-control" required
                                                   value="<?= $_POST['phone'] ?? '' ?>" placeholder="เช่น 081-234-5678">
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="form-group">
                                    <label for="email">อีเมล</label>
                                    <input type="email" name="email" id="email" class="form-control"
                                           value="<?= $_POST['email'] ?? '' ?>" placeholder="example@email.com">
                                    <small class="text-muted">ไม่บังคับ แต่จะช่วยให้เราติดต่อกลับได้สะดวกขึ้น</small>
                                </div>
                                
                                <div class="form-group">
                                    <label for="message">ข้อความ <span class="text-danger">*</span></label>
                                    <textarea name="message" id="message" class="form-control" rows="5" required
                                              placeholder="กรอกข้อความ หรือ สอบถามข้อมูลเกี่ยวกับสินค้า"><?= $_POST['message'] ?? '' ?></textarea>
                                </div>
                                
                                <div class="form-group">
                                    <div class="custom-control custom-checkbox">
                                        <input type="checkbox" class="custom-control-input" id="agree" required>
                                        <label class="custom-control-label" for="agree">
                                            ฉันยอมรับ<a href="#" class="text-primary">เงื่อนไขการใช้บริการ</a>และ<a href="#" class="text-primary">นโยบายความเป็นส่วนตัว</a>
                                        </label>
                                    </div>
                                </div>
                                
                                <div class="alert alert-info">
                                    <i class="fas fa-info-circle"></i>
                                    <strong>หมายเหตุ:</strong> ข้อมูลของท่านจะถูกเก็บเป็นความลับและใช้เพื่อการติดต่อกลับเท่านั้น
                                </div>
                                
                                <button type="submit" class="btn btn-primary btn-lg btn-block">
                                    <i class="fas fa-paper-plane"></i> ส่งข้อความ
                                </button>
                            </form>
                            
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Additional Contact Info -->
    <?php if (!$success_message): ?>
    <section class="py-5" style="background: #f8f9fa;">
        <div class="container">
            <div class="row">
                <div class="col-lg-4">
                    <div class="text-center mb-4">
                        <i class="fas fa-clock fa-3x text-primary mb-3"></i>
                        <h5>เวลาทำการ</h5>
                        <p class="mb-1">จันทร์ - เสาร์: 9:00 - 18:00</p>
                        <p class="mb-0">อาทิตย์: 10:00 - 16:00</p>
                    </div>
                </div>
                
                <div class="col-lg-4">
                    <div class="text-center mb-4">
                        <i class="fas fa-headset fa-3x text-primary mb-3"></i>
                        <h5>การสนับสนุน</h5>
                        <p class="mb-1">แชท LINE: ตลอด 24 ชม.</p>
                        <p class="mb-0">โทรศัพท์: เวลาทำการ</p>
                    </div>
                </div>
                
                <div class="col-lg-4">
                    <div class="text-center mb-4">
                        <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                        <h5>ความปลอดภัย</h5>
                        <p class="mb-1">ข้อมูลเข้ารหัส SSL</p>
                        <p class="mb-0">ปกป้องข้อมูลส่วนตัว</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <?php endif; ?>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Auto format phone number
        $('#phone').on('input', function() {
            let value = $(this).val().replace(/[^0-9]/g, '');
            if (value.length > 3 && value.length <= 6) {
                value = value.substring(0, 3) + '-' + value.substring(3);
            } else if (value.length > 6) {
                value = value.substring(0, 3) + '-' + value.substring(3, 6) + '-' + value.substring(6, 10);
            }
            $(this).val(value);
        });

        // Form validation
        $('#contactForm').on('submit', function(e) {
            const name = $('#name').val().trim();
            const phone = $('#phone').val().trim();
            const message = $('#message').val().trim();
            const agree = $('#agree').is(':checked');
            
            if (!name || !phone || !message) {
                e.preventDefault();
                alert('กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน');
                return false;
            }
            
            if (!agree) {
                e.preventDefault();
                alert('กรุณายอมรับเงื่อนไขการใช้บริการ');
                return false;
            }
            
            // ตรวจสอบรูปแบบเบอร์โทร
            const phonePattern = /^[0-9]{9,10}$/;
            if (!phonePattern.test(phone.replace(/-/g, ''))) {
                e.preventDefault();
                alert('กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง');
                return false;
            }
            
            // Show loading state
            const submitBtn = $(this).find('button[type="submit"]');
            submitBtn.html('<i class="fas fa-spinner fa-spin"></i> กำลังส่ง...').prop('disabled', true);
            
            return true;
        });

        // Character counter for message
        $('#message').on('input', function() {
            const maxLength = 1000;
            const currentLength = $(this).val().length;
            const remaining = maxLength - currentLength;
            
            if (!$(this).next('.char-counter').length) {
                $(this).after(`<small class="char-counter text-muted"></small>`);
            }
            
            $(this).next('.char-counter').text(`${currentLength}/${maxLength} ตัวอักษร`);
            
            if (remaining < 50) {
                $(this).next('.char-counter').removeClass('text-muted').addClass('text-warning');
            }
            
            if (remaining < 0) {
                $(this).next('.char-counter').removeClass('text-warning').addClass('text-danger');
                $(this).val($(this).val().substring(0, maxLength));
            }
        });

        // Auto-close success message
        setTimeout(function() {
            $('.alert-success').fadeOut();
        }, 10000);
    </script>
</body>
</html>