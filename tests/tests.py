from flask_testing import TestCase

from flaskr import create_app, db
from flaskr.models import User, Post
from .data_samples import user_data, post_data

class TestFactory(TestCase):

    SQLALCHEMY_DATABASE_URI = "postgresql://flask_blog:flask_blog@localhost/test_flask_blog"
    TESTING = True

    def create_app(self):
        return create_app({'TESTING': True})

    def setUp(self):
        db.create_all()
        self.user = self.create_user()
        self.post = self.create_post()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def create_user(self):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

    def create_post(self):
        post = Post(author_id=self.user.id, **post_data)
        db.session.add(post)
        db.session.commit()
        return post

class AuthRequestsMixin:
    def post_login(self, username, password):
        return self.client.post('/auth/login', data={'username': username, 'password': password})

    def get_login(self):
        return self.client.get('/auth/login')

    def post_register(self, username, password):
        return self.client.post('/auth/register', data={'username': username, 'password': password})

    def get_register(self):
        return self.client.get('/auth/register')

    def logout(self):
        return self.client.get('/auth/logout')


class BlogRequestsMixin:
    def get_index(self):
        return self.client.get('/')


class AppTestCase(TestFactory):
    def test_config(self):
        assert not create_app().testing
        assert create_app({'TESTING': True}).testing

    def test_hello(self):
        response = self.client.get('/hello')
        assert response.data == b'Hello, World!'
