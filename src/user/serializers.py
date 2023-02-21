from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError, EmailField, CharField
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class SignUpSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'username', 'password']
    extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

  def validate(self, attrs):
    email = attrs.get('email', '')
    first_name = attrs.get('first_name', '')
    last_name = attrs.get('last_name', '')
    username = attrs.get('username', '')

    if not username.isalnum():
      raise ValidationError('Field `username` must be alpha-numeric.')
    return attrs

  def create(self, validated_data):
    return User.objects.create_user(**validated_data)

class TokenSerializer(Serializer):
  access = CharField(max_length=255, read_only=True)
  refresh = CharField(max_length=255, read_only=True)  

class LogInSerializer(Serializer):
  email = EmailField(max_length = 255, min_length = 3, write_only=True)
  password = CharField(max_length = 255, min_length = 3, write_only=True)
  token = TokenSerializer(read_only = True)

  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')
    user = authenticate(email = email, password = password)
    if not user:
      raise AuthenticationFailed('Invalid Credentials')
    if not user.is_active:
      raise AuthenticationFailed('User is Disabled')
    return {
        "token": user.token()
    }

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']

