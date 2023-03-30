import io

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts

VERTICAL = 50
HORIZONTAL = 750
FONT_SIZE = 10

def draw_pdf(data):
    """Функция для создания PDF-файла с ингредиентами для рецептов
     из списка покупок."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    pdfmetrics.registerFont(ttfonts.TTFont('Verdana', 'Verdana.ttf'))
    c.setFont('Verdana', FONT_SIZE)
    horizontal = HORIZONTAL
    for i in range(len(data)):
        c.drawString(VERTICAL, horizontal, f'{data[i]}')
        horizontal -= 30
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
