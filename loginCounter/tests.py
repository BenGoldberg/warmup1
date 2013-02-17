from django.utils import unittest
from loginCounter.models import Users
from django.test.client import Client
from django.utils import simplejson as json

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add only) invalid user name (empty string and longer than 128 characters is invalid)
ERR_BAD_PASSWORD      =  -4  # : (for add only) invalid password (longer than 128 characters is invalid)

class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def testAdd(self):
        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"count": 1, "errCode": 1}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testLogin(self):
        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"count": 2, "errCode": 1}'
        self.c.post('/users/add', json_string, content_type="application/json")
        response = self.c.post('/users/login', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testWrongUser(self):
        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"errCode": -1}'
        response = self.c.post('/users/login', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testWrongPassword(self):
        json_string1 = '{"user": "john", "password": "secret"}'
        json_string2 = '{"user": "john", "password": "wrong"}'
        correct_response = '{"errCode": -1}'
        self.c.post('/users/add', json_string1, content_type="application/json")
        response = self.c.post('/users/login', json_string2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testUserExists(self):
        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"errCode": -2}'
        self.c.post('/users/add', json_string, content_type="application/json")
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testNoUsername(self):
        json_string = '{"user": "", "password": "secret"}'
        correct_response = '{"errCode": -3}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testTooBigUsername(self):
        json_string = '{"user": "wrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrong", "password": "secret"}'
        correct_response = '{"errCode": -3}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testBadPassword(self):
        json_string = '{"user": "john", "password": "wrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrongwrong"}'
        correct_response = '{"errCode": -4}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testNoPassword(self):
        json_string = '{"user": "john", "password": ""}'
        correct_response = '{"count": 1, "errCode": 1}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)
        self.c.post('/TESTAPI/resetFixture')

    def testMultiUsers(self):
        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"count": 1, "errCode": 1}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)

        json_string = '{"user": "ben", "password": "nosecret"}'
        correct_response = '{"count": 1, "errCode": 1}'
        response = self.c.post('/users/add', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)

        json_string = '{"user": "ben", "password": "nosecret"}'
        correct_response = '{"count": 2, "errCode": 1}'
        response = self.c.post('/users/login', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)

        json_string = '{"user": "ben", "password": "nosecret"}'
        correct_response = '{"count": 3, "errCode": 1}'
        response = self.c.post('/users/login', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)

        json_string = '{"user": "john", "password": "secret"}'
        correct_response = '{"count": 2, "errCode": 1}'
        response = self.c.post('/users/login', json_string, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, correct_response)

        self.c.post('/TESTAPI/resetFixture')

