"""
Generation of PDF files using 'pylatex'
https://jeltef.github.io/PyLaTeX/current/index.html
"""

from pylatex import Document, Section, Subsection, Command, Figure, NewPage, MiniPage, SubFigure, Tabular, SmallText
from pylatex.utils import italic, NoEscape


data = """
SimulationBuilder
m_beam_intensity               : 6.1e+12
m_beam_wavelength              : 0.1770
m_inclination_angle            : 0.4
m_time_spend                   : 0.65
SampleBuilderVer1
m_average_layer_thickness      : 200.0
m_roughness                    : 6.0
m_surface_filling_ratio        : 0.25
SingleMesoFactory
MesoCrystalBuilder
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
        geometry_options = {"margin": "0.55in"}
        self.m_doc = Document("pylatex_example", document_options="landscape",
                              geometry_options=geometry_options)
        self.fill_document()

    def fill_document(self):
        self.add_page1()
        self.add_page2()
        self.add_page3()

    def add_page1(self):
        doc = self.m_doc
        with doc.create(Section('A section')):
            doc.append('Some regular text and some ')
            doc.append(italic('italic text. '))

            with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image("meso.png", width=NoEscape(r'0.75\textwidth'))

        doc.append(NewPage())

    def add_page2(self):
        doc = self.m_doc
        with doc.create(Section('A section 2')):
            doc.append('Some regular text and some ')
            doc.append(italic('italic text. '))

            with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image("meso.png", width=NoEscape(r'0.75\textwidth'))

        doc.append(NewPage())

    def add_page3(self):
        doc = self.m_doc
        with doc.create(MiniPage(width=r"0.3\textwidth")):
            lines = data.split("\n")
            with doc.create(Tabular('l l')) as table:
                # doc.append(Command('smallsize'))
                table.add_hline()
                for l in lines:
                    parts = l.split(":")
                    print(parts)
                    if len(parts) == 2:
                        table.add_row(parts[0], parts[1])
                    else:
                        table.add_hline()
                        table.add_row((l, " "))

        with doc.create(MiniPage(width=r"0.6\textwidth")):
            doc.append(Command('includegraphics', options='scale=0.5', arguments='meso.png'))

        doc.append(NewPage())


    def generate_pdf(self):
        self.m_doc.generate_pdf(clean_tex=False)


if __name__ == '__main__':
    doc = PDFReport()
    doc.generate_pdf()


