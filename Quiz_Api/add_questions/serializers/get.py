from rest_framework import serializers


from ...models import QuizQuestions, QuizOptions


class GETAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOptions
        fields = ["id", "option", "correctOption", "isActive", "order"]


class GETAllQuizQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
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

    def get_options(self, obj):
        options_queryset = obj.options.all()
        serializer = GETAnswerSerializer(options_queryset, many=True)
        return serializer.data

    def get_correct_answer(self, obj):
        correctOptions_queryset = obj.options.filter(correctOption=True).values('id')
        result = [option['id'] for option in correctOptions_queryset]
        return result

