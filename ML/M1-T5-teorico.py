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
    "M1-T5-Seleccion-de-Caracteristicas-y-Desbalanceo-Teorico.pdf"
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
            "Módulo 1 - Material 5: Selección de Características"
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
            "Material educativo • Módulo 1 - Material 5"
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

def bullet(text, styles):
    return Paragraph(
        f"• {text}",
        styles["BulletCustom"]
    )


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


# ============================================================
# TABLA DE MÉTODOS DE SELECCIÓN
# ============================================================

def selection_table(styles):

    data = [
        [
            Paragraph("Método", styles["TableHeader"]),
            Paragraph("Tipo", styles["TableHeader"]),
            Paragraph("Idea principal", styles["TableHeader"]),
        ],
        [
            Paragraph("Correlación", styles["TableCellBold"]),
            Paragraph("Filter", styles["TableCell"]),
            Paragraph(
                "Detecta relaciones entre variables numéricas.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("VarianceThreshold", styles["TableCellBold"]),
            Paragraph("Filter", styles["TableCell"]),
            Paragraph(
                "Elimina variables con muy poca variabilidad.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("SelectKBest", styles["TableCellBold"]),
            Paragraph("Filter", styles["TableCell"]),
            Paragraph(
                "Selecciona las K características con mejor puntuación.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Mutual Information", styles["TableCellBold"]),
            Paragraph("Filter", styles["TableCell"]),
            Paragraph(
                "Mide dependencia entre características y objetivo.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("RFE", styles["TableCellBold"]),
            Paragraph("Wrapper", styles["TableCell"]),
            Paragraph(
                "Elimina características de forma iterativa utilizando un modelo.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("L1 / Lasso", styles["TableCellBold"]),
            Paragraph("Embedded", styles["TableCell"]),
            Paragraph(
                "Puede llevar algunos coeficientes a cero.",
                styles["TableCell"]
            ),
        ],
        [
            Paragraph("Random Forest", styles["TableCellBold"]),
            Paragraph("Embedded", styles["TableCell"]),
            Paragraph(
                "Permite estimar importancia de características.",
                styles["TableCell"]
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[145, 75, 284],
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
        title="Selección de Características y Desbalanceo",
        author="Cursos CC",
    )

    story = []

    # ========================================================
    # INTRODUCCIÓN
    # ========================================================

    story.append(
        Paragraph(
            "MÓDULO 1 · PIPELINE DE DATOS Y PREPARACIÓN PROFESIONAL",
            styles["ModuleTag"]
        )
    )

    story.append(
        Paragraph(
            "Selección de Características y Tratamiento del Desbalanceo",
            styles["DocTitle"]
        )
    )

    story.append(
        Paragraph(
            "Material teórico — Feature Selection, métricas y SMOTE",
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
            "Comprender cómo seleccionar las características más útiles "
            "para un modelo de Machine Learning y cómo abordar problemas "
            "de desbalanceo de clases en tareas de clasificación.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 1
    # ========================================================

    story.append(
        Paragraph(
            "1. ¿Qué es Feature Selection?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La <b>selección de características</b> o "
            "<b>Feature Selection</b> consiste en elegir, de un conjunto "
            "de variables disponibles, aquellas que aportan información "
            "relevante para el problema.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Es diferente de Feature Engineering. En Feature Engineering "
            "podemos crear nuevas variables; en Feature Selection decidimos "
            "cuáles conservar.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 2
    # ========================================================

    story.append(
        Paragraph(
            "2. ¿Por qué seleccionar características?",
            styles["H2Custom"]
        )
    )

    for item in [
        "Reducir características irrelevantes.",
        "Eliminar información redundante.",
        "Reducir la complejidad del modelo.",
        "Disminuir el tiempo de entrenamiento.",
        "Facilitar la interpretación.",
        "Reducir el riesgo de sobreajuste en algunos escenarios.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 3
    # ========================================================

    story.append(
        Paragraph(
            "3. Características relevantes, redundantes e irrelevantes",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Relevante:</b> aporta información útil para predecir "
            "la variable objetivo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Irrelevante:</b> aporta poca o ninguna información útil "
            "para la tarea.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Redundante:</b> contiene información muy similar a otras "
            "características.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 4
    # ========================================================

    story.append(
        Paragraph(
            "4. El problema de utilizar demasiadas características",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Agregar muchas variables no garantiza un modelo mejor. "
            "Algunas pueden contener ruido, duplicar información o "
            "aumentar innecesariamente la complejidad.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Principio importante</b><br/><br/>"
            "La selección de características debe estar guiada por "
            "el problema, los datos y la evaluación experimental, "
            "no simplemente por conservar la mayor cantidad posible "
            "de columnas.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 5
    # ========================================================

    story.append(
        Paragraph(
            "5. Métodos de selección",
            styles["H2Custom"]
        )
    )

    story.append(selection_table(styles))

    # ========================================================
    # 6
    # ========================================================

    story.append(
        Paragraph(
            "6. Métodos Filter",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Los métodos <b>Filter</b> analizan las características "
            "mediante medidas estadísticas antes de entrenar el modelo.",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Son relativamente rápidos.",
        "Pueden aplicarse como etapa previa al modelado.",
        "No dependen necesariamente de un algoritmo específico.",
        "Deben interpretarse según el tipo de problema.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 7
    # ========================================================

    story.append(
        Paragraph(
            "7. Selección mediante correlación",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La correlación permite estudiar la relación entre variables "
            "numéricas. Si dos características presentan una correlación "
            "muy alta, puede existir redundancia.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import seaborn as sns<br/>"
            "import matplotlib.pyplot as plt<br/><br/>"
            "sns.heatmap(df.corr(numeric_only=True), annot=True)<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una correlación alta entre dos variables no significa "
            "automáticamente que una deba eliminarse. La decisión debe "
            "considerar el problema y el modelo.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 8
    # ========================================================

    story.append(
        Paragraph(
            "8. VarianceThreshold",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "VarianceThreshold elimina características cuya variabilidad "
            "es inferior a un umbral determinado.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import VarianceThreshold<br/><br/>"
            "selector = VarianceThreshold(threshold=0.0)<br/>"
            "X_new = selector.fit_transform(X)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una característica constante tiene varianza cero y, en "
            "general, no permite distinguir entre observaciones.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 9
    # ========================================================

    story.append(
        Paragraph(
            "9. SelectKBest",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "SelectKBest permite seleccionar las K características "
            "con mejores puntuaciones según una función estadística.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import SelectKBest, f_classif<br/><br/>"
            "selector = SelectKBest(score_func=f_classif, k=5)<br/>"
            "X_new = selector.fit_transform(X, y)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La función estadística debe ser adecuada al tipo de problema "
            "y a las características utilizadas.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 10
    # ========================================================

    story.append(
        Paragraph(
            "10. Mutual Information",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La información mutua permite estimar la dependencia entre "
            "una característica y la variable objetivo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import mutual_info_classif<br/><br/>"
            "scores = mutual_info_classif(X, y, random_state=42)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Un valor mayor puede indicar una relación informativa, "
            "aunque no implica necesariamente una relación causal.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 11
    # ========================================================

    story.append(
        Paragraph(
            "11. Métodos Wrapper",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Los métodos Wrapper utilizan un modelo para evaluar "
            "diferentes conjuntos de características.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Una técnica conocida es <b>RFE</b>, Recursive Feature Elimination.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import RFE<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "model = LogisticRegression(max_iter=1000)<br/>"
            "selector = RFE(model, n_features_to_select=5)<br/>"
            "X_new = selector.fit_transform(X, y)",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 12
    # ========================================================

    story.append(
        Paragraph(
            "12. Métodos Embedded",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Los métodos Embedded realizan la selección como parte "
            "del entrenamiento del modelo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Dos ejemplos frecuentes son:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Regularización L1.",
        "Importancia de características en modelos basados en árboles.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 13
    # ========================================================

    story.append(
        Paragraph(
            "13. L1 y Lasso",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La regularización L1 puede llevar algunos coeficientes "
            "del modelo a cero. Esto permite identificar características "
            "que el modelo no está utilizando de la misma manera.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "model = LogisticRegression(<br/>"
            "    penalty='l1',<br/>"
            "    solver='liblinear'<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 14
    # ========================================================

    story.append(
        Paragraph(
            "14. Importancia de características con árboles",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Modelos como Random Forest pueden proporcionar estimaciones "
            "de importancia de características.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.ensemble import RandomForestClassifier<br/><br/>"
            "model = RandomForestClassifier(random_state=42)<br/>"
            "model.fit(X, y)<br/><br/>"
            "importancias = model.feature_importances_",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Estas importancias deben interpretarse con cuidado y "
            "no deben considerarse automáticamente como una prueba "
            "de causalidad.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 15
    # ========================================================

    story.append(
        Paragraph(
            "15. Selección y Cross-Validation",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Si seleccionamos características utilizando todo el dataset "
            "antes de realizar Cross-Validation, podemos introducir "
            "información del conjunto de validación en el proceso.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Regla:</b><br/><br/>"
            "Las operaciones que aprenden información de los datos deben "
            "realizarse dentro del proceso de entrenamiento y validación, "
            "no utilizando anticipadamente todo el dataset.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 16
    # ========================================================

    story.append(
        Paragraph(
            "16. Data Leakage en Feature Selection",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Existe Data Leakage cuando una transformación utiliza "
            "información que no debería estar disponible durante "
            "el entrenamiento.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, calcular estadísticas sobre todo el dataset "
            "y luego dividirlo puede contaminar el conjunto de prueba.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 17
    # ========================================================

    story.append(
        Paragraph(
            "17. ¿Qué es el desbalanceo de clases?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "En un problema de clasificación existe desbalanceo cuando "
            "las clases tienen cantidades de observaciones muy diferentes.",
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
            "Clase 0: 9500 observaciones<br/>"
            "Clase 1: 500 observaciones",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "La clase 1 representa solamente el 5 % de los datos.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 18
    # ========================================================

    story.append(
        Paragraph(
            "18. ¿Por qué el desbalanceo es un problema?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Un modelo puede aprender a favorecer la clase mayoritaria "
            "y aun así obtener una Accuracy aparentemente alta.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Ejemplo</b><br/><br/>"
            "Si el 95 % de los clientes no abandona y el modelo predice "
            "siempre 'no abandona', podría obtener aproximadamente 95 % "
            "de Accuracy y, sin embargo, no detectar ningún abandono.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 19
    # ========================================================

    story.append(
        Paragraph(
            "19. Matriz de confusión",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "La matriz de confusión permite analizar las predicciones "
            "comparando las clases reales con las predichas.",
            styles["BodyCustom"]
        )
    )

    confusion = [
        [
            Paragraph("", styles["TableHeader"]),
            Paragraph("Predicción positiva", styles["TableHeader"]),
            Paragraph("Predicción negativa", styles["TableHeader"]),
        ],
        [
            Paragraph("Real positiva", styles["TableCellBold"]),
            Paragraph("Verdadero Positivo (TP)", styles["TableCell"]),
            Paragraph("Falso Negativo (FN)", styles["TableCell"]),
        ],
        [
            Paragraph("Real negativa", styles["TableCellBold"]),
            Paragraph("Falso Positivo (FP)", styles["TableCell"]),
            Paragraph("Verdadero Negativo (TN)", styles["TableCell"]),
        ],
    ]

    table = Table(
        confusion,
        colWidths=[150, 177, 177],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(table)

    # ========================================================
    # 20
    # ========================================================

    story.append(
        Paragraph(
            "20. Precision, Recall y F1-score",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Precision:</b> de las predicciones positivas realizadas, "
            "¿cuántas fueron realmente positivas?",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Recall:</b> de todas las observaciones realmente positivas, "
            "¿cuántas logró detectar el modelo?",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>F1-score:</b> combina Precision y Recall mediante su "
            "media armónica.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.metrics import classification_report<br/><br/>"
            "print(classification_report(y_test, y_pred))",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 21
    # ========================================================

    story.append(
        Paragraph(
            "21. Estrategias para tratar el desbalanceo",
            styles["H2Custom"]
        )
    )

    for item in [
        "Modificar los pesos de las clases.",
        "Oversampling de la clase minoritaria.",
        "Undersampling de la clase mayoritaria.",
        "SMOTE.",
        "Utilizar métricas adecuadas.",
        "Comparar diferentes estrategias.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 22
    # ========================================================

    story.append(
        Paragraph(
            "22. Class Weight",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Algunos modelos permiten asignar mayor peso a las clases "
            "minoritarias.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "model = LogisticRegression(<br/>"
            "    class_weight='balanced',<br/>"
            "    max_iter=1000<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Esta estrategia no crea nuevas observaciones. Modifica "
            "la importancia que tienen las clases durante el entrenamiento.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 23
    # ========================================================

    story.append(
        Paragraph(
            "23. Oversampling y Undersampling",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Oversampling:</b> aumenta la representación de la clase "
            "minoritaria.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "<b>Undersampling:</b> reduce la representación de la clase "
            "mayoritaria.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Ambas estrategias deben aplicarse solamente sobre los datos "
            "de entrenamiento.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 24
    # ========================================================

    story.append(
        Paragraph(
            "24. ¿Qué es SMOTE?",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "SMOTE significa <b>Synthetic Minority Over-sampling Technique</b>.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "En lugar de simplemente duplicar observaciones de la clase "
            "minoritaria, SMOTE genera nuevos ejemplos sintéticos "
            "a partir de observaciones existentes y sus vecinos.",
            styles["BodyCustom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Idea conceptual</b><br/><br/>"
            "SMOTE busca crear nuevos puntos dentro de regiones donde "
            "existen observaciones de la clase minoritaria.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 25
    # ========================================================

    story.append(
        Paragraph(
            "25. Aplicar SMOTE",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "SMOTE forma parte de la biblioteca "
            "<b>imbalanced-learn</b>.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from imblearn.over_sampling import SMOTE<br/><br/>"
            "smote = SMOTE(random_state=42)<br/>"
            "X_resampled, y_resampled = smote.fit_resample(X_train, y_train)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Después de la transformación es posible comprobar "
            "la nueva distribución de las clases.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 26
    # ========================================================

    story.append(
        Paragraph(
            "26. SMOTE y Data Leakage",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Uno de los errores más importantes es aplicar SMOTE antes "
            "de dividir los datos en entrenamiento y prueba.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Incorrecto:",
            styles["H3Custom"]
        )
    )    

    story.append(
        Paragraph(
            "X_resampled, y_resampled = smote.fit_resample(X, y)<br/>"
            "X_train, X_test, y_train, y_test = train_test_split(...)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Correcto:",
            styles["H3Custom"]
        )
    )    

    story.append(
        Paragraph(
            "X_train, X_test, y_train, y_test = train_test_split(...)<br/><br/>"
            "X_train, y_train = smote.fit_resample(X_train, y_train)",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 27
    # ========================================================

    story.append(
        Paragraph(
            "27. Pipeline con SMOTE",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Cuando se utiliza Cross-Validation, una alternativa profesional "
            "es incorporar SMOTE dentro de un Pipeline de imbalanced-learn.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "from imblearn.pipeline import Pipeline<br/>"
            "from imblearn.over_sampling import SMOTE<br/>"
            "from sklearn.preprocessing import StandardScaler<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "pipeline = Pipeline([<br/>"
            "    ('scaler', StandardScaler()),<br/>"
            "    ('smote', SMOTE(random_state=42)),<br/>"
            "    ('model', LogisticRegression(max_iter=1000))<br/>"
            "])",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "De esta manera, el sobremuestreo se realiza dentro del "
            "proceso de entrenamiento de cada partición.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 28
    # ========================================================

    story.append(
        Paragraph(
            "28. Selección + Balanceo",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "En un proyecto real pueden combinarse diferentes etapas:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Imputación.",
        "Feature Engineering.",
        "Feature Selection.",
        "Escalado.",
        "SMOTE.",
        "Modelo.",
        "Evaluación.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "El orden exacto depende de las características del problema "
            "y debe diseñarse cuidadosamente para evitar Data Leakage.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 29
    # ========================================================

    story.append(
        Paragraph(
            "29. Flujo profesional completo",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Un flujo simplificado puede representarse como:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Dataset<br/>"
            "↓<br/>"
            "EDA<br/>"
            "↓<br/>"
            "Limpieza<br/>"
            "↓<br/>"
            "Feature Engineering<br/>"
            "↓<br/>"
            "Separación Train/Test<br/>"
            "↓<br/>"
            "Feature Selection<br/>"
            "↓<br/>"
            "Balanceo del entrenamiento<br/>"
            "↓<br/>"
            "Modelo<br/>"
            "↓<br/>"
            "Evaluación",
            styles["CodeCustom"]
        )
    )

    # ========================================================
    # 30
    # ========================================================

    story.append(
        Paragraph(
            "30. Errores frecuentes",
            styles["H2Custom"]
        )
    )

    for item in [
        "Eliminar características únicamente porque tienen correlación baja.",
        "Mantener todas las variables sin evaluar su utilidad.",
        "Seleccionar características utilizando el conjunto de prueba.",
        "Aplicar SMOTE antes del train/test split.",
        "Utilizar Accuracy como única métrica en datasets desbalanceados.",
        "No analizar la matriz de confusión.",
        "Aplicar SMOTE sobre datos de validación.",
        "No comparar diferentes estrategias.",
        "No documentar las decisiones.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 31
    # ========================================================

    story.append(
        Paragraph(
            "31. Buenas prácticas",
            styles["H2Custom"]
        )
    )

    for item in [
        "Comprender el problema antes de seleccionar variables.",
        "Separar entrenamiento y prueba correctamente.",
        "Realizar las transformaciones dentro de Pipelines cuando corresponda.",
        "Utilizar Cross-Validation.",
        "Elegir métricas relacionadas con el objetivo del proyecto.",
        "Comparar modelos y estrategias.",
        "Documentar las características seleccionadas.",
        "Verificar que no exista Data Leakage.",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # 32
    # ========================================================

    story.append(
        Paragraph(
            "32. Caso práctico",
            styles["H2Custom"]
        )
    )

    story.append(
        Paragraph(
            "Supongamos un sistema que debe detectar clientes con "
            "riesgo de abandonar un servicio.",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "El dataset contiene 10 000 clientes:",
            styles["BodyCustom"]
        )
    )    

    story.append(
        Paragraph(
            "Clase 0 — permanece: 9 000<br/>"
            "Clase 1 — abandona: 1 000",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "El proyecto podría seguir estos pasos:",
            styles["BodyCustom"]
        )
    )    

    for number, text in [
        ("1", "Explorar la distribución de las clases."),
        ("2", "Analizar las características."),
        ("3", "Eliminar variables claramente irrelevantes."),
        ("4", "Separar entrenamiento y prueba."),
        ("5", "Seleccionar características dentro del proceso de entrenamiento."),
        ("6", "Aplicar SMOTE solamente sobre entrenamiento."),
        ("7", "Entrenar el modelo."),
        ("8", "Evaluar con Precision, Recall y F1-score."),
        ("9", "Comparar con una estrategia sin SMOTE."),
        ("10", "Analizar si el modelo cumple el objetivo del negocio."),
    ]:
        story.append(
            Paragraph(
                f"<b>{number}.</b> {text}",
                styles["BulletCustom"]
            )
        )

    # ========================================================
    # 33
    # ========================================================

    story.append(
        Paragraph(
            "33. Idea central",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Seleccionar características y tratar el desbalanceo "
            "son decisiones del proceso de preparación, no pasos "
            "aislados.</b><br/><br/>"
            "El objetivo no es modificar los datos de cualquier manera, "
            "sino construir un conjunto de entrenamiento representativo "
            "y un flujo reproducible que permita evaluar correctamente "
            "el modelo.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # 34
    # ========================================================

    story.append(
        Paragraph(
            "34. Glosario",
            styles["H2Custom"]
        )
    )

    glossary = [
        (
            "Feature Selection",
            "Proceso de seleccionar características relevantes para un modelo."
        ),
        (
            "Filter Method",
            "Método de selección basado en criterios estadísticos."
        ),
        (
            "Wrapper Method",
            "Método que utiliza un modelo para evaluar subconjuntos de características."
        ),
        (
            "Embedded Method",
            "Método donde la selección forma parte del entrenamiento."
        ),
        (
            "VarianceThreshold",
            "Método que elimina variables con variabilidad insuficiente."
        ),
        (
            "SelectKBest",
            "Selecciona las K características con mejor puntuación estadística."
        ),
        (
            "RFE",
            "Eliminación recursiva de características."
        ),
        (
            "Desbalanceo",
            "Situación donde las clases tienen cantidades muy diferentes de observaciones."
        ),
        (
            "Oversampling",
            "Aumento de la representación de la clase minoritaria."
        ),
        (
            "Undersampling",
            "Reducción de la representación de la clase mayoritaria."
        ),
        (
            "SMOTE",
            "Técnica que genera ejemplos sintéticos de la clase minoritaria."
        ),
        (
            "Class Weight",
            "Asignación de diferentes pesos a las clases durante el entrenamiento."
        ),
        (
            "Data Leakage",
            "Uso indebido de información que no debería estar disponible durante el entrenamiento."
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
            doc_subtitle="Módulo 1 - Material 5: Selección de Características",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()