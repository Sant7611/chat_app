from rest_framework.views import APIView
from accounts.serializers.login_serializer import LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"msg": "The entered password or email is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request=request, user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)