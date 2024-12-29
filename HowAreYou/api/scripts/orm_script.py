from ..models import Student, Resource, StudentResponse
from uuid import uuid4
import pandas as pd


def create_response():
    """Insert single record into the responses table"""
    student = Student.objects.create(id=uuid4(), gender="M", age=22)

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

    response = StudentResponse.objects.create(**resp_obj, student=student)


def create_resource():
    """Get single record from the resources table"""

    resp_obj_article_pass = {
        "url": "https://www.mindline.sg/youth/article/fighting-depression?type=interest",
        "type": "article",
    }
    resp_obj_article_fail = {
        "type": "article",
    }
    created_resource = Resource.objects.create(**resp_obj_article_pass)


def create_single_student():
    student_obj = {"gender": "M", "age": 24}

    for i in range(10):
        id = uuid4()
        created_student = Student.objects.create(**student_obj, id=id)


def get_students():
    student_records = len(Student.objects.all())


def deduplicate():
    resource_df = pd.read_csv(
        "/Users/bobby/uol/advanced_web_dev/dev/data/resources.csv"
    )
    urls = resource_df["url"].to_list()
    urls_set = set(urls)


def run():
    deduplicate()
    # create_response()
    # create_resource()
    # create_single_student()
    # get_students()
