from django.contrib.auth.models import Group

from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.serializers import UserSerializer, AuthTokenSerializer

from core.models import User


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user.pk,
            'username': user.username,
            'is_verwaltung': user.is_verwaltung,
            'is_benutzerverwaltung': user.is_benutzerverwaltung,
            'is_superuser': user.is_superuser
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class ManageAllUserView(viewsets.ModelViewSet):
    """Manage all user"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
