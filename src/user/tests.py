from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

class SignUpTests(APITestCase):
  url = reverse('signup')
  data_correct = {
      "first_name": "Tes",
      "last_name": "T",
      "username": "test",
      "email": "test@mail.com",
      "password": "testpassword"
  }
  data_incorrect = {
      "email": "test@mail.com",
      "password": "testpassword"
  }

  def test_signup_fails_without_credentials(self):
    response = self.client.post(self.url, {}, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_signup_fails_for_wrong_credentials(self):
    response = self.client.post(self.url, self.data_incorrect, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_signup_succeeds_with_correct_credentials(self):
    response = self.client.post(self.url, self.data_correct, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LogInTests(APITestCase): 
  url = reverse('login')
  signup_url = reverse('signup')
  data_correct = {
      "email": "test@mail.com",
      "password": "testpassword"
  }
  data_incorrect = {
      "email": "test@mail.com",
      "password": "password"
  }

  data_signup = {
      "first_name": "Tes",
      "last_name": "T",
      "username": "test",
      "email": "test@mail.com",
      "password": "testpassword"
  }

  def setUp(self):
    self.client.post(self.signup_url, self.data_signup, format='json')

  def test_login_fails_without_credentials(self):
    response = self.client.post(self.url, {}, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_fails_for_wrong_credentials(self):
    response = self.client.post(self.url, self.data_incorrect, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_login_succeeds_with_correct_credentials(self):
    response = self.client.post(self.url, self.data_correct, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetUserTests(APITestCase):
  url = reverse("me")
  login_url = reverse('login')
  signup_url = reverse('signup')

  data_login = {
      "email": "test@mail.com",
      "password": "testpassword"
  }

  data_signup = {
      "first_name": "Tes",
      "last_name": "T",
      "username": "test",
      "email": "test@mail.com",
      "password": "testpassword"
  }

  data_response = {
      "first_name": "Tes",
      "last_name": "T",
      "username": "test",
      "email": "test@mail.com",
  }

  def setUp(self):
    self.client.post(self.signup_url, self.data_signup, format='json')

  def log_user_in(self, data):
    response = self.client.post(self.login_url, self.data_login, format='json')
    self.token = json.loads(response.content).get('token', '')

  def test_get_user_fails_when_logged_out(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertJSONNotEqual(response.content, self.data_response)

  def test_get_user_succeeds_when_logged_in(self):
    self.log_user_in(self.data_login)
    access = self.token.get('access', '')
    response = self.client.get(self.url, **{'HTTP_AUTHORIZATION': f'Bearer {access}'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, self.data_response)
