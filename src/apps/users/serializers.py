from rest_framework.serializers import ModelSerializer, RelatedField
from .models import User, UserType, RegistrationRequest


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegistrationRequestSerializer(ModelSerializer):
    registration_user = RelatedField(read_only=True)

    class Meta:
        model = RegistrationRequest
        fields = '__all__'


class UserTypeSerializer(ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
