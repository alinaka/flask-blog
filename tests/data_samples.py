from werkzeug.security import generate_password_hash

user_data = {
    'username': 'test',
    'password': generate_password_hash('test')
}

post_data = {
    'title': "Test Title",
    "body": "Post Body",
    "created": '2018-01-01 00:00:00'
}
