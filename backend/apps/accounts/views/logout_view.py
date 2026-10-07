from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        
        refresh = request.data.get('refresh')
        if refresh:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"msg":"successfully logged out "}, status=status.HTTP_200_OK)
        else:
            return Response({'error':"no refresh token found"}, status=status.HTTP_400_BAD_REQUEST)
        