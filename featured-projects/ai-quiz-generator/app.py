"""
AI Quiz Generator web app 
- Main app file using Streamlit for web interface

Tiandra M Taylor
"""

# imports
import streamlit as st
from quiz_generator import generate_quiz
from quiz_grader import validate_inputs, calculate_score, get_detailed_results

import os
from dotenv import load_dotenv
# page config
st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon=":memo:",
    layout="centered"
)

# load api key from .env file
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")

if API_KEY == None or API_KEY.strip() == "":
    st.error("API key not found. Please set ANTHROPIC_API_KEY in your .env file.")
    st.stop()

    
# functions
def initialize_session_state():
    """ Transfer session state variables between reruns if applicable """
    
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "results" not in st.session_state:
        st.session_state.results = None
    if "score" not in st.session_state:
        st.session_state.score = None

def reset_app():
    """ reset all session state variables for new quiz"""
    st.session_state.quiz = None
    st.session_state.user_answers = {}
    st.session_state.results = None
    st.session_state.score = None

def main():
    """ main app logic
    3 main states:
        - no quiz exists - show topic input and generate button
        - quiz exists but not submitted - show questions and submit button
        - if submitted - show results and "take another quiz" button"""

    # reset session state variables 
    initialize_session_state()

    # Front end UI things
    st.title(" AI Quiz Generator :memo: ")

    # state 1
    if st.session_state.quiz == None:
        st.write(" Enter a topic to generate a 5-question multiple choice quiz")
        topic = st.text_input(
            "Quiz Topic",
            placeholder = "e.g., Photosynthesis, Ancient Rome, Python Programming",
        )

        # generate button
        if st.button(" Generate Quiz ", type="primary"):
            if topic == None or topic.strip() == "":
                st.error(" Please enter a topic.")
            else:
                # loading spinner while generating quiz
                with st.spinner(f"Generating quiz about '{topic}'..."):
                    quiz = generate_quiz(topic, API_KEY)

                if quiz == None:
                    st.error("Failed to generate quiz. Please try again.")
                else:
                    # store quiz in session state
                    st.session_state.quiz = quiz
                    st.success(f" Quiz generated! {len(quiz['questions'])} questions ready")
                    st.rerun() # rerun to show quiz

    # state 2
    elif st.session_state.results == None:
        quiz = st.session_state.quiz
        st.write(f"Quiz: {quiz['topic']}")
        st.write(f"Answer all {len(quiz['questions'])} questions, then click Submit.")

        # display questions with radio buttons
        for idx, question_dict in enumerate(quiz["questions"], 1):
            st.write(f"**Question {idx}:** {question_dict['question']}")

            # create radio button options
            options = question_dict["options"]
            option_list = [
                f"A. {options['A']}",
                f"B. {options['B']}",
                f"C. {options['C']}",
                f"D. {options['D']}"
            ]

            # key must be unique for each question - streamlit gets confused
            selected = st.radio(
                f"Select an answer for question {idx}:", # can't be empty
                option_list,
                key=f"question_{idx}",
                label_visibility="collapsed" # hide label - don't need to repeat this
            )

            # store user answer - only the letter
            if selected != None:
                answer_letter = selected[0] # only the letter - leave period out
                st.session_state.user_answers[idx] = answer_letter

        # submit button
        if st.button(" Submit Answers ", type="primary"):
            # all questions answered?
            if len(st.session_state.user_answers) != len(quiz["questions"]):
                st.error("Please answer all questions before submitting!")
            else:
                # add user_answers dict to list in correct order
                user_answers_list = []
                for i in range(1, len(quiz["questions"]) + 1):
                    user_answers_list.append(st.session_state.user_answers[i])
            
                # grade quiz 
                with st.spinner("Grading your quiz..."):
                    # validate inputs
                    is_valid, error_msg, questions_list = validate_inputs(quiz, user_answers_list)
                    
                    if is_valid == False:
                        st.error(f"Error: {error_msg}")
                    else:
                        # get correct answers
                        correct_answers_list = []
                        for q in questions_list:
                            correct_answers_list.append(q["correct_answer"])
                        
                        # calculate score & detailed results
                        score = calculate_score(user_answers_list, correct_answers_list)       
                        details = get_detailed_results(questions_list, user_answers_list)

                        # store results in session state
                        st.session_state.score = score
                        st.session_state.results = details

                        # show results
                        st.rerun()

    # state 3
    else:   
        score = st.session_state.score
        results = st.session_state.results
        quiz = st.session_state.quiz

        # show overall score
        st.subheader(f"Quiz Results: {quiz['topic']}")
        # score, correct & incorrect side by side 
        st.write(f" Your Score: **{score['score_display']}** ({score['score_percentage']:.2f}%) ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", score["score_display"])
        with col2:
            st.metric("Correct", score["correct_count"])
        with col3:
            st.metric("Incorrect", score["incorrect_count"])

        st.progress(score["score_percentage"] / 100)
        st.write(f"**{score['score_percentage']:.2f}%**")

        # display each question's result 
        for result in results:
            # get full text for user answer choice and correct answer choice
            user_answer_text = result["options"][result["user_answer"]]
            correct_answer_text = result["options"][result["correct_answer"]]
            
            # correct or incorrect?
            if result["is_correct"] == True:
                st.success(f"**Question {result['question_number']}:** {result['question_text']}") 
                st.write(f"Your answer: **{result['user_answer']}: {user_answer_text}**")

            else:
                st.error(f"**Question {result['question_number']}:** {result['question_text']}")
                st.write(f"Your answer: **{result['user_answer']}: {user_answer_text}**")
                st.write(f"Correct answer: **{result['correct_answer']}: {correct_answer_text}**")

                # BONUS ADDITION
                with st.spinner("Generating explanation..."):
                    from quiz_generator import generate_explanation
                    explanation = generate_explanation(
                        result["question_text"],
                        result["correct_answer"],
                        correct_answer_text,
                        API_KEY
                    )

                if explanation != None:
                    st.info(f"**Explanation:** {explanation}")
                else:
                    st.info(f"**Explanation:** Because that's just how it is. This is one of those 'You can tell it's an aspen because of the way it is.' - Neature Walk quotes.")
        # take another quiz button
        if st.button(" Take Another Quiz ", type="primary"):
            reset_app()
            st.rerun()


# run main app 
if __name__ == "__main__":
    main()
                    