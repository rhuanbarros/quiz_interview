import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from supabase import create_client, Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.set_page_config(
    page_title="Machine Learning Interview Preparation Trainer",
    page_icon="💪💪💪",
)

st.write(
    """
    # Machine Learning Interview Preparation Trainer
    """
)

FLOW_CONFIGURATION = 0
FLOW_QUESTION = 1
FLOW_RESULTS = 2

if "first_run" not in st.session_state:
    st.session_state.first_run = True
    
if "page_flow" not in st.session_state:
    st.session_state.page_flow = FLOW_QUESTION
    
if "question" not in st.session_state:
    st.session_state.question = None

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

def load_question():
    print("----------------- LOADING QUESTION FUNCTION ------------------")
        
    response = supabase.table("get_question").select("*").execute()
    qty = len(response.data)

    if qty > 0:
        st.session_state.question = response.data[0]
        print(st.session_state.question)

    else:
        st.info("No more questions available")
        # st.session_state.no_more_questions_available = True
        st.session_state.page_flow = FLOW_RESULTS

def on_click_verify_answer(answer):
    print("----------------- on_click_verify_answer ------------------")
    question = st.session_state.question    
    
    if answer != "DONT_KNOW":
        if answer == question["answer_correct"]:
            correct_answer = True
            
    else:
        print("dont know")
        st.session_state.show_explanation = True


def show_question():
    print("----------------- show_question ------------------")
    question = st.session_state.question

    st.write(
        rf"""            
        #### {question["question"]}
        
        - Subject matter: {question["subject_matter"]}
        - Topic description: {question["topic_description"]}
        - Level: {question["level"]}
        """
    )

    st.write("")  # Empty string

    col1, col2 = st.columns([1,10])
    col1.button("A", on_click=on_click_verify_answer, args=["a"])
    col2.write(question["answer_a"])
    
    col1, col2 = st.columns([1,10])
    col1.button("B", on_click=on_click_verify_answer, args=["b"])
    col2.write(question["answer_b"])
    
    col1, col2 = st.columns([1,10])
    col1.button("C", on_click=on_click_verify_answer, args=["c"])
    col2.write(question["answer_c"])
    
    col1, col2 = st.columns([1,10])
    col1.button("D", on_click=on_click_verify_answer, args=["d"])
    col2.write(question["answer_d"])

    # in this case, the button is showed in other section of UI
    if st.session_state.show_explanation == False:
        
        _, col2, col3 = st.columns([1,3,3])
        col2.button("I don't know", key="btn_dont_know", on_click=on_click_verify_answer, args=["DONT_KNOW"])
        # col3.button("Ends session", key="btn_end_session", on_click=on_click_end_session, )
        col3.button("Ends session", key="btn_end_session")







match st.session_state.page_flow:
    # case 0: # FLOW_CONFIGURATION
    #     supabase.table('question_filters').delete().gt('id', 0).execute()
    #     show_config_train()
    
    case 1: # FLOW_QUESTION
        if st.session_state.first_run:
            st.session_state.first_run = False
            load_question()
            
        show_question()

        # if st.session_state.show_explanation:
        #     show_explanation()
    
    # case 2: # FLOW_RESULTS
    #     show_results()