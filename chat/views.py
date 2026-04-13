from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Message


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        messages = Message.objects.filter(
            sender=user
        ).values("mission", "mission__title").distinct()

        conversations = []

        for msg in messages:
            conversations.append({
                "mission_id": msg["mission"],
                "mission_title": msg["mission__title"]
            })

        return Response(conversations)

