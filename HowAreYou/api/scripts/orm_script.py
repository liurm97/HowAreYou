from ..models import students, responses
from uuid import uuid4
def run():
  student = students.objects.create(
    id=uuid4(),
    gender="M",
    age=22
  )

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

  response = responses.objects.create(
    **resp_obj, student=student
  )
  print(response)