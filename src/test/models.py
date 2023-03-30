from django.db import models
from django.conf import settings
from django.utils import timezone

class Test(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name = "Author", related_name = "tests")
  name = models.CharField(max_length=255, verbose_name = "Name")
  description = models.TextField(verbose_name = "Description")
  created_at = models.DateTimeField(auto_now_add = True)
  starts_at = models.DateTimeField(verbose_name = "Starts At")
  duration = models.DurationField(verbose_name = "Duration")

  # candidates = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Registration')

  @property
  def isTestOnline(self):
    return self.starts_at < timezone.now() and self.starts_at + self.duration > timezone.now()

  @property
  def isTestAvailable(self):
    return self.starts_at > timezone.now()

  @property
  def isTestOffline(self):
    return self.starts_at + self.duration < timezone.now()

  def __str__(self):
    return self.name

  class Meta:
    ordering = [ "starts_at" ]

class Question(models.Model):
  test = models.ForeignKey(Test, on_delete = models.CASCADE, verbose_name = "Test", related_name = "questions")
  serial = models.PositiveIntegerField();
  statement = models.TextField(verbose_name = "Question Statement")
  option_1 = models.TextField(max_length = 255)
  option_2 = models.TextField(max_length = 255)
  option_3 = models.TextField(max_length = 255)
  option_4 = models.TextField(max_length = 255)
  answer = models.PositiveIntegerField();

  class Meta:
    constraints = [ models.UniqueConstraint(fields = ['serial', 'test'], name = 'unique_question_serial_per_test') ]
