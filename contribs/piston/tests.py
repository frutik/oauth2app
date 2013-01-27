# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import json
from base64 import b64encode

from django.utils.unittest.case import skip
from django.test.client import Client
from django.test import TestCase
from oauth2app.models import Client as MobileClient

class TestOaut2Authorizer(TestCase):
    """
    Run: python manage.py test --settings=config.test client_api
    """
    fixtures = ['mobile_client_api_data.json']

    def setUp(self):
        self.maxDiff = None #100
        self.client = Client()

        u = User.objects.get(id=1) # User from fixture
        logged_in = self.client.login(username=u.email, password='123qwe')
        self.assertTrue(logged_in)

        u = User.objects.get(pk=1)
        m = MobileClient()
        m.name = 'test'
        m.user = u
        m.key = 'test'
        m.secret = 'test'
        m.save()

    @skip
    def test_get_campaign_details_invalid_request(self):
        response = self.client.get('/client-api/v1/campaign/')

        result = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['error'], 'invalid_request')

    @skip
    def test_get_auth_token_wrong(self):
        response = self.client.post('/client-api/v1/oauth2/token/')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['error'], 'invalid_request')

    @skip
    def test_get_auth_token_client_wrong(self):
        response = self.client.post('/client-api/v1/oauth2/token/', {'test':'test'}, content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION='Basic ' + b64encode('wrong:wrong'))

        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['error'], 'invalid_client')

    @skip
    def _test_get_auth_token_grant_type_wrong(self):
        pass

    @skip
    def _test_get_auth_token_grant_type(self):
        pass

    @skip
    def _test_get_auth_token_wrong_username(self):
        pass

    @skip
    def _test_get_auth_token_wrong_password(self):
        pass

    @skip
    def _test_get_auth_token_success(self):
        pass
