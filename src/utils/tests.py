from django.urls import reverse
from rest_framework.test import APITestCase
import json

class AuthenticatedTests(APITestCase):
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

  def setUp(self):
    self.client.post(self.signup_url, self.data_signup, format='json')

  def log_user_in(self):
    response = self.client.post(self.login_url, self.data_login, format='json')
    self.token = json.loads(response.content).get('token', '')
