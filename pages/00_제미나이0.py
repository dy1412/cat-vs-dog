import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(page_title="Dog vs Cat Global Battle", layout="wide")

# CSS를 활용한 귀여운 폰트 및 스타일 부여
st.markdown("""
    <style>
    .main-title { font-size: 38px !important; font-weight: bold; text-align: center; color: #FF4B4B; }
    .sub-title { font-size: 18px !important; text-align: center; color: #555555; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🐶 세계 강아지 vs 고양이 세력도 🐱</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">실제 글로벌 통계를 기반으로 재구성한 반려동물 대시보드</p>', unsafe_allow_html=True)

# 2. 데이터 구축 (실제 통계 기반 시계열 데이터 가공)
# 미국, 중국, 러시아, 일본, 프랑스, 영국, 브라질 등의 실제 추정치를 연도별로 확장
@st.cache_data
def load_data():
    data = []
    base_stats = [
        {"Country": "United States", "Continent": "North America", "Dog_2024": 70.0, "Cat_2024": 74.0, "Growth": 1.02},
        {"Country": "China", "Continent": "Asia", "Dog_2024": 27.4, "Cat_2024": 53.1, "Growth": 1.05},
        {"Country": "Russia", "Continent": "Europe", "Dog_2024": 17.6, "Cat_2024": 22.0, "Growth": 1.01},
        {"Country": "Japan", "Continent": "Asia", "Dog_2024": 8.5, "Cat_2024": 9.5, "Growth": 0.99},
        {"Country": "United Kingdom", "Continent": "Europe", "Dog_2024": 12.5, "Cat_2024": 12.0, "Growth": 1.03},
        {"Country": "Brazil", "Continent": "South America", "Dog_2024": 55.0, "Cat_2024": 22.0, "Growth": 1.04},
        {"Country": "France", "Continent": "Europe", "Dog_2024": 7.5, "Cat_2024": 15.0, "Growth": 1.01},
        {"Country": "Germany", "Continent": "Europe", "Dog_2024": 10.5, "Cat_2024": 15.5, "Growth": 1.02},
        {"Country": "India", "Continent": "Asia", "Dog_2024": 10.2, "Cat_2024": 2.0, "Growth": 1.08},
        {"Country": "Australia", "Continent": "Oceania", "Dog_2024": 6.3, "Cat_2024": 4.9, "Growth": 1.02},
    ]
    
    # 2020년부터 2024년까지의 애니메이션용 시계열 데이터 생성
    for year in range(2020, 2025):
        for nation in base_stats:
            years_diff = year - 2024
            # 역산 및 정산하여 연도별 데이터 생성
            dog_pop = round(nation["Dog_2024"] * (nation["Growth"] ** years_diff), 1)
            cat_pop = round(nation["Cat_2024"] * (nation["Growth"] ** years_diff), 1)
            total_pop = dog_pop + cat_pop
            
            data.append({
                "Year": year,
                "Country": nation["Country"],
                "Continent": nation["Continent"],
                "Dogs (Millions)": dog_pop,
                "Cats (Millions)": cat_pop,
                "Total Pets (Millions)": total_pop,
                "Leading Team": "🐶 Team Dog" if dog_pop > cat_pop else "🐱 Team Cat"
            })
            
    return pd.DataFrame(data)

df = load_data()

# 3. 팀 토글 (Radio UI 활용)
st.sidebar.header("🕹️ 세력 선택")
team_toggle = st.sidebar.radio(
    "어느 팀의 데이터를 메인으로 보시겠습니까?",
    ["통합 비교 ⚔️", "강아지 팀 🐶", "고양이 팀 🐱"]
)

# 4. 애니메이션 버블 차트 구역
st.subheader("📊 연도별 반려동물 인구 변화 (버블 애니메이션)")

# 토글에 따른 색상 기준 및 변수 동적 변경
if team_toggle == "강아지 팀 🐶":
    color_col = "Dogs (Millions)"
    size_col = "Dogs (Millions)"
    y_col = "Dogs (Millions)"
elif team_toggle == "고양이 팀 🐱":
    color_col = "Cats (Millions)"
    size_col = "Cats (Millions)"
    y_col = "Cats (Millions)"
else:
    color_col = "Leading Team"
    size_col = "Total Pets (Millions)"
    y_col = "Total Pets (Millions)"

fig_bubble = px.scatter(
    df,
    x="Country",
    y=y_col,
    animation_frame="Year",
    animation_group="Country",
    size=size_col,
    color=color_col,
    hover_name="Country",
    facet_col="Continent",
    size_max=60,
    height=500,
    color_discrete_map={"🐶 Team Dog": "#FF6B6B", "🐱 Team Cat": "#4D96FF"} if team_toggle == "통합 비교 ⚔️" else None,
    color_continuous_scale="Reds" if team_toggle == "강아지 팀 🐶" else "Blues" if team_toggle == "고양이 팀 🐱" else None
)

fig_bubble.update_layout(
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis_title="",
    yaxis_title="반려동물 수 (백만 마리)"
)
st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("---")

# 5. 드릴다운 (Drill-down) 구역
st.subheader("🔍 대륙별 데이터 상세 보기 (드릴다운)")

# (1단계: 대륙 선택)
selected_continent = st.selectbox(
    "자세히 보고 싶은 대륙을 선택하세요 👇 (드릴다운 실행)",
    options=["전체 보기"] + list(df["Continent"].unique())
)

# 데이터 필터링 (가장 최신년도인 2024년 기준)
df_2024 = df[df["Year"] == 2024]

if selected_continent == "전체 보기":
    drill_data = df_2024.groupby("Continent")[["Dogs (Millions)", "Cats (Millions)"]].sum().reset_index()
    x_axis = "Continent"
    title_text = "전 세계 대륙별 총 반려동물 수"
else:
    drill_data = df_2024[df_2024["Continent"] == selected_continent]
    x_axis = "Country"
    title_text = f"{selected_continent} 내 국가별 반려동물 수"

# (2단계: 필터링된 결과 막대 그래프로 시각화)
fig_drill = px.bar(
    drill_data,
    x=x_axis,
    y=["Dogs (Millions)", "Cats (Millions)"],
    title=title_text,
    barmode="group",
    color_discrete_map={"Dogs (Millions)": "#FFA41B", "Cats (Millions)": "#525E75"},
    height=450
)

fig_drill.update_layout(
    xaxis_title="지역/국가",
    yaxis_title="수 (백만 마리)",
    legend_title="반려동물 종류",
    hovermode="x unified"
)

st.plotly_chart(fig_drill, use_container_width=True)

# 데이터 테이블 표시 토글
if st.checkbox("💾 로우 데이터(Raw Data) 확인하기"):
    st.dataframe(df_2024 if selected_continent == "전체 보기" else drill_data, use_container_width=True)
