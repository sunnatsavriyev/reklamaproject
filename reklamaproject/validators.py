from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx']
    if ext not in valid_extensions:
        raise ValidationError(f"Fayl turi {ext} qo‘llab-quvvatlanmaydi. Ruxsat etilgan: {', '.join(valid_extensions)}.")
