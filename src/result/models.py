from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.test.models import Test, Question

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User', related_name='registrations')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test', related_name='candidates')
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ "-score", "created_at" ]


class Response(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name='Registration', related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    answer = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = [
        ('C', 'Correct'),
        ('W', 'Wrong'),
        ('U', 'Unanswered'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('registration', 'question')


@receiver(post_save, sender=Response)
def update_response_status_and_registration_score(sender, instance, **kwargs):
    answer = instance.answer
    question = instance.question

    if answer == question.answer:
        instance.status = 'Correct'
        post_save.disconnect(update_response_status_and_registration_score, sender=Response)
        instance.save()
        post_save.connect(update_response_status_and_registration_score, sender=Response)
        # update registration score
        registration = instance.registration
        registration.score = registration.responses.filter(status='Correct').count()
        registration.save()
        return
    elif answer == 0:
        instance.status = 'Unanswered'
    else:
        instance.status = 'Wrong'
    post_save.disconnect(update_response_status_and_registration_score, sender=Response)
    instance.save()
    post_save.connect(update_response_status_and_registration_score, sender=Response)
