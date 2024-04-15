from django.contrib import admin
from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Organization, OrganizationAdmin)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "startDate", "endDate", "resultDate", "prize", "duration",
                    "organization_id", "order", "isActive", "isVerified"]
    # list_max_show_all = 100000000
    list_filter = ['startDate', 'endDate', 'resultDate', 'isActive', 'isVerified']
    search_fields = ['title']


@admin.register(QuizQuestions)
class QuizQuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz_id", "question", "type", "level", "isActive"]
    list_filter = ['quiz_id', "type", "level", "isActive"]




@admin.register(QuizOptions)
class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "question_id", "option", "correctOption", "isActive"]
    list_filter = ['question_id', "isActive", "correctOption"]



@admin.register(QuizEnrollment)
class QuizEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'quiz_id', 'enrollmentDate', 'status', 'playedDate', 'timeTaken',
                     'correctAnswer', 'incorrectAnswer', 'pendingAnswer']
    list_filter = ['user_id', 'quiz_id', 'correctAnswer', 'incorrectAnswer', 'pendingAnswer']




@admin.register(QuizPlay)
class QuizPlayAdmin(admin.ModelAdmin):
    list_display = ["id", "userId", "quizId", "questionId", "answerId", "get_correct_option"]
    list_filter = ['userId', 'quizId', 'questionId']

    def get_correct_option(self, obj):
        return obj.answerId.correctOption

    get_correct_option.short_description = "isCorrect"




