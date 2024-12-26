# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView


from .serializers import (
    GetResourceSerializer,
    GetResourceParamSerializer,
    CreateResourceParamSerializer,
)
from .models import Resource


class GetResourceView(APIView):

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
            resourceOutputSerializer = GetResourceSerializer(output, many=True)
            return Response(resourceOutputSerializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                resourceParamSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateResourceView(APIView):

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

        serializer = CreateResourceParamSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
