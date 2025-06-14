from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Received data: {request.data}")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"User created successfully: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({"error": str(e)}, status=400)
