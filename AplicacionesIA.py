import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# CANVAS PERSONALIZADO (Encabezados y Pies de página con número total de páginas)
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.doc_subtitle = kwargs.pop('doc_subtitle', "HERRAMIENTAS DE INTELIGENCIA ARTIFICIAL")
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
        self.drawString(54, 36, "Material educativo  •  Directorio de Herramientas de IA")
        
        self.restoreState()


# ----------------------------------------------------------------------
# ESTILOS DEL DOCUMENTO
# ----------------------------------------------------------------------
def get_common_styles():
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#0f172a")
    COLOR_ACCENT = colors.HexColor("#0d9488")
    COLOR_TEXT = colors.HexColor("#334155")
    COLOR_LINK = colors.HexColor("#0284c7")

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
    
    # keepWithNext=True evita títulos huérfanos al final de la página
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

    style_link = ParagraphStyle(
        'TableCellLink',
        parent=style_table_cell,
        fontName='Helvetica-Bold',
        textColor=COLOR_LINK
    )

    return {
        'tag': style_module_tag,
        'title': style_doc_title,
        'subtitle': style_doc_subtitle,
        'h2': style_h2,
        'body': style_body,
        'th': style_table_header,
        'td': style_table_cell,
        'td_bold': style_table_cell_bold,
        'link': style_link
    }


# ----------------------------------------------------------------------
# GENERACIÓN DEL PDF DE APLICACIONES DE IA
# ----------------------------------------------------------------------
def create_ai_tools_pdf(filename="Guia_Aplicaciones_IA.pdf"):
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

    # --- Encabezado principal ---
    story.append(Paragraph("RECURSOS Y HERRAMIENTAS", st['tag']))
    story.append(Paragraph("Directorio de Aplicaciones de IA", st['title']))
    story.append(Paragraph("Guía de referencia rápida con enlaces, descripciones y funciones", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=12))

    # --- Datos de las herramientas organizadas por categoría ---
    categorias = [
        {
            "nombre": "1. Generación de Texto y Asistentes Conversacionales",
            "herramientas": [
                ("ChatGPT", "https://chatgpt.com", "Modelos LLM de OpenAI para conversación, redacción, análisis de documentos, solución de problemas complejos y generación de ideas.", "Redacción creativa/técnica, análisis de archivos, traducción, razonamiento avanzado."),
                ("Claude", "https://claude.ai", "Asistente de IA desarrollado por Anthropic, destacado por su tono natural, alta precisión, seguridad y amplio contexto de lectura.", "Resumen de documentos extensos, programación, análisis de datos, redacción académica."),
                ("Google Gemini", "https://gemini.google.com", "IA multimodal de Google integrada con el ecosistema de Google Workspace (Drive, Docs, Gmail, YouTube).", "Búsqueda en tiempo real, integración con herramientas Google, análisis multimodal (texto, imagen, código)."),
                ("Microsoft Copilot", "https://copilot.microsoft.com", "Asistente basado en tecnología de OpenAI con acceso a la web en tiempo real mediante Bing e integración con Microsoft 365.", "Búsquedas web con fuentes, redacción de correo, generación de imágenes con DALL-E 3.")
            ]
        },
        {
            "nombre": "2. Generación y Edición de Imágenes",
            "herramientas": [
                ("Midjourney", "https://www.midjourney.com", "Herramienta líder en calidad artística para generación de imágenes hiperrealistas e ilustraciones mediante prompts.", "Arte digital, fotorrealismo, diseño de conceptos, empaquetado e ilustración."),
                ("DALL-E 3", "https://chatgpt.com", "Modelo de generación de imágenes de OpenAI integrado directamente en ChatGPT, enfocado en comprender instrucciones detalladas.", "Ilustraciones vectoriales, diseño publicitario, interpretación precisa de texto a imagen."),
                ("Adobe Firefly", "https://firefly.adobe.com", "Familia de modelos creativos de IA diseñados para ser seguros comercialmente e integrados en la suite Adobe.", "Relleno generativo, vectorización, efectos de texto, edición profesional de fotos."),
                ("Canva Magic Studio", "https://www.canva.com", "Suite de herramientas con IA integrada en la plataforma de diseño Canva.", "Edición rápida de diseño, eliminación de fondos, redacción y extensión de imágenes.")
            ]
        },
        {
            "nombre": "3. Generación de Audio, Voz y Música",
            "herramientas": [
                ("ElevenLabs", "https://elevenlabs.io", "Plataforma avanzada de síntesis de voz mediante IA para la creación de locuciones naturales e hiperrealistas.", "Clonación de voz, texto a voz (TTS) multilingüe, doblaje automático de videos."),
                ("Suno AI", "https://suno.com", "Generador de canciones completas (música, letra y voces) en múltiples géneros musicales a partir de texto.", "Composición musical completa, creación de jingles, bandas sonoras de apoyo.")
            ]
        },
        {
            "nombre": "4. Programación y Desarrollo de Software",
            "herramientas": [
                ("GitHub Copilot", "https://github.com/features/copilot", "Asistente de código en tiempo real integrado directamente en editores como VS Code y JetBrains.", "Autocompletado de código, generación de pruebas unitarias, explicación de errores."),
                ("Cursor", "https://www.cursor.com", "Editor de código diseñado nativamente para trabajar con IA y analizar repositorios completos.", "Refactorización de código, edición basada en chat, navegación inteligente de proyectos.")
            ]
        },
        {
            "nombre": "5. Productividad, Investigación y Notas",
            "herramientas": [
                ("Perplexity AI", "https://www.perplexity.ai", "Motor de búsqueda conversacional que responde preguntas complejas citando fuentes en tiempo real.", "Investigación académica y de mercado, verificación de datos con referencias directas."),
                ("NotebookLM", "https://notebooklm.google.com", "Cuaderno virtual de Google enfocado en interactuar exclusivamente con los documentos que el usuario sube.", "Generación de resúmenes de lectura, guías de estudio, podcasts sintéticos de los textos.")
            ]
        }
    ]

    # --- Construcción de las tablas por categoría ---
    for cat in categorias:
        story.append(Paragraph(cat["nombre"], st['h2']))
        
        table_data = [
            [
                Paragraph("Aplicación", st['th']),
                Paragraph("Enlace", st['th']),
                Paragraph("Descripción", st['th']),
                Paragraph("Funciones principales", st['th'])
            ]
        ]
        
        for nombre, url, desc, funciones in cat["herramientas"]:
            link_html = f'<a href="{url}" color="#0284c7"><u>Visitar</u></a>'
            
            table_data.append([
                Paragraph(f"<b>{nombre}</b>", st['td_bold']),
                Paragraph(link_html, st['link']),
                Paragraph(desc, st['td']),
                Paragraph(funciones, st['td'])
            ])
        
        tbl = Table(
            table_data, 
            colWidths=[95, 55, 184, 170],
            repeatRows=1
        )
        
        header_bg = COLOR_PRIMARY if "Texto" in cat["nombre"] or "Programación" in cat["nombre"] else COLOR_SECONDARY
        
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), header_bg),
            ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        
        story.append(tbl)
        story.append(Spacer(1, 10))

    # --- Función para construir el Canvas ---
    def canvas_builder(*args, **kwargs):
        return NumberedCanvas(*args, doc_subtitle="DIRECTORIO DE APLICACIONES DE IA", **kwargs)

    doc.build(story, canvasmaker=canvas_builder)
    print(f"Documento de aplicaciones generado exitosamente: {filename}")


if __name__ == "__main__":
    create_ai_tools_pdf()