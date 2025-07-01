import os
import sys
import subprocess
from datetime import datetime

def create_exe():
    """
    สร้างไฟล์ executable สำหรับ Windows
    """
    print("เริ่มสร้างไฟล์ executable...")
    
    # กำหนดชื่อไฟล์และโฟลเดอร์
    exe_name = "ExcelToMySQL"
    
    # สร้างโฟลเดอร์ dist ถ้ายังไม่มี
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # รันคำสั่ง PyInstaller
    try:
        # สร้าง executable ด้วย PyInstaller
        subprocess.run([
            "pyinstaller",
            "--name", exe_name,
            "--onefile",
            "--windowed",
            "--add-data", f"sample_data.xlsx{os.pathsep}.",
            "--clean",
            "--noconfirm",
            "excel_to_mysql_gui.py"
        ], check=True)
        
        print("\nสร้างไฟล์ executable สำเร็จ!")
        print(f"ไฟล์ executable อยู่ที่: {os.path.abspath(os.path.join('dist', f'{exe_name}.exe'))}")
        
        # สร้างไฟล์ README.txt ในโฟลเดอร์ dist
        readme_content = f"""Excel to MySQL Converter
สร้างเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

วิธีการใช้งาน:
1. วางไฟล์ Excel ที่ต้องการแปลงข้อมูลในโฟลเดอร์เดียวกับโปรแกรม
2. ตั้งชื่อไฟล์ Excel เป็น 'sample_data.xlsx'
3. Double-click ที่ไฟล์ {exe_name}.exe เพื่อรันโปรแกรม

หมายเหตุ:
- โปรแกรมจะสร้างโฟลเดอร์ 'logs' สำหรับเก็บไฟล์ log
- ตรวจสอบการเชื่อมต่อฐานข้อมูลก่อนใช้งาน
- ข้อมูลการเชื่อมต่อฐานข้อมูล:
  * Host: 192.168.28.181
  * Port: 3306
  * User: root
  * Password: 1qazXSW@
  * Database: testerdb

การแก้ไขปัญหา:
1. ถ้าโปรแกรมไม่รัน: ตรวจสอบว่าไฟล์ Excel อยู่ในโฟลเดอร์เดียวกัน
2. ถ้าเชื่อมต่อฐานข้อมูลไม่ได้: ตรวจสอบการเชื่อมต่อเครือข่าย
3. ถ้ามีปัญหา: ตรวจสอบไฟล์ log ในโฟลเดอร์ 'logs'
"""
        
        with open(os.path.join("dist", "README.txt"), "w", encoding="utf-8") as f:
            f.write(readme_content)
            
        print("\nสร้างไฟล์ README.txt ในโฟลเดอร์ dist เรียบร้อยแล้ว")
        
    except subprocess.CalledProcessError as e:
        print(f"\nเกิดข้อผิดพลาดในการสร้างไฟล์ executable: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nเกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_exe() 