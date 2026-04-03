from rest_framework import generics, permissions
from .models import Mission
from .serializers import MissionSerializer
from .permissions import IsClient, IsOwnerOrReadOnly


# 🔹 Liste + création
class MissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.all().order_by('-created_at')
    serializer_class = MissionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsClient()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


# 🔹 Détail + update + delete
class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

