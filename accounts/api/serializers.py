from rest_framework import serializers
from django.contrib.auth import get_user_model
import datetime
from django.conf import settings
from django.utils import timezone


#  token expires after a period of EXPIRATION_DELTA
expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

# JWT configuration to use
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

# instance of user model
User = get_user_model()

# Registeration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=User
        fields=[
            'name',
            'phone_number',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message'
        ]   
    def validate_phone_number(self,value):
        qs = User.objects.filter(phone_number__iexact=value)
        import re
        if not re.match("\d{10}",value):
            raise serializers.ValidationError("Enter a valid phone number")
        if qs.exists():
            raise serializers.ValidationError("User with this phone number already exists")
        return value
    def get_message(self,obj):
        return "Registeration Successfull. To login go to /api/auth/"
    def get_expires(self,obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def get_token(self, obj):
        payload=jwt_payload_handler(obj)
        token=jwt_encode_handler(payload)
        return token
    def validate(self,data):
        pw = data.get("password")
        pw2 = data.pop("password2")
        if pw!= pw2:
            raise serializers.ValidationError("Passwords must match")
        return data
    
