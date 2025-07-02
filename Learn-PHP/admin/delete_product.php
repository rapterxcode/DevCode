<?php
require_once '../config/database.php';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

if (isset($_GET['id'])) {
    $product_id = (int)$_GET['id'];
    
    try {
        // ตรวจสอบว่ามีสินค้าอยู่หรือไม่
        $check_query = "SELECT * FROM products WHERE id = :id";
        $check_stmt = $db->prepare($check_query);
        $check_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
        $check_stmt->execute();
        $product = $check_stmt->fetch();
        
        if (!$product) {
            header("Location: index.php?error=product_not_found");
            exit();
        }
        
        // ตรวจสอบว่ามีคำสั่งซื้อที่เกี่ยวข้องหรือไม่
        $orders_check = "SELECT COUNT(*) as order_count FROM orders WHERE product_id = :id";
        $orders_stmt = $db->prepare($orders_check);
        $orders_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
        $orders_stmt->execute();
        $orders_result = $orders_stmt->fetch();
        
        if ($orders_result['order_count'] > 0) {
            // ถ้ามีคำสั่งซื้อ ให้เปลี่ยนสถานะเป็น deleted แทนการลบ
            $update_query = "UPDATE products SET status = 'deleted', updated_at = CURRENT_TIMESTAMP WHERE id = :id";
            $update_stmt = $db->prepare($update_query);
            $update_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
            $update_stmt->execute();
            
            header("Location: index.php?success=product_deactivated");
        } else {
            // ถ้าไม่มีคำสั่งซื้อ ลบได้เลย
            $delete_query = "DELETE FROM products WHERE id = :id";
            $delete_stmt = $db->prepare($delete_query);
            $delete_stmt->bindParam(':id', $product_id, PDO::PARAM_INT);
            $delete_stmt->execute();
            
            header("Location: index.php?success=product_deleted");
        }
        
    } catch (PDOException $e) {
        error_log("Delete product error: " . $e->getMessage());
        header("Location: index.php?error=delete_failed");
    }
} else {
    header("Location: index.php?error=no_id");
}

exit();
?>