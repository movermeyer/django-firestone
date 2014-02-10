"""
This module tests ``firestone.handlers.BaseHandler.post`` and
``firestone.handlers.ModelHandler.post`` methods.
"""
from firestone.handlers import BaseHandler
from firestone.handlers import ModelHandler
from firestone import exceptions
from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from model_mommy import mommy

class TestBaseHandlerPost(TestCase):
    def test_post(self):
        handler = BaseHandler()       
        request = RequestFactory().post('/')

        self.assertRaises(
            exceptions.NotImplemented,
            handler.post,
            request
        )


class TestModelHandlerSinglePost(TestCase):
    def setUp(self):
        self.handler = ModelHandler()
        self.handler.model = User

        self.request = RequestFactory().post('/')
        self.user = User(username='user', password='password')
        self.request.data = self.user

    def test_ret_value(self):
        """
        Test returned value of post method
        """
        self.assertEqual(self.handler.post(self.request), self.user)

    def test_created(self):
        """
        Test that the post method has indeed created the model instance
        """
        res = self.handler.post(self.request)
        self.assertIsNotNone(res.id)

    def test_num_queries(self):
        """
        Test that only one DB query was performed
        """
        self.assertNumQueries(1, self.handler.post, self.request)

class TestModelHandlerBulkPost(TestCase):
    def setUp(self):
        self.handler = ModelHandler()
        self.handler.model = User

        self.request = RequestFactory().post('/')
        self.users = [
            User(username='user1', password='pass1'),
            User(username='user2', password='pass2'),
            User(username='user3', password='pass3'),
            User(username='user4', password='pass4'),
            User(username='user5', password='pass5'),
        ]
        self.request.data = self.users

    def test_ret_value(self):
        self.assertItemsEqual(self.handler.post(self.request), self.users)

    def test_created(self):
        res = self.handler.post(self.request)
        for user in res:
            self.assertIsNotNone(user.id)

    def test_num_queries(self):
        self.assertNumQueries(5, self.handler.post, self.request)


