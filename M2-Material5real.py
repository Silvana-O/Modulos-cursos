import os
import pandas as pd
import numpy as np

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
        self.doc_subtitle = kwargs.pop('doc_subtitle', "PREPARACIÓN Y LIMPIEZA DE DATOS")
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
        self.drawString(54, 36, "Material educativo  •  Módulo 2 - Material 5: Preparación y Limpieza de Datos")
        
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
    )
    
    style_doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
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
# GENERACIÓN DE DOCUMENTO PDF
# ----------------------------------------------------------------------
def create_theory_pdf(filename="Modulo2_Material5_Teoria.pdf"):
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

    # --- Header Principal ---
    story.append(Paragraph("MÓDULO 2 · MATERIAL 5", st['tag']))
    story.append(Paragraph("Preparación y Limpieza de Datos en Machine Learning", st['title']))
    story.append(Paragraph("Material Teórico • Fundamentos, Preprocesamiento, Codificación y Escalado", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Descripción y Objetivos ---
    desc_text = "<b>Descripción:</b> Un modelo de Machine Learning aprende directamente de los datos recibidos. Si contienen valores faltantes, duplicados, errores, formatos inconsistentes o escalas dispares, el modelo aprenderá patrones incorrectos. En este material abordamos las técnicas fundamentales para identificar y resolver estos problemas antes del entrenamiento."
    
    obj_content = [
        Paragraph(desc_text, st['body']),
        Spacer(1, 4),
        Paragraph("<b>Objetivos de aprendizaje:</b>", st['body']),
        Paragraph("• Comprender la importancia de la limpieza y preparación de datos (Data Preprocessing).", st['bullet']),
        Paragraph("• Identificar estrategias para tratar datos faltantes, duplicados, valores incorrectos y atípicos.", st['bullet']),
        Paragraph("• Diferenciar entre variables numéricas y categóricas, y aplicar técnicas de codificación (Label / One-Hot Encoding).", st['bullet']),
        Paragraph("• Entender las técnicas de escalado (Normalización Min-Max y Estandarización Z-score).", st['bullet']),
        Paragraph("• Comprender el flujo correcto de división de datos y cómo prevenir la fuga de información (Data Leakage).", st['bullet']),
    ]
    
    obj_table = Table([[obj_content]], colWidths=[504])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 12))

    # --- Sección de Código / Ejemplo en Documento ---
    story.append(Paragraph("Demostración Práctica del Preprocesamiento", st['h2']))
    
    table_data = [
        [Paragraph("Estudiante", st['th']), Paragraph("Edad", st['th']), Paragraph("Modalidad", st['th']), Paragraph("Horas", st['th'])],
        [Paragraph("Ana", st['td']), Paragraph("20", st['td']), Paragraph("Presencial", st['td']), Paragraph("8", st['td'])],
        [Paragraph("Luis", st['td']), Paragraph("22", st['td']), Paragraph("Virtual", st['td']), Paragraph("5", st['td'])],
        [Paragraph("Marta", st['td']), Paragraph("21 (Imputado)", st['td_bold']), Paragraph("Presencial", st['td']), Paragraph("7", st['td'])],
        [Paragraph("Juan", st['td']), Paragraph("21", st['td']), Paragraph("Virtual", st['td']), Paragraph("3", st['td'])],
    ]
    
    demo_table = Table(table_data, colWidths=[126, 126, 126, 126])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(demo_table)

    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="PREPARACIÓN Y LIMPIEZA DE DATOS", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento PDF generado exitosamente: {filename}")


# ----------------------------------------------------------------------
# EJECUCIÓN PRÁCTICA EN PYTHON
# ----------------------------------------------------------------------
def demostracion_limpieza():
    print("==================================================")
    print("1. DEMOSTRACIÓN: DETECCIÓN Y TRATAMIENTO DE ERRORES")
    print("==================================================\n")

    raw_data = {
        "Estudiante": ["Ana", "Luis", "Marta", "Juan", "Juan", "Pedro"],
        "Edad": [20, 22, np.nan, 21, 21, 250],
        "Modalidad": ["Presencial", "Virtual", "Presencial", "Virtual", "Virtual", "Presencial"],
        "Horas": [8, 5, 7, 3, 3, 4],
        "Asistencia": [90, 75, 95, 60, 60, 55],
        "Resultado": ["Aprobado", "Aprobado", "Aprobado", "Desaprobado", "Desaprobado", "Desaprobado"]
    }

    df = pd.DataFrame(raw_data)
    print("--- Tabla Original ---")
    print(df)
    print("\nResumen de nulos e información:")
    print(df.isna().sum())

    # Paso 1: Eliminar Duplicados
    df_clean = df.drop_duplicates().copy()
    print("\n--- Tras eliminar duplicados ---")
    print(df_clean)

    # Paso 2: Tratar Valores Incorrectos (Outliers implausibles)
    df_clean.loc[df_clean["Edad"] > 100, "Edad"] = np.nan
    print("\n--- Tras reemplazar edades > 100 por NaN ---")
    print(df_clean[["Estudiante", "Edad"]])

    # Paso 3: Imputación de Faltantes (Mediana)
    mediana_edad = df_clean["Edad"].median()
    df_clean["Edad"] = df_clean["Edad"].fillna(mediana_edad)
    print(f"\n--- Tras imputar Edad faltante con la Mediana ({mediana_edad}) ---")
    print(df_clean)


def actividad_identificacion_31():
    print("\n==================================================")
    print("2. ACTIVIDAD DE IDENTIFICACIÓN (SECCIÓN 31)")
    print("==================================================\n")

    data_31 = {
        "Nombre": ["Ana", "Luis", "Marta", "Juan", "Juan", "Pedro"],
        "Edad": [20, 22, np.nan, 21, 21, 250],
        "Departamento": ["Salto", "Artigas", "Salto", "Artigas", "Artigas", "Salto"],
        "Horas de estudio": [8, 5, 7, 3, 3, 4]
    }
    df = pd.DataFrame(data_31)
    
    print("Tabla dada:")
    print(df)
    print("\n--- Respuestas ---")
    print("1. Dato faltante: 'Marta' no tiene valor en 'Edad' (NaN).")
    print("2. Registro duplicado: 'Juan' (Edad 21, Depto Artigas, Horas 3) aparece dos veces.")
    print("3. Posible valor incorrecto: 'Pedro' con Edad 250 (valor fuera de rango biológico).")
    print("4. Variable categórica: 'Departamento' (valores: Salto, Artigas).")
    print("5. Variables numéricas: 'Edad' y 'Horas de estudio'.")


if __name__ == "__main__":
    # 1. Genera el PDF corregido
    create_theory_pdf()
    
    # 2. Ejecuta los análisis de datos
    demostracion_limpieza()
    actividad_identificacion_31()