from rest_framework import serializers
from ..models import Quiz, QuizQuestions, QuizAnswers
from django.db import transaction


class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=["radio", "checkbox"])
    level = serializers.CharField()


class CreateQuestionSerializer(serializers.Serializer):
    quizId = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    question = QuestionSerializer()
    options = serializers.ListField(child=serializers.CharField())
    correct_answer = serializers.ListField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        quiz_id = data['quizId']
        question_data = data['question']
        options_data = data['options']
        correct_answers = data['correct_answer']
        errors = {}
        # custom validation

        # check a question exist only one time in a quiz
        if quiz_id and question_data.get('text'):
            print("condition working..")
            filtered_data = QuizQuestions.objects.filter(quiz_id=quiz_id, question__icontains=question_data['text'].strip()).count()
            if filtered_data > 0:
                errors['question'] = {'text': ["This question is already Added."]}

        # apply validation to add correct_answers based on question 'type'
        # if user select question 'type' =='checkbox' then he must enter at least two correct options
        if question_data.get('type') == 'checkbox' and correct_answers:
            if len(correct_answers) < 2:
                errors['options'] = [f"Please select more then one 'correct options' because you selected question 'type':'checkbox'."]
        # if user select question 'type' == 'radio' then it can add only one correct option
        elif question_data.get('type') == 'radio' and correct_answers:
            if len(correct_answers) > 1:
                errors['options'] = [f"Please select only one 'correct option' because you selected question 'type':'radio'."]

        # check user must pass at least two options
        if options_data and len(options_data) < 2:
            errors['options_data'] = ["Please add at least 2 options."]

        if correct_answers:
            # length of correct answers not more then length of options
            if len(correct_answers) > len(options_data):
                errors['correct_answer'] = [f"'correct_answer' doesn't more then 'options'."]
            else:
                # check user passes correct options or not in 'correct_answer' key
                answers = [value for index, value in enumerate(options_data) if index in correct_answers]
                if len(answers) < 1:
                    errors['correct_answer'] = [f"Please select valid option."]

        # change field into text into title case
        if question_data.get("text"):
            question_data['text'] = question_data['text'].capitalize()

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data

    def create(self, validated_data):

        # Extract data from validated_data
        quiz_id = validated_data['quizId']
        question_data = validated_data['question']
        options_data = validated_data['options']
        correct_answers = validated_data['correct_answer']

        # List to store created question instances
        question_instance = None

        # database transaction
        with (transaction.atomic()):
            try:
                # 1st step: Create QuizQuestions instance
                question_instance = QuizQuestions.objects.create(
                    quiz_id=quiz_id,
                    question=question_data['text'],
                    type=question_data['type'],
                    level=question_data['level']
                )
                # question_instances.append(question_instance.id)
                # 2 Step: match correct answer value
                options = []
                total_options = len(options_data)

                for i in range(total_options):
                    # match correct option to given options
                    if i in correct_answers:
                        options.append(
                            QuizAnswers(quizQuestion_id=question_instance, option=options_data[i], correctOption=True))
                    else:
                        options.append(QuizAnswers(quizQuestion_id=question_instance, option=options_data[i]))

                # step3: create bulk answers
                QuizAnswers.objects.bulk_create(options)
            except Exception:
                # Rollback transaction for the current question if any error occurs
                transaction.set_rollback(True)

        return question_instance


# To fetch the questions and their answers

class GETAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswers
        fields = ["id", "option", "correctOption", "isActive"]


class GETAllQuizQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestions
        fields = ["question", "answers"]

    def get_question(self, obj):
        return {
            "id": obj.id,
            "text": obj.question,
            "type": obj.type,
            "isActive": obj.isActive,
            "level": obj.level
        }

    def get_answers(self, obj):
        answers_queryset = obj.answers.all()
        serializer = GETAnswerSerializer(answers_queryset, many=True)
        return serializer.data

