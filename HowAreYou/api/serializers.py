"""
Serializer for API
"""

from rest_framework import serializers
from .models import Student, StudentResponse, Resource
from datetime import datetime
from uuid import uuid4
from rest_framework.exceptions import ValidationError
import requests as re
import os


class GetResourceParamSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)

    def validate_type(self, data):
        """
        Validate that value passed into 'type' param is in {article, video}
        """

        print(f"GetResourceParamSerializer - validate_type - {data}")
        if data not in ["article", "video"]:
            raise serializers.ValidationError(
                {
                    "error": "Value passed into 'type' parameter is not in ['article', 'video']"
                }
            )

        return data


class GetResourceSerializer(serializers.ModelSerializer):
    """
    Serializer for Resource model
    """

    url = serializers.URLField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = Resource
        fields = ["url", "type"]


class CreateResourceParamSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(required=True)
    url = serializers.URLField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def check_url_is_valid(self, url: str):
        """
        Check url is valid and a valid response is returned within 2.5s
        """
        try:
            status_code = re.get(url=url, timeout=2.5).status_code
            if status_code != 200:
                return False, "url is invalid"
        except Exception:
            return False, "url is invalid"
        return url, None

    def check_url_is_duplicate(self, urlToCheck: str):
        """
        Check url does not already exists in db
        """
        existing_url = Resource.objects.all().filter(url=urlToCheck)
        if existing_url:
            return True
        return False

    class Meta:
        model = Resource
        fields = [
            "url",
            "type",
        ]

    def validate_type(self, data):
        """
        Validate that value passed into 'type' param is in {article, video}
        """
        if data not in ["article", "video"]:
            raise serializers.ValidationError(
                {
                    "error": "Value passed into 'type' parameter is not in ['article', 'video']"
                }
            )
        return data

    def validate_url(self, data):
        """
        Validate url is both valid and not a duplicate
        """
        url = data
        isUrlValid = self.check_url_is_valid(data)
        isUrlDuplicate = self.check_url_is_duplicate(data)

        if not isUrlValid:
            raise serializers.ValidationError(
                {"error": "You have provided an invalid url."}
            )

        if isUrlDuplicate:
            raise serializers.ValidationError(
                {"error": "You have provided a duplicate url."}
            )

        return url

    def create(self, validated_data):
        """
        Create record in db
        """
        url = validated_data["url"]
        type = validated_data["type"]

        created_resource = Resource.objects.create(url=url, type=type)
        return created_resource
