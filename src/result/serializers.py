from rest_framework.serializers import ModelSerializer, CharField, IntegerField
from django.shortcuts import get_object_or_404
from .models import Registration, Response
from src.test.models import Question
from src.user.serializers import UserSerializer
from src.test.serializers import QuestionSerializer

class ResponseSerializer(ModelSerializer):
    question_id = IntegerField(write_only=True)
    question = QuestionSerializer(read_only=True)
    status = CharField(max_length = 255, read_only = True)
    class Meta:
        model = Response
        fields = ['question_id', 'question', 'answer', 'status']

    def create(self, validated_data):
      q = validated_data.pop('question_id', None);
      question = get_object_or_404(Question, id=q)
      validated_data["question"] = question
      return Response.objects.create(**validated_data)

class ResultSerializer(ModelSerializer):
    responses = ResponseSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    class Meta:
        model = Registration
        fields = ['id', 'user', 'score', 'created_at', 'responses']
