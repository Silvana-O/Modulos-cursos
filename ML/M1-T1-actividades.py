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
        # PIE
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
            name="TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=white,
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
# CREAR PDF DE ACTIVIDADES
# ============================================================

def create_activities_pdf():

    output_path = os.path.join(
        OUTPUT_DIR,
        "M1-T1-Metodologia-ML-CRISP-DM-Actividades.pdf",
    )

    styles = get_common_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54,
        title="Actividades - Metodología de Proyectos de Machine Learning y CRISP-DM",
        author="Cursos CC",
    )

    story = []

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "MÓDULO 1 · TEMA 1",
            styles["ModuleTag"],
        )
    )

    story.append(
        Paragraph(
            "Actividades: Metodología de Proyectos de Machine Learning y CRISP-DM",
            styles["DocTitle"],
        )
    )

    story.append(
        Paragraph(
            "Guía práctica · Análisis, aplicación y autoevaluación",
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
                "Estas actividades tienen como objetivo aplicar los conceptos fundamentales "
                "de la metodología CRISP-DM y aprender a transformar una necesidad real en "
                "un problema abordable mediante Machine Learning.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(Spacer(1, 8))

    # --------------------------------------------------------
    # ACTIVIDAD 1
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 1 · ¿Problema de negocio o problema de Machine Learning?",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Lee cada situación e indica si corresponde principalmente a un problema de "
            "negocio o a una formulación de Machine Learning. Luego explica brevemente "
            "tu decisión.",
            styles["BodyCustom"],
        )
    )

    situaciones = [
        "Una empresa quiere reducir la cantidad de clientes que abandonan su servicio.",
        "Construir un modelo que prediga si un cliente abandonará durante los próximos meses.",
        "Una institución quiere disminuir la cantidad de estudiantes que abandonan un curso.",
        "Construir un clasificador que estime si un estudiante presenta riesgo de abandono.",
        "Una inmobiliaria quiere mejorar la estimación de precios de sus propiedades.",
        "Entrenar un modelo de regresión para estimar el precio de una vivienda.",
    ]

    for i, situacion in enumerate(situaciones, 1):
        story.append(
            Paragraph(
                f"<b>{i}.</b> {situacion}",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                "Respuesta: ________________________________________________________________",
                styles["BodyCustom"],
            )
        )

    # --------------------------------------------------------
    # ACTIVIDAD 2
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 2 · Transformar el problema",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Una plataforma educativa quiere identificar anticipadamente a los estudiantes "
            "que podrían abandonar un curso. Dispone de información sobre asistencia, "
            "calificaciones, cantidad de actividades entregadas, tiempo de conexión y "
            "participación.",
            styles["BodyCustom"],
        )
    )

    preguntas = [
        "¿Cuál es el problema de negocio?",
        "¿Cuál podría ser la pregunta de Machine Learning?",
        "¿Cuál sería la variable objetivo?",
        "¿Qué características podrían utilizarse?",
        "¿Se trata de clasificación, regresión, clustering o detección de anomalías?",
        "¿Qué decisión podría tomar la institución utilizando los resultados?",
    ]

    for i, pregunta in enumerate(preguntas, 1):
        story.append(
            Paragraph(
                f"<b>{i}.</b> {pregunta}",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                "________________________________________________________________________________",
                styles["BodyCustom"],
            )
        )

    # --------------------------------------------------------
    # ACTIVIDAD 3
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 3 · Identificar target y features",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Para cada caso, identifica la variable objetivo y al menos tres características "
            "que podrían utilizarse como entradas del modelo.",
            styles["BodyCustom"],
        )
    )

    casos = [
        (
            "Predicción del precio de una vivienda.",
            "Target: ____________________",
            "Features: ____________________, ____________________, ____________________",
        ),
        (
            "Predicción de si un correo electrónico es spam.",
            "Target: ____________________",
            "Features: ____________________, ____________________, ____________________",
        ),
        (
            "Predicción de abandono de un cliente.",
            "Target: ____________________",
            "Features: ____________________, ____________________, ____________________",
        ),
        (
            "Predicción de la cantidad de ventas del próximo mes.",
            "Target: ____________________",
            "Features: ____________________, ____________________, ____________________",
        ),
    ]

    for i, (caso, target, features) in enumerate(casos, 1):

        story.append(
            Paragraph(
                f"<b>{i}. {caso}</b>",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                target,
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                features,
                styles["BodyCustom"],
            )
        )

        story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # ACTIVIDAD 4
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 4 · Reconocer las fases de CRISP-DM",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Relaciona cada situación con la fase de CRISP-DM correspondiente.",
            styles["BodyCustom"],
        )
    )

    tabla_fases = [
        [
            Paragraph("Situación", styles["TableHeader"]),
            Paragraph("Fase", styles["TableHeader"]),
        ],
        [
            Paragraph(
                "La empresa define que quiere reducir el abandono de clientes.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
        [
            Paragraph(
                "Se analizan valores faltantes, tipos de datos y distribución de variables.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
        [
            Paragraph(
                "Se codifican variables categóricas y se preparan los datos.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
        [
            Paragraph(
                "Se entrenan diferentes algoritmos y se comparan sus resultados.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
        [
            Paragraph(
                "Se determina si el modelo cumple los objetivos definidos.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
        [
            Paragraph(
                "El modelo se integra a una aplicación utilizada por los usuarios.",
                styles["TableCell"],
            ),
            Paragraph("________________________", styles["TableCell"]),
        ],
    ]

    fases_table = Table(
        tabla_fases,
        colWidths=[380, 124],
        repeatRows=1,
    )

    fases_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(fases_table)

    # --------------------------------------------------------
    # ACTIVIDAD 5
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 5 · ¿Es necesario Machine Learning?",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Analiza las siguientes situaciones. Decide si Machine Learning sería una "
            "alternativa razonable y justifica tu respuesta.",
            styles["BodyCustom"],
        )
    )

    decisiones = [
        "Una institución necesita calcular el promedio de las calificaciones de sus estudiantes.",
        "Una empresa quiere predecir qué clientes tienen mayor probabilidad de abandonar.",
        "Una tienda quiere ordenar sus productos alfabéticamente.",
        "Una plataforma quiere agrupar clientes según sus hábitos de compra sin categorías previamente definidas.",
        "Un banco quiere detectar transacciones que presentan comportamientos inusuales.",
    ]

    for i, decision in enumerate(decisiones, 1):

        story.append(
            Paragraph(
                f"<b>{i}.</b> {decision}",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                "¿Usaría Machine Learning? __________",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                "Justificación: __________________________________________________________",
                styles["BodyCustom"],
            )
        )

    # --------------------------------------------------------
    # ACTIVIDAD 6
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 6 · Caso práctico: abandono de clientes",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Una empresa de telecomunicaciones posee un conjunto histórico de clientes. "
            "Para cada cliente registra edad, antigüedad, tipo de contrato, consumo mensual, "
            "cantidad de reclamos, cantidad de llamadas al soporte y si finalmente abandonó "
            "el servicio.",
            styles["BodyCustom"],
        )
    )

    preguntas_caso = [
        "Define el problema de negocio.",
        "Formula una pregunta que pueda resolverse mediante Machine Learning.",
        "Identifica el target.",
        "Identifica al menos cinco features.",
        "Determina el tipo de problema.",
        "Indica qué información sería necesario analizar antes de entrenar un modelo.",
        "Propón una forma de evaluar el modelo.",
        "Explica cómo podrían utilizarse los resultados.",
    ]

    for i, pregunta in enumerate(preguntas_caso, 1):

        story.append(
            Paragraph(
                f"<b>{i}.</b> {pregunta}",
                styles["BodyCustom"],
            )
        )

        story.append(
            Paragraph(
                "________________________________________________________________________________",
                styles["BodyCustom"],
            )
        )

    # --------------------------------------------------------
    # ACTIVIDAD 7
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 7 · Mi primer proyecto de Machine Learning",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Selecciona un problema de un contexto real que pueda beneficiarse del uso "
            "de datos. Puede estar relacionado con educación, comercio, transporte, "
            "salud, medio ambiente, industria, entretenimiento u otro ámbito.",
            styles["BodyCustom"],
        )
    )

    proyecto = [
        ("Contexto", "____________________________________________________________"),
        ("Problema de negocio", "____________________________________________________________"),
        ("Pregunta de Machine Learning", "____________________________________________________________"),
        ("Objetivo", "____________________________________________________________"),
        ("Target", "____________________________________________________________"),
        ("Features posibles", "____________________________________________________________"),
        ("Tipo de problema", "____________________________________________________________"),
        ("Datos necesarios", "____________________________________________________________"),
        ("Resultado esperado", "____________________________________________________________"),
    ]

    proyecto_data = [
        [
            Paragraph("Elemento", styles["TableHeader"]),
            Paragraph("Descripción", styles["TableHeader"]),
        ]
    ]

    for elemento, respuesta in proyecto:
        proyecto_data.append(
            [
                Paragraph(elemento, styles["TableCellBold"]),
                Paragraph(respuesta, styles["TableCell"]),
            ]
        )

    proyecto_table = Table(
        proyecto_data,
        colWidths=[150, 354],
    )

    proyecto_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(proyecto_table)

    # --------------------------------------------------------
    # ACTIVIDAD 8
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad 8 · Ordenar un proyecto según CRISP-DM",
            styles["Heading2Custom"],
        )
    )

    story.append(
        Paragraph(
            "Las siguientes acciones están desordenadas. Colócalas en el orden que "
            "consideres adecuado según CRISP-DM.",
            styles["BodyCustom"],
        )
    )

    acciones = [
        "Evaluar el modelo.",
        "Comprender el problema de la organización.",
        "Preparar los datos.",
        "Desplegar el modelo.",
        "Comprender los datos.",
        "Entrenar modelos.",
    ]

    for i, accion in enumerate(acciones, 1):

        story.append(
            Paragraph(
                f"{i}. {accion} → Orden: ______",
                styles["BodyCustom"],
            )
        )

    # --------------------------------------------------------
    # AUTOEVALUACIÓN
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Autoevaluación",
            styles["Heading2Custom"],
        )
    )

    preguntas_test = [
        (
            "1. ¿Cuál debería ser el punto de partida de un proyecto de Machine Learning?",
            [
                "A. Elegir el algoritmo más complejo.",
                "B. Comprender el problema que se quiere resolver.",
                "C. Entrenar un modelo inmediatamente.",
                "D. Descargar un dataset.",
            ],
        ),
        (
            "2. ¿Cuál de las siguientes corresponde a una variable objetivo?",
            [
                "A. Una variable utilizada como entrada.",
                "B. Una variable que el modelo intenta predecir.",
                "C. El nombre del algoritmo.",
                "D. La cantidad de registros.",
            ],
        ),
        (
            "3. ¿Cuál es la primera fase de CRISP-DM?",
            [
                "A. Modelado.",
                "B. Evaluación.",
                "C. Comprensión del negocio.",
                "D. Despliegue.",
            ],
        ),
        (
            "4. ¿Qué tipo de problema intenta predecir una categoría?",
            [
                "A. Clasificación.",
                "B. Regresión.",
                "C. Clustering.",
                "D. Análisis descriptivo.",
            ],
        ),
        (
            "5. ¿CRISP-DM debe entenderse como un proceso completamente lineal?",
            [
                "A. Sí, nunca se vuelve a una fase anterior.",
                "B. No, es posible regresar a etapas anteriores.",
                "C. Solo durante el despliegue.",
                "D. Solo durante la evaluación.",
            ],
        ),
    ]

    for pregunta, opciones in preguntas_test:

        story.append(
            Paragraph(
                f"<b>{pregunta}</b>",
                styles["BodyCustom"],
            )
        )

        for opcion in opciones:
            story.append(
                Paragraph(
                    opcion,
                    styles["BulletCustom"],
                )
            )

        story.append(Spacer(1, 4))

    # --------------------------------------------------------
    # RESPUESTAS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Clave de respuestas",
            styles["Heading2Custom"],
        )
    )

    respuestas = [
        "Autoevaluación 1: B.",
        "Autoevaluación 2: B.",
        "Autoevaluación 3: C.",
        "Autoevaluación 4: A.",
        "Autoevaluación 5: B.",
    ]

    for respuesta in respuestas:
        story.append(
            Paragraph(
                f"• {respuesta}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # ACTIVIDAD INTEGRADORA
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Actividad integradora",
            styles["Heading2Custom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "<b>Consigna:</b> desarrolla una propuesta inicial de proyecto de Machine "
                "Learning. El trabajo debe partir de un problema real y presentar su "
                "transformación en un problema de Machine Learning. Incluye el contexto, "
                "problema de negocio, objetivo, pregunta de Machine Learning, target, "
                "features posibles, tipo de problema, datos necesarios y una propuesta "
                "inicial de evaluación.",
                styles["BodyCustom"],
            )
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "Antes de finalizar, revisa que tu propuesta responda:",
            styles["BodyCustom"],
        )
    )

    checklist = [
        "¿El problema está claramente definido?",
        "¿El objetivo es concreto y medible?",
        "¿La variable objetivo está identificada cuando corresponde?",
        "¿Las características propuestas tienen relación con el problema?",
        "¿El tipo de problema de Machine Learning está correctamente identificado?",
        "¿Los datos necesarios son realistas y suficientes?",
        "¿La forma de evaluar el modelo está relacionada con el objetivo?",
    ]

    for item in checklist:
        story.append(
            Paragraph(
                f"☐ {item}",
                styles["BulletCustom"],
            )
        )

    # --------------------------------------------------------
    # CIERRE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Cierre",
            styles["Heading2Custom"],
        )
    )

    story.append(
        content_card(
            Paragraph(
                "La correcta definición del problema constituye una de las bases de un "
                "proyecto de Machine Learning. Antes de trabajar con algoritmos es necesario "
                "comprender qué se quiere resolver, qué datos existen, qué se desea predecir "
                "y cómo se determinará si el resultado es útil.",
                styles["BodyCustom"],
            )
        )
    )

    # --------------------------------------------------------
    # GENERACIÓN
    # --------------------------------------------------------

    canvas_builder = lambda filename, **kwargs: NumberedCanvas(
        filename,
        doc_subtitle="Metodología de Proyectos de Machine Learning y CRISP-DM - Actividades",
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
    create_activities_pdf()