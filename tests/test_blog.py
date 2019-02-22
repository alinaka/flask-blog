from parameterized import parameterized

from flaskr import db
from flaskr.models import Post
from .tests import TestFactory, AuthRequestsMixin, BlogRequestsMixin


class BlogTestCase(TestFactory, AuthRequestsMixin, BlogRequestsMixin):
    def test_index(self):
        response = self.get_index()
        assert b"Log In" in response.data
        assert b"Register" in response.data

        self.post_login("test", "test")
        response = self.get_index()
        assert b'Log Out' in response.data
        assert b'Test Title' in response.data
        assert b'by test on 2018-01-01' in response.data
        assert b'Post Body' in response.data
        assert b'href="/1/update"' in response.data

    @parameterized.expand([
        '/create',
        '/1/update',
        '/1/delete',
    ])
    def test_login_required(self, path):
        response = self.client.post(path)
        assert response.headers['Location'] == 'http://localhost/auth/login'

    def test_author_required(self):
        self.post_register("test2", "test2")
        post = Post.query.get(self.post.id)
        post.author_id = 2
        db.session.commit()

        self.post_login("test", "test")
        assert self.client.post('/1/update').status_code == 403
        assert self.client.post('/1/delete').status_code == 403
        assert b'href="/1/update"' not in self.client.get('/').data

    @parameterized.expand([
        '/2/update',
        '/2/delete',
    ])
    def test_exists_required(self, path):
        self.post_login("test", "test")
        assert self.client.post(path).status_code == 404

    def test_create(self):
        self.post_login("test", "test")
        assert self.client.get('/create').status_code == 200
        self.client.post('/create', data={'title': 'created', 'body': ''})

        count = Post.query.count()
        assert count == 2

    def test_update(self):
        self.post_login("test", "test")
        assert self.client.get('/1/update').status_code == 200
        self.client.post('/1/update', data={'title': 'updated', 'body': ''})

        post = Post.query.get(1)
        assert post.title == 'updated'

    @parameterized.expand([
            '/create',
            '/1/update',
    ])
    def test_create_update_validate(self, path):
        self.post_login("test", "test")
        response = self.client.post(path, data={'title': '', 'body': ''})
        assert b'Title is required.' in response.data

    def test_delete(self):
        self.post_login("test", "test")
        response = self.client.post('/1/delete')
        assert response.headers['Location'] == 'http://localhost/'
        post = Post.query.get(1)
        assert post is None
