from src.utils.constants import *

data_new_test = {
    "name": "Sample Mock Test",
    "description": "Description for Sample Mock Test",
    "starts_at": TWO_DAYS_LATER,
    "duration": timedelta(hours = 2)
}
data_response = {
    **data_new_test,
    "id": 1,
    "starts_at": data_new_test["starts_at"].strftime(STRTIMEFORMAT),
    "duration": '02:00:00',
    "questions": [],
} 
data_test_offline = {
    **data_new_test,
    "starts_at": TWO_DAYS_AGO,
}
data_response_offline = {
    **data_test_offline,
    "id": 2,
    "starts_at": data_test_offline["starts_at"].strftime(STRTIMEFORMAT),
    "duration": '02:00:00',
    "questions": [],
}
data_test_online = {
    **data_new_test,
    "starts_at": TODAY,
}
data_response_online = {
    **data_test_online,
    "id": 2,
    "starts_at": data_test_online["starts_at"].strftime(STRTIMEFORMAT),
    "duration": '02:00:00',
    "questions": [],
}
data_question_request = {
    "serial": 1,
    "statement": "This is a Sample Test Question Statement",
    "option_1": "Option No. 1",
    "option_2": "Option No. 2",
    "option_3": "Option No. 3",
    "option_4": "Option No. 4",
}
data_new_question = {
    **data_question_request,
    "answer": 1,
}
data_new_test_with_question = {
    **data_new_test,
    "questions": [
      data_new_question
      ]
    }
data_question_response = {
    **data_question_request,
    "id": 1,
}
data_new_test_with_question_response = {
    **data_new_test_with_question,
    "id": 1,
    "starts_at": data_new_test["starts_at"].strftime(STRTIMEFORMAT),
    "duration": '02:00:00',
    "questions": [
      data_question_response
      ]
    }
data_response_test_with_question = {
  **data_new_test,
  "id": 1,
  "starts_at": data_new_test["starts_at"].strftime(STRTIMEFORMAT),
  "duration": '02:00:00',
  "questions": [
    data_question_response,
  ]
}
data_response_test_question = {
    **data_question_request,
    "id": 1,
}
data_new_questions_multiple = [
  {
    **data_question_request,
    "answer": 1,
    "serial": 1,
  },
  {
    **data_question_request,
    "answer": 3,
    "serial": 2,
  },
]
data_questions_multiple_response = [
  {
    **data_question_request,
    "serial": 1,
    "id": 1,
  },
  {
    **data_question_request,
    "serial": 2,
    "id": 2,
  },
]
data_response_test_with_questions_multiple = {
  **data_new_test,
  "id": 1,
  "starts_at": data_new_test["starts_at"].strftime(STRTIMEFORMAT),
  "duration": '02:00:00',
  "questions": data_questions_multiple_response
}