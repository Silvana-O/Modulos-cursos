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
    "M1-T3-Limpieza-e-Imputacion-de-Valores-Faltantes-Actividades.pdf"
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
            "Módulo 1 - Material 3: Actividades"
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
            "Material educativo • Módulo 1 - Material 3"
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
        title="Actividades - Limpieza e Imputación",
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
            "Limpieza e Imputación de Valores Faltantes",
            styles["DocTitle"]
        )
    )

    story.append(
        Paragraph(
            "Actividades prácticas — Calidad de datos e imputación",
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
            "Aplicar técnicas de detección, análisis y tratamiento de "
            "valores faltantes utilizando Pandas y Scikit-learn, "
            "comprendiendo los riesgos de cada estrategia.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 1
    # ========================================================

    activity_title(
        story,
        1,
        "Reconocer valores faltantes",
        styles
    )

    story.append(
        Paragraph(
            "Analiza el siguiente dataset hipotético:",
            styles["BodyCustom"]
        )
    )

    data = [
        [
            Paragraph("Edad", styles["TableHeader"]),
            Paragraph("Ingresos", styles["TableHeader"]),
            Paragraph("Ciudad", styles["TableHeader"]),
            Paragraph("Plan", styles["TableHeader"]),
        ],
        ["22", "25000", "Montevideo", "Básico"],
        ["35", "", "Canelones", "Premium"],
        ["", "61000", "Montevideo", "Premium"],
        ["29", "33000", "", "Básico"],
        ["52", "72000", "Montevideo", ""],
    ]

    table = Table(
        data,
        colWidths=[90, 120, 150, 144],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
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
        "Identifica todas las celdas con información faltante.",
        "¿Qué porcentaje aproximado de datos falta en cada columna?",
        "¿Eliminarías alguna fila? Justifica.",
        "¿Eliminarías alguna columna? Justifica.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 2
    # ========================================================

    activity_title(
        story,
        2,
        "Detectar faltantes con Pandas",
        styles
    )

    story.append(
        Paragraph(
            "Carga un dataset mediante Pandas y ejecuta:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "print(df.isnull().sum())<br/><br/>"
            "porcentaje = df.isnull().mean() * 100<br/>"
            "print(porcentaje)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Registra los resultados e identifica las tres variables "
            "con mayor cantidad de valores faltantes.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 3
    # ========================================================

    activity_title(
        story,
        3,
        "¿Eliminar o imputar?",
        styles
    )

    story.append(
        Paragraph(
            "Para cada situación decide qué estrategia sería más apropiada "
            "y explica por qué.",
            styles["BodyCustom"]
        )
    )

    situations = [
        [
            Paragraph("Situación", styles["TableHeader"]),
            Paragraph("Decisión", styles["TableHeader"]),
            Paragraph("Justificación", styles["TableHeader"]),
        ],
        [
            Paragraph(
                "Una columna tiene 98 % de valores faltantes.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Una variable numérica tiene 2 % de faltantes.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Una variable categórica tiene 5 % de faltantes.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Los faltantes aparecen principalmente en un grupo de clientes.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
    ]

    table = Table(
        situations,
        colWidths=[200, 120, 184],
        rowHeights=[30, 60, 60, 60, 60],
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
    # ACTIVIDAD 4
    # ========================================================

    activity_title(
        story,
        4,
        "Media, mediana y moda",
        styles
    )

    story.append(
        Paragraph(
            "Crea una copia de tu dataset y realiza tres versiones "
            "diferentes de la imputación.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Versión 1 — Media:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "media = df['edad'].mean()<br/>"
            "df['edad'] = df['edad'].fillna(media)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Versión 2 — Mediana:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "mediana = df['edad'].median()<br/>"
            "df['edad'] = df['edad'].fillna(mediana)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Versión 3 — Moda para una variable categórica:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "moda = df['plan'].mode()[0]<br/>"
            "df['plan'] = df['plan'].fillna(moda)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Compara los resultados y explica cómo cambia el dataset "
            "en cada caso.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 5
    # ========================================================

    activity_title(
        story,
        5,
        "Elegir entre media y mediana",
        styles
    )

    story.append(
        Paragraph(
            "Considera los siguientes valores de ingresos:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "25000, 28000, 30000, 32000, 35000, 37000, 40000, 450000",
            styles["CodeCustom"]
        )
    )

    for item in [
        "Calcula la media.",
        "Calcula la mediana.",
        "Compara ambos resultados.",
        "¿Cuál utilizarías para imputar un valor faltante?",
        "Justifica tu elección.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 6
    # ========================================================

    activity_title(
        story,
        6,
        "Imputación por grupos",
        styles
    )

    story.append(
        Paragraph(
            "Supón que tienes una variable de ingresos y otra que indica "
            "si el cliente pertenece al plan Básico o Premium.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Investiga los beneficios de utilizar una mediana diferente "
            "para cada grupo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Implementa una solución utilizando:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.groupby('plan')['ingresos'].transform(<br/>"
            "    lambda x: x.fillna(x.median())<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Explica por qué esta estrategia puede ser mejor que utilizar "
            "una única mediana para todos los clientes.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 7
    # ========================================================

    activity_title(
        story,
        7,
        "SimpleImputer",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza Scikit-learn para imputar una variable numérica "
            "mediante la mediana.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.impute import SimpleImputer<br/><br/>"
            "imputer = SimpleImputer(strategy='median')<br/>"
            "X_imputado = imputer.fit_transform(X)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Luego repite utilizando:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "strategy='mean'",
        "strategy='most_frequent'",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Compara los resultados.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 8
    # ========================================================

    activity_title(
        story,
        8,
        "KNNImputer",
        styles
    )

    story.append(
        Paragraph(
            "Investiga y aplica KNNImputer sobre un conjunto de variables "
            "numéricas.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.impute import KNNImputer<br/><br/>"
            "imputer = KNNImputer(n_neighbors=5)<br/>"
            "X_imputado = imputer.fit_transform(X)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Prueba diferentes cantidades de vecinos y observa si "
            "las estimaciones cambian.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 9
    # ========================================================

    activity_title(
        story,
        9,
        "Imputación iterativa",
        styles
    )

    story.append(
        Paragraph(
            "Implementa una imputación utilizando IterativeImputer.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.experimental import enable_iterative_imputer<br/>"
            "from sklearn.impute import IterativeImputer<br/><br/>"
            "imputer = IterativeImputer(random_state=42)<br/>"
            "X_imputado = imputer.fit_transform(X)",
            styles["CodeCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Compara los valores obtenidos con los métodos anteriores.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 10
    # ========================================================

    activity_title(
        story,
        10,
        "Detectar Data Leakage",
        styles
    )

    story.append(
        Paragraph(
            "Analiza las siguientes dos estrategias:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "<b>Estrategia A</b><br/>"
            "1. Calcular la mediana de todo el dataset.<br/>"
            "2. Dividir en entrenamiento y prueba.<br/>"
            "3. Aplicar la mediana.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "<b>Estrategia B</b><br/>"
            "1. Dividir en entrenamiento y prueba.<br/>"
            "2. Calcular la mediana únicamente con entrenamiento.<br/>"
            "3. Aplicar esa mediana a entrenamiento y prueba.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "¿Cuál es correcta? ¿Por qué?",
            styles["BodyCustom"]
        )
    )    

    # ========================================================
    # ACTIVIDAD 11
    # ========================================================

    activity_title(
        story,
        11,
        "Construir un Pipeline",
        styles
    )

    story.append(
        Paragraph(
            "Construye un pipeline que incluya:",
            styles["BodyCustom"]
        )
    )    

    for item in [
        "Imputación mediante mediana.",
        "Escalado mediante StandardScaler.",
        "Un modelo de clasificación.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Utiliza como referencia:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from sklearn.pipeline import Pipeline<br/>"
            "from sklearn.impute import SimpleImputer<br/>"
            "from sklearn.preprocessing import StandardScaler<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "pipeline = Pipeline([<br/>"
            "    ('imputer', SimpleImputer(strategy='median')),<br/>"
            "    ('scaler', StandardScaler()),<br/>"
            "    ('model', LogisticRegression())<br/>"
            "])",
            styles["CodeCustom"]
        )
    )    

    # ========================================================
    # ACTIVIDAD 12
    # ========================================================

    activity_title(
        story,
        12,
        "Comparar estrategias",
        styles
    )

    story.append(
        Paragraph(
            "Selecciona un dataset que contenga valores faltantes. "
            "Crea tres versiones del dataset:",
            styles["BodyCustom"]
        )
    )    

    for item in [
        "Versión A: eliminación de filas.",
        "Versión B: imputación mediante mediana.",
        "Versión C: imputación mediante KNN.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Compara:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Cantidad de registros.",
        "Cantidad de valores faltantes.",
        "Distribución de las variables.",
        "Cambios en las estadísticas descriptivas.",
        "Resultado de un modelo sencillo.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD INTEGRADORA
    # ========================================================

    story.append(
        Paragraph(
            "Actividad Integradora — Limpieza profesional de un dataset",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Consigna</b><br/><br/>"
            "Selecciona un dataset relacionado con un problema de "
            "Machine Learning. Realiza un diagnóstico de sus valores "
            "faltantes y diseña una estrategia de limpieza e imputación "
            "justificada.",
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
        "1. Descripción del dataset.",
        "2. Cantidad de valores faltantes por variable.",
        "3. Porcentaje de faltantes.",
        "4. Análisis del posible origen de los faltantes.",
        "5. Decisión sobre eliminación o imputación.",
        "6. Aplicación de al menos dos estrategias de imputación.",
        "7. Comparación de los resultados.",
        "8. Análisis de posibles outliers afectados.",
        "9. División entre entrenamiento y prueba.",
        "10. Explicación de cómo se evitó el data leakage.",
        "11. Pipeline de procesamiento.",
        "12. Conclusiones.",
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
            "1. ¿Qué es un valor faltante?",
            "Una observación para la que no se dispone del valor correspondiente."
        ),
        (
            "2. ¿Cómo se detectan valores faltantes con Pandas?",
            "Mediante métodos como isnull() o isna()."
        ),
        (
            "3. ¿Cuándo puede ser conveniente utilizar la mediana?",
            "Cuando la variable numérica presenta asimetría o valores extremos."
        ),
        (
            "4. ¿Qué estrategia suele utilizarse con variables categóricas?",
            "La moda, aunque debe analizarse su conveniencia."
        ),
        (
            "5. ¿Qué es KNNImputer?",
            "Un método que utiliza observaciones similares para estimar faltantes."
        ),
        (
            "6. ¿Qué es Data Leakage?",
            "El uso indebido de información que no debería estar disponible durante el entrenamiento."
        ),
        (
            "7. ¿Con qué datos debe ajustarse un imputador?",
            "Con los datos de entrenamiento."
        ),
        (
            "8. ¿Por qué utilizar un Pipeline?",
            "Para integrar y reproducir correctamente las transformaciones y el modelado."
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
            "Los valores faltantes no deben tratarse automáticamente. "
            "Una estrategia profesional comienza por comprender por qué "
            "faltan los datos, medir su impacto y seleccionar una técnica "
            "de imputación que preserve la información sin introducir "
            "sesgos ni data leakage.",
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
            doc_subtitle="Módulo 1 - Material 3: Actividades",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()