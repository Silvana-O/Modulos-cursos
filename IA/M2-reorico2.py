import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Paginación exacta 'Página X de Y')
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "APRENDIZAJE SUPERVISADO")
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
        
        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(teal_color)
        self.drawString(54, 750, "CURSOS CC")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(115, 750, f"|   {self.doc_subtitle.upper()}")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 750, page_str)
        
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(54, 36, "Material educativo  •  Módulo 2 - Material 2: Aprendizaje Supervisado")
        self.restoreState()


def get_common_styles():
    styles = getSampleStyleSheet()
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_TEXT = colors.HexColor("#334155")

    return {
        'tag': ParagraphStyle('ModuleTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=COLOR_ACCENT, spaceAfter=4),
        'title': ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=COLOR_PRIMARY, spaceAfter=6),
        'subtitle': ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=COLOR_TEXT, spaceAfter=12),
        'h2': ParagraphStyle('Heading2_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=COLOR_PRIMARY, spaceBefore=10, spaceAfter=4, keepWithNext=True),
        'body': ParagraphStyle('Body_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=COLOR_TEXT, spaceAfter=4),
        'bullet': ParagraphStyle('Bullet_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=COLOR_TEXT, leftIndent=12, firstLineIndent=-8, spaceAfter=2),
        'mono': ParagraphStyle('MonoCode', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1e293b")),
        'th': ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1),
        'td': ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=COLOR_TEXT, alignment=1),
        'td_left': ParagraphStyle('TableCellLeft', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=COLOR_TEXT, alignment=0),
        'td_bold': ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=COLOR_PRIMARY, alignment=0)
    }


# ----------------------------------------------------------------------
# DOCUMENTO 1: MATERIAL TEÓRICO COMPLETO
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Modulo2_Material2_Teoria.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=64, bottomMargin=54)
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")
    COLOR_CARD_BG = colors.HexColor("#f1f5f9")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_common_styles()
    story = []

    # Encabezado principal
    story.append(Paragraph("MÓDULO 2 · MATERIAL 2", st['tag']))
    story.append(Paragraph("Aprendizaje Supervisado: Regresión y Clasificación", st['title']))
    story.append(Paragraph("Material Teórico Completo • Fundamentos, Modelos y Conceptos Clave", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=10))

    # Descripción del material
    desc_p1 = "En el Material 1 conocimos el concepto de Machine Learning y el flujo general de un proyecto. En este material comenzaremos a estudiar una de las principales formas de aprendizaje automático: el <b>aprendizaje supervisado</b>."
    desc_p2 = "Aprenderemos cómo funcionan, a nivel introductorio, los problemas de regresión y clasificación, y conoceremos tres algoritmos fundamentales: <b>Regresión Lineal</b>, <b>Árboles de Decisión</b> y <b>k-Nearest Neighbors (k-NN)</b>.<br/><br/>El objetivo no es memorizar fórmulas ni implementar algoritmos complejos, sino comprender qué problema resuelve cada método, cómo utiliza los datos y qué tipo de resultado puede producir."
    
    tbl_desc = Table([[Paragraph(desc_p1, st['body'])], [Paragraph(desc_p2, st['body'])]], colWidths=[504])
    tbl_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tbl_desc)
    story.append(Spacer(1, 8))

    # 1. ¿Qué es el aprendizaje supervisado?
    story.append(Paragraph("1. ¿Qué es el aprendizaje supervisado?", st['h2']))
    story.append(Paragraph("El aprendizaje supervisado es un tipo de Machine Learning en el que el modelo aprende utilizando datos que incluyen un resultado conocido. Podemos imaginarlo como aprender a partir de ejemplos.", st['body']))
    
    data_sup = [
        [Paragraph("Horas de estudio", st['th']), Paragraph("Asistencia", st['th']), Paragraph("Resultado", st['th'])],
        [Paragraph("2", st['td']), Paragraph("60 %", st['td']), Paragraph("No aprueba", st['td'])],
        [Paragraph("4", st['td']), Paragraph("75 %", st['td']), Paragraph("Aprueba", st['td'])],
        [Paragraph("6", st['td']), Paragraph("90 %", st['td']), Paragraph("Aprueba", st['td'])],
        [Paragraph("1", st['td']), Paragraph("50 %", st['td']), Paragraph("No aprueba", st['td'])],
    ]
    tbl_sup = Table(data_sup, colWidths=[168, 168, 168])
    tbl_sup.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_sup)
    story.append(Spacer(1, 4))
    story.append(Paragraph("El modelo recibe: <b>Características → Resultado conocido</b>. Durante el entrenamiento intenta encontrar relaciones entre las características y el resultado. Después puede recibir un nuevo caso (ejemplo: <i>Horas: 5, Asistencia: 85 %</i>) y generar una predicción.", st['body']))

    # 2. Dos grandes tipos de problemas
    story.append(Paragraph("2. Dos grandes tipos de problemas", st['h2']))
    story.append(Paragraph("<b>Regresión:</b> Se utiliza cuando queremos predecir un valor numérico. Ejemplos: precio de una vivienda, temperatura, consumo de energía, tiempo de viaje, ventas de un producto.", st['body']))
    story.append(Paragraph("<i>Ejemplo:</i> ¿Cuál será aproximadamente el precio de una vivienda de 100 m²? → <b>Resultado posible: $210.000</b>", st['bullet']))
    story.append(Paragraph("<b>Clasificación:</b> Se utiliza cuando queremos asignar un dato a una categoría o clase. Ejemplos: spam / no spam, aprobado / no aprobado, gato / perro, fraude / operación normal, riesgo alto / medio / bajo.", st['body']))
    story.append(Paragraph("<i>Ejemplo:</i> ¿Este correo es spam? → <b>Resultado: Spam</b>", st['bullet']))

    # 3. Regresión vs. clasificación
    story.append(Paragraph("3. Regresión vs. Clasificación", st['h2']))
    story.append(Paragraph("Una forma sencilla de diferenciarlas es observar el tipo de resultado:", st['body']))
    
    data_comp = [
        [Paragraph("Regresión", st['th']), Paragraph("Clasificación", st['th'])],
        [Paragraph("Produce un valor numérico", st['td_left']), Paragraph("Produce una categoría", st['td_left'])],
        [Paragraph("Precio", st['td_left']), Paragraph("Spam / No spam", st['td_left'])],
        [Paragraph("Temperatura", st['td_left']), Paragraph("Aprobado / No aprobado", st['td_left'])],
        [Paragraph("Cantidad de ventas", st['td_left']), Paragraph("Perro / Gato", st['td_left'])],
        [Paragraph("Tiempo estimado", st['td_left']), Paragraph("Riesgo alto / bajo", st['td_left'])],
    ]
    tbl_comp = Table(data_comp, colWidths=[252, 252])
    tbl_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_comp)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Regla sencilla:</b> Si queremos estimar una cantidad → <i>regresión</i>. Si queremos elegir una categoría → <i>clasificación</i>.", st['body']))

    # 4 & 5. Regresión lineal
    story.append(Paragraph("4. Regresión lineal", st['h2']))
    story.append(Paragraph("Es uno de los métodos más sencillos para comprender cómo un modelo realiza predicciones numéricas mediante una línea recta.", st['body']))
    
    data_reg = [
        [Paragraph("Horas de estudio", st['th']), Paragraph("Puntuación", st['th'])],
        [Paragraph("1", st['td']), Paragraph("45", st['td'])],
        [Paragraph("2", st['td']), Paragraph("50", st['td'])],
        [Paragraph("3", st['td']), Paragraph("58", st['td'])],
        [Paragraph("4", st['td']), Paragraph("65", st['td'])],
        [Paragraph("5", st['td']), Paragraph("72", st['td'])],
        [Paragraph("6", st['td']), Paragraph("78", st['td'])],
    ]
    tbl_reg = Table(data_reg, colWidths=[252, 252])
    tbl_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tbl_reg)
    story.append(Spacer(1, 4))
    
    graph_ascii = """Puntuación
   |
80 |                  ●
75 |               ●
70 |            ●
65 |         ●
60 |      ●
55 |
50 |   ●
45 |●
   +-------------------------
      1  2  3  4  5  6   Horas de estudio"""
    
    story.append(Preformatted(graph_ascii, st['mono']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Representación matemática:</b> <code>y = mx + b</code> (donde <i>y</i> es el valor predicho, <i>x</i> la característica, <i>m</i> la pendiente y <i>b</i> el intercepto).", st['body']))

    # 6 & 7. Ejemplo de Ventas y Limitaciones
    story.append(Paragraph("5. Ejemplo cotidiano y Limitaciones", st['h2']))
    story.append(Paragraph("Supongamos una relación Publicidad ($100 → $1.000, $200 → $1.800, $300 → $2.500, $400 → $3.100). Una inversión prevista de $500 producirá una estimación basada en patrones.", st['body']))
    story.append(Paragraph("<b>Limitaciones:</b> Supone relaciones lineales. Las predicciones pueden verse afectadas por datos insuficientes/incorrectos, variables omitidas, valores atípicos y cambios de entorno.", st['body']))

    # 8, 9, 10, 11 & 12. Clasificación y Árboles de Decisión
    story.append(Paragraph("6. Árboles de decisión", st['h2']))
    story.append(Paragraph("Un árbol de decisión utiliza preguntas estructuradas en raíz, nodos, ramas y hojas para tomar decisiones.", st['body']))
    
    tree_ascii = """                    ¿Edad >= 18?
                   /            \\
                 Sí              No
                /                  \\
       ¿Tiene permiso?            No
          /       \\
        Sí         No
        /           \\
     Apto          No apto"""
    
    story.append(Preformatted(tree_ascii, st['mono']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Ventajas:</b> Fáciles de interpretar y seguir. <b>Limitaciones:</b> Si es muy complejo puede sobreajustarse (overfitting) a los datos de entrenamiento.", st['body']))

    # 13, 14, 15 & 16. k-NN y Comparación
    story.append(Paragraph("7. k-Nearest Neighbors (k-NN)", st['h2']))
    story.append(Paragraph("Clasifica un nuevo dato observando cuáles son los datos conocidos más cercanos ('vecinos'). La variable <i>k</i> define la cantidad de vecinos a evaluar (ej. k=3 o k=5).", st['body']))

    # 17. Un mismo problema con diferentes soluciones
    story.append(Paragraph("8. Criterios de elección de algoritmos", st['h2']))
    story.append(Paragraph("La elección depende de: cantidad de datos, características disponibles, tipo de problema, rendimiento, interpretabilidad, tiempo de entrenamiento y recursos disponibles.", st['body']))

    # Glosario Completo
    story.append(Paragraph("9. Glosario de Términos", st['h2']))
    data_glo = [
        [Paragraph("Término", st['th']), Paragraph("Definición", st['th'])],
        [Paragraph("Aprendizaje supervisado", st['td_bold']), Paragraph("Tipo de ML que utiliza datos con resultados conocidos para entrenar un modelo.", st['td_left'])],
        [Paragraph("Regresión", st['td_bold']), Paragraph("Tipo de problema en el que se busca predecir un valor numérico.", st['td_left'])],
        [Paragraph("Clasificación", st['td_bold']), Paragraph("Tipo de problema en el que se busca asignar un dato a una categoría.", st['td_left'])],
        [Paragraph("Regresión lineal", st['td_bold']), Paragraph("Método que busca representar una relación lineal entre variables.", st['td_left'])],
        [Paragraph("Árbol de decisión", st['td_bold']), Paragraph("Modelo que utiliza condiciones organizadas en estructura de árbol.", st['td_left'])],
        [Paragraph("k-NN", st['td_bold']), Paragraph("Algoritmo que utiliza los k datos más cercanos para predecir.", st['td_left'])],
        [Paragraph("Característica", st['td_bold']), Paragraph("Variable utilizada como información de entrada para el modelo.", st['td_left'])],
        [Paragraph("Etiqueta", st['td_bold']), Paragraph("Resultado conocido utilizado como referencia en el entrenamiento.", st['td_left'])],
        [Paragraph("Predicción", st['td_bold']), Paragraph("Resultado generado por un modelo para nuevos datos.", st['td_left'])],
        [Paragraph("Vecino", st['td_bold']), Paragraph("Dato considerado cercano a otro según medidas de distancia.", st['td_left'])],
    ]
    tbl_glo = Table(data_glo, colWidths=[130, 374])
    tbl_glo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tbl_glo)

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="MATERIAL TEÓRICO COMPLETO", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"PDF Teórico completo generado: {filename}")


# ----------------------------------------------------------------------
# DOCUMENTO 2: ACTIVIDADES Y AUTOEVALUACIÓN COMPLETAS
# ----------------------------------------------------------------------
def create_activities_pdf(filename="Modulo2_Material2_Actividades.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=64, bottomMargin=54)
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")
    COLOR_CARD_BG = colors.HexColor("#f1f5f9")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_common_styles()
    story = []

    story.append(Paragraph("MÓDULO 2 · MATERIAL 2", st['tag']))
    story.append(Paragraph("Guía Completa de Actividades, Autoevaluación y Cierre", st['title']))
    story.append(Paragraph("Ejercicios Prácticos, Casos de Análisis y Preguntas de Reflexión", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=10))

    # 18. Actividad de clasificación
    story.append(Paragraph("1. Actividad de clasificación", st['h2']))
    story.append(Paragraph("Para cada situación indica si corresponde principalmente a regresión o clasificación:", st['body']))
    story.append(Paragraph("• <b>A.</b> Predecir el precio de una vivienda. __________________", st['bullet']))
    story.append(Paragraph("• <b>B.</b> Determinar si una transacción es fraudulenta o normal. __________________", st['bullet']))
    story.append(Paragraph("• <b>C.</b> Predecir la temperatura de mañana. __________________", st['bullet']))
    story.append(Paragraph("• <b>D.</b> Determinar si una fotografía contiene un perro o un gato. __________________", st['bullet']))
    story.append(Paragraph("• <b>E.</b> Estimar la cantidad de ventas de una tienda durante el próximo mes. __________________", st['bullet']))
    story.append(Spacer(1, 6))

    # 19. Actividad de análisis
    story.append(Paragraph("2. Actividad de análisis", st['h2']))
    story.append(Paragraph("Una empresa quiere crear un sistema que determine si un cliente podría abandonar su servicio. Cuenta con datos históricos: antigüedad, cantidad de reclamos, frecuencia de uso, tipo de plan y si abandonó o no el servicio.", st['body']))
    story.append(Paragraph("<b>a.</b> ¿Cuál sería la variable que queremos predecir?", st['bullet']))
    story.append(Paragraph("<b>b.</b> ¿Es un problema de regresión o clasificación?", st['bullet']))
    story.append(Paragraph("<b>c.</b> Menciona tres características que podrían utilizarse.", st['bullet']))
    story.append(Paragraph("<b>d.</b> ¿Podría utilizarse un árbol de decisión? Explica por qué.", st['bullet']))
    story.append(Paragraph("<b>e.</b> ¿Podría utilizarse k-NN? Explica brevemente.", st['bullet']))
    story.append(Spacer(1, 6))

    # 20. Actividad de reflexión
    story.append(Paragraph("3. Actividad de reflexión", st['h2']))
    story.append(Paragraph("Lee la siguiente afirmación: <i>'Si un modelo hizo una predicción correcta, entonces el modelo es bueno.'</i> ¿Estás de acuerdo? Explica tu respuesta.", st['body']))
    story.append(Spacer(1, 6))

    # 22. Autoevaluación
    story.append(Paragraph("4. Autoevaluación", st['h2']))
    q_content = [
        Paragraph("<b>1. ¿Qué caracteriza al aprendizaje supervisado?</b>", st['body']),
        Paragraph("A. No utiliza datos. | B. Aprende utilizando ejemplos que tienen un resultado conocido. | C. Siempre utiliza imágenes. | D. No necesita entrenamiento.", st['bullet']),
        Spacer(1, 3),
        Paragraph("<b>2. ¿Qué tipo de problema intenta resolver una regresión?</b>", st['body']),
        Paragraph("A. Predecir un valor numérico. | B. Elegir siempre entre dos categorías. | C. Ordenar archivos. | D. Crear imágenes.", st['bullet']),
        Spacer(1, 3),
        Paragraph("<b>3. ¿Cuál sería un problema de clasificación?</b>", st['body']),
        Paragraph("A. Predecir el precio de una casa. | B. Estimar la temperatura. | C. Determinar si un correo es spam. | D. Predecir las ventas.", st['bullet']),
        Spacer(1, 3),
        Paragraph("<b>4. ¿Qué representa la k en k-NN?</b>", st['body']),
        Paragraph("A. La cantidad de variables. | B. La cantidad de vecinos que se consideran. | C. La cantidad de etiquetas. | D. La cantidad de modelos.", st['bullet']),
        Spacer(1, 3),
        Paragraph("<b>5. ¿Qué estructura utiliza un árbol de decisión?</b>", st['body']),
        Paragraph("A. Una secuencia de preguntas o condiciones. | B. Una lista de imágenes. | C. Una base de datos sin categorías. | D. Una fórmula exclusivamente matemática.", st['bullet']),
        Spacer(1, 3),
        Paragraph("<b>6. Verdadero o Falso:</b>", st['body']),
        Paragraph("a. La regresión se utiliza para predecir valores numéricos. ( )", st['bullet']),
        Paragraph("b. La clasificación se utiliza para asignar categorías. ( )", st['bullet']),
        Paragraph("c. k-NN utiliza información de vecinos cercanos. ( )", st['bullet']),
        Paragraph("d. Un árbol de decisión no necesita datos para funcionar. ( )", st['bullet']),
        Paragraph("e. Un modelo puede equivocarse. ( )", st['bullet']),
        Paragraph("f. Siempre existe un único algoritmo adecuado para un problema. ( )", st['bullet']),
    ]
    
    tbl_auto = Table([[q_content]], colWidths=[504])
    tbl_auto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_auto)
    story.append(Spacer(1, 6))

    # 24. Actividad de cierre
    story.append(Paragraph("5. Actividad de cierre", st['h2']))
    data_cierre = [
        [Paragraph("Sistema", st['th']), Paragraph("Problema", st['th']), Paragraph("Tipo de aprendizaje", st['th']), Paragraph("Posible método", st['th'])],
        [Paragraph("Sistema A: Estimar precio de vivienda", st['td_left']), Paragraph("Regresión", st['td']), Paragraph("Supervisado", st['td']), Paragraph("Regresión lineal", st['td'])],
        [Paragraph("Sistema B: Perro o gato en foto", st['td_left']), Paragraph("Clasificación", st['td']), Paragraph("Supervisado", st['td']), Paragraph("Árbol de decisión / k-NN", st['td'])],
        [Paragraph("Sistema C: Transacción normal o sospechosa", st['td_left']), Paragraph("Clasificación", st['td']), Paragraph("Supervisado", st['td']), Paragraph("Árbol de decisión / k-NN", st['td'])],
    ]
    tbl_cierre = Table(data_cierre, colWidths=[150, 100, 114, 140])
    tbl_cierre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_cierre)

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="GUÍA DE ACTIVIDADES COMPLETA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"PDF de Actividades completo generado: {filename}")


if __name__ == "__main__":
    create_theory_pdf()
    create_activities_pdf()