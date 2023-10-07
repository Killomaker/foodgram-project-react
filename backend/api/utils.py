import io

from django.http import HttpResponse
from reportlab.pdfgen import canvas


def create_shopping_cart(ingredients_cart):
    """Функция для создания файла списка покупок"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        "attachment; filename='shopping_cart.pdf'"
    )
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)
    pdf_file.drawString(200, 800, 'Список покупок.')
    from_bottom = 750
    for number, ingredient in enumerate(ingredients_cart, start=1):
        pdf_file.drawString(
            50,
            from_bottom,
            f"{number}. {ingredient['ingredient__name']}: "
            f"{ingredient['ingredient_value']} "
            f"{ingredient['ingredient__measurement_unit']}.",
        )
        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 800
            pdf_file.showPage()
    pdf_file.showPage()
    pdf_file.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response