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
# CONFIGURACIÓN GENERAL
# ============================================================

OUTPUT_DIR = "pdf"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CANVAS NUMERADO
# ============================================================

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop("doc_subtitle", "")
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

        teal = colors.HexColor("#0d9488")
        gray = colors.HexColor("#64748b")

        page_width, page_height = letter

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(teal)

        self.drawString(
            54,
            page_height - 35,
            "CURSOS CC"
        )

        self.setStrokeColor(teal)
        self.setLineWidth(0.8)

        self.line(
            54,
            page_height - 42,
            page_width - 54,
            page_height - 42
        )

        self.setFont("Helvetica", 7.5)
        self.setFillColor(gray)

        self.drawString(
            54,
            page_height - 55,
            self.doc_subtitle.upper()
        )

        self.drawRightString(
            page_width - 54,
            page_height - 55,
            f"Página {self._pageNumber} de {total_pages}"
        )

        # ----------------------------------------------------
        # PIE DE PÁGINA
        # ----------------------------------------------------

        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)

        self.line(
            54,
            38,
            page_width - 54,
            38
        )

        self.setFont("Helvetica", 7)
        self.setFillColor(gray)

        self.drawString(
            54,
            25,
            "Material educativo • Módulo 1 - Tema 1: Metodología de Proyectos de Machine Learning y CRISP-DM"
        )


# ============================================================
# ESTILOS
# ============================================================

def get_common_styles():

    styles = getSampleStyleSheet()

    primary = colors.HexColor("#0f172a")
    accent = colors.HexColor("#0d9488")
    text = colors.HexColor("#334155")
    light = colors.HexColor("#f1f5f9")
    border = colors.HexColor("#cbd5e1")
    white = colors.white

    styles.add(
        ParagraphStyle(
            name="ModuleTag",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=accent,
            spaceAfter=6,
            textTransform="uppercase",
        )
    )

    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=primary,
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
            textColor=text,
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Heading2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=primary,
            spaceBefore=12,
            spaceAfter=7,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Heading3Custom",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=accent,
            spaceBefore=9,
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
            textColor=text,
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
            textColor=text,
            leftIndent=16,
            firstLineIndent=-8,
            bulletIndent=5,
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
            textColor=primary,
            backColor=light,
            borderColor=border,
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=5,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=white,
            alignment=0,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=text,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCellBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=10,
            textColor=primary,
        )
    )

    return styles


# ============================================================
# TARJETA DE CONTENIDO
# ============================================================

def content_card(content, width=504):

    table = Table(
        [[content]],
        colWidths=[width],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    return table


# ============================================================
# TABLA CRISP-DM
# ============================================================

def crisp_dm_table(styles):

    data = [
        [
            Paragraph("Fase", styles["TableHeader"]),
            Paragraph("Propósito", styles["TableHeader"]),
            Paragraph("Preguntas orientadoras", styles["TableHeader"]),
        ],
        [
            Paragraph("1. Comprensión del negocio", styles["TableCellBold"]),
            Paragraph(
                "Comprender el problema, los objetivos y el contexto en el que se utilizará el modelo.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿Qué problema queremos resolver? ¿Qué resultado sería útil para la organización?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("2. Comprensión de los datos", styles["TableCellBold"]),
            Paragraph(
                "Conocer los datos disponibles, su estructura, calidad y posibles relaciones.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿Qué datos tenemos? ¿Son suficientes? ¿Qué problemas de calidad presentan?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("3. Preparación de los datos", styles["TableCellBold"]),
            Paragraph(
                "Transformar los datos para dejarlos preparados para el entrenamiento de modelos.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿Qué variables debemos limpiar, transformar, codificar o seleccionar?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("4. Modelado", styles["TableCellBold"]),
            Paragraph(
                "Seleccionar, entrenar y comparar modelos de Machine Learning.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿Qué algoritmo es apropiado? ¿Qué configuración permite obtener mejores resultados?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("5. Evaluación", styles["TableCellBold"]),
            Paragraph(
                "Determinar si el modelo resuelve adecuadamente el problema planteado.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿El modelo cumple el objetivo? ¿Su rendimiento es suficiente para utilizarlo?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("6. Despliegue", styles["TableCellBold"]),
            Paragraph(
                "Poner el modelo o sus resultados a disposición de los usuarios o sistemas que lo necesitan.",
                styles["TableCell"],
            ),
            Paragraph(
                "¿Cómo se utilizará el modelo? ¿Cómo se mantendrá y monitoreará?",
                styles["TableCell"],
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
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0f172a"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "BACKGROUND",
                    (0, 3),
                    (-1, 3),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "BACKGROUND",
                    (0, 5),
                    (-1, 5),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    return table


# ============================================================
# CREAR PDF TEÓRICO
# ============================================================

def create_theory_pdf():

    output_path = os.path.join(
        OUTPUT_DIR,
        "M1-T1-Metodologia-ML-CRISP-DM-Teoria.pdf",
    )

    styles = get_common_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54,
        title="Metodología de Proyectos de Machine Learning y CRISP-DM",
        author="Cursos CC",
    )

    story = []

    # --------------------------------------------------------
    # PORTADA / TÍTULO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "MÓDULO 1 · TEMA 1",
            styles["ModuleTag"],
        )
    )

    story.append(
        Paragraph(
            "Metodología de Proyectos de Machine Learning y CRISP-DM",
            styles["DocTitle"],
        )
    )

    story.append(
        Paragraph(
            "Material teórico · Fundamentos, metodología y definición del problema",
            styles["DocSubtitle"],
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#0d9488"),
            spaceBefore=2,
            spaceAfter=14,
        )
    )

    # --------------------------------------------------------
    # PRESENTACIÓN
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Presentación",
            styles["Heading2Custom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "Un proyecto de Machine Learning no comienza con la elección de un algoritmo. "
                "Comienza con la comprensión de un problema real, la definición de un objetivo "
                "medible y el análisis de los datos disponibles. En este tema se presenta una "
                "metodología de trabajo que permite organizar el desarrollo de proyectos de "
                "Machine Learning de manera sistemática.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "Objetivos de aprendizaje",
            styles["Heading2Custom"],
        )
    )

    objetivos = [
        "Comprender qué implica desarrollar un proyecto de Machine Learning.",
        "Diferenciar un problema de negocio de un problema de Machine Learning.",
        "Reconocer las etapas principales de la metodología CRISP-DM.",
        "Identificar objetivos, variables objetivo y características de un problema.",
        "Relacionar distintos tipos de problemas con tareas de Machine Learning.",
        "Comprender el carácter iterativo de los proyectos de datos y Machine Learning.",
    ]

    for objetivo in objetivos:
        story.append(
            Paragraph(
                f"• {objetivo}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # 1. MACHINE LEARNING COMO PROYECTO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. Machine Learning como proyecto",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Machine Learning es una disciplina que permite construir sistemas capaces de "
            "aprender patrones a partir de datos para realizar predicciones, clasificaciones, "
            "agrupamientos o detecciones. Sin embargo, un modelo técnicamente correcto no "
            "garantiza que el proyecto sea útil.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "Un proyecto profesional de Machine Learning combina diferentes actividades: "
            "comprender el problema, obtener y analizar datos, prepararlos, construir modelos, "
            "evaluarlos y finalmente integrar los resultados en un contexto real.",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Idea clave:</b> el objetivo de un proyecto de Machine Learning no es "
                "simplemente construir el modelo con mayor precisión posible, sino resolver "
                "un problema relevante mediante el uso adecuado de datos y modelos.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # 2. PROBLEMA DE NEGOCIO VS ML
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "2. Problema de negocio y problema de Machine Learning",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "El punto de partida debe ser el problema que se desea resolver. Este problema "
            "puede pertenecer a una empresa, institución educativa, organización, servicio "
            "público o cualquier otro contexto.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "Por ejemplo, una empresa puede plantear el siguiente problema:",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Problema de negocio:</b> muchos clientes abandonan el servicio y la empresa "
                "quiere anticipar cuáles presentan mayor riesgo de abandono.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(
        Spacer(1, 6)
    )

    story.append(
        Paragraph(
            "Este problema puede transformarse en un problema de Machine Learning:",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Problema de Machine Learning:</b> construir un modelo de clasificación "
                "capaz de estimar si un cliente probablemente abandonará el servicio.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(
        Paragraph(
            "La transformación es importante porque permite determinar qué datos se necesitan, "
            "qué variable se quiere predecir y qué tipo de modelo puede ser adecuado.",
            styles["BodyCustom"],
        )
    )

    # --------------------------------------------------------
    # 3. DEFINICIÓN DEL PROBLEMA
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. De la pregunta de negocio a la tarea de Machine Learning",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Antes de comenzar a programar es necesario formular una pregunta concreta. "
            "Una buena pregunta debe permitir establecer posteriormente cómo se medirá el "
            "éxito del proyecto.",
            styles["BodyCustom"],
        )
    )

    tabla_problema = [
        [
            Paragraph("Elemento", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
        ],
        [
            Paragraph("Problema", styles["TableCellBold"]),
            Paragraph(
                "La empresa pierde clientes y quiere reducir la cantidad de abandonos.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Pregunta", styles["TableCellBold"]),
            Paragraph(
                "¿Podemos identificar anticipadamente a los clientes con mayor riesgo?",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Objetivo", styles["TableCellBold"]),
            Paragraph(
                "Predecir la probabilidad de abandono de cada cliente.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Variable objetivo", styles["TableCellBold"]),
            Paragraph(
                "Abandonó: sí/no.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Tipo de problema", styles["TableCellBold"]),
            Paragraph(
                "Clasificación binaria.",
                styles["TableCell"],
            ),
        ],
    ]

    table = Table(
        tabla_problema,
        colWidths=[145, 359],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------------
    # 4. CRISP-DM
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "4. Metodología CRISP-DM",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "CRISP-DM significa <b>Cross-Industry Standard Process for Data Mining</b>. "
            "Es una metodología que organiza los proyectos relacionados con datos en etapas "
            "claramente diferenciadas.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "Aunque fue desarrollada originalmente para proyectos de minería de datos, "
            "sus principios continúan siendo útiles para estructurar proyectos actuales "
            "de Data Science y Machine Learning.",
            styles["BodyCustom"],
        )
    )

    story.append(Spacer(1, 5))

    story.append(crisp_dm_table(styles))

    # --------------------------------------------------------
    # 5. COMPRENSIÓN DEL NEGOCIO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "5. Fase 1: Comprensión del negocio",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "En esta etapa se define qué problema se quiere resolver y por qué es importante. "
            "No se comienza todavía seleccionando algoritmos.",
            styles["BodyCustom"],
        )
    )

    preguntas = [
        "¿Cuál es el problema concreto?",
        "¿Quién utilizará los resultados?",
        "¿Qué decisión se quiere mejorar?",
        "¿Qué resultado se considera exitoso?",
        "¿Qué restricciones existen?",
        "¿Cómo se medirá el impacto?",
    ]

    for pregunta in preguntas:
        story.append(
            Paragraph(
                f"• {pregunta}",
                styles["BulletCustom"],
            )
        )

    story.append(
        content_card(
            Paragraph(
                "<b>Ejemplo:</b> una institución educativa quiere detectar estudiantes "
                "con riesgo de abandonar un curso para poder ofrecer apoyo antes de que "
                "se produzca el abandono.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # 6. COMPRENSIÓN DE LOS DATOS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "6. Fase 2: Comprensión de los datos",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Una vez definido el problema, se analiza qué datos están disponibles. "
            "En esta etapa se estudian las fuentes, estructura, tipos de variables, "
            "cantidad de registros y posibles problemas de calidad.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "Algunas preguntas iniciales son:",
            styles["BodyCustom"],
        )
    )

    for item in [
        "¿Cuántos registros existen?",
        "¿Qué variables están disponibles?",
        "¿Existen valores faltantes?",
        "¿Hay valores atípicos?",
        "¿Existen errores o inconsistencias?",
        "¿Los datos representan adecuadamente el problema?",
    ]:
        story.append(
            Paragraph(
                f"• {item}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # 7. PREPARACIÓN
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "7. Fase 3: Preparación de los datos",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "La preparación transforma los datos originales en un conjunto adecuado para "
            "el modelado. Puede incluir limpieza, tratamiento de valores faltantes, "
            "codificación de variables categóricas, escalado, creación de nuevas variables "
            "y selección de características.",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Importante:</b> la preparación de datos suele ocupar una parte considerable "
                "del trabajo de un proyecto de Machine Learning. La calidad de los datos puede "
                "tener un impacto mayor que la elección de un algoritmo sofisticado.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # 8. MODELADO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "8. Fase 4: Modelado",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "En esta etapa se seleccionan y entrenan modelos de Machine Learning. "
            "La elección depende del tipo de problema, de los datos disponibles, "
            "de las restricciones y de los objetivos definidos.",
            styles["BodyCustom"],
        )
    )

    model_table = [
        [
            Paragraph("Tarea", styles["TableHeader"]),
            Paragraph("Ejemplos de modelos", styles["TableHeader"]),
        ],
        [
            Paragraph("Clasificación", styles["TableCellBold"]),
            Paragraph(
                "Regresión logística, árboles de decisión, Random Forest, SVM.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Regresión", styles["TableCellBold"]),
            Paragraph(
                "Regresión lineal, Ridge, Lasso, árboles de regresión.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Clustering", styles["TableCellBold"]),
            Paragraph(
                "K-Means, DBSCAN, clustering jerárquico.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Detección de anomalías", styles["TableCellBold"]),
            Paragraph(
                "Métodos estadísticos y algoritmos específicos de detección de anomalías.",
                styles["TableCell"],
            ),
        ],
    ]

    model_table_obj = Table(
        model_table,
        colWidths=[150, 354],
    )

    model_table_obj.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(model_table_obj)

    # --------------------------------------------------------
    # 9. EVALUACIÓN
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "9. Fase 5: Evaluación",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Un modelo debe evaluarse en relación con el problema original. "
            "No alcanza con observar que el algoritmo produce resultados: es necesario "
            "determinar si esos resultados son suficientemente buenos y si permiten "
            "cumplir el objetivo planteado.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "Las métricas utilizadas dependen del tipo de problema. Por ejemplo, en "
            "clasificación pueden utilizarse accuracy, precision, recall o F1-score. "
            "En regresión pueden utilizarse MAE, MSE o RMSE.",
            styles["BodyCustom"],
        )
    )

    # --------------------------------------------------------
    # 10. DESPLIEGUE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "10. Fase 6: Despliegue",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "El despliegue consiste en poner el modelo o sus resultados a disposición "
            "de quienes los necesitan. Dependiendo del proyecto, esto puede implicar "
            "integrarlo en una aplicación, una API, un sistema interno o un proceso "
            "automatizado.",
            styles["BodyCustom"],
        )
    )

    story.append(
        Paragraph(
            "El despliegue no significa que el proyecto haya terminado definitivamente. "
            "Los datos pueden cambiar y el rendimiento del modelo puede disminuir, por lo "
            "que es necesario considerar mantenimiento y monitoreo.",
            styles["BodyCustom"],
        )
    )

    # --------------------------------------------------------
    # 11. PROCESO ITERATIVO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "11. CRISP-DM como proceso iterativo",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Las fases de CRISP-DM no deben interpretarse como una secuencia rígida que "
            "solo puede recorrerse una vez. En un proyecto real es frecuente volver a "
            "etapas anteriores.",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Ejemplo:</b> durante la evaluación puede descubrirse que el modelo "
                "no funciona correctamente para determinados grupos. Esto puede llevar "
                "a regresar a la fase de comprensión de los datos o de preparación para "
                "investigar el problema.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # 12. TARGET Y FEATURES
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "12. Variable objetivo y características",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "En los problemas supervisados es importante distinguir entre la variable "
            "que se desea predecir y las variables utilizadas para realizar la predicción.",
            styles["BodyCustom"],
        )
    )

    feature_table = [
        [
            Paragraph("Concepto", styles["TableHeader"]),
            Paragraph("Descripción", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
        ],
        [
            Paragraph("Variable objetivo (target)", styles["TableCellBold"]),
            Paragraph(
                "Variable que el modelo intenta predecir.",
                styles["TableCell"],
            ),
            Paragraph(
                "Abandono del cliente: sí/no.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Características (features)", styles["TableCellBold"]),
            Paragraph(
                "Variables utilizadas como información de entrada para el modelo.",
                styles["TableCell"],
            ),
            Paragraph(
                "Edad, antigüedad, cantidad de compras, frecuencia de uso.",
                styles["TableCell"],
            ),
        ],
    ]

    feature_table_obj = Table(
        feature_table,
        colWidths=[130, 190, 184],
    )

    feature_table_obj.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(feature_table_obj)

    # --------------------------------------------------------
    # 13. TIPOS DE PROBLEMAS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "13. Tipos de problemas de Machine Learning",
            styles["Heading2Custom"],
        )
    )

    problem_table = [
        [
            Paragraph("Tipo", styles["TableHeader"]),
            Paragraph("Objetivo", styles["TableHeader"]),
            Paragraph("Ejemplo", styles["TableHeader"]),
        ],
        [
            Paragraph("Clasificación", styles["TableCellBold"]),
            Paragraph(
                "Asignar una observación a una categoría.",
                styles["TableCell"],
            ),
            Paragraph(
                "Determinar si un correo es spam.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Regresión", styles["TableCellBold"]),
            Paragraph(
                "Predecir un valor numérico.",
                styles["TableCell"],
            ),
            Paragraph(
                "Predecir el precio de una vivienda.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Clustering", styles["TableCellBold"]),
            Paragraph(
                "Agrupar observaciones según similitud.",
                styles["TableCell"],
            ),
            Paragraph(
                "Segmentar clientes.",
                styles["TableCell"],
            ),
        ],
        [
            Paragraph("Anomalías", styles["TableCellBold"]),
            Paragraph(
                "Detectar observaciones inusuales.",
                styles["TableCell"],
            ),
            Paragraph(
                "Detectar transacciones sospechosas.",
                styles["TableCell"],
            ),
        ],
    ]

    problem_table_obj = Table(
        problem_table,
        colWidths=[110, 190, 204],
    )

    problem_table_obj.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(problem_table_obj)

    # --------------------------------------------------------
    # 14. CASO COMPLETO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "14. Caso integrador: predicción de abandono de clientes",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Una empresa de servicios quiere disminuir la cantidad de clientes que "
            "abandonan sus servicios. Para ello dispone de información histórica.",
            styles["BodyCustom"],
        )
    )

    caso = [
        "Problema de negocio: reducir el abandono de clientes.",
        "Pregunta: ¿podemos anticipar qué clientes tienen mayor riesgo?",
        "Objetivo de Machine Learning: predecir el abandono.",
        "Target: abandono.",
        "Features: antigüedad, frecuencia de uso, cantidad de reclamos, tipo de plan y gasto mensual.",
        "Tipo de problema: clasificación.",
        "Evaluación: utilizar métricas apropiadas para determinar la capacidad predictiva.",
        "Uso del modelo: generar alertas para orientar acciones de retención.",
    ]

    for item in caso:
        story.append(
            Paragraph(
                f"• {item}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # 15. ERRORES FRECUENTES
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "15. Errores frecuentes al iniciar un proyecto",
            styles["Heading2Custom"],
        )
    )

    errores = [
        "Comenzar seleccionando un algoritmo sin comprender el problema.",
        "Utilizar todos los datos disponibles sin analizar su calidad.",
        "Confundir correlación con causalidad.",
        "No definir una variable objetivo clara cuando el problema es supervisado.",
        "Evaluar el modelo solamente con los datos utilizados para entrenarlo.",
        "Elegir métricas que no representan el objetivo real del proyecto.",
        "Ignorar las restricciones del contexto donde se utilizará el modelo.",
    ]

    for error in errores:
        story.append(
            Paragraph(
                f"• {error}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # 16. CRISP-DM Y PIPELINE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "16. CRISP-DM y el pipeline profesional",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "CRISP-DM proporciona una estructura general para organizar el proyecto. "
            "Dentro de sus etapas se desarrollan actividades técnicas concretas que forman "
            "parte de un pipeline de Machine Learning.",
            styles["BodyCustom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Ejemplo de recorrido:</b> problema → datos → exploración → limpieza → "
                "transformación → selección de características → entrenamiento → evaluación "
                "→ despliegue → monitoreo.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(
        Paragraph(
            "Los siguientes temas del módulo profundizarán especialmente en la preparación "
            "profesional de los datos, incluyendo exploración, limpieza, ingeniería de "
            "características, selección de variables y tratamiento del desbalanceo.",
            styles["BodyCustom"],
        )
    )

    # --------------------------------------------------------
    # 17. GLOSARIO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "17. Glosario básico",
            styles["Heading2Custom"],
        )
    )

    glossary = [
        ("Dataset", "Conjunto de datos utilizado en un proyecto."),
        ("Feature", "Variable utilizada como entrada de un modelo."),
        ("Target", "Variable que se desea predecir en aprendizaje supervisado."),
        ("Modelo", "Representación matemática o computacional aprendida a partir de datos."),
        ("Entrenamiento", "Proceso mediante el cual el modelo aprende patrones de los datos."),
        ("Evaluación", "Proceso de medir el desempeño del modelo."),
        ("Despliegue", "Integración del modelo en un entorno donde puede ser utilizado."),
        ("CRISP-DM", "Metodología para organizar proyectos de minería de datos y Machine Learning."),
    ]

    glossary_data = [
        [
            Paragraph("Concepto", styles["TableHeader"]),
            Paragraph("Definición", styles["TableHeader"]),
        ]
    ]

    for concept, definition in glossary:
        glossary_data.append(
            [
                Paragraph(concept, styles["TableCellBold"]),
                Paragraph(definition, styles["TableCell"]),
            ]
        )

    glossary_table = Table(
        glossary_data,
        colWidths=[130, 374],
        repeatRows=1,
    )

    glossary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(glossary_table)

    # --------------------------------------------------------
    # CIERRE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Síntesis",
            styles["Heading2Custom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "Un proyecto de Machine Learning comienza con una necesidad concreta y "
                "se desarrolla mediante un proceso organizado. CRISP-DM permite estructurar "
                "ese proceso en seis grandes fases: comprensión del negocio, comprensión "
                "de los datos, preparación, modelado, evaluación y despliegue. "
                "Comprender esta metodología permite abordar los temas técnicos posteriores "
                "con una visión profesional del proyecto completo.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # GENERACIÓN
    # --------------------------------------------------------

    canvas_builder = lambda filename, **kwargs: NumberedCanvas(
        filename,
        doc_subtitle="Metodología de Proyectos de Machine Learning y CRISP-DM - Teoría",
        **kwargs
    )

    doc.build(
        story,
        canvasmaker=canvas_builder,
    )

    print(f"PDF generado correctamente: {output_path}")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    create_theory_pdf()