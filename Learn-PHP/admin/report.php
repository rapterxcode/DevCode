<?php
require_once '../config/database.php';

// ตัวแปรเริ่มต้น
$product_stats = [];
$sales_stats = [];
$numerology_stats = [];
$contact_stats = [];
$monthly_report = [];
$network_stats = [];
$province_stats = [];
$price_range_stats = [];
$error_message = '';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    $error_message = "ไม่สามารถเชื่อมต่อฐานข้อมูลได้";
} else {
    try {
        // ดึงสถิติรายการสินค้า
        $product_stats = getProductStats($db);
        
        // ดึงสถิติการขาย
        $sales_stats = getSalesStats($db);
        
        // ดึงข้อมูลเลขศาสตร์ยอดนิยม
        $numerology_stats = getNumerologyStats($db);
        
        // ดึงข้อมูลการติดต่อ
        $contact_stats = getContactStats($db);
        
        // ดึงรายงานรายเดือน
        $monthly_report = getMonthlyReport($db);
        
        // ดึงสถิติเครือข่าย
        $network_stats = getNetworkStats($db);
        
        // ดึงสถิติจังหวัด
        $province_stats = getProvinceStats($db);
        
        // ดึงสถิติช่วงราคา
        $price_range_stats = getPriceRangeStats($db);
        
    } catch (Exception $e) {
        $error_message = "เกิดข้อผิดพลาดในการสร้างรายงาน: " . $e->getMessage();
        error_log("Report error: " . $e->getMessage());
    }
}

function getProductStats($db) {
    try {
        $query = "
            SELECT 
                product_type,
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'available' THEN 1 END) as available,
                COUNT(CASE WHEN status = 'reserved' THEN 1 END) as reserved,
                COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold,
                COALESCE(AVG(price), 0) as avg_price,
                COALESCE(MIN(price), 0) as min_price,
                COALESCE(MAX(price), 0) as max_price,
                COALESCE(SUM(CASE WHEN status = 'available' THEN price ELSE 0 END), 0) as available_value
            FROM products 
            GROUP BY product_type
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        // ถ้าไม่มีข้อมูล ให้ return ข้อมูลเริ่มต้น
        if (empty($result)) {
            return [
                ['product_type' => 'phone', 'total' => 0, 'available' => 0, 'reserved' => 0, 'sold' => 0, 'avg_price' => 0, 'min_price' => 0, 'max_price' => 0, 'available_value' => 0],
                ['product_type' => 'license', 'total' => 0, 'available' => 0, 'reserved' => 0, 'sold' => 0, 'avg_price' => 0, 'min_price' => 0, 'max_price' => 0, 'available_value' => 0]
            ];
        }
        
        return $result;
    } catch (PDOException $e) {
        error_log("getProductStats error: " . $e->getMessage());
        return [];
    }
}

function getSalesStats($db) {
    try {
        $query = "
            SELECT 
                COUNT(*) as total_orders,
                COUNT(CASE WHEN order_status = 'confirmed' THEN 1 END) as confirmed_orders,
                COUNT(CASE WHEN order_status = 'pending' THEN 1 END) as pending_orders,
                COUNT(CASE WHEN order_status = 'cancelled' THEN 1 END) as cancelled_orders,
                COALESCE(SUM(CASE WHEN order_status = 'confirmed' THEN p.price ELSE 0 END), 0) as total_revenue,
                COALESCE(AVG(CASE WHEN order_status = 'confirmed' THEN p.price ELSE NULL END), 0) as avg_order_value
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetch();
        
        // ถ้าไม่มีข้อมูล ให้ return ข้อมูลเริ่มต้น
        if (!$result) {
            return [
                'total_orders' => 0,
                'confirmed_orders' => 0,
                'pending_orders' => 0,
                'cancelled_orders' => 0,
                'total_revenue' => 0,
                'avg_order_value' => 0
            ];
        }
        
        return $result;
    } catch (PDOException $e) {
        error_log("getSalesStats error: " . $e->getMessage());
        return [
            'total_orders' => 0,
            'confirmed_orders' => 0,
            'pending_orders' => 0,
            'cancelled_orders' => 0,
            'total_revenue' => 0,
            'avg_order_value' => 0
        ];
    }
}

function getNumerologyStats($db) {
    try {
        $query = "
            SELECT 
                numerology_sum,
                numerology_meaning,
                COUNT(*) as product_count,
                COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold_count,
                COALESCE(AVG(price), 0) as avg_price,
                COALESCE(ROUND((COUNT(CASE WHEN status = 'sold' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)), 2), 0) as sold_percentage
            FROM products 
            WHERE numerology_sum IS NOT NULL
            GROUP BY numerology_sum, numerology_meaning
            HAVING COUNT(*) >= 1
            ORDER BY sold_percentage DESC, sold_count DESC
            LIMIT 10
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        return $result ?: [];
    } catch (PDOException $e) {
        error_log("getNumerologyStats error: " . $e->getMessage());
        return [];
    }
}

function getContactStats($db) {
    try {
        $query = "
            SELECT 
                COUNT(*) as total_contacts,
                COUNT(CASE WHEN status = 'new' THEN 1 END) as new_contacts,
                COUNT(CASE WHEN status = 'replied' THEN 1 END) as replied_contacts,
                COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_contacts
            FROM contacts
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetch();
        
        // ถ้าไม่มีข้อมูล ให้ return ข้อมูลเริ่มต้น
        if (!$result) {
            return [
                'total_contacts' => 0,
                'new_contacts' => 0,
                'replied_contacts' => 0,
                'closed_contacts' => 0
            ];
        }
        
        return $result;
    } catch (PDOException $e) {
        error_log("getContactStats error: " . $e->getMessage());
        return [
            'total_contacts' => 0,
            'new_contacts' => 0,
            'replied_contacts' => 0,
            'closed_contacts' => 0
        ];
    }
}

function getMonthlyReport($db) {
    try {
        $query = "
            SELECT 
                DATE_FORMAT(order_date, '%Y-%m') as month,
                DATE_FORMAT(order_date, '%m/%Y') as month_thai,
                COUNT(*) as total_orders,
                COUNT(CASE WHEN order_status = 'confirmed' THEN 1 END) as confirmed_orders,
                COALESCE(SUM(CASE WHEN order_status = 'confirmed' THEN p.price ELSE 0 END), 0) as revenue
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY month DESC
            LIMIT 12
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        return $result ?: [];
    } catch (PDOException $e) {
        error_log("getMonthlyReport error: " . $e->getMessage());
        return [];
    }
}

function getNetworkStats($db) {
    try {
        $query = "
            SELECT 
                network_provider,
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold,
                COALESCE(AVG(price), 0) as avg_price,
                COALESCE(SUM(CASE WHEN status = 'available' THEN price ELSE 0 END), 0) as available_value
            FROM products 
            WHERE product_type = 'phone' AND network_provider IS NOT NULL
            GROUP BY network_provider
            ORDER BY total DESC
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        return $result ?: [];
    } catch (PDOException $e) {
        error_log("getNetworkStats error: " . $e->getMessage());
        return [];
    }
}

function getProvinceStats($db) {
    try {
        $query = "
            SELECT 
                province,
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold,
                COALESCE(AVG(price), 0) as avg_price,
                COALESCE(SUM(CASE WHEN status = 'available' THEN price ELSE 0 END), 0) as available_value
            FROM products 
            WHERE product_type = 'license' AND province IS NOT NULL
            GROUP BY province
            ORDER BY total DESC
            LIMIT 10
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        return $result ?: [];
    } catch (PDOException $e) {
        error_log("getProvinceStats error: " . $e->getMessage());
        return [];
    }
}

function getPriceRangeStats($db) {
    try {
        $query = "
            SELECT 
                CASE 
                    WHEN price < 10000 THEN 'ต่ำกว่า 10,000'
                    WHEN price BETWEEN 10000 AND 20000 THEN '10,000-20,000'
                    WHEN price BETWEEN 20001 AND 30000 THEN '20,001-30,000'
                    WHEN price BETWEEN 30001 AND 50000 THEN '30,001-50,000'
                    ELSE 'มากกว่า 50,000'
                END as price_range,
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold,
                COALESCE(AVG(price), 0) as avg_price
            FROM products 
            GROUP BY 
                CASE 
                    WHEN price < 10000 THEN 'ต่ำกว่า 10,000'
                    WHEN price BETWEEN 10000 AND 20000 THEN '10,000-20,000'
                    WHEN price BETWEEN 20001 AND 30000 THEN '20,001-30,000'
                    WHEN price BETWEEN 30001 AND 50000 THEN '30,001-50,000'
                    ELSE 'มากกว่า 50,000'
                END
            ORDER BY AVG(price)
        ";
        
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll();
        
        return $result ?: [];
    } catch (PDOException $e) {
        error_log("getPriceRangeStats error: " . $e->getMessage());
        return [];
    }
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>รายงานสถิติ - จัดการสินค้า</title>
    
    <!-- Bootstrap 4 CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            font-family: 'Kanit', sans-serif; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .navbar-brand { 
            font-weight: 600; 
            font-size: 1.5rem;
        }
        
        .report-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0 50px;
            margin-top: -56px;
            padding-top: 106px;
            position: relative;
            overflow: hidden;
        }
        
        .report-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="80" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="60" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="90" cy="30" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="10" cy="70" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .report-title {
            font-size: 3rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
        }
        
        .report-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            position: relative;
            z-index: 2;
        }
        
        .report-content {
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .stats-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 25px;
            transition: all 0.3s ease;
            border-left: 5px solid #667eea;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 5px;
            color: #667eea;
        }
        
        .stats-label {
            font-size: 1rem;
            font-weight: 500;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .table-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            border-top: 4px solid #667eea;
        }
        
        .table-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .table-title i {
            margin-right: 10px;
            color: #667eea;
        }
        
        .table-responsive {
            border-radius: 10px;
            overflow: hidden;
        }
        
        .table thead th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-weight: 600;
            padding: 15px;
            font-size: 0.9rem;
        }
        
        .table tbody tr {
            transition: all 0.3s ease;
        }
        
        .table tbody tr:hover {
            background-color: #f8f9ff;
        }
        
        .table tbody td {
            padding: 12px 15px;
            vertical-align: middle;
        }
        
        .progress-custom {
            height: 8px;
            border-radius: 50px;
            background: #e9ecef;
        }
        
        .progress-custom .progress-bar {
            border-radius: 50px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .badge-custom {
            padding: 6px 12px;
            border-radius: 15px;
            font-weight: 500;
            font-size: 0.8rem;
        }
        
        .section-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
            margin: 40px 0;
            border-radius: 2px;
        }
        
        .summary-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .summary-box h3 {
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .summary-item {
            display: inline-block;
            margin: 0 20px;
            text-align: center;
        }
        
        .summary-item h4 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .summary-item span {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        @media print {
            .navbar, .btn, .no-print { display: none !important; }
            .report-header { margin-top: 0; padding-top: 20px; }
            .report-content { margin-top: 0; }
            body { background: white; }
        }
        
        @media (max-width: 768px) {
            .report-title { font-size: 2rem; }
            .stats-number { font-size: 2rem; }
            .table-container { padding: 20px; }
            .summary-item { margin: 10px 0; display: block; }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top no-print" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand" href="../index.php">
                <i class="fas fa-phone-alt text-warning"></i> เบอร์สวย & ทะเบียนรถ
            </a>
            
            <div class="ml-auto">
                <button class="btn btn-light mr-3" onclick="window.print()">
                    <i class="fas fa-print"></i> พิมพ์รายงาน
                </button>
                <button class="btn btn-info mr-3" onclick="exportReport()">
                    <i class="fas fa-download"></i> ส่งออกรายงาน
                </button>
                <a href="index.php" class="btn btn-warning">
                    <i class="fas fa-arrow-left"></i> กลับหน้าจัดการ
                </a>
            </div>
        </div>
    </nav>

    <!-- Report Header -->
    <section class="report-header">
        <div class="container text-center mt-10">
            <h1 class="report-title">
                <i class="fas fa-file-alt"></i> รายงานสถิติธุรกิจ
            </h1>
            <p class="report-subtitle">
                การวิเคราะห์ข้อมูลการขายและการจัดการสินค้า<br>
                <i class="fas fa-clock"></i> อัพเดท ณ วันที่ <?= date('d/m/Y H:i:s') ?> น.
            </p>
        </div>
    </section>

    <!-- Report Content -->
    <div class="report-content">
        <div class="container py-5">
            
            <?php if (!empty($error_message)): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> <?= $error_message ?>
                </div>
            <?php else: ?>
                
                <!-- สรุปสถิติหลัก -->
                <div class="summary-box">
                    <h3><i class="fas fa-chart-bar"></i> สรุปข้อมูลภาพรวม</h3>
                    <div class="row">
                        <div class="col-md-3">
                            <div class="summary-item">
                                <h4><?= !empty($product_stats) ? array_sum(array_column($product_stats, 'total')) : 0 ?></h4>
                                <span>สินค้าทั้งหมด</span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="summary-item">
                                <h4><?= isset($sales_stats['confirmed_orders']) ? $sales_stats['confirmed_orders'] : 0 ?></h4>
                                <span>ยอดขายสำเร็จ</span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="summary-item">
                                <h4><?= isset($sales_stats['pending_orders']) ? $sales_stats['pending_orders'] : 0 ?></h4>
                                <span>รอดำเนินการ</span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="summary-item">
                                <h4>฿<?= number_format(isset($sales_stats['total_revenue']) ? $sales_stats['total_revenue'] : 0, 0) ?></h4>
                                <span>รายได้รวม</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- รายละเอียดสินค้าตามประเภท -->
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-boxes"></i> รายละเอียดสินค้าตามประเภท
                    </h5>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>ประเภทสินค้า</th>
                                    <th>จำนวนทั้งหมด</th>
                                    <th>ว่าง</th>
                                    <th>จองแล้ว</th>
                                    <th>ขายแล้ว</th>
                                    <th>ราคาเฉลี่ย</th>
                                    <th>มูลค่าคงเหลือ</th>
                                    <th>อัตราการขาย</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($product_stats as $stat): ?>
                                <tr>
                                    <td>
                                        <span class="badge badge-custom badge-<?= $stat['product_type'] == 'phone' ? 'primary' : 'info' ?>">
                                            <i class="fas fa-<?= $stat['product_type'] == 'phone' ? 'mobile-alt' : 'car' ?>"></i>
                                            <?= $stat['product_type'] == 'phone' ? 'เบอร์โทรศัพท์' : 'ทะเบียนรถ' ?>
                                        </span>
                                    </td>
                                    <td><strong><?= number_format($stat['total']) ?></strong></td>
                                    <td><span class="badge badge-success"><?= number_format($stat['available']) ?></span></td>
                                    <td><span class="badge badge-warning"><?= number_format($stat['reserved']) ?></span></td>
                                    <td><span class="badge badge-danger"><?= number_format($stat['sold']) ?></span></td>
                                    <td>฿<?= number_format($stat['avg_price'], 0) ?></td>
                                    <td>฿<?= number_format($stat['available_value'], 0) ?></td>
                                    <td>
                                        <?php 
                                        $sale_rate = $stat['total'] > 0 ? round(($stat['sold'] * 100) / $stat['total'], 1) : 0;
                                        ?>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-custom flex-grow-1 mr-2" style="min-width: 80px;">
                                                <div class="progress-bar" style="width: <?= $sale_rate ?>%"></div>
                                            </div>
                                            <small><strong><?= $sale_rate ?>%</strong></small>
                                        </div>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- รายงานยอดขายรายเดือน -->
                <?php if (!empty($monthly_report)): ?>
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-calendar-alt"></i> รายงานยอดขาย 12 เดือนที่ผ่านมา
                    </h5>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>เดือน/ปี</th>
                                    <th>คำสั่งซื้อทั้งหมด</th>
                                    <th>คำสั่งซื้อสำเร็จ</th>
                                    <th>รายได้</th>
                                    <th>อัตราสำเร็จ</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($monthly_report as $month): ?>
                                <tr>
                                    <td><strong><?= $month['month_thai'] ?></strong></td>
                                    <td><?= number_format($month['total_orders']) ?></td>
                                    <td><span class="badge badge-success"><?= number_format($month['confirmed_orders']) ?></span></td>
                                    <td><strong>฿<?= number_format($month['revenue'], 0) ?></strong></td>
                                    <td>
                                        <?php 
                                        $success_rate = $month['total_orders'] > 0 ? round(($month['confirmed_orders'] * 100) / $month['total_orders'], 1) : 0;
                                        ?>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-custom flex-grow-1 mr-2" style="min-width: 60px;">
                                                <div class="progress-bar bg-success" style="width: <?= $success_rate ?>%"></div>
                                            </div>
                                            <small><strong><?= $success_rate ?>%</strong></small>
                                        </div>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
                <?php endif; ?>

                <!-- เลขศาสตร์ยอดนิยม -->
                <?php if (!empty($numerology_stats)): ?>
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-star"></i> เลขศาสตร์ยอดนิยม (อันดับการขาย)
                    </h5>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>อันดับ</th>
                                    <th>เลขศาสตร์</th>
                                    <th>ความหมาย</th>
                                    <th>จำนวนสินค้า</th>
                                    <th>ขายแล้ว</th>
                                    <th>อัตราการขาย</th>
                                    <th>ราคาเฉลี่ย</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($numerology_stats as $index => $stat): ?>
                                <tr>
                                    <td>
                                        <?php if ($index == 0): ?>
                                            <span class="badge badge-warning"><i class="fas fa-trophy"></i> 1</span>
                                        <?php elseif ($index == 1): ?>
                                            <span class="badge badge-secondary"><i class="fas fa-medal"></i> 2</span>
                                        <?php elseif ($index == 2): ?>
                                            <span class="badge badge-dark"><i class="fas fa-medal"></i> 3</span>
                                        <?php else: ?>
                                            <span class="badge badge-light"><?= $index + 1 ?></span>
                                        <?php endif; ?>
                                    </td>
                                    <td><strong class="text-primary"><?= $stat['numerology_sum'] ?></strong></td>
                                    <td><?= $stat['numerology_meaning'] ?></td>
                                    <td><?= number_format($stat['product_count']) ?></td>
                                    <td><span class="badge badge-success"><?= number_format($stat['sold_count']) ?></span></td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-custom flex-grow-1 mr-2" style="min-width: 60px;">
                                                <div class="progress-bar bg-info" style="width: <?= $stat['sold_percentage'] ?>%"></div>
                                            </div>
                                            <small><strong><?= $stat['sold_percentage'] ?>%</strong></small>
                                        </div>
                                    </td>
                                    <td>฿<?= number_format($stat['avg_price'], 0) ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
                <?php endif; ?>

                <div class="section-divider"></div>

                <!-- สถิติตามเครือข่ายและจังหวัด -->
                <div class="row">
                    <!-- สถิติเครือข่าย -->
                    <?php if (!empty($network_stats)): ?>
                    <div class="col-lg-6 mb-4">
                        <div class="table-container">
                            <h5 class="table-title">
                                <i class="fas fa-signal"></i> สถิติตามเครือข่าย
                            </h5>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>เครือข่าย</th>
                                            <th>ทั้งหมด</th>
                                            <th>ขายแล้ว</th>
                                            <th>ราคาเฉลี่ย</th>
                                            <th>มูลค่าคงเหลือ</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($network_stats as $stat): ?>
                                        <tr>
                                            <td>
                                                <span class="badge badge-<?= strtolower($stat['network_provider']) == 'ais' ? 'success' : (strtolower($stat['network_provider']) == 'dtac' ? 'danger' : 'warning') ?>">
                                                    <?= $stat['network_provider'] ?>
                                                </span>
                                            </td>
                                            <td><?= number_format($stat['total']) ?></td>
                                            <td><span class="badge badge-info"><?= number_format($stat['sold']) ?></span></td>
                                            <td>฿<?= number_format($stat['avg_price'], 0) ?></td>
                                            <td>฿<?= number_format($stat['available_value'], 0) ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <?php endif; ?>
                    
                    <!-- สถิติจังหวัด -->
                    <?php if (!empty($province_stats)): ?>
                    <div class="col-lg-6 mb-4">
                        <div class="table-container">
                            <h5 class="table-title">
                                <i class="fas fa-map-marker-alt"></i> สถิติตามจังหวัด (Top 10)
                            </h5>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>จังหวัด</th>
                                            <th>ทั้งหมด</th>
                                            <th>ขายแล้ว</th>
                                            <th>ราคาเฉลี่ย</th>
                                            <th>มูลค่าคงเหลือ</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($province_stats as $stat): ?>
                                        <tr>
                                            <td><strong><?= $stat['province'] ?></strong></td>
                                            <td><?= number_format($stat['total']) ?></td>
                                            <td><span class="badge badge-info"><?= number_format($stat['sold']) ?></span></td>
                                            <td>฿<?= number_format($stat['avg_price'], 0) ?></td>
                                            <td>฿<?= number_format($stat['available_value'], 0) ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <?php endif; ?>
                </div>

                <!-- สถิติช่วงราคา -->
                <?php if (!empty($price_range_stats)): ?>
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-money-bill-wave"></i> สถิติตามช่วงราคา
                    </h5>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>ช่วงราคา (บาท)</th>
                                    <th>จำนวนสินค้า</th>
                                    <th>ขายแล้ว</th>
                                    <th>ราคาเฉลี่ย</th>
                                    <th>อัตราการขาย</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($price_range_stats as $stat): ?>
                                <tr>
                                    <td><strong><?= $stat['price_range'] ?></strong></td>
                                    <td><?= number_format($stat['total']) ?></td>
                                    <td><span class="badge badge-success"><?= number_format($stat['sold']) ?></span></td>
                                    <td>฿<?= number_format($stat['avg_price'], 0) ?></td>
                                    <td>
                                        <?php 
                                        $sale_rate = $stat['total'] > 0 ? round(($stat['sold'] * 100) / $stat['total'], 1) : 0;
                                        ?>
                                        <div class="d-flex align-items-center">
                                            <div class="progress progress-custom flex-grow-1 mr-2" style="min-width: 60px;">
                                                <div class="progress-bar bg-warning" style="width: <?= $sale_rate ?>%"></div>
                                            </div>
                                            <small><strong><?= $sale_rate ?>%</strong></small>
                                        </div>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
                <?php endif; ?>

                <!-- สถิติการติดต่อ -->
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-envelope"></i> สถิติการติดต่อ
                    </h5>
                    <div class="row text-center">
                        <div class="col-md-3">
                            <div class="stats-card">
                                <div class="stats-number text-primary"><?= $contact_stats['total_contacts'] ?></div>
                                <div class="stats-label">ทั้งหมด</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stats-card">
                                <div class="stats-number text-warning"><?= $contact_stats['new_contacts'] ?></div>
                                <div class="stats-label">ใหม่</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stats-card">
                                <div class="stats-number text-success"><?= $contact_stats['replied_contacts'] ?></div>
                                <div class="stats-label">ตอบแล้ว</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="stats-card">
                                <div class="stats-number text-secondary"><?= $contact_stats['closed_contacts'] ?></div>
                                <div class="stats-label">ปิดแล้ว</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- สรุปข้อมูลการขาย -->
                <div class="table-container">
                    <h5 class="table-title">
                        <i class="fas fa-calculator"></i> สรุปข้อมูลการขาย
                    </h5>
                    <div class="row">
                        <div class="col-md-4">
                            <div class="stats-card text-center">
                                <div class="stats-number"><?= $sales_stats['total_orders'] ?></div>
                                <div class="stats-label">คำสั่งซื้อทั้งหมด</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stats-card text-center">
                                <div class="stats-number">฿<?= number_format($sales_stats['avg_order_value'] ?? 0, 0) ?></div>
                                <div class="stats-label">ยอดขายเฉลี่ย</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stats-card text-center">
                                <div class="stats-number"><?= $sales_stats['total_orders'] > 0 ? round(($sales_stats['confirmed_orders'] * 100) / $sales_stats['total_orders'], 1) : 0 ?>%</div>
                                <div class="stats-label">อัตราการยืนยัน</div>
                            </div>
                        </div>
                    </div>
                </div>
                
            <?php endif; ?>
        </div>
    </div>

    <!-- Bootstrap 4 JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Export Report Function
        function exportReport() {
            const reportData = {
                product_stats: <?= json_encode($product_stats) ?>,
                sales_stats: <?= json_encode($sales_stats) ?>,
                numerology_stats: <?= json_encode($numerology_stats) ?>,
                contact_stats: <?= json_encode($contact_stats) ?>,
                monthly_report: <?= json_encode($monthly_report) ?>,
                network_stats: <?= json_encode($network_stats) ?>,
                province_stats: <?= json_encode($province_stats) ?>,
                price_range_stats: <?= json_encode($price_range_stats) ?>,
                generated_at: '<?= date('Y-m-d H:i:s') ?>'
            };
            
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(reportData, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "report_" + new Date().toISOString().slice(0,10) + ".json");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }

        // Auto refresh data every 5 minutes
        setInterval(function() {
            location.reload();
        }, 300000);
    </script>
</body>
</html>