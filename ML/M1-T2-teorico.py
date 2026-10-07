import os

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


# ============================================================
# CONFIGURACIÓN
# ============================================================

OUTPUT_DIR = "pdf"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "M1-T2-Exploracion-Avanzada-de-Datos-Teorico.pdf"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# COLORES
# ============================================================

PRIMARY = colors.HexColor("#0f172a")
ACCENT = colors.HexColor("#0d9488")
TEXT = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748b")
LIGHT = colors.HexColor("#f8fafc")
BORDER = colors.HexColor("#cbd5e1")
WHITE = colors.white


# ============================================================
# CANVAS CON NUMERACIÓN
# ============================================================

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop(
            "doc_subtitle",
            "Módulo 1 - Material 2: Exploración Avanzada de Datos"
        )
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_decorations(total_pages)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):

        width, height = letter

        # Línea superior
        self.setStrokeColor(ACCENT)
        self.setLineWidth(2)
        self.line(54, height - 42, width - 54, height - 42)

        # Encabezado
        self.setFillColor(ACCENT)
        self.setFont("Helvetica-Bold", 9)
        self.drawString(54, height - 31, "CURSOS CC")

        self.setFillColor(MUTED)
        self.setFont("Helvetica", 8)
        self.drawRightString(
            width - 54,
            height - 31,
            self.doc_subtitle
        )

        # Pie
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.6)
        self.line(54, 39, width - 54, 39)

        self.setFillColor(MUTED)
        self.setFont("Helvetica", 7.5)
        self.drawString(
            54,
            25,
            "Material educativo • Módulo 1 - Material 2"
        )

        self.drawRightString(
            width - 54,
            25,
            f"Página {self._pageNumber} de {total_pages}"
        )


# ============================================================
# ESTILOS
# ============================================================

def get_common_styles():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ModuleTag",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=ACCENT,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=PRIMARY,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=MUTED,
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=PRIMARY,
            spaceBefore=12,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="H3Custom",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=ACCENT,
            spaceBefore=8,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=TEXT,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=TEXT,
            leftIndent=15,
            firstLineIndent=-7,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=10,
            textColor=PRIMARY,
            backColor=colors.HexColor("#f1f5f9"),
            borderColor=BORDER,
            borderWidth=0.5,
            borderPadding=7,
            spaceBefore=5,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=10,
            textColor=WHITE,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=TEXT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCellBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=PRIMARY,
        )
    )

    return styles


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def add_card(story, content, styles):

    table = Table(
        [[content]],
        colWidths=[504],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 8))


def bullet(text, styles):
    return Paragraph(f"• {text}", styles["BulletCustom"])


# ============================================================
# TABLA: PROCESO EDA
# ============================================================

def eda_process_table(styles):

    data = [
        [
            Paragraph("Etapa", styles["TableHeader"]),
            Paragraph("Qué se analiza", styles["TableHeader"]),
            Paragraph("Preguntas orientadoras", styles["TableHeader"]),
        ],
        [
            Paragraph("1. Conocer el dataset", styles["TableCellBold"]),
            Paragraph(
                "Filas, columnas, tipos de datos y estructura general.",
                styles["TableCell"]
            ),
            Paragraph(
                "¿Qué datos tenemos? ¿Cuántos registros existen?",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("2. Calidad de datos", styles["TableCellBold"]),
            Paragraph(
                "Valores faltantes, duplicados, inconsistencias y formatos.",
                styles["TableCell"]
            ),
            Paragraph(
                "¿Los datos están completos? ¿Hay errores evidentes?",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("3. Estadística descriptiva", styles["TableCellBold"]),
            Paragraph(
                "Media, mediana, desviación estándar, mínimos y máximos.",
                styles["TableCell"]
            ),
            Paragraph(
                "¿Cómo se distribuyen los valores?",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("4. Visualización", styles["TableCellBold"]),
            Paragraph(
                "Gráficos de distribución, relaciones y categorías.",
                styles["TableCell"]
            ),
            Paragraph(
                "¿Qué patrones podemos observar visualmente?",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("5. Relaciones", styles["TableCellBold"]),
            Paragraph(
                "Correlaciones y asociaciones entre variables.",
                styles["TableCell"]
            ),
            Paragraph(
                "¿Qué variables parecen estar relacionadas?",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[155, 165, 184],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    WHITE,
                    colors.HexColor("#f8fafc"),
                ]),
            ]
        )
    )

    return table


# ============================================================
# TABLA: VISUALIZACIONES
# ============================================================

def visualization_table(styles):

    data = [
        [
            Paragraph("Gráfico", styles["TableHeader"]),
            Paragraph("Uso principal", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
        ],
        [
            Paragraph("Histograma", styles["TableCellBold"]),
            Paragraph(
                "Analizar la distribución de una variable numérica.",
                styles["TableCell"]
            ),
            Paragraph(
                "Edad, ingresos, precio.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Boxplot", styles["TableCellBold"]),
            Paragraph(
                "Observar dispersión y posibles valores atípicos.",
                styles["TableCell"]
            ),
            Paragraph(
                "Ingresos por categoría.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Countplot", styles["TableCellBold"]),
            Paragraph(
                "Contar observaciones por categoría.",
                styles["TableCell"]
            ),
            Paragraph(
                "Clientes por tipo de plan.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Scatterplot", styles["TableCellBold"]),
            Paragraph(
                "Observar la relación entre dos variables numéricas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Edad e ingresos.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Heatmap", styles["TableCellBold"]),
            Paragraph(
                "Representar matrices de correlación.",
                styles["TableCell"]
            ),
            Paragraph(
                "Correlación entre variables numéricas.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[125, 200, 179],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    WHITE,
                    colors.HexColor("#f8fafc"),
                ]),
            ]
        )
    )

    return table


# ============================================================
# DOCUMENTO
# ============================================================

def build_pdf():

    styles = get_common_styles()

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54,
        title="Exploración Avanzada de Datos",
        author="Cursos CC",
    )

    story = []

    # --------------------------------------------------------
    # PORTADA / TÍTULO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "MÓDULO 1 · PIPELINE DE DATOS Y PREPARACIÓN PROFESIONAL",
            styles["ModuleTag"]
        )
    )

    story.append(
        Paragraph(
            "Exploración Avanzada de Datos (EDA)",
            styles["DocTitle"]
        )
    )

    story.append(
        Paragraph(
            "Material teórico — Pandas, Seaborn y YData Profiling",
            styles["DocSubtitle"]
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=ACCENT,
            spaceBefore=2,
            spaceAfter=14,
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Objetivo del material</b><br/>"
            "Comprender cómo realizar una Exploratory Data Analysis (EDA) "
            "para conocer la estructura, calidad, distribución y relaciones "
            "presentes en un conjunto de datos antes de construir modelos "
            "de Machine Learning.",
            styles["BodyCustom"]
        ),
        styles,
    )

    # --------------------------------------------------------
    # 1
    # --------------------------------------------------------

    story.append(
        Paragraph("1. ¿Qué es la Exploración de Datos?", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "La <b>Exploratory Data Analysis (EDA)</b>, o Exploración "
            "Exploratoria de Datos, es el proceso mediante el cual se "
            "investiga un conjunto de datos antes de utilizarlo para "
            "construir un modelo de Machine Learning.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "La EDA permite conocer qué información contiene el dataset, "
            "cómo están representadas las variables, qué problemas de "
            "calidad existen y qué patrones o relaciones pueden observarse.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "No se trata simplemente de generar gráficos. Una EDA debe "
            "ayudar a responder preguntas y tomar decisiones sobre las "
            "etapas posteriores del proyecto.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 2
    # --------------------------------------------------------

    story.append(
        Paragraph("2. Objetivos de una EDA", styles["H2Custom"])
    )

    for item in [
        "Comprender la estructura del conjunto de datos.",
        "Identificar variables numéricas y categóricas.",
        "Detectar valores faltantes.",
        "Detectar registros duplicados.",
        "Encontrar valores inesperados o inconsistentes.",
        "Analizar la distribución de las variables.",
        "Identificar posibles valores atípicos.",
        "Explorar relaciones entre variables.",
        "Detectar posibles problemas antes del modelado.",
        "Generar hipótesis que orienten el proyecto de Machine Learning.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # 3
    # --------------------------------------------------------

    story.append(
        Paragraph("3. EDA dentro de un proyecto de Machine Learning", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "La exploración de datos se encuentra principalmente en la "
            "fase de <b>Comprensión de los datos</b> de CRISP-DM, aunque "
            "sus resultados influyen en las fases posteriores.",
            styles["BodyCustom"]
        )
    )

    story.append(
        eda_process_table(styles)
    )

    story.append(Spacer(1, 8))

    # --------------------------------------------------------
    # 4
    # --------------------------------------------------------

    story.append(
        Paragraph("4. Primer contacto con un dataset", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Cuando se recibe un dataset, el primer paso no debería ser "
            "entrenar un modelo. Primero debemos conocer qué tenemos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Con <b>Pandas</b> podemos cargar y explorar rápidamente los datos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import pandas as pd<br/><br/>"
            "df = pd.read_csv('clientes.csv')<br/>"
            "print(df.head())",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La función <b>head()</b> permite observar las primeras filas "
            "del dataset y obtener una primera impresión de su contenido.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 5
    # --------------------------------------------------------

    story.append(
        Paragraph("5. Conocer la estructura del dataset", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "<b>shape</b> devuelve la cantidad de filas y columnas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "print(df.shape)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, si el resultado es <b>(1000, 8)</b>, significa "
            "que tenemos 1000 registros y 8 columnas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>info()</b> permite conocer los nombres de las columnas, "
            "cantidad de valores no nulos y tipos de datos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.info()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>columns</b> permite consultar los nombres de las columnas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "print(df.columns)",
            styles["CodeCustom"]
        )
    )

    # --------------------------------------------------------
    # 6
    # --------------------------------------------------------

    story.append(
        Paragraph("6. Tipos de variables", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Identificar correctamente el tipo de cada variable es "
            "fundamental para decidir qué análisis y transformaciones "
            "serán necesarios.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "<b>Numéricas:</b> edades, precios, cantidades, ingresos.",
        "<b>Categóricas:</b> ciudad, tipo de cliente, categoría.",
        "<b>Binarias:</b> sí/no, 0/1, abandono/no abandono.",
        "<b>Fechas:</b> fecha de compra, fecha de registro.",
        "<b>Texto:</b> comentarios, descripciones o mensajes.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Pandas puede mostrar los tipos mediante:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "print(df.dtypes)",
            styles["CodeCustom"]
        )
    )

    # --------------------------------------------------------
    # 7
    # --------------------------------------------------------

    story.append(
        Paragraph("7. Estadística descriptiva", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "La estadística descriptiva permite resumir las principales "
            "características de las variables numéricas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.describe()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Entre los valores que podemos encontrar se encuentran:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "<b>count:</b> cantidad de valores disponibles.",
        "<b>mean:</b> promedio.",
        "<b>std:</b> desviación estándar.",
        "<b>min:</b> valor mínimo.",
        "<b>25%:</b> primer cuartil.",
        "<b>50%:</b> mediana.",
        "<b>75%:</b> tercer cuartil.",
        "<b>max:</b> valor máximo.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "La estadística descriptiva no reemplaza la visualización. "
            "Ambas herramientas se complementan.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 8
    # --------------------------------------------------------

    story.append(
        Paragraph("8. Valores faltantes", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Un valor faltante aparece cuando una observación no posee "
            "información para una determinada variable.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Antes de decidir cómo tratarlos, debemos conocer su cantidad "
            "y distribución.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.isnull().sum()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "También podemos calcular el porcentaje de valores faltantes:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "porcentaje = df.isnull().mean() * 100<br/>"
            "print(porcentaje)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La EDA permite detectar el problema. La decisión sobre "
            "cómo imputar o eliminar esos valores corresponde a la "
            "etapa de preparación de datos.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 9
    # --------------------------------------------------------

    story.append(
        Paragraph("9. Registros duplicados", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Los registros duplicados pueden distorsionar análisis y "
            "modelos si representan accidentalmente la misma observación.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.duplicated().sum()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Encontrar duplicados no significa eliminarlos automáticamente. "
            "Primero debe determinarse si son realmente errores o si "
            "representan observaciones válidas.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 10
    # --------------------------------------------------------

    story.append(
        Paragraph("10. Distribuciones", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Una distribución muestra cómo se concentran los valores "
            "de una variable.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, al analizar la edad de clientes podemos encontrar "
            "una concentración entre determinados valores y pocos registros "
            "en los extremos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Las distribuciones ayudan a detectar:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "asimetrías;",
        "concentraciones de valores;",
        "rangos inesperados;",
        "valores extremos;",
        "posibles errores de carga.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # 11
    # --------------------------------------------------------

    story.append(
        Paragraph("11. Valores atípicos (Outliers)", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Un <b>outlier</b> es una observación que se encuentra "
            "muy alejada del comportamiento predominante de una variable.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Un valor atípico no necesariamente es un error. Puede "
            "representar una situación real e importante.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, si analizamos ingresos mensuales, una persona "
            "con ingresos muy superiores al resto puede ser un caso real.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por este motivo, los outliers deben investigarse antes "
            "de decidir eliminarlos.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 12
    # --------------------------------------------------------

    story.append(
        Paragraph("12. Visualización con Seaborn", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "<b>Seaborn</b> es una biblioteca de Python construida sobre "
            "Matplotlib que facilita la creación de visualizaciones "
            "estadísticas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import seaborn as sns<br/>"
            "import matplotlib.pyplot as plt",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La visualización permite detectar patrones que pueden ser "
            "difíciles de identificar observando únicamente una tabla.",
            styles["BodyCustom"]
        )
    )

    story.append(
        visualization_table(styles)
    )

    # --------------------------------------------------------
    # 13
    # --------------------------------------------------------

    story.append(
        Paragraph("13. Análisis univariado", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "El análisis univariado estudia una variable a la vez.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, podemos analizar la distribución de la edad "
            "de los clientes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "sns.histplot(data=df, x='edad', kde=True)<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    # --------------------------------------------------------
    # 14
    # --------------------------------------------------------

    story.append(
        Paragraph("14. Análisis bivariado", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "El análisis bivariado estudia la relación entre dos variables.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, podemos analizar la relación entre edad e ingresos:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "sns.scatterplot(data=df, x='edad', y='ingresos')<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "El objetivo no es afirmar automáticamente que una variable "
            "cause a la otra. Una relación observada no implica causalidad.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 15
    # --------------------------------------------------------

    story.append(
        Paragraph("15. Correlación", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "La correlación permite medir la intensidad y dirección de "
            "una relación lineal entre variables numéricas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "correlaciones = df.corr(numeric_only=True)<br/>"
            "print(correlaciones)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una correlación cercana a 1 indica una relación lineal "
            "positiva fuerte. Una cercana a -1 indica una relación "
            "lineal negativa fuerte. Una cercana a 0 indica poca "
            "relación lineal.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "La correlación no demuestra causalidad.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 16
    # --------------------------------------------------------

    story.append(
        Paragraph("16. Matriz de correlación y Heatmap", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Una matriz de correlación puede visualizarse mediante "
            "un mapa de calor o <b>heatmap</b>.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "corr = df.corr(numeric_only=True)<br/><br/>"
            "sns.heatmap(corr, annot=True, cmap='coolwarm')<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Este gráfico permite identificar rápidamente pares de "
            "variables que presentan relaciones lineales fuertes.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 17
    # --------------------------------------------------------

    story.append(
        Paragraph("17. YData Profiling", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "<b>YData Profiling</b> permite generar automáticamente "
            "un informe exploratorio de un dataset.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "La herramienta resume información estadística, tipos de "
            "variables, valores faltantes, distribuciones, correlaciones "
            "y posibles advertencias.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Instalación:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "pip install ydata-profiling",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Uso básico:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from ydata_profiling import ProfileReport<br/><br/>"
            "profile = ProfileReport(df, title='Reporte EDA')<br/>"
            "profile.to_file('reporte_eda.html')",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "El informe generado puede abrirse en un navegador y utilizarse "
            "como apoyo para analizar el dataset.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 18
    # --------------------------------------------------------

    story.append(
        Paragraph("18. Ventajas y límites de la automatización", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Las herramientas automáticas son útiles para acelerar el "
            "diagnóstico inicial, pero no sustituyen el análisis humano.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "<b>Ventaja:</b> permiten revisar rápidamente muchas variables.",
        "<b>Ventaja:</b> detectan posibles problemas de calidad.",
        "<b>Ventaja:</b> facilitan la generación de estadísticas y gráficos.",
        "<b>Límite:</b> no conocen el contexto del problema de negocio.",
        "<b>Límite:</b> una advertencia automática debe ser interpretada.",
        "<b>Límite:</b> no todas las correlaciones tienen valor práctico.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # 19
    # --------------------------------------------------------

    story.append(
        Paragraph("19. EDA y toma de decisiones", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "El resultado más importante de una EDA no es el gráfico "
            "en sí mismo, sino la decisión que puede fundamentarse "
            "a partir de él.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Ejemplo</b><br/><br/>"
            "Si observamos que una variable tiene un 45 % de valores "
            "faltantes, no basta con registrar el porcentaje. Debemos "
            "preguntarnos por qué ocurre, si la variable es importante "
            "y qué estrategia será adecuada para tratarla.",
            styles["BodyCustom"]
        ),
        styles,
    )

    # --------------------------------------------------------
    # 20
    # --------------------------------------------------------

    story.append(
        Paragraph("20. Buenas prácticas para una EDA profesional", styles["H2Custom"])
    )

    for item in [
        "No comenzar el modelado sin conocer los datos.",
        "Documentar las decisiones tomadas durante la exploración.",
        "Combinar análisis estadístico y visualización.",
        "No eliminar datos automáticamente sin investigar su significado.",
        "Distinguir entre problemas reales y comportamientos válidos.",
        "Analizar las variables en relación con el problema de negocio.",
        "Evitar conclusiones causales a partir de simples correlaciones.",
        "Repetir la exploración cuando se incorporen nuevos datos.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # 21
    # --------------------------------------------------------

    story.append(
        Paragraph("21. Ejemplo de flujo EDA con Pandas y Seaborn", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "Un flujo inicial podría ser:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import pandas as pd<br/>"
            "import seaborn as sns<br/>"
            "import matplotlib.pyplot as plt<br/><br/>"
            "df = pd.read_csv('clientes.csv')<br/><br/>"
            "print(df.head())<br/>"
            "print(df.shape)<br/>"
            "df.info()<br/>"
            "print(df.describe())<br/>"
            "print(df.isnull().sum())<br/>"
            "print(df.duplicated().sum())<br/><br/>"
            "sns.histplot(data=df, x='edad', kde=True)<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Este código no constituye una EDA completa, pero muestra "
            "una secuencia inicial de inspección.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # 22
    # --------------------------------------------------------

    story.append(
        Paragraph("22. Relación entre EDA y preparación de datos", styles["H2Custom"])
    )

    story.append(
        Paragraph(
            "La EDA permite descubrir problemas que posteriormente deberán "
            "resolverse durante la preparación de los datos.",
            styles["BodyCustom"]
        )
    )

    data = [
        [
            Paragraph("Hallazgo en EDA", styles["TableHeader"]),
            Paragraph("Posible acción posterior", styles["TableHeader"]),
        ],
        [
            Paragraph("Valores faltantes", styles["TableCellBold"]),
            Paragraph("Imputación o eliminación justificada.", styles["TableCell"]),
        ],
        [
            Paragraph("Variables categóricas", styles["TableCellBold"]),
            Paragraph("Codificación adecuada.", styles["TableCell"]),
        ],
        [
            Paragraph("Escalas muy diferentes", styles["TableCellBold"]),
            Paragraph("Escalado cuando el algoritmo lo requiera.", styles["TableCell"]),
        ],
        [
            Paragraph("Outliers", styles["TableCellBold"]),
            Paragraph("Investigar, transformar o tratar según contexto.", styles["TableCell"]),
        ],
        [
            Paragraph("Clases desbalanceadas", styles["TableCellBold"]),
            Paragraph("Aplicar estrategias específicas de balanceo.", styles["TableCell"]),
        ],
    ]

    table = Table(
        data,
        colWidths=[210, 294],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    WHITE,
                    colors.HexColor("#f8fafc"),
                ]),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------------
    # 23
    # --------------------------------------------------------

    story.append(
        Paragraph("23. Idea central", styles["H2Custom"])
    )

    add_card(
        story,
        Paragraph(
            "<b>Una buena EDA permite conocer los datos antes de pedirles "
            "que aprendan algo.</b><br/><br/>"
            "El objetivo es transformar un conjunto de datos desconocido "
            "en información comprensible que permita tomar decisiones "
            "fundamentadas durante el proyecto de Machine Learning.",
            styles["BodyCustom"]
        ),
        styles,
    )

    # --------------------------------------------------------
    # 24
    # --------------------------------------------------------

    story.append(
        Paragraph("24. Glosario", styles["H2Custom"])
    )

    glossary = [
        ("EDA", "Exploratory Data Analysis o análisis exploratorio de datos."),
        ("Dataset", "Conjunto estructurado de datos."),
        ("Feature", "Variable utilizada como entrada para un modelo."),
        ("Target", "Variable que el modelo intenta predecir."),
        ("Outlier", "Observación alejada del comportamiento habitual."),
        ("Correlación", "Medida de asociación lineal entre variables."),
        ("Distribución", "Forma en que se concentran los valores."),
        ("Pandas", "Biblioteca de Python para manipulación y análisis de datos."),
        ("Seaborn", "Biblioteca de Python para visualización estadística."),
        ("YData Profiling", "Herramienta para generar informes automáticos de exploración."),
    ]

    data = [
        [
            Paragraph("Concepto", styles["TableHeader"]),
            Paragraph("Definición", styles["TableHeader"]),
        ]
    ]

    for term, definition in glossary:
        data.append(
            [
                Paragraph(term, styles["TableCellBold"]),
                Paragraph(definition, styles["TableCell"]),
            ]
        )

    table = Table(
        data,
        colWidths=[145, 359],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    WHITE,
                    colors.HexColor("#f8fafc"),
                ]),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------------
    # GENERAR
    # --------------------------------------------------------

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            doc_subtitle="Módulo 1 - Material 2: Exploración Avanzada de Datos",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()