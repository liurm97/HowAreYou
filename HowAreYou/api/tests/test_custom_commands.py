"""
Test custom management commands
"""

from django.core.management import call_command
from unittest import TestCase
import pandas as pd
from pathlib import Path as p
from ..models import Student, StudentResponse, Resource

CURRENT_PATH = p.cwd()
DATA_PATH = str(CURRENT_PATH.parent) + "/data"

RELATIVE_CSV_PATHS = {
    "data": DATA_PATH + "/data.csv",
    "resources": DATA_PATH + "/resources.csv",
}


class CustomCommandTest(TestCase):
    """
    Testing for custom management commands
    """

    def setUp(self) -> None:
        call_command("seed_db")

    def tearDown(self) -> None:
        Resource.objects.all().delete()
        Student.objects.all().delete()
        StudentResponse.objects.all().delete()

    def test_seed_db_command(self):
        """
        Test `seed_db` management command

        Pass criteria:
        - number of inserted records in students table equals to rows in data.csv
        - number of inserted records in responses table equals to rows in data.csv
        - number of inserted records in resources table equals to rows in resources.data
        """
        # students and responses row are expected to be the same
        expected_students_and_responses_rows = len(
            pd.read_csv(RELATIVE_CSV_PATHS["data"])
        )
        expected_resources_rows = len(pd.read_csv(RELATIVE_CSV_PATHS["resources"]))

        actual_students_created_records = len(Student.objects.all())
        actual_responses_created_records = len(StudentResponse.objects.all())
        actual_resources_created_records = len(Resource.objects.all())

        self.assertEqual(
            expected_students_and_responses_rows, actual_students_created_records
        )
        self.assertEqual(
            expected_students_and_responses_rows, actual_responses_created_records
        )
        self.assertEqual(expected_resources_rows, actual_resources_created_records)
