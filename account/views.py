from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrSerializer
from rest_framework.response import Response
from .models import User
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegistrSerializer())
    def post(self, request):
        data = request.data
        serializer = RegistrSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered',201)
        

class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email,activation_code=activation_code).first()
        if not user:
            return Response(
                'User does not exict',400
            )
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated',200)