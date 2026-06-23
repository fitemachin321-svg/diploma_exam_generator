from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# Регистрация шрифта
try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Пробуем разные варианты
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux (Render)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",                 # Linux
        "C:/Windows/Fonts/arial.ttf",                                       # Windows
        "C:/Windows/Fonts/ariali.ttf",                                     # Windows (альтернатива)
    ]
    
    font_registered = False
    for path in font_paths:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont('Arial', path))
            font_registered = True
            print(f"Шрифт загружен: {path}")
            break
    
    if not font_registered:
        # Используем стандартный шрифт ReportLab
        from reportlab.lib.fonts import addMapping
        addMapping('Helvetica', 0, 0, 'Helvetica')
        print("Используется шрифт Helvetica (без кириллицы)")
        
except Exception as e:
    print(f"Ошибка загрузки шрифта: {e}")

class ExamPDFGenerator:
    def __init__(self, filename, title):
        self.filename = filename
        self.title = title
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                     rightMargin=2*cm, leftMargin=2*cm,
                                     topMargin=2*cm, bottomMargin=2*cm)
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle('RussianNormal', parent=self.styles['Normal'],
                                       fontName='Arial', fontSize=11, leading=14, encoding='utf-8'))
        self.styles.add(ParagraphStyle('RussianHeader', parent=self.styles['Heading1'],
                                       fontName='Arial', fontSize=16, alignment=1, spaceAfter=20, encoding='utf-8'))
        self.styles.add(ParagraphStyle('RussianVariant', parent=self.styles['Heading2'],
                                       fontName='Arial', fontSize=13, spaceAfter=10, encoding='utf-8'))
        self.styles.add(ParagraphStyle('RussianAnswer', parent=self.styles['Normal'],
                                       fontName='Arial', fontSize=11, leftIndent=20, encoding='utf-8'))
        self.story = []
    
    def _add_header_info(self):
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.story.append(Paragraph(f"Дата генерации: {date_str}",
                                    self.styles['RussianNormal']))
        self.story.append(Spacer(1, 0.3*cm))
    
    def generate_header(self):
        self.story.append(Paragraph(self.title, self.styles['RussianHeader']))
        self._add_header_info()
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_variant(self, variant_number, questions):
        self.story.append(Paragraph(f"Вариант {variant_number}", self.styles['RussianVariant']))
        self.story.append(Spacer(1, 0.2*cm))
        for i, q in enumerate(questions, 1):
            q_text = f"{i}. {q.get('text', 'Нет текста')}"
            if q.get('points'):
                q_text += f" (макс. {q.get('points')} баллов)"
            self.story.append(Paragraph(q_text, self.styles['RussianNormal']))
            self.story.append(Spacer(1, 0.4*cm))
            if 'answers' not in self.filename:
                self.story.append(Paragraph("Ответ: ____________________", self.styles['RussianNormal']))
                self.story.append(Spacer(1, 0.3*cm))
        self.story.append(Spacer(1, 0.7*cm))
    
    def generate_answers(self, answers):
        self.story.append(Paragraph("ОТВЕТЫ (для учителя)", self.styles['RussianVariant']))
        self.story.append(Spacer(1, 0.5*cm))
        for variant_num in sorted(answers.keys()):
            self.story.append(Paragraph(f"Вариант {variant_num}:", self.styles['RussianVariant']))
            for i, ans in enumerate(answers[variant_num], 1):
                self.story.append(Paragraph(f"{i}. {ans}", self.styles['RussianAnswer']))
            self.story.append(Spacer(1, 0.3*cm))
    
    def build(self):
        self.doc.build(self.story)