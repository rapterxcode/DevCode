-- สร้างฐานข้อมูล
CREATE DATABASE IF NOT EXISTS phone_license_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE phone_license_db;

-- ตารางสำหรับเก็บข้อมูลสินค้า (เบอร์โทรศัพท์และทะเบียนรถ)
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_type ENUM('phone', 'license') NOT NULL,
    number VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    network_provider VARCHAR(10) DEFAULT NULL, -- สำหรับเบอร์โทรศัพท์ (AIS, DTAC, TRUE)
    province VARCHAR(50) DEFAULT NULL, -- สำหรับทะเบียนรถ
    status ENUM('available', 'reserved', 'sold') DEFAULT 'available',
    numerology_sum INT NOT NULL,
    numerology_meaning VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_number (number, product_type)
);

-- ตารางสำหรับเก็บข้อมูลการสั่งซื้อ
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_email VARCHAR(100) DEFAULT NULL,
    order_status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT DEFAULT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ตารางสำหรับเก็บข้อความติดต่อ
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) DEFAULT NULL,
    message TEXT NOT NULL,
    status ENUM('new', 'replied', 'closed') DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ตารางสำหรับผู้ดูแลระบบ
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- เพิ่มข้อมูลตัวอย่าง
INSERT INTO products (product_type, number, price, network_provider, status, numerology_sum, numerology_meaning) VALUES
('phone', '081-234-5678', 12000.00, 'AIS', 'available', 42, 'ความสำเร็จในการงาน'),
('phone', '089-888-8888', 25000.00, 'DTAC', 'reserved', 64, 'ความมั่งคั่งทางการเงิน'),
('phone', '065-777-7777', 18000.00, 'TRUE', 'available', 57, 'ความรักและความสัมพันธ์'),
('phone', '080-999-9999', 30000.00, 'AIS', 'available', 72, 'ความสุขและความเจริญ'),
('phone', '084-555-5555', 15000.00, 'DTAC', 'sold', 45, 'ความแข็งแกร่ง'),
('phone', '066-123-4567', 8000.00, 'TRUE', 'available', 38, 'ความก้าวหน้า');

INSERT INTO products (product_type, number, price, province, status, numerology_sum, numerology_meaning) VALUES
('license', '8888', 35000.00, 'กรุงเทพมหานคร', 'available', 32, 'ความโชคดี'),
('license', '4242', 28000.00, 'ชลบุรี', 'sold', 12, 'ความเจริญ'),
('license', '9999', 45000.00, 'เชียงใหม่', 'available', 36, 'ความสุข'),
('license', '1111', 20000.00, 'กรุงเทพมหานคร', 'reserved', 4, 'ความมั่นคง'),
('license', '7777', 38000.00, 'ภูเก็ต', 'available', 28, 'ปัญญา'),
('license', '6666', 32000.00, 'ขอนแก่น', 'available', 24, 'ความรับผิดชอบ');

-- เพิ่มผู้ดูแลระบบ (รหัสผ่าน: admin123)
INSERT INTO admins (username, password, email, full_name) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin@phonebeauty.com', 'ผู้ดูแลระบบ');

-- สร้าง Index เพื่อเพิ่มประสิทธิภาพการค้นหา
CREATE INDEX idx_product_type ON products(product_type);
CREATE INDEX idx_network_provider ON products(network_provider);
CREATE INDEX idx_province ON products(province);
CREATE INDEX idx_status ON products(status);
CREATE INDEX idx_numerology_sum ON products(numerology_sum);
CREATE INDEX idx_price ON products(price);

-- สร้าง View สำหรับสถิติ
CREATE VIEW product_stats AS
SELECT 
    product_type,
    COUNT(*) as total_products,
    COUNT(CASE WHEN status = 'available' THEN 1 END) as available_count,
    COUNT(CASE WHEN status = 'reserved' THEN 1 END) as reserved_count,
    COUNT(CASE WHEN status = 'sold' THEN 1 END) as sold_count,
    AVG(price) as average_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM products
GROUP BY product_type;

-- สร้าง Function สำหรับคำนวณเลขศาสตร์
DELIMITER //
CREATE FUNCTION calculate_numerology(input_number VARCHAR(20)) 
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE sum_result INT DEFAULT 0;
    DECLARE i INT DEFAULT 1;
    DECLARE digit CHAR(1);
    DECLARE clean_number VARCHAR(20);
    
    -- ลบตัวอักษรที่ไม่ใช่ตัวเลขออก
    SET clean_number = REGEXP_REPLACE(input_number, '[^0-9]', '');
    
    -- คำนวณผลรวมของแต่ละหลัก
    WHILE i <= LENGTH(clean_number) DO
        SET digit = SUBSTRING(clean_number, i, 1);
        SET sum_result = sum_result + CAST(digit AS UNSIGNED);
        SET i = i + 1;
    END WHILE;
    
    -- ลดผลรวมจนกว่าจะเหลือตัวเลขหลักเดียวหรือเลขมงคล (11, 22, 33)
    WHILE sum_result > 9 AND sum_result NOT IN (11, 22, 33) DO
        SET i = 1;
        SET input_number = CAST(sum_result AS CHAR);
        SET sum_result = 0;
        
        WHILE i <= LENGTH(input_number) DO
            SET digit = SUBSTRING(input_number, i, 1);
            SET sum_result = sum_result + CAST(digit AS UNSIGNED);
            SET i = i + 1;
        END WHILE;
    END WHILE;
    
    RETURN sum_result;
END//
DELIMITER ;

-- สร้าง Stored Procedure สำหรับการค้นหาสินค้า
DELIMITER //
CREATE PROCEDURE search_products(
    IN search_type VARCHAR(20),
    IN search_value VARCHAR(100),
    IN product_filter VARCHAR(20),
    IN status_filter VARCHAR(20)
)
BEGIN
    DECLARE sql_query TEXT;
    
    SET sql_query = 'SELECT * FROM products WHERE 1=1';
    
    -- กรองตามประเภทสินค้า
    IF product_filter IS NOT NULL AND product_filter != '' THEN
        SET sql_query = CONCAT(sql_query, ' AND product_type = "', product_filter, '"');
    END IF;
    
    -- กรองตามสถานะ
    IF status_filter IS NOT NULL AND status_filter != '' THEN
        SET sql_query = CONCAT(sql_query, ' AND status = "', status_filter, '"');
    END IF;
    
    -- ค้นหาตามเงื่อนไข
    CASE search_type
        WHEN 'number' THEN
            SET sql_query = CONCAT(sql_query, ' AND number LIKE "%', search_value, '%"');
        WHEN 'numerology' THEN
            SET sql_query = CONCAT(sql_query, ' AND numerology_sum = ', search_value);
        WHEN 'network' THEN
            SET sql_query = CONCAT(sql_query, ' AND network_provider = "', search_value, '"');
        WHEN 'province' THEN
            SET sql_query = CONCAT(sql_query, ' AND province LIKE "%', search_value, '%"');
        ELSE
            SET sql_query = sql_query;
    END CASE;
    
    SET sql_query = CONCAT(sql_query, ' ORDER BY created_at DESC');
    
    SET @sql = sql_query;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END//
DELIMITER ;