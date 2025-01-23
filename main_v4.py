import streamlit as st
from LLama_config import GoalQuiz, Analyzer, RoadmapGenerator
from setup import ChatSetup
import json

def run_quiz(quiz_type):
    predefined_questions = {
        GoalQuiz: {
            "question": "What are your primary goals for the next year?",
            "options": [
                "Personal growth (learning new skills, self-improvement)",
                "Career progression (promotion, new role, etc.)",
                "Health and fitness (improving physical health, fitness goals)",
                "Other: Please specify your answer."
            ]
        }
    }

    if 'chat_setup' not in st.session_state:
        st.session_state.chat_setup = ChatSetup()
        st.session_state.quiz = quiz_type()
        st.session_state.current_user = "user"
        st.session_state.question_index = 0

    st.subheader(f"Starting {quiz_type.__name__}")

    if st.session_state.question_index == 0:
        # First predefined question
        first_question = predefined_questions[quiz_type]
        st.write(f"Question: {first_question['question']}")
        user_answer = st.radio("Choose an option:", first_question['options'], key=f"{quiz_type.__name__}_first")
        
        if user_answer == "Other: Please specify your answer.":
            user_answer = st.text_input("Please specify your answer:", key=f"{quiz_type.__name__}_first_other")

        if st.button("Next", key=f"{quiz_type.__name__}_first_next"):
            st.session_state.chat_setup.chat_history.append({
                "question": first_question["question"],
                "options": first_question["options"],
                "response": user_answer
            })
            st.session_state.question_index += 1
            st.rerun()

    elif st.session_state.question_index <= 4:
        if 'current_question' not in st.session_state:
            last_response = st.session_state.chat_setup.get_last_user_response()
            formatted_history = st.session_state.chat_setup.get_formatted_chat_history()
            response = st.session_state.quiz.get_quiz_response(last_response, formatted_history, st.session_state.current_user)
            st.session_state.current_question = st.session_state.chat_setup.parse_llm_response(response.content)

        st.write(f"Question: {st.session_state.current_question['question']}")
        user_answer = st.radio("Choose an option:", st.session_state.current_question['options'], key=f"{quiz_type.__name__}_{st.session_state.question_index}")
        
        if user_answer == "Other: Please specify your answer.":
            user_answer = st.text_input("Please specify your answer:", key=f"{quiz_type.__name__}_{st.session_state.question_index}_other")

        if st.button("Next", key=f"{quiz_type.__name__}_{st.session_state.question_index}_next"):
            st.session_state.chat_setup.process_interaction(json.dumps(st.session_state.current_question), user_answer)
            st.session_state.question_index += 1
            if st.session_state.question_index <= 4:
                del st.session_state.current_question
                st.rerun()

    if st.session_state.question_index > 4:
        st.success("Quiz completed!")
        return st.session_state.chat_setup.chat_history

    return None

def main():
    st.title("Goal-Oriented Quiz")

    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    if st.session_state.stage == 0:
        if st.button("Start Goal-Oriented Quiz"):
            st.session_state.stage = 1
            st.rerun()

    if st.session_state.stage == 1:
        goal_quiz_history = run_quiz(GoalQuiz)
        if goal_quiz_history:
            st.session_state.goal_quiz_history = goal_quiz_history
            st.session_state.stage = 2
            st.rerun()

    if st.session_state.stage == 2:
        analyzer = Analyzer()
        goal_analysis = analyzer.get_analysis("Goal-Oriented", st.session_state.goal_quiz_history)

        st.subheader("Goal-Oriented Analysis:")
        st.write(goal_analysis)

        roadmap_generator = RoadmapGenerator()
        career_roadmap = roadmap_generator.get_roadmap(goal_analysis)

        st.subheader("Your Personalized Career Roadmap:")
        st.write(career_roadmap)

        if st.button("Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
