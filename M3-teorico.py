import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Encabezados y Pies de página de dos pasadas)
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    """
    Canvas dinámico con línea gráfica corporativa y paginación exacta 'Página X de Y'.
    Acepta un subtítulo personalizado para diferenciar Teórico de Actividades.
    """
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "APRENDIZAJE NO SUPERVISADO")
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
        self.drawString(54, 36, "Material educativo  •  Módulo 2 - Material 3: Aprendizaje No Supervisado")
        
        self.restoreState()


def get_common_styles():
    """Retorna los estilos globales tipográficos y de párrafos."""
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")   # Slate 900
    COLOR_ACCENT = colors.HexColor("#0d9488")    # Teal 600
    COLOR_TEXT = colors.HexColor("#334155")      # Slate 700

    style_module_tag = ParagraphStyle(
        'ModuleTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=COLOR_ACCENT,
        spaceAfter=4,
        textTransform='uppercase'
    )
    
    style_doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_PRIMARY,
        spaceAfter=6
    )
    
    style_doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=COLOR_TEXT,
        spaceAfter=12
    )
    
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=COLOR_TEXT,
        spaceAfter=6
    )
    
    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=style_body,
        leftIndent=12,
        firstLineIndent=-10,
        spaceAfter=3
    )

    style_code_box = ParagraphStyle(
        'CodeBox',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b")
    )
    
    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    
    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
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
        'body': style_body,
        'bullet': style_bullet,
        'code': style_code_box,
        'th': style_table_header,
        'td': style_table_cell,
        'td_bold': style_table_cell_bold
    }


# ----------------------------------------------------------------------
# DOCUMENTO 1: MATERIAL TEÓRICO
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Modulo2_Material3_Teoria.pdf"):
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
    COLOR_CARD_BG = colors.HexColor("#f1f5f9")
    COLOR_BORDER = colors.HexColor("#cbd5e1")
    
    st = get_common_styles()
    story = []

    # --- Header Principal ---
    story.append(Paragraph("MÓDULO 2 · MATERIAL 3", st['tag']))
    story.append(Paragraph("Aprendizaje No Supervisado: Clustering y Reducción de Dimensionalidad", st['title']))
    story.append(Paragraph("Material Teórico • Fundamentos, Algoritmos y Aplicaciones", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Descripción y Objetivos ---
    desc_text = "<b>Descripción:</b> En los materiales anteriores estudiamos qué es Machine Learning y cómo funcionan algunos métodos de aprendizaje supervisado, donde los datos contienen información sobre el resultado esperado. En este material conoceremos el aprendizaje no supervisado, donde el sistema trabaja con datos sin etiquetas previas para descubrir estructuras, grupos y patrones no evidentes a simple vista."
    
    obj_content = [
        Paragraph(desc_text, st['body']),
        Spacer(1, 4),
        Paragraph("<b>Objetivos de aprendizaje:</b>", st['body']),
        Paragraph("• Explicar qué es el aprendizaje no supervisado y diferenciarlo del supervisado.", st['bullet']),
        Paragraph("• Comprender el concepto de clustering y la técnica K-Means a nivel introductorio.", st['bullet']),
        Paragraph("• Reconocer aplicaciones prácticas del agrupamiento en diferentes dominios.", st['bullet']),
        Paragraph("• Comprender qué es la reducción de dimensionalidad (PCA) y para qué se utiliza.", st['bullet']),
    ]
    
    obj_table = Table([[obj_content]], colWidths=[504])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 10))

    # --- 1. ¿Qué es el aprendizaje no supervisado? ---
    story.append(Paragraph("1. ¿Qué es el aprendizaje no supervisado?", st['h2']))
    story.append(Paragraph("En el aprendizaje supervisado, el modelo recibe ejemplos en los que conocemos el resultado esperado (por ejemplo, relacionar <i>Horas de estudio</i> y <i>Asistencia</i> con un <i>Resultado</i> de Aprobado/No Aprobado). En el aprendizaje no supervisado, en cambio, no tenemos esa columna de resultado.", st['body']))
    
    # Tabla Comparativa de Datos
    data_ej_sup = [
        [Paragraph("Horas de estudio", st['th']), Paragraph("Asistencia", st['th']), Paragraph("Resultado (Supervisado)", st['th'])],
        [Paragraph("2", st['td']), Paragraph("60%", st['td']), Paragraph("No aprobado", st['td'])],
        [Paragraph("5", st['td']), Paragraph("80%", st['td']), Paragraph("Aprobado", st['td'])],
        [Paragraph("8", st['td']), Paragraph("95%", st['td']), Paragraph("Aprobado", st['td'])],
    ]
    tbl_sup = Table(data_ej_sup, colWidths=[168, 168, 168])
    tbl_sup.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_sup)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Si eliminamos la etiqueta de resultado, el algoritmo no supervisado debe intentar encontrar alguna estructura dentro de los datos (por ejemplo, descubrir que existen grupos de estudiantes con características similares).", st['body']))

    idea_box = [Paragraph("<b>Idea principal:</b> En el aprendizaje no supervisado, el modelo busca patrones o estructuras en los datos sin disponer de etiquetas previamente conocidas.", st['body'])]
    tbl_idea = Table([[idea_box]], colWidths=[504])
    tbl_idea.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_idea)

    # --- 2. Supervisado vs. No Supervisado ---
    story.append(Paragraph("2. Supervisado vs. no supervisado", st['h2']))
    data_comp = [
        [Paragraph("Característica", st['th']), Paragraph("Supervisado", st['th']), Paragraph("No supervisado", st['th'])],
        [Paragraph("¿Tiene etiquetas?", st['td_bold']), Paragraph("Sí", st['td']), Paragraph("No", st['td'])],
        [Paragraph("¿Conoce el resultado?", st['td_bold']), Paragraph("Sí", st['td']), Paragraph("No", st['td'])],
        [Paragraph("Objetivo", st['td_bold']), Paragraph("Predecir", st['td']), Paragraph("Encontrar patrones", st['td'])],
        [Paragraph("Ejemplo", st['td_bold']), Paragraph("Detectar spam", st['td']), Paragraph("Agrupar clientes", st['td'])],
        [Paragraph("Técnicas", st['td_bold']), Paragraph("Regresión, clasificación", st['td']), Paragraph("Clustering, reducción de dimensionalidad", st['td'])],
    ]
    tbl_comp = Table(data_comp, colWidths=[130, 187, 187])
    tbl_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_comp)

    # --- 3 & 4. Clustering y Representación ---
    story.append(Paragraph("3. ¿Qué es el clustering?", st['h2']))
    story.append(Paragraph("Clustering (o agrupamiento) es una técnica que busca dividir un conjunto de datos en grupos cuyos elementos tengan características similares. Cada grupo recibe el nombre de <b>cluster</b>. Los grupos no son definidos por una persona, sino descubiertos a partir de datos como edad, frecuencia de compra o gasto.", st['body']))

    story.append(Paragraph("4. Una representación sencilla", st['h2']))
    story.append(Paragraph("Podemos representar visualmente a los individuos en un plano cartesiano (Edad vs. Gasto Mensual). Los puntos cercanos forman concentraciones de datos que el clustering intenta identificar automáticamente:", st['body']))

    ascii_art = """Gasto
  ↑
  |                 ● ●
  |              ● ● ●
  |       ● ●
  |      ● ● ●
  |                         ●
  |                       ● ●
  +--------------------------------→ Edad"""
    
    tbl_ascii = Table([[Paragraph(ascii_art.replace('\n', '<br/>').replace(' ', '&nbsp;'), st['code'])]], colWidths=[504])
    tbl_ascii.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tbl_ascii)

    # --- 5 & 6. K-Means ---
    story.append(Paragraph("5. Algoritmo K-Means", st['h2']))
    story.append(Paragraph("Es uno de los algoritmos de clustering más conocidos. La letra <b>K</b> representa la cantidad de grupos elegida (ej. K=3). La palabra <i>Means</i> hace referencia a la media o promedio. K-Means intenta encontrar un punto representativo para cada grupo, llamado <b>centroide</b>.", st['body']))

    story.append(Paragraph("6. ¿Cómo funciona K-Means?", st['h2']))
    steps_kmeans = [
        Paragraph("<b>Paso 1: Elegir K.</b> Decidir cuántos grupos se desea formar (ej. K = 3).", st['bullet']),
        Paragraph("<b>Paso 2: Ubicar centroides iniciales.</b> El algoritmo establece K puntos provisionales en el espacio.", st['bullet']),
        Paragraph("<b>Paso 3: Asignar datos al centroide más cercano.</b> Cada punto se asocia a su centroide próximo.", st['bullet']),
        Paragraph("<b>Paso 4: Recalcular centroides.</b> Se calcula la posición central real de los puntos asignados a cada grupo.", st['bullet']),
        Paragraph("<b>Paso 5: Repetir.</b> El proceso se itera hasta que los grupos dejan de cambiar significativamente.", st['bullet']),
    ]
    for s in steps_kmeans:
        story.append(s)

    # --- 7, 8 & 9. Ejemplo, Elección de K y Aplicaciones ---
    story.append(Paragraph("7. Ejemplo y elección del número K", st['h2']))
    story.append(Paragraph("En un análisis de clientes con K=3, K-Means podría segmentar: <i>Grupo 1 (Bajo gasto/poca frecuencia)</i>, <i>Grupo 2 (Gasto medio/frecuencia alta)</i> y <i>Grupo 3 (Alto gasto/frecuencia alta)</i>. La interpretación del significado de cada grupo la realiza posteriormente el especialista.", st['body']))
    story.append(Paragraph("Para elegir K se suele utilizar el <b>método del codo</b>: se evalúa cómo cambia el error interno del agrupamiento al variar K; cuando aumentar K deja de producir mejoras importantes, se identifica un punto similar a un 'codo'.", st['body']))

    story.append(Paragraph("8. Aplicaciones del clustering", st['h2']))
    apps = [
        "<b>Segmentación de clientes:</b> Agrupar usuarios según hábitos de consumo o gasto.",
        "<b>Agrupamiento de documentos:</b> Clasificar textos automáticamente por temática (deportes, economía, tecnología).",
        "<b>Análisis de imágenes y recomendación:</b> Detectar regiones con características similares o identificar patrones de comportamiento entre usuarios.",
        "<b>Detección de anomalías:</b> Identificar comportamientos que se alejan significativamente de los patrones habituales."
    ]
    for a in apps:
        story.append(Paragraph(f"• {a}", st['bullet']))

    # --- 10 & 11. Clustering vs Clasificación y Reducción de Dimensionalidad ---
    story.append(Paragraph("9. Clustering no es Clasificación", st['h2']))
    story.append(Paragraph("En <b>clasificación</b> las categorías ya están previamente definidas (ej. Correo → Spam / No Spam). En <b>clustering</b> las categorías NO existen de antemano; el algoritmo descubre las agrupaciones presentes en los datos.", st['body']))

    story.append(Paragraph("10. Reducción de dimensionalidad y PCA", st['h2']))
    story.append(Paragraph("Cuando un dataset contiene decenas o cientos de características (edad, ingresos, compras, tiempo de sesión, etc.), decimos que tiene alta dimensionalidad. La <b>reducción de dimensionalidad</b> busca representar los datos con menos variables conservando la mayor cantidad de información relevante.", st['body']))
    story.append(Paragraph("Una técnica fundamental es <b>PCA (Análisis de Componentes Principales)</b>, la cual transforma múltiples características originales en un número menor de componentes principales que resumen la variabilidad de los datos.", st['body']))

    # --- Resumen y Glosario ---
    story.append(Paragraph("11. Glosario de conceptos", st['h2']))
    glosario_data = [
        [Paragraph("Concepto", st['th']), Paragraph("Definición", st['th'])],
        [Paragraph("Aprendizaje No Supervisado", st['td_bold']), Paragraph("Enfoque de ML que busca patrones o estructuras sin etiquetas conocidas.", st['td'])],
        [Paragraph("Clustering", st['td_bold']), Paragraph("Técnica para agrupar datos según su similitud.", st['td'])],
        [Paragraph("K-Means / Centroide", st['td_bold']), Paragraph("Algoritmo de agrupamiento basado en K centroides que representan el centro de cada grupo.", st['td'])],
        [Paragraph("Reducción de Dimensionalidad", st['td_bold']), Paragraph("Proceso de representar datos complejos utilizando menos dimensiones/variables.", st['td'])],
        [Paragraph("PCA", st['td_bold']), Paragraph("Análisis de Componentes Principales. Transforma variables originales en componentes principales sintetizados.", st['td'])],
    ]
    tbl_glos = Table(glosario_data, colWidths=[150, 354])
    tbl_glos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([tbl_glos]))

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="APRENDIZAJE NO SUPERVISADO - TEORÍA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento teórico generado: {filename}")


# ----------------------------------------------------------------------
# DOCUMENTO 2: ACTIVIDADES Y EVALUACIONES
# ----------------------------------------------------------------------
def create_activities_pdf(filename="Modulo2_Material3_Actividades.pdf"):
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
    
    st = get_common_styles()
    story = []

    # --- Header Principal ---
    story.append(Paragraph("MÓDULO 2 · MATERIAL 3", st['tag']))
    story.append(Paragraph("Aprendizaje No Supervisado: Clustering y Reducción de Dimensionalidad", st['title']))
    story.append(Paragraph("Guía de Actividades, Análisis y Autoevaluación", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Actividad 1: Descubrir grupos ---
    story.append(Paragraph("1. Actividad práctica: Descubrir grupos de clientes", st['h2']))
    story.append(Paragraph("Una empresa registra la siguiente información sobre seis clientes:", st['body']))
    
    data_cli = [
        [Paragraph("Cliente", st['th']), Paragraph("Compras por mes", st['th']), Paragraph("Gasto mensual ($)", st['th'])],
        [Paragraph("A", st['td']), Paragraph("2", st['td']), Paragraph("50", st['td'])],
        [Paragraph("B", st['td']), Paragraph("3", st['td']), Paragraph("70", st['td'])],
        [Paragraph("C", st['td']), Paragraph("8", st['td']), Paragraph("250", st['td'])],
        [Paragraph("D", st['td']), Paragraph("7", st['td']), Paragraph("220", st['td'])],
        [Paragraph("E", st['td']), Paragraph("1", st['td']), Paragraph("30", st['td'])],
        [Paragraph("F", st['td']), Paragraph("9", st['td']), Paragraph("280", st['td'])],
    ]
    tbl_cli = Table(data_cli, colWidths=[168, 168, 168])
    tbl_cli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_cli)
    story.append(Spacer(1, 6))

    act1_questions = [
        Paragraph("<b>Preguntas de análisis:</b>", st['body']),
        Paragraph("1. ¿Qué clientes parecen tener comportamientos similares?", st['bullet']),
        Paragraph("2. ¿Cuántos grupos identificarías observando los datos y qué características utilizaste?", st['bullet']),
        Paragraph("3. ¿Qué podría significar comercialmente cada grupo?", st['bullet']),
        Paragraph("4. Para realizar este análisis de forma automática, ¿utilizarías aprendizaje supervisado o no supervisado?", st['bullet']),
    ]
    t_act1 = Table([[act1_questions]], colWidths=[504])
    t_act1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_act1)
    story.append(Spacer(1, 10))

    # --- Actividad 2: Clasificación o Clustering ---
    story.append(Paragraph("2. Actividad: Clasificación vs. Clustering", st['h2']))
    story.append(Paragraph("Indica qué enfoque (Supervisado o No Supervisado) utilizarías en cada situación:", st['body']))
    
    situaciones = [
        ("Situación A", "Una institución quiere predecir si un estudiante aprobará o no a partir de datos históricos."),
        ("Situación B", "Una empresa quiere descubrir grupos de clientes con comportamientos similares sin categorías previas."),
        ("Situación C", "Un banco quiere detectar fraudes utilizando ejemplos históricos etiquetados como normales o fraudulentos."),
        ("Situación D", "Una tienda busca descubrir diferentes perfiles de compradores a partir de sus hábitos de consumo.")
    ]
    for sit, desc in situaciones:
        story.append(Paragraph(f"• <b>{sit}:</b> {desc}", st['bullet']))
    story.append(Spacer(1, 10))

    # --- Actividad 3: Reflexión analítica ---
    story.append(Paragraph("3. Actividad de reflexión crítica", st['h2']))
    refl_box = [
        Paragraph("<b>Analiza la siguiente afirmación:</b>", st['body']),
        Paragraph("<i>«El algoritmo encontró tres grupos, por lo tanto sabemos que existen exactamente tres tipos de clientes.»</i>", st['body']),
        Spacer(1, 4),
        Paragraph("<b>Consigna:</b> ¿Estás de acuerdo? Explica tu respuesta teniendo en cuenta cómo influyen las decisiones del analista, la elección de K y las variables seleccionadas.", st['body'])
    ]
    t_refl = Table([[refl_box]], colWidths=[504])
    t_refl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_refl)
    story.append(Spacer(1, 10))

    # --- Autoevaluación ---
    story.append(Paragraph("4. Autoevaluación de conocimientos", st['h2']))
    
    auto_q = [
        "<b>1. ¿Qué caracteriza al aprendizaje no supervisado?</b><br/>A) Trabaja siempre con datos etiquetados.<br/>B) Busca patrones o estructuras sin disponer de etiquetas conocidas.<br/>C) Solamente sirve para realizar regresiones.<br/>D) No utiliza datos.",
        "<b>2. ¿Qué es clustering?</b><br/>A) Un método para eliminar datos.<br/>B) Una técnica para agrupar datos según su similitud.<br/>C) Un tipo de red neuronal.<br/>D) Una técnica exclusiva de clasificación.",
        "<b>3. En K-Means, ¿qué representa la letra K?</b><br/>A) La cantidad de características.<br/>B) La cantidad de datos.<br/>C) La cantidad de grupos que se desea formar.<br/>D) La cantidad de predicciones.",
        "<b>4. ¿Cuál es el objetivo principal de la reducción de dimensionalidad?</b><br/>A) Aumentar la cantidad de variables.<br/>B) Representar los datos utilizando menos dimensiones.<br/>C) Convertir todos los datos en etiquetas.<br/>D) Eliminar todos los registros.",
        "<b>5. ¿Qué significa PCA?</b><br/>A) Predictive Classification Algorithm.<br/>B) Principal Component Analysis.<br/>C) Programming Component Architecture.<br/>D) Python Clustering Algorithm.",
        "<b>6. Verdadero o Falso:</b><br/>a) K-Means es una técnica de clustering.<br/>b) En clustering las categorías siempre están definidas antes de comenzar.<br/>c) La reducción de dimensionalidad puede facilitar la visualización de datos.<br/>d) El número de grupos elegido en K-Means puede influir en el resultado."
    ]
    
    for q in auto_q:
        story.append(Paragraph(q, st['body']))
        story.append(Spacer(1, 4))

    # Solucionario
    respuestas_content = [
        Paragraph("<b>Clave de Respuestas (Autoevaluación):</b>", st['body']),
        Spacer(1, 2),
        Paragraph("<b>1:</b> B  |  <b>2:</b> B  |  <b>3:</b> C  |  <b>4:</b> B  |  <b>5:</b> B", st['body']),
        Paragraph("<b>6:</b> a) Verdadero, b) Falso, c) Verdadero, d) Verdadero", st['body'])
    ]
    tbl_resp = Table([[respuestas_content]], colWidths=[504])
    tbl_resp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([tbl_resp]))
    story.append(Spacer(1, 10))

    # --- Actividad Integradora Final ---
    story.append(Paragraph("5. Actividad integradora final", st['h2']))
    story.append(Paragraph("Una universidad desea analizar sus datos de estudiantes (edad, materias, asistencia, horas de estudio, actividades) sin categorías previas para descubrir perfiles de alumnos. Completa la tabla de planificación:", st['body']))

    data_plan = [
        [Paragraph("Pregunta", st['th']), Paragraph("Respuesta del estudiante", st['th'])],
        [Paragraph("¿Qué tipo de aprendizaje utilizarías?", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("¿Qué técnica específica se podría aplicar?", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("¿Qué características/variables seleccionarías?", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("¿Qué podría representar cada grupo descubierto?", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("¿Qué dificultades o sesgos podrían aparecer?", st['td_bold']), Paragraph("", st['td'])],
    ]
    tbl_plan = Table(data_plan, colWidths=[180, 324])
    tbl_plan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(KeepTogether([tbl_plan]))

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="APRENDIZAJE NO SUPERVISADO - ACTIVIDADES", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de actividades generado: {filename}")


if __name__ == "__main__":
    create_theory_pdf()
    create_activities_pdf()