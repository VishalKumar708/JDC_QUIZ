from rest_framework import serializers
from masterApi.models import MstRelation
from django.db.models import Q

from utils.base_serializer import BaseSerializer


class CREATERelationSerializer(BaseSerializer):
    class Meta:
        model = MstRelation
        fields = ['description', 'order']

    def to_internal_value(self, data):
        description = data.get('description')
        errors = {}
        if description:
            filtered_obj_count = MstRelation.objects.filter(description__iexact=description.strip()).count()
            if filtered_obj_count > 0:
                errors['description'] = [f"'{description}' is already exist."]

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

        # return all validations errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data


class UPDATERelationSerializer(BaseSerializer):
    class Meta:
        model = MstRelation
        fields = ['description', 'order', 'isActive']

    def to_internal_value(self, data):
        description = data.get('description')
        id = self.context.get('id')
        errors = {}
        if description:
            filtered_obj_count = MstRelation.objects.filter(Q(description__iexact=description.strip()),
                                                              ~Q(id=id)).count()
            if filtered_obj_count > 0:
                errors['description'] = [f"'{description}' is already exist."]

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

        # return all validations errors
        if errors:
            raise serializers.ValidationError(errors)

        return validated_data

    def validate(self, data):
        # Check if at least one field is being updated
        updated_fields = {key: value for key, value in data.items() if key in self.Meta.fields}
        if len(updated_fields) == 0:
            raise serializers.ValidationError({"update_validation_error": ["At least one field must be provided for the update."]})
        return data

class GETRelationDetailsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description', 'order', 'isActive']


class GETAllRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description', 'order']


class GETAllRelationForDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = MstRelation
        fields = ['id', 'description']
