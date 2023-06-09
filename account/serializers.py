from rest_framework import serializers
from .models import User
from .utils import send_activation_code
from .tasks import send_activation_code_celery
from django.core.mail import send_mail

class RegistSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length = 4, required = True, write_only = True)
    password = serializers.CharField(min_length = 4, required = True, write_only = True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm  = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError( 'passwords not same')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user
    

class ForgotPasswordSerialazer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email нет')
        return email
    

    def send_verification_email(self):
        email=self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_mail('Восстановление пароля',f'Ваш код восстановления {user.activation_code}','test@gmail.com',[user.email])

    
    

class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.CharField()
    code= serializers.CharField()
    password = serializers.CharField(min_length = 4, required=True)
    password_confirm = serializers.CharField(min_length = 4, required=True)
    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        passw = data.get('password')
        pass_con = data.get('password_confirm')
        if not User.objects.filter(email=email, activation_code = code).exists():
            raise serializers.ValidationError('Пользователь с таким email нет')
        if passw !=pass_con:
            raise serializers.ValidationError('Пароли не совпадают')
        return data
        
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email = email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangePasswordSerialazer(serializers.Serializer):     #мы наследуемся от потому что мы сами можем задавать поля
    old_password = serializers.CharField(min_length = 4, required=True)
    new_password = serializers.CharField(min_length = 4, required=True)
    new_password_confirm = serializers.CharField(min_length = 4, required=True)

    def validate_old_password(self, old_password):
        request= self.context.get('request')
        user = request.user
        if not user.check_password(old_password):     #проверяет пароль и под капотом хэширует его
            raise serializers.ValidationError('Вы ввели некорректный пароль')
        return old_password
    

    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')
        new_pass_con = data.get('new_password_confirm')
        if new_pass !=new_pass_con:
            raise serializers.ValidationError('Пароли не совпадают')
        if old_pass ==new_pass:
            raise serializers.ValidationError('Пароль должен отличаться от прошлых')
        return data
    
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()
