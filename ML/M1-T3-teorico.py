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
    "M1-T3-Limpieza-e-Imputacion-de-Valores-Faltantes-Teorico.pdf"
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
            "Módulo 1 - Material 3: Limpieza e Imputación"
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


# ============================================================
# TABLA: TIPOS DE VALORES FALTANTES
# ============================================================

def missing_values_table(styles):

    data = [
        [
            Paragraph("Situación", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
            Paragraph("Problema", styles["TableHeader"]),
        ],
        [
            Paragraph("Celda vacía", styles["TableCellBold"]),
            Paragraph(
                "Edad = NaN",
                styles["TableCell"]
            ),
            Paragraph(
                "No existe un valor registrado.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Valor especial", styles["TableCellBold"]),
            Paragraph(
                "Edad = -1",
                styles["TableCell"]
            ),
            Paragraph(
                "Puede representar un faltante codificado incorrectamente.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Texto indicador", styles["TableCellBold"]),
            Paragraph(
                "Ciudad = 'Desconocido'",
                styles["TableCell"]
            ),
            Paragraph(
                "El faltante fue almacenado como texto.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Código especial", styles["TableCellBold"]),
            Paragraph(
                "9999",
                styles["TableCell"]
            ),
            Paragraph(
                "El código puede confundirse con un valor real.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[145, 145, 214],
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
# TABLA: ESTRATEGIAS DE IMPUTACIÓN
# ============================================================

def imputation_table(styles):

    data = [
        [
            Paragraph("Estrategia", styles["TableHeader"]),
            Paragraph("Cuándo utilizarla", styles["TableHeader"]),
            Paragraph("Ventaja / riesgo", styles["TableHeader"]),
        ],
        [
            Paragraph("Media", styles["TableCellBold"]),
            Paragraph(
                "Variables numéricas con distribución relativamente estable.",
                styles["TableCell"]
            ),
            Paragraph(
                "Simple, pero sensible a valores extremos.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Mediana", styles["TableCellBold"]),
            Paragraph(
                "Variables numéricas con asimetría o outliers.",
                styles["TableCell"]
            ),
            Paragraph(
                "Más robusta frente a valores extremos.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Moda", styles["TableCellBold"]),
            Paragraph(
                "Variables categóricas.",
                styles["TableCell"]
            ),
            Paragraph(
                "Simple, pero puede aumentar artificialmente una categoría.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Por grupos", styles["TableCellBold"]),
            Paragraph(
                "Cuando existen grupos con comportamientos diferentes.",
                styles["TableCell"]
            ),
            Paragraph(
                "Más contextualizada, pero requiere mayor análisis.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("KNN", styles["TableCellBold"]),
            Paragraph(
                "Cuando la similitud entre observaciones aporta información.",
                styles["TableCell"]
            ),
            Paragraph(
                "Puede ser costosa y requiere variables adecuadamente escaladas.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Iterativa", styles["TableCellBold"]),
            Paragraph(
                "Cuando las variables presentan relaciones útiles para estimar faltantes.",
                styles["TableCell"]
            ),
            Paragraph(
                "Más flexible, pero más compleja y costosa.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[110, 205, 189],
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
# TABLA: COMPARACIÓN
# ============================================================

def comparison_table(styles):

    data = [
        [
            Paragraph("Método", styles["TableHeader"]),
            Paragraph("Complejidad", styles["TableHeader"]),
            Paragraph("Conserva relaciones", styles["TableHeader"]),
            Paragraph("Uso habitual", styles["TableHeader"]),
        ],
        [
            Paragraph("Media", styles["TableCellBold"]),
            Paragraph("Baja", styles["TableCell"]),
            Paragraph("No", styles["TableCell"]),
            Paragraph("Datos numéricos simples", styles["TableCell"]),
        ],
        [
            Paragraph("Mediana", styles["TableCellBold"]),
            Paragraph("Baja", styles["TableCell"]),
            Paragraph("No", styles["TableCell"]),
            Paragraph("Datos con outliers", styles["TableCell"]),
        ],
        [
            Paragraph("Moda", styles["TableCellBold"]),
            Paragraph("Baja", styles["TableCell"]),
            Paragraph("No", styles["TableCell"]),
            Paragraph("Variables categóricas", styles["TableCell"]),
        ],
        [
            Paragraph("KNN", styles["TableCellBold"]),
            Paragraph("Media", styles["TableCell"]),
            Paragraph("Parcialmente", styles["TableCell"]),
            Paragraph("Datos donde la similitud importa", styles["TableCell"]),
        ],
        [
            Paragraph("Iterativa", styles["TableCellBold"]),
            Paragraph("Alta", styles["TableCell"]),
            Paragraph("Sí", styles["TableCell"]),
            Paragraph("Relaciones entre variables", styles["TableCell"]),
        ],
    ]

    table = Table(
        data,
        colWidths=[105, 85, 135, 179],
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
        title="Limpieza e Imputación de Valores Faltantes",
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
            "Material teórico — Calidad de datos, imputación y estrategias profesionales",
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
            "Comprender cómo identificar, analizar y tratar valores faltantes "
            "en un conjunto de datos, seleccionando estrategias de imputación "
            "adecuadas y evitando problemas como la pérdida innecesaria de "
            "información y el data leakage.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 1
    # ========================================================

    story.append(
        Paragraph(
            "1. La calidad de los datos",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Un modelo de Machine Learning aprende a partir de los datos "
            "que recibe. Si esos datos contienen errores, inconsistencias "
            "o información ausente, el modelo puede aprender patrones "
            "incorrectos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por este motivo, la preparación de datos constituye una etapa "
            "fundamental de cualquier proyecto profesional de Machine Learning.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Datos incompletos.",
        "Datos duplicados.",
        "Valores incorrectos.",
        "Formatos inconsistentes.",
        "Valores extremos.",
        "Categorías mal escritas.",
        "Variables con unidades diferentes.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 2
    # ========================================================

    story.append(
        Paragraph(
            "2. ¿Qué es un valor faltante?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Un <b>valor faltante</b> es una observación en la que no "
            "se dispone del valor correspondiente a una determinada variable.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "En Pandas, los valores faltantes suelen representarse mediante "
            "<b>NaN</b> (Not a Number) o <b>None</b>, dependiendo del tipo "
            "de dato y de cómo se hayan cargado los datos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        missing_values_table(styles)
    )

    # ========================================================
    # 3
    # ========================================================

    story.append(
        Paragraph(
            "3. ¿Por qué aparecen valores faltantes?",
            styles["H2Custom"]
        )
    )

    for item in [
        "El usuario no proporcionó un dato.",
        "Un sensor dejó de funcionar.",
        "Una pregunta no era aplicable.",
        "Se produjo un error durante la carga.",
        "Los datos provienen de diferentes fuentes.",
        "El proceso de integración perdió información.",
        "El valor fue ocultado por motivos de privacidad.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "La causa es importante porque condiciona la estrategia de tratamiento.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 4
    # ========================================================

    story.append(
        Paragraph(
            "4. Detectar valores faltantes con Pandas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La primera tarea es identificar cuántos valores faltantes "
            "existen y en qué variables aparecen.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df.isnull()<br/>"
            "df.isnull().sum()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>isnull()</b> devuelve una estructura booleana que indica "
            "qué posiciones contienen valores faltantes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>isnull().sum()</b> permite obtener la cantidad de valores "
            "faltantes por columna.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 5
    # ========================================================

    story.append(
        Paragraph(
            "5. Porcentaje de valores faltantes",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La cantidad absoluta de valores faltantes no siempre es suficiente. "
            "También debemos conocer qué proporción representan.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "porcentaje_faltantes = df.isnull().mean() * 100<br/>"
            "print(porcentaje_faltantes)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, 20 valores faltantes pueden ser insignificantes "
            "en un dataset de un millón de registros, pero pueden ser "
            "muy importantes en un dataset de 50 registros.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 6
    # ========================================================

    story.append(
        Paragraph(
            "6. Analizar el patrón de ausencia",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "No todos los valores faltantes aparecen de la misma manera. "
            "Es importante observar si la ausencia está concentrada en "
            "determinadas variables, grupos o períodos.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "¿Los faltantes aparecen en una única columna?",
        "¿Se concentran en determinados registros?",
        "¿Aparecen más en un grupo de clientes?",
        "¿Están relacionados con una determinada fecha?",
        "¿Existe alguna variable que permita explicar su ausencia?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 7
    # ========================================================

    story.append(
        Paragraph(
            "7. Eliminar filas con valores faltantes",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Una estrategia sencilla consiste en eliminar las filas que "
            "contienen valores faltantes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df_limpio = df.dropna()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Esta estrategia puede ser apropiada cuando existen pocos "
            "valores faltantes y su eliminación no implica perder "
            "información importante.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Riesgo:</b> si existen muchos valores faltantes, podemos "
            "terminar eliminando una gran cantidad de registros.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 8
    # ========================================================

    story.append(
        Paragraph(
            "8. Eliminar columnas",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Si una variable contiene una proporción extremadamente alta "
            "de valores faltantes y no resulta útil para el problema, "
            "puede considerarse eliminarla.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df = df.drop(columns=['variable'])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Sin embargo, esta decisión debe basarse en el contexto del "
            "problema y no solamente en un porcentaje arbitrario.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 9
    # ========================================================

    story.append(
        Paragraph(
            "9. Imputación de valores faltantes",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La <b>imputación</b> consiste en reemplazar un valor faltante "
            "por una estimación.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "El objetivo es conservar la mayor cantidad posible de "
            "información sin introducir distorsiones importantes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        imputation_table(styles)
    )

    # ========================================================
    # 10
    # ========================================================

    story.append(
        Paragraph(
            "10. Imputación mediante la media",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La media puede utilizarse para completar valores faltantes "
            "de una variable numérica.",
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
            "Es sencilla, pero puede verse afectada por valores extremos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 11
    # ========================================================

    story.append(
        Paragraph(
            "11. Imputación mediante la mediana",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La mediana suele ser una alternativa más robusta cuando "
            "la variable presenta asimetría o valores atípicos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "mediana = df['ingresos'].median()<br/>"
            "df['ingresos'] = df['ingresos'].fillna(mediana)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La mediana divide los valores ordenados en dos grupos de "
            "igual tamaño y suele verse menos afectada por valores extremos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 12
    # ========================================================

    story.append(
        Paragraph(
            "12. Imputación mediante la moda",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La moda es el valor que aparece con mayor frecuencia. "
            "Es especialmente útil para variables categóricas.",
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
            "Debe utilizarse con cuidado porque puede aumentar "
            "artificialmente la frecuencia de una categoría.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 13
    # ========================================================

    story.append(
        Paragraph(
            "13. Imputación por grupos",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "En algunos problemas, la media o mediana global no representa "
            "bien a todos los registros. Puede ser más apropiado calcular "
            "la estadística dentro de un grupo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, los ingresos pueden comportarse de manera "
            "diferente según el tipo de cliente.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "df['ingresos'] = df.groupby('tipo_cliente')['ingresos'].transform(<br/>"
            "    lambda x: x.fillna(x.median())<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Esta estrategia incorpora información contextual y puede "
            "ser más adecuada que una única mediana global.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 14
    # ========================================================

    story.append(
        Paragraph(
            "14. SimpleImputer de Scikit-learn",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Scikit-learn ofrece herramientas específicas para realizar "
            "imputación dentro de pipelines de Machine Learning.",
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
            "Entre las estrategias disponibles se encuentran "
            "<b>mean</b>, <b>median</b> y <b>most_frequent</b>, entre otras.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 15
    # ========================================================

    story.append(
        Paragraph(
            "15. ¿Por qué utilizar Scikit-learn?",
            styles["H2Custom"]
        )
    )

    for item in [
        "Permite integrar la imputación en un pipeline.",
        "Facilita reproducir el mismo procedimiento.",
        "Evita aplicar manualmente transformaciones diferentes.",
        "Permite separar el aprendizaje de parámetros y la transformación.",
        "Se integra con otros pasos de preparación y modelado.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 16
    # ========================================================

    story.append(
        Paragraph(
            "16. KNNImputer",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "KNNImputer utiliza observaciones similares para estimar "
            "los valores faltantes.",
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
            "La idea es que observaciones similares pueden proporcionar "
            "información útil para estimar el valor que falta.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Su principal desventaja es que puede resultar más costoso "
            "computacionalmente y requiere especial atención a las escalas "
            "de las variables.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 17
    # ========================================================

    story.append(
        Paragraph(
            "17. Imputación iterativa",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La imputación iterativa utiliza las relaciones entre variables "
            "para estimar progresivamente los valores faltantes.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una implementación disponible en Scikit-learn es "
            "<b>IterativeImputer</b>.",
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
            "Este método puede producir estimaciones más sofisticadas, "
            "pero también requiere mayor complejidad y análisis.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 18
    # ========================================================

    story.append(
        Paragraph(
            "18. Comparación de estrategias",
            styles["H2Custom"]
        )
    )

    story.append(
        comparison_table(styles)
    )

    # ========================================================
    # 19
    # ========================================================

    story.append(
        Paragraph(
            "19. ¿Cómo elegir una estrategia?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "No existe una estrategia universalmente correcta. "
            "La elección depende de la naturaleza de los datos, "
            "la cantidad de faltantes y el problema que se intenta resolver.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Cantidad de valores faltantes.",
        "Porcentaje de datos ausentes.",
        "Tipo de variable.",
        "Distribución de la variable.",
        "Presencia de outliers.",
        "Relación con otras variables.",
        "Importancia de la variable para el modelo.",
        "Contexto del problema de negocio.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 20
    # ========================================================

    story.append(
        Paragraph(
            "20. El problema del Data Leakage",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Uno de los errores más importantes durante la preparación "
            "de datos es utilizar información del conjunto de prueba "
            "para calcular transformaciones que deberían aprenderse "
            "únicamente con los datos de entrenamiento.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, si calculamos la mediana utilizando todo el "
            "dataset antes de dividirlo en entrenamiento y prueba, "
            "estamos permitiendo que información del conjunto de prueba "
            "influya en el proceso.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Regla profesional</b><br/><br/>"
            "Primero se separan los datos en entrenamiento y prueba. "
            "Luego se calcula la estrategia de imputación utilizando "
            "solamente el conjunto de entrenamiento. Finalmente, "
            "esa transformación se aplica al conjunto de prueba.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 21
    # ========================================================

    story.append(
        Paragraph(
            "21. Pipeline de Scikit-learn",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Los pipelines permiten encadenar transformaciones y modelos "
            "de manera reproducible.",
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

    story.append(
        Paragraph(
            "Este enfoque ayuda a evitar errores de preparación y "
            "permite aplicar exactamente las mismas transformaciones "
            "durante entrenamiento y predicción.",
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
        "Eliminar automáticamente todas las filas con faltantes.",
        "Utilizar siempre la media sin analizar la distribución.",
        "Utilizar la moda sin considerar el equilibrio de categorías.",
        "Tratar códigos especiales como valores reales.",
        "No investigar por qué faltan los datos.",
        "Calcular estadísticas utilizando también el conjunto de prueba.",
        "Imputar antes de realizar la división entrenamiento/prueba.",
        "Aplicar estrategias diferentes entre entrenamiento y producción.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 23
    # ========================================================

    story.append(
        Paragraph(
            "23. Flujo profesional para tratar valores faltantes",
            styles["H2Custom"]
        )
    )

    for number, text in [
        ("1", "Detectar los valores faltantes."),
        ("2", "Medir su cantidad y porcentaje."),
        ("3", "Investigar el motivo de la ausencia."),
        ("4", "Analizar su distribución."),
        ("5", "Separar entrenamiento y prueba."),
        ("6", "Elegir una estrategia."),
        ("7", "Ajustar la estrategia con los datos de entrenamiento."),
        ("8", "Aplicar la transformación."),
        ("9", "Validar el resultado."),
        ("10", "Documentar la decisión."),
    ]:
        story.append(
            Paragraph(
                f"<b>{number}.</b> {text}",
                styles["BulletCustom"]
            )
        )

    # ========================================================
    # 24
    # ========================================================

    story.append(
        Paragraph(
            "24. Ejemplo completo",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Un flujo sencillo utilizando Scikit-learn puede ser:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "import pandas as pd<br/>"
            "from sklearn.model_selection import train_test_split<br/>"
            "from sklearn.impute import SimpleImputer<br/><br/>"
            "df = pd.read_csv('clientes.csv')<br/><br/>"
            "X = df.drop(columns=['abandono'])<br/>"
            "y = df['abandono']<br/><br/>"
            "X_train, X_test, y_train, y_test = train_test_split(<br/>"
            "    X, y, test_size=0.2, random_state=42<br/>"
            ")<br/><br/>"
            "imputer = SimpleImputer(strategy='median')<br/>"
            "X_train = imputer.fit_transform(X_train)<br/>"
            "X_test = imputer.transform(X_test)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La diferencia entre <b>fit_transform()</b> y <b>transform()</b> "
            "es fundamental: el primero aprende los parámetros utilizando "
            "el entrenamiento y el segundo aplica esos parámetros a nuevos datos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 25
    # ========================================================

    story.append(
        Paragraph(
            "25. Idea central",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Limpiar datos no significa borrar problemas.</b><br/><br/>"
            "Una limpieza profesional busca comprender el origen de las "
            "inconsistencias, conservar la mayor cantidad de información "
            "posible y aplicar transformaciones que puedan reproducirse "
            "correctamente en nuevos datos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 26
    # ========================================================

    story.append(
        Paragraph(
            "26. Glosario",
            styles["H2Custom"]
        )
    )

    glossary = [
        (
            "Valor faltante",
            "Observación para la que no se dispone del valor de una variable."
        ),
        (
            "Imputación",
            "Proceso de estimar y reemplazar valores faltantes."
        ),
        (
            "Media",
            "Promedio aritmético de un conjunto de valores."
        ),
        (
            "Mediana",
            "Valor central de una distribución ordenada."
        ),
        (
            "Moda",
            "Valor que aparece con mayor frecuencia."
        ),
        (
            "KNN",
            "Método basado en vecinos cercanos para realizar estimaciones."
        ),
        (
            "Data Leakage",
            "Uso indebido de información que no debería estar disponible durante el entrenamiento."
        ),
        (
            "Pipeline",
            "Secuencia reproducible de transformaciones y pasos de procesamiento."
        ),
        (
            "SimpleImputer",
            "Herramienta de Scikit-learn para imputación de valores faltantes."
        ),
        (
            "IterativeImputer",
            "Método de imputación que utiliza relaciones entre variables."
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
            doc_subtitle="Módulo 1 - Material 3: Limpieza e Imputación",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()