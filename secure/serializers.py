from rest_framework.serializers import ModelSerializer, CharField

from .models import CustomUser


class CustomUserModelSerializer(ModelSerializer):
    password = CharField(write_only=True)
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
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        return rep

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_internal_value(self, data):
        if self.context['request'].method == 'POST':
            allowed = {'username', 'email', 'password'}
            data = {k: v for k, v in data.items() if k in allowed}
        return super().to_internal_value(data)
