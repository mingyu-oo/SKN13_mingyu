import streamlit as st
import pandas as pd
from utils.db import get_engine  # ✅ SQLAlchemy 엔진 가져오기

def show():
    st.title("⚾ KBO 선수 은퇴 예측")

    # ✅ 팀 목록
    teams = ['(선택)', 'KIA', 'KT', 'LG', 'NC', 'SSG', '두산', '롯데', '삼성', '키움', '한화']
    selected_team = st.selectbox("팀을 선택하세요", teams)

    engine = get_engine()  # ✅ SQLAlchemy 엔진 사용

    # 전체 선수 불러오기
    query = "SELECT name, pic_url, team FROM kbo_final_team_2025"
    df = pd.read_sql(query, engine)

    # 선택된 팀으로 필터링
    if selected_team != '(선택)':
        df = df[df['team'] == selected_team]

    if df.empty:
        st.warning("해당 팀의 선수 정보가 없습니다.")
        return

    # 이름은 보여주고 내부적으로 pic_url 사용
    player_dict = {row['name']: row['pic_url'] for _, row in df.iterrows()}
    selected_name = st.selectbox("선수를 선택하세요", list(player_dict.keys()))
    selected_pic_url = player_dict[selected_name]

    # 검색 버튼
    if st.button("검색"):
        stats_query = f"""
        SELECT *
        FROM kbo_active
        WHERE pic_url = '{selected_pic_url}'
        ORDER BY season DESC
        """
        stat_df = pd.read_sql(stats_query, engine)

        if not stat_df.empty:
            st.image(selected_pic_url, width=200)
            st.markdown(f"### {selected_name} 선수의 시즌 기록 (최신순)")
            stat_cols = ['season', 'AVG', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR',
                         'RBI', 'SB', 'CS', 'BB', 'SO', 'SLG', 'OBP']
            st.dataframe(stat_df[stat_cols])
        else:
            st.warning("해당 선수의 시즌 기록이 없습니다.")

    engine.dispose()  # ✅ 연결 닫기
