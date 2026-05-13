# AI Quiz Generator 

**Python · Streamlit · Claude API · Error Handling**

---

Built as a take-home interview project, this is an end-to-end AI-powered quiz application that generates, delivers, and grades a 5-question multiple choice quiz on any topic a user provides. I wanted to go beyond a basic API call and build something that felt production-ready — with real validation, retry logic, and a clean user experience.

The app is split into three modules: 
- A generator that calls the Claude API and validates the response structure
- A grader that scores answers and returns per-question detail
- A Streamlit frontend that ties it together with session state management

For incorrect answers, the app makes a second API call to generate a plain-language explanation of why the correct answer is right.


**Key features:**
- Generates a validated 5-question quiz on any topic using the Claude API
- Retry logic (up to 3 attempts) handles malformed or failed API responses
- Instant grading with correct/incorrect breakdown per question
- AI-generated explanations for missed answers
- Modular architecture — generator, grader, and UI are fully independent

---

## Getting Started

### Prerequisites
- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation
```bash
git clone https://github.com/Tiandra123/ai-quiz-generator.git
cd ai-quiz-generator
pip install -r requirements.txt
```

### Add Your API Key
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### Run
```bash
streamlit run app.py
```
App opens at `http://localhost:8501`

---

## Architecture

```
app.py              # Streamlit UI and session state management
quiz_generator.py   # Claude API integration, validation, retry logic
quiz_grader.py      # Input validation, scoring, detailed results
requirements.txt    # Dependencies
```
