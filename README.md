# PDF Inverted Page Detector  

## Overview  
The PDF Inverted Page Detector is a Python-based tool that scans multiple PDF files within a specified directory (including subfolders) and identifies pages that are rotated 180 degrees (inverted). The detected data (file path, document name, and rotated pages) is then stored in a MySQL database for easy tracking and reporting.  

## Features  
- Scans all PDF files in a given folder and subfolders  
- Detects and records pages that are rotated 180 degrees  
- Stores the results in a MySQL database  
- Deletes old data before every new scan to ensure fresh results  
- Ensures auto-incremented IDs start from 1 on every execution  

## Technologies Used  
- Python  
- PyMuPDF (pymupdf) – for reading and analyzing PDFs  
- MySQL – for storing detected results  
- OS Module – for file system operations  

## Prerequisites  
Make sure you have the following installed before running the script:  
1. Python (3.x recommended)  
2. MySQL Server (Ensure it's running on localhost)  

## Installation  
Install the required Python packages using:  
```
pip install pymupdf mysql-connector-python
```

## Setup and Configuration  

### Step 1: Create MySQL Database and Table  
Run the following SQL queries to set up the database and table:  
```
CREATE DATABASE IF NOT EXISTS pdf_check;

USE pdf_check;

CREATE TABLE IF NOT EXISTS inverted_pdf_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folder_name VARCHAR(255),
    document_name VARCHAR(255),
    rotated_page_number VARCHAR(255)
);
```

### Step 2: Configure the Script  
Modify the `pdf_folder` path in `app.py` to match your PDF storage location:  
```
pdf_folder = "D:\\Aditya Personal\\seeddms\\Images"  # Change if needed
```

### Step 3: Run the Script  
Execute the script using:  
```
python app.py
```

## How It Works  
1. The script scans the specified folder and its subfolders for PDF files.  
2. It checks each page for a rotation of 180 degrees.  
3. If inverted pages are found, the script stores the results in the MySQL database.  
4. Before each execution, the script clears previous data (TRUNCATE TABLE) to maintain fresh records.  
5. The output displays detected inverted pages and stores them in the database.  

## Example Output  
```
🔄 Attempting to connect to MySQL...
✅ Connected to MySQL successfully!
✅ Table 'inverted_pdf_details' is ready.
✅ Table cleared, IDs will start from 1.

✅ Inverted Page Report:
📂 Folder: Reports | 📄 Document: Invoice.pdf | 🔄 Inverted Pages: 2, 5
📂 Folder: Contracts | 📄 Document: Agreement.pdf | 🔄 Inverted Pages: 3

✅ Inserted into database: Invoice.pdf
✅ Inserted into database: Agreement.pdf

✅ PDF analysis and database update complete!
```

## Troubleshooting  
- ModuleNotFoundError: No module named ‘mysql.connector’  
  - Run `pip install mysql-connector-python`  
- No PDFs found or detected pages  
  - Check if the specified folder contains valid PDF files  

## Future Enhancements  
- Add Web UI to upload PDFs and display results  
- Implement email notifications for detected issues  
- Support for detecting other types of PDF page misalignment
