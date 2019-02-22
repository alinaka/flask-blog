from flask_testing import TestCase

from flaskr import create_app, db


class TestFactory(TestCase):

    SQLALCHEMY_DATABASE_URI = "postgresql://flask_blog:flask_blog@localhost/test_flask_blog"
    TESTING = True

    def create_app(self):
        return create_app({'TESTING': True})

    def setUp(self):
        db.create_all()
        self.client.post('/auth/register', data={'username': 'test', 'password': 'test'})

    def tearDown(self):

        db.session.remove()
        db.drop_all()


