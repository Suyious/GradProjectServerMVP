from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import TestSerializer, QuestionSerializer
from .models import Test, Question
from src.result.serializers import ResultSerializer
from src.result.models import Registration

class TestsAPI(APIView):
  """
  @extends APIView
  @description APIView for listing and creating tests
  @url /tests/
  """
  serializer_class = TestSerializer
  authentication_classes = (JWTAuthentication, )
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def get(self, request):
    """
    @description returns all tests filtered by query params
    @method GET
    """
    filter_param = request.GET.get("filter", "")
    query_set = Test.objects.all()
    if(filter_param and filter_param == "online"):
      query_set = [ x for x in query_set if x.isTestOnline ]
    if(filter_param and filter_param == "available"):
      query_set = [ x for x in query_set if x.isTestAvailable ]
    if(filter_param and filter_param == "offline"):
      query_set = [ x for x in query_set if x.isTestOffline ]
    serializer = self.serializer_class(query_set, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

  def post(self, request):
    """
    @description creates new test and returns
    @method POST
    """
    data = request.data
    # serializer = self.serializer_class(data = data, context = { 'request': request });
    serializer = self.serializer_class(data = data);
    serializer.is_valid(raise_exception = True)
    serializer.save(author = request.user)
    response = { "success": True, "data": serializer.data }
    return Response(response, status = status.HTTP_200_OK)

class TestDetailAPI(APIView):
  """
  @extends APIView
  @description APIView for test details
  @url /tests/<int:id>/
  """
  serializer_class = TestSerializer

  def get(self, request, id):
    """
    @description returns detail for test with id=`id`
    @method GET
    """
    data = get_object_or_404(Test, id = id)
    serializer = self.serializer_class(data)
    response = { "success": True, "data": serializer.data }
    return Response(response, status = status.HTTP_200_OK)

  def delete(self, request, id):
    """
    @description deletes test with id=`id`
    @method DELETE
    """
    data = get_object_or_404(Test, id = id)
    data.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class TestQuestionAPI(APIView):
  """
  @extends APIView
  @description APIView for test questions list and create
  @url /tests/<int:id>/questions/
  """
  serializer_class = QuestionSerializer
  authentication_classes = (JWTAuthentication, )
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def get(self, request, id):
    """
    @description returns all questions for test with id=`id`
    @method GET
    """
    serializer = self.serializer_class(Question.objects.filter(test__id = id), many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

  def post(self, request, id):
    """
    @description creates single or multiple questions for test with id=`id`
    @method POST
    """
    data = request.data
    test = get_object_or_404(Test, id = id)
    if not request.user == test.author:
      response = {"success": False, "data": "you are not authenticated"}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(data, list):
      serializer = self.serializer_class(data = data, many=True)
    else:
      serializer = self.serializer_class(data = data)
    serializer.is_valid(raise_exception = True)
    try:
      serializer.save(test = test)
    except IntegrityError:
      response = {"success": False, "data": "duplicate question"}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    response = { "success": True, "data": serializer.data }
    return Response(response, status = status.HTTP_200_OK)

class TestQuestionDetailAPI(APIView):
  """
  @extends APIView
  @description APIView for test question detail
  @url /tests/<int:tid>/questions/<int:qid>/
  """
  serializer_class = QuestionSerializer
  authentication_classes = (JWTAuthentication, )
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def get(self, request, tid, qid):
    """
    @description returns question with serial=`qid` for test with id=`tid`
    @method GET
    """
    data = get_object_or_404(Question.objects.filter(test__id = tid), serial = qid)
    serializer = self.serializer_class(data)
    return Response(serializer.data, status = status.HTTP_200_OK)


class TestResultAPI(APIView):
  """
  @extends APIView
  @description APIView for test results
  @url /tests/<int:tid>/registrations/
  """
  serializer_class = ResultSerializer
  authentication_classes = (JWTAuthentication, )
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def get(self, request, id):
    """
    @description returns all registrations for a test with score results
    @method GET
    """
    # data = get_list_or_404(Registration, test__id = id)
    data = Registration.objects.filter(test__id = id)
    serializer = self.serializer_class(data, many=True)
    return Response(serializer.data, status = status.HTTP_200_OK)
  
  def post(self, request, id):
    """
    @description 
    - allows registering for a test
    - returns created registration
    @method POST
    """
    data = get_object_or_404(Test, id = id)
    if not data.isTestAvailable:
      response = { "success": False, "data": "unavailable" }
      return Response(response, status = status.HTTP_400_BAD_REQUEST)
    serializer = self.serializer_class(data = request.data)
    serializer.is_valid(raise_exception=True)
    try:
      serializer.save(test=data, user=request.user)
    except IntegrityError:
      response = {"success": False, "data": "already registered"}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    response = { "success": True, "data": serializer.data }
    return Response(response, status = status.HTTP_200_OK)
