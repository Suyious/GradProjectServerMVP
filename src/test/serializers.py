from rest_framework.serializers import ModelSerializer, BooleanField
from .models import Test, Question
from src.user.serializers import UserSerializer

class QuestionSerializer(ModelSerializer):
  class Meta:
    model = Question
    fields = ['id', 'serial', 'statement', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']
    extra_kwargs = {
      'answer': {'write_only': True}
    }

  def validate(self, attrs):
    serial = attrs.get('serial', '')
    statement = attrs.get('statement', '')
    option_1 = attrs.get('option_1', '')
    option_2 = attrs.get('option_2', '')
    option_3 = attrs.get('option_3', '')
    option_4 = attrs.get('option_4', '')
    answer = attrs.get('answer', '')
    return attrs

  def create(self, validated_data):
    test = validated_data.get('test', None)
    return Question.objects.create(**validated_data)

class TestSerializer(ModelSerializer):
  questions = QuestionSerializer(many = True, required=False, write_only=True)
  author = UserSerializer(required=False)

  class Meta:
    model = Test
    fields = [ 'id', 'name', 'description', 'created_at' ,'starts_at', 'duration', 'questions', 'author',
                'isTestOnline', 'isTestAvailable', 'isTestOffline', 'endsAt' ]

  def validate(self, attrs):
    name = attrs.get('name','')
    description = attrs.get('description','')
    starts_at = attrs.get('starts_at','')
    duration = attrs.get('duration','')
    return attrs

  def create(self, validated_data):
    questions_data = validated_data.pop('questions', [])
    # validated_data["author"] = self.context['request'].user
    test = Test.objects.create(**validated_data)
    self._create_questions(test, questions_data)
    return test

  def _create_questions(self, test, questions_data):
    for question_data in questions_data:
      question = Question.objects.create(test=test, **question_data)
      test.questions.add(question)
