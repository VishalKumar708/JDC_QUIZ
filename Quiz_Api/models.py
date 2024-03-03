from django.db import models
from utils.base_model import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    isVerified = models.BooleanField(default=False)


class Quiz(BaseModel):
    tittle = models.CharField(max_length=250)
    startDate = models.DateField()
    endDate = models.DateField()
    resultDate = models.DateField()
    prize = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    totalQuestions = models.IntegerField(default=None, null=True)
    order = models.IntegerField()
    organization = models.ForeignKey('Quiz_Api.Organization', on_delete=models.SET_NULL,
                                     related_name="organization_quiz", null=True, default=None, blank=True)
    isVerified = models.BooleanField(default=False)


class QuizQuestions(BaseModel):
    TYPE_CHOICES = [
        ("radio", "Radio"),
        ("checkbox", "Checkbox")
    ]

    quiz_id = models.ForeignKey('Quiz_Api.Quiz', on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.TextField()
    type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    level = models.CharField(max_length=100)
    # isVerified = models.BooleanField(default=True)


class QuizAnswers(BaseModel):
    quizQuestion_id = models.ForeignKey('Quiz_Api.QuizQuestions', on_delete=models.CASCADE, related_name='answers')
    option = models.TextField()
    correctOption = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    # isVerified = models.BooleanField(default=True)

# Create your models here.





