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
    "M1-T2-Exploracion-Avanzada-de-Datos-Actividades.pdf"
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
# CANVAS
# ============================================================

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop(
            "doc_subtitle",
            "Módulo 1 - Material 2: Actividades"
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

        self.setStrokeColor(ACCENT)
        self.setLineWidth(2)
        self.line(54, height - 42, width - 54, height - 42)

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

def add_card(story, content):

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


def activity_title(story, number, title, styles):

    story.append(
        Paragraph(
            f"Actividad {number}. {title}",
            styles["H2Custom"]
        )
    )


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
        title="Actividades - Exploración Avanzada de Datos",
        author="Cursos CC",
    )

    story = []

    # --------------------------------------------------------
    # TÍTULO
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
            "Actividades prácticas — Pandas, Seaborn y YData Profiling",
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
            "<b>Propósito</b><br/>"
            "Aplicar técnicas de Exploratory Data Analysis para conocer "
            "la estructura, calidad, distribución y relaciones presentes "
            "en un conjunto de datos antes del modelado.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 1
    # --------------------------------------------------------

    activity_title(
        story,
        1,
        "Reconocer un dataset",
        styles
    )

    story.append(
        Paragraph(
            "Observa el siguiente conjunto de datos hipotético:",
            styles["BodyCustom"]
        )
    )

    data = [
        [
            Paragraph("Edad", styles["TableHeader"]),
            Paragraph("Ingresos", styles["TableHeader"]),
            Paragraph("Ciudad", styles["TableHeader"]),
            Paragraph("Plan", styles["TableHeader"]),
            Paragraph("Abandono", styles["TableHeader"]),
        ],
        ["22", "$25000", "Montevideo", "Básico", "No"],
        ["35", "$52000", "Canelones", "Premium", "No"],
        ["41", "$61000", "Montevideo", "Premium", "Sí"],
        ["29", "$33000", "Salto", "Básico", "No"],
        ["52", "$72000", "Montevideo", "Premium", "Sí"],
    ]

    table = Table(
        data,
        colWidths=[70, 100, 130, 100, 104],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 8))

    for item in [
        "¿Cuántas variables contiene el dataset?",
        "¿Cuáles son numéricas?",
        "¿Cuáles son categóricas?",
        "¿Cuál podría ser la variable objetivo?",
        "¿Qué variables podrían utilizarse como características?",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD 2
    # --------------------------------------------------------

    activity_title(
        story,
        2,
        "Primer diagnóstico con Pandas",
        styles
    )

    story.append(
        Paragraph(
            "Crea un archivo Python y carga un dataset utilizando Pandas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Realiza las siguientes operaciones:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Mostrar las primeras cinco filas.",
        "Mostrar la cantidad de filas y columnas.",
        "Mostrar los nombres de las columnas.",
        "Mostrar los tipos de datos.",
        "Mostrar información general del dataset.",
        "Mostrar estadísticas descriptivas.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Código de referencia:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import pandas as pd<br/><br/>"
            "df = pd.read_csv('dataset.csv')<br/><br/>"
            "print(df.head())<br/>"
            "print(df.shape)<br/>"
            "print(df.columns)<br/>"
            "print(df.dtypes)<br/>"
            "df.info()<br/>"
            "print(df.describe())",
            styles["CodeCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 3
    # --------------------------------------------------------

    activity_title(
        story,
        3,
        "Detectar problemas de calidad",
        styles
    )

    story.append(
        Paragraph(
            "Utilizando el mismo dataset, investiga:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "¿Cuántos valores faltantes existen por columna?",
        "¿Qué porcentaje de valores faltantes tiene cada variable?",
        "¿Existen registros duplicados?",
        "¿Hay variables con tipos de datos incorrectos?",
        "¿Existen valores imposibles o sospechosos?",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Utiliza como mínimo:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.isnull().sum()<br/>"
            "df.duplicated().sum()<br/>"
            "df.info()",
            styles["CodeCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 4
    # --------------------------------------------------------

    activity_title(
        story,
        4,
        "Estadística descriptiva",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona tres variables numéricas de tu dataset y analiza "
            "sus estadísticas descriptivas.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "¿Cuál es el promedio?",
        "¿Cuál es la mediana?",
        "¿Cuál es el valor mínimo?",
        "¿Cuál es el valor máximo?",
        "¿Existe una diferencia importante entre media y mediana?",
        "¿Qué podría indicar esa diferencia?",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD 5
    # --------------------------------------------------------

    activity_title(
        story,
        5,
        "Análisis de distribuciones",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona una variable numérica y construye un histograma "
            "utilizando Seaborn.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import seaborn as sns<br/>"
            "import matplotlib.pyplot as plt<br/><br/>"
            "sns.histplot(data=df, x='variable', kde=True)<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Luego responde:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "¿Dónde se concentra la mayor cantidad de observaciones?",
        "¿La distribución parece simétrica?",
        "¿Se observan valores extremos?",
        "¿Hay algo que resulte inesperado?",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD 6
    # --------------------------------------------------------

    activity_title(
        story,
        6,
        "Detectar posibles outliers",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona una variable numérica y construye un boxplot.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "sns.boxplot(data=df, x='variable')<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Identifica si existen observaciones alejadas del resto.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Importante:</b> no elimines los outliers. En esta actividad "
            "solo debes identificarlos y formular una posible explicación.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 7
    # --------------------------------------------------------

    activity_title(
        story,
        7,
        "Análisis de variables categóricas",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona una variable categórica y analiza la cantidad "
            "de observaciones de cada categoría.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "sns.countplot(data=df, x='categoria')<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    for item in [
        "¿Cuál es la categoría más frecuente?",
        "¿Cuál es la menos frecuente?",
        "¿Las categorías están equilibradas?",
        "¿Podría existir un problema de desbalance?",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD 8
    # --------------------------------------------------------

    activity_title(
        story,
        8,
        "Explorar relaciones entre variables",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona dos variables numéricas y crea un scatterplot.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "sns.scatterplot(data=df, x='variable_1', y='variable_2')<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    for item in [
        "¿Parece existir alguna relación?",
        "¿La relación parece positiva o negativa?",
        "¿Existen grupos de observaciones?",
        "¿Hay valores que se alejan del patrón general?",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD 9
    # --------------------------------------------------------

    activity_title(
        story,
        9,
        "Matriz de correlación",
        styles
    )

    story.append(
        Paragraph(
            "Calcula la matriz de correlación de las variables numéricas "
            "y represéntala mediante un heatmap.",
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
            "Selecciona dos relaciones que te llamen la atención y "
            "explica qué significan.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 10
    # --------------------------------------------------------

    activity_title(
        story,
        10,
        "Generar un informe automático con YData Profiling",
        styles
    )

    story.append(
        Paragraph(
            "Instala la biblioteca si aún no está disponible:",
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
            "Luego genera un informe:",
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
            "Abre el archivo HTML y compara los resultados automáticos "
            "con el análisis realizado manualmente.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 11
    # --------------------------------------------------------

    activity_title(
        story,
        11,
        "Interpretar, no solamente ejecutar",
        styles
    )

    story.append(
        Paragraph(
            "Una herramienta de análisis puede producir muchos resultados. "
            "El objetivo de esta actividad es aprender a interpretarlos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Para tres hallazgos encontrados durante la EDA, completa:",
            styles["BodyCustom"]
        )
    )

    data = [
        [
            Paragraph("Hallazgo", styles["TableHeader"]),
            Paragraph("Evidencia", styles["TableHeader"]),
            Paragraph("Interpretación", styles["TableHeader"]),
            Paragraph("Acción posible", styles["TableHeader"]),
        ],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
    ]

    table = Table(
        data,
        colWidths=[120, 125, 135, 124],
        rowHeights=[30, 65, 65, 65],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------------
    # ACTIVIDAD 12
    # --------------------------------------------------------

    activity_title(
        story,
        12,
        "EDA de un dataset de clientes",
        styles
    )

    story.append(
        Paragraph(
            "Realiza una exploración completa sobre un dataset de clientes "
            "o usuarios.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Tu análisis debe incluir como mínimo:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Descripción del dataset.",
        "Cantidad de filas y columnas.",
        "Tipos de variables.",
        "Estadísticas descriptivas.",
        "Valores faltantes.",
        "Duplicados.",
        "Al menos un histograma.",
        "Al menos un boxplot.",
        "Al menos un gráfico categórico.",
        "Al menos un scatterplot.",
        "Matriz de correlación.",
        "Informe de YData Profiling.",
        "Cinco conclusiones relevantes.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # ACTIVIDAD INTEGRADORA
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad Integradora — Informe EDA profesional",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Consigna</b><br/><br/>"
            "Selecciona un dataset relacionado con un problema que pueda "
            "abordarse mediante Machine Learning. Realiza una Exploración "
            "Exploratoria de Datos completa y presenta un informe que "
            "permita comprender el estado del dataset antes del modelado.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "El informe debe contener:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "1. Descripción del problema y del dataset.",
        "2. Cantidad de registros y variables.",
        "3. Identificación de tipos de datos.",
        "4. Análisis de valores faltantes.",
        "5. Análisis de duplicados.",
        "6. Estadística descriptiva.",
        "7. Análisis de distribuciones.",
        "8. Identificación de posibles outliers.",
        "9. Análisis de variables categóricas.",
        "10. Análisis de relaciones entre variables.",
        "11. Matriz de correlación.",
        "12. Informe generado con YData Profiling.",
        "13. Principales hallazgos.",
        "14. Problemas que deberían resolverse antes del modelado.",
    ]:
        story.append(bullet(item, styles))

    # --------------------------------------------------------
    # AUTOEVALUACIÓN
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Autoevaluación",
            styles["H2Custom"]
        )
    )

    questions = [
        (
            "1. ¿Qué significa EDA?",
            "Exploratory Data Analysis o análisis exploratorio de datos."
        ),
        (
            "2. ¿Para qué sirve df.info()?",
            "Para conocer estructura, columnas, valores no nulos y tipos de datos."
        ),
        (
            "3. ¿Qué devuelve df.shape?",
            "Una tupla con cantidad de filas y columnas."
        ),
        (
            "4. ¿Qué permite observar un histograma?",
            "La distribución de una variable numérica."
        ),
        (
            "5. ¿Para qué sirve un boxplot?",
            "Para analizar distribución, dispersión y posibles valores atípicos."
        ),
        (
            "6. ¿Qué representa una correlación cercana a 1?",
            "Una relación lineal positiva fuerte."
        ),
        (
            "7. ¿Una correlación demuestra causalidad?",
            "No. Correlación y causalidad son conceptos diferentes."
        ),
        (
            "8. ¿Para qué sirve YData Profiling?",
            "Para generar un informe automatizado de exploración de datos."
        ),
    ]

    for question, answer in questions:

        story.append(
            Paragraph(
                f"<b>{question}</b>",
                styles["BodyCustom"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Respuesta:</b> {answer}",
                styles["BodyCustom"]
            )
        )

    # --------------------------------------------------------
    # CIERRE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Cierre",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Idea clave:</b><br/><br/>"
            "Antes de entrenar un modelo de Machine Learning debemos "
            "comprender los datos con los que vamos a trabajar. "
            "La EDA permite transformar un dataset desconocido en "
            "información que puede ser analizada y utilizada para "
            "tomar decisiones fundamentadas.",
            styles["BodyCustom"]
        )
    )

    # --------------------------------------------------------
    # GENERAR PDF
    # --------------------------------------------------------

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            doc_subtitle="Módulo 1 - Material 2: Actividades",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()