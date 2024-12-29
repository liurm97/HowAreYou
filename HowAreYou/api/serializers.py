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
    """
    Serializer to validate parameter passed into GET /api/v1/resources
    """

    type = serializers.CharField(required=False)

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


class ResourceModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Resource model
    """

    url = serializers.URLField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = Resource
        fields = ["url", "type"]


class CreateResourceRequestBodySerializer(serializers.ModelSerializer):
    """
    Serializer to validate request body passed into POST /api/v1/resources/create
    """

    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(required=True)
    url = serializers.URLField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Resource
        fields = ["id", "type", "url", "created_at", "updated_at"]

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


class GetStudentParamSerializer(serializers.Serializer):
    """
    Serializer to validate query params and value:
        1. Validate query params is in [age_gte, age_lte, gender]
        2. Validate age_gte <= age_lte and age_lte >= age_gte
        3. Validate age_gte & age_lte are between 12 (inclusive) and 24 (inclusive)
        3. Validate gender is in ['f', 'm', 'o']
    """

    agelte = serializers.IntegerField(required=False)
    agegte = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)

    def validate(self, data):

        # if gender is passed:
        if "gender" in data:
            gender_value = data["gender"]
            if gender_value not in ["f", "m", "o"]:
                raise serializers.ValidationError(
                    {
                        "error": "Value passed into 'gender' parameter is not in ['f' , 'm', 'o']"
                    }
                )

        # if agelt is passed:
        if "agelte" in data:
            agelte_value = data["agelte"]
            if agelte_value < 12 or agelte_value > 24:
                raise serializers.ValidationError(
                    {"agelte": "Value must be between 12(inclusive) and 24(inclusive)."}
                )

            ## if agegt is passed:
            if "agegte" in data:
                agegte_value = data["agegte"]

                if agelte_value < agegte_value:
                    raise serializers.ValidationError(
                        {"agegte": "Value must be smaller or equal to 'agelte'"}
                    )

        # if agegt is passed:
        if "agegte" in data:
            agegte_value = data["agegte"]

            ## if agelt is not passed:
            if agegte_value < 12 or agegte_value > 24:
                raise serializers.ValidationError(
                    {"agegte": "Value must be between 12(inclusive) and 24(inclusive)."}
                )

        return data


class StudentModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model
    """

    id = serializers.CharField(read_only=True)
    age = serializers.IntegerField()
    gender = serializers.CharField()

    class Meta:
        model = Student
        fields = ["id", "age", "gender"]

    def validate_gender(self, data):
        if data not in ["m", "f", "o"]:
            raise serializers.ValidationError("Value must be in ['f' , 'm', 'o']")
        return data

    def validate_age(self, data):
        if data < 12 or data > 24:
            raise serializers.ValidationError(
                "Value must be between 12(inclusive) and 24(inclusive)."
            )

        return data


class GetStudentResponseModelSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentResponse model
    """

    student = StudentModelSerializer(read_only=True)

    class Meta:
        model = StudentResponse
        fields = [
            "q1_resp",
            "q2_resp",
            "q3_resp",
            "q4_resp",
            "q5_resp",
            "q6_resp",
            "q7_resp",
            "q8_resp",
            "q9_resp",
            "score",
            "student",
        ]


class CreateStudentRequestBodySerializer(serializers.ModelSerializer):
    """
    Serializer to validate request body passed into POST /api/v1/students/create
    """

    created_at = serializers.DateTimeField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    q1_resp = serializers.IntegerField()
    q2_resp = serializers.IntegerField()
    q3_resp = serializers.IntegerField()
    q4_resp = serializers.IntegerField()
    q5_resp = serializers.IntegerField()
    q6_resp = serializers.IntegerField()
    q7_resp = serializers.IntegerField()
    q8_resp = serializers.IntegerField()
    q9_resp = serializers.IntegerField()

    student = StudentModelSerializer()

    class Meta:
        model = StudentResponse
        fields = [
            "q1_resp",
            "q2_resp",
            "q3_resp",
            "q4_resp",
            "q5_resp",
            "q6_resp",
            "q7_resp",
            "q8_resp",
            "q9_resp",
            "score",
            "student",
            "created_at",
        ]

    def validate_q1_resp(self, data):
        """
        Validate q1_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q2_resp(self, data):
        """
        Validate q2_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q3_resp(self, data):
        """
        Validate q3_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q4_resp(self, data):
        """
        Validate q4_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q5_resp(self, data):
        """
        Validate q5_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q6_resp(self, data):
        """
        Validate q6_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q7_resp(self, data):
        """
        Validate q7_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q8_resp(self, data):
        """
        Validate q8_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def validate_q9_resp(self, data):
        """
        Validate q9_resp must be between 0(inclusive) and 3(inclusive).
        """
        if data < 0 or data > 3:
            raise serializers.ValidationError(
                "Value must be between 0(inclusive) and 3(inclusive)."
            )
        return data

    def calculate_score(self, q_responses: list[int]):
        """
        Return sum of 9 response scores
        """
        return sum(q_responses)

    def create(self, validated_data: dict):
        q_responses: list[int] = []

        q1_resp = validated_data["q1_resp"]
        q2_resp = validated_data["q2_resp"]
        q3_resp = validated_data["q3_resp"]
        q4_resp = validated_data["q4_resp"]
        q5_resp = validated_data["q5_resp"]
        q6_resp = validated_data["q6_resp"]
        q7_resp = validated_data["q7_resp"]
        q8_resp = validated_data["q8_resp"]
        q9_resp = validated_data["q9_resp"]

        q_responses.append(q1_resp)
        q_responses.append(q2_resp)
        q_responses.append(q3_resp)
        q_responses.append(q4_resp)
        q_responses.append(q5_resp)
        q_responses.append(q6_resp)
        q_responses.append(q7_resp)
        q_responses.append(q8_resp)
        q_responses.append(q9_resp)

        age = validated_data["student"]["age"]
        gender = validated_data["student"]["gender"]
        score = self.calculate_score(q_responses)
        student_id = uuid4()

        # 1. create student
        created_student = Student.objects.create(age=age, gender=gender, id=student_id)

        # 2. create student response
        created_studentResponse = StudentResponse.objects.create(
            q1_resp=q1_resp,
            q2_resp=q2_resp,
            q3_resp=q3_resp,
            q4_resp=q4_resp,
            q5_resp=q5_resp,
            q6_resp=q6_resp,
            q7_resp=q7_resp,
            q8_resp=q8_resp,
            q9_resp=q9_resp,
            score=score,
            student=created_student,
        )

        return created_studentResponse


class StudentStatisticsModel(serializers.ModelSerializer):

    gender = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ["gender"]


class StudentResponseStatisticsModel(serializers.ModelSerializer):
    """
    Serializer for Student Response statistics model
    """

    # student = StudentStatisticsModel(read_only=True)
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudentResponse
        fields = [
            "score",
            # "student",
        ]


class StudentDeleteSerializer(serializers.Serializer):
    """
    Serializer to validate delete student
    """

    student_id = serializers.UUIDField()
