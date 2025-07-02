import sys
import os
import json
import pandas as pd
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                            QProgressBar, QTextEdit, QMessageBox, QTableWidget, 
                            QTableWidgetItem, QPlainTextEdit, QFrame, QSizePolicy, 
                            QLineEdit, QInputDialog, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)

    def __init__(self, excel_file):
        super().__init__()
        self.excel_file = excel_file

    def safe_json_parse(self, val):
        if pd.isnull(val):
            return None
        if hasattr(val, 'strftime'):
            return val.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(val, str):
            try:
                # First try to parse as JSON
                return json.loads(val)
            except json.JSONDecodeError:
                try:
                    # If JSON parsing fails, try to evaluate as Python literal
                    import ast
                    return ast.literal_eval(val)
                except:
                    return val
        if isinstance(val, (list, dict)):
            return val
        return str(val)

    def run(self):
        def log_to_file(msg):
            with open('log_process_converter.txt', 'a', encoding='utf-8') as logf:
                logf.write(msg + '\n')

        try:
            # Read Excel file
            self.status.emit("Reading Excel file...")
            log_to_file("Reading Excel file...")
            df = pd.read_excel(self.excel_file)
            self.progress.emit(10)

            # Use all columns dynamically from the first row
            selected_cols = list(df.columns)
            df_selected = df[selected_cols]

            # Convert 'timestamp' column to string if it exists
            if 'timestamp' in df_selected.columns:
                def safe_to_str(x):
                    if pd.isnull(x):
                        return None
                    if hasattr(x, 'strftime'):
                        return x.strftime('%Y-%m-%d %H:%M:%S')
                    return str(x)
                df_selected['timestamp'] = df_selected['timestamp'].apply(safe_to_str)

            self.progress.emit(20)

            # Convert to JSON row by row, show status for each row
            self.status.emit("Converting to JSON (row by row)...")
            log_to_file("Converting to JSON (row by row)...")
            json_data = []
            total_rows = len(df_selected)
            for idx, row in df_selected.iterrows():
                try:
                    row_dict = {col: self.safe_json_parse(row[col]) for col in df_selected.columns}
                    json_data.append(row_dict)
                    msg = f"Row {idx+1}/{total_rows}: Success"
                    self.status.emit(msg)
                    log_to_file(msg)
                except Exception as e:
                    msg = f"Row {idx+1}/{total_rows}: Error - {str(e)}"
                    self.status.emit(msg)
                    log_to_file(msg)
                # Update progress bar
                progress = 20 + int(60 * (idx+1) / total_rows)
                self.progress.emit(progress)
                time.sleep(0.001)

            # Save JSON file
            self.status.emit("Saving JSON file...")
            log_to_file("Saving JSON file...")
            output_file = os.path.splitext(self.excel_file)[0] + '.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            self.progress.emit(100)

            summary = f'Successfully converted to {output_file} | Rows processed: {len(json_data)}'
            result = {
                'success': True,
                'message': f'Successfully converted to {output_file}',
                'rows_processed': len(json_data)
            }
            log_to_file(summary)
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            result = {
                'success': False,
                'message': error_msg,
                'rows_processed': 0
            }
            log_to_file(error_msg)
        
        self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QProgressBar {
                border: 2px solid #2196F3;
                border-radius: 5px;
                text-align: center;
                background-color: #E3F2FD;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
            QTextEdit, QPlainTextEdit {
                border: 2px solid #BDBDBD;
                border-radius: 4px;
                background-color: white;
                padding: 4px;
            }
            QTableWidget {
                border: 2px solid #BDBDBD;
                border-radius: 4px;
                background-color: white;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 4px;
                border: 1px solid #1976D2;
            }
        """)
        # Initialize history for undo/redo
        self.history = []
        self.history_index = -1
        self.max_history = 50
        # Initialize clipboard for copy/paste
        self.clipboard_data = None

    def initUI(self):
        self.setWindowTitle('Excel/JSON Converter & Editor')
        self.setGeometry(100, 100, 1200, 1000)
        self.setMinimumSize(800, 600)  # Set minimum window size

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 10)

        # Add header section with logo and title
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #1976D2;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)
        
        # Logo text
        logo_label = QLabel('RaptorXCode')
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Arial';
                padding: 5px;
            }
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Program title
        title_label = QLabel('Excel/JSON Converter and Editor')
        title_label.setStyleSheet("""
            QLabel {
                color: #E3F2FD;
                font-size: 20px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        main_layout.addWidget(header_widget)

        # Add a subtle shadow effect
        shadow_widget = QWidget()
        shadow_widget.setFixedHeight(3)
        shadow_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1565C0, stop:1 #1976D2);
            }
        """)
        main_layout.addWidget(shadow_widget)

        # Content container with margins
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Top section - File selection and progress
        top_section = QWidget()
        top_layout = QVBoxLayout(top_section)
        top_layout.setSpacing(5)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.select_button = QPushButton('Select File')
        self.select_button.setMinimumWidth(120)
        self.select_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.select_button)
        top_layout.addLayout(file_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_layout.addWidget(self.progress_bar)

        content_layout.addWidget(top_section)

        # Middle section - Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.convert_button = QPushButton('Convert to JSON')
        self.convert_button.setMinimumWidth(150)
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setEnabled(False)
        button_layout.addWidget(self.convert_button)

        self.json_to_excel_button = QPushButton('Convert JSON to Excel')
        self.json_to_excel_button.setMinimumWidth(150)
        self.json_to_excel_button.clicked.connect(self.json_to_excel)
        button_layout.addWidget(self.json_to_excel_button)

        self.view_json_button = QPushButton('View/Edit JSON')
        self.view_json_button.setMinimumWidth(150)
        self.view_json_button.clicked.connect(self.view_edit_json)
        button_layout.addWidget(self.view_json_button)

        self.save_json_button = QPushButton('Save JSON')
        self.save_json_button.setMinimumWidth(150)
        self.save_json_button.clicked.connect(self.save_json)
        self.save_json_button.setEnabled(False)
        button_layout.addWidget(self.save_json_button)

        self.done_button = QPushButton('Done')
        self.done_button.setMinimumWidth(100)
        self.done_button.clicked.connect(self.close_app)
        self.done_button.setVisible(False)
        button_layout.addWidget(self.done_button)

        content_layout.addLayout(button_layout)

        # Bottom section - Split view for table and JSON editor
        bottom_section = QWidget()
        bottom_layout = QHBoxLayout(bottom_section)
        bottom_layout.setSpacing(10)

        # Left side - Status display and buttons
        status_container = QWidget()
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)
        
        status_label = QLabel("Status Display")
        status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1976D2;")
        status_layout.addWidget(status_label)
        
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setMinimumHeight(100)
        self.status_display.setMaximumHeight(150)
        self.status_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_display.setStyleSheet("font-size: 12px;")
        status_layout.addWidget(self.status_display)

        # Add Row Management Group below Status display
        row_management_group = QWidget()
        row_management_layout = QHBoxLayout(row_management_group)
        row_management_layout.setSpacing(5)
        row_management_layout.setContentsMargins(0, 0, 0, 0)

        # Single row operations
        self.add_row_button = QPushButton('Add Row')
        self.add_row_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_row_button.clicked.connect(self.add_row)
        row_management_layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton('Delete Row')
        self.delete_row_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_row_button.clicked.connect(self.delete_row)
        row_management_layout.addWidget(self.delete_row_button)

        # Copy/Paste operations
        self.copy_row_button = QPushButton('Copy Row')
        self.copy_row_button.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
        """)
        self.copy_row_button.clicked.connect(self.copy_row)
        row_management_layout.addWidget(self.copy_row_button)

        self.paste_row_button = QPushButton('Paste Row')
        self.paste_row_button.setStyleSheet("""
            QPushButton {
                background-color: #009688;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #00796B;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.paste_row_button.clicked.connect(self.paste_row)
        self.paste_row_button.setEnabled(False)
        row_management_layout.addWidget(self.paste_row_button)

        status_layout.addWidget(row_management_group)

        # Add Multiple Row Management Group below Status display
        multi_row_group = QWidget()
        multi_row_layout = QHBoxLayout(multi_row_group)
        multi_row_layout.setSpacing(5)
        multi_row_layout.setContentsMargins(0, 0, 0, 0)

        self.add_multiple_button = QPushButton('Add Multiple')
        self.add_multiple_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_multiple_button.clicked.connect(self.add_multiple_rows)
        multi_row_layout.addWidget(self.add_multiple_button)

        self.delete_multiple_button = QPushButton('Delete Selected')
        self.delete_multiple_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_multiple_button.clicked.connect(self.delete_multiple_rows)
        multi_row_layout.addWidget(self.delete_multiple_button)

        status_layout.addWidget(multi_row_group)

        # Add Undo/Redo group
        undo_redo_group = QWidget()
        undo_redo_layout = QHBoxLayout(undo_redo_group)
        undo_redo_layout.setSpacing(5)
        undo_redo_layout.setContentsMargins(0, 0, 0, 0)

        self.undo_button = QPushButton('Undo')
        self.undo_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.undo_button.clicked.connect(self.undo_action)
        self.undo_button.setEnabled(False)
        undo_redo_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton('Redo')
        self.redo_button.setStyleSheet("""
            QPushButton {
                background-color: #673AB7;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #512DA8;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.redo_button.clicked.connect(self.redo_action)
        self.redo_button.setEnabled(False)
        undo_redo_layout.addWidget(self.redo_button)

        status_layout.addWidget(undo_redo_group)
        status_layout.addStretch()  # Add stretch to push buttons to the top
        bottom_layout.addWidget(status_container, stretch=1)

        # Right side - JSON editor
        json_container = QWidget()
        json_layout = QVBoxLayout(json_container)
        json_layout.setContentsMargins(0, 0, 0, 0)
        
        json_label = QLabel("JSON Editor")
        json_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1976D2;")
        json_layout.addWidget(json_label)
        
        self.json_row_editor = QPlainTextEdit()
        self.json_row_editor.setPlaceholderText('Selected row as JSON will appear here...')
        self.json_row_editor.setVisible(True)
        self.json_row_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.json_row_editor.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace; font-size: 12px;")
        json_layout.addWidget(self.json_row_editor)

        self.update_row_button = QPushButton('Update Row')
        self.update_row_button.setMinimumWidth(120)
        self.update_row_button.clicked.connect(self.update_row_from_json)
        self.update_row_button.setVisible(True)
        json_layout.addWidget(self.update_row_button)
        bottom_layout.addWidget(json_container, stretch=1)

        content_layout.addWidget(bottom_section, stretch=1)

        # Data Table section
        table_section = QWidget()
        table_layout = QVBoxLayout(table_section)
        table_layout.setSpacing(5)
        
        # Add search box above table
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-size: 12px; color: #1976D2;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search in table...")
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #BDBDBD;
                border-radius: 3px;
                background-color: white;
            }
        """)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        table_layout.addLayout(search_layout)
        
        table_label = QLabel("Data Table")
        table_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1976D2;")
        table_layout.addWidget(table_label)
        
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.table_widget.setVisible(True)
        self.table_widget.itemSelectionChanged.connect(self.show_selected_row_json)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setSortingEnabled(True)  # Enable sorting
        self.table_widget.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 4px;
                border: 1px solid #1976D2;
            }
            QHeaderView::section:hover {
                background-color: #1976D2;
            }
        """)
        # Initialize empty table with some default columns
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(1)
        self.table_widget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        table_layout.addWidget(self.table_widget)
        content_layout.addWidget(table_section, stretch=2)  # Give more space to the table

        main_layout.addWidget(content_widget, stretch=1)

        self.excel_file = None
        self.current_json_data = None
        self.current_json_path = None

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Select File',
            '',
            'All Files (*.*);;Excel Files (*.xlsx *.xls);;JSON Files (*.json)')
        
        if file_name:
            self.excel_file = file_name
            self.file_label.setText(os.path.basename(file_name))
            self.convert_button.setEnabled(True)
            self.status_display.clear()
            self.progress_bar.setValue(0)

    def start_conversion(self):
        if not self.excel_file:
            return

        self.convert_button.setEnabled(False)
        self.select_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_display.clear()

        # Create worker with check_and_convert_json_value function
        self.worker = ConversionWorker(self.excel_file)
        self.worker.check_and_convert_json_value = self.check_and_convert_json_value
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_display.append(message)
        QApplication.processEvents()  # Force GUI update immediately

    def conversion_finished(self, result):
        self.convert_button.setEnabled(True)
        self.select_button.setEnabled(True)
        self.done_button.setVisible(True)
        if result['success']:
            self.status_display.append(f"\nConversion Summary:")
            self.status_display.append(f"✓ {result['message']}")
            self.status_display.append(f"✓ Rows processed: {result['rows_processed']}")
        else:
            self.status_display.append(f"\nConversion Failed:")
            self.status_display.append(f"✗ {result['message']}")

    def json_to_excel(self):
        def log_to_file(msg):
            with open('log_process_converter.txt', 'a', encoding='utf-8') as logf:
                logf.write(msg + '\n')

        if not self.excel_file or not self.excel_file.lower().endswith('.json'):
            QMessageBox.warning(self, "Warning", "Please select a .json file first using the Select File button.")
            return
        json_file = self.excel_file
        try:
            self.status_display.append(f"Reading JSON file: {os.path.basename(json_file)}")
            log_to_file(f"Reading JSON file: {os.path.basename(json_file)}")
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate and convert data
            processed_data = []
            if isinstance(data, list):
                total_rows = len(data)
                for idx, row in enumerate(data):
                    try:
                        # Convert each value using check_and_convert_json_value
                        row_dict = {}
                        for key, value in row.items():
                            try:
                                row_dict[key] = self.check_and_convert_json_value(str(value))
                            except ValueError as e:
                                msg = f"Row {idx+1}, Column '{key}': {str(e)}"
                                self.status_display.append(msg)
                                log_to_file(msg)
                                raise
                        processed_data.append(row_dict)
                        msg = f"Row {idx+1}/{total_rows}: Success"
                        self.status_display.append(msg)
                        log_to_file(msg)
                    except Exception as e:
                        msg = f"Row {idx+1}/{total_rows}: Error - {str(e)}"
                        self.status_display.append(msg)
                        log_to_file(msg)
            else:
                # Single dict
                row_dict = {}
                for key, value in data.items():
                    try:
                        row_dict[key] = self.check_and_convert_json_value(str(value))
                    except ValueError as e:
                        msg = f"Column '{key}': {str(e)}"
                        self.status_display.append(msg)
                        log_to_file(msg)
                        raise
                processed_data.append(row_dict)
                msg = f"Row 1/1: Success"
                self.status_display.append(msg)
                log_to_file(msg)

            df = pd.DataFrame(processed_data)
            output_file = os.path.splitext(json_file)[0] + '_from_json.xlsx'
            df.to_excel(output_file, index=False)
            summary = f"✓ Successfully converted to {os.path.basename(output_file)} | Rows processed: {len(df)}"
            self.status_display.append(summary)
            log_to_file(summary)
            QMessageBox.information(self, "Success", f"Exported to {output_file}")
            self.done_button.setVisible(True)
        except Exception as e:
            msg = f"✗ Error: {str(e)}"
            self.status_display.append(msg)
            log_to_file(msg)
            QMessageBox.critical(self, "Error", f"Failed to convert JSON to Excel: {str(e)}")
            self.done_button.setVisible(True)

    def view_edit_json(self):
        if not self.excel_file or not self.excel_file.lower().endswith('.json'):
            QMessageBox.warning(self, "Warning", "Please select a .json file first using the Select File button.")
            return
        json_file = self.excel_file
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list) or not data:
                QMessageBox.warning(self, "Warning", "JSON file must contain a list of objects and not be empty.")
                return
            self.current_json_data = data
            self.current_json_path = json_file
            self.populate_table_from_json(data)
            self.table_widget.setVisible(True)
            self.save_json_button.setEnabled(True)
            self.status_display.append(f"Loaded {len(data)} rows from {os.path.basename(json_file)} for editing.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON: {str(e)}")

    def populate_table_from_json(self, data):
        self.table_widget.clear()
        headers = list(data[0].keys())
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setRowCount(len(data))
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        # Disable sorting temporarily while populating
        self.table_widget.setSortingEnabled(False)
        
        for row_idx, row in enumerate(data):
            for col_idx, key in enumerate(headers):
                val = row.get(key, "")
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setData(Qt.DisplayRole, str(val) if val is not None else "")  # For proper sorting
                self.table_widget.setItem(row_idx, col_idx, item)
        
        # Re-enable sorting
        self.table_widget.setSortingEnabled(True)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        
        # Enable row management buttons
        self.add_row_button.setEnabled(True)
        self.delete_row_button.setEnabled(True)
        self.copy_row_button.setEnabled(True)
        self.paste_row_button.setEnabled(False)  # Reset paste button state
        self.clipboard_data = None  # Clear clipboard

    def check_and_convert_json_value(self, value):
        """
        Check and convert string value to JSON object if possible
        Returns the converted value or original string if conversion fails
        """
        if not isinstance(value, str):
            return value
            
        try:
            # Remove any extra quotes and spaces
            value = value.strip()
            
            # Handle cases where JSON object/array is wrapped in quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                # Remove outer quotes
                value = value[1:-1]
                # If the inner content is a JSON object/array, parse it
                if (value.startswith('{') and value.endswith('}')) or \
                   (value.startswith('[') and value.endswith(']')):
                    try:
                        parsed_value = json.loads(value)
                        # Validate JSON structure
                        if isinstance(parsed_value, dict):
                            # Check if all keys are strings
                            if not all(isinstance(k, str) for k in parsed_value.keys()):
                                # Fix non-string keys
                                fixed_dict = {str(k): v for k, v in parsed_value.items()}
                                return fixed_dict
                            return parsed_value
                        elif isinstance(parsed_value, list):
                            return parsed_value
                    except json.JSONDecodeError as e:
                        # Try to fix common JSON format issues
                        try:
                            # Fix missing quotes around keys
                            import re
                            fixed_value = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', value)
                            # Fix single quotes to double quotes
                            fixed_value = fixed_value.replace("'", '"')
                            # Fix missing commas
                            fixed_value = re.sub(r'"\s*}\s*"', '"},"', fixed_value)
                            fixed_value = re.sub(r'"\s*]\s*"', '"],"', fixed_value)
                            # Remove trailing commas
                            fixed_value = re.sub(r',\s*([}\]])', r'\1', fixed_value)
                            
                            parsed_value = json.loads(fixed_value)
                            if isinstance(parsed_value, dict):
                                # Ensure all keys are strings
                                fixed_dict = {str(k): v for k, v in parsed_value.items()}
                                return fixed_dict
                            return parsed_value
                        except:
                            raise ValueError(f"Invalid JSON format: {str(e)}")
                    except Exception as e:
                        raise ValueError(f"JSON validation error: {str(e)}")
                return value
            
            # Check if it's a JSON object
            if value.startswith('{') and value.endswith('}'):
                try:
                    parsed_value = json.loads(value)
                    # Validate JSON structure
                    if isinstance(parsed_value, dict):
                        # Check if all keys are strings
                        if not all(isinstance(k, str) for k in parsed_value.keys()):
                            # Fix non-string keys
                            fixed_dict = {str(k): v for k, v in parsed_value.items()}
                            return fixed_dict
                        return parsed_value
                except json.JSONDecodeError as e:
                    # Try to fix common JSON format issues
                    try:
                        # Fix missing quotes around keys
                        import re
                        fixed_value = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', value)
                        # Fix single quotes to double quotes
                        fixed_value = fixed_value.replace("'", '"')
                        # Fix missing commas
                        fixed_value = re.sub(r'"\s*}\s*"', '"},"', fixed_value)
                        fixed_value = re.sub(r'"\s*]\s*"', '"],"', fixed_value)
                        # Remove trailing commas
                        fixed_value = re.sub(r',\s*([}\]])', r'\1', fixed_value)
                        
                        parsed_value = json.loads(fixed_value)
                        if isinstance(parsed_value, dict):
                            # Ensure all keys are strings
                            fixed_dict = {str(k): v for k, v in parsed_value.items()}
                            return fixed_dict
                        return parsed_value
                    except:
                        raise ValueError(f"Invalid JSON format: {str(e)}")
                except Exception as e:
                    raise ValueError(f"JSON validation error: {str(e)}")
            # Check if it's a JSON array
            elif value.startswith('[') and value.endswith(']'):
                try:
                    parsed_value = json.loads(value)
                    if isinstance(parsed_value, list):
                        return parsed_value
                except json.JSONDecodeError as e:
                    # Try to fix common JSON array format issues
                    try:
                        # Fix single quotes to double quotes
                        fixed_value = value.replace("'", '"')
                        # Fix missing commas
                        fixed_value = re.sub(r'"\s*]\s*"', '"],"', fixed_value)
                        # Remove trailing commas
                        fixed_value = re.sub(r',\s*]', ']', fixed_value)
                        
                        parsed_value = json.loads(fixed_value)
                        if isinstance(parsed_value, list):
                            return parsed_value
                    except:
                        raise ValueError(f"Invalid JSON array format: {str(e)}")
            # Check if it's a number
            elif value.replace('.', '', 1).isdigit():
                if '.' in value:
                    return float(value)
                return int(value)
            # Check if it's a boolean
            elif value.lower() in ['true', 'false']:
                return value.lower() == 'true'
            # Check if it's null
            elif value.lower() == 'null':
                return None
        except Exception as e:
            # If any conversion fails, raise the error
            raise ValueError(str(e))
            
        return value

    def save_json(self):
        if self.current_json_data is None or self.current_json_path is None:
            QMessageBox.warning(self, "Warning", "No JSON data loaded for editing.")
            return

        # Create preview dialog
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Preview JSON Data")
        preview_dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(preview_dialog)
        
        # Add preview label
        preview_label = QLabel("Preview of data to be saved:")
        preview_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1976D2;")
        layout.addWidget(preview_label)
        
        # Add preview text area
        preview_text = QPlainTextEdit()
        preview_text.setReadOnly(True)
        preview_text.setStyleSheet("""
            QPlainTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        layout.addWidget(preview_text)
        
        # Add buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Get data from table and check all rows
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
        new_data = []
        validation_messages = []
        fixed_messages = []
        
        # First pass: Validate and collect issues
        for row_idx in range(self.table_widget.rowCount()):
            row_dict = {}
            row_valid = True
            row_messages = []
            
            for col_idx, key in enumerate(headers):
                item = self.table_widget.item(row_idx, col_idx)
                if item:
                    value = item.text()
                    try:
                        # Try to convert and fix the value
                        converted_value = self.check_and_convert_json_value(value)
                        row_dict[key] = converted_value
                    except ValueError as e:
                        row_valid = False
                        row_messages.append(f"Column '{key}': {str(e)}")
                else:
                    row_dict[key] = ""
            
            if not row_valid:
                validation_messages.append(f"Row {row_idx + 1}:")
                validation_messages.extend([f"  - {msg}" for msg in row_messages])
            new_data.append(row_dict)

        # Second pass: Fix all rows
        fixed_data = []
        for row_idx, row_dict in enumerate(new_data):
            fixed_row = {}
            row_fixed = []
            
            for key, value in row_dict.items():
                try:
                    # Try to fix the value
                    if isinstance(value, str):
                        # Remove extra quotes and spaces
                        value = value.strip()
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        
                            # Try to fix JSON format
                            if value.startswith('{') and value.endswith('}'):
                                try:
                                    # Fix missing quotes around keys
                                    import re
                                    fixed_value = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', value)
                                    # Fix single quotes to double quotes
                                    fixed_value = fixed_value.replace("'", '"')
                                    # Fix missing commas
                                    fixed_value = re.sub(r'"\s*}\s*"', '"},"', fixed_value)
                                    fixed_value = re.sub(r'"\s*]\s*"', '"],"', fixed_value)
                                    # Remove trailing commas
                                    fixed_value = re.sub(r',\s*([}\]])', r'\1', fixed_value)
                                    
                                    parsed_value = json.loads(fixed_value)
                                    if isinstance(parsed_value, dict):
                                        # Ensure all keys are strings
                                        fixed_dict = {str(k): v for k, v in parsed_value.items()}
                                        fixed_row[key] = fixed_dict
                                        if str(value) != str(fixed_dict):
                                            row_fixed.append(f"Column '{key}': Fixed format from '{value}' to '{fixed_dict}'")
                                        continue
                                except:
                                    pass
                            elif value.startswith('[') and value.endswith(']'):
                                try:
                                    # Fix array format
                                    fixed_value = value.replace("'", '"')
                                    fixed_value = re.sub(r',\s*]', ']', fixed_value)
                                    parsed_value = json.loads(fixed_value)
                                    if isinstance(parsed_value, list):
                                        fixed_row[key] = parsed_value
                                        if str(value) != str(parsed_value):
                                            row_fixed.append(f"Column '{key}': Fixed format from '{value}' to '{parsed_value}'")
                                        continue
                                except:
                                    pass
                    
                    # If no fixes were applied, keep original value
                    fixed_row[key] = value
                except Exception as e:
                    fixed_row[key] = value
            
            if row_fixed:
                fixed_messages.append(f"Row {row_idx + 1}:")
                fixed_messages.extend([f"  - {msg}" for msg in row_fixed])
            fixed_data.append(fixed_row)

        # Show validation messages if any
        if validation_messages or fixed_messages:
            if fixed_messages:
                fixed_label = QLabel("Fixed Format Issues:")
                fixed_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
                layout.insertWidget(0, fixed_label)
                
                fixed_text = QPlainTextEdit()
                fixed_text.setReadOnly(True)
                fixed_text.setStyleSheet("""
                    QPlainTextEdit {
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 12px;
                        background-color: #e8f5e9;
                        border: 1px solid #c8e6c9;
                        border-radius: 4px;
                        padding: 8px;
                    }
                """)
                fixed_text.setPlainText("\n".join(fixed_messages))
                fixed_text.setMaximumHeight(150)
                layout.insertWidget(1, fixed_text)
            
            if validation_messages:
                validation_label = QLabel("Validation Issues Found:")
                validation_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f44336;")
                layout.insertWidget(2 if fixed_messages else 0, validation_label)
                
                validation_text = QPlainTextEdit()
                validation_text.setReadOnly(True)
                validation_text.setStyleSheet("""
                    QPlainTextEdit {
                        font-family: 'Consolas', 'Courier New', monospace;
                        font-size: 12px;
                        background-color: #ffebee;
                        border: 1px solid #ffcdd2;
                        border-radius: 4px;
                        padding: 8px;
                    }
                """)
                validation_text.setPlainText("\n".join(validation_messages))
                validation_text.setMaximumHeight(150)
                layout.insertWidget(3 if fixed_messages else 1, validation_text)

        # Show preview of fixed data
        preview_text.setPlainText(json.dumps(fixed_data, ensure_ascii=False, indent=4))
        
        # Connect buttons
        save_button.clicked.connect(preview_dialog.accept)
        cancel_button.clicked.connect(preview_dialog.reject)
        
        # Show dialog
        if preview_dialog.exec_() == QDialog.Accepted:
            try:
                save_path, _ = QFileDialog.getSaveFileName(self, 'Save JSON File', self.current_json_path, 'JSON Files (*.json)')
                if not save_path:
                    return
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(fixed_data, f, ensure_ascii=False, indent=4)
                self.status_display.append(f"Saved edited JSON to {os.path.basename(save_path)}.")
                if fixed_messages:
                    self.status_display.append("Fixed format issues were applied.")
                QMessageBox.information(self, "Success", f"Saved edited JSON to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save JSON: {str(e)}")

    def close_app(self):
        QApplication.quit()

    def show_selected_row_json(self):
        try:
            selected = self.table_widget.selectedItems()
            if not selected:
                self.json_row_editor.setVisible(False)
                self.update_row_button.setVisible(False)
                return

            row_idx = self.table_widget.currentRow()
            if row_idx < 0:
                return

            headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
            row_dict = {}
            for col_idx, key in enumerate(headers):
                item = self.table_widget.item(row_idx, col_idx)
                value = item.text() if item else ""
                # Parse nested JSON if the value is a string
                row_dict[key] = self.safe_json_parse(value)
            
            formatted_json = {
                "data": row_dict
            }
            self.json_row_editor.setPlainText(json.dumps(formatted_json, ensure_ascii=False, indent=4))
            self.json_row_editor.setVisible(True)
            self.update_row_button.setVisible(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error showing JSON: {str(e)}")

    def safe_json_parse(self, value):
        if pd.isnull(value):
            return None
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, str):
            try:
                # First try to parse as JSON
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    # If JSON parsing fails, try to evaluate as Python literal
                    import ast
                    return ast.literal_eval(value)
                except:
                    return value
        if isinstance(value, (list, dict)):
            return value
        return str(value)

    def update_row_from_json(self):
        row_idx = self.table_widget.currentRow()
        if row_idx < 0:
            QMessageBox.warning(self, "Warning", "No row selected.")
            return
        try:
            import json
            json_data = json.loads(self.json_row_editor.toPlainText())
            row_dict = json_data.get("data", {})
            headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
            for col_idx, key in enumerate(headers):
                val = row_dict.get(key, "")
                # Convert complex objects to string representation
                if isinstance(val, (dict, list)):
                    val = json.dumps(val, ensure_ascii=False)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
            self.status_display.append(f"Updated row {row_idx+1} from JSON editor.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON: {str(e)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure the table and JSON editor maintain their proportions
        if self.table_widget.isVisible() and self.json_row_editor.isVisible():
            total_width = self.width() - 40  # Account for margins
            self.table_widget.setMinimumWidth(total_width // 2)
            self.json_row_editor.setMinimumWidth(total_width // 2)

    def filter_table(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table_widget.rowCount()):
            show_row = False
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table_widget.setRowHidden(row, not show_row)

    def add_row(self):
        try:
            current_row = self.table_widget.currentRow()
            if current_row < 0:
                current_row = self.table_widget.rowCount()
            
            # Save state for undo
            self.save_state()
            
            self.table_widget.insertRow(current_row)
            for col in range(self.table_widget.columnCount()):
                item = QTableWidgetItem("")
                self.table_widget.setItem(current_row, col, item)
            
            # Select the new row
            self.table_widget.selectRow(current_row)
            
            # Update JSON data if exists
            if self.current_json_data is not None:
                new_row = {self.table_widget.horizontalHeaderItem(i).text(): "" 
                          for i in range(self.table_widget.columnCount())}
                self.current_json_data.insert(current_row, new_row)
            
            self.status_display.append(f"Added new row at position {current_row + 1}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add row: {str(e)}")

    def delete_row(self):
        try:
            current_row = self.table_widget.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a row to delete")
                return
            
            reply = QMessageBox.question(self, 'Confirm Delete', 
                                       'Are you sure you want to delete this row?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Save state for undo
                self.save_state()
                
                self.table_widget.removeRow(current_row)
                
                # Update JSON data if exists
                if self.current_json_data is not None:
                    self.current_json_data.pop(current_row)
                
                self.status_display.append(f"Deleted row at position {current_row + 1}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete row: {str(e)}")

    def add_multiple_rows(self):
        try:
            count, ok = QInputDialog.getInt(self, 'Add Multiple Rows', 
                                          'Enter number of rows to add:', 1, 1, 100, 1)
            if ok:
                current_row = self.table_widget.currentRow()
                if current_row < 0:
                    current_row = self.table_widget.rowCount()
                
                # Save state for undo
                self.save_state()
                
                for i in range(count):
                    self.table_widget.insertRow(current_row + i)
                    for col in range(self.table_widget.columnCount()):
                        item = QTableWidgetItem("")
                        self.table_widget.setItem(current_row + i, col, item)
                
                # Update JSON data if exists
                if self.current_json_data is not None:
                    new_rows = [{self.table_widget.horizontalHeaderItem(i).text(): "" 
                               for i in range(self.table_widget.columnCount())} 
                              for _ in range(count)]
                    self.current_json_data[current_row:current_row] = new_rows
                
                self.status_display.append(f"Added {count} new rows at position {current_row + 1}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add rows: {str(e)}")

    def delete_multiple_rows(self):
        try:
            selected_rows = sorted(set(item.row() for item in self.table_widget.selectedItems()))
            if not selected_rows:
                QMessageBox.warning(self, "Warning", "Please select rows to delete")
                return
            
            reply = QMessageBox.question(self, 'Confirm Delete', 
                                       f'Are you sure you want to delete {len(selected_rows)} rows?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Save state for undo
                self.save_state()
                
                # Delete rows in reverse order to maintain correct indices
                for row in reversed(selected_rows):
                    self.table_widget.removeRow(row)
                    if self.current_json_data is not None:
                        self.current_json_data.pop(row)
                
                self.status_display.append(f"Deleted {len(selected_rows)} rows")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete rows: {str(e)}")

    def save_state(self):
        # Save current table state
        state = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            state.append(row_data)
        
        # Remove any future states if we're not at the end of history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add new state
        self.history.append(state)
        self.history_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1
        
        # Update undo/redo buttons
        self.undo_button.setEnabled(self.history_index > 0)
        self.redo_button.setEnabled(self.history_index < len(self.history) - 1)

    def undo_action(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.restore_state(self.history[self.history_index])
            self.undo_button.setEnabled(self.history_index > 0)
            self.redo_button.setEnabled(True)
            self.status_display.append("Undo: Restored previous state")

    def redo_action(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.restore_state(self.history[self.history_index])
            self.undo_button.setEnabled(True)
            self.redo_button.setEnabled(self.history_index < len(self.history) - 1)
            self.status_display.append("Redo: Restored next state")

    def restore_state(self, state):
        self.table_widget.setRowCount(len(state))
        for row, row_data in enumerate(state):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, col, item)
        
        # Update JSON data if exists
        if self.current_json_data is not None:
            headers = [self.table_widget.horizontalHeaderItem(i).text() 
                      for i in range(self.table_widget.columnCount())]
            self.current_json_data = [{headers[i]: row[i] for i in range(len(headers))} 
                                    for row in state]

    def copy_row(self):
        try:
            current_row = self.table_widget.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a row to copy")
                return
            
            # Save state for undo
            self.save_state()
            
            # Copy row data
            self.clipboard_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(current_row, col)
                self.clipboard_data.append(item.text() if item else "")
            
            # Enable paste button
            self.paste_row_button.setEnabled(True)
            self.status_display.append(f"Copied row {current_row + 1}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy row: {str(e)}")

    def paste_row(self):
        try:
            if not self.clipboard_data:
                return
            
            current_row = self.table_widget.currentRow()
            if current_row < 0:
                current_row = self.table_widget.rowCount()
            
            # Save state for undo
            self.save_state()
            
            # Insert new row
            self.table_widget.insertRow(current_row)
            for col, value in enumerate(self.clipboard_data):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(current_row, col, item)
            
            # Update JSON data if exists
            if self.current_json_data is not None:
                new_row = {self.table_widget.horizontalHeaderItem(i).text(): self.clipboard_data[i]
                          for i in range(self.table_widget.columnCount())}
                self.current_json_data.insert(current_row, new_row)
            
            # Select the new row
            self.table_widget.selectRow(current_row)
            self.status_display.append(f"Pasted row at position {current_row + 1}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to paste row: {str(e)}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1) 