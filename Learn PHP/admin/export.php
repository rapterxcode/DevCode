<?php
require_once '../config/database.php';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

// รับพารามิเตอร์
$export_type = $_GET['type'] ?? 'products';
$format = $_GET['format'] ?? 'csv';

try {
    switch ($export_type) {
        case 'products':
            exportProducts($db, $format);
            break;
        case 'orders':
            exportOrders($db, $format);
            break;
        case 'contacts':
            exportContacts($db, $format);
            break;
        case 'all':
            exportAll($db, $format);
            break;
        default:
            throw new Exception("ประเภทการส่งออกไม่ถูกต้อง");
    }
} catch (Exception $e) {
    header("Location: index.php?error=export_failed&message=" . urlencode($e->getMessage()));
    exit();
}

function exportProducts($db, $format) {
    $query = "SELECT 
                id,
                CASE 
                    WHEN product_type = 'phone' THEN 'เบอร์โทรศัพท์'
                    WHEN product_type = 'license' THEN 'ทะเบียนรถ'
                END as product_type_thai,
                number,
                COALESCE(network_provider, province) as network_or_province,
                price,
                CASE 
                    WHEN status = 'available' THEN 'ว่าง'
                    WHEN status = 'reserved' THEN 'จอง'
                    WHEN status = 'sold' THEN 'ขายแล้ว'
                END as status_thai,
                numerology_sum,
                numerology_meaning,
                DATE_FORMAT(created_at, '%d/%m/%Y %H:%i') as created_at_thai,
                DATE_FORMAT(updated_at, '%d/%m/%Y %H:%i') as updated_at_thai
              FROM products 
              ORDER BY created_at DESC";
    
    $stmt = $db->prepare($query);
    $stmt->execute();
    $data = $stmt->fetchAll();
    
    $headers = [
        'รหัส', 'ประเภท', 'หมายเลข', 'เครือข่าย/จังหวัด', 'ราคา', 'สถานะ', 
        'เลขศาสตร์', 'ความหมาย', 'วันที่สร้าง', 'วันที่แก้ไข'
    ];
    
    exportData($data, $headers, "products_" . date('Y-m-d'), $format);
}

function exportOrders($db, $format) {
    $query = "SELECT 
                o.id,
                o.customer_name,
                o.customer_phone,
                o.customer_email,
                CASE 
                    WHEN p.product_type = 'phone' THEN 'เบอร์โทรศัพท์'
                    WHEN p.product_type = 'license' THEN 'ทะเบียนรถ'
                END as product_type_thai,
                p.number,
                COALESCE(p.network_provider, p.province) as network_or_province,
                p.price,
                CASE 
                    WHEN o.order_status = 'pending' THEN 'รอดำเนินการ'
                    WHEN o.order_status = 'confirmed' THEN 'ยืนยันแล้ว'
                    WHEN o.order_status = 'cancelled' THEN 'ยกเลิก'
                END as order_status_thai,
                DATE_FORMAT(o.order_date, '%d/%m/%Y %H:%i') as order_date_thai,
                o.notes
              FROM orders o
              JOIN products p ON o.product_id = p.id
              ORDER BY o.order_date DESC";
    
    $stmt = $db->prepare($query);
    $stmt->execute();
    $data = $stmt->fetchAll();
    
    $headers = [
        'รหัสคำสั่งซื้อ', 'ชื่อลูกค้า', 'เบอร์โทร', 'อีเมล', 'ประเภทสินค้า', 
        'หมายเลข', 'เครือข่าย/จังหวัด', 'ราคา', 'สถานะ', 'วันที่สั่งซื้อ', 'หมายเหตุ'
    ];
    
    exportData($data, $headers, "orders_" . date('Y-m-d'), $format);
}

function exportContacts($db, $format) {
    $query = "SELECT 
                id,
                name,
                phone,
                email,
                message,
                CASE 
                    WHEN status = 'new' THEN 'ใหม่'
                    WHEN status = 'replied' THEN 'ตอบกลับแล้ว'
                    WHEN status = 'closed' THEN 'ปิด'
                END as status_thai,
                DATE_FORMAT(created_at, '%d/%m/%Y %H:%i') as created_at_thai
              FROM contacts 
              ORDER BY created_at DESC";
    
    $stmt = $db->prepare($query);
    $stmt->execute();
    $data = $stmt->fetchAll();
    
    $headers = [
        'รหัส', 'ชื่อ', 'เบอร์โทร', 'อีเมล', 'ข้อความ', 'สถานะ', 'วันที่ติดต่อ'
    ];
    
    exportData($data, $headers, "contacts_" . date('Y-m-d'), $format);
}

function exportAll($db, $format) {
    // สร้างไฟล์ ZIP ที่มีทุกข้อมูล
    $zip = new ZipArchive();
    $zipname = "all_data_" . date('Y-m-d_H-i-s') . ".zip";
    $temp_dir = sys_get_temp_dir() . "/export_" . time() . "/";
    
    if (!mkdir($temp_dir, 0777, true)) {
        throw new Exception("ไม่สามารถสร้างโฟลเดอร์ชั่วคราวได้");
    }
    
    $zip_path = $temp_dir . $zipname;
    
    if ($zip->open($zip_path, ZipArchive::CREATE) !== TRUE) {
        throw new Exception("ไม่สามารถสร้างไฟล์ ZIP ได้");
    }
    
    // Export แต่ละประเภทและเพิ่มใน ZIP
    ob_start();
    exportProducts($db, $format);
    $products_content = ob_get_clean();
    $zip->addFromString("products." . $format, $products_content);
    
    ob_start();
    exportOrders($db, $format);
    $orders_content = ob_get_clean();
    $zip->addFromString("orders." . $format, $orders_content);
    
    ob_start();
    exportContacts($db, $format);
    $contacts_content = ob_get_clean();
    $zip->addFromString("contacts." . $format, $contacts_content);
    
    $zip->close();
    
    // ส่งไฟล์ ZIP
    header('Content-Type: application/zip');
    header('Content-Disposition: attachment; filename="' . $zipname . '"');
    header('Content-Length: ' . filesize($zip_path));
    readfile($zip_path);
    
    // ลบไฟล์ชั่วคราว
    unlink($zip_path);
    rmdir($temp_dir);
    exit();
}

function exportData($data, $headers, $filename, $format) {
    if (empty($data)) {
        throw new Exception("ไม่มีข้อมูลสำหรับส่งออก");
    }
    
    switch ($format) {
        case 'csv':
            exportCSV($data, $headers, $filename);
            break;
        case 'excel':
            exportExcel($data, $headers, $filename);
            break;
        case 'json':
            exportJSON($data, $filename);
            break;
        default:
            throw new Exception("รูปแบบไฟล์ไม่ถูกต้อง");
    }
}

function exportCSV($data, $headers, $filename) {
    header('Content-Type: text/csv; charset=UTF-8');
    header('Content-Disposition: attachment; filename="' . $filename . '.csv"');
    
    // เพิ่ม BOM สำหรับ UTF-8
    echo "\xEF\xBB\xBF";
    
    $output = fopen('php://output', 'w');
    
    // เขียน headers
    fputcsv($output, $headers);
    
    // เขียนข้อมูล
    foreach ($data as $row) {
        fputcsv($output, array_values($row));
    }
    
    fclose($output);
    exit();
}

function exportExcel($data, $headers, $filename) {
    // สร้างไฟล์ Excel แบบง่าย (XML format)
    header('Content-Type: application/vnd.ms-excel; charset=UTF-8');
    header('Content-Disposition: attachment; filename="' . $filename . '.xls"');
    
    echo "\xEF\xBB\xBF"; // BOM
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    echo "<Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\"\n";
    echo " xmlns:o=\"urn:schemas-microsoft-com:office:office\"\n";
    echo " xmlns:x=\"urn:schemas-microsoft-com:office:excel\"\n";
    echo " xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"\n";
    echo " xmlns:html=\"http://www.w3.org/TR/REC-html40\">\n";
    echo "<Worksheet ss:Name=\"Sheet1\">\n";
    echo "<Table>\n";
    
    // Headers
    echo "<Row>\n";
    foreach ($headers as $header) {
        echo "<Cell><Data ss:Type=\"String\">" . htmlspecialchars($header, ENT_XML1) . "</Data></Cell>\n";
    }
    echo "</Row>\n";
    
    // Data
    foreach ($data as $row) {
        echo "<Row>\n";
        foreach (array_values($row) as $cell) {
            $type = is_numeric($cell) ? "Number" : "String";
            echo "<Cell><Data ss:Type=\"$type\">" . htmlspecialchars($cell, ENT_XML1) . "</Data></Cell>\n";
        }
        echo "</Row>\n";
    }
    
    echo "</Table>\n";
    echo "</Worksheet>\n";
    echo "</Workbook>\n";
    exit();
}

function exportJSON($data, $filename) {
    header('Content-Type: application/json; charset=UTF-8');
    header('Content-Disposition: attachment; filename="' . $filename . '.json"');
    
    echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit();
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ส่งออกข้อมูล - จัดการสินค้า</title>
    
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
        
        .export-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
        }
        
        .export-form {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .export-option {
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .export-option:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .export-option.selected {
            border-color: #667eea;
            background: #e3f2fd;
        }
        
        .format-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .format-btn {
            flex: 1;
            min-width: 120px;
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

    <!-- Export Header -->
    <section class="export-header">
        <div class="container text-center">
            <h1><i class="fas fa-download"></i> ส่งออกข้อมูล</h1>
            <p class="lead">เลือกข้อมูลและรูปแบบไฟล์ที่ต้องการส่งออก</p>
        </div>
    </section>

    <!-- Export Form -->
    <section class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="export-form">
                        
                        <h5><i class="fas fa-database"></i> เลือกข้อมูลที่ต้องการส่งออก</h5>
                        
                        <div class="export-option" data-type="products">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-boxes fa-2x text-primary mr-3"></i>
                                <div>
                                    <h6 class="mb-1">ข้อมูลสินค้า</h6>
                                    <small class="text-muted">เบอร์โทรศัพท์และทะเบียนรถทั้งหมด พร้อมราคาและสถานะ</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="export-option" data-type="orders">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-shopping-cart fa-2x text-success mr-3"></i>
                                <div>
                                    <h6 class="mb-1">ข้อมูลคำสั่งซื้อ</h6>
                                    <small class="text-muted">รายการคำสั่งซื้อทั้งหมด พร้อมข้อมูลลูกค้าและสถานะ</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="export-option" data-type="contacts">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-envelope fa-2x text-info mr-3"></i>
                                <div>
                                    <h6 class="mb-1">ข้อมูลการติดต่อ</h6>
                                    <small class="text-muted">ข้อความและการติดต่อจากลูกค้า</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="export-option" data-type="all">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-archive fa-2x text-warning mr-3"></i>
                                <div>
                                    <h6 class="mb-1">ข้อมูลทั้งหมด</h6>
                                    <small class="text-muted">ส่งออกข้อมูลทุกประเภทในไฟล์ ZIP เดียว</small>
                                </div>
                            </div>
                        </div>
                        
                        <hr>
                        
                        <h5><i class="fas fa-file-export"></i> เลือกรูปแบบไฟล์</h5>
                        
                        <div class="format-buttons">
                            <button class="btn btn-outline-primary format-btn" data-format="csv">
                                <i class="fas fa-file-csv"></i><br>
                                CSV<br>
                                <small>Excel, Numbers</small>
                            </button>
                            
                            <button class="btn btn-outline-success format-btn" data-format="excel">
                                <i class="fas fa-file-excel"></i><br>
                                Excel<br>
                                <small>Microsoft Excel</small>
                            </button>
                            
                            <button class="btn btn-outline-info format-btn" data-format="json">
                                <i class="fas fa-file-code"></i><br>
                                JSON<br>
                                <small>สำหรับนักพัฒนา</small>
                            </button>
                        </div>
                        
                        <hr>
                        
                        <div class="text-center">
                            <button class="btn btn-primary btn-lg" id="exportBtn" disabled>
                                <i class="fas fa-download"></i> ส่งออกข้อมูล
                            </button>
                        </div>
                        
                        <div class="mt-4 alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            <strong>หมายเหตุ:</strong>
                            <ul class="mb-0 mt-2">
                                <li>ไฟล์ CSV เหมาะสำหรับการเปิดใน Excel หรือ Google Sheets</li>
                                <li>ไฟล์ Excel จะมีการจัดรูปแบบที่สวยงามกว่า</li>
                                <li>ไฟล์ JSON เหมาะสำหรับการนำไปใช้ในระบบอื่น</li>
                                <li>การส่งออกข้อมูลทั้งหมดจะได้ไฟล์ ZIP ที่บรรจุไฟล์แยกตามประเภท</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        let selectedType = '';
        let selectedFormat = '';
        
        // Select export type
        $('.export-option').on('click', function() {
            $('.export-option').removeClass('selected');
            $(this).addClass('selected');
            selectedType = $(this).data('type');
            updateExportButton();
        });
        
        // Select format
        $('.format-btn').on('click', function() {
            $('.format-btn').removeClass('btn-primary btn-success btn-info').addClass('btn-outline-primary btn-outline-success btn-outline-info');
            
            if ($(this).hasClass('btn-outline-primary')) {
                $(this).removeClass('btn-outline-primary').addClass('btn-primary');
            } else if ($(this).hasClass('btn-outline-success')) {
                $(this).removeClass('btn-outline-success').addClass('btn-success');
            } else if ($(this).hasClass('btn-outline-info')) {
                $(this).removeClass('btn-outline-info').addClass('btn-info');
            }
            
            selectedFormat = $(this).data('format');
            updateExportButton();
        });
        
        // Update export button
        function updateExportButton() {
            if (selectedType && selectedFormat) {
                $('#exportBtn').prop('disabled', false);
            } else {
                $('#exportBtn').prop('disabled', true);
            }
        }
        
        // Export data
        $('#exportBtn').on('click', function() {
            if (!selectedType || !selectedFormat) {
                alert('กรุณาเลือกข้อมูลและรูปแบบไฟล์');
                return;
            }
            
            const exportUrl = `export.php?type=${selectedType}&format=${selectedFormat}`;
            
            // Show loading
            $(this).html('<i class="fas fa-spinner fa-spin"></i> กำลังส่งออก...').prop('disabled', true);
            
            // Create hidden link and click it
            const link = document.createElement('a');
            link.href = exportUrl;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Reset button after delay
            setTimeout(() => {
                $(this).html('<i class="fas fa-download"></i> ส่งออกข้อมูล').prop('disabled', false);
            }, 3000);
        });
    </script>
</body>
</html>