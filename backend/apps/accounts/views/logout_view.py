from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from rest_framework import status


class LogoutView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        logout(request)
        return Response({'msg':'successfully logged out'}, status=status.HTTP_204_NO_CONTENT)