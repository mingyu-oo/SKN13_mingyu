import streamlit as st
import pandas as pd
from utils.db import get_engine

# 메인 함수 정의
def show():
    st.title("학습")
    st.write("학습과정과 그 에 따른 과정!~~~~~!")
