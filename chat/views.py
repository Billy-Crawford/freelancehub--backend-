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


# +++++++++++++++++++++ MESSAGERIE ++++++++++++++++++++++++++++++

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Message

class MessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, mission_id):
        messages = Message.objects.filter(mission_id=mission_id).order_by("timestamp")

        data = [
            {
                "id": msg.id,
                "content": msg.content,
                "file": msg.file.url if msg.file else None,
                "sender_id": msg.sender.id,
                "sender_email": msg.sender.email,
                "timestamp": msg.timestamp,
            }
            for msg in messages
        ]

        return Response(data)

    def post(self, request, mission_id):
        content = request.data.get("message")
        file = request.FILES.get("file")

        if not content and not file:
            return Response({"error": "Message vide"}, status=400)

        message = Message.objects.create(
            sender=request.user,
            mission_id=mission_id,
            content=content,
            file=file
        )

        return Response({
            "id": message.id,
            "content": message.content,
            "file": message.file.url if message.file else None,
            "sender_id": message.sender.id,
            "sender_email": message.sender.email,
            "timestamp": message.timestamp,
        })