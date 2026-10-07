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
    "M1-T5-Seleccion-de-Caracteristicas-y-Desbalanceo-Actividades.pdf"
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
            "Módulo 1 - Material 5: Actividades"
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
        title="Actividades - Selección de Características y Desbalanceo",
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
            "Selección de Características y Tratamiento del Desbalanceo",
            styles["DocTitle"]
        )
    )

    story.append(
        Paragraph(
            "Actividades prácticas — Feature Selection, métricas y SMOTE",
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
            "Aplicar técnicas de selección de características y estrategias "
            "para trabajar con datasets desbalanceados, prestando especial "
            "atención a la evaluación y a la prevención de Data Leakage.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 1
    # ========================================================

    activity_title(
        story,
        1,
        "Identificar características relevantes",
        styles
    )

    story.append(
        Paragraph(
            "Imagina un modelo que debe predecir si un cliente abandonará "
            "un servicio. Analiza las siguientes variables:",
            styles["BodyCustom"]
        )
    )

    variables = [
        "edad",
        "ingresos",
        "color_favorito",
        "cantidad_meses_cliente",
        "cantidad_llamadas_soporte",
        "tipo_plan",
        "fecha_ultimo_contacto",
        "ID_cliente",
        "nombre_cliente",
    ]

    for variable in variables:
        story.append(
            Paragraph(
                f"<b>{variable}</b> → "
                "¿Relevante / posiblemente relevante / irrelevante?",
                styles["BulletCustom"]
            )
        )

    story.append(
        Paragraph(
            "Justifica especialmente tus decisiones sobre ID_cliente "
            "y nombre_cliente.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 2
    # ========================================================

    activity_title(
        story,
        2,
        "Detectar características redundantes",
        styles
    )

    story.append(
        Paragraph(
            "Supón que un dataset contiene:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "ingresos_anuales<br/>"
            "ingresos_mensuales<br/>"
            "edad<br/>"
            "cantidad_productos",
            styles["CodeCustom"]
        )
    )

    for item in [
        "¿Qué variables podrían contener información redundante?",
        "¿Qué análisis realizarías para comprobarlo?",
        "¿Eliminarías automáticamente alguna de ellas?",
        "¿Qué información adicional necesitarías para decidir?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 3
    # ========================================================

    activity_title(
        story,
        3,
        "Analizar correlaciones",
        styles
    )

    story.append(
        Paragraph(
            "Carga un dataset numérico y genera una matriz de correlación.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "correlacion = df.corr(numeric_only=True)<br/>"
            "print(correlacion)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Luego utiliza un mapa de calor:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import seaborn as sns<br/>"
            "import matplotlib.pyplot as plt<br/><br/>"
            "sns.heatmap(correlacion, annot=True)<br/>"
            "plt.show()",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Identifica al menos dos pares de variables con alta relación "
            "y analiza si existe una posible redundancia.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 4
    # ========================================================

    activity_title(
        story,
        4,
        "Aplicar VarianceThreshold",
        styles
    )

    story.append(
        Paragraph(
            "Crea un dataset que contenga una variable constante:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "import pandas as pd<br/><br/>"
            "X = pd.DataFrame({<br/>"
            "    'edad': [20, 25, 30, 35, 40],<br/>"
            "    'ingresos': [20000, 25000, 30000, 35000, 40000],<br/>"
            "    'constante': [1, 1, 1, 1, 1]<br/>"
            "})",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Aplica:",
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
            "¿Qué característica fue eliminada? ¿Por qué?",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 5
    # ========================================================

    activity_title(
        story,
        5,
        "Aplicar SelectKBest",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza un dataset de clasificación y selecciona las "
            "cinco mejores características.",
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

    for item in [
        "¿Cuántas características tenía el dataset originalmente?",
        "¿Cuántas quedaron después de la selección?",
        "¿Cuáles fueron seleccionadas?",
        "¿Qué puntuación obtuvo cada una?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 6
    # ========================================================

    activity_title(
        story,
        6,
        "Mutual Information",
        styles
    )

    story.append(
        Paragraph(
            "Calcula la información mutua entre las características "
            "y la variable objetivo.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import mutual_info_classif<br/><br/>"
            "scores = mutual_info_classif(<br/>"
            "    X,<br/>"
            "    y,<br/>"
            "    random_state=42<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Ordena las características desde la mayor hasta la menor "
            "puntuación y analiza el resultado.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 7
    # ========================================================

    activity_title(
        story,
        7,
        "Recursive Feature Elimination",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza RFE para seleccionar cinco características:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.feature_selection import RFE<br/>"
            "from sklearn.linear_model import LogisticRegression<br/><br/>"
            "model = LogisticRegression(max_iter=1000)<br/>"
            "selector = RFE(model, n_features_to_select=5)<br/>"
            "selector.fit(X, y)",
            styles["CodeCustom"]
        )
    )

    for item in [
        "¿Qué características fueron seleccionadas?",
        "¿Qué características fueron descartadas?",
        "¿Coinciden con las seleccionadas mediante SelectKBest?",
        "¿Por qué pueden producir resultados diferentes?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 8
    # ========================================================

    activity_title(
        story,
        8,
        "Importancia de características con Random Forest",
        styles
    )

    story.append(
        Paragraph(
            "Entrena un Random Forest y analiza la importancia "
            "de sus características.",
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
            "Ordena las características según su importancia y "
            "selecciona las cinco primeras.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 9
    # ========================================================

    activity_title(
        story,
        9,
        "Comparar métodos de selección",
        styles
    )

    story.append(
        Paragraph(
            "Compara los resultados obtenidos mediante:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Correlación.",
        "VarianceThreshold.",
        "SelectKBest.",
        "Mutual Information.",
        "RFE.",
        "Random Forest.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Construye una tabla donde indiques qué características "
            "seleccionó cada método.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 10
    # ========================================================

    activity_title(
        story,
        10,
        "Detectar desbalanceo",
        styles
    )

    story.append(
        Paragraph(
            "Considera la siguiente distribución:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "Clase 0: 9500<br/>"
            "Clase 1: 500",
            styles["CodeCustom"]
        )
    )

    for item in [
        "Calcula el porcentaje de cada clase.",
        "¿Existe desbalanceo?",
        "¿Cuál es la clase minoritaria?",
        "¿Qué problemas podría generar durante el entrenamiento?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 11
    # ========================================================

    activity_title(
        story,
        11,
        "Analizar un dataset desbalanceado",
        styles
    )

    story.append(
        Paragraph(
            "Carga un dataset de clasificación y analiza la cantidad "
            "de observaciones de cada clase.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "print(y.value_counts())<br/>"
            "print(y.value_counts(normalize=True))",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Representa gráficamente la distribución y escribe "
            "una conclusión.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 12
    # ========================================================

    activity_title(
        story,
        12,
        "Analizar Accuracy, Precision, Recall y F1",
        styles
    )

    story.append(
        Paragraph(
            "Entrena un modelo de clasificación y calcula:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score<br/><br/>"
            "print('Accuracy:', accuracy_score(y_test, y_pred))<br/>"
            "print('Precision:', precision_score(y_test, y_pred))<br/>"
            "print('Recall:', recall_score(y_test, y_pred))<br/>"
            "print('F1:', f1_score(y_test, y_pred))",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Explica qué métrica consideras más importante para detectar "
            "correctamente la clase minoritaria y por qué.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 13
    # ========================================================

    activity_title(
        story,
        13,
        "Interpretar una matriz de confusión",
        styles
    )

    story.append(
        Paragraph(
            "Supón que obtienes:",
            styles["BodyCustom"]
        )
    )

    confusion = [
        [
            Paragraph("", styles["TableHeader"]),
            Paragraph("Pred. 0", styles["TableHeader"]),
            Paragraph("Pred. 1", styles["TableHeader"]),
        ],
        [
            Paragraph("Real 0", styles["TableCellBold"]),
            Paragraph("850", styles["TableCell"]),
            Paragraph("100", styles["TableCell"]),
        ],
        [
            Paragraph("Real 1", styles["TableCellBold"]),
            Paragraph("30", styles["TableCell"]),
            Paragraph("20", styles["TableCell"]),
        ],
    ]

    table = Table(
        confusion,
        colWidths=[160, 172, 172],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(table)

    for item in [
        "Identifica TP, TN, FP y FN.",
        "¿Cuántos casos positivos reales fueron detectados?",
        "¿Cuántos positivos fueron omitidos?",
        "¿Qué problema observas?",
    ]:
        story.append(bullet(item, styles))

    # ========================================================
    # ACTIVIDAD 14
    # ========================================================

    activity_title(
        story,
        14,
        "Class Weight",
        styles
    )

    story.append(
        Paragraph(
            "Entrena un modelo con y sin:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "class_weight='balanced'",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Compara Precision, Recall y F1-score.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 15
    # ========================================================

    activity_title(
        story,
        15,
        "Random Oversampling",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza RandomOverSampler para aumentar la representación "
            "de la clase minoritaria.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from imblearn.over_sampling import RandomOverSampler<br/><br/>"
            "ros = RandomOverSampler(random_state=42)<br/>"
            "X_resampled, y_resampled = ros.fit_resample(X_train, y_train)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Compara la cantidad de observaciones antes y después.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 16
    # ========================================================

    activity_title(
        story,
        16,
        "Random Undersampling",
        styles
    )

    story.append(
        Paragraph(
            "Utiliza RandomUnderSampler:",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from imblearn.under_sampling import RandomUnderSampler<br/><br/>"
            "rus = RandomUnderSampler(random_state=42)<br/>"
            "X_resampled, y_resampled = rus.fit_resample(X_train, y_train)",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Analiza qué ventaja y qué posible desventaja presenta "
            "esta estrategia.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 17
    # ========================================================

    activity_title(
        story,
        17,
        "Aplicar SMOTE",
        styles
    )

    story.append(
        Paragraph(
            "Aplica SMOTE exclusivamente sobre el conjunto de entrenamiento.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "from imblearn.over_sampling import SMOTE<br/><br/>"
            "smote = SMOTE(random_state=42)<br/>"
            "X_train_smote, y_train_smote = smote.fit_resample(<br/>"
            "    X_train,<br/>"
            "    y_train<br/>"
            ")",
            styles["CodeCustom"]
        )
    )

    story.append(
        Paragraph(
            "Comprueba la distribución de las clases antes y después.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 18
    # ========================================================

    activity_title(
        story,
        18,
        "Comparar estrategias de balanceo",
        styles
    )

    story.append(
        Paragraph(
            "Entrena el mismo modelo utilizando:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Sin balanceo.",
        "Class Weight.",
        "Random Oversampling.",
        "Random Undersampling.",
        "SMOTE.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Construye una tabla con Accuracy, Precision, Recall y F1-score.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 19
    # ========================================================

    activity_title(
        story,
        19,
        "Detectar Data Leakage",
        styles
    )

    story.append(
        Paragraph(
            "Determina si las siguientes situaciones son correctas "
            "o incorrectas:",
            styles["BodyCustom"]
        )
    )

    situations = [
        [
            Paragraph("Situación", styles["TableHeader"]),
            Paragraph("¿Correcto?", styles["TableHeader"]),
            Paragraph("Justificación", styles["TableHeader"]),
        ],
        [
            Paragraph(
                "Aplicar SMOTE antes de train_test_split.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Aplicar SMOTE solamente a X_train e y_train.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Seleccionar características usando todo el dataset antes de separar.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
        [
            Paragraph(
                "Utilizar Pipeline para integrar la selección.",
                styles["TableCell"]
            ),
            "",
            "",
        ],
    ]

    table = Table(
        situations,
        colWidths=[230, 85, 189],
        rowHeights=[30, 55, 55, 55, 55],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
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
    # ACTIVIDAD 20
    # ========================================================

    activity_title(
        story,
        20,
        "Construir un Pipeline con SMOTE",
        styles
    )

    story.append(
        Paragraph(
            "Construye un Pipeline que incluya escalado, SMOTE "
            "y un modelo de clasificación.",
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
            "Entrena el pipeline y evalúa el resultado sobre X_test.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 21
    # ========================================================

    activity_title(
        story,
        21,
        "Combinar Feature Selection y SMOTE",
        styles
    )

    story.append(
        Paragraph(
            "Construye un flujo que realice:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "Selección de características.",
        "Escalado.",
        "SMOTE.",
        "Modelo de clasificación.",
    ]:
        story.append(bullet(item, styles))

    story.append(
        Paragraph(
            "Utiliza un Pipeline y explica por qué el orden elegido "
            "es adecuado.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD 22
    # ========================================================

    activity_title(
        story,
        22,
        "Comparar modelos y estrategias",
        styles
    )

    story.append(
        Paragraph(
            "Construye una tabla final donde compares al menos "
            "tres configuraciones:",
            styles["BodyCustom"]
        )
    )

    comparison = [
        [
            Paragraph("Configuración", styles["TableHeader"]),
            Paragraph("Accuracy", styles["TableHeader"]),
            Paragraph("Precision", styles["TableHeader"]),
            Paragraph("Recall", styles["TableHeader"]),
            Paragraph("F1", styles["TableHeader"]),
        ],
        [
            Paragraph("Modelo sin balanceo", styles["TableCell"]),
            "",
            "",
            "",
            "",
        ],
        [
            Paragraph("Modelo + class_weight", styles["TableCell"]),
            "",
            "",
            "",
            "",
        ],
        [
            Paragraph("Modelo + SMOTE", styles["TableCell"]),
            "",
            "",
            "",
            "",
        ],
    ]

    table = Table(
        comparison,
        colWidths=[160, 86, 86, 86, 86],
        rowHeights=[30, 45, 45, 45],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)

    story.append(
        Paragraph(
            "Escribe una conclusión justificando qué configuración "
            "elegirías y por qué.",
            styles["BodyCustom"]
        )
    )

    # ========================================================
    # ACTIVIDAD INTEGRADORA
    # ========================================================

    story.append(
        Paragraph(
            "Actividad Integradora — Preparación profesional de un dataset",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Consigna</b><br/><br/>"
            "Selecciona un dataset de clasificación que presente varias "
            "características y, preferentemente, cierto grado de "
            "desbalanceo entre sus clases. Realiza un proceso completo "
            "de preparación profesional de los datos.",
            styles["BodyCustom"]
        )
    )

    story.append(
        Paragraph(
            "El trabajo deberá incluir:",
            styles["BodyCustom"]
        )
    )

    for item in [
        "1. Descripción del problema.",
        "2. Descripción del dataset.",
        "3. Distribución de la variable objetivo.",
        "4. Identificación de características relevantes e irrelevantes.",
        "5. Análisis de características redundantes.",
        "6. Aplicación de al menos un método Filter.",
        "7. Aplicación de al menos un método Wrapper o Embedded.",
        "8. Comparación de los métodos de selección.",
        "9. Separación correcta entre entrenamiento y prueba.",
        "10. Selección de una estrategia para el desbalanceo.",
        "11. Aplicación de Class Weight, Oversampling, Undersampling o SMOTE.",
        "12. Comparación de las estrategias utilizadas.",
        "13. Evaluación mediante Precision, Recall y F1-score.",
        "14. Análisis de la matriz de confusión.",
        "15. Construcción de un Pipeline.",
        "16. Verificación de posibles casos de Data Leakage.",
        "17. Conclusiones y justificación de las decisiones.",
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
            "1. ¿Qué es Feature Selection?",
            "Es el proceso de seleccionar las características más útiles para un modelo."
        ),
        (
            "2. ¿Cuál es la diferencia entre Feature Engineering y Feature Selection?",
            "Feature Engineering crea o transforma variables; Feature Selection elige cuáles conservar."
        ),
        (
            "3. ¿Qué hace VarianceThreshold?",
            "Elimina características con una variabilidad inferior al umbral establecido."
        ),
        (
            "4. ¿Para qué sirve SelectKBest?",
            "Selecciona las K características con mejor puntuación según una función estadística."
        ),
        (
            "5. ¿Qué significa que un dataset esté desbalanceado?",
            "Que las clases tienen cantidades significativamente diferentes de observaciones."
        ),
        (
            "6. ¿Por qué Accuracy puede ser engañosa?",
            "Porque un modelo puede favorecer la clase mayoritaria y obtener alta Accuracy sin detectar correctamente la minoritaria."
        ),
        (
            "7. ¿Qué mide Recall?",
            "La proporción de casos positivos reales que el modelo consigue detectar."
        ),
        (
            "8. ¿Qué es SMOTE?",
            "Una técnica de sobremuestreo que genera ejemplos sintéticos de la clase minoritaria."
        ),
        (
            "9. ¿Dónde debe aplicarse SMOTE?",
            "Sobre el conjunto de entrenamiento, dentro del proceso de entrenamiento."
        ),
        (
            "10. ¿Qué problema evita un Pipeline?",
            "Ayuda a mantener las transformaciones dentro del flujo correcto y reduce riesgos de Data Leakage."
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
            "Cierre del Módulo 1",
            styles["H2Custom"]
        )
    )

    add_card(
        story,
        Paragraph(
            "<b>Del dato al modelo.</b><br/><br/>"
            "A lo largo del Módulo 1 se construyó un pipeline profesional "
            "de preparación de datos: comprensión del problema, EDA, "
            "limpieza, imputación, Feature Engineering, selección de "
            "características y tratamiento del desbalanceo.<br/><br/>"
            "El siguiente paso será utilizar estos datos preparados "
            "para construir y optimizar modelos supervisados.",
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
            doc_subtitle="Módulo 1 - Material 5: Actividades",
            **kwargs
        )
    )

    print(f"PDF generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()
    