import sqlite3
import os
import datetime
from fpdf import FPDF
from directories import DB_DIR, REPORTS_DIR as REPORT_DIR, BRAND_DIR

DB_PATH = os.path.join(DB_DIR, "devices.db")


class PDFReport(FPDF):
    def header(self):
        # Logo
        self.image(os.path.join(BRAND_DIR, 'company_logo.png'), 10, 8, 33)
        self.set_font('Arial', 'B', 12)

        # Title
        self.cell(276, 10, 'Device Report', 0, 1, 'C')

        # Date and Time
        self.set_font('Arial', '', 10)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cell(276, 10, f'Date and Time: {current_time}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report():
    try:
        conn = sqlite3.connect(DB_DIR)
        cursor = conn.cursor()

        query = "SELECT * FROM devices"
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        pdf = PDFReport(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_fill_color(200, 220, 255)
        col_width = pdf.get_string_width(max(columns, key=len)) + 6

        # Headers
        for col in columns:
            pdf.cell(col_width, 10, col, 1, fill=True)

        pdf.ln()

        # Data
        for row in data:
            for item in row:
                pdf.cell(col_width, 10, str(item), 1)
            pdf.ln()

        report_path = os.path.join(REPORT_DIR, f"Device_Report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        pdf.output(report_path)

        conn.close()

        return report_path

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

if __name__ == "__main__":
    generate_pdf_report()
