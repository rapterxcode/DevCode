<?php
require_once '../config/database.php';

header('Content-Type: application/json; charset=UTF-8');

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    echo json_encode(['error' => 'ไม่สามารถเชื่อมต่อฐานข้อมูลได้']);
    exit();
}

try {
    // ดึงข้อมูลสินค้าทั้งหมด
    $query = "SELECT id, number FROM products";
    $stmt = $db->prepare($query);
    $stmt->execute();
    $products = $stmt->fetchAll();
    
    $updated_count = 0;
    
    // คำนวณเลขศาสตร์ใหม่สำหรับแต่ละสินค้า
    foreach ($products as $product) {
        $numerology_sum = calculateNumerology($product['number']);
        $numerology_meaning = getNumerologyMeaning($numerology_sum);
        
        // อัพเดทข้อมูลในฐานข้อมูล
        $update_query = "UPDATE products SET 
                        numerology_sum = :numerology_sum, 
                        numerology_meaning = :numerology_meaning,
                        updated_at = CURRENT_TIMESTAMP
                        WHERE id = :id";
        
        $update_stmt = $db->prepare($update_query);
        $update_stmt->bindParam(':numerology_sum', $numerology_sum);
        $update_stmt->bindParam(':numerology_meaning', $numerology_meaning);
        $update_stmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
        
        if ($update_stmt->execute()) {
            $updated_count++;
        }
    }
    
    echo json_encode([
        'success' => true,
        'message' => "คำนวณเลขศาสตร์ใหม่สำเร็จ อัพเดท $updated_count รายการ",
        'updated_count' => $updated_count,
        'total_count' => count($products)
    ]);
    
} catch (PDOException $e) {
    echo json_encode([
        'error' => 'เกิดข้อผิดพลาดในการคำนวณ: ' . $e->getMessage()
    ]);
}
?>