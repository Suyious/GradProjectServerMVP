from django.urls import reverse
from rest_framework import status
from src.utils.tests import AuthenticatedTests
from . import constants

class TestBaseTest(AuthenticatedTests):
  """
  @extends AuthenticatedTests
  @description Base Test for views in test app
  """
  URL_TEST_LIST = reverse('tests')

  def url_question_create(self, test_id):
    return reverse('test-questions', kwargs = { "id": test_id })

  def url_test_detail(self, test_id):
    return reverse('test-detail', kwargs = { "id": test_id })

  def url_test_question_detail(self, test_id, question_id):
    return reverse('test-question-detail', kwargs = { "tid": test_id, "qid": question_id })

  def url_test_results(self, test_id):
    return reverse('test-results', kwargs = { "id": test_id })
  
  def get_all_tests(self):
    """
    @return Response with list of tests
    """
    return self.client.get(self.URL_TEST_LIST)

  def create_new_test(self, data):
    """
    @args data: dict for new test
    @return Response with newly created test
    """
    self.log_user_in()
    access = self.token.get('access', '')
    response = self.client.post(self.URL_TEST_LIST, data, format='json', **{'HTTP_AUTHORIZATION': f'Bearer {access}'})
    return response

  def create_new_question(self, test_id, data):
    """
    @args test_id : the test to create questions for
          data    : question(s) for the test as dict/dict[]
    @returns Response with newly created question
    """
    access = self.token.get('access', '')
    response = self.client.post(self.url_question_create(test_id), data, format='json', **{'HTTP_AUTHORIZATION': f'Bearer {access}'})
    return response
  
  def create_new_registration(self, test_id):
    """
    @args test_id : the test to create registrations for
    @returns Response with newly created registration
    """
    access = self.token.get('access', '')
    response = self.client.post(self.url_test_results(test_id), format='json', **{'HTTP_AUTHORIZATION': f'Bearer {access}'})
    return response


class TestListTest(TestBaseTest):
  """
  @extends TestBaseTest
  @description
    - tests the view TestAPI
    - corresponding url: /tests/
  """

  def test_list_all_tests_empty(self):
    """
    @description tests the GET endpoint for
    - returning [] when no tests are created
    """
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [])

  def test_create_new_test_and_list(self):
    """
    @description tests the POST endpoint for
    - allowing creation of single test and return the test
    - showing the created test in the list api
    """
    response = self.create_new_test(constants.data_new_test)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, { "success": True, "data": constants.data_response })
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response ])

  def test_list_only_online_tests(self):
    """
    @description tests the GET endpoint for
    - returning only the tests that are currently being
    conducted using the query param `?filter=online`
    """
    self.create_new_test(constants.data_new_test)
    self.create_new_test(constants.data_test_online)
    response = self.client.get(self.URL_TEST_LIST, { "filter": "online" })
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response_online ])

  def test_list_only_available_tests(self):
    """
    @description tests the GET endpoint for
    - returning only the tests that are currently
    available using the query param `?filter=available`
    """
    self.create_new_test(constants.data_new_test)
    self.create_new_test(constants.data_test_offline)
    response = self.client.get(self.URL_TEST_LIST)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response_offline, constants.data_response, ])
    response = self.client.get(self.URL_TEST_LIST, { "filter": "available" })
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response ])

  def test_create_new_test_with_questions(self):
    """
    @description tests the POST endpoint for
    - allowing creation of new test while accepting
    the questions for the test and creating them as well
    """
    response = self.create_new_test(constants.data_new_test_with_question)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, { "success": True, "data": constants.data_new_test_with_question_response })
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_new_test_with_question_response ])
    

class TestDetailTest(TestBaseTest):
  """
  @extends TestBaseTest
  @description test for
  - view TestDetailAPI
  - corresponding url /test/<int:id>/
  """

  def test_get_details_for_valid_id(self):
    """
    @description tests the GET endpoint for
    - returning single test corrsponding to given id
    """
    self.create_new_test(constants.data_new_test)
    response = self.client.get(self.url_test_detail(1))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, { "success": True, "data": constants.data_response })

  def test_delete_for_valid_id(self):
    """
    @description tests the DELETE endpoint for
    - deleting single test corresponding to given id
    """
    self.create_new_test(constants.data_new_test)
    self.create_new_test(constants.data_new_test)
    response = self.client.delete(self.url_test_detail(1))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ { **constants.data_response, "id": 2 } ])


class TestQuestionListTest(TestBaseTest):
  """
  @extends TestBaseTest
  @description test for
  - view TestQuestionAPI
  - corresponding url /test/<int:id>/question/
  """

  def test_get_questions_for_test_empty(self):
    """
    @description tests the GET endpoint for
    - returning all the questions that relate to
    the test with given id
    """
    self.create_new_test(constants.data_new_test)
    response = self.client.get(self.url_question_create(1))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [])

  def test_create_new_question_single(self):
    """
    @description tests the POST endpoint for
    - creating a new question for the test with the 
    given id
    - return the newly created question
    """
    self.create_new_test(constants.data_new_test)
    response = self.create_new_question(1, constants.data_new_question)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, { "success": True, "data": constants.data_question_response })
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response_test_with_question ])

  def test_create_new_questions_multiple(self):
    """
    @description tests the POST endpoint for
    - creating multiple new questions for the test with the 
    given id
    - return the newly created questions
    """
    self.create_new_test(constants.data_new_test)
    response = self.create_new_question(1, constants.data_new_questions_multiple)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, { "success": True, "data": constants.data_questions_multiple_response })
    response = self.get_all_tests()
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, [ constants.data_response_test_with_questions_multiple ])


class TestQuestionDetailTest(TestBaseTest):
  """
  @extends TestBaseTest
  @description test for
  - view TestQuestionDetailAPI
  - corresponding url /test/<int:tid>/question/<int:qid>
  """

  def test_get_404_for_invalid_test(self):
    """
    @description tests GET endpoint for
    - returning 404 for invalid test or question id
    """
    response = self.client.get(self.url_test_question_detail(1, 1))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_404_for_invalid_question(self):
    """
    @description tests GET endpoint for
    - returning 404 for invalid question id
    """
    self.create_new_test(constants.data_new_test)
    response = self.client.get(self.url_test_question_detail(1, 1))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_question_for_valid_test_and_question(self):
    """
    @description tests GET endpoint for
    - returning the corresponding question for 
    the given test and question id
    """
    self.create_new_test(constants.data_new_test)
    self.create_new_question(1, constants.data_new_question)
    response = self.client.get(self.url_test_question_detail(1, 1))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertJSONEqual(response.content, constants.data_response_test_question)


class TestResultsTest(TestBaseTest):
  """
  @extends TestBaseTest
  @description test for
  - view TestResultsAPI
  - corresponding url /test/<int:tid>/registrations/
  @methods:
    - GET (to get results for a test)
    - POST (to register for a test, 
            create new registration)
  """
  def test_get_404_for_invalid_test(self):
    """
    @description tests GET endpoint for
    - returning 404 for invalid test
    """
    response = self.client.get(self.url_test_results(1))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
  def test_register_for_test(self):
    """
    @description tests POST endpoint for
    - register user for test
    - create new registration
    """    
    self.create_new_test(constants.data_new_test)
    response = self.create_new_registration(1)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response = self.client.get(self.url_test_results(1))
    self.assertEqual(response.status_code, status.HTTP_200_OK)