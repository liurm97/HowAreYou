"""
Seed database script
"""

import pandas as pd
from pathlib import Path as p
import json
from uuid import uuid4

from ..models import Student, StudentResponse, Resource

CURRENT_PATH = p.cwd()
DATA_PATH = str(CURRENT_PATH.parent) + "/data"

RELATIVE_CSV_PATHS = {
    "data": DATA_PATH + "/data.csv",
    "resources": DATA_PATH + "/resources.csv",
}


def prepare_data(filename: str) -> list[dict]:
    df = pd.read_csv(RELATIVE_CSV_PATHS[filename])

    # prepare data.csv
    if filename == "data":
        students_output: list[Student] = []
        responses_output: list[StudentResponse] = []

        column_rename_mapping = {
            "PHQ9 score": "score",
            "Gender": "gender",
            "Age": "age",
            "q1": "q1_resp",
            "q2": "q2_resp",
            "q3": "q3_resp",
            "q4": "q4_resp",
            "q5": "q5_resp",
            "q6": "q6_resp",
            "q7": "q7_resp",
            "q8": "q8_resp",
            "q9": "q9_resp",
        }

        gender_mapping = {"Female": "F", "Male": "M"}

        data_df_copy = df.copy()
        data_df_copy.drop(["Institute"], axis=1, inplace=True)
        data_df_copy = data_df_copy.rename(columns=column_rename_mapping)

        # iterate through data
        for ind, _ in data_df_copy.iterrows():
            r = data_df_copy.iloc[ind,]
            json_r = json.loads(r.to_json())
            json_r["gender"] = gender_mapping[json_r["gender"]]
            json_r["id"] = str(uuid4())
            student_obj = Student(
                id=json_r["id"], age=json_r["age"], gender=json_r["gender"]
            )

            students_output.append(student_obj)
            responses_output.append(
                StudentResponse(
                    q1_resp=json_r["q1_resp"],
                    q2_resp=json_r["q2_resp"],
                    q3_resp=json_r["q3_resp"],
                    q4_resp=json_r["q4_resp"],
                    q5_resp=json_r["q5_resp"],
                    q6_resp=json_r["q6_resp"],
                    q7_resp=json_r["q7_resp"],
                    q8_resp=json_r["q8_resp"],
                    q9_resp=json_r["q9_resp"],
                    score=json_r["score"],
                    student=student_obj,
                )
            )
        print(f"students_output:: {len(students_output)}")
        print(f"responses_output:: {len(responses_output)}")
        return students_output, responses_output

    # prepare resources.csv
    elif filename == "resources":
        resources_output: list[Resource] = []
        resources_df_copy = df.copy()
        for ind, _ in resources_df_copy.iterrows():
            r = resources_df_copy.iloc[ind,]
            json_r = json.loads(r.to_json())
            resources_output.append(Resource(url=json_r["url"], type=json_r["type"]))
    return resources_output


def seed_students_and_responses_db() -> None:
    """
    Seed students and responses database
    """
    processed_data_students, processed_data_responses = prepare_data("data")
    print(f"processed_data_students", len(processed_data_students))
    print(f"processed_data_responses", len(processed_data_responses))
    Student.objects.bulk_create(processed_data_students)

    StudentResponse.objects.bulk_create(processed_data_responses)


def seed_resources_db() -> None:
    """
    Seed resources database,
    """

    processed_data_resources: list[Resource] = prepare_data("resources")
    Resource.objects.bulk_create(processed_data_resources)


def run():
    pass
    # seed_students_and_responses_db()
    # seed_resources_db()
    # prepare_data()
