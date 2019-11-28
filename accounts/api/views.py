from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth import logout,login

# rest_framework
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# relative imports
from .serializers import UserRegisterSerializer
from .permissions import AnonPermissionOnly

# jwt handlers
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

# User model
User=get_user_model()

# Login ENDPOINT Handler
class AuthView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"data":"You are already authenticated"})
        data=request.data
        query=data.get("phone_number")
        password=data.get("password")
        qs=User.objects.filter(
            Q(phone_number__iexact=query)|
            Q(email__iexact=query)
        ).distinct()
        if qs.count()==1:
            user_obj=qs.first()
            if  user_obj.check_password(password):
                user=user_obj
                login(request,user)
                payload=jwt_payload_handler(user)
                token=jwt_encode_handler(payload)
                response=jwt_response_payload_handler(token,user,request=request)
                return Response(response)
        return Response({"data":"Invalid Credentials"},status=401).add_post_render_callback

# Register ENDPOINT Handler
class RegisterAPIView(generics.CreateAPIView):
    queryset            =  User.objects.all()
    serializer_class    =  UserRegisterSerializer
    permission_classes  =  [AnonPermissionOnly]

    def get_serializer_context(self, *args,**kwargs):
        return {"request": self.request}

# Logout ENDPOINT Handler
class LogoutAPIView(APIView):
    def post(self,request,*args,**kwargs):
        logout(request)
        return Response({"Message":"Successfully Logged out"},status=200)