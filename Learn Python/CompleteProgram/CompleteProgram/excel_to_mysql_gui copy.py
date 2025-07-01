import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QLineEdit, QFileDialog, QMessageBox, QVBoxLayout, 
                            QHBoxLayout, QWidget, QGroupBox, QFormLayout,
                            QProgressBar, QTextEdit, QScrollArea, QDialog)
from PyQt5.QtCore import Qt, QTimer
import logging
from datetime import datetime
import os

class SummaryDialog(QDialog):
    def __init__(self, summary_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operation Summary")
        self.setGeometry(200, 200, 500, 400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add summary text
        summary_text = QTextEdit()
        summary_text.setReadOnly(True)
        summary_text.setText(summary_data)
        layout.addWidget(summary_text)
        
        # Add Done button
        done_button = QPushButton("Done")
        done_button.clicked.connect(self.accept)
        layout.addWidget(done_button)
        
        self.setLayout(layout)

class ExcelToMySQLApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # กำหนดค่าเริ่มต้นสำหรับการเชื่อมต่อฐานข้อมูล
        self.DB_CONFIG = {
            'host': '192.168.28.181',
            'port': 3306,  # เพิ่ม port สำหรับการเชื่อมต่อ MySQL
            'user': 'root',
            'password': '1qazXSW@',
            'database': 'testerdb'
        }
        
        # กำหนดชื่อไฟล์ Excel ที่จะอ่าน
        self.EXCEL_FILE = 'sample_data.xlsx'
        
        # กำหนด path ของไฟล์ Excel ให้อยู่ในโฟลเดอร์เดียวกับ exe
        if getattr(sys, 'frozen', False):
            # ถ้าเป็น exe file
            self.EXCEL_PATH = os.path.join(os.path.dirname(sys.executable), self.EXCEL_FILE)
        else:
            # ถ้าเป็น python script
            self.EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.EXCEL_FILE)
            
        self.setup_logging()
        self.initUI()
        # Initialize counters for summary
        self.total_records = 0
        self.successful_records = 0
        self.failed_records = 0
        self.skipped_records = 0
        self.salary_skipped_records = 0
        self.empty_cell_records = 0
        self.zero_value_records = 0
        self.updated_records = 0
        
    def setup_logging(self):
        """
        ตั้งค่าระบบ logging
        - สร้างโฟลเดอร์ logs ถ้ายังไม่มี
        - กำหนดชื่อไฟล์ log ด้วย timestamp
        - ตั้งค่าระดับการ log และรูปแบบ
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Create log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'logs/excel_to_mysql_{timestamp}.txt'
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info('Application started')
        
    def initUI(self):
        """
        ตั้งค่า UI ของโปรแกรม
        - กำหนดขนาดหน้าต่าง
        - สร้างส่วนประกอบต่างๆ ของ UI
        - ตั้งค่าการแสดงผล
        """
        self.setWindowTitle('Excel to MySQL Converter')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Database Connection Group - แสดงข้อมูลการเชื่อมต่อฐานข้อมูล
        db_group = QGroupBox("Database Connection")
        db_layout = QFormLayout()
        
        # กำหนดค่าเริ่มต้นสำหรับการเชื่อมต่อฐานข้อมูล
        self.host_input = QLineEdit(self.DB_CONFIG['host'])
        self.user_input = QLineEdit(self.DB_CONFIG['user'])
        self.password_input = QLineEdit(self.DB_CONFIG['password'])
        self.database_input = QLineEdit(self.DB_CONFIG['database'])
        
        # ทำให้ไม่สามารถแก้ไขค่าได้
        self.host_input.setReadOnly(True)
        self.user_input.setReadOnly(True)
        self.password_input.setReadOnly(True)
        self.database_input.setReadOnly(True)
        
        # ตั้งค่าให้แสดงรหัสผ่านเป็น *
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # เพิ่มปุ่มแสดง/ซ่อนรหัสผ่าน
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        show_password_button = QPushButton("Show")
        show_password_button.setFixedWidth(60)
        show_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(show_password_button)
        
        db_layout.addRow('Host:', self.host_input)
        db_layout.addRow('Username:', self.user_input)
        db_layout.addRow('Password:', password_layout)
        db_layout.addRow('Database:', self.database_input)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        # Excel File Selection - แสดงข้อมูลไฟล์ Excel
        excel_group = QGroupBox("Excel File")
        excel_layout = QHBoxLayout()
        
        self.file_path_label = QLabel(self.EXCEL_PATH)
        excel_layout.addWidget(self.file_path_label)
        
        excel_group.setLayout(excel_layout)
        layout.addWidget(excel_group)
        
        # Progress Bar - แสดงความคืบหน้า
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Status Display - แสดงสถานะการทำงาน
        status_group = QGroupBox("Processing Status")
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(200)
        
        status_layout.addWidget(self.status_text)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Convert Button - ปุ่มเริ่มการแปลงข้อมูล
        self.convert_button = QPushButton('Convert to MySQL')
        self.convert_button.clicked.connect(self.convert_data)
        layout.addWidget(self.convert_button)
        
        self.logger.info('UI initialized')
        
    def toggle_password_visibility(self):
        """สลับการแสดง/ซ่อนรหัสผ่าน"""
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.sender().setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.sender().setText("Show")
            
    def show_summary_dialog(self, summary_data):
        """แสดงหน้าต่างสรุปผลการทำงาน"""
        dialog = SummaryDialog(summary_data, self)
        dialog.exec_()
        
    def create_database_connection(self):
        """
        เชื่อมต่อกับฐานข้อมูล MySQL
        - ใช้ค่าที่กำหนดไว้ใน DB_CONFIG
        - ตรวจสอบการเชื่อมต่อ
        - แสดงข้อความสถานะ
        """
        try:
            self.logger.info(f'Attempting to connect to MySQL database: {self.DB_CONFIG["database"]} on {self.DB_CONFIG["host"]}:{self.DB_CONFIG["port"]}')
            connection = mysql.connector.connect(
                host=self.DB_CONFIG['host'],
                port=self.DB_CONFIG['port'],
                user=self.DB_CONFIG['user'],
                password=self.DB_CONFIG['password'],
                database=self.DB_CONFIG['database']
            )
            if connection.is_connected():
                self.logger.info('Successfully connected to MySQL database')
                self.update_status_display('Successfully connected to MySQL database')
                return connection
        except Error as e:
            error_msg = f"Error connecting to MySQL database: {e}"
            self.logger.error(error_msg)
            self.update_status_display(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            return None
            
    def update_status_display(self, message):
        """Update the status display with new message"""
        self.status_text.append(message)
        # Scroll to bottom
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
        
    def update_progress(self, current, total):
        """Update progress bar and status"""
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        
        status_msg = f"""
        Progress: {percentage}%
        Processed: {current}/{total} records
        Success: {self.successful_records}
        Failed: {self.failed_records}
        Skipped (Salary): {self.salary_skipped_records}
        Empty Cells: {self.empty_cell_records}
        Zero Values: {self.zero_value_records}
        """
        self.update_status_display(status_msg)
        
    def validate_salary(self, salary):
        """Validate salary value"""
        try:
            # Convert to float and check if it's greater than 50000
            salary_value = float(salary)
            return salary_value <= 50000
        except (ValueError, TypeError):
            return False
            
    def process_cell_value(self, value, field_name):
        """Process cell value and handle empty/zero values"""
        if pd.isna(value) or value == '':
            self.logger.info(f'Empty cell found in {field_name}, using default value')
            self.empty_cell_records += 1
            return None
        elif value == 0:
            self.logger.info(f'Zero value found in {field_name}')
            self.zero_value_records += 1
            return 0
        return value
        
    def insert_data(self, connection, data):
        """
        แทรกหรืออัพเดทข้อมูลในตาราง employees
        - ตรวจสอบข้อมูลแต่ละแถว
        - แทรกข้อมูลใหม่หรืออัพเดทข้อมูลที่มีอยู่
        - บันทึก log การทำงาน
        """
        try:
            cursor = connection.cursor()
            
            # คำสั่ง SQL สำหรับแทรกข้อมูลใหม่
            insert_query = """
            INSERT INTO employees (name, age, city, salary)
            VALUES (%s, %s, %s, %s)
            """
            
            # คำสั่ง SQL สำหรับอัพเดทข้อมูล
            update_query = """
            UPDATE employees 
            SET age = %s,
                city = %s,
                salary = %s
            WHERE name = %s
            """
            
            # เพิ่ม counter สำหรับการอัพเดท
            self.total_records = len(data)
            self.successful_records = 0
            self.failed_records = 0
            self.skipped_records = 0
            self.salary_skipped_records = 0
            self.empty_cell_records = 0
            self.zero_value_records = 0
            self.updated_records = 0  # เพิ่ม counter สำหรับการอัพเดท
            
            self.update_status_display(f'Starting to process {self.total_records} records')
            self.logger.info(f'Starting to insert/update {self.total_records} records')
            
            for index, row in data.iterrows():
                try:
                    # Process each cell value
                    name = self.process_cell_value(row['Name'], 'Name')
                    age = self.process_cell_value(row['Age'], 'Age')
                    city = self.process_cell_value(row['City'], 'City')
                    salary = self.process_cell_value(row['Salary'], 'Salary')
                    
                    # Check salary condition
                    if salary is not None and not self.validate_salary(salary):
                        self.logger.warning(f'Skipping row {index + 1}: Salary {salary} exceeds 50000')
                        self.salary_skipped_records += 1
                        continue
                    
                    # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
                    check_query = "SELECT COUNT(*) FROM employees WHERE name = %s"
                    cursor.execute(check_query, (name,))
                    exists = cursor.fetchone()[0] > 0
                    
                    # Log the values being processed
                    row_msg = f"""
                    Processing row {index + 1}/{self.total_records}:
                    Name: {name}
                    Age: {age}
                    City: {city}
                    Salary: {salary}
                    Action: {'Update' if exists else 'Insert'}
                    """
                    self.update_status_display(row_msg)
                    self.logger.info(row_msg)
                    
                    if exists:
                        # อัพเดทข้อมูลที่มีอยู่
                        update_values = (age, city, salary, name)
                        cursor.execute(update_query, update_values)
                        self.updated_records += 1
                        self.logger.info(f'Successfully updated row {index + 1}')
                    else:
                        # แทรกข้อมูลใหม่
                        insert_values = (name, age, city, salary)
                        cursor.execute(insert_query, insert_values)
                        self.successful_records += 1
                        self.logger.info(f'Successfully inserted row {index + 1}')
                    
                except Error as e:
                    self.failed_records += 1
                    error_msg = f'Failed to process row {index + 1}: {values} - Error: {e}'
                    self.logger.error(error_msg)
                    self.update_status_display(error_msg)
                
                # Update progress
                self.update_progress(index + 1, self.total_records)
                QApplication.processEvents()
            
            connection.commit()
            
            # Log summary after completion
            self.log_summary()
            
            success_msg = f"""
            Data processing completed:
            - Successfully Inserted: {self.successful_records}
            - Successfully Updated: {self.updated_records}
            - Failed Records: {self.failed_records}
            - Skipped (Salary > 50000): {self.salary_skipped_records}
            - Records with Empty Cells: {self.empty_cell_records}
            - Records with Zero Values: {self.zero_value_records}
            """
            self.update_status_display(success_msg)
            self.logger.info(success_msg)
            
        except Error as e:
            error_msg = f"Error during data processing: {e}"
            self.logger.error(error_msg)
            self.update_status_display(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            
    def log_summary(self):
        """Log the summary of all operations"""
        self.logger.info('=' * 50)
        self.logger.info('OPERATION SUMMARY')
        self.logger.info('=' * 50)
        self.logger.info(f'Total Records Processed: {self.total_records}')
        self.logger.info(f'Successfully Inserted: {self.successful_records}')
        self.logger.info(f'Successfully Updated: {self.updated_records}')
        self.logger.info(f'Failed Records: {self.failed_records}')
        self.logger.info(f'Skipped Records (Salary > 50000): {self.salary_skipped_records}')
        self.logger.info(f'Records with Empty Cells: {self.empty_cell_records}')
        self.logger.info(f'Records with Zero Values: {self.zero_value_records}')
        self.logger.info('=' * 50)
        
        # Calculate success rate
        if self.total_records > 0:
            success_rate = ((self.successful_records + self.updated_records) / self.total_records) * 100
            self.logger.info(f'Success Rate: {success_rate:.2f}%')
        self.logger.info('=' * 50)
        
    def convert_data(self):
        """
        เริ่มกระบวนการแปลงข้อมูล
        - อ่านไฟล์ Excel
        - เชื่อมต่อฐานข้อมูล
        - แทรกหรืออัพเดทข้อมูล
        """
        try:
            # ตรวจสอบว่าไฟล์ Excel มีอยู่จริง
            if not os.path.exists(self.EXCEL_PATH):
                error_msg = f"ไม่พบไฟล์ Excel: {self.EXCEL_PATH}"
                self.logger.error(error_msg)
                self.update_status_display(error_msg)
                QMessageBox.critical(self, "Error", error_msg)
                return
                
            # Reset progress
            self.progress_bar.setValue(0)
            self.status_text.clear()
            
            # Reset counters
            self.total_records = 0
            self.successful_records = 0
            self.failed_records = 0
            self.skipped_records = 0
            self.salary_skipped_records = 0
            self.empty_cell_records = 0
            self.zero_value_records = 0
            self.updated_records = 0
            
            # Read Excel file
            self.update_status_display(f'Reading Excel file: {self.EXCEL_PATH}')
            self.logger.info(f'Reading Excel file: {self.EXCEL_PATH}')
            df = pd.read_excel(self.EXCEL_PATH)
            self.update_status_display(f'Successfully read {len(df)} rows from Excel file')
            self.logger.info(f'Successfully read {len(df)} rows from Excel file')
            
            # Connect to MySQL
            connection = self.create_database_connection()
            if connection is None:
                return
                
            try:
                # Insert or update data
                self.insert_data(connection, df)
                
                # Show summary in message box
                summary_msg = f"""
                Operation Summary:
                Total Records: {self.total_records}
                Successfully Inserted: {self.successful_records}
                Successfully Updated: {self.updated_records}
                Failed Records: {self.failed_records}
                Skipped (Salary > 50000): {self.salary_skipped_records}
                Records with Empty Cells: {self.empty_cell_records}
                Records with Zero Values: {self.zero_value_records}
                """
                self.logger.info('Data conversion completed successfully!')
                self.show_summary_dialog(summary_msg)
                
            finally:
                if connection.is_connected():
                    connection.close()
                    self.logger.info('MySQL connection closed')
                    self.update_status_display('MySQL connection closed')
                    
        except Exception as e:
            error_msg = f"Error processing data: {e}"
            self.logger.error(error_msg)
            self.update_status_display(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

def main():
    app = QApplication(sys.argv)
    ex = ExcelToMySQLApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 