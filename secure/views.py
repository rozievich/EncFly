import base64
from tkinter.tix import Tree
from uuid import uuid4
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser

from .serializers import CustomUserModelSerializer, FileModelSerializer
from .models import CustomUser, FileModel
from .permissions import IsOwnerPermission
from .utils.encryption import aes_encrypt_file


class CustomUserModelViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsOwnerPermission()]


class FileModelViewSet(ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileModelSerializer
    permission_classes = [IsOwnerPermission]
    parser_classes = (MultiPartParser, )

    def create(self, request, *args, **kwargs):
        upload_file = request.FILES['file']
        secret_key = base64.b64decode(request.user.secret_key)

        file_bytes = upload_file.read()

        file_name = uuid4()
        encrypted_file = aes_encrypt_file(file_bytes, key=secret_key)
        encrypted_content = ContentFile(encrypted_file, name=file_name + '.enc')

        serializer = self.get_serializer(data={
            "file": encrypted_content,
            "file_type": upload_file.content_type,
            "file_id": file_name,
            "user": request.user.id
        })
        serializer.is_valid()

