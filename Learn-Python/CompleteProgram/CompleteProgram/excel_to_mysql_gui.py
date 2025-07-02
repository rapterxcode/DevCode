import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QLineEdit, QFileDialog, QMessageBox, QVBoxLayout, 
                            QHBoxLayout, QWidget, QGroupBox, QFormLayout,
                            QProgressBar, QTextEdit, QScrollArea, QDialog,
                            QCheckBox)
from PyQt5.QtCore import Qt, QTimer
import logging
from datetime import datetime
import os
import json

class SummaryDialog(QDialog):
    """
    Dialog class for displaying operation summary
    Shows the results of the data processing operation
    """
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
        done_button.clicked.connect(self.on_done_clicked)
        layout.addWidget(done_button)
        
        self.setLayout(layout)
        
    def on_done_clicked(self):
        """Handle Done button click - set progress to 100% and exit application"""
        if self.parent():
            self.parent().progress_bar.setValue(100)
        self.accept()
        QApplication.quit()

class ExcelToMySQLApp(QMainWindow):
    """
    Main application class for Excel to MySQL conversion
    Handles UI, database operations, and data processing
    """
    def __init__(self):
        super().__init__()
        self.initialize_defaults()
        self.setup_logging()
        self.initUI()
        self.initialize_counters()
        
    def initialize_defaults(self):
        """Initialize default values and configurations"""
        # Default database configuration
        self.DB_CONFIG = {
            'host': '192.168.28.181',
            'port': 3306,
            'user': 'root',
            'password': '1qazXSW@',
            'database': 'testerdb'
        }
        
        # Load saved database configuration if exists
        self.load_db_config()
        
        # Set Excel file path
        self.EXCEL_FILE = 'sample_data.xlsx'
        if getattr(sys, 'frozen', False):
            self.EXCEL_PATH = os.path.join(os.path.dirname(sys.executable), self.EXCEL_FILE)
        else:
            self.EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.EXCEL_FILE)
            
    def initialize_counters(self):
        """Initialize all counters for tracking operation statistics"""
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
        Configure logging system
        - Creates logs directory if not exists
        - Sets up log file with timestamp
        - Configures logging format and handlers
        """
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'logs/excel_to_mysql_{timestamp}.txt'
        
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

    def load_db_config(self):
        """Load saved database configuration from file"""
        try:
            if os.path.exists('db_config.json'):
                with open('db_config.json', 'r') as f:
                    saved_config = json.load(f)
                    self.DB_CONFIG.update(saved_config)
        except Exception as e:
            self.logger.error(f"Error loading database configuration: {e}")

    def save_db_config(self):
        """Save database configuration to file"""
        try:
            with open('db_config.json', 'w') as f:
                json.dump(self.DB_CONFIG, f)
        except Exception as e:
            self.logger.error(f"Error saving database configuration: {e}")

    def initUI(self):
        """
        Initialize and setup the user interface
        Creates all UI components and layouts
        """
        self.setWindowTitle('Excel to MySQL Converter')
        self.setGeometry(100, 100, 800, 600)
        
        # Create main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add UI components
        layout.addWidget(self.create_database_group())
        layout.addWidget(self.create_excel_group())
        layout.addWidget(self.create_progress_group())
        layout.addWidget(self.create_status_group())
        layout.addWidget(self.create_convert_button())
        
        self.logger.info('UI initialized')

    def create_database_group(self):
        """Create database connection group with all its components"""
        db_group = QGroupBox("Database Connection")
        db_layout = QFormLayout()
        
        # Create input fields
        self.host_input = QLineEdit(self.DB_CONFIG['host'])
        self.port_input = QLineEdit(str(self.DB_CONFIG['port']))
        self.user_input = QLineEdit(self.DB_CONFIG['user'])
        self.password_input = QLineEdit(self.DB_CONFIG['password'])
        self.database_input = QLineEdit(self.DB_CONFIG['database'])
        
        # Setup password field
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        show_password_button = QPushButton("Show")
        show_password_button.setFixedWidth(60)
        show_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(show_password_button)
        
        # Add test connection button
        test_conn_button = QPushButton("Test Connection")
        test_conn_button.clicked.connect(self.test_connection)

        # Add remember connection checkbox
        self.remember_connection = QCheckBox("Remember Database Connection")
        self.remember_connection.setChecked(True)
        
        # Add all components to layout
        db_layout.addRow('Host:', self.host_input)
        db_layout.addRow('Port:', self.port_input)
        db_layout.addRow('Username:', self.user_input)
        db_layout.addRow('Password:', password_layout)
        db_layout.addRow('Database:', self.database_input)
        db_layout.addRow('', test_conn_button)
        db_layout.addRow('', self.remember_connection)
        
        db_group.setLayout(db_layout)
        return db_group

    def create_excel_group(self):
        """Create Excel file selection group"""
        excel_group = QGroupBox("Excel File")
        excel_layout = QHBoxLayout()
        
        self.file_path_label = QLabel(self.EXCEL_PATH)
        excel_layout.addWidget(self.file_path_label)
        
        excel_group.setLayout(excel_layout)
        return excel_group

    def create_progress_group(self):
        """Create progress bar group"""
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        return progress_group

    def create_status_group(self):
        """Create status display group"""
        status_group = QGroupBox("Processing Status")
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(200)
        
        status_layout.addWidget(self.status_text)
        status_group.setLayout(status_layout)
        return status_group

    def create_convert_button(self):
        """Create convert button"""
        convert_button = QPushButton('Convert to MySQL')
        convert_button.clicked.connect(self.convert_data)
        return convert_button

    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.sender().setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.sender().setText("Show")

    def update_status_display(self, message):
        """
        Update status display and log message
        Args:
            message (str): Message to display and log
        """
        formatted_message = message.strip()
        self.status_text.append(formatted_message)
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
        self.logger.info(formatted_message)

    def update_progress(self, current, total):
        """
        Update progress bar and status display
        Args:
            current (int): Current progress
            total (int): Total items to process
        """
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        
        status_msg = f"""Progress: {percentage}%
Processed: {current}/{total} records
Success: {self.successful_records}
Failed: {self.failed_records}
Skipped (Salary): {self.salary_skipped_records}
Empty Cells: {self.empty_cell_records}
Zero Values: {self.zero_value_records}"""
        self.update_status_display(status_msg)

    def validate_salary(self, salary):
        """
        Validate salary value
        Args:
            salary: Salary value to validate
        Returns:
            bool: True if salary is valid (<= 50000), False otherwise
        """
        try:
            salary_value = float(salary)
            return salary_value <= 50000
        except (ValueError, TypeError):
            return False

    def process_cell_value(self, value, field_name):
        """
        Process cell value and handle empty/zero values
        Args:
            value: Cell value to process
            field_name (str): Name of the field being processed
        Returns:
            Processed value or None if empty
        """
        if pd.isna(value) or value == '':
            self.logger.info(f'Empty cell found in {field_name}, using default value')
            self.empty_cell_records += 1
            return None
        elif value == 0:
            self.logger.info(f'Zero value found in {field_name}')
            self.zero_value_records += 1
            return 0
        return value

    def create_database_connection(self):
        """
        Create database connection
        Returns:
            Connection object or None if connection fails
        """
        try:
            self.logger.info(f'Attempting to connect to MySQL database: {self.DB_CONFIG["database"]} on {self.DB_CONFIG["host"]}:{self.DB_CONFIG["port"]}')
            connection = mysql.connector.connect(**self.DB_CONFIG)
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

    def test_connection(self):
        """Test database connection with current settings"""
        try:
            self.update_db_config()
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Database connection successful!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database connection failed:\n{str(e)}")

    def update_db_config(self):
        """Update database configuration from UI inputs"""
        self.DB_CONFIG = {
            'host': self.host_input.text(),
            'port': int(self.port_input.text()),
            'user': self.user_input.text(),
            'password': self.password_input.text(),
            'database': self.database_input.text()
        }
        
        if self.remember_connection.isChecked():
            self.save_db_config()
        
        self.logger.info("Database configuration updated")
        self.logger.debug(f"New config: {self.DB_CONFIG}")

    def insert_data(self, connection, data):
        """
        Insert or update data in the database
        Args:
            connection: Database connection object
            data: DataFrame containing data to process
        """
        try:
            cursor = connection.cursor()
            
            # SQL queries
            insert_query = """
            INSERT INTO employees (name, age, city, salary)
            VALUES (%s, %s, %s, %s)
            """
            
            update_query = """
            UPDATE employees 
            SET age = %s,
                city = %s,
                salary = %s
            WHERE name = %s
            """
            
            self.initialize_counters()
            self.update_status_display(f'Starting to process {len(data)} records')
            
            for index, row in data.iterrows():
                try:
                    # Process row data
                    name = self.process_cell_value(row['Name'], 'Name')
                    age = self.process_cell_value(row['Age'], 'Age')
                    city = self.process_cell_value(row['City'], 'City')
                    salary = self.process_cell_value(row['Salary'], 'Salary')
                    
                    # Validate salary
                    if salary is not None and not self.validate_salary(salary):
                        self.logger.warning(f'Skipping row {index + 1}: Salary {salary} exceeds 50000')
                        self.salary_skipped_records += 1
                        continue
                    
                    # Check if record exists
                    check_query = "SELECT COUNT(*) FROM employees WHERE name = %s"
                    cursor.execute(check_query, (name,))
                    exists = cursor.fetchone()[0] > 0
                    
                    # Log processing
                    row_msg = f"""Processing row {index + 1}/{len(data)}:
Name: {name}
Age: {age}
City: {city}
Salary: {salary}
Action: {'Update' if exists else 'Insert'}"""
                    self.update_status_display(row_msg)
                    
                    # Insert or update
                    if exists:
                        update_values = (age, city, salary, name)
                        cursor.execute(update_query, update_values)
                        self.updated_records += 1
                    else:
                        insert_values = (name, age, city, salary)
                        cursor.execute(insert_query, insert_values)
                        self.successful_records += 1
                    
                except Error as e:
                    self.failed_records += 1
                    error_msg = f'Failed to process row {index + 1}: {values} - Error: {e}'
                    self.logger.error(error_msg)
                    self.update_status_display(error_msg)
                
                self.update_progress(index + 1, len(data))
                QApplication.processEvents()
            
            connection.commit()
            self.log_summary()
            
            success_msg = f"""Data processing completed:
Successfully Inserted: {self.successful_records}
Successfully Updated: {self.updated_records}
Failed Records: {self.failed_records}
Skipped (Salary > 50000): {self.salary_skipped_records}
Records with Empty Cells: {self.empty_cell_records}
Records with Zero Values: {self.zero_value_records}"""
            self.update_status_display(success_msg)
            
        except Error as e:
            error_msg = f"Error during data processing: {e}"
            self.logger.error(error_msg)
            self.update_status_display(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def log_summary(self):
        """Log operation summary"""
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
        
        if self.total_records > 0:
            success_rate = ((self.successful_records + self.updated_records) / self.total_records) * 100
            self.logger.info(f'Success Rate: {success_rate:.2f}%')
        self.logger.info('=' * 50)

    def convert_data(self):
        """Main data conversion process"""
        try:
            # Check Excel file
            if not os.path.exists(self.EXCEL_PATH):
                error_msg = f"ไม่พบไฟล์ Excel: {self.EXCEL_PATH}"
                self.logger.error(error_msg)
                self.update_status_display(error_msg)
                QMessageBox.critical(self, "Error", error_msg)
                return
                
            # Reset UI
            self.progress_bar.setValue(0)
            self.status_text.clear()
            self.initialize_counters()
            
            # Read Excel file
            self.update_status_display(f'Reading Excel file: {self.EXCEL_PATH}')
            df = pd.read_excel(self.EXCEL_PATH)
            self.update_status_display(f'Successfully read {len(df)} rows from Excel file')
            
            # Connect to database
            connection = self.create_database_connection()
            if connection is None:
                return
                
            try:
                # Process data
                self.insert_data(connection, df)
                
                # Show summary
                summary_msg = f"""Operation Summary:
Total Records: {self.total_records}
Successfully Inserted: {self.successful_records}
Successfully Updated: {self.updated_records}
Failed Records: {self.failed_records}
Skipped (Salary > 50000): {self.salary_skipped_records}
Records with Empty Cells: {self.empty_cell_records}
Records with Zero Values: {self.zero_value_records}"""
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
    """
    Main function to start the application
    """
    app = QApplication(sys.argv)
    ex = ExcelToMySQLApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 