from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'display_name','username', 'email','password', 'password2')
        read_only_fileds = ('id',)
        
        
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("User already exists for this email!!")
        return value
    
    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)
        return user