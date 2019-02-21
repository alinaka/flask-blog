from flask_testing import TestCase
from flask import g, session

from flaskr import create_app, db
from flaskr.models import User


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "postgresql://flask_blog:flask_blog@localhost/test_flask_blog"
    TESTING = True

    def create_app(self):
        return create_app({'TESTING': True})

    def setUp(self):
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


class AuthTestCase(MyTest):
    def login(self, username, password):
        return self.client.post('/auth/login', data={'username': username, 'password': password})

    def test_register_empty_username(self):
        response = self.client.post("/auth/register", data={"username":"", "password": "fdf"})
        assert b"Username is required." in response.data

    def test_register(self):
        self.assert200(self.client.get('/auth/register'))
        self.client.post('/auth/register', data={'username': 'a', 'password': 'a'})
        assert User.query.filter_by(username='a').one_or_none() is not None
        response = self.client.post('/auth/register', data={'username': 'a', 'password': 'a'})
        assert b"already registered" in response.data

    def test_login(self):
        self.client.post("/auth/register", data={"username": "test", "password": "test"})
        self.login("test", "test")
        user = User.query.filter_by(username='test').one_or_none()
        assert user is not None
        self.client.get('/')
        assert user in db.session
        assert g.user.username == 'test'

    def test_login_invalid_credentials(self):
        self.client.post("/auth/register", data={"username": "test", "password": "test"})
        response = self.login("a", "test")
        assert b"Incorrect username" in response.data
        response = self.login("test", "test2")
        assert b"Incorrect password" in response.data

    def test_logout(self):
        self.client.post("/auth/register", data={"username": "test2", "password": "test2"})
        self.login("test2", "test2")
        self.client.get('/auth/logout')
        assert "user_id" not in session
