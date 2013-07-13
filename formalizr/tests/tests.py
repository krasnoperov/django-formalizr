import json
from django.utils import unittest
from django.test.client import RequestFactory
from formalizr.tests.views import SimpleFormView, SimpleCreateView, SimpleUpdateView
from formalizr.tests.models import SimpleModel


class AjaxFormViewTest(unittest.TestCase):

    view_class = SimpleFormView

    VALUE = 1

    def setUp(self):
        self.factory = RequestFactory()
        SimpleModel.objects.all().delete()

    def testRequest(self):
        """
        Posts valid form in normal way
        """
        data = {"value": AjaxFormViewTest.VALUE}
        request = self.factory.post('/', data)
        response = self.view_class.as_view()(request)

        self.assertEqual(302, response.status_code)
        self.assertEqual(self.view_class.success_url, response["location"])

    def testNotValid(self):
        """
        Posts not valid form in normal way
        """
        data = {}
        request = self.factory.post('/', data)
        response = self.view_class.as_view()(request)

        self.assertEqual(200, response.status_code)
        self.assertIn("value", response.context_data["form"].errors)

    def testAjaxRequest(self):
        """
        Posts valid form through AJAX request.
        Response with redirect must be in JSON.
        """
        data = {"value": AjaxFormViewTest.VALUE}
        request = self.factory.post('/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.view_class.as_view()(request)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response['content-type'].split(';')[0])

        resp = json.loads(response.content)
        self.assertEqual("redirect", resp["status"])
        self.assertEqual(self.view_class.success_url, resp["location"])

        return resp

    def testAjaxNotValid(self):
        """
        Posts not valid form through AJAX request.
        Response with errors must be in JSON.
        """
        data = {}
        request = self.factory.post('/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.view_class.as_view()(request)

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response['content-type'].split(';')[0])

        resp = json.loads(response.content)
        self.assertEqual("error", resp["status"])
        self.assertIn("value", resp["errors"])

        return resp

    def testAjaxResultRequest(self):
        """
        Posts valid form through AJAX request.
        Response with result must be in JSON.
        """
        data = {"value": AjaxFormViewTest.VALUE, "_return": "result"}
        request = self.factory.post('/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.view_class.as_view()(request)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response['content-type'].split(';')[0])

        resp = json.loads(response.content)
        self.assertEqual("success", resp["status"])

        return resp


class AjaxCreateViewTest(AjaxFormViewTest):

    view_class = SimpleCreateView

    def testRequest(self):
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 0)
        super(AjaxCreateViewTest, self).testRequest()
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 1)

    def testAjaxRequest(self):
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 0)
        super(AjaxCreateViewTest, self).testAjaxRequest()
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 1)

    def testAjaxResultRequest(self):
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 0)
        resp = super(AjaxCreateViewTest, self).testAjaxResultRequest()
        self.assertEqual(SimpleModel.objects.filter(value=AjaxFormViewTest.VALUE).count(), 1)

        self.assertIn("pk", resp["object"])
        obj = SimpleModel.objects.get(pk=resp["object"]["pk"])
        self.assertEqual(AjaxFormViewTest.VALUE, obj.value)


class AjaxUpdateViewTest(AjaxCreateViewTest):
    view_class = SimpleUpdateView

    def setUp(self):
        super(AjaxUpdateViewTest, self).setUp()
        SimpleModel.objects.filter(value=SimpleUpdateView.VALUE).delete()
        SimpleModel(value=SimpleUpdateView.VALUE).save()
