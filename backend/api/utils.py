from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from recipies.models import IngridientInRecipe


def download_table_as_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="table.pdf"'

    # Получите данные из вашей модели
    queryset = IngridientInRecipe.objects.all()

    # Создайте таблицу и добавьте данные из базы данных
    data = []
    data.append(['Ингредиент', 'Единицы изменения', 'Количество'])
    for item in queryset:
        data.append([item.field1, item.field2, item.field3])

    table = Table(data)
    table.setStyle(TableStyle(
        [
            # Стилизуйте таблицу по вашему усмотрению
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]
    ))

    # Создайте документ и добавьте таблицу
    doc = SimpleDocTemplate(response)
    doc.build([table])

    return response