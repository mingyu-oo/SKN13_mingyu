##################################################################
#  streamlit/04_streamlit_chat_exam_session_state_llm_streaming.py
#  챗봇 대화 관련 위젯 

# 1. chat_input() : 사용자 입력을 받는 위젯
# 2. chat_message() : 메세지를 container(내용 창)에 입력하는 위젯.

# chat_input(): str
# - 사용자 입력을 받는 위젯.
# - 사용자가 입력한 내용은 엔터를 치면 반환되고, 입력폼에 작성된 글은 지워진다.
# - 코드가 어디에 위치하든지 상관없이 **맨 아래**에 위치한다.
# - 주요파라미터
#    - placeholder:str - 입력폼에 표시할 힌트
#    - key:str|int - 위젯의 고유 식별자
#    - max_chars: int - 최대 입력 글자수. None(default): 제한 없음
#    - on_submit: Callable - 엔터를 눌렀을 때(submit) 호출할 함수
# - https://docs.streamlit.io/develop/api-reference/chat/st.chat_input

# chat_message(name, *, avatar=None): Container
# - 메세지를 container(내용 창)에 입력하는 위젯.
# - 반환된 container에 write() 하거나 with 문을 이용해 write() 한다.
# - parameter
#    - name:str =  입력하는 메세지 작성자. ("assistant", "ai", "human", "user" or str)
#        - "assistant", "ai": 챗봇이 작성한 메세지, "human", "user": 사용자가 작성한 메세지
#    - avatar: str|st.image|None 
#        - 문자열, emoji, 이미지 등을 사용하여 아바타 이미지를 표현한다.
#        - 메세지 작성자를 표현하는 아바타 이미지. 
#        - avatar=None 이면 name에 따라 결정된다. 
#              - name이 user, human, assistant, ai 일 경우 정해진 아이콘이 사용된다.
#              - name이 다른 문자열일 경우 첫번째 글자를 아바타로 사용한다.
#        - avatar 를 지정하면 지정한 avatar를 사용한다.
#              - 단 이름이 user, human, assistant, ai 일 경우 default avatar 가 나오고 그 뒤에 지정한 avatar가 나온다.
# - https://docs.streamlit.io/develop/api-reference/chat/st.chat_message

# st.session_state: 사용자의 상태를 저장하는 객체
#   - 페이지가 reload(rerun) 되더라도 유지 되야하는 값들을 저장하는 저장소 역할.
#       - 변수에 저장된 값은 rerun시 사라지게 된다. 그런데 rerun 후에도 그 값이 유지 되어야 하는 경우가 있다. 이런 값들을 저장하는 저장소.
#       - dictionary 형식으로 key=value 형태로 값을 저장한다.
#   - key 가 있는지 여부 확인
#       - in 연산자를 이용해 확인한다. `if "key" in st.session_state:` 형식으로 확인.
#   - 값 조회
#       - st.session_state.key 또는 st.session_state['key'] 를 이용해 조회한다.
#   - 값 저장
#       - st.session_state.key = value 또는 st.session_state['key'] = value 를 이용해 저장한다.
#       - 값을 저장하려는 key가 없으면 KeyError 발생한다. 그래서 미리 key를 생성해 놓고 사용해야 한다.
# 
#   - https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
##################################################################
import streamlit as st
import random
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# API KEY 불러오기.
load_dotenv()

# LLM model 생성
@st.cache_resource  # cache에 올리겠다는 뜻. cache에 올라가 있으니 rerun해도 이 함수를 실행하지 않음. 다시 껐다 켜야함
def get_llm_model():
    load_dotenv()
    return ChatOpenAI(model_name = "gpt-4o-mini")

model = get_llm_model()   # cache에 올려져 있는걸 사용.

st.title("Chatbot + Session State + LLM 연동 튜토리얼")

# Session State 생성
## session_state : dictionary 구현체, 시작 ~ 종료할 때 까지 사용자 별로 유지되어야 하는 값들을 저장하는 곳

# 0. 대화 내욕을 session_state의 "messages" : list 로 저장
# 1. session state에 messages key 조회(없으면 생성)
if "messages" not in st.session_state:   # return T/F
    st.session_state["messages"] = []    # 대화 내용들을 저장할 list를 "messages" 키로 저장


# 기존 대화 이력 출력
for message in st.session_state["messages"]:
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

    with st.chat_message("ai"):
        message_placeholder = st.empty()    # updatee가 가능한 container
        full_message = ""   # LLM이 응답하는 토큰들을 저장할 문자열 변수.
        for token in model.stream(prompt):
            full_message += token.content
            message_placeholder.write(full_message) # 기존 내용을 full_message로 갱신.
            print(full_message)
            print("-"*50)
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