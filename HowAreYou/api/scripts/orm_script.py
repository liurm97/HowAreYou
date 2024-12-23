from ..models import students, responses, resources
from uuid import uuid4


def create_response():
    """Insert single record into the responses table"""
    student = students.objects.create(id=uuid4(), gender="M", age=22)

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

    response = responses.objects.create(**resp_obj, student=student)
    print(response)


def create_resource():
    """Get single record from the resources table"""

    resp_obj_article_pass = {
        "url": "https://www.mindline.sg/youth/article/fighting-depression?type=interest",
        "type": "article",
    }
    resp_obj_article_fail = {
        "type": "article",
    }
    created_resource = resources.objects.create(**resp_obj_article_pass)


def run():
    # create_response()
    create_resource()
