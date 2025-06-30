<?php
require_once 'config/database.php';

header('Content-Type: application/json');

if (isset($_GET['id'])) {
    $product_id = (int)$_GET['id'];
    
    try {
        $query = "SELECT * FROM products WHERE id = :id";
        $stmt = $db->prepare($query);
        $stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
        $stmt->execute();
        
        $product = $stmt->fetch();
        
        if ($product) {
            echo json_encode($product);
        } else {
            echo json_encode(['error' => 'ไม่พบสินค้า']);
        }
    } catch (PDOException $e) {
        echo json_encode(['error' => 'เกิดข้อผิดพลาดในการค้นหาข้อมูล']);
    }
} else {
    echo json_encode(['error' => 'ไม่ระบุรหัสสินค้า']);
}
?>