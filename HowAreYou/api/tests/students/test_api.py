"""
Test Students endpoints
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import RequestsClient, APITestCase
from rest_framework import status
from ...models import Resource, Student, StudentResponse
from django.core.management import call_command
from ...scripts.seed_db_script import seed_students_and_responses_db


class StudentsAPITests(APITestCase):
    """
    Test for Students API endpoints
    """

    BASE_URL = "http://127.0.0.1:8000/api/v1/students"

    def setUp(self) -> None:
        seed_students_and_responses_db()

    def tearDown(self) -> None:
        Student.objects.all().delete()
        StudentResponse.objects.all().delete()

    def test_get_students_valid_params_should_return_200_ok(self):
        """
        Test GET /api/v1/students
            valid params: ['agegt', 'agelt', 'age']
            valid params should return 200 OK
        """

        valid_params = [
            "?agegte=20&agelte=24&gender=m",
            "?agegte=20&agelte=24",
            "?agegte=20",
        ]

        valid_params_responses: list[int] = []

        for p in valid_params:
            response = self.client.get(f"{self.BASE_URL}{p}", format="json")
            status_code = response.status_code
            valid_params_responses.append(status_code)

        self.assertNotIn(400, valid_params_responses)

    def test_get_students_pagination(self):
        """
        Test GET /api/v1/students
            'page' param should returned paginated output
        """
        GLOBAL_PAGE_SIZE = 10

        response = self.client.get(self.BASE_URL).data

        actual_per_page_responses_size = len(response["data"])

        self.assertEqual(GLOBAL_PAGE_SIZE, actual_per_page_responses_size)

    def test_get_students_invalid_param_should_return_400_bad_request(self):
        """
        Test GET /api/v1/students
            invalid params should return 400 Bad Request
        """

        invalid_params = [
            "?agegt=20&agelte=24&gender=m",  # 'agegt' is invalid
            "?agegte=20&agelt=24",  # 'agelt' is invalid
            "?agegte=20&age=20",  # 'age' is invalid
            "gender=a&sex=f",  # 'sex' is invalid and 'gender=a' is invalid
        ]

        invalid_params_responses: list[int] = []

        for p in invalid_params:
            response = self.client.get(f"{self.BASE_URL}{p}", format="json")
            status_code = response.status_code
            invalid_params_responses.append(status_code)

        self.assertIn(400, invalid_params_responses)

    def test_create_students_valid_request_body_should_return_201_ok(self):
        """
        Test POST /api/v1/students
            valid request body should return 201 OK
        """

        valid_request_body = {
            "student": {"age": 12, "gender": "f"},
            "q1_resp": 2,
            "q2_resp": 3,
            "q3_resp": 2,
            "q4_resp": 3,
            "q5_resp": 3,
            "q6_resp": 3,
            "q7_resp": 3,
            "q8_resp": 3,
            "q9_resp": 0,
        }

        response = self.client.post(
            self.BASE_URL + "/create", valid_request_body, format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_create_students_invalid_request_body_should_return_400_bad_request(self):
        """
        Test POST /api/v1/students
            valid request body should return 400 BAD REQUEST
        """

        invalid_request_bodies = [
            {
                "student": {"age": 12, "gender": "n"},  # invalid student.gender
                "q1_resp": 2,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 11, "gender": "f"},  # invalid student.age
                "q1_resp": 2,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": -1,  # i invalid q1_resp
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": -1,  # invalid q2_resp
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": -1,  # invalid q3_resp
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": -1,  # invalid q4_resp
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": -1,  # invalid q5_resp
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": -1,  # invalid q6_resp
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": -1,  # invalid q7_resp
                "q8_resp": 3,
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 0,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": -1,  # invalid q8_resp
                "q9_resp": 0,
            },
            {
                "student": {"age": 12, "gender": "m"},
                "q1_resp": 2,
                "q2_resp": 3,
                "q3_resp": 2,
                "q4_resp": 3,
                "q5_resp": 3,
                "q6_resp": 3,
                "q7_resp": 3,
                "q8_resp": 3,
                "q9_resp": -1,  # invalid q9_resp
            },
        ]

        invalid_response_status_codes: list[int] = []

        for body in invalid_request_bodies:
            response = self.client.post(self.BASE_URL + "/create", body, format="json")
            response_status_code = response.status_code
            invalid_response_status_codes.append(response_status_code)

        self.assertNotIn(200, invalid_response_status_codes)
