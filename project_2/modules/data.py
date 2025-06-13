import streamlit as st
import pandas as pd
from utils.db import get_engine


# 메인 함수 정의
def show():
    st.title("산출물")
    st.write("데이터 전처리 및 시각화")

