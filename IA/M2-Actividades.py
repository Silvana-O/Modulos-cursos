import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO FOR ACTIVITIES
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "ACTIVIDADES Y AUTOEVALUACIÓN")
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
        self.drawString(54, 36, "Guía Práctica  •  Módulo 2 · Material 1")
        
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
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_TEXT,
        spaceAfter=6
    )

    style_option = ParagraphStyle(
        'Option_Custom',
        parent=style_body,
        leftIndent=15,
        spaceAfter=3
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

    return {
        'tag': style_module_tag,
        'title': style_doc_title,
        'subtitle': style_doc_subtitle,
        'h2': style_h2,
        'body': style_body,
        'option': style_option,
        'th': style_table_header,
        'td': style_table_cell
    }


# ----------------------------------------------------------------------
# GENERACIÓN DEL PDF DE ACTIVIDADES
# ----------------------------------------------------------------------
def create_activities_pdf(filename="Módulo_2_Actividades.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=64, bottomMargin=54
    )
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_SECONDARY = colors.HexColor("#0369a1")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_common_styles()
    story = []

    # --- Encabezado Principal ---
    story.append(Paragraph("MÓDULO 2 · MATERIAL 1", st['tag']))
    story.append(Paragraph("Guía de Actividades y Autoevaluación", st['title']))
    story.append(Paragraph("Ejercicios de reflexión, caso práctico y autoevaluación teórica", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- 1. Actividad de reflexión ---
    story.append(Paragraph("1. Actividad de reflexión", st['h2']))
    story.append(Paragraph("Responde con tus propias palabras a los siguientes planteamientos:", st['body']))
    
    preguntas_ref = [
        "1. ¿Cuál es la principal diferencia entre decirle a una computadora exactamente qué debe hacer y utilizar Machine Learning?",
        "2. ¿Por qué los datos son fundamentales e insustituibles para el Machine Learning?",
        "3. ¿Por qué no es suficiente entrenar un modelo y asumir inmediatamente que funciona correctamente?",
        "4. ¿Qué significa formalmente que un modelo realice una predicción?"
    ]
    for pr in preguntas_ref:
        story.append(Paragraph(f"<b>{pr}</b>", st['body']))
        story.append(Spacer(1, 15)) # Espacio para responder

    # --- 2. Actividad práctica ---
    story.append(Paragraph("2. Actividad práctica: Análisis de caso", st['h2']))
    story.append(Paragraph("Analiza la siguiente situación en una institución educativa:", st['body']))
    story.append(Paragraph("<i>Se busca desarrollar un sistema que estime si un estudiante podría necesitar apoyo adicional en una asignatura.</i>", st['body']))

    t_data_caso = [
        [Paragraph("Estudiante", st['th']), Paragraph("Asistencia", st['th']), Paragraph("Entregas realizadas", st['th']), Paragraph("Horas de estudio", st['th']), Paragraph("Resultado", st['th'])],
        [Paragraph("A", st['td']), Paragraph("95 %", st['td']), Paragraph("97 %", st['td']), Paragraph("8 hrs", st['td']), Paragraph("Adecuado", st['td'])],
        [Paragraph("B", st['td']), Paragraph("60 %", st['td']), Paragraph("42 %", st['td']), Paragraph("2 hrs", st['td']), Paragraph("Requiere apoyo", st['td'])],
        [Paragraph("C", st['td']), Paragraph("85 %", st['td']), Paragraph("85 %", st['td']), Paragraph("6 hrs", st['td']), Paragraph("Adecuado", st['td'])],
        [Paragraph("D", st['td']), Paragraph("55 %", st['td']), Paragraph("31 %", st['td']), Paragraph("1 hr", st['td']), Paragraph("Requiere apoyo", st['td'])]
    ]
    tbl_caso = Table(t_data_caso, colWidths=[70, 100, 110, 104, 120], repeatRows=1)
    tbl_caso.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_caso)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Consignas a resolver:</b>", st['body']))
    story.append(Paragraph("a. Identifica tres características (features) que podrían utilizarse.", st['body']))
    story.append(Paragraph("b. Identifica cuál es la etiqueta (label) del problema.", st['body']))
    story.append(Paragraph("c. Explica qué datos utilizarías concretamente para entrenar el modelo.", st['body']))
    story.append(Paragraph("d. ¿Por qué es estrictamente necesario evaluar el modelo con datos no utilizados en el entrenamiento?", st['body']))
    story.append(Paragraph("e. Menciona al menos una limitación o riesgo ético de implementar este sistema.", st['body']))
    story.append(Spacer(1, 10))

    # --- 3. Autoevaluación ---
    story.append(Paragraph("3. Autoevaluación", st['h2']))

    story.append(Paragraph("<b>1. ¿Qué es Machine Learning?</b>", st['body']))
    story.append(Paragraph("A. Un lenguaje de programación.", st['option']))
    story.append(Paragraph("B. Un conjunto de métodos que permite aprender patrones a partir de datos.", st['option']))
    story.append(Paragraph("C. Un tipo de computadora.", st['option']))
    story.append(Paragraph("D. Un sistema operativo.", st['option']))

    story.append(Paragraph("<b>2. En Machine Learning, ¿qué función cumplen los datos?</b>", st['body']))
    story.append(Paragraph("A. No tienen importancia.", st['option']))
    story.append(Paragraph("B. Se utilizan para analizar patrones y entrenar modelos.", st['option']))
    story.append(Paragraph("C. Solamente sirven para almacenar resultados.", st['option']))
    story.append(Paragraph("D. Reemplazan al algoritmo.", st['option']))

    story.append(Paragraph("<b>3. En la predicción del precio de una vivienda, ¿cuál es una característica?</b>", st['body']))
    story.append(Paragraph("A. El precio a predecir.", st['option']))
    story.append(Paragraph("B. La superficie de la vivienda.", st['option']))
    story.append(Paragraph("C. La estimación final.", st['option']))
    story.append(Paragraph("D. El resultado de la evaluación.", st['option']))

    story.append(Paragraph("<b>4. ¿Qué ocurre durante el entrenamiento?</b>", st['body']))
    story.append(Paragraph("A. Se elimina el modelo.", st['option']))
    story.append(Paragraph("B. El algoritmo utiliza datos para construir o ajustar el modelo.", st['option']))
    story.append(Paragraph("C. Se borran los datos.", st['option']))
    story.append(Paragraph("D. Se desconecta la computadora.", st['option']))

    story.append(Paragraph("<b>5. ¿Por qué se utilizan datos de prueba?</b>", st['body']))
    story.append(Paragraph("A. Para evaluar el funcionamiento con datos que no utilizó en el entrenamiento.", st['option']))
    story.append(Paragraph("B. Para aumentar la cantidad de datos automáticamente.", st['option']))
    story.append(Paragraph("C. Para reemplazar los datos de entrenamiento.", st['option']))
    story.append(Paragraph("D. Para evitar la evaluación.", st['option']))

    story.append(Paragraph("<b>6. Indique si las siguientes afirmaciones son Verdaderas (V) o Falsas (F):</b>", st['body']))
    story.append(Paragraph("a. Machine Learning y programación tradicional son exactamente lo mismo. (  )", st['option']))
    story.append(Paragraph("b. Un modelo puede producir predicciones incorrectas. (  )", st['option']))
    story.append(Paragraph("c. La calidad de los datos puede afectar los resultados. (  )", st['option']))
    story.append(Paragraph("d. Todos los problemas de Machine Learning utilizan etiquetas. (  )", st['option']))
    story.append(Paragraph("e. Es importante evaluar un modelo después de entrenarlo. (  )", st['option']))
    story.append(Spacer(1, 10))

    # --- 4. Actividad de Cierre ---
    story.append(Paragraph("4. Actividad de cierre", st['h2']))
    story.append(Paragraph(
        "Explica con tus propias palabras el flujo completo: <b>Datos → Entrenamiento → Modelo → Predicción → Evaluación</b>. "
        "Tu redacción debe detallar los insumos, el proceso de ajuste, qué representa la salida y la importancia de la métrica final (Extensión: 150 - 250 palabras).", st['body']
    ))
    story.append(Spacer(1, 15))

    # --- Solucionario en Cuadro Protegido ---
    solución_block = []
    solución_block.append(Paragraph("<b>Solucionario de Autoevaluación (Uso exclusivo para verificación)</b>", st['body']))
    
    t_sol_data = [
        [Paragraph("Pregunta", st['th']), Paragraph("Respuesta Correcta", st['th'])],
        [Paragraph("1", st['td']), Paragraph("B — Un conjunto de métodos que permite aprender patrones a partir de datos.", st['td'])],
        [Paragraph("2", st['td']), Paragraph("B — Se utilizan para analizar patrones y entrenar modelos.", st['td'])],
        [Paragraph("3", st['td']), Paragraph("B — La superficie de la vivienda.", st['td'])],
        [Paragraph("4", st['td']), Paragraph("B — El algoritmo utiliza datos para construir o ajustar el modelo.", st['td'])],
        [Paragraph("5", st['td']), Paragraph("A — Para evaluar el funcionamiento con datos no vistos.", st['td'])],
        [Paragraph("6", st['td']), Paragraph("a) F,  b) V,  c) V,  d) F,  e) V", st['td'])]
    ]
    tbl_sol = Table(t_sol_data, colWidths=[80, 424])
    tbl_sol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    solución_block.append(tbl_sol)
    
    story.append(KeepTogether(solución_block))

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="INTRODUCCIÓN AL MACHINE LEARNING - ACTIVIDADES", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de actividades generado con éxito: {filename}")


if __name__ == "__main__":
    create_activities_pdf()