"""
Test seeding students db
"""

from unittest import TestCase
from pathlib import Path as p
import pandas as pd
from ...scripts.seed_db_script import seed_students_and_responses_db
from ...models import Student, StudentResponse

CURRENT_PATH = p.cwd()
DATA_PATH = str(CURRENT_PATH.parent) + "/data"

RELATIVE_CSV_PATHS = {
    "data": DATA_PATH + "/data.csv",
    "resources": DATA_PATH + "/resources.csv",
}


class StudentSeedTests(TestCase):
    """
    Test script that seeds students database
    """

    def setUp(self) -> None:
        seed_students_and_responses_db()

    def tearDown(self) -> None:
        Student.objects.all().delete()
        StudentResponse.objects.all().delete()

    def test_relative_data_csv_file_exists(self):
        """
        Test data csv relative path exists
        Pass criteria: size of students dataframe is greater than 0
        """
        students_df_records = len(pd.read_csv(RELATIVE_CSV_PATHS["data"]))
        self.assertTrue(students_df_records > 0)

    def test_seed_students_successful(self):
        """
        Test seeding script successfully inserts records into students table
        Pass criteria: number of records in students table equals number of rows in data.csv
        """

        expected_students_rows = len(pd.read_csv(RELATIVE_CSV_PATHS["data"]))

        actual_students_records_in_db = len(Student.objects.all())

        self.assertEqual(expected_students_rows, actual_students_records_in_db)
