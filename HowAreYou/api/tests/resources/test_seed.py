"""
Test seeding resources db
"""

from unittest import TestCase
from pathlib import Path as p
import pandas as pd
from ...scripts.seed_db_script import seed_resources_db
from ...models import Resource

CURRENT_PATH = p.cwd()
DATA_PATH = str(CURRENT_PATH.parent) + "/data"

RELATIVE_CSV_PATHS = {
    "data": DATA_PATH + "/data.csv",
    "resources": DATA_PATH + "/resources.csv",
}


class ResourcesSeedTests(TestCase):
    """
    Test script that seeds students database
    """

    def setUp(self) -> None:
        seed_resources_db()

    def tearDown(self) -> None:
        Resource.objects.all().delete()

    def test_relative_resources_csv_file_exists(self):
        """
        Test resources csv relative path exists
        Pass criteria: size of resources dataframe is greater than 0
        """
        resources_df_records = len(pd.read_csv(RELATIVE_CSV_PATHS["resources"]))
        self.assertTrue(resources_df_records > 0)

    def test_seed_resources_successful(self):
        """
        Test seeding script successfully inserts records into students table
        Pass criteria: number of records in students table equals number of rows in data.csv
        """

        expected_resources_rows = len(pd.read_csv(RELATIVE_CSV_PATHS["resources"]))

        actual_resources_records_in_db = len(Resource.objects.all())

        self.assertEqual(expected_resources_rows, actual_resources_records_in_db)
