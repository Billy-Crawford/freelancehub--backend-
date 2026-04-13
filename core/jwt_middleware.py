# core/jwt_middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except:
        return None


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)

        token = params.get("token")

        if token:
            user = await get_user(token[0])
            scope["user"] = user
        else:
            scope["user"] = None

        return await self.inner(scope, receive, send)

