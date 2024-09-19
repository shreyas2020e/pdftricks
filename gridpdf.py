from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter

def create_coordinate_grid(output_path, page_size=letter, step=0.5*inch):
    c = canvas.Canvas(output_path, pagesize=page_size)
    width, height = page_size

    # Draw vertical lines
    for x in range(0, int(width), int(step)):
        c.line(x, 0, x, height)
        c.drawString(x, 0, str(x))

    # Draw horizontal lines
    for y in range(0, int(height), int(step)):
        c.line(0, y, width, y)
        c.drawString(0, y, str(y))

    c.save()

# Create the coordinate grid
create_coordinate_grid("coordinate_grid.pdf")

def overlay_grid_on_pdf(input_pdf, output_pdf):
    from PyPDF2 import PdfReader, PdfWriter

    # Read the input PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Create the grid
    create_coordinate_grid("temp_grid.pdf")
    grid = PdfReader("temp_grid.pdf")

    # Overlay the grid on each page
    for page in reader.pages:
        page.merge_page(grid.pages[0])
        writer.add_page(page)

    # Write the result
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

# Usage
overlay_grid_on_pdf("form.pdf", "form_with_grid.pdf")
