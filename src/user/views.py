from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, LogInSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SignUp(APIView):
  serializer_class = SignUpSerializer
  def post(self, request):
    data = request.data
    serializer = self.serializer_class(data = data)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data, status = status.HTTP_201_CREATED)

class LogIn(APIView):
  serializer_class = LogInSerializer
  def post(self, request):
    data = request.data
    serializer = self.serializer_class(data = data)
    serializer.is_valid(raise_exception = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

class GetUser(APIView):
  authentication_classes = (JWTAuthentication, )
  permission_classes = (IsAuthenticated,)
  serializer_class = UserSerializer
  def get(self, request):
    serializer = self.serializer_class(instance = request.user)
    return Response(serializer.data, status = status.HTTP_200_OK)
