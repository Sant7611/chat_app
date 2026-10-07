from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(trim_whitespace=False, write_only=True)


    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user=authenticate(request=self.context['request'], email =email, password = password)
            
            if user is None:
                raise serializers.ValidationError("The entered password or email is incorrect")

            attrs['user']=user
                
        else:
            raise serializers.ValidationError("Both email and password is required")

        return attrs