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
    "M1-T4-Ingenieria-de-Caracteristicas-Actividades.pdf"
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
            "Módulo 1 - Material 4: Actividades"
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
        title="Actividades - Ingeniería de Características",
        author="Cursos CC",
    )

    story = []

    # ========================================================
    # TÍTULO
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
            "Actividades prácticas — Feature Engineering, codificación y escalado",
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
            "Aplicar técnicas de Feature Engineering para transformar "
            "datos originales en características adecuadas para un modelo "
            "de Machine Learning.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 1
    # ========================================================

    activity_title(
        story,
        1,
        "Identificar tipos de variables",
        styles
    )

    story.append(
        Paragraph(
            "Clasifica las siguientes variables como numéricas, categóricas, "
            "ordinales, temporales o de texto.",
            styles["BodyCustom"]
        )
    )

    variables = [
        "edad",
        "ingresos",
        "ciudad",
        "tipo_plan",
        "nivel_satisfaccion",
        "fecha_compra",
        "comentario_cliente",
        "cantidad_productos",
        "estado_civil",
    ]

    for variable in variables:
        story.append(
            Paragraph(
                f"<b>{variable}</b> → __________________________",
                styles["BulletCustom"]
            )
        )

    # ========================================================
    # ACTIVIDAD 2
    # ========================================================

    activity_title(
        story,
        2,
        "Analizar una variable categórica",
        styles
    )

    story.append(
        Paragraph(
            "Considera la variable:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "tipo_plan = ['Básico', 'Premium', 'Básico', 'Estudiante', 'Premium']",
            styles["CodeCustom"]
        )
    )

    for item in [
        "¿Es una variable nominal u ordinal?",
        "¿Tiene sentido asignarle directamente 0, 1 y 2?",
        "¿Qué método de codificación utilizarías?",
        "¿Por qué?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 3
    # ========================================================

    activity_title(
        story,
        3,
        "Aplicar One-Hot Encoding",
        styles
    )

    story.append(
        Paragraph(
            "Crea un pequeño DataFrame:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import pandas as pd<br/><br/>"
            "df = pd.DataFrame({<br/>"
            "    'ciudad': ['Montevideo', 'Canelones', 'Maldonado', 'Montevideo']<br/>"
            "})",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Aplica OneHotEncoder:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.preprocessing import OneHotEncoder<br/><br/>"
            "encoder = OneHotEncoder(handle_unknown='ignore')<br/>"
            "resultado = encoder.fit_transform(df[['ciudad']])<br/>"
            "print(resultado.toarray())",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Responde: ¿cuántas columnas se generaron?",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 4
    # ========================================================

    activity_title(
        story,
        4,
        "Comparar codificaciones",
        styles
    )

    story.append(
        Paragraph(
            "Compara las siguientes situaciones:",
            styles["BodyCustom"]
        )
    )

    comparison = [
        [
            Paragraph("Variable", styles["TableHeader"]),
            Paragraph("Codificación sugerida", styles["TableHeader"]),
            Paragraph("Justificación", styles["TableHeader"]),
        ],
        [
            Paragraph("Color", styles["TableCell"]),
            "",
            "",
        ],
        [
            Paragraph("Nivel educativo", styles["TableCell"]),
            "",
            "",
        ],
        [
            Paragraph("Tipo de cliente", styles["TableCell"]),
            "",
            "",
        ],
        [
            Paragraph("Nivel de satisfacción: bajo/medio/alto", styles["TableCell"]),
            "",
            "",
        ],
    ]

    table = Table(
        comparison,
        colWidths=[190, 130, 184],
        rowHeights=[30, 55, 55, 55, 55],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    # ========================================================
    # ACTIVIDAD 5
    # ========================================================

    activity_title(
        story,
        5,
        "Aplicar StandardScaler",
        styles
    )

    story.append(
        Paragraph(
            "Crea un DataFrame con variables de escalas diferentes:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df = pd.DataFrame({<br/>"
            "    'edad': [20, 30, 40, 50],<br/>"
            "    'ingresos': [25000, 45000, 70000, 120000]<br/>"
            "})",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Aplica StandardScaler y compara los valores originales "
            "con los valores transformados.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.preprocessing import StandardScaler<br/><br/>"
            "scaler = StandardScaler()<br/>"
            "X_scaled = scaler.fit_transform(df)",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 6
    # ========================================================

    activity_title(
        story,
        6,
        "Comparar métodos de escalado",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza el mismo dataset y aplica:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "StandardScaler",
        "MinMaxScaler",
        "RobustScaler",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Observa cómo cambia la escala de las variables.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 7
    # ========================================================

    activity_title(
        story,
        7,
        "Crear una variable derivada",
        styles
    )

    story.append(
        Paragraph(
            "Supón que tienes las columnas:",
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
            "Crea:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "ingreso_por_persona",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Explica por qué esta característica podría aportar información "
            "diferente de las variables originales.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 8
    # ========================================================

    activity_title(
        story,
        8,
        "Crear variables temporales",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza el siguiente ejemplo:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df['fecha'] = pd.to_datetime(df['fecha'])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Crea las siguientes variables:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Año.",
        "Mes.",
        "Día.",
        "Día de la semana.",
        "Fin de semana.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Utiliza las propiedades de fecha de Pandas para realizarlo.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 9
    # ========================================================

    activity_title(
        story,
        9,
        "Discretizar una variable",
        styles
    )

    story.append(
        Paragraph(
            "Tienes una variable <b>edad</b>. Crea grupos:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "0–17: Menor.",
        "18–29: Joven.",
        "30–49: Adulto.",
        "50 o más: Mayor.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Puedes utilizar:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df['grupo_edad'] = pd.cut(<br/>"
            "    df['edad'],<br/>"
            "    bins=[0, 17, 29, 49, 100],<br/>"
            "    labels=['Menor', 'Joven', 'Adulto', 'Mayor']<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 10
    # ========================================================

    activity_title(
        story,
        10,
        "Transformar una variable sesgada",
        styles
    )

    story.append(
        Paragraph(
            "Considera una variable de ingresos con valores muy diferentes:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "25000, 27000, 30000, 32000, 35000, 40000, 450000",
            styles["CodeCustom"]
        )
    )

    for item in [
        "Calcula la media y la mediana.",
        "Identifica el valor extremo.",
        "Aplica una transformación logarítmica.",
        "Compara la distribución antes y después.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Puedes utilizar:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df['log_ingresos'] = np.log1p(df['ingresos'])",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 11
    # ========================================================

    activity_title(
        story,
        11,
        "Crear interacciones entre variables",
        styles
    )

    story.append(
        Paragraph(
            "A partir de:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "precio<br/>"
            "superficie",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "crea:",
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
            "Luego propone dos nuevas características que podrían ser "
            "útiles para el mismo problema.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 12
    # ========================================================

    activity_title(
        story,
        12,
        "Feature Engineering de un dataset",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona un dataset que contenga al menos:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Dos variables numéricas.",
        "Dos variables categóricas.",
        "Una variable temporal.",
        "Una variable objetivo.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Realiza las siguientes transformaciones:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Codifica las variables categóricas.",
        "Escala las variables numéricas.",
        "Extrae información de la fecha.",
        "Crea al menos dos variables derivadas.",
        "Evalúa si alguna variable necesita transformación.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 13
    # ========================================================

    activity_title(
        story,
        13,
        "Construir un Pipeline",
        styles
    )

    story.append(
        Paragraph(
            "Construye un pipeline que incluya al menos:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Imputación.",
        "Escalado de variables numéricas.",
        "Codificación de variables categóricas.",
        "Un modelo de Machine Learning.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Utiliza Pipeline y ColumnTransformer.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.compose import ColumnTransformer<br/>"
            "from sklearn.pipeline import Pipeline<br/>"
            "from sklearn.impute import SimpleImputer<br/>"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "preprocessor = ColumnTransformer([<br/>"
            "    ('num', Pipeline([<br/>"
            "        ('imputer', SimpleImputer(strategy='median')),<br/>"
            "        ('scaler', StandardScaler())<br/>"
            "    ]), columnas_numericas),<br/>"
            "    ('cat', Pipeline([<br/>"
            "        ('imputer', SimpleImputer(strategy='most_frequent')),<br/>"
            "        ('encoder', OneHotEncoder(handle_unknown='ignore'))<br/>"
            "    ]), columnas_categoricas)<br/>"
            "])<br/><br/>"
            "pipeline = Pipeline([<br/>"
            "    ('preprocessor', preprocessor),<br/>"
            "    ('model', LogisticRegression())<br/>"
            "])",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 14
    # ========================================================

    activity_title(
        story,
        14,
        "Detectar Data Leakage",
        styles
    )

    story.append(
        Paragraph(
            "Analiza estas situaciones y determina si existe riesgo de "
            "data leakage.",
            styles["BodyCustom"]
        )
    )

    situations = [
        [
            Paragraph("Situación", styles["TableHeader"]),
            Paragraph("¿Hay leakage?", styles["TableHeader"]),
            Paragraph("Justificación", styles["TableHeader"]),
        ],
        [
            Paragraph(
                "Escalar todo el dataset antes de dividirlo.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Crear una variable usando una fecha posterior a la predicción.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Ajustar OneHotEncoder con entrenamiento y luego transformar prueba.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Ajustar StandardScaler solamente con X_train.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
    ]

    table = Table(
        situations,
        colWidths=[230, 100, 174],
        rowHeights=[30, 55, 55, 55, 55],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    # ========================================================
    # ACTIVIDAD 15
    # ========================================================

    activity_title(
        story,
        15,
        "Comparar antes y después",
        styles
    )

    story.append(
        Paragraph(
            "Toma un dataset y compara el conjunto original con el "
            "conjunto después de aplicar Feature Engineering.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Cantidad de columnas.",
        "Tipos de variables.",
        "Cantidad de variables numéricas.",
        "Cantidad de variables categóricas.",
        "Distribución de las variables.",
        "Valores faltantes.",
        "Características nuevas.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Explica qué cambios consideras beneficiosos y cuáles "
            "podrían generar problemas.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD INTEGRADORA
    # ========================================================

    story.append(
        Paragraph(
            "Actividad Integradora — Construcción de características",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Consigna</b><br/><br/>"
            "Selecciona un problema de Machine Learning y un dataset "
            "adecuado. Realiza un proceso completo de Feature Engineering "
            "que transforme los datos originales en un conjunto de "
            "características listo para utilizar en un modelo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "El trabajo debe incluir:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "1. Descripción del problema.",
        "2. Descripción del dataset.",
        "3. Identificación de los tipos de variables.",
        "4. Identificación de variables categóricas.",
        "5. Elección y justificación de métodos de codificación.",
        "6. Escalado de variables numéricas cuando corresponda.",
        "7. Creación de al menos tres nuevas características.",
        "8. Al menos una transformación temporal o matemática.",
        "9. Análisis de posibles variables sesgadas.",
        "10. Identificación de posibles riesgos de data leakage.",
        "11. Construcción de un Pipeline.",
        "12. Comparación del dataset antes y después.",
        "13. Justificación de las decisiones tomadas.",
        "14. Conclusiones.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # AUTOEVALUACIÓN
    # ========================================================

    story.append(
        Paragraph(
            "Autoevaluación",
            styles["H2Custom"]
        )
    )

    questions = [
        (
            "1. ¿Qué es Feature Engineering?",
            "Es el proceso de crear o transformar características para representar mejor un problema de Machine Learning."
        ),
        (
            "2. ¿Para qué sirve One-Hot Encoding?",
            "Para representar categorías mediante columnas binarias."
        ),
        (
            "3. ¿Cuándo puede utilizarse Ordinal Encoding?",
            "Cuando las categorías tienen un orden significativo."
        ),
        (
            "4. ¿Para qué sirve StandardScaler?",
            "Para estandarizar variables numéricas utilizando su media y desviación estándar."
        ),
        (
            "5. ¿Cuándo puede ser útil RobustScaler?",
            "Cuando existen valores atípicos que pueden afectar a otros métodos de escalado."
        ),
        (
            "6. ¿Qué es una variable derivada?",
            "Una variable creada a partir de una o más variables existentes."
        ),
        (
            "7. ¿Qué información puede extraerse de una fecha?",
            "Año, mes, día, día de semana, trimestre, hora y otras características."
        ),
        (
            "8. ¿Qué es Data Leakage?",
            "El uso de información que no debería estar disponible durante el entrenamiento."
        ),
        (
            "9. ¿Para qué sirve ColumnTransformer?",
            "Para aplicar diferentes transformaciones a distintos grupos de columnas."
        ),
        (
            "10. ¿Por qué utilizar un Pipeline?",
            "Para integrar y reproducir de forma consistente las transformaciones y el modelo."
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

    # ========================================================
    # CIERRE
    # ========================================================

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
            "Un buen modelo no depende solamente del algoritmo elegido. "
            "La forma en que los datos son representados puede ser "
            "determinante. Feature Engineering permite transformar "
            "datos disponibles en características que expresen mejor "
            "el problema y faciliten el aprendizaje del modelo.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # GENERAR PDF
    # ========================================================

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            doc_subtitle="Módulo 1 - Material 4: Actividades",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()