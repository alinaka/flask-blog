from flask import g, session
from parameterized import parameterized

from flaskr import db
from flaskr.models import User
from .tests import TestFactory


class AuthTestCase(TestFactory):

    def login(self, username, password):
        return self.client.post('/auth/login', data={'username': username, 'password': password})

    @parameterized.expand([
        ("", "test", b"Username is required."),
        ("test2", "", b"Password is required."),
        ("test", "test", b'already registered'),
    ])
    def test_register_invalid_data(self, username, password, expected):
        response = self.client.post("/auth/register", data={"username":username, "password": password})
        assert expected in response.data

    def test_register(self):
        self.assert200(self.client.get('/auth/register'))
        self.client.post('/auth/register', data={'username': 'a', 'password': 'a'})
        assert User.query.filter_by(username='a').one_or_none() is not None
        response = self.client.post('/auth/register', data={'username': 'a', 'password': 'a'})
        assert b"already registered" in response.data

    def test_login(self):
        self.login("test", "test")
        user = User.query.filter_by(username='test').one_or_none()
        assert user is not None
        self.client.get('/')
        assert user in db.session
        assert g.user.username == 'test'

    @parameterized.expand([
        ("a", "test", b"Incorrect username"),
        ("test", "test2", b"Incorrect password"),
    ])
    def test_login_invalid_credentials(self, username, password, expected):
        response = self.login(username, password)
        assert expected in response.data

    def test_logout(self):
        self.login("test", "test")
        self.client.get('/auth/logout')
        assert "user_id" not in session
