"""
Define API data models
"""
from django.db import models
from uuid import uuid4

class students(models.Model):
  """
  Normalized data model for students
  """
  MALE = "M"
  FEMALE = "F"
  OTHERS = "O"
  GENDER_CHOICES = [
      (MALE, "Male"),
      (FEMALE, "Female"),
      (OTHERS, "Others"),
  ]
  id = models.UUIDField(primary_key=True, db_index=True, blank=False, null=False, default=uuid4())
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)
  age = models.IntegerField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"id: {self.id} | gender: {self.gender} | age: {self.age}"

  class Meta:
    """
    1. age_constraint: age >=12 and age <= 24
    2. gender_constraint: age is in ["M", "F", "O"]
    """
    constraints = [
      models.CheckConstraint(
        check=models.Q(age__gte=12) & models.Q(age__lte=24),
        name="Age constraint",
        violation_error_message="Age must be between 12 (inclusive) and 24 (inclusive)"),
      models.CheckConstraint(
        check=models.Q(gender='M') | models.Q(gender='F') | models.Q(gender='O'),
        name="Gender constraint",
        violation_error_message="Gender must be one of {M, F, Q}")]

class responses(models.Model):
  """
  Normalized responses model
  """
  q1_resp= models.IntegerField()
  q1_resp= models.IntegerField()
  q1_resp= models.IntegerField()
  q2_resp= models.IntegerField()
  q3_resp= models.IntegerField()
  q4_resp= models.IntegerField()
  q5_resp= models.IntegerField()
  q6_resp= models.IntegerField()
  q7_resp= models.IntegerField()
  q8_resp= models.IntegerField()
  q9_resp= models.IntegerField()
  score = models.PositiveSmallIntegerField()
  student = models.ForeignKey(students, related_name="student", on_delete=models.CASCADE)
  
  def __str__(self):
     return f"score: {self.score}"

  class Meta:
        constraints = [
           models.CheckConstraint(
              check=models.Q(q1_resp__gte=0) & 
              models.Q(q1_resp__lte=3),
              name="q1_resp constraint",
              violation_error_message="q1_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q2_resp__gte=0) & 
        models.Q(q2_resp__lte=3),
        name="q2_resp constraint",
        violation_error_message="q2_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q3_resp__gte=0) & 
        models.Q(q3_resp__lte=3),
        name="q3_resp constraint",
        violation_error_message="q3_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q4_resp__gte=0) & 
        models.Q(q4_resp__lte=3),
        name="q4_resp constraint",
        violation_error_message="q4_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q5_resp__gte=0) & 
        models.Q(q5_resp__lte=3),
        name="q5_resp constraint",
        violation_error_message="q5_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q6_resp__gte=0) & 
        models.Q(q6_resp__lte=3),
        name="q6_resp constraint",
        violation_error_message="q6_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q7_resp__gte=0) & 
        models.Q(q7_resp__lte=3),
        name="q7_resp constraint",
        violation_error_message="q7_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q8_resp__gte=0) & 
        models.Q(q8_resp__lte=3),
        name="q8_resp constraint",
        violation_error_message="q8_resp must be between 12 (inclusive) and 24 (inclusive)"),

              models.CheckConstraint(
        check=models.Q(q9_resp__gte=0) & 
        models.Q(q9_resp__lte=3),
        name="q9_resp constraint",
        violation_error_message="q9_resp must be between 12 (inclusive) and 24 (inclusive)"),

          models.CheckConstraint(
        check=models.Q(score__gte=0) & 
        models.Q(score__lte=27),
        name="score constraint",
        violation_error_message="score must be between 12 (inclusive) and 24 (inclusive)"),

        ]