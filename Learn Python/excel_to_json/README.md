# Excel to JSON Converter

A simple GUI application to convert Excel files to JSON format.

## Features
- User-friendly graphical interface
- Progress bar showing conversion status
- Detailed conversion summary
- Support for .xlsx and .xls files
- Converts Excel data to formatted JSON

## How to Use
1. Run the application
2. Click "Select Excel File" to choose your Excel file
3. Click "Convert to JSON" to start the conversion
4. The converted JSON file will be saved in the same directory as the Excel file
5. View the conversion summary in the status display

## Building from Source
1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python excel_to_json_converter.py
   ```

## Building Executable
To create a standalone executable:
```
python build_exe.py
```
The executable will be created in the `dist` folder. 