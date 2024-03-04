from django.contrib import admin
from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Organization, OrganizationAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "startDate", "endDate", "resultDate", "prize", "duration", "totalQuestions",
                    "organization_id", "order", "isActive", "isVerified"]


admin.site.register(Quiz, QuizAdmin)


class QuizQuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz_id", "question", "type", "level", "isActive"]


admin.site.register(QuizQuestions, QuizQuestionsAdmin)


class QuizAnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "question_id", "option", "correctOption", "isActive"]


admin.site.register(QuizOptions, QuizAnswersAdmin)


# Register your models here.
