from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegistSerializer, ForgotPasswordCompleteSerializer, ForgotPasswordSerialazer, ChangePasswordSerialazer
from rest_framework.response import Response
from .models import User
from .permissions import IsActivePermission
import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegistSerializer())
    def post(self, request):
        data = request.data
        serializer = RegistSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Succesfully registerd', 201)
        
class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', 200)
    
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerialazer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Мы выслали сообщение для востановления')
        
class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('password sucsessfully changed')


class ChangePasswordView(APIView):
    permission_classes = (IsActivePermission,)
    def post(self, request):
        serializer = ChangePasswordSerialazer(data = request.data, context={'request':request})    #context- словарь с какими-то данными, все что связано с запросами . С context можно вытаскивать ...
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Status: 200. Password sucsessfuly changed')