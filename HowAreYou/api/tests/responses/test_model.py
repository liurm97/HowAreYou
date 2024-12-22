# """
# Test responses model
# """

# from django.test import TestCase
# from ...models import responses, students
# from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError

# class ResponsesModelTests(TestCase):
#   """
#   Test for responses model
#   """
#   def test_create_student_should_pass(self):
#     """
#     Test create student record is successful
#     """
#     gender = "M"
#     age = 20
#     created_student = students.objects.create(
#       gender=gender,
#       age=age
#     )
#     self.assertEqual(created_student.age, age)
#     self.assertEqual(created_student.gender, gender)

#     created_response = responses.objects.create(
#        q1_resp = 3,
#        q2_resp = 3,
#        q3_resp = 3,
#        q4_resp = 3,
#        q5_resp = 3,
#        q6_resp = 3,
#        q7_resp = 3,
#        q8_resp = 3,
#        q9_resp = 3,
#        score = 27,
#        student=created_student)

#     self.assertEqual(
       
#     )

#   # def test_create_student_should_fail_gender_constraint(self):
#   #   """
#   #   Test create student record fails due to incorrect gender input
#   #   """
#   #   gender = "Female"
#   #   age = 20
#   #   with self.assertRaises(IntegrityError):
#   #       students.objects.create(
#   #          gender=gender,
#   #          age=age)

#   # def test_create_student_should_fail_age_constraint(self):
#   #   """
#   #   Test create student record fails due to incorrect age input
#   #   """
#   #   gender = "F"
#   #   age = 25
#   #   with self.assertRaises(IntegrityError):
#   #       students.objects.create(
#   #          gender=gender,
#   #          age=age)