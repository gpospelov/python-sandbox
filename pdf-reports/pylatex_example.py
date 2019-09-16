"""
Generation of PDF files using 'pylatex'
https://jeltef.github.io/PyLaTeX/current/index.html
"""

import pylatex as pl
from pylatex.utils import italic, NoEscape
from pylatex.utils import bold



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

def mono(s):
    return NoEscape(r'\texttt{' + s + '}')

def tiny(s):
    return NoEscape(r'\tiny{' + s + '}')


class PDFReport:
    def __init__(self):
        geometry_options = {"margin": "0.5in"}
        self.m_doc = pl.Document("pylatex_example", document_options="landscape",
                              geometry_options=geometry_options)
        self.fill_document()

    def fill_document(self):
        self.add_page1()
        self.add_page2()
        self.add_page3()

    def add_page1(self):
        doc = self.m_doc
        with doc.create(pl.Section('A section')):
            doc.append('Some regular text and some ')
            doc.append(italic('italic text. '))

            with doc.create(pl.Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image("meso.png", width=NoEscape(r'0.75\textwidth'))

        doc.append(pl.NewPage())

    def add_page2(self):
        doc = self.m_doc
        with doc.create(pl.Section('A section 2')):
            doc.append('Some regular text and some ')
            doc.append(italic('italic text. '))

            with doc.create(pl.Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image("meso.png", width=NoEscape(r'0.75\textwidth'))

        doc.append(pl.NewPage())

    def add_page3(self):
        doc = self.m_doc
        doc.append("Influence of mesocrystal height")
        doc.append(pl.VerticalSpace("2cm"))
        doc.append("\n")
        with doc.create(pl.MiniPage(width=r"0.2\textwidth", height=r"0.25\textwidth", content_pos='t')):
            lines = data.split("\n")
            with doc.create(pl.Tabular('l l', row_height=0.8)) as table:
                myfont = [mono, tiny]
                for l in lines:
                    parts = l.split(":")
                    print(parts)
                    if len(parts) == 2:
                        table.add_row(parts[0], parts[1], mapper=myfont)
                    elif len(parts) == 1:
                        table.add_hline()
                        table.add_row((l, " "), mapper=myfont)
            doc.append("\n")

        with doc.create(pl.MiniPage(width=r"0.8\textwidth", height=r"0.25\textwidth", content_pos='t')):
            doc.append(pl.Command('includegraphics', options='scale=0.8', arguments='meso.png'))
            doc.append("\n")

        doc.append(pl.NewPage())


    def generate_pdf(self):
        self.m_doc.generate_pdf(clean_tex=False)


if __name__ == '__main__':
    doc = PDFReport()
    doc.generate_pdf()


