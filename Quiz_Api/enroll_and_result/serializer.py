from ..models import QuizEnrollment, Quiz, QuizPlay
from User.models import User
from rest_framework import serializers
from django.conf import settings
from django.core.cache import cache
date_format = getattr(settings, 'DEFAULT_DATE_FORMAT', "%d/%m/%Y")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'phoneNumber']
        model = User

    def to_internal_value(self, data):
        errors = {}
        phone_number = data.get('phone_number')

        if phone_number:
            filtered_records = User.objects.filter(phoneNumber=phone_number).count()
            # print('filtered_record==> ', filtered_records)
            if filtered_records > 0:
                errors['phoneNumber'] = ["This number is already register."]

        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                # if key not in errors:
                errors[key] = value  # Add new keys to the errors dictionary
                # else:
                #     print(f"value==>{key} ", value)

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)
        # print("to_internal_function end.....")
        return validated_data


class QuizEnrolmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, allow_null=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, error_messages={
        'does_not_exist': "Invalid user id.",
        'incorrect_type': "Incorrect type. Expected a valid user id."
    }, allow_null=True)
    quizId = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=True, error_messages={
        'does_not_exist': "Invalid quiz id.",
        'incorrect_type': "Incorrect type. Expected a valid quiz id."
    }, source='quiz_id')


    class Meta:
        model = QuizEnrollment
        fields = ['user', 'user_id', 'quizId']
        # 'completingDate', 'score', 'timeTaken', 'correctAnswer', 'incorrectAnswer', 'pendingAnswer'

    def to_internal_value(self, data):
        errors = {}
        user_data = data.get('user')
        user_id = data.get('user_id')
        # check if user don't pass 'user' data and 'user_id'
        if user_data is None and user_id is None:
            errors['user_id'] = [f"please either provide 'user' data or 'user_id'."]

        if data:
            quiz_id = data.get('quizId')
            phone_number = user_data.get('phoneNumber') if user_data is not None else None

            # check user exist or not
            if phone_number and user_id is None:
                filtered_records = User.objects.filter(phoneNumber=phone_number)

                if len(filtered_records) > 0:
                    data['user_id'] = filtered_records[0].id
                else:
                    serializer = UserSerializer(data=user_data)
                    if serializer.is_valid():
                        user_object = serializer.save()
                        data['user_id'] = user_object.id
                    else:
                        errors['user'] = serializer.errors
            #  check user is already enrolled or not
            user_id = user_id if data['user_id'] is None else data['user_id']

            if user_id and quiz_id:
                enrolled_count = QuizEnrollment.objects.filter(quiz_id=quiz_id, user_id=user_id).count()
                if enrolled_count > 0:
                    errors['user_id'] = [f"This user has already enrolled."]
        # default validation
        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                # if key not in errors:
                errors[key] = value  # Add new keys to the errors dictionary
                # else:
                #     print(f"value==>{key} ", value)

        # raise validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)
        # print("to_internal_function end.....")
        return validated_data

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        quiz_id = validated_data.get('quiz_id')
        QuizEnrollment.objects.create(user_id=user_id, quiz_id=quiz_id, status='enroll')
        return user_id


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phoneNumber']


class QuizDetailsSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(format=date_format)
    endDate = serializers.DateField(format=date_format)
    resultDate = serializers.DateField(format=date_format)
    totalQuestions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'startDate', 'endDate', 'resultDate', 'prize', 'duration', 'totalQuestions']

    def get_totalQuestions(self, instance):
        cache_key = f"quiz_{instance.pk}_total_questions"
        # get value from cache
        total_questions = cache.get(cache_key)
        # print(f'cache value=>{cache_key}:{total_questions}')
        if total_questions is None:
            total_questions = instance.quiz_questions.filter(isActive=True).count()
            # store value in cache
            cache.set(cache_key, total_questions, timeout=30)  # Cache for 2 seconds
            # print("orm total questions=> ", total_questions)
        return total_questions


class GETAllQuizEnrolmentSerializer(serializers.ModelSerializer):
    playedDate = serializers.DateTimeField(format=date_format)
    quiz = QuizDetailsSerializer(source='quiz_id')
    user = UserDetailsSerializer(source='user_id')

    class Meta:
        model = QuizEnrollment
        fields = ['id', 'playedDate', 'score', 'timeTaken', 'correctAnswer', 'incorrectAnswer', 'pendingAnswer', 'user', 'quiz']

    def get_name(self, instance):
        return instance.user_id.name



