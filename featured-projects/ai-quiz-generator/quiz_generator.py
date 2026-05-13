"""
AI Quiz Generator Module
- Handles all AI interactions for generating quiz questions.

Tiandra M Taylor
"""

# Imports
import anthropic as anth
import json

# Functions
def generate_quiz(topic, api_key, max_retries=3):
    """
    Generate multiple choice quiz about user given topic using Claude.
    Handles prompt creation, API call, response parsing, validation, and retry logic.
    Returns quiz data as dict or None if generation fails.
    """
    connection = anth.Anthropic(api_key=api_key)

    prompt = f"""Generate a multiple choice quiz about the topic: {topic}
    Requirements:
    - Create EXACTLY 5 questions
    - Each question MUST have EXACTLY 4 answer options labeled A, B, C, D
    - Each question MUST have ONLY 1 correct answer
    - Questions should be educational and factually accurate
    - Vary difficulty from easier to hard questions

    Return your response as VALID JSON with this EXACT structure (no extra text):
    {{
        "questions":[
            {{
                "question": "Question text here",
                "options": {{
                    "A": "Option A text",
                    "B": "Option B text",
                    "C": "Option C text",
                    "D": "Option D text"
                }},
                "correct_answer": "A"
            }},
            ...
        ]
    }}
    Return ONLY the JSON. No markdown code blocks, no explanations, just the JSON."""

    for attempt in range(max_retries):
        try:
            print(f" Attempt {attempt + 1} of {max_retries} to generate quiz about '{topic}'.")

            message = connection.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text

            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            quiz_data = json.loads(response_text)

            is_valid, validation_message = validate_quiz(quiz_data)
            if is_valid == False:
                raise ValueError(f" Quiz validation failed: {validation_message}")

            quiz_data["topic"] = topic
            print(f" Quiz about '{topic}' successfully generated with {len(quiz_data['questions'])} questions!")
            return quiz_data

        except json.JSONDecodeError as json_err:
            print(f" Attempt {attempt + 1} failed. JSON parsing error: {json_err}.")
            if attempt == max_retries - 1:
                print(" Max retries reached. Quiz generation failed.")
                return None

        except ValueError as val_err:
            print(f" Attempt {attempt + 1} failed. Error: {val_err}.")
            if attempt == max_retries - 1:
                print(" Max retries reached. Quiz generation failed.")
                return None

        except anth.APIError as api_err:
            print(f" Attempt {attempt + 1} failed. API error: {api_err}.")
            if attempt == max_retries - 1:
                print(" Max retries reached. Quiz generation failed.")
                return None

        except Exception as e:
            print(f" Attempt {attempt + 1} failed. Error type: {type(e)}, Message: {e}.")
            if attempt == max_retries - 1:
                print(" Max retries reached. Quiz generation failed.")
                return None


def validate_quiz(quiz_data):
    """
    Validate quiz structure and content before displaying to user.
    Returns tuple (is_valid: bool, message: str).
    """
    if "questions" not in quiz_data:
        return False, "Response is missing the 'questions' field"

    if not isinstance(quiz_data["questions"], list):
        return False, "'questions' field is not a list"

    if len(quiz_data["questions"]) != 5:
        return False, f"Expected exactly 5 questions, got {len(quiz_data['questions'])}"

    for idx, question_dict in enumerate(quiz_data["questions"], 1):
        if "question" not in question_dict:
            return False, f"Question {idx} is missing the 'question' field"
        if "options" not in question_dict:
            return False, f"Question {idx} is missing the 'options' field"
        if "correct_answer" not in question_dict:
            return False, f"Question {idx} is missing the 'correct_answer' field"

        options = question_dict["options"]
        if not isinstance(options, dict):
            return False, f"'options' in question {idx} is not a dictionary"

        required_letters = ["A", "B", "C", "D"]
        for letter in required_letters:
            if letter not in options:
                return False, f"Option '{letter}' is missing in question {idx}"

        if question_dict["correct_answer"] not in required_letters:
            return False, f"'correct_answer' in question {idx} is not one of {required_letters}"

    return True, "Quiz data is valid!"


def display_quiz(quiz_data):
    """
    Print quiz to console — used for testing and debugging.
    """
    if quiz_data is None:
        print(" No quiz data to display.")
        return

    print(f"\n QUIZ: {quiz_data['topic']}\n")
    for idx, question_dict in enumerate(quiz_data["questions"], 1):
        print(f" Question {idx}: {question_dict['question']}")
        for letter in ["A", "B", "C", "D"]:
            print(f"  {letter}. {question_dict['options'][letter]}")
        print(f"  Correct Answer: {question_dict['correct_answer']}")
        print()


def generate_explanation(question, correct_answer, correct_option_text, api_key):
    """
    Generate a brief explanation for why an answer is correct.
    Only called for incorrectly answered questions.
    """
    connection = anth.Anthropic(api_key=api_key)

    prompt = f"""Explain why this answer is correct in 2-3 sentences. Be educational, factual, and concise.
    Question: {question}
    Correct Answer: {correct_answer}. {correct_option_text}
    Provide a brief explanation of why this is the correct answer."""

    try:
        message = connection.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()

    except Exception as e:
        print(f" Error generating explanation: {e}")
        return None


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    test_topic = str(input(" Enter a quiz topic: "))
    print(f"Testing quiz generation for topic: {test_topic}")

    quiz = generate_quiz(test_topic, api_key)
    try:
        display_quiz(quiz)
        print(f"\n Raw JSON:\n {json.dumps(quiz, indent=4)}")
    except Exception:
        print("Failed — nothing to display.")
