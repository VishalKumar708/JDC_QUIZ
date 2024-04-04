from django.db import connection
from rest_framework import serializers


from ...models import QuizQuestions, QuizOptions


class GETAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOptions
        fields = ["id", "option", "correctOption", "isActive", "order"]

    # def to_representation(self, instance):
    #     # Before serializing each instance, we can check the number of queries
    #     print("Number of queries before serialization(option):", len(connection.queries))
    #     # Proceed with serialization
    #     return super().to_representation(instance)

class GETQuestionSerializer(serializers.ModelSerializer):
    # text = serializers.CharField(source='question')

    class Meta:
        model = QuizQuestions
        fields = ['id',  'type', 'isActive', 'level']
        # fields = '__all__'


class GETAllQuizQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    # options = serializers.SerializerMethodField()
    options = GETAnswerSerializer(many=True)
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestions
        fields = ["question", "options", "correct_answer"]

    def get_question(self, obj):

        return {
            "id": obj.id,
            "text": obj.question,
            "type": obj.type,
            "isActive": obj.isActive,
            "level": obj.level,
        }

    def get_correct_answer(self, obj):

        result = obj.options.filter(correctOption=True).values_list('id', flat=True) #using database therefore no.of quires increase
        # result = [option.id for option in obj.options.all() if option.correctOption]
        # print("Number of queries before serialization(Quiz_question) in correct_answer:", len(connection.queries))
        return result



    # def to_representation(self, instance):
    #     # Before serializing each instance, we can check the number of queries
    #     print("Number of queries before serialization(Quiz_question):", len(connection.queries))
    #     # Proceed with serialization
    #     return super().to_representation(instance)
#  Get all questions


class GETAllQuizQuestionsByQuizIdAndUserIdSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    correct_answer = serializers.SerializerMethodField()
    selected_option = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestions
        fields = ["question", "options", "correct_answer", "selected_option"]

    def get_question(self, obj):
        return {
            "id": obj.id,
            "text": obj.question,
            "type": obj.type,
            "isActive": obj.isActive,
            "level": obj.level,
        }

    def get_options(self, obj):
        options_queryset = obj.options.all()
        serializer = GETAnswerSerializer(options_queryset, many=True)
        return serializer.data

    def get_correct_answer(self, obj):
        correctOptions_queryset = obj.options.filter(correctOption=True).values_list('id', flat=True)
        return correctOptions_queryset

    def get_selected_option(self, obj):
        selected_options = obj.quiz_plays.filter(userId=self.context.get('user_id'), quizId=self.context.get('quiz_id')).values_list('answerId', flat=True)
        if selected_options:
            return selected_options
        else:
            return []
    # def get_selected_option(self, obj):
    #     # selected_options = obj.quiz_plays.all().values_list('answerId__id', flat=True)
    #     # if selected_options:
    #     #     return selected_options
    #     return obj.quiz_plays.user_answers_id

    # def to_representation(self, instance):
    #     # Before serializing each instance, we can check the number of queries
    #     print("Number of queries before serialization:", len(connection.queries))
    #     # Proceed with serialization
    #     return super().to_representation(instance)
