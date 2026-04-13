# core/asgi.py
import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from chat.consumers import ChatConsumer
from core.jwt_middleware import JWTAuthMiddleware

django_asgi_app = get_asgi_application()

from django.urls import path
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter([
            path("ws/chat/<int:mission_id>/", ChatConsumer.as_asgi()),
        ])
    ),
})


