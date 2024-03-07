from rest_framework import serializers


from ...models import QuizQuestions, QuizOptions

from django.db.models import Q


class UPDATEQuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, source='question')
    level = serializers.CharField(required=False)
    isActive = serializers.BooleanField(required=False)

    class Meta:
        model = QuizQuestions
        fields = ["text", "level", "isActive"]

    def to_internal_value(self, data):
        quiz_id = self.context.get('quiz_id')
        question_id = self.context.get('question_id')
        question_text = data.get('text')

        errors = {}
        # print("quiz_id=> ", quiz_id)
        # print("question_id=> ", question_id)
        # print("question_text=> ", question_text)

        if quiz_id is not None and question_text:
            filtered_data = QuizQuestions.objects.filter(Q(question__icontains=question_text.strip(), quiz_id=quiz_id), ~Q(id=question_id)).count()
            if filtered_data > 0:
                errors['text'] = ["This question is already added."]

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



class UPDATEOptionSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)
    option = serializers.CharField(required=False)
    correctOption = serializers.BooleanField(required=False)

    class Meta:
        fields = ["option", "isActive", "order", "correctOption"]
        model = QuizOptions

    def to_internal_value(self, data):
        option_text = data.get('option')
        errors = {}
        if option_text:
            filtered_data = QuizOptions.objects.filter(~Q(id=self.context.get('answer_id')), Q(option__iexact=option_text.strip(), question_id=self.context.get('question_id'))).count()
            # print("filtered_data => ", filtered_data)
            if filtered_data > 0:
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

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # change the question type
        # Get the associated QuizQuestions instance
        question_instance = instance.question_id
        # check no. of options are correct
        filtered_data = QuizOptions.objects.filter(question_id=instance.question_id.id,
                                                   correctOption=True).count()
        if filtered_data >= 2:
            question_instance.type = 'checkbox'
        elif filtered_data == 1:
            question_instance.type = 'radio'
        question_instance.save()  # Save the modified instance to update the 'type' field
        return instance
