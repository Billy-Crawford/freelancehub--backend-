# users/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, UserSerializer,
    FreelanceProfileSerializer, ClientProfileSerializer
)
from .models import User, FreelanceProfile, ClientProfile


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Compte créé avec succès.",
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=201)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FreelanceProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'freelance':
            return Response({"error": "Accès réservé aux freelances."}, status=403)

        profile, _ = FreelanceProfile.objects.get_or_create(user=request.user)

        return Response(FreelanceProfileSerializer(profile).data)

    def put(self, request):
        if request.user.role != 'freelance':
            return Response({"error": "Accès réservé aux freelances."}, status=403)

        profile, _ = FreelanceProfile.objects.get_or_create(user=request.user)

        serializer = FreelanceProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ClientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'client':
            return Response({"error": "Accès réservé aux clients."}, status=403)
        profile, _ = ClientProfile.objects.get_or_create(user=request.user)
        return Response(ClientProfileSerializer(profile).data)

    def put(self, request):
        if request.user.role != 'client':
            return Response({"error": "Accès réservé aux clients."}, status=403)
        profile, _ = ClientProfile.objects.get_or_create(user=request.user)
        serializer = ClientProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PublicFreelanceProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        return generics.get_object_or_404(User, pk=self.kwargs['pk'], role='freelance')

