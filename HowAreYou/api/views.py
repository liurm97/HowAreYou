# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from random import randint
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .serializers import (
    ResourceModelSerializer,
    GetResourceParamSerializer,
    CreateResourceRequestBodySerializer,
    GetStudentParamSerializer,
    GetStudentResponseModelSerializer,
    CreateStudentRequestBodySerializer,
    StudentDeleteSerializer,
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

    @extend_schema(
        request=GetResourceParamSerializer,
        methods=["GET"],
        description="Return a list of all resources. Accept optional `type` parameter, values: [`video`, `article`]",
        parameters=[
            OpenApiParameter(name="type", description="Filter by type", required=False)
        ],
    )
    def get(self, request, format=None):
        """
        Return a list of all resources.
        """

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
            resources = Resource.objects.all().order_by("-created_at")
            acceptable_param = request.query_params.get("type")

            if acceptable_param:
                output = resources.filter(type=acceptable_param)
            else:
                output = resources

            resourceOutputSerializer = ResourceModelSerializer(output, many=True)
            return Response(resourceOutputSerializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                resourceParamSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(request=CreateResourceRequestBodySerializer, methods=["POST"])
class CreateResourceView(APIView):
    """
    Create new resource
    """

    def validate_postResourcesValidParams(self, data: dict):
        """
        Validate that accepted optional parameter.
        Fail if any thing other than 'type', 'url', 'csrfmiddlewaretoken'  is used.
        """
        ACCEPTABLE_PARAMS = ["type", "url", "csrfmiddlewaretoken"]
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
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    "Something wrong happened. Please try again.",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


#  ----------- Students ------------ #
@extend_schema(
    request=GetStudentParamSerializer,
    methods=["GET"],
    description="Return information and responses to questions of all students. Accept optional `gender`, `agegte`, `agelte` parameter",
    parameters=[
        OpenApiParameter(
            name="gender",
            description="Filter by gender. Accepted values: [`m`, `f`, `o`]",
            required=False,
        ),
        OpenApiParameter(
            name="agelte",
            description="Must be between 12(inclusive) and 24(inclusive). `agelte` must be greater or equal to `agegte`",
            required=False,
        ),
        OpenApiParameter(
            name="agegte",
            description="Must be between 12(inclusive) and 24(inclusive). `agegte` must be lesser or equal to `agelte`",
            required=False,
        ),
    ],
)
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


@extend_schema(request=CreateStudentRequestBodySerializer, methods=["POST"])
class CreateStudentView(APIView):
    """
    Create new student, evaluate responses to questions, and return message and resources.

    <h3>PHQ-9 questions:</h3>

    Q1: Little interest or pleasure in doing things?

    Q2: Feeling down, depressed, or hopeless?

    Q3: Trouble falling or staying asleep, or sleeping too much?

    Q4: Feeling tired or having little energy?

    Q5: Poor appetite or overeating?

    Q6: Feeling bad about yourself — or that you are a failure or have let yourself or your family down?

    Q7: Trouble concentrating on things, such as reading the newspaper or watching television?

    Q8: Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?

    Q9: Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?


    """

    def get_message(self, score: int) -> dict[str, str]:
        resources: list[str] = []

        if score >= 20:
            message = "Thanks for sharing what you are feeling. Given your current emotional state, we would ask that you seek immediate help"

        if score >= 15 and score <= 19:
            message = "Thanks for sharing what you are feeling. Given your current emotional state, we would ask that you seek active treatment with psychotherapy as soon as possible."

        if score >= 10 and score <= 14:
            message = "Thanks for sharing what you are feeling. You seem to be facing some challenges in maintaining a positive emotional state.  Having someone to talk to might be beneficial for you."

        if score >= 5 and score <= 9:
            message = "Thanks for sharing what you are feeling. You seem to be coping well. Remember to take time to relax during the day."

        if score <= 4:
            message = "Thanks for sharing what you are feeling. You seem to be coping well. Remember to take time to relax during the day."

        num_resource = len(Resource.objects.all())
        resource_ids = Resource.objects.values_list("id", flat=True)
        for i in range(3):
            random_index = randint(0, num_resource - 1)
            random_resource_id = resource_ids[random_index]

            random_url = Resource.objects.get(pk=random_resource_id).url
            random_type = Resource.objects.get(pk=random_resource_id).type
            resources.append({"url": random_url, "type": random_type})

        return {
            "message": message,
            "resources": resources,
        }

    def post(self, request, format=None):

        studentRequestBodySerializer = CreateStudentRequestBodySerializer(
            data=request.data
        )
        if studentRequestBodySerializer.is_valid():

            try:
                studentRequestBodySerializer.save()

                score = studentRequestBodySerializer.data["score"]

                message = self.get_message(score)

                return Response(
                    {
                        **message,
                        **studentRequestBodySerializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                return Response(
                    "Something wrong happened. Please try again.",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                studentRequestBodySerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class GetStudentStatisticsView(APIView):
    """
    Generate statistics of the range of depression among students and return statistics.

    <h3>Depression Score interpretation (PHQ-9):</h3>

    None-minimal: 0 - 4

    Mild: 5 - 9

    Moderate: 10 - 14

    Moderately Severe: 15 - 19

    Severe: 20 - 27
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

        statistics_output = {"category": "depression", "statistics": [categories]}

        return Response(statistics_output, status=status.HTTP_200_OK)


class DeleteStudentView(APIView):
    """
    Delete single student and response record by unique student id
    """

    def check_student_id_exists(self, student_id: str) -> bool:
        students = Student.objects.all()
        filtered_student = students.filter(id=student_id)

        if not filtered_student:
            return False

        return True

    def delete(self, request, student_id, format=None):
        student_id = {"student_id": student_id}

        serializer = StudentDeleteSerializer(data=student_id)

        if serializer.is_valid():
            validated_student_id = serializer.validated_data["student_id"]
            student_id_exists = self.check_student_id_exists(validated_student_id)

            if student_id_exists:
                try:
                    Student.objects.get(pk=validated_student_id).delete()
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                except Exception as e:
                    return Response(
                        "Something wrong happened. Please try again.",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response(
                    f"(The student id ({validated_student_id}) provided cannot be found.",
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                f"The student id ({student_id['student_id']}) provided is invalid.",
                status=status.HTTP_400_BAD_REQUEST,
            )
