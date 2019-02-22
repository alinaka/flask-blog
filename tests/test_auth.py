from flask import g, session
from parameterized import parameterized

from flaskr import db
from flaskr.models import User
from .tests import TestFactory, AuthRequestsMixin, BlogRequestsMixin


class AuthTestCase(TestFactory, AuthRequestsMixin, BlogRequestsMixin):

    @parameterized.expand([
        ("", "test", b"Username is required."),
        ("test2", "", b"Password is required."),
        ("test", "test", b'already registered'),
    ])
    def test_register_invalid_data(self, username, password, expected):
        response = self.client.post("/auth/register", data={"username": username, "password": password})
        assert expected in response.data

    def test_register(self):
        self.assert200(self.get_register())
        self.post_register('a', 'a')
        assert User.query.filter_by(username='a').one_or_none() is not None

    def test_login(self):
        with self.client:
            self.post_login("test", "test")
            user = User.query.filter_by(username='test').one_or_none()
            assert user is not None
            self.get_index()
            assert user in db.session
            assert "user_id" in session
        assert g.user.username == 'test'

    @parameterized.expand([
        ("a", "test", b"Incorrect username"),
        ("test", "test2", b"Incorrect password"),
    ])
    def test_login_invalid_credentials(self, username, password, expected):
        response = self.post_login(username, password)
        assert expected in response.data

    def test_logout(self):
        self.post_login("test", "test")
        self.logout()
        assert "user_id" not in session
