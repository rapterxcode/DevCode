import PyInstaller.__main__
import os
import sys
import shutil

def create_exe():
    # กำหนดชื่อไฟล์และไอคอน
    app_name = "vm_log_generator"  # เปลี่ยนชื่อเป็น vm_log_generator
    icon_path = "NONE"

    # กำหนดไฟล์ที่ต้องการรวมใน exe
    additional_files = [
        ('README.md', '.'),
    ]

    # สร้างคำสั่งสำหรับ PyInstaller
    pyinstaller_args = [
        'create_vm_log_excel.py',    # เปลี่ยนเป็นไฟล์ create_vm_log_excel.py
        '--name=' + app_name,        # ชื่อไฟล์ exe
        '--onefile',                 # สร้างเป็นไฟล์เดียว
        '--windowed',                # ไม่แสดง console
        '--clean',                   # ล้าง cache ก่อนสร้าง
        '--noconfirm',               # ไม่ถามยืนยัน
    ]

    # เพิ่มไฟล์เพิ่มเติม
    for src, dst in additional_files:
        pyinstaller_args.extend(['--add-data', f'{src}{os.pathsep}{dst}'])

    # เพิ่มไอคอนถ้ามี
    if icon_path != "NONE":
        pyinstaller_args.extend(['--icon', icon_path])

    try:
        # ลบโฟลเดอร์ build และ dist ถ้ามี
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')

        print("เริ่มสร้างไฟล์ executable...")
        print("กำลังสร้างไฟล์ Excel Generator...")

        # รัน PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)

        # ตรวจสอบว่าสร้างไฟล์สำเร็จ
        exe_path = os.path.join('dist', f'{app_name}.exe')
        if os.path.exists(exe_path):
            print(f"\nสร้างไฟล์ {app_name}.exe สำเร็จ!")
            print(f"ไฟล์อยู่ที่: {os.path.abspath(exe_path)}")
            
            # แสดงขนาดไฟล์
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # แปลงเป็น MB
            print(f"ขนาดไฟล์: {file_size:.2f} MB")
            print("\nวิธีการใช้งาน:")
            print("1. ดับเบิลคลิกที่ไฟล์ vm_log_generator.exe")
            print("2. โปรแกรมจะสร้างไฟล์ ubuntu_vm_logs.xlsx ในโฟลเดอร์เดียวกับ exe")
            print("3. ไฟล์ Excel จะมีข้อมูล log ของ VM และสรุปข้อมูล")
        else:
            print("เกิดข้อผิดพลาด: ไม่พบไฟล์ exe ที่สร้าง")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_exe() 