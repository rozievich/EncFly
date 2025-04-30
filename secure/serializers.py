import base64
from rest_framework.serializers import ModelSerializer, CurrentUserDefault, HiddenField, CharField

from .models import CustomUser, FileModel
from .utils.hashing import key_from_password


class CustomUserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password',
            'first_name', 'last_name', 'is_active',
            'is_staff', 'is_superuser', 'date_joined',
            'last_login', 'secret_key', 'groups', 'user_permissions'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'groups': {'read_only': True},
            'secret_key': {'read_only': True},
            'user_permissions': {'read_only': True},

        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        secret_key, salt = key_from_password(password)
        validated_data['secret_key'] = base64.b64encode(secret_key).decode('utf-8')
        validated_data['salt'] = base64.b64encode(salt).decode('utf-8')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FileModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    file_id = CharField(read_only=True)
    file_type = CharField(read_only=True)

    class Meta:
        model = FileModel
        fields = '__all__'
