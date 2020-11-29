from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps


class SafeModelManager(models.Manager):
    """
    Базовый менеджер, возвращает модели, для которых поле is_deleted == False
    """
    def get_queryset(self):
        return super(SafeModelManager, self).get_queryset().exclude(is_deleted=True)


class ExtendedModelManager(models.Manager):
    """
    Расширенный менеджер, позволяющий доступ к удаленным объектам
    """
    def get_queryset(self):
        return super(ExtendedModelManager, self).get_queryset()


class SafeModel(models.Model):
    """
    Безопасная для удаления модель
    """
    # Зависимые модели, используется методом safe_delete
    # Вид: app_label: app_dict, например
    # {'users': {'model': 'RegistrationRequest', 'related_field': 'user'}} - модель юзера в приложении auth
    RELATED_MODELS = {}

    created_at = models.DateTimeField(default=timezone.now(), editable=False)

    is_deleted = models.BooleanField(default=False, verbose_name=_('Удален'))

    objects = SafeModelManager()
    extended_objects = ExtendedModelManager()

    class Meta:
        db_table = 'safe_model'
        ordering = ['-created_at']
        verbose_name_plural = 'Безопасные модели'
        verbose_name = 'Безопасная модель'

    def safe_delete(self):
        """Безопасное удаление, не удаляет данные из БД, но скрывает их для дефолтного менеджера данных"""
        self.is_deleted = True
        for app_label, app_dict in self.RELATED_MODELS.items():
            model = apps.get_model(app_label, app_dict['model'])
            filter_dict = {app_dict['related_field']: self.id}
            objs = model.objects.filter(**filter_dict)
            for obj in objs:
                obj.safe_delete()
        self.save()

    def __str__(self):
        return 'Safe model'

    def save(self, *args, **kwargs):
        if self.is_deleted:
            self.safe_delete()
        super(SafeModel, self).save(*args, **kwargs)
