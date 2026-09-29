
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    Preformatted,
)
from reportlab.pdfgen import canvas


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

CARPETA_SALIDA = Path("material5")

CARPETA_SALIDA.mkdir(exist_ok=True)


# ============================================================
# COLORES
# ============================================================

COLOR_PRIMARY = colors.HexColor("#0f172a")
COLOR_TEXT = colors.HexColor("#334155")
COLOR_MUTED = colors.HexColor("#64748b")
COLOR_ACCENT = colors.HexColor("#0d9488")
COLOR_LIGHT = colors.HexColor("#f8fafc")
COLOR_CARD = colors.HexColor("#f1f5f9")
COLOR_BORDER = colors.HexColor("#cbd5e1")


# ============================================================
# CANVAS PERSONALIZADO
# ============================================================

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado que agrega:

    - Encabezado institucional.
    - Subtítulo del documento.
    - Número de página.
    - Cantidad total de páginas.
    - Pie de página.
    """

    def __init__(self, *args, **kwargs):

        self.doc_subtitle = kwargs.pop(
            "doc_subtitle",
            "PREPARACIÓN Y LIMPIEZA DE DATOS"
        )

        super().__init__(*args, **kwargs)

        self._saved_page_states = []

    def showPage(self):

        self._saved_page_states.append(
            dict(self.__dict__)
        )

        self._startPage()

    def save(self):

        total_pages = len(self._saved_page_states)

        for state in self._saved_page_states:

            self.__dict__.update(state)

            self.draw_page_decorations(total_pages)

            super().showPage()

        super().save()

    def draw_page_decorations(self, total_pages):

        self.saveState()

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(COLOR_ACCENT)

        self.drawString(
            54,
            750,
            "CURSOS CC"
        )

        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        self.drawString(
            115,
            750,
            f"|  {self.doc_subtitle.upper()}"
        )

        # Número de página

        self.drawRightString(
            558,
            750,
            f"Página {self._pageNumber} de {total_pages}"
        )

        # Línea superior

        self.setStrokeColor(
            colors.HexColor("#e2e8f0")
        )

        self.setLineWidth(0.75)

        self.line(
            54,
            742,
            558,
            742
        )

        # ----------------------------------------------------
        # PIE DE PÁGINA
        # ----------------------------------------------------

        self.setFont(
            "Helvetica",
            7.5
        )

        self.setFillColor(
            COLOR_MUTED
        )

        self.drawString(
            54,
            36,
            "Material educativo  |  "
            "Módulo 2 - Material 5: Preparación y Limpieza de Datos"
        )

        self.restoreState()


# ============================================================
# ESTILOS
# ============================================================

def obtener_estilos():

    styles = getSampleStyleSheet()

    return {

        "tag": ParagraphStyle(
            "ModuleTag",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=COLOR_ACCENT,
            spaceAfter=4,
        ),

        "title": ParagraphStyle(
            "DocumentTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=COLOR_PRIMARY,
            spaceAfter=6,
        ),

        "subtitle": ParagraphStyle(
            "DocumentSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=COLOR_TEXT,
            spaceAfter=12,
        ),

        "h1": ParagraphStyle(
            "HeadingCustom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=COLOR_PRIMARY,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),

        "h2": ParagraphStyle(
            "SubHeadingCustom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=COLOR_PRIMARY,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),

        "body": ParagraphStyle(
            "BodyCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=COLOR_TEXT,
            spaceAfter=6,
        ),

        "bullet": ParagraphStyle(
            "BulletCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=COLOR_TEXT,
            leftIndent=14,
            firstLineIndent=-9,
            spaceAfter=3,
        ),

        "small": ParagraphStyle(
            "SmallCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=COLOR_MUTED,
            spaceAfter=4,
        ),

        "table_header": ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        ),

        "table_cell": ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=COLOR_TEXT,
        ),

        "table_cell_bold": ParagraphStyle(
            "TableCellBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=COLOR_PRIMARY,
        ),

        "code": ParagraphStyle(
            "CodeCustom",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=7.5,
            leading=9.5,
            textColor=COLOR_PRIMARY,
        ),
    }


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def P(texto, estilo):

    estilos = obtener_estilos()

    return Paragraph(
        texto,
        estilos[estilo]
    )


def crear_info_box(titulo, contenido):

    estilos = obtener_estilos()

    tabla = Table(
        [
            [
                Paragraph(
                    titulo,
                    estilos["table_cell_bold"]
                )
            ],
            [
                Paragraph(
                    contenido,
                    estilos["table_cell"]
                )
            ],
        ],
        colWidths=[504],
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    COLOR_CARD,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    COLOR_LIGHT,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    COLOR_BORDER,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
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

    return tabla


def crear_bullet(texto):

    return P(
        f"• {texto}",
        "bullet"
    )


def crear_documento(
    archivo,
    subtitulo
):

    ruta = CARPETA_SALIDA / archivo

    return SimpleDocTemplate(
        str(ruta),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54,
        title="Módulo 2 - Material 5",
        author="Cursos CC",
        subject=subtitulo,
    )


# ============================================================
# PDF TEÓRICO
# ============================================================

def crear_pdf_teoria():

    estilos = obtener_estilos()

    doc = crear_documento(
        "Modulo2_Material5_Teoria.pdf",
        "PREPARACIÓN Y LIMPIEZA DE DATOS",
    )

    story = []

    # --------------------------------------------------------
    # PORTADA / ENCABEZADO
    # --------------------------------------------------------

    story.append(
        P(
            "MÓDULO 2 · MATERIAL 5",
            "tag"
        )
    )

    story.append(
        P(
            "Preparación y Limpieza de Datos en Machine Learning",
            "title"
        )
    )

    story.append(
        P(
            "Material teórico · Calidad de datos, "
            "preprocesamiento, codificación, escalado "
            "y prevención de Data Leakage",
            "subtitle"
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=COLOR_ACCENT,
            spaceAfter=12,
        )
    )

    # --------------------------------------------------------
    # DESCRIPCIÓN
    # --------------------------------------------------------

    story.append(
        crear_info_box(
            "Descripción",
            "Un modelo de Machine Learning aprende a partir "
            "de los datos que recibe. Si esos datos contienen "
            "valores faltantes, duplicados, errores, formatos "
            "inconsistentes o variables en escalas diferentes, "
            "el modelo puede aprender patrones poco confiables. "
            "Por esta razón, la preparación de los datos es "
            "una etapa fundamental del flujo de trabajo."
        )
    )

    story.append(Spacer(1, 10))

    # --------------------------------------------------------
    # OBJETIVOS
    # --------------------------------------------------------

    story.append(
        P(
            "Objetivos de aprendizaje",
            "h1"
        )
    )

    objetivos = [
        "Comprender por qué la calidad de los datos afecta el entrenamiento y la evaluación de un modelo.",
        "Identificar datos faltantes, duplicados, valores inválidos y valores atípicos.",
        "Aplicar estrategias básicas de limpieza e imputación.",
        "Diferenciar variables numéricas y categóricas.",
        "Comprender Label Encoding y One-Hot Encoding.",
        "Comprender la Normalización Min-Max y la Estandarización Z-score.",
        "Dividir los datos en entrenamiento y prueba de forma adecuada.",
        "Reconocer y prevenir la fuga de información o Data Leakage.",
    ]

    for objetivo in objetivos:

        story.append(
            crear_bullet(objetivo)
        )

    # --------------------------------------------------------
    # CONTENIDOS
    # --------------------------------------------------------

    contenidos = [

        (
            "1. ¿Qué significa preparar los datos?",
            """
            La preparación de datos consiste en transformar un conjunto
            de información original en una representación adecuada para
            un algoritmo de Machine Learning. No significa modificar los
            datos arbitrariamente: implica detectar problemas, documentar
            decisiones y aplicar transformaciones justificadas.

            Un flujo habitual incluye cargar los datos, inspeccionarlos,
            limpiarlos, transformarlos, dividirlos en entrenamiento y
            prueba y finalmente preparar las variables para el modelo.
            """
        ),

        (
            "2. Calidad de los datos",
            """
            La calidad puede analizarse desde diferentes dimensiones:
            completitud, consistencia, validez, unicidad y coherencia
            con el dominio del problema.

            Una columna puede no contener valores nulos y aun así
            presentar datos incorrectos. Por ejemplo, una edad de 250
            no es un dato faltante, pero es inválida para un problema
            que representa edades humanas.
            """
        ),

        (
            "3. Datos faltantes",
            """
            Un dato faltante puede aparecer como NaN, None, una celda
            vacía u otra marca definida por el sistema.

            Antes de decidir qué hacer, conviene medir cuántos faltantes
            existen y en qué variables aparecen.

            Algunas estrategias son eliminar registros, eliminar una
            variable, imputar con media o mediana en variables numéricas
            o utilizar la moda para variables categóricas.

            La mediana suele ser más resistente a valores extremos que
            la media.
            """
        ),

        (
            "4. Registros duplicados",
            """
            Un duplicado es un registro repetido que puede representar
            la misma observación. La duplicación puede provocar que
            determinados casos tengan un peso artificialmente mayor
            durante el entrenamiento.

            En pandas se pueden detectar con duplicated() y eliminar
            con drop_duplicates().

            Antes de eliminar registros es necesario comprobar que
            realmente representan observaciones repetidas.
            """
        ),

        (
            "5. Valores incorrectos y reglas de dominio",
            """
            Una regla de dominio establece qué valores son razonables
            para una determinada variable.

            Por ejemplo, una edad humana debe encontrarse dentro de un
            rango coherente con el problema. Una temperatura, una
            cantidad o un porcentaje también pueden tener restricciones.

            Un valor inválido no debe confundirse automáticamente con
            un outlier estadístico.
            """
        ),

        (
            "6. Valores atípicos u outliers",
            """
            Un outlier es una observación que se aleja considerablemente
            del comportamiento general de los datos.

            Puede representar un error, un caso poco frecuente pero real
            o una característica importante del fenómeno estudiado.

            Una técnica habitual es el rango intercuartílico (IQR):

            IQR = Q3 - Q1

            Límite inferior = Q1 - 1.5 × IQR

            Límite superior = Q3 + 1.5 × IQR

            La detección estadística no demuestra por sí sola que el dato
            sea incorrecto. Siempre debe considerarse el contexto.
            """
        ),

        (
            "7. Variables numéricas y categóricas",
            """
            Las variables numéricas representan cantidades que pueden
            utilizarse mediante operaciones matemáticas, como edad,
            horas de estudio o precio.

            Las variables categóricas representan clases o categorías,
            como modalidad, departamento o tipo de curso.

            Muchos algoritmos necesitan transformar las categorías a
            representaciones numéricas antes del entrenamiento.
            """
        ),

        (
            "8. Label Encoding",
            """
            Label Encoding asigna un número a cada categoría.

            Por ejemplo:

            Presencial → 0
            Virtual → 1

            Puede resultar apropiado en determinadas situaciones,
            especialmente cuando las categorías poseen un orden real.

            Sin embargo, si las categorías son nominales y no tienen
            orden, la codificación numérica puede generar una relación
            matemática que en realidad no existe.
            """
        ),

        (
            "9. One-Hot Encoding",
            """
            One-Hot Encoding crea una columna binaria para cada categoría.

            Si una variable Modalidad contiene Presencial y Virtual,
            se pueden generar:

            Modalidad_Presencial
            Modalidad_Virtual

            Para cada registro, una de las columnas tendrá valor 1
            y las restantes tendrán valor 0.

            Esta representación evita establecer un orden numérico
            artificial entre categorías nominales.
            """
        ),

        (
            "10. Escalado de variables",
            """
            Algunos algoritmos son sensibles a la escala de las
            variables.

            Por ejemplo, una variable que toma valores entre 0 y 1
            y otra que toma valores entre 0 y 100000 no se encuentran
            en una escala comparable.

            Dos técnicas frecuentes son la Normalización Min-Max y la
            Estandarización Z-score.
            """
        ),

        (
            "11. Normalización Min-Max",
            """
            La normalización Min-Max transforma una variable para
            llevarla habitualmente al intervalo [0, 1].

            x' = (x - mínimo) / (máximo - mínimo)

            Es útil cuando se desea trabajar dentro de un rango
            determinado.

            Los valores extremos pueden influir en el mínimo y máximo
            utilizados para realizar la transformación.
            """
        ),

        (
            "12. Estandarización Z-score",
            """
            La estandarización expresa cada valor en relación con la
            media y el desvío estándar.

            z = (x - media) / desvío estándar

            Una variable estandarizada presenta aproximadamente media 0
            y desvío estándar 1 dentro del conjunto utilizado para
            ajustar la transformación.
            """
        ),

        (
            "13. División de los datos",
            """
            Una división habitual separa los datos en entrenamiento y
            prueba.

            El conjunto de entrenamiento se utiliza para aprender los
            parámetros del modelo.

            El conjunto de prueba se reserva para estimar cómo se
            comporta el modelo frente a datos que no utilizó durante
            el entrenamiento.

            También puede utilizarse un conjunto de validación o
            validación cruzada.
            """
        ),

        (
            "14. Data Leakage o fuga de información",
            """
            Existe Data Leakage cuando información que no debería estar
            disponible durante el entrenamiento termina influyendo en
            el modelo.

            Un error frecuente consiste en calcular la media, mediana,
            escalado o codificación utilizando todo el dataset antes de
            dividirlo.

            La regla práctica es:

            Primero se separan los datos.

            Después se ajustan las transformaciones utilizando únicamente
            el conjunto de entrenamiento.

            Finalmente se aplican esas transformaciones al conjunto de
            prueba.
            """
        ),

        (
            "15. Flujo recomendado",
            """
            Un flujo básico y seguro es:

            1. Cargar los datos.
            2. Explorar estructura, tipos y calidad.
            3. Separar variables predictoras y objetivo.
            4. Dividir los datos en entrenamiento y prueba.
            5. Ajustar imputación, codificación y escalado con entrenamiento.
            6. Aplicar las transformaciones al entrenamiento y a la prueba.
            7. Entrenar el modelo.
            8. Evaluar sobre los datos de prueba.

            En proyectos reales, scikit-learn permite organizar estas
            operaciones mediante Pipeline y ColumnTransformer.
            """
        ),
    ]

    for titulo, contenido in contenidos:

        story.append(
            P(titulo, "h1")
        )

        for parrafo in contenido.strip().split("\n\n"):

            texto = parrafo.strip().replace(
                "\n",
                " "
            )

            story.append(
                P(texto, "body")
            )

    # --------------------------------------------------------
    # ACTIVIDAD DE IDENTIFICACIÓN
    # --------------------------------------------------------

    story.append(
        P(
            "16. Actividad de identificación",
            "h1"
        )
    )

    story.append(
        P(
            "Analiza la siguiente tabla y responde las preguntas.",
            "body"
        )
    )

    datos = [
        [
            P("Nombre", "table_header"),
            P("Edad", "table_header"),
            P("Departamento", "table_header"),
            P("Horas de estudio", "table_header"),
        ],
        [
            P("Ana", "table_cell"),
            P("20", "table_cell"),
            P("Salto", "table_cell"),
            P("8", "table_cell"),
        ],
        [
            P("Luis", "table_cell"),
            P("22", "table_cell"),
            P("Artigas", "table_cell"),
            P("5", "table_cell"),
        ],
        [
            P("Marta", "table_cell"),
            P("Faltante", "table_cell"),
            P("Salto", "table_cell"),
            P("7", "table_cell"),
        ],
        [
            P("Juan", "table_cell"),
            P("21", "table_cell"),
            P("Artigas", "table_cell"),
            P("3", "table_cell"),
        ],
        [
            P("Juan", "table_cell"),
            P("21", "table_cell"),
            P("Artigas", "table_cell"),
            P("3", "table_cell"),
        ],
        [
            P("Pedro", "table_cell"),
            P("250", "table_cell"),
            P("Salto", "table_cell"),
            P("4", "table_cell"),
        ],
    ]

    tabla = Table(
        datos,
        colWidths=[
            100,
            90,
            130,
            120,
        ],
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    COLOR_ACCENT,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_BORDER,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(tabla)

    story.append(Spacer(1, 8))

    preguntas = [
        "Identifica un dato faltante.",
        "Identifica un registro duplicado.",
        "Identifica un valor que debería validarse mediante una regla de dominio.",
        "Indica qué variables son numéricas y cuál es categórica.",
        "Propón una estrategia de limpieza para cada problema.",
    ]

    for pregunta in preguntas:

        story.append(
            crear_bullet(pregunta)
        )

    # --------------------------------------------------------
    # ACTIVIDAD PRÁCTICA
    # --------------------------------------------------------

    story.append(
        P(
            "17. Actividad práctica con Python",
            "h1"
        )
    )

    story.append(
        P(
            "Ejecuta los archivos Python incluidos con este material. "
            "Observa las tablas antes y después de cada transformación "
            "y explica qué cambió y por qué.",
            "body"
        )
    )

    # --------------------------------------------------------
    # AUTOEVALUACIÓN
    # --------------------------------------------------------

    story.append(
        P(
            "18. Preguntas de autoevaluación",
            "h1"
        )
    )

    preguntas_auto = [
        "¿Por qué no conviene eliminar automáticamente todos los registros que contienen valores faltantes?",
        "¿Cuál es la diferencia entre un valor inválido y un outlier?",
        "¿Cuándo puede ser problemática una codificación Label Encoding?",
        "¿Qué diferencia existe entre Min-Max y Z-score?",
        "¿Por qué una transformación calculada con todo el dataset puede producir Data Leakage?",
        "¿Qué información debe utilizarse para ajustar un escalador antes de evaluar el modelo?",
    ]

    for pregunta in preguntas_auto:

        story.append(
            crear_bullet(pregunta)
        )

    # --------------------------------------------------------
    # ACTIVIDAD INTEGRADORA
    # --------------------------------------------------------

    story.append(
        P(
            "19. Actividad integradora",
            "h1"
        )
    )

    story.append(
        crear_info_box(
            "Primer proyecto de preparación de datos",
            "Utiliza un dataset pequeño relacionado con estudiantes, "
            "cursos, ventas, productos u otra temática. Identifica al "
            "menos un problema de calidad, justifica su tratamiento, "
            "prepara las variables para Machine Learning y documenta "
            "cada decisión. El resultado debe incluir el dataset "
            "original, el dataset preparado, el código Python y una "
            "breve explicación de las transformaciones realizadas."
        )
    )

    # --------------------------------------------------------
    # GENERACIÓN
    # --------------------------------------------------------

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs:
            NumberedCanvas(
                *args,
                doc_subtitle="PREPARACIÓN Y LIMPIEZA DE DATOS",
                **kwargs
            ),
    )

    print(
        f"PDF teórico creado: {doc.filename}"
    )


# ============================================================
# PDF DE ACTIVIDADES
# ============================================================

def crear_pdf_actividades():

    doc = crear_documento(
        "Modulo2_Material5_Actividades.pdf",
        "ACTIVIDADES Y PRÁCTICA",
    )

    story = []

    story.append(
        P(
            "MÓDULO 2 · MATERIAL 5",
            "tag"
        )
    )

    story.append(
        P(
            "Actividades prácticas: Preparación y Limpieza de Datos",
            "title"
        )
    )

    story.append(
        P(
            "Consignas para trabajar con Python, pandas, NumPy y scikit-learn",
            "subtitle"
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=COLOR_ACCENT,
            spaceAfter=12,
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 1
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 1 - Identificación de problemas",
            "h1"
        )
    )

    story.append(
        P(
            "Observa la tabla presentada en el material teórico. "
            "Identifica datos faltantes, duplicados, valores inválidos "
            "y tipos de variables. Justifica cada respuesta.",
            "body"
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 2
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 2 - Limpieza con pandas",
            "h1"
        )
    )

    story.append(
        P(
            "Ejecuta 01_limpieza_y_calidad.py. Observa el dataset "
            "original y explica el efecto de cada operación: "
            "drop_duplicates(), validación de la edad e imputación "
            "con la mediana.",
            "body"
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 3
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 3 - Codificación",
            "h1"
        )
    )

    story.append(
        P(
            "Ejecuta 02_codificacion.py. Compara Label Encoding y "
            "One-Hot Encoding. Explica qué información representa "
            "cada columna generada y por qué una variable nominal "
            "no debería interpretarse automáticamente como ordinal.",
            "body"
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 4
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 4 - Escalado",
            "h1"
        )
    )

    story.append(
        P(
            "Ejecuta 03_escalado.py. Compara los resultados de "
            "Min-Max y Z-score. Explica qué ocurre con una variable "
            "que posee un valor extremo.",
            "body"
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 5
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 5 - Entrenamiento y prueba",
            "h1"
        )
    )

    story.append(
        P(
            "Ejecuta 04_division_y_leakage.py. Comprueba por qué las "
            "transformaciones deben ajustarse con los datos de "
            "entrenamiento y luego aplicarse al conjunto de prueba.",
            "body"
        )
    )

    # --------------------------------------------------------
    # ACTIVIDAD 6
    # --------------------------------------------------------

    story.append(
        P(
            "Actividad 6 - Actividad integradora",
            "h1"
        )
    )

    story.append(
        crear_info_box(
            "Primer proyecto de preparación de datos",
            "Selecciona un dataset pequeño y comprensible. Puede ser "
            "de estudiantes, ventas, cursos, productos u otra temática "
            "relacionada con un problema de datos. El dataset debe "
            "contener al menos una variable numérica y una categórica."
        )
    )

    story.append(
        P(
            "Realiza las siguientes etapas:",
            "h2"
        )
    )

    etapas = [
        "Describe brevemente el dataset y su propósito.",
        "Inspecciona las columnas y los tipos de datos.",
        "Detecta valores faltantes y decide cómo tratarlos.",
        "Detecta duplicados y justifica su eliminación o conservación.",
        "Identifica al menos un posible valor inválido o atípico.",
        "Codifica las variables categóricas cuando sea necesario.",
        "Escala las variables numéricas utilizando una técnica adecuada.",
        "Divide los datos en entrenamiento y prueba.",
        "Explica cómo evitaste Data Leakage.",
        "Entrega el código y una breve conclusión.",
    ]

    for i, etapa in enumerate(etapas, start=1):

        story.append(
            crear_bullet(
                f"{i}. {etapa}"
            )
        )

    # --------------------------------------------------------
    # ENTREGA
    # --------------------------------------------------------

    story.append(
        P(
            "Producto a entregar",
            "h2"
        )
    )

    entregables = [
        "Archivo Python (.py).",
        "Dataset utilizado (.csv u otro formato permitido).",
        "Dataset preparado, si corresponde.",
        "Breve informe con las decisiones tomadas.",
    ]

    for item in entregables:

        story.append(
            crear_bullet(item)
        )

    # --------------------------------------------------------
    # CRITERIOS
    # --------------------------------------------------------

    story.append(
        P(
            "Criterios de revisión",
            "h2"
        )
    )

    criterios = [
        "El código se ejecuta sin errores.",
        "Las decisiones de limpieza están justificadas.",
        "Las variables están correctamente identificadas.",
        "Las transformaciones se aplican sin producir fuga de información.",
        "El estudiante puede explicar con sus palabras qué hizo y por qué.",
    ]

    for criterio in criterios:

        story.append(
            crear_bullet(criterio)
        )

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs:
            NumberedCanvas(
                *args,
                doc_subtitle="ACTIVIDADES Y PRÁCTICA",
                **kwargs
            ),
    )

    print(
        f"PDF de actividades creado: {doc.filename}"
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    crear_pdf_teoria()
    crear_pdf_actividades()

    print()
    print("=" * 60)
    print("PROCESO FINALIZADO")
    print("=" * 60)
    print()
    print(
        "Los archivos fueron creados en la carpeta:"
    )
    print(
        CARPETA_SALIDA.resolve()
    )

