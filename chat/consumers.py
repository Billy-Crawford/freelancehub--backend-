# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from missions.models import Mission
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.mission_id = self.scope['url_route']['kwargs']['mission_id']

        self.user = self.scope.get("user")

        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        mission = await self.get_mission(self.mission_id)

        if not mission:
            await self.close()
            return

        # 🔥 ROOM UNIQUE BASÉE SUR MISSION
        self.room_group_name = f"chat_mission_{self.mission_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_mission(self, mission_id):
        try:
            return Mission.objects.get(id=mission_id)
        except:
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        await self.save_message(self.user.id, self.mission_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "sender_email": self.user.email,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_email": event["sender_email"],
        }))

    # 🔐 Vérification accès chat
    @database_sync_to_async
    def can_access_chat(self, user, mission_id, freelance_id):
        try:
            mission = Mission.objects.get(id=mission_id)

            # ✔ Client propriétaire
            if user == mission.client:
                return True

            # ✔ Freelance concerné
            if user.id == int(freelance_id):
                return True

            return False
        except:
            return False

    # 💾 Sauvegarde message
    @database_sync_to_async
    def save_message(self, user_id, mission_id, message):
        try:
            user = User.objects.get(id=user_id)
            mission = Mission.objects.get(id=mission_id)

            Message.objects.create(
                sender=user,
                mission=mission,
                content=message
            )
        except Exception as e:
            print("Erreur save_message:", e)


