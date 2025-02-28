import fitz  # PyMuPDF
import os
import mysql.connector

# Set the folder containing PDF files
pdf_folder = "D:\\Aditya Personal\\seeddms\\Images"  # Change if needed

# MySQL Connection Configuration
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "pdf_check"
}

# Try connecting to MySQL
print("🔄 Attempting to connect to MySQL...")
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully!")

    # Ensure the table exists with correct column names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inverted_pdf_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            folder_name VARCHAR(255),
            document_name VARCHAR(255),
            rotated_page_number VARCHAR(255)
        )
    """)
    conn.commit()
    print("✅ Table 'inverted_pdf_details' is ready.")

    # **Delete all existing data and reset the auto-increment ID to 1**
    cursor.execute("TRUNCATE TABLE inverted_pdf_details")
    conn.commit()
    print("✅ Table cleared, IDs will start from 1.")

except mysql.connector.Error as err:
    print(f"❌ MySQL connection error: {err}")
    exit()

# Dictionary to store results
inverted_pages = {}

# Recursively find all PDF files in the folder and subfolders
for root, _, files in os.walk(pdf_folder):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            folder_name = os.path.basename(root)  # Get correct folder name
            doc = fitz.open(pdf_path)
            inverted_pages[(folder_name, file)] = []

            # Loop through each page
            for page_number in range(len(doc)):
                page = doc[page_number]
                rotation = page.rotation

                # Check if the page is inverted (180 degrees)
                if rotation == 180:
                    inverted_pages[(folder_name, file)].append(page_number + 1)

# Insert results into MySQL
print("\n✅ Inverted Page Report:\n")
for (folder, pdf), pages in inverted_pages.items():
    if pages:
        pages_str = ", ".join(map(str, pages))
        print(f"📂 Folder: {folder} | 📄 Document: {pdf} | 🔄 Inverted Pages: {pages_str}")

        # Insert data into MySQL
        try:
            insert_query = """
                INSERT INTO inverted_pdf_details (folder_name, document_name, rotated_page_number)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (folder, pdf, pages_str))
            conn.commit()
            print(f"✅ Inserted into database: {pdf}")
        except mysql.connector.Error as err:
            print(f"❌ MySQL Insert Error: {err}")

# Close MySQL connection
cursor.close()
conn.close()
print("\n✅ PDF analysis and database update complete!")
