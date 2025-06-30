<?php
// การตั้งค่าฐานข้อมูล
define('DB_HOST', 'localhost');
define('DB_NAME', 'phone_license_db');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_CHARSET', 'utf8mb4');

// ตั้งค่าสำหรับการแสดงข้อผิดพลาด
error_reporting(E_ALL);
ini_set('display_errors', 1);

class Database {
    private $host = DB_HOST;
    private $db_name = DB_NAME;
    private $username = DB_USER;
    private $password = DB_PASS;
    private $charset = DB_CHARSET;
    public $conn;

    public function getConnection() {
        $this->conn = null;
        
        try {
            $dsn = "mysql:host=" . $this->host . ";dbname=" . $this->db_name . ";charset=" . $this->charset;
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4"
            ];
            
            $this->conn = new PDO($dsn, $this->username, $this->password, $options);
        } catch(PDOException $exception) {
            echo "Connection error: " . $exception->getMessage();
        }
        
        return $this->conn;
    }
}

// สร้าง instance ของ database
$database = new Database();
$db = $database->getConnection();

// ฟังก์ชันสำหรับตรวจสอบการเชื่อมต่อ
function testConnection() {
    global $db;
    try {
        $query = "SELECT 1";
        $stmt = $db->prepare($query);
        $stmt->execute();
        return true;
    } catch(PDOException $e) {
        return false;
    }
}

// ฟังก์ชันสำหรับป้องกัน SQL Injection
function sanitize($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// ฟังก์ชันสำหรับแสดงข้อผิดพลาด
function showError($message) {
    echo "<div class='alert alert-danger alert-dismissible fade show' role='alert'>";
    echo "<strong>เกิดข้อผิดพลาด!</strong> " . $message;
    echo "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>";
    echo "<span aria-hidden='true'>&times;</span>";
    echo "</button>";
    echo "</div>";
}

// ฟังก์ชันสำหรับแสดงข้อความสำเร็จ
function showSuccess($message) {
    echo "<div class='alert alert-success alert-dismissible fade show' role='alert'>";
    echo "<strong>สำเร็จ!</strong> " . $message;
    echo "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>";
    echo "<span aria-hidden='true'>&times;</span>";
    echo "</button>";
    echo "</div>";
}

// ฟังก์ชันสำหรับคำนวณเลขศาสตร์
function calculateNumerology($number) {
    $digits = preg_replace('/[^0-9]/', '', $number);
    $sum = 0;
    
    for ($i = 0; $i < strlen($digits); $i++) {
        $sum += (int)$digits[$i];
    }
    
    // ลดผลรวมจนกว่าจะเหลือตัวเลขหลักเดียวหรือเลขมงคล
    while ($sum > 9 && !in_array($sum, [11, 22, 33])) {
        $temp = 0;
        $sumStr = (string)$sum;
        for ($i = 0; $i < strlen($sumStr); $i++) {
            $temp += (int)$sumStr[$i];
        }
        $sum = $temp;
    }
    
    return $sum;
}

// ฟังก์ชันสำหรับหาความหมายเลขศาสตร์
function getNumerologyMeaning($sum) {
    $meanings = [
        1 => "ความเป็นผู้นำ",
        2 => "ความร่วมมือ",
        3 => "ความคิดสร้างสรรค์",
        4 => "ความมั่นคง",
        5 => "ความเสรี",
        6 => "ความรับผิดชอบ",
        7 => "ปัญญา",
        8 => "ความสำเร็จทางวัตถุ",
        9 => "ความเมตตา",
        11 => "ความเป็นผู้นำทางจิตวิญญาณ",
        22 => "ผู้สร้างฝัน",
        33 => "ความรักและการเสียสละ",
        42 => "ความสำเร็จในการงาน",
        57 => "ความรักและความสัมพันธ์",
        64 => "ความมั่งคั่งทางการเงิน"
    ];
    
    return isset($meanings[$sum]) ? $meanings[$sum] : "ความหมายพิเศษ";
}

// ฟังก์ชันสำหรับจัดรูปแบบราคา
function formatPrice($price) {
    return number_format($price, 0) . " บาท";
}

// ฟังก์ชันสำหรับจัดรูปแบบวันที่
function formatDate($date) {
    $thai_months = [
        1 => "มกราคม", 2 => "กุมภาพันธ์", 3 => "มีนาคม", 4 => "เมษายน",
        5 => "พฤษภาคม", 6 => "มิถุนายน", 7 => "กรกฎาคม", 8 => "สิงหาคม",
        9 => "กันยายน", 10 => "ตุลาคม", 11 => "พฤศจิกายน", 12 => "ธันวาคม"
    ];
    
    $timestamp = strtotime($date);
    $day = date('j', $timestamp);
    $month = $thai_months[(int)date('n', $timestamp)];
    $year = date('Y', $timestamp) + 543;
    $time = date('H:i', $timestamp);
    
    return "$day $month $year เวลา $time น.";
}

// ตั้งค่า timezone
date_default_timezone_set('Asia/Bangkok');
?>