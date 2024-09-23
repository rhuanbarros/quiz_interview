import uuid
from supabase import create_client, Client
import streamlit as st
import pandas as pd

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


#############################################
############### STATE
#############################################

FLOW_CONFIGURATION = 0
FLOW_QUESTION = 1
FLOW_RESULTS = 2

if "first_run" not in st.session_state:
    st.session_state.first_run = True

if "page_flow" not in st.session_state:
    st.session_state.page_flow = FLOW_CONFIGURATION

if "question" not in st.session_state:
    st.session_state.question = None

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

if "answered_correct" not in st.session_state:
    st.session_state.answered_correct = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "subject_matter_selected" not in st.session_state:
    st.session_state.subject_matter_selected = []

if "level_selected" not in st.session_state:
    st.session_state.level_selected = []

if "show_elaborate_more" not in st.session_state:
    st.session_state.show_elaborate_more = False

if "elaborate_more_content" not in st.session_state:
    st.session_state.elaborate_more_content = ""

#############################################
############### GENERATIVE AI
#############################################

print('Inicializando LLM')
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

prompt_elaborate_more = PromptTemplate(
    template="""
                TASK CONTEXT:
                I am studying machine learning practicing some questions.
                
                TASK DESCRIPTION:
                I need you to act like a professor.
                I need you to think critical if the said correct answer is indeed correct.
                You should give a elaborated explanation.
                                
                TASK REQUIREMENTS:
                Use at least 2 sentences to explain your answer.
                
                QUESTION:
                {question}
            """,
    input_variables=["question"]
)

#############################################
############### LISTENERS
#############################################

def on_click_verify_answer(answer):
    print("----------------- on_click_verify_answer ------------------")
    question = st.session_state.question

    if answer != "DONT_KNOW":
        answered_correct = answer == question["answer_correct"]
        response = supabase.table('answer').insert(
            {
                "question_id": question['id'],
                "correct_answer": answered_correct,
                "session_id": st.session_state.session_id
            }).execute()
        st.session_state.answered_correct = answered_correct

    print("dont know")
    st.session_state.show_explanation = True

def on_click_end_session():
    st.session_state.page_flow = FLOW_RESULTS


def on_click_next():
    st.session_state.show_explanation = False
    st.session_state.show_elaborate_more = False
    load_question()

def on_click_start_over_again():
    # reset app state
    st.session_state.first_run = True
    st.session_state.page_flow = FLOW_CONFIGURATION
    st.session_state.question = None
    st.session_state.show_explanation = False
    st.session_state.answered_correct = None
    # st.session_state.answered_questions = []
    # st.session_state.subject_matter_1s_list_selected = []
    # st.session_state.topic_descriptions_list_selected = []
    # st.session_state.use_subject_matter_1_filter = True
    # st.session_state.questions_available = False

def on_click_start(subject_matter_selected, level_selected):
    if "All" in subject_matter_selected:
        subject_matter_selected.remove("All")
    st.session_state.subject_matter_selected = subject_matter_selected
    
    if "All" in level_selected:
        level_selected.remove("All")
    st.session_state.level_selected = level_selected
    
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.page_flow = FLOW_QUESTION

    load_question()

def on_click_elaborate_more_the_explanation():
    chain = prompt_elaborate_more | llm
    parameters = {
        "question": st.session_state.question
    }
    response = chain.invoke(parameters)

    st.session_state.show_elaborate_more = True
    st.session_state.elaborate_more_content = response.content


#############################################
############### OTHER FUNCTIONS
#############################################

def load_question():
    print("----------------- LOADING QUESTION FUNCTION ------------------")

    subject_matter_selected = st.session_state.subject_matter_selected
    level_selected = st.session_state.level_selected

    query = supabase.table("get_question").select("*")

    for item in subject_matter_selected:
        query = query.eq("subject_matter", item)
    
    # print("level_selected")
    # print(level_selected)
    for item in level_selected:
        query = query.eq("level", item)

    response = query.neq("session_id", st.session_state.session_id).limit(1).execute()

    print(response)
    
    qty = len(response.data)
    print(qty)

    if qty > 0:
        st.session_state.question = response.data[0]
        print(st.session_state.question)

    else:
        st.info("No more questions available")
        # st.session_state.no_more_questions_available = True
        st.session_state.page_flow = FLOW_RESULTS

@st.cache_resource
def get_subject_matter():
    response = supabase.table('get_subject_matter').select("*").execute()
    data_list = ["All"]
    for row in response.data:
        data_list.append(row["subject_matter"])
    
    return data_list

@st.cache_resource
def get_level():
    response = supabase.table('get_level').select("*").execute()
    data_list = ["All"]
    for row in response.data:
        data_list.append(row["level"])
    
    return data_list

#############################################
############### WIDGETS
#############################################

def show_config_train():
    st.write(
        rf"""
        #### Configuration
        """
    )
    subject_matter_selected = st.multiselect("Subject matter", get_subject_matter(), ["All"])
    get_level_selected = st.multiselect("Level", get_level(), ["All"])
    
    st.button("Start!", on_click=on_click_start, args=[subject_matter_selected, get_level_selected])

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

    col1, col2 = st.columns([1, 10])
    col1.button("A", on_click=on_click_verify_answer, args=["a"])
    col2.write(question["answer_a"])

    col1, col2 = st.columns([1, 10])
    col1.button("B", on_click=on_click_verify_answer, args=["b"])
    col2.write(question["answer_b"])

    col1, col2 = st.columns([1, 10])
    col1.button("C", on_click=on_click_verify_answer, args=["c"])
    col2.write(question["answer_c"])

    col1, col2 = st.columns([1, 10])
    col1.button("D", on_click=on_click_verify_answer, args=["d"])
    col2.write(question["answer_d"])

    # in this case, the button is showed in other section of UI
    if st.session_state.show_explanation == False:

        _, col2, col3 = st.columns([1, 3, 3])
        col2.button("I don't know", key="btn_dont_know",
                    on_click=on_click_verify_answer, args=["DONT_KNOW"])
        col3.button("Ends session", key="btn_end_session", on_click=on_click_end_session, )


def show_explanation():
    st.write("")  # Empty string
    
    if st.session_state.answered_correct != None:
        if st.session_state.answered_correct:
            st.success("Correct answer!")
        else:
            st.error("Wrong answer!")
        st.session_state.answered_correct = None
        
    explanation = st.session_state.question["explanation"]
    
    # st.write("")  # Empty string
    st.write("")  # Empty string
    st.write(
        rf"""
        #### Explanation
        """
    )

    st.info(f'{explanation}', icon="ℹ️")
    
    st.write("")  # Empty string
    st.write("")  # Empty string
    
    _, col2, col3, col4, _ = st.columns([5,7,14,7,5])
    
    col2.button("Ends session", key="btn_end_session", on_click=on_click_end_session, )
    
    col3.button("Elaborate more the explanation", on_click=on_click_elaborate_more_the_explanation)
    
    col4.button("Next", on_click=on_click_next)

def show_results():
    st.write(
        rf"""
        #### Results
        """
    )
    
    response = supabase.table('get_report').select("*").eq("session_id", st.session_state.session_id).execute()
    st.write( pd.DataFrame(response.data) )

    st.button("Start over again", on_click=on_click_start_over_again)

def show_elaborate_more():
    st.info(f'{st.session_state.elaborate_more_content}', icon="ℹ️")

#############################################
############### WIDGET CONTROL
#############################################

st.set_page_config(
    page_title="Machine Learning Interview Preparation Trainer",
    page_icon="💪💪💪",
)

st.write(
    """
    # Machine Learning Interview Preparation Trainer
    """
)


match st.session_state.page_flow:
    case 0: # FLOW_CONFIGURATION
        show_config_train()

    case 1:  # FLOW_QUESTION
        show_question()

        if st.session_state.show_explanation:
            show_explanation()
        if st.session_state.show_elaborate_more:
            show_elaborate_more()

    case 2: # FLOW_RESULTS
        show_results()
