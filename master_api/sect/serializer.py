from rest_framework import serializers
from masterApi.models import MstSect
from accounts.models import User
from django.db.models import Q

from utils.base_serializer import BaseSerializer


class GETAllSectWithCountForResidentsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'count']

    def get_count(self, sect):
        # Calculate the count of records in the 'Saint' model based on the 'Sect' field
        return User.objects.filter(sectId=sect.id).count()


class CREATESectSerializer(BaseSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order']

    def to_internal_value(self, data):
        sectName = data.get('sectName')
        errors = {}
        if sectName:
            filtered_obj_count = MstSect.objects.filter(sectName__iexact=sectName.strip()).count()
            if filtered_obj_count > 0:
                errors['sectName'] = [f"'{sectName}' is already exist."]

        #  default validation
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


class UPDATESectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['sectName', 'order', 'isActive']

    def update(self, instance, validated_data):
        # Update the user instance with modified data
        if validated_data.get('sectName'):
            validated_data['sectName'] = validated_data['sectName'].capitalize()

        user_id_by_token = self.context.get('user_id_by_token')
        validated_data['updatedBy'] = user_id_by_token
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        sect_name = data.get('sectName')
        id = self.context.get('id')
        errors = {}
        if sect_name:
            filtered_obj_count = MstSect.objects.filter(Q(sectName__iexact=sect_name.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['sectName'] = [f"'{sect_name}' is already exist."]

        #  default validation
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

        # return super().to_internal_value(data)

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data


class GETSectDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order', 'isActive']


class GETAllSectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName', 'order']


class GETAllSectForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstSect
        fields = ['id', 'sectName']
