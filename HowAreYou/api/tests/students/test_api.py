"""
Test Students endpoints
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import RequestsClient, APITestCase
from rest_framework import status
from ...models import Resource, Student, StudentResponse
from django.core.management import call_command
from ...scripts.seed_db_script import seed_students_and_responses_db, seed_resources_db


class StudentsAPITests(APITestCase):
    """
    Test for Students API endpoints
    """

    BASE_URL = "http://127.0.0.1:8000/api/v1/students"

    def setUp(self) -> None:
        seed_students_and_responses_db()
        seed_resources_db()

    def tearDown(self) -> None:
        Student.objects.all().delete()
        StudentResponse.objects.all().delete()
        Resource.objects.all().delete()

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

    def test_create_students_valid_request_body_should_return_score_evaluation_message(
        self,
    ):
        """
        Test POST /api/v1/students
            Evaluation message should be returned on successful student creation
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
        expected_message = response.data["message"]

        self.assertNotEqual("", expected_message)

    def test_create_students_valid_request_body_should_return_3_resources(self):
        """
        Test POST /api/v1/students
            Successful student creation should return links to 3 resource urls
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
        expected_resource_length = len(response.data["resources"])

        self.assertEqual(3, expected_resource_length)

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

    def test_get_student_statistics_return_correct_total_students(self):
        """
        Test GET /api/v1/students/stats
            The sum of students should be equal to the total number of students
        """

        expected_total_students = len(Student.objects.all())

        response = self.client.get(self.BASE_URL + "/stats", format="json")
        response_data = response.data

        statistics = response_data["statistics"]

        actual_student_counter = 0

        for s in statistics:
            for k, v in s.items():
                for _k, _v in v.items():
                    actual_student_counter += _v
        self.assertEqual(actual_student_counter, expected_total_students)

    def test_delete_students_valid_student_id_should_return_204_no_content(self):
        """
        Test DELETE /api/v1/students/<student_id>
            valid student id should be deleted and returned 204
        """
        valid_student_id = Student.objects.first().id

        response = self.client.delete(
            f"{self.BASE_URL}/delete/{valid_student_id}", format="json"
        )

        response_status_code = response.status_code

        self.assertEqual(response_status_code, 204)

    def test_delete_students_invalid_UUID_student_id_should_return_400_bad_request(
        self,
    ):
        """
        Test DELETE /api/v1/students/<student_id>
            student id that is not in UUID format should return 400
        """

        invalid_student_id = ["123", 123]

        response_status_codes: list[int] = []

        for id in invalid_student_id:
            response = self.client.delete(f"{self.BASE_URL}/delete/{id}", format="json")
            response_status_code = response.status_code
            response_status_codes.append(response_status_code)

        self.assertEqual([400, 400], response_status_codes)

    def test_delete_students_not_found_student_id_should_return_404_not_found(self):
        """
        Test DELETE /api/v1/students/<student_id>
            student id that is not found in db should return 404
        """
        from uuid import uuid4

        random_student_id = uuid4()

        response = self.client.delete(
            f"{self.BASE_URL}/delete/{random_student_id}", format="json"
        )

        response_status_code = response.status_code

        self.assertEqual(response_status_code, 404)
