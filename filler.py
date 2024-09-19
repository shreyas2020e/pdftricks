import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def fill_pdf(input_pdf_path, output_pdf_path, data, font_name='Helvetica', font_size=4):
    # Read the input PDF
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    # Get the first page
    page = pdf_reader.pages[0]

    # Create a new PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Set the font and font size
    can.setFont(font_name, font_size)

    # Add text to the new PDF
    for key, value in data.items():
        can.drawString(key[0], key[1], value)

    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Add the "watermark" (new pdf) on the existing page
    page.merge_page(new_pdf.pages[0])

    # Add the modified page to the output PDF
    pdf_writer.add_page(page)

    # Write the output PDF
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

# Example usage
input_pdf = 'form.pdf'
output_pdf = 'filled_form.pdf'
form_data = {
    (340, 730): ' J   o    h   n      D    o    e',  # (x, y) coordinates: value
    
}

# Fill the PDF with Helvetica font at size 14
fill_pdf(input_pdf, output_pdf, form_data, font_name='Helvetica', font_size=12)
