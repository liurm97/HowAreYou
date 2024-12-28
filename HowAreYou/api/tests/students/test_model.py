"""
Test students model
"""

from django.test import TestCase
from ...models import Student
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class StudentModelTests(TestCase):
    """
    Test for student model
    """

    def test_create_student_should_pass(self):
        """
        Test create student record is successful
        """
        gender = "m"
        age = 20
        created_student = Student.objects.create(gender=gender, age=age)
        self.assertEqual(created_student.age, age)
        self.assertEqual(created_student.gender, gender)

    def test_create_student_should_fail_gender_constraint(self):
        """
        Test create student record fails due to incorrect gender input
        """
        gender = "Female"
        age = 20
        with self.assertRaises(IntegrityError):
            Student.objects.create(gender=gender, age=age)

    def test_create_student_should_fail_age_constraint(self):
        """
        Test create student record fails due to incorrect age input
        """
        gender = "f"
        age = 25
        with self.assertRaises(IntegrityError):
            Student.objects.create(gender=gender, age=age)
