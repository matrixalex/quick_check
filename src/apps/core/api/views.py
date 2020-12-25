from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from src.apps.core.errors import ErrorMessages
from src.apps.core.excetions.main import FieldException
from src.apps.core import service
from django.db import models


class BaseModelView(APIView):
    model = None


class BaseCreateOrChangeView(BaseModelView):
    """
    Базовый класс создания сущности

    fields: словарь полей для создания сущности, формат каждого элемента
        field_name: str {
            'required': bool - необходимость наличия данных в поле
            'type': FieldTypeEnumerate
            'default': значение по умолчанию
            'validator': function - валидатор поля,
            'model': SafeModel subclass - для типа FOREIGN_KEY или MANY_TO_MANY
        }
    """
    class FieldTypeEnumerate:
        INT = 0
        STR = 1
        BOOL = 2
        FLOAT = 3
        FILE = 4
        FOREIGN_KEY = 5
        MANY_TO_MANY = 6
        DATE = 7

    _fields = {}
    # Объект создания
    obj = None
    edit = False

    def parse_field(self, field_conf, value):
        """Приведение поля к типу."""
        field_type = field_conf.get('type', self.FieldTypeEnumerate.STR)
        if field_type == self.FieldTypeEnumerate.INT:
            return int(value)
        elif field_type == self.FieldTypeEnumerate.BOOL:
            return bool(value)
        elif field_type == self.FieldTypeEnumerate.FLOAT:
            return float(value)
        elif field_type == self.FieldTypeEnumerate.FOREIGN_KEY:
            value = field_conf['model'].objects.get(pk=value)
            return value
        elif field_type == self.FieldTypeEnumerate.MANY_TO_MANY:
            value = field_conf['model'].objects.filter(id__in=value)
            return value
        elif field_type == self.FieldTypeEnumerate.FILE:
            value = service.upload_file(value)
            return value
        elif field_type == self.FieldTypeEnumerate.DATE:
            return service.parse_date(value)
        return value

    def get_fields(self, request):
        """Получение полей из реквеста."""
        fields = {}
        for field_name in self._fields:
            value = request.data.get(field_name)
            if self._fields[field_name].get('required', False) and not value:
                raise FieldException('Поле {} обазательно для заполнения'.format(field_name))

            field_type = self._fields[field_name].get('type')
            if field_type:
                try:
                    value = self.parse_field(self._fields[field_name], value)
                except:
                    raise FieldException('Поле {} со значением {} невозможно привести к типу {}'.format(
                        field_name, value, field_type
                    ))
            validator = self._fields[field_name].get('validator')
            if validator and value:
                check = validator(value)
                if not check:
                    raise FieldException("Поле {} не прошло валидацию".format(field_name))
            if value:
                fields[field_name] = value
        return fields

    def create_object(self, create_fields):
        try:
            obj = self.model.objects.create(**create_fields)
            return obj
        except:
            return None

    def change_object(self, change_fields):
        """Изменение объекта"""
        obj = self.model.objects.get(pk=change_fields['id'])
        change_fields.pop('id')
        for attr, value in change_fields.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

    def extra_post(self, request):
        """Позволяет выполнить дополнительные действия после создания или редактирования."""
        pass

    def post(self, request):
        try:
            fields = self.get_fields(request)
            if 'id' in fields:
                self.obj = self.change_object(fields)
            else:
                self.obj = self.create_object(fields)
            self.extra_post(request)
            if self.obj:
                return Response({'result': {'status': True}}, HTTP_200_OK)
            return Response({'result': {'status': False}}, HTTP_400_BAD_REQUEST)
        except FieldException as e:
            return Response({'result': {'message': str(e)}}, HTTP_400_BAD_REQUEST)
        except models.ObjectDoesNotExist:
            return Response({'result': {'message': ErrorMessages.NO_OBJECT}}, HTTP_400_BAD_REQUEST)


class BaseDeleteView(BaseModelView):
    """Базовый класс удаления сущности"""
    model = None

    def post(self, request):
        object_id = request.data.get('id')
        try:
            self.model.objects.get(pk=object_id).safe_delete()
        except Exception as e:
            print('something gone wrong')
            print(repr(e))
            return Response({'result': {'status': True}}, HTTP_400_BAD_REQUEST)
        return Response({'result': {'status': True}}, HTTP_200_OK)
