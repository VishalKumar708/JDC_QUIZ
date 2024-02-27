from django.contrib import admin
from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Organization, OrganizationAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "tittle", "startDate", "endDate", "resultDate", "prize", "duration", "totalQuestions",
                    "organization", "order"]


admin.site.register(Quiz, QuizAdmin)


class QuizQuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz_id", "question", "type", "level", "status"]


admin.site.register(QuizQuestions, QuizQuestionsAdmin)


class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "quizQuestion_id", "option", "correctOption", "status"]


admin.site.register(QuizAnswers, QuizAnswersAdmin)


# Register your models here.
