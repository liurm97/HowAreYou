"""
Test Resources endpoint
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import RequestsClient, APITestCase
from rest_framework import status
from ...models import Resource, Student, StudentResponse
from django.core.management import call_command
from ...scripts.seed_db_script import seed_resources_db


class ResourceAPITests(APITestCase):
    """
    Test for Resources API endpoints
    """

    BASE_URL = "http://127.0.0.1:8000/api/v1/resources"

    def setUp(self) -> None:
        seed_resources_db()

    def tearDown(self) -> None:
        Resource.objects.all().delete()

    def test_get_resources_no_params_should_return_all_output(self):
        """
        Test GET api/v1/resources
            should return article and video resources
        """
        expected_resources_records = len(Resource.objects.all())

        response = self.client.get(self.BASE_URL, format="json")

        self.assertEqual(expected_resources_records, len(response.data))

    def test_get_resources_type_param_should_return_filtered_output(self):
        """
        Test GET api/v1/resources?type={article, video}
            should return filtered resources
        """

        type_value = "article"

        expected_filtered_records = len(Resource.objects.all().filter(type=type_value))

        response = self.client.get(self.BASE_URL + f"?type={type_value}", format="json")

        self.assertEqual(expected_filtered_records, len(response.data))

    def test_get_resources_unacceptable_param_should_return_400(self):
        """
        Test GET api/v1/resources
            unacceptable params should return 400 status code
        """

        invalid_requests = [
            self.BASE_URL + "?type=artic",  # invalid value
            self.BASE_URL + "?type=vide",  # invalid value
            self.BASE_URL + "?type=article&type=video",  # more than one 'type' params
            self.BASE_URL + "?type=artic&typ=article",  # invalid param
            self.BASE_URL + "?type=artic&typ=video",  # invalid param
        ]

        resp_status_codes = []

        for invalid_r in invalid_requests:
            resp_status_code: int = self.client.get(invalid_r).status_code
            resp_status_codes.append(resp_status_code)

        self.assertNotIn(200, resp_status_codes)

    def test_create_resources_with_valid_body_should_return_201_created(self):
        """
        Test POST api/v1/resources
            valid request body should create resources successfully and
            return 201 status code
        """
        valid_request_body = {"type": "article", "url": "https://www.mindline.sg"}
        created_resource_status_code = self.client.post(
            self.BASE_URL + "/create", data=valid_request_body
        ).status_code

        self.assertEqual(created_resource_status_code, 201)

    def test_create_resources_with_invalid_url_format_should_return_400_bad_request(
        self,
    ):
        """
        Test POST api/v1/resources
            invalid formatted value passed to 'url' field should return 400 status code
        """
        invalid_url_values = [
            "www.com",
            "www.",
            "w",
            "htt://ww.google.com",
            "ht://www.google.com",
        ]

        resp_status_codes = []

        for invalid_url in invalid_url_values:
            resp_status_code: int = self.client.post(
                self.BASE_URL + "/create", data={"url": invalid_url, type: "article"}
            ).status_code
            resp_status_codes.append(resp_status_code)

        self.assertNotIn(200, resp_status_codes)

    def test_create_resources_with_inactive_url_should_return_400_bad_request(self):
        """
        Test POST api/v1/resources
            value passed to 'url' field that does not return 200
        should return 400 status code
        """
        invalid_url_values = [
            "https://www.g.com",
            "https://www.g3.com",
            "https://www.mindline.com.sg",
        ]

        resp_status_codes = []

        for invalid_url in invalid_url_values:
            resp_status_code: int = self.client.post(
                self.BASE_URL + "/create", data={"url": invalid_url, type: "article"}
            ).status_code
            resp_status_codes.append(resp_status_code)

        self.assertNotIn(200, resp_status_codes)

    def test_create_resources_with_duplicate_url_value_should_return_400_bad_request(
        self,
    ):
        """
        Test POST api/v1/resources
            value passsed to 'url' field that is a duplicate
            should return 400 status code
        """
        existing_url_in_db = Resource.objects.first().url

        resp_status_code: int = self.client.post(
            self.BASE_URL + "/create", data={"url": existing_url_in_db, type: "article"}
        ).status_code

        self.assertEqual(resp_status_code, 400)

    def test_create_resources_with_invalid_type_value_should_return_400_bad_request(
        self,
    ):
        """
        Test api/v1/resources
            value passsed to 'type' field that is invalid
            should return 400 status code
        """
        invalid_type_requests = [
            {"url": "https://www.mindline.com", "type": "articl"},
            {"url": "https://www.mindline.sg", "type": "vidoe"},
        ]

        resp_status_codes = []

        for invalid_type_request in invalid_type_requests:
            resp_status_code: int = self.client.post(
                self.BASE_URL + "/create", data=invalid_type_request
            ).status_code
            resp_status_codes.append(resp_status_code)

        self.assertNotIn(200, resp_status_codes)
