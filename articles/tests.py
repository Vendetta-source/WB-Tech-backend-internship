from rest_framework.test import APITestCase
from rest_framework import status


class TestArticle(APITestCase):
    """ Test Articles"""
    def setUp(self):
        self.user_data = {'username': 'test_user3',
                          'password': 'wbtech1234'}
        self.article = {'title': 'test title 3',
                        'content': 'test text content 3'}

    def test_all_articles(self):
        response = self.client.get('/api/v1/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_article(self):
        response = self.client.post('/api/v1/articles/', self.article)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.post('/api/v1/auth/users/', self.user_data)
        response = self.client.post('/api/v1/auth/token/login/', self.user_data)
        token = response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/api/v1/articles/', self.article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_mark(self):
        self.client.post('/api/v1/auth/users/', self.user_data)
        response = self.client.post('/api/v1/auth/token/login/', self.user_data)
        token = response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.client.post('/api/v1/articles/', self.article)

        response = self.client.post('/api/v1/articles/2/read_mark/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/v1/articles/2/read_mark/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)




