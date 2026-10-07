from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Encabezados y Pies de página con 'Página X de Y')
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    """Canvas dinámico con línea gráfica corporativa y paginación exacta."""
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "ACTIVIDAD INTEGRADORA · MÓDULO 2")
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
        
        # Colores corporativos (Teal & Slate Gray)
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
        self.drawString(54, 36, "Material educativo  •  Módulo 2: Primer proyecto de Machine Learning")
        
        self.restoreState()


def get_styles():
    """Retorna los estilos globales de tipografía."""
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")   # Slate 900
    COLOR_ACCENT = colors.HexColor("#0d9488")    # Teal 600
    COLOR_TEXT = colors.HexColor("#334155")      # Slate 700

    return {
        'tag': ParagraphStyle('Tag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=COLOR_ACCENT, spaceAfter=4),
        'title': ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=COLOR_PRIMARY, spaceAfter=4),
        'subtitle': ParagraphStyle('Subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=COLOR_TEXT, spaceAfter=10),
        'h2': ParagraphStyle('H2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=COLOR_PRIMARY, spaceBefore=10, spaceAfter=4, keepWithNext=True),
        'body': ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=COLOR_TEXT, spaceAfter=4),
        'bullet': ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=COLOR_TEXT, leftIndent=12, firstLineIndent=-8, spaceAfter=2),
        'th': ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1),
        'td': ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=COLOR_TEXT, alignment=1),
        'td_bold': ParagraphStyle('TDBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=COLOR_PRIMARY, alignment=1),
        'formula': ParagraphStyle('Formula', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=COLOR_PRIMARY, alignment=1)
    }


def create_activity_pdf(filename="Modulo2_ActividadIntegradora.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=64, bottomMargin=54
    )
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")
    COLOR_CARD_BG = colors.HexColor("#f1f5f9")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_styles()
    story = []

    # --- Header Principal ---
    story.append(Paragraph("ACTIVIDAD INTEGRADORA · MÓDULO 2", st['tag']))
    story.append(Paragraph("Primer proyecto de Machine Learning", st['title']))
    story.append(Paragraph("Guía de desarrollo e integración práctica", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=8))

    # --- Consigna y Situación ---
    consigna_text = "<b>Consigna:</b> En esta actividad vas a integrar los conocimientos trabajados durante el módulo para desarrollar, de forma guiada, tu primer proyecto de Machine Learning. El objetivo es analizar un conjunto de datos, prepararlo para trabajar con un modelo, realizar predicciones y evaluar sus resultados."
    situacion_text = "<b>Situación:</b> Una institución educativa quiere analizar el desempeño de sus estudiantes y utilizar Machine Learning para predecir si un estudiante podría aprobar o desaprobar un curso. Para realizar esta tarea se dispone de los siguientes datos:"
    
    box_header = [
        Paragraph(consigna_text, st['body']),
        Spacer(1, 4),
        Paragraph(situacion_text, st['body'])
    ]
    
    tbl_header = Table([[box_header]], colWidths=[504])
    tbl_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tbl_header)
    story.append(Spacer(1, 8))

    # --- Tabla de Datos del Problema ---
    data_alumnos = [
        [Paragraph("Estudiante", st['th']), Paragraph("Horas de estudio", st['th']), Paragraph("Asistencia (%)", st['th']), Paragraph("Actividades entregadas", st['th']), Paragraph("Resultado", st['th'])],
        [Paragraph("Ana", st['td']), Paragraph("8", st['td']), Paragraph("95", st['td']), Paragraph("9", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Bruno", st['td']), Paragraph("6", st['td']), Paragraph("85", st['td']), Paragraph("8", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Carla", st['td']), Paragraph("3", st['td']), Paragraph("70", st['td']), Paragraph("5", st['td']), Paragraph("Desaprobado", st['td'])],
        [Paragraph("Diego", st['td']), Paragraph("9", st['td']), Paragraph("98", st['td']), Paragraph("10", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Elena", st['td']), Paragraph("—", st['td']), Paragraph("60", st['td']), Paragraph("4", st['td']), Paragraph("Desaprobado", st['td'])],
        [Paragraph("Facundo", st['td']), Paragraph("5", st['td']), Paragraph("80", st['td']), Paragraph("7", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Gabriela", st['td']), Paragraph("1", st['td']), Paragraph("55", st['td']), Paragraph("3", st['td']), Paragraph("Desaprobado", st['td'])],
        [Paragraph("Hugo", st['td']), Paragraph("7", st['td']), Paragraph("90", st['td']), Paragraph("8", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Irene", st['td']), Paragraph("4", st['td']), Paragraph("72", st['td']), Paragraph("5", st['td']), Paragraph("Desaprobado", st['td'])],
        [Paragraph("Joaquín", st['td']), Paragraph("6", st['td']), Paragraph("88", st['td']), Paragraph("7", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Joaquín", st['td']), Paragraph("6", st['td']), Paragraph("88", st['td']), Paragraph("7", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("Karen", st['td']), Paragraph("20", st['td']), Paragraph("65", st['td']), Paragraph("4", st['td']), Paragraph("Desaprobado", st['td'])],
        [Paragraph("Lucas", st['td']), Paragraph("8", st['td']), Paragraph("92", st['td']), Paragraph("9", st['td']), Paragraph("Aprobado", st['td'])],
    ]
    tbl_alumnos = Table(data_alumnos, colWidths=[100, 100, 100, 104, 100])
    tbl_alumnos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tbl_alumnos)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Observa que el conjunto de datos contiene algunos problemas que deberán ser identificados y analizados antes de utilizarlo.</i>", st['body']))
    story.append(Spacer(1, 6))

    # --- Tareas 1, 2 y 3 ---
    story.append(Paragraph("1. Comprender el problema", st['h2']))
    story.append(Paragraph("Identifica:", st['body']))
    story.append(Paragraph("• ¿Cuál es el objetivo del proyecto?", st['bullet']))
    story.append(Paragraph("• ¿Cuál es la variable que queremos predecir?", st['bullet']))
    story.append(Paragraph("• ¿Qué variables pueden utilizarse como características?", st['bullet']))
    story.append(Paragraph("• ¿Se trata de un problema de regresión o de clasificación? Explica por qué.", st['bullet']))

    story.append(Paragraph("2. Analizar y limpiar los datos", st['h2']))
    story.append(Paragraph("Examina el conjunto de datos e identifica al menos:", st['body']))
    story.append(Paragraph("• Un dato faltante.", st['bullet']))
    story.append(Paragraph("• Un registro duplicado.", st['bullet']))
    story.append(Paragraph("• Un valor que podría considerarse un dato atípico o posiblemente incorrecto.", st['bullet']))
    story.append(Paragraph("Explica qué decisión tomarías en cada caso y por qué.", st['body']))
    
    note_box = [Paragraph("<b>Importante:</b> Un dato atípico no debe eliminarse automáticamente. Primero debemos analizar si representa un error o una situación real.", st['body'])]
    tbl_note = Table([[note_box]], colWidths=[504])
    tbl_note.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_note)

    story.append(Paragraph("3. Preparar los datos", st['h2']))
    story.append(Paragraph("Indica qué transformaciones serían necesarias para que los datos puedan utilizarse en un modelo de Machine Learning. Considera aspectos como: datos faltantes, duplicados, atípicos, variables numéricas, categóricas y la separación entre entrenamiento y prueba.", st['body']))

    # --- Tareas 4 y 5 ---
    story.append(Paragraph("4. Entrenar un modelo", st['h2']))
    story.append(Paragraph("Selecciona un algoritmo de clasificación estudiado en el módulo (por ejemplo, un árbol de decisión) y explica brevemente por qué puede utilizarse para este problema.", st['body']))

    story.append(Paragraph("5. Realizar predicciones", st['h2']))
    story.append(Paragraph("Supongamos que recibimos los datos de dos nuevos estudiantes:", st['body']))
    
    data_pred = [
        [Paragraph("Estudiante", st['th']), Paragraph("Horas de estudio", st['th']), Paragraph("Asistencia (%)", st['th']), Paragraph("Actividades entregadas", st['th'])],
        [Paragraph("Estudiante A", st['td']), Paragraph("6", st['td']), Paragraph("85", st['td']), Paragraph("8", st['td'])],
        [Paragraph("Estudiante B", st['td']), Paragraph("2", st['td']), Paragraph("60", st['td']), Paragraph("3", st['td'])],
    ]
    tbl_pred = Table(data_pred, colWidths=[126, 126, 126, 126])
    tbl_pred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_pred)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Utilizando la información disponible y el modelo planteado, indica qué resultado esperarías para cada estudiante (Aprobado / Desaprobado) y explica brevemente tu razonamiento.", st['body']))

    # --- Tarea 6: Evaluar el modelo ---
    story.append(Paragraph("6. Evaluar el modelo", st['h2']))
    story.append(Paragraph("Supongamos que, al evaluar el modelo sobre un conjunto de prueba, obtenemos los siguientes resultados en la matriz de confusión:", st['body']))
    
    data_cm = [
        [Paragraph("", st['th']), Paragraph("Predijo Aprobado", st['th']), Paragraph("Predijo Desaprobado", st['th'])],
        [Paragraph("Real: Aprobado", st['td_bold']), Paragraph("4", st['td']), Paragraph("1", st['td'])],
        [Paragraph("Real: Desaprobado", st['td_bold']), Paragraph("1", st['td']), Paragraph("4", st['td'])],
    ]
    tbl_cm = Table(data_cm, colWidths=[168, 168, 168])
    tbl_cm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_cm)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Considerando <b>'Aprobado'</b> como la clase positiva, identifica: Verdaderos positivos (TP), Verdaderos negativos (TN), Falsos positivos (FP) y Falsos negativos (FN). Luego calcula las métricas:", st['body']))
    
    # Fórmulas de métricas
    f_text = "Precisión = TP / (TP + FP) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; Recall = TP / (TP + FN)"
    tbl_formulas = Table([[Paragraph(f_text, st['formula'])]], colWidths=[504])
    tbl_formulas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_formulas)

    # --- Tareas 7 y 8 ---
    story.append(Paragraph("7. Interpretar los resultados", st['h2']))
    story.append(Paragraph("• ¿Qué significa que el modelo haya cometido falsos positivos?", st['bullet']))
    story.append(Paragraph("• ¿Qué significa que haya cometido falsos negativos?", st['bullet']))
    story.append(Paragraph("• ¿Por qué es importante analizar los errores del modelo?", st['bullet']))
    story.append(Paragraph("• ¿Por qué no sería conveniente utilizar un modelo sin evaluar previamente sus resultados?", st['bullet']))

    story.append(Paragraph("8. Reflexión final", st['h2']))
    story.append(Paragraph("Responde con tus propias palabras:", st['body']))
    story.append(Paragraph("• ¿Por qué es importante limpiar y preparar los datos antes de entrenar un modelo?", st['bullet']))
    story.append(Paragraph("• ¿Qué podría ocurrir si utilizamos datos incorrectos o incompletos?", st['bullet']))
    story.append(Paragraph("• ¿Por qué debemos separar los datos de entrenamiento de los datos de prueba?", st['bullet']))
    story.append(Paragraph("• ¿Qué información aporta una matriz de confusión?", st['bullet']))
    story.append(Paragraph("• ¿Qué diferencia existe entre precisión y recall?", st['bullet']))
    story.append(Paragraph("• ¿Consideras que un modelo de Machine Learning debería tomar por sí solo la decisión final sobre si un estudiante aprueba o desaprueba? Fundamenta tu respuesta.", st['bullet']))
    story.append(Paragraph("• ¿Qué otros datos podrían incorporarse al proyecto para intentar mejorar el análisis?", st['bullet']))

    # --- Entrega y Producto Esperado (en bloque para no romperse) ---
    entrega_box = [
        Paragraph("<b>Entrega y Producto Esperado</b>", st['h2']),
        Paragraph("Presenta un informe breve que contenga: Descripción del problema, Identificación de variables, Análisis y limpieza de los datos, Preparación de los datos, Modelo seleccionado, Predicciones, Evaluación, Interpretación de resultados y Reflexión final.", st['body']),
        Spacer(1, 4),
        Paragraph("<b>Flujo completo del proyecto:</b>", st['body']),
        Paragraph("Problema → Datos → Limpieza → Preparación → Entrenamiento → Predicción → Evaluación → Interpretación", st['formula']),
        Spacer(1, 4),
        Paragraph("<i>No es necesario desarrollar un sistema complejo. Lo importante es comprender y explicar cada etapa de un proyecto de Machine Learning y justificar las decisiones tomadas.</i>", st['body'])
    ]
    
    tbl_entrega = Table([[entrega_box]], colWidths=[504])
    tbl_entrega.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 8))
    story.append(KeepTogether([tbl_entrega]))

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="ACTIVIDAD INTEGRADORA · MÓDULO 2", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de actividad generado con éxito: {filename}")


if __name__ == "__main__":
    create_activity_pdf()