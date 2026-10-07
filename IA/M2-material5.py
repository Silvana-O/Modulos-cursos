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
        self.doc_subtitle = kwargs.pop('doc_subtitle', "EVALUACIÓN DE MODELOS DE ML")
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
        self.drawString(54, 36, "Material educativo  •  Módulo 2 - Material 4: Evaluación de modelos de Machine Learning")
        
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
    
    style_formula = ParagraphStyle(
        'FormulaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=10,
        leading=14,
        alignment=1, # Centrado
        textColor=COLOR_PRIMARY,
        spaceBefore=4,
        spaceAfter=4
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )
    
    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=COLOR_TEXT,
        alignment=1
    )
    
    style_table_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=style_table_cell,
        alignment=0
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
        'formula': style_formula,
        'th': style_table_header,
        'td': style_table_cell,
        'td_left': style_table_cell_left,
        'td_bold': style_table_cell_bold
    }


# ----------------------------------------------------------------------
# DOCUMENTO 1: MATERIAL TEÓRICO
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Modulo2_Material4_Teoria.pdf"):
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
    story.append(Paragraph("MÓDULO 2 · MATERIAL 4", st['tag']))
    story.append(Paragraph("Evaluación de Modelos de Machine Learning", st['title']))
    story.append(Paragraph("Material Teórico • Matriz de Confusión, Métricas de Clasificación y Regresión", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Descripción y Objetivos ---
    desc_text = "<b>Descripción:</b> Entrenar un modelo no significa automáticamente que sus resultados sean correctos o útiles. Un modelo puede realizar predicciones acertadas y cometer errores importantes. En este material aprenderemos a analizar modelos de clasificación mediante la matriz de confusión, precisión y recall, así como métricas para modelos de regresión (MAE y MSE)."
    
    obj_content = [
        Paragraph(desc_text, st['body']),
        Spacer(1, 4),
        Paragraph("<b>Objetivos de aprendizaje:</b>", st['body']),
        Paragraph("• Entender por qué es indispensable evaluar un modelo de Machine Learning.", st['bullet']),
        Paragraph("• Comprender y construir la Matriz de Confusión (TP, TN, FP, FN).", st['bullet']),
        Paragraph("• Calcular e interpretar la Precisión (Precision) y el Recall (Exhaustividad).", st['bullet']),
        Paragraph("• Evaluar modelos de regresión utilizando MAE y MSE.", st['bullet']),
        Paragraph("• Interpretar métricas en el contexto específico del negocio o problema.", st['bullet']),
    ]
    
    obj_table = Table([[obj_content]], colWidths=[504])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 10))

    # --- 1. ¿Por qué evaluar un modelo? ---
    story.append(Paragraph("1. ¿Por qué evaluar un modelo?", st['h2']))
    story.append(Paragraph("Imaginemos un modelo que detecta si un correo es spam o no spam. Para saber si sus predicciones son buenas, comparamos la predicción con el resultado real:", st['body']))
    
    data_eval_ej = [
        [Paragraph("Resultado Real", st['th']), Paragraph("Predicción", st['th']), Paragraph("¿Acertó?", st['th'])],
        [Paragraph("Spam", st['td']), Paragraph("Spam", st['td']), Paragraph("Sí", st['td'])],
        [Paragraph("Spam", st['td']), Paragraph("No spam", st['td']), Paragraph("No", st['td'])],
        [Paragraph("No spam", st['td']), Paragraph("Spam", st['td']), Paragraph("No", st['td'])],
        [Paragraph("No spam", st['td']), Paragraph("No spam", st['td']), Paragraph("Sí", st['td'])],
    ]
    tbl_eval = Table(data_eval_ej, colWidths=[168, 168, 168])
    tbl_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_eval)
    story.append(Spacer(1, 6))

    idea_box = [Paragraph("<b>Idea fundamental:</b> Un modelo no es bueno simplemente porque produce predicciones. Debemos comprobar qué tan acertadas son, qué errores comete y con qué frecuencia se equivoca.", st['body'])]
    tbl_idea = Table([[idea_box]], colWidths=[504])
    tbl_idea.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('LINELEFT', (0,0), (-1,-1), 3, COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_idea)

    # --- 2 & 3. Matriz de confusión ---
    story.append(Paragraph("2. Predicciones correctas e incorrectas: Matriz de Confusión", st['h2']))
    story.append(Paragraph("En clasificación binaria definimos dos clases: <b>Positivo</b> (ej. Es Spam) y <b>Negativo</b> (ej. No es Spam). La combinación entre la realidad y la predicción genera cuatro situaciones:", st['body']))

    data_cm_def = [
        [Paragraph("", st['th']), Paragraph("Predicción Positiva", st['th']), Paragraph("Predicción Negativa", st['th'])],
        [Paragraph("Real Positivo", st['th']), Paragraph("<b>TP</b> (Verdadero Positivo)<br/>Acertó", st['td']), Paragraph("<b>FN</b> (Falso Negativo)<br/>Se le escapó un positivo", st['td'])],
        [Paragraph("Real Negativo", st['th']), Paragraph("<b>FP</b> (Falso Positivo)<br/>Detectó algo que no era", st['td']), Paragraph("<b>TN</b> (Verdadero Negativo)<br/>Acertó", st['td'])],
    ]
    tbl_cm = Table(data_cm_def, colWidths=[130, 187, 187])
    tbl_cm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), COLOR_PRIMARY),
        ('BACKGROUND', (1,0), (-1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (1,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_cm)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Definiciones clave:</b>", st['body']))
    story.append(Paragraph("• <b>TP (Verdadero Positivo):</b> Realmente es positivo y el modelo predice positivo.", st['bullet']))
    story.append(Paragraph("• <b>TN (Verdadero Negativo):</b> Realmente es negativo y el modelo predice negativo.", st['bullet']))
    story.append(Paragraph("• <b>FP (Falso Positivo):</b> Realmente es negativo, pero el modelo predice positivo (Error Tipo I).", st['bullet']))
    story.append(Paragraph("• <b>FN (Falso Negativo):</b> Realmente es positivo, pero el modelo predice negativo (Error Tipo II).", st['bullet']))

    # --- Ejemplo Completo ---
    story.append(Paragraph("3. Ejemplo numérico de Matriz de Confusión", st['h2']))
    story.append(Paragraph("Supongamos que un modelo analiza 10 correos electrónicos (5 realmente spam, 5 realmente no spam):", st['body']))
    
    data_cm_num = [
        [Paragraph("", st['th']), Paragraph("Predicción: Spam", st['th']), Paragraph("Predicción: No spam", st['th'])],
        [Paragraph("Real: Spam", st['th']), Paragraph("TP = 3", st['td_bold']), Paragraph("FN = 2", st['td'])],
        [Paragraph("Real: No spam", st['th']), Paragraph("FP = 3", st['td']), Paragraph("TN = 2", st['td_bold'])],
    ]
    tbl_cm_num = Table(data_cm_num, colWidths=[130, 187, 187])
    tbl_cm_num.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), COLOR_PRIMARY),
        ('BACKGROUND', (1,0), (-1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_cm_num)

    # --- 4 & 5. Precisión y Recall ---
    story.append(Paragraph("4. Métricas de Clasificación: Precisión y Recall", st['h2']))
    story.append(Paragraph("A partir de la matriz de confusión calculamos dos métricas fundamentales:", st['body']))

    # Precisión Box
    prec_box = [
        Paragraph("<b>Precisión (Precision):</b> ¿De todos los casos que el modelo predijo como positivos, cuántos eran realmente positivos?", st['body']),
        Paragraph("Fórmula:  <b>Precisión = TP / (TP + FP)</b>", st['formula']),
        Paragraph("En el ejemplo: Precisión = 3 / (3 + 3) = 3 / 6 = <b>50%</b>", st['body'])
    ]
    tbl_prec = Table([[prec_box]], colWidths=[504])
    tbl_prec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_prec)
    story.append(Spacer(1, 6))

    # Recall Box
    rec_box = [
        Paragraph("<b>Recall (Exhaustividad / Sensibilidad):</b> ¿De todos los casos que realmente eran positivos, cuántos logró detectar?", st['body']),
        Paragraph("Fórmula:  <b>Recall = TP / (TP + FN)</b>", st['formula']),
        Paragraph("En el ejemplo: Recall = 3 / (3 + 2) = 3 / 5 = <b>60%</b>", st['body'])
    ]
    tbl_rec = Table([[rec_box]], colWidths=[504])
    tbl_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_rec)
    story.append(Spacer(1, 8))

    # Tabla Comparativa Precisión vs Recall
    data_m_comp = [
        [Paragraph("Métrica", st['th']), Paragraph("Pregunta Principal", st['th']), Paragraph("Error Relacionado", st['th'])],
        [Paragraph("Precisión", st['td_bold']), Paragraph("¿Cuántos positivos predichos eran realmente positivos?", st['td_left']), Paragraph("Falsos Positivos (FP)", st['td'])],
        [Paragraph("Recall", st['td_bold']), Paragraph("¿Cuántos positivos reales conseguimos detectar?", st['td_left']), Paragraph("Falsos Negativos (FN)", st['td'])],
    ]
    tbl_m_comp = Table(data_m_comp, colWidths=[100, 254, 150])
    tbl_m_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_m_comp)

    # --- 6. Umbral de Clasificación ---
    story.append(Paragraph("5. Umbral de Clasificación", st['h2']))
    story.append(Paragraph("Los modelos de clasificación generan puntuaciones o probabilidades (ej. 0,82). Por defecto se utiliza un <b>umbral de 0,50</b>. Si aumentamos el umbral (ej. a 0,70), el modelo se vuelve más 'exigente': disminuyen los falsos positivos (aumenta la precisión) pero aumentan los falsos negativos (disminuye el recall).", st['body']))

    # --- 7. Métricas de Regresión ---
    story.append(Paragraph("6. Evaluación de Modelos de Regresión (MAE y MSE)", st['h2']))
    story.append(Paragraph("En regresión predecimos valores continuos (ej. precio de una casa). Evaluamos la diferencia entre el valor real (y) y la predicción (ŷ):", st['body']))

    # MAE Box
    mae_box = [
        Paragraph("<b>MAE (Error Absoluto Medio):</b> Promedio de los errores absolutos. Trata todos los errores proporcionalmente.", st['body']),
        Paragraph("Fórmula:  <b>MAE = (1 / n) * Σ | y_i - ŷ_i |</b>", st['formula']),
        Paragraph("<i>Ejemplo con errores [2, 4, 3, 1]:</i> MAE = (2 + 4 + 3 + 1) / 4 = <b>2.5</b>", st['body'])
    ]
    tbl_mae = Table([[mae_box]], colWidths=[504])
    tbl_mae.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_mae)
    story.append(Spacer(1, 6))

    # MSE Box
    mse_box = [
        Paragraph("<b>MSE (Error Cuadrático Medio):</b> Promedio de los errores al cuadrado. Penaliza fuertemente los errores grandes.", st['body']),
        Paragraph("Fórmula:  <b>MSE = (1 / n) * Σ (y_i - ŷ_i)²</b>", st['formula']),
        Paragraph("<i>Ejemplo con errores [2, 4, 3, 1]:</i> MSE = (2² + 4² + 3² + 1²) / 4 = (4 + 16 + 9 + 1) / 4 = <b>7.5</b>", st['body'])
    ]
    tbl_mse = Table([[mse_box]], colWidths=[504])
    tbl_mse.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tbl_mse)

    # --- Glosario ---
    story.append(Paragraph("Glosario de conceptos", st['h2']))
    glosario_data = [
        [Paragraph("Concepto", st['th']), Paragraph("Definición", st['th'])],
        [Paragraph("Matriz de Confusión", st['td_bold']), Paragraph("Tabla de doble entrada que organiza los aciertos y errores de clasificación.", st['td_left'])],
        [Paragraph("Precisión (Precision)", st['td_bold']), Paragraph("Proporción de predicciones positivas que resultaron ser realmente positivas.", st['td_left'])],
        [Paragraph("Recall / Exhaustividad", st['td_bold']), Paragraph("Proporción de casos positivos reales que el modelo logró identificar.", st['td_left'])],
        [Paragraph("MAE", st['td_bold']), Paragraph("Error Absoluto Medio. Promedio de las diferencias en valor absoluto.", st['td_left'])],
        [Paragraph("MSE", st['td_bold']), Paragraph("Error Cuadrático Medio. Promedio de los errores elevados al cuadrado.", st['td_left'])],
        [Paragraph("Umbral (Threshold)", st['td_bold']), Paragraph("Corte numérico de probabilidad a partir del cual se decide la clase positiva.", st['td_left'])],
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
        return NumberedCanvas(*args, doc_subtitle="EVALUACIÓN DE MODELOS - TEORÍA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento teórico generado: {filename}")


# ----------------------------------------------------------------------
# DOCUMENTO 2: ACTIVIDADES Y EVALUACIONES
# ----------------------------------------------------------------------
def create_activities_pdf(filename="Modulo2_Material4_Actividades.pdf"):
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
    story.append(Paragraph("MÓDULO 2 · MATERIAL 4", st['tag']))
    story.append(Paragraph("Evaluación de Modelos de Machine Learning", st['title']))
    story.append(Paragraph("Guía de Actividades, Ejercicios Prácticos y Autoevaluación", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Actividad 1: Reflexión Detección Fraudulenta ---
    story.append(Paragraph("1. Actividad de reflexión: Detección de mensajes fraudulentos", st['h2']))
    story.append(Paragraph("Un sistema analiza 100 mensajes sospechosos y arroja los siguientes resultados: <b>TP = 30</b>, <b>TN = 50</b>, <b>FP = 10</b>, <b>FN = 10</b>.", st['body']))
    
    act1_questions = [
        Paragraph("<b>Responde a las siguientes cuestiones:</b>", st['body']),
        Paragraph("1. ¿Cuántos mensajes fueron clasificados correctamente?", st['bullet']),
        Paragraph("2. ¿Cuántos fueron clasificados incorrectamente?", st['bullet']),
        Paragraph("3. ¿Cuántos mensajes eran realmente positivos y cuántos fueron predichos como positivos?", st['bullet']),
        Paragraph("4. ¿Qué representan concretamente los 10 falsos positivos y los 10 falsos negativos?", st['bullet']),
        Paragraph("5. Calcula la <b>Precisión</b> y el <b>Recall</b> de este modelo.", st['bullet']),
    ]
    t_act1 = Table([[act1_questions]], colWidths=[504])
    t_act1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_act1)
    story.append(Spacer(1, 10))

    # --- Actividad 2: Ejercicio de Clasificación ---
    story.append(Paragraph("2. Ejercicio práctico: Cálculo de Matriz de Confusión", st['h2']))
    story.append(Paragraph("Dada la siguiente matriz de confusión obtenida por un modelo:", st['body']))
    
    data_ex_cm = [
        [Paragraph("", st['th']), Paragraph("Predicción Positiva", st['th']), Paragraph("Predicción Negativa", st['th'])],
        [Paragraph("Real Positivo", st['th']), Paragraph("8", st['td_bold']), Paragraph("2", st['td'])],
        [Paragraph("Real Negativo", st['th']), Paragraph("1", st['td']), Paragraph("9", st['td_bold'])],
    ]
    tbl_ex_cm = Table(data_ex_cm, colWidths=[130, 187, 187])
    tbl_ex_cm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), COLOR_PRIMARY),
        ('BACKGROUND', (1,0), (-1,0), COLOR_ACCENT),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_ex_cm)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Consignas:</b>", st['body']))
    story.append(Paragraph("a) Identifica los valores de TP, TN, FP y FN.", st['bullet']))
    story.append(Paragraph("b) Calcula la Precisión: <i>TP / (TP + FP)</i>.", st['bullet']))
    story.append(Paragraph("c) Calcula el Recall: <i>TP / (TP + FN)</i>.", st['bullet']))
    story.append(Paragraph("d) Explica qué significan ambos resultados en el contexto del problema.", st['bullet']))
    story.append(Spacer(1, 10))

    # --- Actividad 3: Ejercicio de Regresión ---
    story.append(Paragraph("3. Ejercicio práctico: Evaluación de Regresión (MAE)", st['h2']))
    story.append(Paragraph("Un modelo intenta predecir las ventas diarias de una tienda. Los errores absolutos de cinco predicciones fueron:", st['body']))
    
    data_reg_err = [
        [Paragraph("Predicción", st['th']), Paragraph("P1", st['th']), Paragraph("P2", st['th']), Paragraph("P3", st['th']), Paragraph("P4", st['th']), Paragraph("P5", st['th'])],
        [Paragraph("Error Absoluto", st['td_bold']), Paragraph("2", st['td']), Paragraph("3", st['td']), Paragraph("5", st['td']), Paragraph("4", st['td']), Paragraph("1", st['td'])],
    ]
    tbl_reg = Table(data_reg_err, colWidths=[104, 80, 80, 80, 80, 80])
    tbl_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tbl_reg)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Consignas:</b>", st['body']))
    story.append(Paragraph("1. Calcula el MAE sustituyendo en la fórmula: <i>MAE = (2 + 3 + 5 + 4 + 1) / 5</i>.", st['bullet']))
    story.append(Paragraph("2. Interpreta el valor obtenido: ¿Qué representa este número?", st['bullet']))
    story.append(Paragraph("3. ¿Qué información adicional necesitarías para determinar si el resultado es aceptable?", st['bullet']))
    story.append(Spacer(1, 10))

    # --- Autoevaluación ---
    story.append(Paragraph("4. Autoevaluación de conocimientos", st['h2']))
    
    auto_q = [
        "<b>1. ¿Para qué sirve evaluar un modelo?</b><br/>A) Para aumentar datos.<br/>B) Para conocer cómo se comporta el modelo y sus errores.<br/>C) Para eliminar variables.<br/>D) Para convertir clasificación en regresión.",
        "<b>2. ¿Qué es un verdadero positivo (TP)?</b><br/>A) Caso negativo clasificado como positivo.<br/>B) Caso positivo clasificado como negativo.<br/>C) Caso positivo clasificado correctamente como positivo.<br/>D) Caso negativo clasificado correctamente.",
        "<b>3. ¿Qué es un falso positivo (FP)?</b><br/>A) Caso positivo correctamente detectado.<br/>B) Caso negativo clasificado como positivo.<br/>C) Caso positivo clasificado como negativo.<br/>D) Caso negativo correctamente detectado.",
        "<b>4. ¿Qué mide principalmente la precisión?</b><br/>A) La proporción de positivos predichos que realmente son positivos.<br/>B) La cantidad total de datos.<br/>C) El error promedio de regresión.<br/>D) La cantidad de variables.",
        "<b>5. ¿Qué mide principalmente el recall?</b><br/>A) La cantidad de falsos positivos.<br/>B) La proporción de positivos reales que el modelo logró detectar.<br/>C) La cantidad de variables categóricas.<br/>D) El tamaño del dataset.",
        "<b>6. ¿Cuál de estas métricas se utiliza para regresión?</b><br/>A) Matriz de confusión.<br/>B) Recall.<br/>C) MAE.<br/>D) Verdadero positivo.",
        "<b>7. ¿Qué característica distingue al MSE respecto al MAE?</b><br/>A) Ignora los errores grandes.<br/>B) Penaliza especialmente los errores grandes al elevarlos al cuadrado.<br/>C) Solo se aplica en clasificación.<br/>D) No requiere valores reales.",
        "<b>8. ¿Por qué una métrica debe interpretarse en contexto?</b><br/>A) Porque el mismo valor puede tener diferentes impactos según el problema.<br/>B) Porque las métricas son siempre subjetivas.<br/>C) Porque no se pueden comparar modelos.<br/>D) Porque no contienen información."
    ]
    
    for q in auto_q:
        story.append(Paragraph(q, st['body']))
        story.append(Spacer(1, 3))

    # Solucionario
    respuestas_content = [
        Paragraph("<b>Clave de Respuestas (Autoevaluación):</b>", st['body']),
        Spacer(1, 2),
        Paragraph("<b>1:</b> B  |  <b>2:</b> C  |  <b>3:</b> B  |  <b>4:</b> A  |  <b>5:</b> B  |  <b>6:</b> C  |  <b>7:</b> B  |  <b>8:</b> A", st['body']),
        Spacer(1, 2),
        Paragraph("<b>Soluciones de ejercicios prácticos:</b><br/>• <b>Actividad 1:</b> Aciertos=80 (TP+TN), Errores=20 (FP+FN), Positivos Reales=40, Predichos Positivos=40. Precisión = 30/40 = 75%, Recall = 30/40 = 75%.<br/>• <b>Actividad 2:</b> TP=8, TN=9, FP=1, FN=2. Precisión = 8/9 = 88,89%, Recall = 8/10 = 80%.<br/>• <b>Actividad 3:</b> MAE = 15 / 5 = 3,0 unidades de error promedio.", st['body'])
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

    # --- Plantilla de Planificación ---
    story.append(Paragraph("5. Plantilla de análisis de modelos en proyectos reales", st['h2']))
    story.append(Paragraph("Completa la siguiente plantilla aplicando los criterios de evaluación aprendidos para un proyecto de Machine Learning de tu elección:", st['body']))

    data_plan = [
        [Paragraph("Criterio de Evaluación", st['th']), Paragraph("Análisis del Estudiante", st['th'])],
        [Paragraph("1. Tipo de Problema (Clasificación / Regresión)", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("2. Métricas Seleccionadas (ej. Precisión, Recall, MAE)", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("3. Impacto de un Falso Positivo (FP)", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("4. Impacto de un Falso Negativo (FN)", st['td_bold']), Paragraph("", st['td'])],
        [Paragraph("5. Decisión de Negocio / Tolerancia al Error", st['td_bold']), Paragraph("", st['td'])],
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
        return NumberedCanvas(*args, doc_subtitle="EVALUACIÓN DE MODELOS - ACTIVIDADES", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de actividades generado: {filename}")


if __name__ == "__main__":
    create_theory_pdf()
    create_activities_pdf()