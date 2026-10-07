import os

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
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
    "M1-T4-Ingenieria-de-Caracteristicas-Teorico.pdf"
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
            "Módulo 1 - Material 4: Ingeniería de Características"
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
            "Material educativo • Módulo 1 - Material 4"
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
    return Paragraph(
        f"• {text}",
        styles["BulletCustom"]
    )


# ============================================================
# TABLA DE TIPOS DE VARIABLES
# ============================================================

def variables_table(styles):

    data = [
        [
            Paragraph("Tipo", styles["TableHeader"]),
            Paragraph("Descripción", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
        ],
        [
            Paragraph("Numérica", styles["TableCellBold"]),
            Paragraph(
                "Representa cantidades o medidas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Edad, ingresos, temperatura.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Categórica", styles["TableCellBold"]),
            Paragraph(
                "Representa categorías sin orden numérico.",
                styles["TableCell"]
            ),
            Paragraph(
                "Ciudad, color, tipo de cliente.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Ordinal", styles["TableCellBold"]),
            Paragraph(
                "Categorías que poseen un orden.",
                styles["TableCell"]
            ),
            Paragraph(
                "Bajo, medio, alto.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Temporal", styles["TableCellBold"]),
            Paragraph(
                "Representa fechas u horas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Fecha de compra.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Texto", styles["TableCellBold"]),
            Paragraph(
                "Contiene información textual.",
                styles["TableCell"]
            ),
            Paragraph(
                "Comentarios, reseñas.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[110, 210, 184],
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

    return table


# ============================================================
# TABLA DE CODIFICACIÓN
# ============================================================

def encoding_table(styles):

    data = [
        [
            Paragraph("Método", styles["TableHeader"]),
            Paragraph("Uso", styles["TableHeader"]),
            Paragraph("Resultado", styles["TableHeader"]),
        ],
        [
            Paragraph("One-Hot Encoding", styles["TableCellBold"]),
            Paragraph(
                "Variables categóricas nominales.",
                styles["TableCell"]
            ),
            Paragraph(
                "Una columna por categoría.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Ordinal Encoding", styles["TableCellBold"]),
            Paragraph(
                "Categorías con orden.",
                styles["TableCell"]
            ),
            Paragraph(
                "Cada categoría recibe un valor ordenado.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Label Encoding", styles["TableCellBold"]),
            Paragraph(
                "Habitualmente utilizado para representar etiquetas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Cada categoría recibe un número.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[130, 185, 189],
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

    return table


# ============================================================
# TABLA DE ESCALADO
# ============================================================

def scaling_table(styles):

    data = [
        [
            Paragraph("Método", styles["TableHeader"]),
            Paragraph("Característica", styles["TableHeader"]),
            Paragraph("Cuándo utilizarlo", styles["TableHeader"]),
        ],
        [
            Paragraph("StandardScaler", styles["TableCellBold"]),
            Paragraph(
                "Media 0 y desviación estándar 1.",
                styles["TableCell"]
            ),
            Paragraph(
                "Modelos sensibles a la escala.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("MinMaxScaler", styles["TableCellBold"]),
            Paragraph(
                "Transforma normalmente al rango 0–1.",
                styles["TableCell"]
            ),
            Paragraph(
                "Cuando interesa un rango definido.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("RobustScaler", styles["TableCellBold"]),
            Paragraph(
                "Utiliza estadísticas robustas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Cuando existen outliers.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[125, 190, 189],
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
        title="Ingeniería de Características",
        author="Cursos CC",
    )

    story = []

    # ========================================================
    # PORTADA / INTRODUCCIÓN
    # ========================================================

    story.append(
        Paragraph(
            "MÓDULO 1 · PIPELINE DE DATOS Y PREPARACIÓN PROFESIONAL",
            styles["ModuleTag"]
        )
    )

    story.append(
        Paragraph(
            "Ingeniería de Características",
            styles["DocTitle"]
        )
    )

    story.append(
        Paragraph(
            "Material teórico — Feature Engineering, codificación y escalado",
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
            "Comprender cómo transformar los datos originales en "
            "características útiles para un modelo de Machine Learning, "
            "aplicando técnicas de codificación, escalado, transformación "
            "y creación de nuevas variables.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 1
    # ========================================================

    story.append(
        Paragraph(
            "1. ¿Qué es Feature Engineering?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La <b>Ingeniería de Características</b> o "
            "<b>Feature Engineering</b> es el proceso de transformar "
            "los datos disponibles para construir variables que permitan "
            "a un modelo de Machine Learning aprender de manera más efectiva.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una característica o <i>feature</i> es una variable utilizada "
            "como entrada de un modelo.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Idea central</b><br/><br/>"
            "Los modelos no comprenden directamente el significado de "
            "conceptos como 'cliente Premium', 'lunes' o 'alto nivel de "
            "ingresos'. Debemos representar esa información de una forma "
            "que el algoritmo pueda procesar.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 2
    # ========================================================

    story.append(
        Paragraph(
            "2. ¿Por qué es importante?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La calidad de las características puede tener un impacto "
            "significativo en el rendimiento de un modelo.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Permite representar mejor el problema.",
        "Facilita que el modelo encuentre patrones.",
        "Puede mejorar el rendimiento predictivo.",
        "Puede reducir ruido o información irrelevante.",
        "Puede hacer más interpretables los resultados.",
        "Puede reducir la cantidad de variables necesarias.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 3
    # ========================================================

    story.append(
        Paragraph(
            "3. Variables originales y variables derivadas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una variable original es aquella que proviene directamente "
            "de la fuente de datos. Una variable derivada se construye "
            "a partir de una o más variables existentes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, si tenemos:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "fecha_nacimiento<br/>"
            "fecha_actual",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "podemos crear:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "edad = fecha_actual - fecha_nacimiento",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La nueva variable puede resultar más útil para el modelo "
            "que las fechas originales.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 4
    # ========================================================

    story.append(
        Paragraph(
            "4. Tipos de variables",
            styles["H2Custom"]
        )
    )

    story.append(
        variables_table(styles)
    )

    # ========================================================
    # 5
    # ========================================================

    story.append(
        Paragraph(
            "5. Codificación de variables categóricas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Muchos algoritmos de Machine Learning trabajan con valores "
            "numéricos. Por este motivo, las variables categóricas suelen "
            "necesitar una transformación.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        encoding_table(styles)
    )

    # ========================================================
    # 6
    # ========================================================

    story.append(
        Paragraph(
            "6. One-Hot Encoding",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Supongamos una variable llamada <b>ciudad</b>:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Montevideo<br/>"
            "Canelones<br/>"
            "Maldonado",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "One-Hot Encoding puede generar una columna para cada categoría:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "ciudad_Montevideo<br/>"
            "ciudad_Canelones<br/>"
            "ciudad_Maldonado",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Una observación tendrá 1 en la categoría correspondiente "
            "y 0 en las demás.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "En Scikit-learn:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.preprocessing import OneHotEncoder<br/><br/>"
            "encoder = OneHotEncoder(handle_unknown='ignore')<br/>"
            "X_encoded = encoder.fit_transform(X)",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 7
    # ========================================================

    story.append(
        Paragraph(
            "7. Ordinal Encoding",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Cuando las categorías tienen un orden natural, puede utilizarse "
            "una codificación ordinal.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Bajo → 1<br/>"
            "Medio → 2<br/>"
            "Alto → 3",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Esta representación es adecuada cuando el orden tiene "
            "significado real.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "No debe utilizarse indiscriminadamente para categorías "
            "nominales como colores o ciudades, porque podría introducir "
            "un orden que no existe.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 8
    # ========================================================

    story.append(
        Paragraph(
            "8. Label Encoding",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Label Encoding asigna un número a cada categoría. "
            "Es especialmente habitual para representar la variable "
            "objetivo cuando las clases son categóricas.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.preprocessing import LabelEncoder<br/><br/>"
            "encoder = LabelEncoder()<br/>"
            "y_encoded = encoder.fit_transform(y)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Debe utilizarse con cuidado sobre variables de entrada, "
            "porque asignar números puede generar una relación de orden "
            "artificial entre categorías.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 9
    # ========================================================

    story.append(
        Paragraph(
            "9. Escalado de variables",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "El escalado transforma las variables numéricas para que "
            "tengan magnitudes comparables.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Esto es especialmente importante para algoritmos que utilizan "
            "distancias o son sensibles a la magnitud de las variables.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        scaling_table(styles)
    )

    # ========================================================
    # 10
    # ========================================================

    story.append(
        Paragraph(
            "10. StandardScaler",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "StandardScaler estandariza las variables utilizando su media "
            "y desviación estándar.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.preprocessing import StandardScaler<br/><br/>"
            "scaler = StandardScaler()<br/>"
            "X_scaled = scaler.fit_transform(X)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Después de la transformación, las variables suelen quedar "
            "centradas alrededor de 0.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 11
    # ========================================================

    story.append(
        Paragraph(
            "11. MinMaxScaler",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "MinMaxScaler transforma los valores para ubicarlos normalmente "
            "dentro de un intervalo entre 0 y 1.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.preprocessing import MinMaxScaler<br/><br/>"
            "scaler = MinMaxScaler()<br/>"
            "X_scaled = scaler.fit_transform(X)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Es útil cuando interesa trabajar con un rango definido, "
            "aunque puede verse afectado por valores extremos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 12
    # ========================================================

    story.append(
        Paragraph(
            "12. RobustScaler",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "RobustScaler utiliza estadísticas robustas como la mediana "
            "y el rango intercuartílico.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.preprocessing import RobustScaler<br/><br/>"
            "scaler = RobustScaler()<br/>"
            "X_scaled = scaler.fit_transform(X)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Puede ser una alternativa apropiada cuando existen valores "
            "atípicos importantes.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 13
    # ========================================================

    story.append(
        Paragraph(
            "13. Creación de nuevas variables",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una de las tareas más importantes de Feature Engineering "
            "consiste en crear variables que representen mejor el problema.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Por ejemplo, a partir de:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "ingresos<br/>"
            "cantidad_personas_hogar",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "podemos crear:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "ingreso_por_persona = ingresos / cantidad_personas_hogar",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La nueva característica puede representar mejor la capacidad "
            "económica relativa del hogar.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 14
    # ========================================================

    story.append(
        Paragraph(
            "14. Transformaciones matemáticas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Las transformaciones matemáticas pueden ayudar a representar "
            "mejor variables con distribuciones difíciles.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "df['log_ingresos'] = np.log1p(df['ingresos'])",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "La transformación logarítmica puede reducir el efecto "
            "de valores extremadamente grandes y disminuir la asimetría "
            "de algunas distribuciones.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Debe aplicarse solamente cuando tenga sentido para la variable "
            "y teniendo en cuenta sus posibles valores.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 15
    # ========================================================

    story.append(
        Paragraph(
            "15. Variables temporales",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una fecha completa puede contener mucha información que "
            "conviene separar en características independientes.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "df['fecha'] = pd.to_datetime(df['fecha'])<br/><br/>"
            "df['anio'] = df['fecha'].dt.year<br/>"
            "df['mes'] = df['fecha'].dt.month<br/>"
            "df['dia'] = df['fecha'].dt.day<br/>"
            "df['dia_semana'] = df['fecha'].dt.dayofweek",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "También pueden crearse variables como trimestre, fin de semana, "
            "hora del día o antigüedad desde una fecha determinada.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 16
    # ========================================================

    story.append(
        Paragraph(
            "16. Binning o discretización",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La discretización transforma una variable numérica continua "
            "en categorías o intervalos.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "df['grupo_edad'] = pd.cut(<br/>"
            "    df['edad'],<br/>"
            "    bins=[0, 18, 30, 50, 100],<br/>"
            "    labels=['Menor', 'Joven', 'Adulto', 'Mayor']<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Esta técnica puede ser útil cuando el significado del problema "
            "se expresa mejor mediante rangos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 17
    # ========================================================

    story.append(
        Paragraph(
            "17. Interacciones entre variables",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una interacción representa una relación combinada entre "
            "dos o más variables.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Por ejemplo:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "precio_por_m2 = precio / superficie",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "En otros problemas pueden crearse productos, razones, "
            "diferencias o combinaciones de variables.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 18
    # ========================================================

    story.append(
        Paragraph(
            "18. Variables altamente sesgadas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una variable sesgada presenta una distribución en la que "
            "los valores se concentran en una zona y existe una cola "
            "hacia valores más altos o más bajos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una transformación logarítmica puede ser útil en algunas "
            "variables positivas con fuerte asimetría.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "np.log1p(df['ingresos'])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La decisión debe comprobarse mediante análisis exploratorio "
            "y conocimiento del dominio.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 19
    # ========================================================

    story.append(
        Paragraph(
            "19. Feature Engineering y Data Leakage",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Las nuevas características también pueden generar "
            "<b>data leakage</b> si utilizan información que no estaría "
            "disponible en el momento real de realizar una predicción.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Ejemplo</b><br/><br/>"
            "Si queremos predecir si un cliente abandonará el servicio "
            "el próximo mes, no podemos utilizar una variable que registre "
            "una acción realizada después de ese abandono.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 20
    # ========================================================

    story.append(
        Paragraph(
            "20. Feature Engineering dentro de un Pipeline",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Las transformaciones deben integrarse al flujo de Machine "
            "Learning para evitar diferencias entre entrenamiento y "
            "predicción.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.pipeline import Pipeline<br/>"
            "from sklearn.preprocessing import StandardScaler<br/>"
            "from sklearn.impute import SimpleImputer<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "pipeline = Pipeline([<br/>"
            "    ('imputer', SimpleImputer(strategy='median')),<br/>"
            "    ('scaler', StandardScaler()),<br/>"
            "    ('model', LogisticRegression())<br/>"
            "])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "En proyectos con variables numéricas y categóricas diferentes "
            "puede utilizarse <b>ColumnTransformer</b> para aplicar "
            "transformaciones específicas a cada grupo.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 21
    # ========================================================

    story.append(
        Paragraph(
            "21. ColumnTransformer",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "ColumnTransformer permite definir diferentes transformaciones "
            "para diferentes columnas.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.compose import ColumnTransformer<br/>"
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler<br/><br/>"
            "preprocessor = ColumnTransformer([<br/>"
            "    ('num', StandardScaler(), columnas_numericas),<br/>"
            "    ('cat', OneHotEncoder(handle_unknown='ignore'), columnas_categoricas)<br/>"
            "])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Esta estructura resulta especialmente útil en datasets "
            "reales donde conviven diferentes tipos de variables.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 22
    # ========================================================

    story.append(
        Paragraph(
            "22. Errores frecuentes",
            styles["H2Custom"]
        )
    )

    for item in [
        "Codificar todas las variables categóricas de la misma manera.",
        "Aplicar Label Encoding a categorías sin orden.",
        "Escalar antes de separar entrenamiento y prueba.",
        "Crear variables utilizando información futura.",
        "Generar demasiadas características sin evaluar su utilidad.",
        "No considerar el significado de las variables.",
        "Crear variables que duplican información existente.",
        "Ignorar valores atípicos y distribuciones.",
        "No reproducir las transformaciones en producción.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 23
    # ========================================================

    story.append(
        Paragraph(
            "23. Buenas prácticas profesionales",
            styles["H2Custom"]
        )
    )

    for item in [
        "Comprender el problema de negocio antes de crear variables.",
        "Analizar las variables mediante EDA.",
        "Documentar cada transformación.",
        "Separar entrenamiento y prueba antes de aprender parámetros.",
        "Utilizar Pipelines cuando sea posible.",
        "Evitar transformaciones arbitrarias.",
        "Comparar el rendimiento antes y después.",
        "Mantener solamente características justificadas.",
        "Verificar que las variables estén disponibles en producción.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 24
    # ========================================================

    story.append(
        Paragraph(
            "24. Caso práctico: predicción de abandono",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Supongamos que queremos predecir si un cliente abandonará "
            "un servicio.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Variables originales:",
            styles["BodyCustom"]
        )
    )    

    for item in [
        "edad",
        "ingresos",
        "fecha_alta",
        "cantidad_llamadas_soporte",
        "tipo_plan",
        "cantidad_meses",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Podemos crear:",
            styles["BodyCustom"]
        )
    )    

    for item in [
        "antiguedad_meses",
        "llamadas_por_mes",
        "ingreso_por_mes",
        "es_plan_premium",
        "cliente_mayor_50",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Estas nuevas variables pueden representar de forma más "
            "directa algunos factores relacionados con el abandono.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 25
    # ========================================================

    story.append(
        Paragraph(
            "25. Flujo profesional de Feature Engineering",
            styles["H2Custom"]
        )
    )

    for number, text in [
        ("1", "Comprender el problema."),
        ("2", "Explorar los datos."),
        ("3", "Identificar tipos de variables."),
        ("4", "Detectar problemas de calidad."),
        ("5", "Seleccionar transformaciones."),
        ("6", "Crear características relevantes."),
        ("7", "Codificar variables categóricas."),
        ("8", "Escalar cuando corresponda."),
        ("9", "Evitar data leakage."),
        ("10", "Evaluar el impacto de las características."),
        ("11", "Documentar el proceso."),
    ]:
        story.append(
            Paragraph(
                f"<b>{number}.</b> {text}",
                styles["BulletCustom"]
            )
        )

    # ========================================================
    # 26
    # ========================================================

    story.append(
        Paragraph(
            "26. Idea central",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Feature Engineering convierte datos en información útil "
            "para un modelo.</b><br/><br/>"
            "No consiste simplemente en crear muchas variables. "
            "Consiste en representar el problema de una forma que permita "
            "al algoritmo aprender patrones relevantes, evitando ruido, "
            "sesgos y fuga de información.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 27
    # ========================================================

    story.append(
        Paragraph(
            "27. Glosario",
            styles["H2Custom"]
        )
    )

    glossary = [
        (
            "Feature",
            "Característica o variable utilizada como entrada de un modelo."
        ),
        (
            "Feature Engineering",
            "Proceso de crear o transformar características para mejorar la representación del problema."
        ),
        (
            "One-Hot Encoding",
            "Transformación que representa categorías mediante columnas binarias."
        ),
        (
            "Label Encoding",
            "Asignación de números a categorías."
        ),
        (
            "Ordinal Encoding",
            "Codificación que conserva un orden significativo entre categorías."
        ),
        (
            "StandardScaler",
            "Transformación que estandariza las variables alrededor de una media 0."
        ),
        (
            "MinMaxScaler",
            "Transformación que lleva los valores a un rango definido."
        ),
        (
            "RobustScaler",
            "Escalador menos sensible a valores extremos."
        ),
        (
            "Data Leakage",
            "Uso de información que no debería estar disponible durante el entrenamiento."
        ),
        (
            "Pipeline",
            "Secuencia reproducible de transformaciones y modelado."
        ),
        (
            "ColumnTransformer",
            "Herramienta para aplicar transformaciones diferentes a grupos de columnas."
        ),
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

    # ========================================================
    # GENERAR
    # ========================================================

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            doc_subtitle="Módulo 1 - Material 4: Ingeniería de Características",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()