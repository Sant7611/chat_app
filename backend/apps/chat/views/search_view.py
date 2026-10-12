from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from apps.chat.serializers.conversation_serializer import UserMiniSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserSearchView(ListAPIView):

    serializer_class = UserMiniSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()

        if not query:
            return User.objects.none()

        if query:
            return (
                User.objects.exclude(id=self.request.user.pk)
                .filter(
                    Q(username__icontains=query)
                    | Q(email__iexact=query)
                    | Q(display_name__icontains=query)
                )
                .order_by("username")[:10]
            )
