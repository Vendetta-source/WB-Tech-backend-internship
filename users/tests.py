from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class SettingsForTests(APITestCase):

    def setUp(self):
        self.wrong_user = {'username': 'wrong_user',
                           'password': ''}
        self.user_data1 = {'username': 'test_user1',
                           'password': 'wbtech1234'}
        self.user_data2 = {'username': 'test_user2',
                           'password': 'wbtech1234'}
        self.article = {'title': 'test title',
                        'content': 'test text content'}
        self.article2 = {'title': 'test title 2',
                         'content': 'test text content 2'}
        self.client.post('/api/v1/auth/users/', self.user_data1)
        self.client2 = APIClient()
        self.client2.post('/api/v1/auth/users/', self.user_data2)
        response = self.client.post('/api/v1/auth/token/login/', self.user_data1)
        self.token = response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.post('/api/v1/articles/', self.article)
        self.client.post('/api/v1/articles/', self.article2)


class TestAuthorizationUsers(APITestCase):
    """Tests for Users Authentication"""

    def test_registration(self):
        response_wrong = self.client.post('/api/v1/auth/users/', {'username': 'wrong_user', 'password': ''})
        self.assertEqual(response_wrong.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/v1/auth/users/', {'username': 'test_user3', 'password': 'wbtech1234'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        self.client.post('/api/v1/auth/users/', {'username': 'test_user3', 'password': 'wbtech1234'})
        response = self.client.post('/api/v1/auth/token/login/', {'username': 'test_user3', 'password': 'wbtech1234'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestManageUser(SettingsForTests):

    def test_logout(self):
        response = self.client.post('/api/v1/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post('/api/v1/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_of_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_articles_of_user(self):
        response = self.client.get('/api/v1/users/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/v1/users/')
        pk = response.json()['results'][0]['id']
        response = self.client.get(f'/api/v1/users/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe_and_unsubscribe(self):
        # subscribe
        response = self.client2.post('/api/v1/users/1/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client2.post('/api/v1/auth/token/login/', self.user_data2)
        token2 = response.json()['auth_token']
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + token2)

        response = self.client2.post('/api/v1/users/9/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client2.post('/api/v1/users/9/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client2.post('/api/v1/users/10/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # unsubscribe
        response = self.client2.post('/api/v1/users/9/unsubscribe/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscribed_authors_articles(self):
        response = self.client2.get('/api/v1/users/subscribed_authors_articles/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client2.post('/api/v1/auth/token/login/', self.user_data2)
        token2 = response.json()['auth_token']
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + token2)

        self.client2.post('/api/v1/users/11/subscribe/')
        response = self.client2.get('/api/v1/users/subscribed_authors_articles/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.post('/api/v1/articles/', self.article)
        response = self.client2.get('/api/v1/users/subscribed_authors_articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
