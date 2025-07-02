import PyInstaller.__main__
import os

# กำหนดชื่อไฟล์และไอคอน
app_name = "ExcelToJSONConverter"
icon_path = "NONE"  # ถ้ามีไฟล์ .ico สามารถระบุ path ได้

# กำหนดไฟล์ที่ต้องการรวมใน exe
additional_files = [
    ('README.md', '.'),
]

# สร้างคำสั่งสำหรับ PyInstaller
pyinstaller_args = [
    'excel_to_json_converter.py',  # ไฟล์หลัก
    '--name=' + app_name,          # ชื่อไฟล์ exe
    '--onefile',                   # สร้างเป็นไฟล์เดียว
    '--windowed',                  # ไม่แสดง console
    '--clean',                     # ล้าง cache ก่อนสร้าง
    '--noconfirm',                 # ไม่ถามยืนยัน
]

# เพิ่มไฟล์เพิ่มเติม
for src, dst in additional_files:
    pyinstaller_args.extend(['--add-data', f'{src}{os.pathsep}{dst}'])

# เพิ่มไอคอนถ้ามี
if icon_path != "NONE":
    pyinstaller_args.extend(['--icon', icon_path])

# รัน PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print(f"\nสร้างไฟล์ {app_name}.exe เรียบร้อยแล้ว")
print("ไฟล์จะอยู่ในโฟลเดอร์ dist/") 