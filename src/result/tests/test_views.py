from django.urls import reverse
from rest_framework import status

from src.test.tests.test_views import TestBaseTest
from . import constants

class ResultBaseTest(TestBaseTest):
    """
    @extends Authenticated Tests
    @description Base Tests for views in registration app
    """
    URL_RESULT_LIST = reverse('results')

    def url_result_detail(self, result_id):
        return reverse('results-detail', kwargs={ "id": result_id })
    
    def url_result_response_list(self, result_id):
        return reverse('results-responses', kwargs={ "id": result_id})
    
    def get_all_results(self):
        """
        @return Response with list of results
        """
        return self.client.get(self.URL_RESULT_LIST)
    
    def create_new_response(self, regis_id, data):
        """
        @return newly created response
        """
        if(not hasattr(self, "token")):
            self.log_user_in()
        access = self.token.get('access', '')
        return self.client.post(self.url_result_response_list(regis_id), data,  format='json', **{'HTTP_AUTHORIZATION': f'Bearer {access}'})
    
class ResultListTest(ResultBaseTest):
    """
    @extends ResultBaseTest
    @description
    - tests the view ResultAPI
    - corresponding url: /registrations/
    - methods: 
        - GET (to get all results)
    """

    def test_all_tests_empty(self):
        """
        @description tests the GET endpoint for
        - returning [] when no tests are created
        """
        response = self.get_all_results()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [])

class ResultDetailTest(ResultBaseTest):
    """
    @extends ResultBaseTest
    @description
    - tests the view ResultDetailAPI
    - corresponding url /registrations/<int:rid>/
    - methods:
        - GET (to get details of a registration)
    """
    def test_get_404_for_invalid(self):
        """
        @description tests the GET endpoint for
        - returning 404 NOT FOUND for invalid registration id
        """
        response = self.client.get(self.url_result_detail(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_result_detail_for_valid(self):
        """
        @description tests the GET endpoint for
        - returning result detail for valid registration id
        """
        self.create_new_test(constants.data_new_test)
        response = self.create_new_registration(1)
        response = self.client.get(self.url_result_detail(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ResultResponseListTest(ResultBaseTest):
    """
    @extends ResultBaseTest
    @description
    - tests the view ResultResponseListAPI
    - corresponding url /registration/<int:rid>/response/
    - methods:
        - GET (to get all responses made under a registration)
        - POST (to make new response)
    """

    def test_get_404_for_invalid(self):
        """
        @description tests the GET endpoint for
        - returning 404 for invalid registration id
        """
        response = self.client.get(self.url_result_response_list(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_404_for_registrations_with_no_responses(self):
        """
        @description tests the GET endpoint for
        - returning 404 for registration with no responses
        """
        self.create_new_test(constants.data_new_test)
        self.create_new_registration(1)
        response = self.client.get(self.url_result_response_list(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_404_for_create_invalid(self):
        """
        @description tests the POST endpoint for
        - returning 404 for invalid registration id
        - [TODO] returning 404 for invalid question id
        """
        response = self.create_new_response(1, constants.data_new_response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.create_new_test(constants.data_new_test)
        self.create_new_registration(1)
        response = self.create_new_response(1, constants.data_new_response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_new_response(self):
        """
        @description tests the POST endpoint for
        - creating new response for the registration
        - updating score for the registration
        by answering question
        - returning created response
        """
        self.create_new_test(constants.data_new_test_with_questions)
        self.create_new_registration(1)
        response = self.create_new_response(1, constants.data_new_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.url_result_response_list(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["status"], "Correct")
        response = self.client.get(self.url_result_detail(1))
        self.assertEqual(response.json()["score"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_multiple_new_responses(self):
        """
        @description tests the POST endpoint for
        - creating multiple new responses for the registration
        - returning created responses
        """
        self.create_new_test(constants.data_new_test_with_questions)
        self.create_new_registration(1)
        response = self.create_new_response(1, constants.data_new_multiple_responses)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

