<?php
// ไฟล์สำหรับตั้งค่าระบบครั้งแรก
require_once 'config/database.php';

echo "<h2>ตั้งค่าระบบขายเบอร์สวยและทะเบียนรถ</h2>";

try {
    // ทดสอบการเชื่อมต่อฐานข้อมูล
    if (!$db) {
        throw new Exception("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
    }
    
    echo "<p>✅ เชื่อมต่อฐานข้อมูลสำเร็จ</p>";
    
    // ตรวจสอบและสร้างตาราง
    $tables = ['products', 'orders', 'contacts', 'admins'];
    
    foreach ($tables as $table) {
        $check_query = "SHOW TABLES LIKE '$table'";
        $stmt = $db->prepare($check_query);
        $stmt->execute();
        
        if ($stmt->rowCount() > 0) {
            echo "<p>✅ ตาราง $table มีอยู่แล้ว</p>";
        } else {
            echo "<p>❌ ไม่พบตาราง $table</p>";
        }
    }
    
    // เพิ่มข้อมูลตัวอย่าง
    echo "<h3>เพิ่มข้อมูลตัวอย่าง</h3>";
    
    // ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
    $count_query = "SELECT COUNT(*) as count FROM products";
    $count_stmt = $db->prepare($count_query);
    $count_stmt->execute();
    $count_result = $count_stmt->fetch();
    
    if ($count_result['count'] == 0) {
        // เพิ่มข้อมูลตัวอย่าง
        $sample_products = [
            ['phone', '081-234-5678', 12000.00, 'AIS', null, 'available', 42, 'ความสำเร็จในการงาน'],
            ['phone', '089-888-8888', 25000.00, 'DTAC', null, 'reserved', 64, 'ความมั่งคั่งทางการเงิน'],
            ['phone', '065-777-7777', 18000.00, 'TRUE', null, 'available', 57, 'ความรักและความสัมพันธ์'],
            ['phone', '080-999-9999', 30000.00, 'AIS', null, 'available', 72, 'ความสุขและความเจริญ'],
            ['license', '8888', 35000.00, null, 'กรุงเทพมหานคร', 'available', 32, 'ความโชคดี'],
            ['license', '4242', 28000.00, null, 'ชลบุรี', 'sold', 12, 'ความเจริญ'],
            ['license', '9999', 45000.00, null, 'เชียงใหม่', 'available', 36, 'ความสุข'],
            ['license', '7777', 38000.00, null, 'ภูเก็ต', 'available', 28, 'ปัญญา']
        ];
        
        $insert_query = "INSERT INTO products (product_type, number, price, network_provider, province, status, numerology_sum, numerology_meaning) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        $insert_stmt = $db->prepare($insert_query);
        
        foreach ($sample_products as $product) {
            $insert_stmt->execute($product);
        }
        
        echo "<p>✅ เพิ่มข้อมูลตัวอย่าง " . count($sample_products) . " รายการสำเร็จ</p>";
    } else {
        echo "<p>ℹ️ มีข้อมูลสินค้าอยู่แล้ว " . $count_result['count'] . " รายการ</p>";
    }
    
    echo "<h3>ลิงก์สำคัญ</h3>";
    echo "<ul>";
    echo "<li><a href='index.php'>หน้าแรก</a></li>";
    echo "<li><a href='admin/index.php'>หน้าจัดการสินค้า</a></li>";
    echo "<li><a href='search.php?type=phone'>ทดสอบค้นหาเบอร์</a></li>";
    echo "<li><a href='search.php?type=numerology&numerology=42'>ทดสอบค้นหาเลขศาสตร์</a></li>";
    echo "</ul>";
    
    echo "<h3>การใช้งาน</h3>";
    echo "<ol>";
    echo "<li>เปิด <a href='index.php'>หน้าแรก</a> เพื่อดูสินค้า</li>";
    echo "<li>ใช้ฟังก์ชันค้นหาเพื่อหาเบอร์หรือทะเบียนที่ต้องการ</li>";
    echo "<li>เข้า <a href='admin/index.php'>หน้าจัดการ</a> เพื่อเพิ่ม/แก้ไข/ลบสินค้า</li>";
    echo "<li>ทดสอบระบบสั่งซื้อโดยกดปุ่ม 'สั่งซื้อ' ที่สินค้า</li>";
    echo "</ol>";
    
} catch (Exception $e) {
    echo "<p>❌ เกิดข้อผิดพลาด: " . $e->getMessage() . "</p>";
    echo "<p>กรุณาตรวจสอบ:</p>";
    echo "<ul>";
    echo "<li>MySQL Server ทำงานอยู่หรือไม่</li>";
    echo "<li>ฐานข้อมูล 'phone_license_db' ถูกสร้างแล้วหรือไม่</li>";
    echo "<li>ไฟล์ database.sql ถูก import หรือไม่</li>";
    echo "<li>การตั้งค่าใน config/database.php ถูกต้องหรือไม่</li>";
    echo "</ul>";
}
?>

<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ตั้งค่าระบบ</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; margin: 20px; }
        h2 { color: #333; }
        h3 { color: #666; }
        p { margin: 5px 0; }
        ul, ol { margin: 10px 0; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
</body>
</html>