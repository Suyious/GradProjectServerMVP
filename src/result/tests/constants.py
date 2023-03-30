from src.utils.constants import *

data_new_test = {
    "name": "Sample Mock Test",
    "description": "Description for Sample Mock Test",
    "starts_at": TWO_DAYS_LATER,
    "duration": timedelta(hours = 2)
}
data_question_request = {
    "statement": "This is a Sample Test Question Statement",
    "option_1": "Option No. 1",
    "option_2": "Option No. 2",
    "option_3": "Option No. 3",
    "option_4": "Option No. 4",
}
data_question_multiple = [ { **data_question_request, "serial": i + 1, "answer": i % 4 + 1 } for i in range(0, 8)]
data_new_test_with_questions = {
    **data_new_test,
    "questions": 
      data_question_multiple
    }
data_new_response = {
    "question_id": 1,
    "answer": 2
}