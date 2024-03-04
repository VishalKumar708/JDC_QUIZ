from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Quiz, QuizQuestions, QuizAnswers
from django.db import transaction


# *********************************      To create question and their options(start)      ******************************
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
        if options_data is not None and len(options_data) < 2:
            errors['options_data'] = ["Please add at least 2 options."]

        if correct_answers is not None:
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
# *********************************      END       ******************************


# ***********************************      To get all question and answers(start)      ********************************

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
# ***********************************     END       ********************************

# *****************************************      To update the question(start)      **********************************

class UPDATEQuestionSerializer(serializers.ModelSerializer):
    quiz_id = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=False,
                                                 error_messages={
                                                     'does_not_exist': "Invalid quiz_id",
                                                     'incorrect_type': "Incorrect type. Expected a valid quiz_id."
                                                 }
                                                 )
    question = serializers.CharField(required=False)
    level = serializers.CharField(required=False)
    isActive = serializers.BooleanField(required=False)

    class Meta:
        model = QuizQuestions
        fields = ["quiz_id", "question", "level", "isActive"]

    def to_internal_value(self, data):
        quiz_id = data.get('quiz_id')
        question_data = data.get('question')
        errors = {}

        if quiz_id is not None and question_data and 'text' in question_data:
            filtered_data = QuizQuestions.objects.filter(quiz_id=quiz_id,
                                                         question__icontains=question_data['text'].strip()).count()
            if filtered_data > 0:
                errors['question'] = {'text': ["This question is already added."]}

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

        # raise validation errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data
# *****************************************      END     ************************************

# *****************************************      To update the answers(start)      ************************************


class UPDATEAnswerSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)
    option = serializers.CharField(required=False)

    class Meta:
        fields = ["option", "isActive", "order"]
        model = QuizAnswers

    def to_internal_value(self, data):
        option_text = data.get('option')
        errors = {}
        if option_text:

            filtered_data = QuizAnswers.objects.filter(~Q(id=self.context.get('answer_id')), Q(option__iexact=option_text.strip(), quizQuestion_id=self.context.get('question_id'))).count()
            # print("filtered_data => ", filtered_data)
            if filtered_data > 0:
                errors['options'] = [f"This option is already exist."]

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

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # change the question type
        # Get the associated QuizQuestions instance
        question_instance = instance.quizQuestion_id
        # check no. of options are correct
        filtered_data = QuizAnswers.objects.filter(quizQuestion_id=instance.quizQuestion_id.id,
                                                   correctOption=True).count()
        if filtered_data >= 2:
            question_instance.type = 'checkbox'
        elif filtered_data == 1:
            question_instance.type = 'radio'
        question_instance.save()  # Save the modified instance to update the 'type' field
        return instance


class CREATEAnswerSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=QuizQuestions.objects.all(),
                                            source='quizQuestion_id',
                                            error_messages={
                                                'does_not_exist': "Invalid question id.",
                                                'incorrect_type': "Incorrect type. Expected a valid question id."
                                            }
                                            )
    option = serializers.CharField(required=True)
    isActive = serializers.BooleanField()
    correctOption = serializers.BooleanField(default=False)

    class Meta:
        fields = ['id', 'option', "isActive", "correctOption", "order"]
        model = QuizAnswers

    def to_internal_value(self, data):
        question_id = data.get('quizQuestion_id')
        option = data.get('option')
        errors = {}
        if option:
            filtered_data_count = QuizAnswers.objects.filter(quizQuestion_id=question_id, option__iexact=option.strip()).count()
            if filtered_data_count > 0:
                errors['option'] = [f"This option is already exist."]

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
        instance = QuizAnswers.objects.create(**validated_data)
        # check no. of options are correct
        filtered_data = QuizAnswers.objects.filter(quizQuestion_id=instance.quizQuestion_id.id, correctOption=True).count()
        # Get the associated QuizQuestions instance
        question_instance = instance.quizQuestion_id

        if filtered_data >= 2:
            question_instance.type = 'checkbox'
        elif filtered_data == 1:
            question_instance.type = 'radio'
        question_instance.save()  # Save the modified instance to update the 'type' field
        return instance

# *****************************************      END       ************************************
