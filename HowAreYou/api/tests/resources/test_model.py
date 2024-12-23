"""
Test resources model
"""

from django.test import TestCase
from ...models import responses, students, resources
from django.db.utils import IntegrityError
from copy import deepcopy


resp_obj_article = {
    "url": "https://www.mindline.sg/youth/article/fighting-depression?type=interest",
    "type": "article",
}

resp_obj_video = {
    "url": "https://mindline.sg/youth/article/mental-health-is-not-nothing?type=interest",
    "type": "video",
}


class ResourcesModelTests(TestCase):
    """
    Test for resources model
    """

    def test_create_article_resource_should_pass(self):
        """
        Test create response record is successful
        Pass criteria:
            - foreign key of response record should be equal to primary key of student record
        """
        created_resource = resources.objects.create(**resp_obj_article)
        print(f"created_resource:: {created_resource}")
        self.assertEqual(created_resource.type, resp_obj_article["type"])

    def test_create_video_resource_should_pass(self):
        """
        Test create response record is successful
        Pass criteria:
            - foreign key of response record should be equal to primary key of student record
        """
        created_resource = resources.objects.create(**resp_obj_video)

        self.assertEqual(created_resource.type, resp_obj_video["type"])

    def test_create_resource_should_fail_due_to_incorrect_type(self):
        """
        Test create response record fails due to incorrect type passed
        Fail criteria:
            - type is neither 'article' nor 'video' raises IntegrityError exception
        """
        resp_obj_article_copy = deepcopy(resp_obj_article)
        resp_obj_article_copy["type"] = "articl"

        with self.assertRaises(IntegrityError):
            resources.objects.create(**resp_obj_article_copy)

    def test_create_resource_should_fail_due_to_missing_url(self):
        """
        Test create response record fails due to missing url
        Fail criteria:
            - url is not provided raises IntegrityError exception
        """
        resp_obj_article_copy = deepcopy(resp_obj_article)
        resp_obj_article_copy.pop("url")

        with self.assertRaises(IntegrityError):
            resources.objects.create(**resp_obj_article_copy)
