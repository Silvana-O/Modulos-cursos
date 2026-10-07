import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Encabezados y Pies de página)
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    """
    Canvas dinámico con la línea gráfica de CURSOS CC.
    Acepta un subtítulo personalizado para diferenciar Teórico de Actividades.
    """
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL")
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
        
        # Colores corporativos (Ciberseguridad / CURSOS CC)
        teal_color = colors.HexColor("#0d9488")
        gray_text = colors.HexColor("#64748b")
        
        # --- Encabezado ---
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(teal_color)
        self.drawString(54, 750, "CURSOS CC")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(115, 750, f"|   {self.doc_subtitle.upper()}")
        
        # Página X
        page_str = f"Página {self._pageNumber}"
        self.drawRightString(612 - 54, 750, page_str)
        
        # Línea divisoria superior
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # --- Pie de página ---
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(54, 36, "Material educativo  •  Módulo 1: Fundamentos e historia de la IA")
        
        self.restoreState()


def get_common_styles():
    """Retorna los estilos globales de texto y párrafos."""
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")   # Slate 900
    COLOR_ACCENT = colors.HexColor("#0d9488")    # Teal 600
    COLOR_TEXT = colors.HexColor("#334155")      # Slate 700

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
        spaceBefore=12,
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
    
    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=style_body,
        leftIndent=12,
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
        'body': style_body,
        'bullet': style_bullet,
        'th': style_table_header,
        'td': style_table_cell,
        'td_bold': style_table_cell_bold
    }


# ----------------------------------------------------------------------
# DOCUMENTO 1: TEORÍA Y CONCEPTOS
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Material_1_IA_Teoria.pdf"):
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

    # --- Encabezado principal ---
    story.append(Paragraph("MÓDULO 1", st['tag']))
    story.append(Paragraph("Introducción a la Inteligencia Artificial", st['title']))
    story.append(Paragraph("Material Teórico • Fundamentos e Historia", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Descripción y Objetivos ---
    desc_text = "<b>Descripción del módulo:</b> Este material presenta los conceptos fundamentales para realizar un primer acercamiento a la Inteligencia Artificial. Se aborda qué es la IA, cómo se diferencia de la automatización tradicional, cuáles son algunas de sus aplicaciones actuales, los principales mitos asociados a esta tecnología y la prueba de Turing. También se introduce la importancia de los datos, los patrones y la evaluación crítica de los resultados generados por sistemas de IA."
    
    obj_content = [
        Paragraph(desc_text, st['body']),
        Spacer(1, 6),
        Paragraph("<b>Objetivos de aprendizaje:</b>", st['body']),
        Paragraph("• Explicar con sus propias palabras qué es la Inteligencia Artificial.", st['bullet']),
        Paragraph("• Diferenciar Inteligencia Artificial de una automatización tradicional.", st['bullet']),
        Paragraph("• Reconocer aplicaciones actuales de la IA en la vida cotidiana.", st['bullet']),
        Paragraph("• Identificar algunos mitos y limitaciones de los sistemas de IA.", st['bullet']),
        Paragraph("• Comprender de manera introductoria la prueba de Turing.", st['bullet']),
        Paragraph("• Reconocer la importancia de los datos y de la verificación de los resultados.", st['bullet']),
    ]
    
    obj_table = Table([[obj_content]], colWidths=[504])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 10))

    # --- 1. Qué es la IA ---
    story.append(Paragraph("1. ¿Qué es la Inteligencia Artificial?", st['h2']))
    story.append(Paragraph("La Inteligencia Artificial (IA) es un campo de la informática que estudia y desarrolla sistemas capaces de realizar tareas que normalmente asociamos con determinadas capacidades humanas, como reconocer patrones, interpretar información, aprender a partir de datos, procesar lenguaje, realizar predicciones o tomar determinadas decisiones.", st['body']))
    story.append(Paragraph("<b>Algunas tareas relacionadas con la IA son:</b>", st['body']))
    
    tasks = [
        "Reconocer objetos en una imagen.", "Identificar una voz.", "Traducir un texto.",
        "Recomendar contenido.", "Clasificar información.", "Realizar predicciones.",
        "Generar texto, imágenes o código."
    ]
    for t in tasks:
        story.append(Paragraph(f"• {t}", st['bullet']))
    
    # --- 2. IA y el pensamiento humano ---
    story.append(Paragraph("2. ¿La IA piensa como una persona?", st['h2']))
    story.append(Paragraph("Cuando decimos que una computadora «aprende», «reconoce» o «comprende», utilizamos palabras asociadas habitualmente con las personas. Sin embargo, esto no significa necesariamente que una máquina tenga pensamientos, emociones o conciencia como un ser humano. Un sistema de IA puede aprender patrones a partir de datos y utilizar esos patrones para producir una predicción.", st['body']))
    
    ejemplo_2 = [
        Paragraph("<b>Ejemplo:</b> Un sistema puede recibir miles de imágenes de perros y gatos, encontrar patrones presentes en ellas y luego clasificar una imagen nueva. El sistema produce una predicción a partir de lo aprendido; esto no implica que perciba o comprenda la imagen exactamente de la misma manera que una persona.", st['body'])
    ]
    tbl_ej2 = Table([[ejemplo_2]], colWidths=[504])
    tbl_ej2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_SECONDARY),
    ]))
    story.append(tbl_ej2)

    # --- 3. Automatización vs ML ---
    story.append(Paragraph("3. Inteligencia Artificial y automatización", st['h2']))
    story.append(Paragraph("No todo programa automático utiliza Inteligencia Artificial. Una automatización tradicional ejecuta reglas previamente definidas. Por ejemplo: <i>SI temperatura &gt; 30 → ENTONCES encender ventilador</i>. En cambio, en Machine Learning se utilizan datos para encontrar patrones que luego pueden utilizarse para realizar predicciones.", st['body']))
    
    data_aut = [
        [Paragraph("Automatización tradicional", st['th']), Paragraph("Machine Learning", st['th'])],
        [Paragraph("Reglas definidas previamente", st['td']), Paragraph("Patrones aprendidos a partir de datos", st['td'])],
        [Paragraph("Las reglas son explícitas", st['td']), Paragraph("El modelo encuentra relaciones en los datos", st['td'])],
        [Paragraph("No necesita aprender de ejemplos", st['td']), Paragraph("Necesita datos para entrenarse", st['td'])]
    ]
    tbl_aut = Table(data_aut, colWidths=[252, 252])
    tbl_aut.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_aut)

    # --- 4. Aplicaciones ---
    story.append(Paragraph("4. Aplicaciones de la IA", st['h2']))
    data_app = [
        [Paragraph("Aplicación", st['th']), Paragraph("Ejemplo de uso", st['th'])],
        [Paragraph("Motores de búsqueda", st['td_bold']), Paragraph("Interpretación de consultas y selección de resultados relevantes.", st['td'])],
        [Paragraph("Sistemas de recomendación", st['td_bold']), Paragraph("Recomendación de películas, música, videos o productos a partir de diferentes señales y patrones.", st['td'])],
        [Paragraph("Asistentes de voz", st['td_bold']), Paragraph("Reconocimiento del habla y procesamiento del lenguaje natural.", st['td'])],
        [Paragraph("Traducción automática", st['td_bold']), Paragraph("Procesamiento de información lingüística para producir traducciones.", st['td'])],
        [Paragraph("Visión por computadora", st['td_bold']), Paragraph("Identificación y clasificación de objetos o características en imágenes.", st['td'])],
        [Paragraph("Detección de fraude", st['td_bold']), Paragraph("Identificación de operaciones que presentan patrones diferentes de los habituales.", st['td'])],
        [Paragraph("Educación", st['td_bold']), Paragraph("Generación de ejercicios, adaptación de materiales y asistencia a docentes y estudiantes.", st['td'])],
    ]
    tbl_app = Table(data_app, colWidths=[160, 344])
    tbl_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_app)

    # --- 5. IA Generativa ---
    story.append(Paragraph("5. IA generativa", st['h2']))
    story.append(Paragraph("La Inteligencia Artificial Generativa comprende sistemas capaces de producir contenido nuevo a partir de instrucciones. Entre los contenidos que pueden generar se encuentran texto, imágenes, audio, video y código.", st['body']))
    story.append(Paragraph("Una instrucción dada a un sistema generativo suele denominarse <b>prompt</b>. Por ejemplo: <i>«Explica el concepto de energía cinética para un estudiante de educación media utilizando un ejemplo cotidiano»</i>. El sistema genera una respuesta siguiendo esa instrucción.", st['body']))

    # --- 6. Mitos y Realidades ---
    story.append(Paragraph("6. Mitos y realidades", st['h2']))
    mitos = [
        ("Mito: La IA piensa exactamente como una persona.", "Realidad: Puede realizar tareas asociadas con capacidades humanas, pero eso no significa que funcione igual que el cerebro humano."),
        ("Mito: La IA siempre tiene razón.", "Realidad: Puede producir resultados incorrectos. En sistemas generativos puede presentar información falsa o no verificada."),
        ("Mito: La IA puede hacer cualquier cosa.", "Realidad: Cada sistema tiene capacidades, condiciones de funcionamiento y limitaciones específicas."),
        ("Mito: Toda automatización es IA.", "Realidad: Existen automatizaciones basadas solamente en reglas previamente programadas."),
        ("Mito: La IA apareció recientemente.", "Realidad: La investigación en IA tiene varias décadas de historia."),
        ("Mito: La IA reemplazará automáticamente todos los trabajos.", "Realidad: El impacto sobre el trabajo depende de las tareas, tecnologías, organizaciones y otros factores.")
    ]
    for m, r in mitos:
        m_content = [
            Paragraph(f"<b>{m}</b>", ParagraphStyle('MitoStyle', parent=st['body'], textColor=colors.HexColor("#991b1b"))),
            Paragraph(f"<b>{r}</b>", ParagraphStyle('RealidadStyle', parent=st['body'], textColor=colors.HexColor("#166534")))
        ]
        t_m = Table([[m_content]], colWidths=[504])
        t_m.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_m)
        story.append(Spacer(1, 3))

    # --- 7. Prueba de Turing ---
    story.append(Paragraph("7. La prueba de Turing", st['h2']))
    story.append(Paragraph("En 1950, Alan Turing planteó una forma de abordar la pregunta sobre si las máquinas podían pensar. En lugar de intentar definir directamente el pensamiento, propuso analizar si una máquina podía participar en una conversación de modo que un evaluador no pudiera distinguirla de una persona bajo determinadas condiciones.", st['body']))
    story.append(Paragraph("En la idea básica de la prueba, un evaluador se comunica mediante texto con una persona y una máquina sin saber cuál es cuál. La cuestión central es si las respuestas de la máquina pueden resultar indistinguibles de las humanas en esa situación.", st['body']))
    story.append(Paragraph("<b>Importante:</b> Superar una prueba de conversación no demuestra por sí mismo que una máquina tenga conciencia, emociones, experiencias subjetivas o inteligencia general.", st['body']))

    # --- 8 & 9. Datos y Patrones ---
    story.append(Paragraph("8. IA, datos y patrones", st['h2']))
    story.append(Paragraph("Una gran parte de la IA moderna depende de los datos. Estos pueden ser números, textos, imágenes, sonidos, videos, registros de actividad o mediciones.", st['body']))
    
    data_viv = [
        [Paragraph("Superficie", st['th']), Paragraph("Habitaciones", st['th']), Paragraph("Distancia al centro", st['th']), Paragraph("Precio", st['th'])],
        [Paragraph("50 m²", st['td']), Paragraph("2", st['td']), Paragraph("5 km", st['td']), Paragraph("$100.000", st['td'])],
        [Paragraph("70 m²", st['td']), Paragraph("3", st['td']), Paragraph("4 km", st['td']), Paragraph("$140.000", st['td'])],
        [Paragraph("90 m²", st['td']), Paragraph("3", st['td']), Paragraph("2 km", st['td']), Paragraph("$190.000", st['td'])],
        [Paragraph("120 m²", st['td']), Paragraph("4", st['td']), Paragraph("1 km", st['td']), Paragraph("$250.000", st['td'])]
    ]
    tbl_viv = Table(data_viv, colWidths=[126, 126, 126, 126])
    tbl_viv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_viv)
    story.append(Spacer(1, 4))
    story.append(Paragraph("En este ejemplo, un algoritmo podría analizar las características de viviendas y sus precios para encontrar relaciones y realizar una predicción sobre una vivienda nueva. Este concepto será desarrollado en el módulo de Machine Learning.", st['body']))

    story.append(Paragraph("9. ¿Por qué los datos son importantes?", st['h2']))
    story.append(Paragraph("La calidad de los datos puede afectar los resultados de un sistema de IA. Datos con errores, información incompleta, poca variedad o representaciones desequilibradas pueden contribuir a resultados problemáticos.", st['body']))
    story.append(Paragraph("<b>Preguntas que debemos hacernos:</b>", st['body']))
    preguntas_datos = [
        "¿De dónde provienen los datos?", "¿Son suficientes?", "¿Son representativos?",
        "¿Tienen errores?", "¿Qué información contienen?", "¿Cómo fueron obtenidos?"
    ]
    for p in preguntas_datos:
        story.append(Paragraph(f"• {p}", st['bullet']))

    # --- 10 & 11. Capacidades, Limitaciones y Resumen ---
    story.append(Paragraph("10. Capacidades y limitaciones", st['h2']))
    story.append(Paragraph("<b>Capacidades:</b> Analizar información, encontrar patrones, clasificar, generar contenido, automatizar tareas, realizar predicciones, procesar lenguaje y analizar imágenes.", st['body']))
    story.append(Paragraph("<b>Limitaciones:</b> Cometer errores, producir información falsa, depender de los datos, presentar sesgos, interpretar incorrectamente instrucciones y generar respuestas convincentes pero incorrectas.", st['body']))
    story.append(Paragraph("<i>Una competencia fundamental en el uso de IA es evaluar críticamente sus resultados.</i>", st['body']))

    story.append(Paragraph("11. Para recordar", st['h2']))
    data_rec = [
        [Paragraph("Concepto", st['th']), Paragraph("Definición breve", st['th'])],
        [Paragraph("Inteligencia Artificial", st['td_bold']), Paragraph("Campo de la informática que desarrolla sistemas capaces de realizar determinadas tareas asociadas con capacidades inteligentes.", st['td'])],
        [Paragraph("Machine Learning", st['td_bold']), Paragraph("Métodos que permiten aprender patrones a partir de datos y utilizarlos para realizar predicciones o acciones.", st['td'])],
        [Paragraph("IA Generativa", st['td_bold']), Paragraph("IA capaz de generar contenido nuevo a partir de una entrada o instrucción.", st['td'])],
        [Paragraph("Automatización", st['td_bold']), Paragraph("Ejecución automática de tareas mediante reglas o procedimientos definidos.", st['td'])],
        [Paragraph("Prueba de Turing", st['td_bold']), Paragraph("Propuesta asociada a Alan Turing para analizar si el comportamiento conversacional de una máquina puede resultar indistinguible del de una persona.", st['td'])],
        [Paragraph("Datos", st['td_bold']), Paragraph("Información utilizada por los sistemas para analizar, entrenar modelos, encontrar patrones o realizar predicciones.", st['td'])]
    ]
    tbl_rec = Table(data_rec, colWidths=[150, 354])
    tbl_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_rec)

    # --- Glosario y Recursos ---
    story.append(Paragraph("Glosario del módulo", st['h2']))
    glosario_data = [
        [Paragraph("Término", st['th']), Paragraph("Definición", st['th'])],
        [Paragraph("Algoritmo", st['td_bold']), Paragraph("Conjunto de pasos o instrucciones utilizados para resolver un problema o realizar una tarea.", st['td'])],
        [Paragraph("Datos", st['td_bold']), Paragraph("Información que puede ser analizada o utilizada por un sistema.", st['td'])],
        [Paragraph("Patrón", st['td_bold']), Paragraph("Regularidad o relación que puede identificarse en un conjunto de datos.", st['td'])],
        [Paragraph("Modelo", st['td_bold']), Paragraph("Representación aprendida o construida para realizar una tarea, como una predicción.", st['td'])],
        [Paragraph("Predicción", st['td_bold']), Paragraph("Resultado estimado por un sistema a partir de información disponible.", st['td'])],
        [Paragraph("Prompt", st['td_bold']), Paragraph("Instrucción o entrada proporcionada a un sistema generativo para orientar su respuesta.", st['td'])],
        [Paragraph("Sesgo", st['td_bold']), Paragraph("Tendencia sistemática que puede afectar los datos, el modelo o sus resultados.", st['td'])],
        [Paragraph("Verificación", st['td_bold']), Paragraph("Proceso de comprobar si una información o resultado es correcto y confiable.", st['td'])],
    ]
    tbl_glos = Table(glosario_data, colWidths=[120, 384])
    tbl_glos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_glos)

    story.append(Paragraph("Recursos para profundizar", st['h2']))
    story.append(Paragraph("• Alan Turing, «Computing Machinery and Intelligence» (1950).", st['bullet']))
    story.append(Paragraph("• Materiales introductorios sobre Inteligencia Artificial y Machine Learning.", st['bullet']))
    story.append(Paragraph("• Documentación y recursos de Google Colab, que se utilizarán en materiales posteriores del módulo.", st['bullet']))

    # Crear PDF teórico
    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL - TEORÍA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento teórico generado: {filename}")


# ----------------------------------------------------------------------
# DOCUMENTO 2: ACTIVIDADES Y EVALUACIONES
# ----------------------------------------------------------------------
def create_activities_pdf(filename="Material_1_IA_Actividades.pdf"):
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

    # --- Encabezado principal ---
    story.append(Paragraph("MÓDULO 1", st['tag']))
    story.append(Paragraph("Introducción a la Inteligencia Artificial", st['title']))
    story.append(Paragraph("Guía de Actividades y Autoevaluación", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Actividad de Reflexión ---
    story.append(Paragraph("1. Actividad de reflexión", st['h2']))
    act_ref = [
        Paragraph("Responde las siguientes preguntas analizando los conceptos teóricos abordados en el módulo:", st['body']),
        Spacer(1, 4),
        Paragraph("• Una aplicación de mapas calcula automáticamente la ruta más rápida. ¿Necesariamente utiliza Inteligencia Artificial? Explica.", st['bullet']),
        Paragraph("• Una plataforma recomienda una película según el historial de visualización. ¿Qué datos podría utilizar?", st['bullet']),
        Paragraph("• Una IA genera una respuesta sobre un tema histórico. ¿Qué debería hacer el estudiante antes de utilizarla en un trabajo?", st['bullet']),
        Paragraph("• Una persona afirma: «Si una IA conversa como una persona, necesariamente piensa como una persona». Fundamenta tu posición.", st['bullet']),
    ]
    t_act_ref = Table([[act_ref]], colWidths=[504])
    t_act_ref.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_act_ref)
    story.append(Spacer(1, 10))

    # --- Actividad Práctica ---
    story.append(Paragraph("2. Actividad práctica: Detectar IA en nuestra vida cotidiana", st['h2']))
    story.append(Paragraph("Identifica cinco situaciones en las que interactúes con una aplicación o sistema que pueda utilizar Inteligencia Artificial (celular, redes sociales, buscadores, entretenimiento, transporte, correo, videojuegos, etc.).", st['body']))
    
    data_pract = [
        [Paragraph("Aplicación o servicio", st['th']), Paragraph("¿Dónde aparece la IA?", st['th']), Paragraph("¿Qué tarea realiza?", st['th']), Paragraph("¿Qué datos podría utilizar?", st['th'])],
        [Paragraph("Ejemplo: Plataforma de música", st['td']), Paragraph("Recomendaciones", st['td']), Paragraph("Sugiere canciones", st['td']), Paragraph("Historial de reproducción", st['td'])],
        [Paragraph("1.", st['td']), Paragraph("", st['td']), Paragraph("", st['td']), Paragraph("", st['td'])],
        [Paragraph("2.", st['td']), Paragraph("", st['td']), Paragraph("", st['td']), Paragraph("", st['td'])],
        [Paragraph("3.", st['td']), Paragraph("", st['td']), Paragraph("", st['td']), Paragraph("", st['td'])],
        [Paragraph("4.", st['td']), Paragraph("", st['td']), Paragraph("", st['td']), Paragraph("", st['td'])],
        [Paragraph("5.", st['td']), Paragraph("", st['td']), Paragraph("", st['td']), Paragraph("", st['td'])],
    ]
    tbl_pract = Table(data_pract, colWidths=[120, 120, 134, 130])
    tbl_pract.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_pract)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Pregunta final:</b> ¿Cuál de los ejemplos encontrados te sorprendió más y por qué?", st['body']))
    story.append(Spacer(1, 10))

    # --- Autoevaluación ---
    story.append(Paragraph("3. Autoevaluación", st['h2']))
    
    # Preguntas limpias sin marcas de respuesta
    auto_q = [
        "<b>1. ¿Cuál describe mejor la IA?</b><br/>A) Cualquier programa automático.<br/>B) Un campo de la informática que desarrolla sistemas capaces de realizar determinadas tareas asociadas con capacidades inteligentes.<br/>C) Una máquina con conciencia.<br/>D) Un robot humanoide.",
        "<b>2. ¿Qué diferencia a Machine Learning de una automatización tradicional?</b><br/>A) Siempre utiliza robots.<br/>B) Puede aprender patrones a partir de datos.<br/>C) No necesita datos.<br/>D) Son exactamente lo mismo.",
        "<b>3. ¿Con quién se relaciona la prueba de Turing?</b><br/>A) Isaac Newton.<br/>B) Charles Babbage.<br/>C) Alan Turing.<br/>D) Steve Jobs.",
        "<b>4. ¿Cuál es correcta?</b><br/>A) Una IA siempre es correcta.<br/>B) Los datos no influyen.<br/>C) Una IA puede producir resultados incorrectos y deben evaluarse.<br/>D) Toda IA tiene conciencia.",
        "<b>5. Una plataforma recomienda películas según el historial del usuario. ¿Qué concepto se relaciona directamente?</b><br/>A) Sistemas de recomendación.<br/>B) Compresión de archivos.<br/>C) Texto manual.<br/>D) Sistema operativo.",
        "<b>6. Verdadero o Falso:</b><br/>a) Toda automatización es IA.<br/>b) La calidad de los datos puede afectar los resultados.<br/>c) La prueba de Turing demuestra conciencia.<br/>d) La IA puede analizar imágenes.<br/>e) Una respuesta generada por IA debe aceptarse siempre sin verificarla."
    ]
    
    for q in auto_q:
        story.append(Paragraph(q, st['body']))
        story.append(Spacer(1, 4))
    
    story.append(Spacer(1, 6))

    # --- Solucionario / Clave de Respuestas ---
    respuestas_content = [
        Paragraph("<b>Respuestas correctas (Autoevaluación):</b>", st['body']),
        Spacer(1, 3),
        Paragraph("<b>1:</b> B  |  <b>2:</b> B  |  <b>3:</b> C  |  <b>4:</b> C  |  <b>5:</b> A", st['body']),
        Paragraph("<b>6:</b> a) Falso, b) Verdadero, c) Falso, d) Verdadero, e) Falso", st['body'])
    ]
    
    tbl_respuestas = Table([[respuestas_content]], colWidths=[504])
    tbl_respuestas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    
    # KeepTogether asegura que el cuadro de respuestas no se rompa al final de la página
    story.append(KeepTogether([tbl_respuestas]))
    story.append(Spacer(1, 10))

    # --- Actividad de Cierre ---
    story.append(Paragraph("4. Actividad de cierre", st['h2']))
    cierre_box = [
        Paragraph("<b>¿Qué es la Inteligencia Artificial y por qué es importante aprender sobre ella actualmente?</b>", st['body']),
        Paragraph("La respuesta debería incluir:<br/>• Una definición de IA con tus propias palabras.<br/>• Un ejemplo de aplicación cotidiana.<br/>• Una capacidad de los sistemas de IA.<br/>• Una limitación.<br/>• Una reflexión sobre el uso responsable de la IA.<br/><br/><i>Extensión sugerida: 150 a 250 palabras.</i>", st['body'])
    ]
    t_cierre = Table([[cierre_box]], colWidths=[504])
    t_cierre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cierre)

    # Crear PDF de actividades
    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL - ACTIVIDADES", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de actividades generado: {filename}")


if __name__ == "__main__":
    create_theory_pdf()
    create_activities_pdf()