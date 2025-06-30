<?php
require_once '../config/database.php';

// ตรวจสอบการเชื่อมต่อฐานข้อมูล
if (!$db) {
    die("ไม่สามารถเชื่อมต่อฐานข้อมูลได้");
}

if (isset($_GET['id'])) {
    $order_id = (int)$_GET['id'];
    $reason = sanitize($_GET['reason'] ?? 'ไม่ระบุเหตุผล');
    
    try {
        // เริ่ม transaction
        $db->beginTransaction();
        
        // ตรวจสอบว่าคำสั่งซื้อมีอยู่และยังไม่ถูกยกเลิก
        $check_query = "
            SELECT o.*, p.id as product_id, p.status as product_status 
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            WHERE o.id = :id AND o.order_status != 'cancelled'
        ";
        $check_stmt = $db->prepare($check_query);
        $check_stmt->bindParam(':id', $order_id, PDO::PARAM_INT);
        $check_stmt->execute();
        $order = $check_stmt->fetch();
        
        if (!$order) {
            throw new Exception("ไม่พบคำสั่งซื้อหรือคำสั่งซื้อถูกยกเลิกแล้ว");
        }
        
        // อัพเดทสถานะคำสั่งซื้อเป็น cancelled
        $update_order_query = "UPDATE orders SET order_status = 'cancelled', notes = CONCAT(COALESCE(notes, ''), '\n\nเหตุผลการยกเลิก: ', :reason) WHERE id = :id";
        $update_order_stmt = $db->prepare($update_order_query);
        $update_order_stmt->bindParam(':reason', $reason);
        $update_order_stmt->bindParam(':id', $order_id, PDO::PARAM_INT);
        $update_order_stmt->execute();
        
        // ถ้าสินค้าถูก reserved จากคำสั่งซื้อนี้ ให้เปลี่ยนกลับเป็น available
        if ($order['product_status'] == 'reserved') {
            $update_product_query = "UPDATE products SET status = 'available', updated_at = CURRENT_TIMESTAMP WHERE id = :product_id";
            $update_product_stmt = $db->prepare($update_product_query);
            $update_product_stmt->bindParam(':product_id', $order['product_id'], PDO::PARAM_INT);
            $update_product_stmt->execute();
        }
        
        // ยืนยัน transaction
        $db->commit();
        
        header("Location: index.php?success=order_cancelled&order_id=" . $order_id);
        
    } catch (Exception $e) {
        if ($db->inTransaction()) {
            $db->rollBack();
        }
        error_log("Cancel order error: " . $e->getMessage());
        header("Location: index.php?error=cancel_failed&message=" . urlencode($e->getMessage()));
    }
} else {
    header("Location: index.php?error=no_order_id");
}

exit();
?>