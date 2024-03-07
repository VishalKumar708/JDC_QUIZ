from rest_framework import serializers
from masterApi.models import MstProfession
from django.db.models import Q
from utils.base_serializer import BaseSerializer

class CREATEProfessionSerializer(BaseSerializer):
    class Meta:
        model = MstProfession
        fields = ['description', 'order']

    def to_internal_value(self, data):
        description = data.get('description')
        errors = {}
        if description:
            filtered_obj_count = MstProfession.objects.filter(description__iexact=description.strip()).count()
            if filtered_obj_count > 0:
                errors['description'] = [f"'{description}' is already exist."]

        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATEProfessionSerializer(BaseSerializer):
    class Meta:
        model = MstProfession
        fields = ['description', 'order', 'isActive']

    def to_internal_value(self, data):
        description = data.get('description')
        id = self.context.get('id')
        errors={}
        if description:
            filtered_obj_count = MstProfession.objects.filter(Q(description__iexact=description.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['description'] = [f"'{description}' is already exist."]

        validated_data = None
        try:
            # store all data in "validated_data" variable and return it
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            new_errors = e.detail.copy()  # Make a copy of the custom errors
            for key, value in new_errors.items():
                if key not in errors:
                    errors[key] = value  # Add new keys to the errors dictionary

        # return all validations errors
        if errors:
            # print('errors ==> ', errors)
            raise serializers.ValidationError(errors)

        return validated_data

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETProfessionDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description', 'order', 'isActive']


class GETAllProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description', 'order']


class GETAllProfessionForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstProfession
        fields = ['id', 'description']
