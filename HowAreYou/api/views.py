# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg, Sum
from django.db import connection


from .serializers import (
    ResourceModelSerializer,
    GetResourceParamSerializer,
    CreateResourceRequestBodySerializer,
    GetStudentParamSerializer,
    GetStudentResponseModelSerializer,
    CreateStudentRequestBodySerializer,
    StudentModelSerializer,
    StudentResponseStatisticsModel,
)
from .models import Resource, Student, StudentResponse


#  ----------- Resource ------------ #
class GetResourceView(APIView):
    """
    View to get resources
    """

    def validate_getResourcesParamHasOnlyType(self, queryDict):
        """
        Validate that 'type' is the only accepted optional parameter.
        Fail if any thing other than 'type' is used.
        """
        ACCEPTABLE_PARAMS = ["type"]
        provided_param_keys = queryDict.keys()
        unacceptable_params = []

        for provided_param_key in provided_param_keys:
            if provided_param_key not in ACCEPTABLE_PARAMS:
                unacceptable_params.append(provided_param_key)

        if len(unacceptable_params) > 0:
            return unacceptable_params, False

        return None, True

    def validate_getResourcesTypeParamHasOnlyOneValue(self, queryDict):
        """
        Validate that only one acceptable value {article, video} is allowed to be passed into the 'type' parameter.

        Fail if more than one acceptable value is passed in. Eg: /resources?type=article&type=video
        """
        typeValues = queryDict.getlist("type")

        if len(typeValues) > 1:
            return False
        return True

    def get(self, request, format=None):
        """
        Return a list of all resources.
        """

        print("----- start ------")
        unaccepted_params, isOnlyTypeParamValidated = (
            self.validate_getResourcesParamHasOnlyType(request.query_params)
        )

        isTypeParamValueValidated = self.validate_getResourcesTypeParamHasOnlyOneValue(
            request.query_params
        )

        #  Validate that 'type' is the only accepted optional parameter.
        if not isOnlyTypeParamValidated:
            return Response(
                {
                    "error": f"You have passed in invalid parameter: ({', '.join(unaccepted_params)})"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        #   Validate that only one acceptable value {article, video} is allowed to be passed into the 'type' parameter
        if not isTypeParamValueValidated:
            return Response(
                {
                    "error": f"You have passed more than one acceptable values: ({', '.join(list(request.query_params.getlist('type')))})"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate that value passed into 'type' param is in {article, video}
        resourceParamSerializer = GetResourceParamSerializer(data=request.query_params)

        # Check value passed to 'type' field is either 'article' or 'video'
        if resourceParamSerializer.is_valid():
            resources = Resource.objects.all()
            acceptable_param = request.query_params.get("type")

            if acceptable_param:
                output = resources.filter(type=acceptable_param)
            else:
                output = resources

            print(f"output:: {output}")
            resourceOutputSerializer = ResourceModelSerializer(output, many=True)
            return Response(resourceOutputSerializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                resourceParamSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateResourceView(APIView):
    """
    View to create resources
    """

    def validate_postResourcesValidParams(self, data: dict):
        """
        Validate that 'type' is the only accepted optional parameter.
        Fail if any thing other than 'type' is used.
        """
        ACCEPTABLE_PARAMS = ["type", "url"]
        provided_param_keys: list[str] = list(data.keys())
        unacceptable_params = []

        for provided_param_key in provided_param_keys:
            if provided_param_key not in ACCEPTABLE_PARAMS:
                unacceptable_params.append(provided_param_key)

        if len(unacceptable_params) > 0:
            return unacceptable_params, False, "Invalid Params"

        return None, True, None

    def post(self, request, format=None):
        unaccepted_params, isValidParams, resourceValidParamsReason = (
            self.validate_postResourcesValidParams(request.data)
        )

        if not isValidParams:
            return JsonResponse(
                {
                    "message": f"You have passed in invalid field: ({', '.join(unaccepted_params)})",
                    "reason": resourceValidParamsReason,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CreateResourceRequestBodySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


#  ----------- Students ------------ #
class GetStudentView(APIView, PageNumberPagination):
    """
    View to get student and response
    """

    def validate_getStudentsAllowedParams(self, queryDict):
        """
        validate allowed optional params are in ['agelte', 'agegte', 'gender', 'page']
        """
        unacceptable_params = []
        allowed_params = ["agelte", "agegte", "gender", "page"]
        params = queryDict.keys()

        for p in params:
            if p not in allowed_params:
                unacceptable_params.append(p)

        if len(unacceptable_params) > 0:
            return False, unacceptable_params

        return True, None

    def return_filtered_data(self, validated_data, studentResponses):
        ## if agelt, agegt, gender are present
        if (
            "agelte" in validated_data
            and "agegte" in validated_data
            and "gender" in validated_data
        ):
            filtered = studentResponses.filter(
                student__age__gte=validated_data["agegte"],
                student__age__lte=validated_data["agelte"],
                student__gender=validated_data["gender"],
            )

        ## if agelt, agegt are present
        elif "agelte" in validated_data and "agegte" in validated_data:
            filtered = studentResponses.filter(
                student__age__gte=validated_data["agegte"],
                student__age__lte=validated_data["agelte"],
            )

        ## if agelt, gender are present
        elif "agelte" in validated_data and "gender" in validated_data:
            filtered = studentResponses.filter(
                student__gender=validated_data["gender"],
                student__age__lte=validated_data["agelte"],
            )

        ## if agegt, gender are present
        elif "agegte" in validated_data and "gender" in validated_data:
            filtered = studentResponses.filter(
                student__gender=validated_data["gender"],
                student__age__gte=validated_data["agegte"],
            )

        ## if only agelt is present
        elif "agelte" in validated_data:
            filtered = studentResponses.filter(
                student__age__lte=validated_data["agelte"],
            )

        ## if only agegt is present
        elif "agegte" in validated_data:
            filtered = studentResponses.filter(
                student__age__gte=validated_data["agegte"],
            )

        ## if only gender is present
        elif "gender" in validated_data:
            filtered = studentResponses.filter(
                student__gender=validated_data["gender"],
            )

        return filtered

    def get(self, request, format=None):
        """
        Get student and student response records.
        Allowed optional parameters: [age_gte, age_lte, gender, page]
        Eg: http://127.0.0.1:8000/api/v1/students?agegte=14&agelte=14&gender=m&page=2
        """
        # 1. validate query params is in [age_gt, age_lt, gender]
        query_params = request.query_params

        isParamValid, unaccepted_params = self.validate_getStudentsAllowedParams(
            query_params
        )

        if not isParamValid:
            return Response(
                {
                    "error": f"You have passed in invalid parameter: ({', '.join(unaccepted_params)})"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:

            getstudentParamSerializer = GetStudentParamSerializer(data=query_params)

            if getstudentParamSerializer.is_valid():
                validated_data = getstudentParamSerializer.validated_data

                studentResponses = StudentResponse.objects.all()

                # if no param is passed in
                # or if 'page' is the only param
                # return unfiltered responses
                if len(query_params.keys()) == 0 or (
                    len(query_params.keys()) == 1 and "page" in query_params.keys()
                ):
                    results = self.paginate_queryset(
                        studentResponses, request, view=self
                    )

                # if any one of accepted param is passed in
                # return filtered responses
                elif len(query_params.keys()) > 0:
                    filtered_studentResponses = self.return_filtered_data(
                        validated_data, studentResponses
                    )

                    results = self.paginate_queryset(
                        filtered_studentResponses, request, view=self
                    )

                serializer = GetStudentResponseModelSerializer(results, many=True)

                return Response(
                    {
                        "data": serializer.data,
                        "links": {
                            "next": self.get_next_link(),
                            "previous": self.get_previous_link(),
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(getstudentParamSerializer.errors)


class CreateStudentView(APIView):
    """
    View to create student and response
    """

    def post(self, request, format=None):

        studentRequestBodySerializer = CreateStudentRequestBodySerializer(
            data=request.data
        )
        if studentRequestBodySerializer.is_valid():
            created_student = studentRequestBodySerializer.save()
            # print(f"created_student:: {created_student['score']}")
            print(
                f"studentRequestBodySerializer.student:: {studentRequestBodySerializer['score']}"
            )
            print(f"created_student:: {created_student}")
            return Response(
                studentRequestBodySerializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                studentRequestBodySerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class GetStudentStatisticsView(APIView):
    """
    View to generate statistics of the range of depression among students

    Score interpretation:
        > 0 - 4: None-minimal
        > 5 - 9: Mild
        > 10 - 14: Moderate
        > 15 - 19: Moderately Severe
        > 20 - 27: Severe
    """

    def get(self, request, format=None):
        categories = {
            "None - Minimal": {},
            "Mild": {},
            "Moderate": {},
            "Moderately Severe": {},
            "Severe": {},
        }

        gender_mapping = {"m": "Male", "f": "Female", "o": "Others"}
        print(f"StudentResponse.objects.all()::: {len(StudentResponse.objects.all())}")

        for o in StudentResponse.objects.all():
            gender = o.student.gender  # m, f, o
            score = o.score
            if score >= 20:
                if gender_mapping[gender] not in categories["Severe"]:
                    categories["Severe"][gender_mapping[gender]] = 1
                else:
                    categories["Severe"][gender_mapping[gender]] += 1

            if score >= 15 and score <= 19:
                if gender_mapping[gender] not in categories["Moderately Severe"]:
                    categories["Moderately Severe"][gender_mapping[gender]] = 1
                else:
                    categories["Moderately Severe"][gender_mapping[gender]] += 1

            if score >= 10 and score <= 14:
                if gender_mapping[gender] not in categories["Moderate"]:
                    categories["Moderate"][gender_mapping[gender]] = 1
                else:
                    categories["Moderate"][gender_mapping[gender]] += 1

            if score >= 5 and score <= 9:
                if gender_mapping[gender] not in categories["Mild"]:
                    categories["Mild"][gender_mapping[gender]] = 1
                else:
                    categories["Mild"][gender_mapping[gender]] += 1

            if score <= 4:
                if gender_mapping[gender] not in categories["None - Minimal"]:
                    categories["None - Minimal"][gender_mapping[gender]] = 1
                else:
                    categories["None - Minimal"][gender_mapping[gender]] += 1

        print(f"categories:: {categories}")

        statistics_output = {"category": "depression", "statistics": [categories]}

        return Response(statistics_output, status=status.HTTP_200_OK)


class DeleteStudentView(APIView):
    pass
