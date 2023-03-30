from rest_framework.serializers import ModelSerializer, CharField
from .models import Registration, Response
from src.test.models import Question
from src.user.serializers import UserSerializer
from src.test.serializers import QuestionSerializer

class ResponseSerializer(ModelSerializer):
    question = QuestionSerializer(required = False)
    status = CharField(max_length = 255, read_only = True)
    class Meta:
        model = Response
        fields = ['question', 'answer', 'status']


class ResultSerializer(ModelSerializer):
    responses = ResponseSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    class Meta:
        model = Registration
        fields = ['id', 'user', 'score', 'created_at', 'responses']