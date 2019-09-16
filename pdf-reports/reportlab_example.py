"""
Some "Hello world" exercises for PDF generation using 'reportlab'.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib import utils
from reportlab.platypus import Frame, Image
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

data = """
SimulationBuilder
m_beam_intensity               : 6.1e+12
m_beam_wavelength              : 0.1770
m_inclination_angle            : 0.4
m_time_spend                   : 0.65
---
SampleBuilderVer1
m_average_layer_thickness      : 200.0
m_roughness                    : 6.0
m_surface_filling_ratio        : 0.25
---
SingleMesoFactory
---
MesoCrystalBuilder
---
MesoParameters
m_lattice_length_a             : 12.45
m_lattice_length_c             : 31.0
m_meso_height                  : 200.0
m_meso_radius                  : 800.0
m_nanoparticle_radius          : 5.0
m_rotation_z                   : 0
m_sigma_lattice_length_a       : 0.5
m_sigma_meso_height            : 20.0
m_sigma_meso_radius            : 20.0
m_sigma_nanoparticle_radius    : 0.3
"""


class PDFReport:
    def __init__(self):
        self.m_page = landscape(A4)
        self.m_canvas = canvas.Canvas("reportlab_output.pdf", pagesize=self.m_page)
        self.m_width = self.m_page[0]
        self.m_height = self.m_page[1]
        self.create_pages()

    def get_image(self, path, width=1*cm):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))

    def draw_image(self, path, x, y, width):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        self.m_canvas.drawImage(path, x, y, width=width, height=(width*aspect))

    def create_pages(self):
        self.add_page1()
        self.add_page2()
        self.add_page3()
        self.add_page4()
        self.add_page5()

    def add_page1(self):
        w = self.m_width
        h = self.m_height
        self.m_canvas.drawString(1*cm, h-1*cm, "Hello World")
        self.m_canvas.drawImage("meso.png", w/4, h/4, width=w/2, height=w/2)
        self.m_canvas.showPage()

    def add_page2(self):
        w = self.m_width
        h = self.m_height
        self.m_canvas.drawString(1*cm, h-1*cm, "Hello World")
        self.m_canvas.drawImage("meso.png", w/4, h/4, width=w/2, preserveAspectRatio=True, anchor='sw')
        self.m_canvas.showPage()

    def add_page3(self):
        w = self.m_width
        h = self.m_height
        self.draw_image("meso.png", w/4, h/4, width=w/2)
        self.m_canvas.showPage()

    def add_page4(self):
        w = self.m_width
        h = self.m_height
        frame = Frame(w/4, h/4, w/2, h/2, showBoundary=1)
        story = []
        story.append(self.get_image('meso.png', width=w/2))
        frame.addFromList(story, self.m_canvas)
        self.m_canvas.showPage()

    def add_page5(self):
        w = self.m_width
        h = self.m_height
        frame = Frame(0, 0, w/4, h-4*cm, showBoundary=1)
        story = []
        styles = getSampleStyleSheet()
        style = styles["Code"]
        style.alignment = TA_LEFT

        lines = data.split("\n")
        for l in lines:
            story.append(Paragraph(l, style))

        frame.addFromList(story, self.m_canvas)
        self.m_canvas.showPage()


    def save(self):
        self.m_canvas.save()


def generate_report():
    pdf = PDFReport()
    pdf.save()


if __name__ == '__main__':
    generate_report()
