from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs


@database_sync_to_async
def get_user_id(token):
    User = get_user_model()

    try:
        access = AccessToken(token)
        user_id = access.get("user_id")
        return User.objects.get(id=user_id)
    except (KeyError, User.DoesNotExist, TokenError):
        return AnonymousUser()


class JWTAuthMiddleware:

    async def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        scope["user"] = get_user_id(token) if token else AnonymousUser()

        return await self.ap(scope, receive, send)
