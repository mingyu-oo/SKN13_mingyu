import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# DB 연결 함수
def get_connection():
    username = 'SKN13_2nd_2Team'
    password = '1111'
    host = '127.0.0.1'
    port = '3306'
    database = 'brp'
    return create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# 데이터 불러오기
@st.cache_data
def load_data():
    engine = get_connection()
    query = "SELECT * FROM kbo_active_nodrop_total;"
    df = pd.read_sql(query, engine)
    return df

# 데이터 로드
df = load_data()

st.title("⚾ KBO 현역 선수 조회")

# 🔍 이름/출생연도 필터
name_query = st.text_input("선수 이름으로 검색 (전체 또는 일부)")
birth_year_query = st.text_input("출생 연도로 검색 (예: 1999)")


# ✅ 필터 적용
filtered_df = df.copy()

if name_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(name_query, case=False, na=False)]

if birth_year_query:
    if birth_year_query.isdigit():
        filtered_df = filtered_df[filtered_df['birth_year'] == int(birth_year_query)]
    else:
        st.warning("출생 연도는 숫자로 입력하세요.")

# 🎯 결과 출력
st.write(f"조회된 선수 수: {len(filtered_df)}명")
st.dataframe(filtered_df)