import matplotlib
from pandas import DataFrame

from pylatex import Document, Figure, NoEscape, Section, Command

matplotlib.use("Agg")  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa


def FromClass(fname: str, cls, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options, default_filepath="latex_reports")

    doc.preamble.append(Command("title", "Análisis Sísmico"))
    doc.preamble.append(Command("author", "Anonymous author"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))

    with doc.create(Section("Introducción")):
        doc.append(
            """
            Vamos a realizar un análisis de los terremotos registrados en estas coordenadas: {}N {}W y {}N {}W.
            Para ello, vamos a extraerlos de la página web del Instituto Geográfico Nacional.
            """.format(cls.latMin, cls.longMin, cls.latMax, cls.longMax)
            )
        
        doc.append(
            """
            En primer lugar, vamos a visualizar un mapa de la zona que vamos a analizar
            """
        )

        with doc.create(Figure(position="H")) as plot_map:
            # Dibujo mapa
            pass
        
    with doc.create(Section("Análisis Dataset")) as seccion_dataset:

        doc.append(
            """
            Vamos a analizar un poco por encima el dataset.
            """
        )

        doc.append(
            """
            Columnas: {}
            """.format(cls.df.columnas)
        )

        doc.append(
            """
            Cabeza: {}
            """.format(cls.df.head())
        )

        doc.append(
            """
            Info: {}
            """.format(cls.df.info)
        )

    with doc.create(Section("Análisis Mapa")):

        with doc.create(Figure(position="H")) as plot_map_eq:
            cls.plot_map_data()

        with doc.create(Figure(position="H")) as plot_map_fullanal:
            cls.plot_full_map_analysis()

        with doc.create(Figure(position="H")) as plot_mag_distr:
            cls.plot_mag_distribution()

        with doc.create(Figure(position="H")) as plot_mag_distr_rit:
            cls.plot_mag_distribution_ritcher_law()

        doc.append("Created using matplotlib.")


    doc.generate_pdf(clean_tex=False)


def FromLocal(fname: str, df: DataFrame, imgs: dict, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options, default_filepath="latex_reports")

    doc.preamble.append(Command("title", "Análisis Sísmico"))
    doc.preamble.append(Command("author", "Anonymous author"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))

    with doc.create(Section("Introducción")):
        doc.append(
            """
            Vamos a realizar un análisis de los terremotos registrados en estas coordenadas: {}N {}W y {}N {}W.
            Para ello, vamos a extraerlos de la página web del Instituto Geográfico Nacional.
            """.format(df.Latitud.min(), df.Longitud.min(), df.Latitud.max(), df.Longitud.max())
            )
        
        doc.append(
            """
            En primer lugar, vamos a visualizar un mapa de la zona que vamos a analizar
            """
        )

        with doc.create(Figure(position="H")) as plot_map:
            imgs['plot_map']
            pass
        
    with doc.create(Section("Análisis Dataset")) as seccion_dataset:

        doc.append(
            """
            Vamos a analizar un poco por encima el dataset.
            """
        )

        doc.append(
            """
            Columnas: {}
            """.format(df.columnas)
        )

        doc.append(
            """
            Cabeza: {}
            """.format(df.head())
        )

        doc.append(
            """
            Info: {}
            """.format(df.info)
        )

    with doc.create(Section("Análisis Mapa")):

        with doc.create(Figure(position="H")) as plot_map_eq:
            imgs['plot_map_data']

        with doc.create(Figure(position="H")) as plot_map_fullanal:
            imgs['plot_full_map_analysis']

        with doc.create(Figure(position="H")) as plot_mag_distr:
            imgs['plot_mag_distribution']

        with doc.create(Figure(position="H")) as plot_mag_distr_rit:
            imgs['plot_mag_distribution_ritcher_law']

        doc.append("Created using matplotlib.")


    doc.generate_pdf(clean_tex=False)