############################################################################
#  streamlit/05_streamlit_chat_exam_session_state_llm_streaming_memory2.py
############################################################################
from debugpy import connect
from requests import session
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import SQLChatMessageHistory
from sqlalchemy import create_engine
from langchain_core.runnables import RunnableWithMessageHistory

# API KEY 불러오기.
load_dotenv()

# LLM model 생성
@st.cache_resource  # cache에 올리겠다는 뜻. cache에 올라가 있으니 rerun해도 이 함수를 실행하지 않음. 다시 껐다 켜야함
def get_llm_model():
    load_dotenv()
    model = ChatOpenAI(model_name = "gpt-4o-mini")
    prompt_template = ChatPromptTemplate(
    messages = [
        ("system" , "답변을 100단어 이내로 작성해줘"),
        MessagesPlaceholder(variable_name = "history", optional = True),    # 대화 이력
        ("user", "{query}")    # 사용자 입력
        ]
    )
    return prompt_template | model | StrOutputParser()

@st.cache_resource
def get_chain():
    # RunnableWithMessageHistory를 생성해서 반환
    runnable = get_llm_model()
    engine = create_engine("sqlite:///chat_history.sqlite")
    chain = RunnableWithMessageHistory(
        runnable=runnable,
        get_session_history = lambda session_id : SQLChatMessageHistory(session_id = session_id, connection = engine),
        input_messages_key= "query",    # 사용자 입력
        history_messages_key= "history"
    )
    return chain


model = get_chain()   # cache에 올려져 있는걸 사용, chain이 넘어옴.

st.title("Chatbot + Session State + LLM 연동 튜토리얼")


# Session State 생성
## session_state : dictionary 구현체, 시작 ~ 종료할 때 까지 사용자 별로 유지되어야 하는 값들을 저장하는 곳

# 0. 대화 내욕을 session_state의 "messages" : list 로 저장
# 1. session state에 messages key 조회(없으면 생성)
if "messages" not in st.session_state:   # return T/F
    st.session_state["messages"] = []    # 대화 내용들을 저장할 list를 "messages" 키로 저장


# session_state에서 session_id를 조회, 없으면 빈 상태값을 저장.
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None


# Sidebar에 session_id 입력 위젯 생성
session_id = st.sidebar.text_input("Session ID", placeholder="ID를 입력하세요.")


# 기존 대화 이력 출력
message_list = st.session_state["messages"] # 변수로 저장.
for message in message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# user의 prompt를 입력 받는 위젯
prompt = st.chat_input("User Prompt")    # user가 입력한 문자열을 반환.


## 대화 작업
if prompt is not None:
    # session_state의 messages에 대화 내역을 저장
    st.session_state["messages"].append({"role" : "user", "content" : prompt})
    with st.chat_message("user"):
        st.write(prompt)
    # 입력된 session_id 를 상태값으로 저장
    if st.session_state["session_id"] is None:
        st.session_state["session_id"] = session_id

    config = {"configurable" : {"session_id" : st.session_state["session_id"]}}
    print(session_id)

    with st.chat_message("ai"):
        message_placeholder = st.empty()    # update가 가능한 container
        full_message = ""   # LLM이 응답하는 토큰들을 저장할 문자열 변수.
        for token in model.stream({"query" : prompt}, config = config):
            full_message += token
            message_placeholder.write(full_message) # 기존 내용을 full_message로 갱신.
        st.session_state["messages"].append({"role" : "ai", "content" : full_message})







# # 대화 내역을 chat_message container에 출력
# for message_dict in st.session_state["messages"]:
#     with st.chat_message(message_dict["role"]):
#         st.write(message_dict["content"])


# [
#     {
#     "role" : "user", "content" : prompt
#     },
#     {
#     "role" : "AI", "content" : ai_message
#     }
# ]