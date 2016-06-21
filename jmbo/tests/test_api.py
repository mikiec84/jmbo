import unittest
import json

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test.client import Client

from rest_framework.test import APIClient

from jmbo.models import ModelBase
from jmbo.tests.models import TestModel


class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()

        # Editor
        cls.editor = get_user_model().objects.create(
            username="editor-api",
            email="editor-api@test.com",
            is_superuser=True,
            is_staff=True
        )
        cls.editor.set_password("password")
        cls.editor.save()
        cls.client.login(username="editor-api", password="password")

        # Prep
        Site.objects.all().delete()
        Site.objects.create(id=1, domain="site.example.com")
        ModelBase.objects.all().delete()

        # Objects for this test
        cls.obj1 = TestModel(title="title1")
        cls.obj1.save()
        cls.obj2 = TestModel(title="title2", state="published")
        cls.obj2.save()
        cls.obj2.sites = Site.objects.all()
        cls.obj2.save()

    def test_modelbase_list(self):
        response = self.client.get("/api/v1/jmbo-modelbases/")
        as_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(as_json), 2)

    def test_permitted_modelbase_list(self):
        response = self.client.get("/api/v1/jmbo-permitted-modelbases/")
        as_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(as_json), 1)

    def test_testmodel_list(self):
        response = self.client.get("/api/v1/tests-testmodels/")
        as_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(as_json), 2)

    def test_permitted_testmodel_list(self):
        response = self.client.get("/api/v1/tests-permitted-testmodels/")
        as_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(as_json), 1)

    def test_testmodel_create(self):
        """Light test since DRF and DRFE already test similar paths"""
        new_pk = TestModel.objects.all().last().id + 1
        data = {
            "title": "title",
            "slug": "title",
            "content": "content"
        }
        response = self.client.post("/api/v1/tests-testmodels/", data)
        as_json = json.loads(response.content)
        self.assertEqual(as_json["content"], "content")
        self.assertTrue(TestModel.objects.filter(pk=new_pk).exists())
        # Cleanup else it pollutes other tests
        TestModel.objects.filter(pk=new_pk).delete()