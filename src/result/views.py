from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ResultSerializer, ResponseSerializer
from .models import Registration, Response as ResponseModel

class ResultAPI(APIView):
    """
    @extends APIView
    @description APIView for listing all Results
    @url /registrations/
    """

    serializer_class = ResultSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        """
        @description returns all the results
        @method GET
        """
        query_set = Registration.objects.all()
        serializer = self.serializer_class(query_set, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ResultDetailAPI(APIView):
    """
    @extends APIView
    @description APIView for single Result Details
    @url /registrations/<int:id>/
    """
    serializer_class = ResultSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, id):
        query_set = get_object_or_404(Registration, id = id)
        serializer = self.serializer_class(query_set)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ResultResponseAPI(APIView):
    """
    @extends APIView
    @description APIView for listing all responses under a registration
    @url /registrations/<int:id>/responses/
    """
    serializer_class = ResponseSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, id):
        query_set = get_list_or_404(ResponseModel, registration__id = id)
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        data = request.data
        registration = get_object_or_404(Registration, id = id)
        if(isinstance(data, list)):
            serializer = self.serializer_class(data = data, many=True)
        else:
            serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save(registration = registration)
        response = { "success": True, data: serializer.data}
        return Response(response, status=status.HTTP_200_OK)