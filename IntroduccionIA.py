import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para agregar encabezado y pie de página dinámico 
    estilo 'CURSOS CC' (similar al documento de Ciberseguridad).
    """
    def __init__(self, *args, **kwargs):
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
        
        # Colores corporativos (Inspirados en Ciberseguridad)
        primary_color = colors.HexColor("#0f172a") # Azul oscuro / Slate
        teal_color = colors.HexColor("#0d9488")    # Verde azulado / Teal
        gray_text = colors.HexColor("#64748b")     # Gris secundario
        
        # ---------------- ENCABEZADO ----------------
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(teal_color)
        self.drawString(54, 750, "CURSOS CC")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(115, 750, "|   INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL")
        
        # Número de página en encabezado derecho
        page_str = f"Página {self._pageNumber}"
        self.drawRightString(612 - 54, 750, page_str)
        
        # Línea divisoria superior
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)
        
        # ---------------- PIE DE PÁGINA ----------------
        self.setFont("Helvetica", 8)
        self.setFillColor(gray_text)
        self.drawString(54, 36, "Material educativo introductorio  •  Módulo 1: Fundamentos e historia")
        
        self.restoreState()

def create_ai_pdf(filename="Material_1_IA_Corregido_Diseno_CC.pdf"):
    # Configuración de página
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )
    
    # Paleta de colores
    COLOR_PRIMARY = colors.HexColor("#0f172a")   # Slate 900
    COLOR_SECONDARY = colors.HexColor("#0369a1") # Sky 700
    COLOR_ACCENT = colors.HexColor("#0d9488")    # Teal 600
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")  # Slate 50
    COLOR_CARD_BG = colors.HexColor("#f1f5f9")   # Slate 100
    COLOR_BORDER = colors.HexColor("#cbd5e1")    # Slate 300
    COLOR_TEXT = colors.HexColor("#334155")      # Slate 700

    styles = getSampleStyleSheet()
    
    # Estilos personalizados
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
        fontSize=24,
        leading=28,
        textColor=COLOR_PRIMARY,
        spaceAfter=8
    )
    
    style_doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=COLOR_TEXT,
        spaceAfter=15
    )
    
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=COLOR_PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
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

    story = []

    # ---------------- ENCABEZADO PRINCIPAL ----------------
    story.append(Paragraph("MÓDULO 1", style_module_tag))
    story.append(Paragraph("Introducción a la Inteligencia Artificial", style_doc_title))
    story.append(Paragraph("Fundamentos e historia de la Inteligencia Artificial", style_doc_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # ---------------- DESCRIPCIÓN Y OBJETIVOS EN CAJA ----------------
    desc_text = "<b>Descripción del módulo:</b> Este material presenta los conceptos fundamentales para realizar un primer acercamiento a la Inteligencia Artificial. Se aborda qué es la IA, cómo se diferencia de la automatización tradicional, cuáles son algunas de sus aplicaciones actuales, los principales mitos asociados a esta tecnología y la prueba de Turing. También se introduce la importancia de los datos, los patrones y la evaluación crítica de los resultados generados por sistemas de IA."
    
    obj_content = [
        Paragraph(desc_text, style_body),
        Spacer(1, 6),
        Paragraph("<b>Objetivos de aprendizaje:</b>", style_body),
        Paragraph("• Explicar con sus propias palabras qué es la Inteligencia Artificial.", style_bullet),
        Paragraph("• Diferenciar Inteligencia Artificial de una automatización tradicional.", style_bullet),
        Paragraph("• Reconocer aplicaciones actuales de la IA en la vida cotidiana.", style_bullet),
        Paragraph("• Identificar algunos mitos y limitaciones de los sistemas de IA.", style_bullet),
        Paragraph("• Comprender de manera introductoria la prueba de Turing.", style_bullet),
        Paragraph("• Reconocer la importancia de los datos y de la verificación de los resultados.", style_bullet),
    ]
    
    obj_table = Table([[obj_content]], colWidths=[504])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 10))

    # ---------------- SECCIÓN 1 ----------------
    story.append(Paragraph("1. ¿Qué es la Inteligencia Artificial?", style_h2))
    story.append(Paragraph("La Inteligencia Artificial (IA) es un campo de la informática que estudia y desarrolla sistemas capaces de realizar tareas que normalmente asociamos con determinadas capacidades humanas, como reconocer patrones, interpretar información, aprender a partir de datos, procesar lenguaje, realizar predicciones o tomar determinadas decisiones.", style_body))
    story.append(Paragraph("<b>Algunas tareas relacionadas con la IA son:</b>", style_body))
    
    tasks = [
        "Reconocer objetos en una imagen.", "Identificar una voz.", "Traducir un texto.",
        "Recomendar contenido.", "Clasificar información.", "Realizar predicciones.",
        "Generar texto, imágenes o código."
    ]
    for t in tasks:
        story.append(Paragraph(f"• {t}", style_bullet))
    
    # ---------------- SECCIÓN 2 ----------------
    story.append(Paragraph("2. ¿La IA piensa como una persona?", style_h2))
    story.append(Paragraph("Cuando decimos que una computadora «aprende», «reconoce» o «comprende», utilizamos palabras asociadas habitualmente con las personas. Sin embargo, esto no significa necesariamente que una máquina tenga pensamientos, emociones o conciencia como un ser humano. Un sistema de IA puede aprender patrones a partir de datos y utilizar esos patrones para producir una predicción.", style_body))
    
    ejemplo_2 = [
        Paragraph("<b>Ejemplo:</b> Un sistema puede recibir miles de imágenes de perros y gatos, encontrar patrones presentes en ellas y luego clasificar una imagen nueva. El sistema produce una predicción a partir de lo aprendido; esto no implica que perciba o comprenda la imagen exactamente de la misma manera que una persona.", style_body)
    ]
    tbl_ej2 = Table([[ejemplo_2]], colWidths=[504])
    tbl_ej2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_SECONDARY),
    ]))
    story.append(tbl_ej2)

    # ---------------- SECCIÓN 3 ----------------
    story.append(Paragraph("3. Inteligencia Artificial y automatización", style_h2))
    story.append(Paragraph("No todo programa automático utiliza Inteligencia Artificial. Una automatización tradicional ejecuta reglas previamente definidas. Por ejemplo: <i>SI temperatura &gt; 30 → ENTONCES encender ventilador</i>. En cambio, en Machine Learning se utilizan datos para encontrar patrones que luego pueden utilizarse para realizar predicciones.", style_body))
    
    # Tabla Aut vs ML
    data_aut = [
        [Paragraph("Automatización tradicional", style_table_header), Paragraph("Machine Learning", style_table_header)],
        [Paragraph("Reglas definidas previamente", style_table_cell), Paragraph("Patrones aprendidos a partir de datos", style_table_cell)],
        [Paragraph("Las reglas son explícitas", style_table_cell), Paragraph("El modelo encuentra relaciones en los datos", style_table_cell)],
        [Paragraph("No necesita aprender de ejemplos", style_table_cell), Paragraph("Necesita datos para entrenarse", style_table_cell)]
    ]
    tbl_aut = Table(data_aut, colWidths=[252, 252])
    tbl_aut.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tbl_aut)

    # ---------------- SECCIÓN 4 ----------------
    story.append(Paragraph("4. Aplicaciones de la IA", style_h2))
    data_app = [
        [Paragraph("Aplicación", style_table_header), Paragraph("Ejemplo de uso", style_table_header)],
        [Paragraph("Motores de búsqueda", style_table_cell_bold), Paragraph("Interpretación de consultas y selección de resultados relevantes.", style_table_cell)],
        [Paragraph("Sistemas de recomendación", style_table_cell_bold), Paragraph("Recomendación de películas, música, videos o productos a partir de diferentes señales y patrones.", style_table_cell)],
        [Paragraph("Asistentes de voz", style_table_cell_bold), Paragraph("Reconocimiento del habla y procesamiento del lenguaje natural.", style_table_cell)],
        [Paragraph("Traducción automática", style_table_cell_bold), Paragraph("Procesamiento de información lingüística para producir traducciones.", style_table_cell)],
        [Paragraph("Visión por computadora", style_table_cell_bold), Paragraph("Identificación y clasificación de objetos o características en imágenes.", style_table_cell)],
        [Paragraph("Detección de fraude", style_table_cell_bold), Paragraph("Identificación de operaciones que presentan patrones diferentes de los habituales.", style_table_cell)],
        [Paragraph("Educación", style_table_cell_bold), Paragraph("Generación de ejercicios, adaptación de materiales y asistencia a docentes y estudiantes.", style_table_cell)],
    ]
    tbl_app = Table(data_app, colWidths=[160, 344])
    tbl_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tbl_app)

    # ---------------- SECCIÓN 5 ----------------
    story.append(Paragraph("5. IA generativa", style_h2))
    story.append(Paragraph("La Inteligencia Artificial Generativa comprende sistemas capaces de producir contenido nuevo a partir de instrucciones. Entre los contenidos que pueden generar se encuentran texto, imágenes, audio, video y código.", style_body))
    story.append(Paragraph("Una instrucción dada a un sistema generativo suele denominarse <b>prompt</b>. Por ejemplo: <i>«Explica el concepto de energía cinética para un estudiante de educación media utilizando un ejemplo cotidiano»</i>. El sistema genera una respuesta siguiendo esa instrucción.", style_body))

    # ---------------- SECCIÓN 6 ----------------
    story.append(Paragraph("6. Mitos y realidades", style_h2))
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
            Paragraph(f"<b>{m}</b>", ParagraphStyle('MitoStyle', parent=style_body, textColor=colors.HexColor("#991b1b"))),
            Paragraph(f"<b>{r}</b>", ParagraphStyle('RealidadStyle', parent=style_body, textColor=colors.HexColor("#166534")))
        ]
        t_m = Table([[m_content]], colWidths=[504])
        t_m.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_m)
        story.append(Spacer(1, 4))

    # ---------------- SECCIÓN 7 ----------------
    story.append(Paragraph("7. La prueba de Turing", style_h2))
    story.append(Paragraph("En 1950, Alan Turing planteó una forma de abordar la pregunta sobre si las máquinas podían pensar. En lugar de intentar definir directamente el pensamiento, propuso analizar si una máquina podía participar en una conversación de modo que un evaluador no pudiera distinguirla de una persona bajo determinadas condiciones.", style_body))
    story.append(Paragraph("En la idea básica de la prueba, un evaluador se comunica mediante texto con una persona y una máquina sin saber cuál es cuál. La cuestión central es si las respuestas de la máquina pueden resultar indistinguibles de las humanas en esa situación.", style_body))
    story.append(Paragraph("<b>Importante:</b> Superar una prueba de conversación no demuestra por sí mismo que una máquina tenga conciencia, emociones, experiencias subjetivas o inteligencia general.", style_body))

    # ---------------- SECCIÓN 8 Y 9 ----------------
    story.append(Paragraph("8. IA, datos y patrones", style_h2))
    story.append(Paragraph("Una gran parte de la IA moderna depende de los datos. Estos pueden ser números, textos, imágenes, sonidos, videos, registros de actividad o mediciones.", style_body))
    
    # Tabla de viviendas corregida
    data_viv = [
        [Paragraph("Superficie", style_table_header), Paragraph("Habitaciones", style_table_header), Paragraph("Distancia al centro", style_table_header), Paragraph("Precio", style_table_header)],
        [Paragraph("50 m²", style_table_cell), Paragraph("2", style_table_cell), Paragraph("5 km", style_table_cell), Paragraph("$100.000", style_table_cell)],
        [Paragraph("70 m²", style_table_cell), Paragraph("3", style_table_cell), Paragraph("4 km", style_table_cell), Paragraph("$140.000", style_table_cell)],
        [Paragraph("90 m²", style_table_cell), Paragraph("3", style_table_cell), Paragraph("2 km", style_table_cell), Paragraph("$190.000", style_table_cell)],
        [Paragraph("120 m²", style_table_cell), Paragraph("4", style_table_cell), Paragraph("1 km", style_table_cell), Paragraph("$250.000", style_table_cell)]
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
    story.append(Spacer(1, 6))
    story.append(Paragraph("En este ejemplo, un algoritmo podría analizar las características de viviendas y sus precios para encontrar relaciones y realizar una predicción sobre una vivienda nueva. Este concepto será desarrollado en el módulo de Machine Learning.", style_body))

    story.append(Paragraph("9. ¿Por qué los datos son importantes?", style_h2))
    story.append(Paragraph("La calidad de los datos puede afectar los resultados de un sistema de IA. Datos con errores, información incompleta, poca variedad o representaciones desequilibradas pueden contribuir a resultados problemáticos.", style_body))
    story.append(Paragraph("<b>Preguntas que debemos hacernos:</b>", style_body))
    preguntas_datos = [
        "¿De dónde provienen los datos?", "¿Son suficientes?", "¿Son representativos?",
        "¿Tienen errores?", "¿Qué información contienen?", "¿Cómo fueron obtenidos?"
    ]
    for p in preguntas_datos:
        story.append(Paragraph(f"• {p}", style_bullet))

    # ---------------- SECCIÓN 10 Y 11 ----------------
    story.append(Paragraph("10. Capacidades y limitaciones", style_h2))
    story.append(Paragraph("<b>Capacidades:</b> Analizar información, encontrar patrones, clasificar, generar contenido, automatizar tareas, realizar predicciones, procesar lenguaje y analizar imágenes.", style_body))
    story.append(Paragraph("<b>Limitaciones:</b> Cometer errores, producir información falsa, depender de los datos, presentar sesgos, interpretar incorrectamente instrucciones y generar respuestas convincentes pero incorrectas.", style_body))
    story.append(Paragraph("<i>Una competencia fundamental en el uso de IA es evaluar críticamente sus resultados.</i>", style_body))

    story.append(Paragraph("11. Para recordar", style_h2))
    data_rec = [
        [Paragraph("Concepto", style_table_header), Paragraph("Definición breve", style_table_header)],
        [Paragraph("Inteligencia Artificial", style_table_cell_bold), Paragraph("Campo de la informática que desarrolla sistemas capaces de realizar determinadas tareas asociadas con capacidades inteligentes.", style_table_cell)],
        [Paragraph("Machine Learning", style_table_cell_bold), Paragraph("Métodos que permiten aprender patrones a partir de datos y utilizarlos para realizar predicciones o acciones.", style_table_cell)],
        [Paragraph("IA Generativa", style_table_cell_bold), Paragraph("IA capaz de generar contenido nuevo a partir de una entrada o instrucción.", style_table_cell)],
        [Paragraph("Automatización", style_table_cell_bold), Paragraph("Ejecución automática de tareas mediante reglas o procedimientos definidos.", style_table_cell)],
        [Paragraph("Prueba de Turing", style_table_cell_bold), Paragraph("Propuesta asociada a Alan Turing para analizar si el comportamiento conversacional de una máquina puede resultar indistinguible del de una persona.", style_table_cell)],
        [Paragraph("Datos", style_table_cell_bold), Paragraph("Información utilizada por los sistemas para analizar, entrenar modelos, encontrar patrones o realizar predicciones.", style_table_cell)]
    ]
    tbl_rec = Table(data_rec, colWidths=[150, 354])
    tbl_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_rec)

    # ---------------- SECCIÓN 12, 13, 14 (ACTIVIDADES) ----------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("12. Actividades", style_h2))
    
    act_ref = [
        Paragraph("<b>Actividad de reflexión</b>", style_body),
        Paragraph("• Una aplicación de mapas calcula automáticamente la ruta más rápida. ¿Necesariamente utiliza Inteligencia Artificial? Explica.", style_bullet),
        Paragraph("• Una plataforma recomienda una película según el historial de visualización. ¿Qué datos podría utilizar?", style_bullet),
        Paragraph("• Una IA genera una respuesta sobre un tema histórico. ¿Qué debería hacer el estudiante antes de utilizarla en un trabajo?", style_bullet),
        Paragraph("• Una persona afirma: «Si una IA conversa como una persona, necesariamente piensa como una persona». Fundamenta tu posición.", style_bullet),
    ]
    t_act_ref = Table([[act_ref]], colWidths=[504])
    t_act_ref.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_act_ref)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Actividad práctica: Detectar IA en nuestra vida cotidiana</b>", style_body))
    story.append(Paragraph("Identifica cinco situaciones en las que interactúes con una aplicación o sistema que pueda utilizar Inteligencia Artificial (celular, redes sociales, buscadores, transporte, etc.).", style_body))
    
    data_pract = [
        [Paragraph("Aplicación o servicio", style_table_header), Paragraph("¿Dónde aparece la IA?", style_table_header), Paragraph("¿Qué tarea realiza?", style_table_header), Paragraph("¿Qué datos podría utilizar?", style_table_header)],
        [Paragraph("Ejemplo: Plataforma de música", style_table_cell), Paragraph("Recomendaciones", style_table_cell), Paragraph("Sugiere canciones", style_table_cell), Paragraph("Historial de reproducción", style_table_cell)],
        [Paragraph("1.", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell)],
        [Paragraph("2.", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell)],
        [Paragraph("3.", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell)],
        [Paragraph("4.", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell)],
        [Paragraph("5.", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell), Paragraph("", style_table_cell)],
    ]
    tbl_pract = Table(data_pract, colWidths=[120, 120, 134, 130])
    tbl_pract.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_pract)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Pregunta final:</b> ¿Cuál de los ejemplos encontrados te sorprendió más y por qué?", style_body))

    # AUTOEVALUACIÓN
    story.append(Paragraph("13. Autoevaluación", style_h2))
    
    auto_q = [
        "<b>1. ¿Cuál describe mejor la IA?</b><br/>A) Cualquier programa automático.<br/><b>B) Un campo de la informática que desarrolla sistemas capaces de realizar determinadas tareas asociadas con capacidades inteligentes.</b><br/>C) Una máquina con conciencia.<br/>D) Un robot humanoide.",
        "<b>2. ¿Qué diferencia a Machine Learning de una automatización tradicional?</b><br/>A) Siempre utiliza robots.<br/><b>B) Puede aprender patrones a partir de datos.</b><br/>C) No necesita datos.<br/>D) Son exactamente lo mismo.",
        "<b>3. ¿Con quién se relaciona la prueba de Turing?</b><br/>A) Isaac Newton.<br/>B) Charles Babbage.<br/><b>C) Alan Turing.</b><br/>D) Steve Jobs.",
        "<b>4. ¿Cuál es correcta?</b><br/>A) Una IA siempre es correcta.<br/>B) Los datos no influyen.<br/><b>C) Una IA puede producir resultados incorrectos y deben evaluarse.</b><br/>D) Toda IA tiene conciencia.",
        "<b>5. Una plataforma recomienda películas según el historial del usuario. ¿Qué concepto se relaciona directamente?</b><br/><b>A) Sistemas de recomendación.</b><br/>B) Compresión de archivos.<br/>C) Texto manual.<br/>D) Sistema operativo.",
        "<b>6. Verdadero o Falso:</b><br/>a) Toda automatización es IA. <i>(Falso)</i><br/>b) La calidad de los datos puede afectar los resultados. <i>(Verdadero)</i><br/>c) La prueba de Turing demuestra conciencia. <i>(Falso)</i><br/>d) La IA puede analizar imágenes. <i>(Verdadero)</i><br/>e) Una respuesta generada por IA debe aceptarse siempre sin verificarla. <i>(Falso)</i>"
    ]
    
    for q in auto_q:
        story.append(Paragraph(q, style_body))
        story.append(Spacer(1, 3))

    # ACTIVIDAD DE CIERRE
    story.append(Paragraph("14. Actividad de cierre", style_h2))
    cierre_box = [
        Paragraph("<b>¿Qué es la Inteligencia Artificial y por qué es importante aprender sobre ella actualmente?</b>", style_body),
        Paragraph("La respuesta debería incluir:<br/>• Una definición de IA con tus propias palabras.<br/>• Un ejemplo de aplicación cotidiana.<br/>• Una capacidad de los sistemas de IA.<br/>• Una limitación.<br/>• Una reflexión sobre el uso responsable de la IA.<br/><br/><i>Extensión sugerida: 150 a 250 palabras.</i>", style_body)
    ]
    t_cierre = Table([[cierre_box]], colWidths=[504])
    t_cierre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cierre)

    # GLOSARIO Y RECURSOS
    story.append(Paragraph("Glosario del módulo", style_h2))
    glosario_data = [
        [Paragraph("Término", style_table_header), Paragraph("Definición", style_table_header)],
        [Paragraph("Algoritmo", style_table_cell_bold), Paragraph("Conjunto de pasos o instrucciones utilizados para resolver un problema o realizar una tarea.", style_table_cell)],
        [Paragraph("Datos", style_table_cell_bold), Paragraph("Información que puede ser analizada o utilizada por un sistema.", style_table_cell)],
        [Paragraph("Patrón", style_table_cell_bold), Paragraph("Regularidad o relación que puede identificarse en un conjunto de datos.", style_table_cell)],
        [Paragraph("Modelo", style_table_cell_bold), Paragraph("Representación aprendida o construida para realizar una tarea, como una predicción.", style_table_cell)],
        [Paragraph("Predicción", style_table_cell_bold), Paragraph("Resultado estimado por un sistema a partir de información disponible.", style_table_cell)],
        [Paragraph("Prompt", style_table_cell_bold), Paragraph("Instrucción o entrada proporcionada a un sistema generativo para orientar su respuesta.", style_table_cell)],
        [Paragraph("Sesgo", style_table_cell_bold), Paragraph("Tendencia sistemática que puede afectar los datos, el modelo o sus resultados.", style_table_cell)],
        [Paragraph("Verificación", style_table_cell_bold), Paragraph("Proceso de comprobar si una información o resultado es correcto y confiable.", style_table_cell)],
    ]
    tbl_glos = Table(glosario_data, colWidths=[120, 384])
    tbl_glos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_glos)

    story.append(Paragraph("Recursos para profundizar", style_h2))
    story.append(Paragraph("• Alan Turing, «Computing Machinery and Intelligence» (1950).", style_bullet))
    story.append(Paragraph("• Materiales introductorios sobre Inteligencia Artificial y Machine Learning.", style_bullet))
    story.append(Paragraph("• Documentación y recursos de Google Colab, que se utilizarán en materiales posteriores del módulo.", style_bullet))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documento generado con éxito: {filename}")

if __name__ == "__main__":
    create_ai_pdf()