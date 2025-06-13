import streamlit as st
import pandas as pd
from utils.db import get_engine


# 메인 함수 정의
def show():
    st.title("여러 모델 사용")
    st.write("모델 학습과 그에 따른 평가지표")
