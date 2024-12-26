"""
Test responses model
"""

from django.test import TestCase
from ...models import Student, StudentResponse
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from copy import deepcopy


resp_obj = {
    "q1_resp": 2,
    "q2_resp": 2,
    "q3_resp": 2,
    "q4_resp": 2,
    "q5_resp": 2,
    "q6_resp": 2,
    "q7_resp": 2,
    "q8_resp": 2,
    "q9_resp": 2,
    "score": 2,
}


class ResponsesModelTests(TestCase):
    """
    Test for responses model
    """

    def test_create_response_should_pass(self):
        """
        Test create response record is successful
        Pass criteria:
            - foreign key of response record should be equal to primary key of student record
        """
        gender = "M"
        age = 20
        created_student = Student.objects.create(gender=gender, age=age)
        self.assertEqual(created_student.age, age)
        self.assertEqual(created_student.gender, gender)

        resp_obj_copy_1 = deepcopy(resp_obj)
        created_response = StudentResponse.objects.create(
            **resp_obj_copy_1,
            student=created_student,
        )

        self.assertEqual(created_response.student.id, created_student.id)

    def test_create_response_should_fail_response_less_than_zero(self):
        """
        Test create response record fails due to responses < 0 for any one question
        Fail criteria:
            - response to any one of the queston is less than 0
        """
        gender = "M"
        age = 20
        created_student = Student.objects.create(gender=gender, age=age)

        self.assertEqual(created_student.age, age)
        self.assertEqual(created_student.gender, gender)

        resp_obj_copy_2 = deepcopy(resp_obj)
        resp_obj_copy_2["q1_resp"] = -1
        with self.assertRaises(IntegrityError):
            StudentResponse.objects.create(**resp_obj_copy_2, student=created_student)

    def test_create_response_should_fail_score_less_than_zero(self):
        """
        Test create response record fails due to response score < 0
        Fail criteria:
            - overall score of the response is less than 0
        """

        gender = "M"
        age = 20
        created_student = Student.objects.create(gender=gender, age=age)

        self.assertEqual(created_student.age, age)
        self.assertEqual(created_student.gender, gender)

        resp_obj_copy_3 = deepcopy(resp_obj)
        resp_obj_copy_3["score"] = -27

        with self.assertRaises(IntegrityError):
            StudentResponse.objects.create(**resp_obj_copy_3, student=created_student)
