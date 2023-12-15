from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UploadDataSerializer(serializers.Serializer):
    """Загрузка файла в систему."""

    file = serializers.FileField(required=True)

    def validate_file(self, file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        """Проверка файла."""
        if file.content_type != 'text/csv':
            raise ValidationError(
                _('Возможно загружать только csv-файл'),
            )
        return file
