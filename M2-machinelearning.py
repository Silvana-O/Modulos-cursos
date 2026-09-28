import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Encabezados y Pies de página con número total)
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "INTRODUCCIÓN AL MACHINE LEARNING")
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        teal_color = colors.HexColor("#0d9488")
        gray_text = colors.HexColor("#64748b")
        
        # --- Encabezado ---
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(teal_color)
        self.drawString(54, 750, "CURSOS CC")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(115, 750, f"|   {self.doc_subtitle.upper()}")
        
        # Página X de Y
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 750, page_str)
        
        # Línea divisoria superior
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # --- Pie de página ---
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(54, 36, "Material Teórico  •  Módulo 2 · Material 1")
        
        self.restoreState()


# ----------------------------------------------------------------------
# ESTILOS DEL DOCUMENTO
# ----------------------------------------------------------------------
def get_common_styles():
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_TEXT = colors.HexColor("#334155")

    style_module_tag = ParagraphStyle(
        'ModuleTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=COLOR_ACCENT,
        spaceAfter=4,
        textTransform='uppercase'
    )
    
    style_doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=COLOR_PRIMARY,
        spaceAfter=8
    )
    
    style_doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=15,
        textColor=COLOR_TEXT,
        spaceAfter=15
    )
    
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=COLOR_ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_TEXT,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )
    
    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_TEXT
    )
    
    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=style_table_cell,
        fontName='Helvetica-Bold'
    )

    return {
        'tag': style_module_tag,
        'title': style_doc_title,
        'subtitle': style_doc_subtitle,
        'h2': style_h2,
        'h3': style_h3,
        'body': style_body,
        'bullet': style_bullet,
        'th': style_table_header,
        'td': style_table_cell,
        'td_bold': style_table_cell_bold
    }


# ----------------------------------------------------------------------
# GENERACIÓN DEL PDF TEÓRICO
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Módulo_2_Material_1_Teoria.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=64, bottomMargin=54
    )
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_common_styles()
    story = []

    # --- Encabezado Principal ---
    story.append(Paragraph("MÓDULO 2 · MATERIAL 1", st['tag']))
    story.append(Paragraph("Introducción al Machine Learning", st['title']))
    story.append(Paragraph("Fundamentos, conceptos clave y flujo de trabajo de un proyecto de ML", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Descripción y Objetivos ---
    story.append(Paragraph("Descripción del material", st['h2']))
    story.append(Paragraph(
        "Este material presenta los fundamentos del Machine Learning o aprendizaje automático, una de las áreas "
        "principales de la Inteligencia Artificial. Se explica qué significa que una máquina aprenda a partir de datos, "
        "cómo se diferencia este enfoque de la programación tradicional y cuáles son las etapas básicas de un proyecto. "
        "El objetivo es comprender el proceso general antes de estudiar algoritmos específicos como regresión lineal, "
        "árboles de decisión, k-NN y K-Means.", st['body']
    ))

    story.append(Paragraph("Objetivos de aprendizaje", st['h2']))
    objetivos = [
        "Explicar con sus propias palabras qué es Machine Learning.",
        "Diferenciar Machine Learning de la programación tradicional.",
        "Reconocer qué papel cumplen los datos en el aprendizaje automático.",
        "Identificar características y etiquetas dentro de un conjunto de datos.",
        "Comprender qué significa entrenar un modelo.",
        "Diferenciar datos de entrenamiento y datos de prueba.",
        "Reconocer las etapas básicas de un proyecto de Machine Learning.",
        "Explicar qué es un modelo y qué es una predicción.",
        "Identificar situaciones cotidianas en las que se utiliza Machine Learning."
    ]
    for obj in objetivos:
        story.append(Paragraph(f"• {obj}", st['bullet']))
    story.append(Spacer(1, 10))

    # --- 1. ¿Qué es Machine Learning? ---
    story.append(Paragraph("1. ¿Qué es Machine Learning?", st['h2']))
    story.append(Paragraph(
        "En el material anterior vimos que la Inteligencia Artificial es un campo amplio de la informática que busca "
        "desarrollar sistemas capaces de realizar tareas inteligentes. Dentro de la IA encontramos el Machine Learning.", st['body']
    ))
    story.append(Paragraph(
        "<b>Definición:</b> Machine Learning es un conjunto de métodos que permite que un sistema aprenda patrones a "
        "partir de datos y utilice esos patrones para realizar predicciones o tomar determinadas decisiones.", st['body']
    ))
    story.append(Paragraph(
        "En lugar de indicarle a la computadora todas las reglas necesarias, le proporcionamos datos y utilizamos "
        "algoritmos para encontrar relaciones o patrones dentro de ellos.", st['body']
    ))

    # Ejemplo Tabla Casas
    story.append(Paragraph("Ejemplo: Predicción del precio de una vivienda", st['h3']))
    t_data_1 = [
        [Paragraph("Superficie", st['th']), Paragraph("Habitaciones", st['th']), Paragraph("Distancia al centro", st['th']), Paragraph("Precio", st['th'])],
        [Paragraph("50 m²", st['td']), Paragraph("2", st['td']), Paragraph("5 km", st['td']), Paragraph("$100.000", st['td_bold'])],
        [Paragraph("70 m²", st['td']), Paragraph("3", st['td']), Paragraph("4 km", st['td']), Paragraph("$140.000", st['td_bold'])],
        [Paragraph("90 m²", st['td']), Paragraph("3", st['td']), Paragraph("2 km", st['td']), Paragraph("$190.000", st['td_bold'])],
        [Paragraph("120 m²", st['td']), Paragraph("4", st['td']), Paragraph("1 km", st['td']), Paragraph("$250.000", st['td_bold'])]
    ]
    tbl_1 = Table(t_data_1, colWidths=[120, 120, 134, 130], repeatRows=1)
    tbl_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_1)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Proceso general:</b> Datos → Aprendizaje → Modelo → Predicción", st['body']))

    # --- 2. Programación Tradicional vs ML ---
    story.append(Paragraph("2. Machine Learning y programación tradicional", st['h2']))
    story.append(Paragraph("<b>Programación tradicional:</b> Una persona desarrolla las reglas que debe seguir la computadora. (Ejemplo: <i>SI temperatura > 30 ENTONCES encender ventilador</i>).", st['body']))
    story.append(Paragraph("<b>Esquema tradicional:</b> Datos + Reglas programadas → Resultado", st['bullet']))
    story.append(Paragraph("<b>Esquema Machine Learning:</b> Datos + Algoritmo de aprendizaje → Modelo", st['bullet']))
    story.append(Paragraph("<b>Uso del modelo:</b> Modelo + Nuevos datos → Predicción", st['bullet']))

    # --- 3 y 4. Aprendizaje y Datos ---
    story.append(Paragraph("3. ¿Qué significa que una máquina aprenda?", st['h2']))
    story.append(Paragraph(
        "En Machine Learning, 'aprender' no implica procesos cognitivos humanos. Un algoritmo analiza datos y "
        "ajusta un modelo para representar patrones presentes en ellos. Por ejemplo, al mostrarle imágenes etiquetadas "
        "de 'Perro' o 'Gato', el sistema encuentra patrones útiles para clasificar imágenes nuevas sin entender conceptualmente qué es un animal.", st['body']
    ))

    story.append(Paragraph("4. Los datos", st['h2']))
    story.append(Paragraph("Los datos son la materia prima. Pueden ser números, textos, imágenes, sonidos, videos, registros de actividad o mediciones de sensores. La calidad de los datos influye directamente en los resultados del modelo.", st['body']))

    # --- 5. Características y Etiquetas ---
    story.append(Paragraph("5. Características y etiquetas", st['h2']))
    story.append(Paragraph("• <b>Características (Features):</b> Variables que contienen información que el modelo utiliza (ej. superficie, habitaciones, distancia).", st['bullet']))
    story.append(Paragraph("• <b>Etiqueta (Label / Variable objetivo):</b> El valor que queremos predecir o identificar (ej. el precio de la vivienda).", st['bullet']))

    # --- 6, 7 y 8. Modelo, Entrenamiento y Prueba ---
    story.append(Paragraph("6. ¿Qué es un modelo?", st['h2']))
    story.append(Paragraph("Es la representación construida por el sistema a partir de los datos para realizar una tarea específica.", st['body']))

    story.append(Paragraph("7. Entrenamiento", st['h2']))
    story.append(Paragraph("Proceso mediante el cual el algoritmo analiza los datos de entrenamiento y ajusta el modelo para que encuentre patrones generalizables.", st['body']))

    story.append(Paragraph("8. Datos de entrenamiento y datos de prueba", st['h2']))
    story.append(Paragraph(
        "Separamos los datos para evaluar el modelo de forma objetiva. Si evaluáramos el modelo con los mismos datos "
        "con los que aprendió, tendríamos una visión demasiado optimista. Queremos comprobar si puede trabajar con datos desconocidos.", st['body']
    ))

    # --- 9. Flujo de trabajo ---
    story.append(Paragraph("9. El flujo de trabajo de un proyecto de Machine Learning", st['h2']))
    etapas = [
        ("1. Definir el problema", "Determinar claramente qué queremos resolver (ej. predecir el precio de una vivienda)."),
        ("2. Obtener los datos", "Reunir la información necesaria relacionada con el problema."),
        ("3. Explorar los datos", "Analizar cantidad de registros, variables, valores faltantes o errores."),
        ("4. Preparar los datos", "Limpiar datos inconsistentes, tratar valores faltantes y dar formato adecuado."),
        ("5. Dividir los datos", "Separar el conjunto de datos (ej. 80% entrenamiento, 20% prueba)."),
        ("6. Seleccionar un algoritmo", "Elegir la técnica adecuada (regresión lineal, árboles de decisión, k-NN, etc.)."),
        ("7. Entrenar el modelo", "Construir el modelo utilizando los datos de entrenamiento."),
        ("8. Realizar predicciones", "Proporcionar nuevos datos al modelo para obtener resultados."),
        ("9. Evaluar el modelo", "Medir el rendimiento mediante métricas (precisión, error medio, etc.).")
    ]
    for tit, desc in etapas:
        story.append(Paragraph(f"<b>{tit}:</b> {desc}", st['body']))

    # --- 10 y 11. Ejemplo Completo y Errores ---
    story.append(Paragraph("10. Un ejemplo completo", st['h2']))
    t_data_2 = [
        [Paragraph("Horas de estudio", st['th']), Paragraph("Asistencia", st['th']), Paragraph("Resultado (Etiqueta)", st['th'])],
        [Paragraph("2 hrs", st['td']), Paragraph("60 %", st['td']), Paragraph("No aprueba", st['td_bold'])],
        [Paragraph("4 hrs", st['td']), Paragraph("75 %", st['td']), Paragraph("Aprueba", st['td_bold'])],
        [Paragraph("6 hrs", st['td']), Paragraph("90 %", st['td']), Paragraph("Aprueba", st['td_bold'])],
        [Paragraph("1 hr", st['td']), Paragraph("50 %", st['td']), Paragraph("No aprueba", st['td_bold'])],
        [Paragraph("7 hrs", st['td']), Paragraph("95 %", st['td']), Paragraph("Aprueba", st['td_bold'])]
    ]
    tbl_2 = Table(t_data_2, colWidths=[160, 160, 184], repeatRows=1)
    tbl_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("11. ¿Puede un modelo equivocarse?", st['h2']))
    story.append(Paragraph("Sí. Un modelo produce estimaciones basadas en patrones. Nunca debemos aceptar ciegamente un resultado ('la IA lo dijo') sin auditar los datos de entrenamiento, su evaluación y sus limitaciones.", st['body']))

    # --- 12 y 13. ML en la Vida Cotidiana y no es Magia ---
    story.append(Paragraph("12. Machine Learning en la vida cotidiana", st['h2']))
    usos = [
        ("Recomendaciones", "Películas, música y productos en plataformas digitales."),
        ("Filtros de correo", "Detección automática de correo no deseado (spam)."),
        ("Reconocimiento de imagen", "Identificación de objetos y rostros."),
        ("Detección de fraude", "Análisis de patrones en operaciones bancarias."),
        ("Procesamiento de texto", "Traducción, clasificación y generación de texto.")
    ]
    for u_tit, u_desc in usos:
        story.append(Paragraph(f"• <b>{u_tit}:</b> {u_desc}", st['bullet']))

    story.append(Paragraph("13. Machine Learning no es magia", st['h2']))
    story.append(Paragraph("Un sistema de ML requiere: <i>Problema + Datos + Preparación + Algoritmo + Entrenamiento + Evaluación</i>. Si los datos son insuficientes o erróneos, la solución fallará.", st['body']))

    # --- 16. Para recordar ---
    story.append(Paragraph("16. Para recordar", st['h2']))
    puntos_clave = [
        "Machine Learning permite aprender patrones a partir de datos.",
        "Las características (features) aportan información; la etiqueta (label) es lo que se busca predecir.",
        "El entrenamiento construye el modelo; las pruebas evalúan su capacidad de generalización.",
        "Un modelo puede equivocarse y requiere validación crítica constante.",
        "ML no elimina la necesidad del criterio humano."
    ]
    for pk in puntos_clave:
        story.append(Paragraph(f"• {pk}", st['bullet']))

    # --- 18. Glosario ---
    story.append(Paragraph("18. Glosario de términos", st['h2']))
    glosario_data = [
        [Paragraph("Término", st['th']), Paragraph("Definición", st['th'])],
        [Paragraph("Machine Learning", st['td_bold']), Paragraph("Conjunto de métodos que permite a los sistemas aprender patrones a partir de datos.", st['td'])],
        [Paragraph("Dato", st['td_bold']), Paragraph("Información utilizada por un sistema para analizar un problema.", st['td'])],
        [Paragraph("Característica (feature)", st['td_bold']), Paragraph("Variable que proporciona información utilizada por el modelo.", st['td'])],
        [Paragraph("Etiqueta (label)", st['td_bold']), Paragraph("Resultado o categoría que se busca predecir.", st['td'])],
        [Paragraph("Modelo", st['td_bold']), Paragraph("Representación construida a partir de datos para realizar una tarea.", st['td'])],
        [Paragraph("Entrenamiento", st['td_bold']), Paragraph("Proceso de construcción o ajuste del modelo mediante datos.", st['td'])],
        [Paragraph("Predicción", st['td_bold']), Paragraph("Resultado producido por un modelo para nuevos datos de entrada.", st['td'])],
        [Paragraph("Datos de prueba", st['td_bold']), Paragraph("Conjunto de datos reservado para evaluar el rendimiento final.", st['td'])]
    ]
    tbl_g = Table(glosario_data, colWidths=[150, 354], repeatRows=1)
    tbl_g.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_g)
    story.append(Spacer(1, 10))

    # --- 20. Conexión ---
    story.append(Paragraph("20. Conexión con el siguiente material", st['h2']))
    story.append(Paragraph("En el próximo material abordaremos el <b>Aprendizaje Supervisado</b>, clasificando problemas en Regresión (valores continuos) y Clasificación (categorías), e introduciendo algoritmos como Regresión Lineal, Árboles de Decisión y k-NN.", st['body']))

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="INTRODUCCIÓN AL MACHINE LEARNING - TEORÍA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento teórico generado con éxito: {filename}")


if __name__ == "__main__":
    create_theory_pdf()