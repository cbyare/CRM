# reports.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def total_customers(customers):
    return len(customers)

def list_customer_names(customers):
    return [c.name for c in customers]

def generate_pdf_report(customers, filename="customer_report.pdf"):
    """Generate a PDF report of customers."""
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Customer Report")
    c.drawString(50, 730, f"Total Customers: {total_customers(customers)}")
    
    y = 710
    for idx, customer in enumerate(customers, start=1):
        c.drawString(50, y, f"{idx}. {customer.name} - {customer.email or 'No Email'}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return filename
