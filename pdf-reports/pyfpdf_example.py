"""
Example PDF file generation using PyPDF package.

See documentation at
https://pyfpdf.readthedocs.io/en/latest/index.html

git clone https://github.com/reingart/pyfpdf.git
sudo python3 setup.py install

"""

from fpdf import FPDF

pdf = FPDF()
pdf.add_page(orientation='L', format='A4')
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')

pdf.output('pyfpdf_output.pdf', 'F')

