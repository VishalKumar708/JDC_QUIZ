from django.db import models
from utils.base_model import BaseModel
from django.utils import timezone


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    isVerified = models.BooleanField(default=False)


class Quiz(BaseModel):
    title = models.CharField(max_length=250)
    startDate = models.DateField()
    endDate = models.DateField()
    resultDate = models.DateField()
    prize = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    totalQuestions = models.IntegerField(default=None, null=True)
    order = models.IntegerField()
    organization_id = models.ForeignKey('Quiz_Api.Organization', on_delete=models.SET_NULL,
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


class QuizOptions(BaseModel):
    question_id = models.ForeignKey('Quiz_Api.QuizQuestions', on_delete=models.CASCADE, related_name='options')
    option = models.TextField()
    correctOption = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    # isVerified = models.BooleanField(default=True)


class QuizEnrollment(BaseModel):
    STATUS_CHOICES = (
        ('enroll', "Enroll"),
        # ('pending', "Pending"),
        ('start', "Start"),
        ('complete', "Complete"),
        # ('expire', "Expire"),
    )
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='quiz_enrollments')
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='enrollments')
    enrollmentDate = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    completingDate = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    timeTaken = models.IntegerField(default=0)
    correctAnswer = models.IntegerField(default=0)
    incorrectAnswer = models.IntegerField(default=0)
    pendingAnswer = models.IntegerField(default=0)


# Create your models here.





