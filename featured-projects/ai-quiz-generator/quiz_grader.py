"""
Quiz Grader Module
- Handles scoring and calculates result for quizzes.

Tiandra M Taylor
"""

# imports


# functions
def validate_inputs(quiz_data, user_answers):
    """
    Validate quiz data and answer lists (user_answers and correct_answers)
    Needs to return:
        tuple (is_valid: bool, error_message: str or None, questions_list: list or None)
    """
    # check quiz data 
    if quiz_data == None:
        return False, "Quiz data cannot be None", None
    
    if "questions" not in quiz_data:
        return False, "Quiz data is missing 'questions' field", None
    
    questions = quiz_data["questions"]
    
    if questions == None or len(questions) == 0:
        return False, "Quiz has no questions", None
    
    # Check user_answers
    if user_answers == None:
        return False, "User answers cannot be None", None
    
    if len(user_answers) == 0:
        return False, "User answers cannot be empty", None
    
    # Check if counts match
    if len(user_answers) != len(questions):
        return False, f"Answer count ({len(user_answers)}) doesn't match question count ({len(questions)})", None
    
    # Everything is valid
    return True, None, questions


def calculate_score(user_answers, correct_answers):
    """
    Calculate the quiz score based on user answers and correct answers.
    Function needs to handle:
    - comparing user answers to correct answers (one by one) & calc total score / percentage
    - NOTES:
        - return dict of score details in this format:
        {
                "total_questions": 5,
                "correct_count": 3,
                "incorrect_count": 2,
                "score_percentage": 60.0,
                "score_display": "3/5"
            }
        OR None if inputs are invalid

    """
    

    correct_count = 0
    total_questions = len(correct_answers)

    # loop through both lists and compare - use zip
    for i in zip(user_answers, correct_answers):
        if i[0] == i[1]:
            correct_count += 1


    # calculate it
    incorrect_count = total_questions - correct_count
    score_percentage = (correct_count / total_questions) * 100

    # result dict
    result = {
        "total_questions": total_questions,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "score_percentage": score_percentage,
        "score_display": f"{correct_count}/{total_questions}"
    }
    
    return result

def get_detailed_results(questions, user_answers):
    """
    get detailed results per question - must show correct answer and user answer for each question
    Needs to return:
    list of dicts in this format:
            [
                {
                    "question_number": 1,
                    "question_text": "What is...",
                    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
                    "user_answer": "A",
                    "correct_answer": "A",
                    "is_correct": True
                },
                ...
            ]
    """
    results = []
    for idx, question_dict in enumerate(questions, 1):
        user_ans = user_answers[idx - 1] # idx starts at 1 but list at 0
        correct_ans = question_dict["correct_answer"]

        result_detailed = {
            "question_number": idx,
            "question_text": question_dict["question"],
            "options": question_dict["options"],
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": user_ans == correct_ans
        }

        results.append(result_detailed)

    return results


# test code - body
if __name__ == "__main__":
    # only runs if this file is executed directly
    # test data
    # Create fake quiz data
    fake_quiz = {
        "topic": "Test Topic",
        "questions": [
            {
                "question": "What is 2 + 2?",
                "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
                "correct_answer": "B"
            },
            {
                "question": "What is the capital of France?",
                "options": {"A": "London", "B": "Berlin", "C": "Paris", "D": "Madrid"},
                "correct_answer": "C"
            },
            {
                "question": "How many days in a week?",
                "options": {"A": "5", "B": "6", "C": "7", "D": "8"},
                "correct_answer": "C"
            },
            {
                "question": "What color is the sky?",
                "options": {"A": "Blue", "B": "Green", "C": "Red", "D": "Yellow"},
                "correct_answer": "A"
            },
            {
                "question": "What is 10 / 2?",
                "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
                "correct_answer": "C"
            }
        ]
    }
    # Simulate user answers 
    fake_user_answers = ["A", "C", "B", "D", "A"]

    # Validate inputs
    is_valid, error_msg, questions_list = validate_inputs(fake_quiz, fake_user_answers)
    if is_valid == False:
        print(f"Input validation failed: {error_msg}")
    else:
        print(f"{len(questions_list)} questions and {len(fake_user_answers)} user answers.")

        # calculate score
        # get correct answers
        correct_answers_list = []
        for q in questions_list:
            correct_answers_list.append(q["correct_answer"])

        score = calculate_score(fake_user_answers, correct_answers_list)
        print(f"Score: {score['score_display']} ({score['score_percentage']}")
        print(f" Correct: {score['correct_count']}, Incorrect: {score['incorrect_count']}")

        # get detailed results
        details = get_detailed_results(questions_list, fake_user_answers)
        print(f"Detailed Results Example: \n Question: {details[0]['question_text']}\n Answer Choices: {details[0]["options"]}\n User Answer: {details[0]['user_answer']}\n Correct Answer: {details[0]['correct_answer']}\n Is Correct: {details[0]['is_correct']}")
        