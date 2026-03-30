import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="🐱 vs 🐶 세계 반려동물 대전",
    page_icon="🐾",
    layout="wide",
)

st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }
.team-header {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    padding: 0.5rem 0 0.2rem;
    letter-spacing: -0.5px;
}
.subheader {
    text-align: center;
    color: #888;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}
.metric-box {
    background: #fafafa;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    border: 1px solid #eee;
    text-align: center;
}
.metric-val { font-size: 1.6rem; font-weight: 700; }
.metric-lbl { font-size: 0.8rem; color: #999; margin-top: 2px; }
.winner-banner {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 600;
    padding: 0.7rem;
    border-radius: 12px;
    margin: 0.5rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── 데이터 ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = {
        "국가":         ["미국","중국","브라질","러시아","일본","독일","프랑스","영국","이탈리아","캐나다",
                        "호주","멕시코","한국","아르헨티나","인도","태국","폴란드","네덜란드","스페인","터키"],
        "대륙":         ["아메리카","아시아","아메리카","유럽","아시아","유럽","유럽","유럽","유럽","아메리카",
                        "오세아니아","아메리카","아시아","아메리카","아시아","아시아","유럽","유럽","유럽","아시아"],
        "고양이_수":    [74.1, 53.1, 22.1, 22.8, 15.3, 16.7, 15.1, 11.1, 10.6, 9.3,
                        3.8,  6.9,  7.8,  3.8,  4.5,  8.7,  8.0,  3.5,  6.4,  4.2],
        "강아지_수":    [89.7, 27.4, 54.2, 17.4, 12.0, 10.6, 7.6,  12.5, 8.7,  8.2,
                        6.4,  43.8, 6.0,  9.2,  19.5, 13.5, 8.1,  2.9,  9.3,  9.0],
        "인구":         [331, 1412, 215, 145, 126, 83, 68, 67, 60, 38,
                        26, 130, 52, 45, 1380, 70, 38, 17, 47, 84],
        "반려동물_지출_USD": [1500, 320, 280, 180, 950, 780, 710, 850, 620, 1100,
                             980, 150, 690, 190, 60,  200, 310, 830, 540, 170],
        "SNS_고양이_해시태그_M": [450, 280, 95,  120, 310, 180, 160, 190, 140, 130,
                                  80,  75,  210, 55,  95,  170, 70,  90,  110, 65],
        "SNS_강아지_해시태그_M": [380, 190, 160, 85,  220, 140, 100, 200, 110, 115,
                                  95,  130, 130, 80,  140, 145, 65,  75,  100, 90],
    }
    df = pd.DataFrame(data)
    df["총_반려동물"] = df["고양이_수"] + df["강아지_수"]
    df["고양이_비율"] = (df["고양이_수"] / df["총_반려동물"] * 100).round(1)
    df["강아지_비율"] = (df["강아지_수"] / df["총_반려동물"] * 100).round(1)
    df["우세팀"] = df.apply(lambda r: "고양이" if r["고양이_수"] > r["강아지_수"] else "강아지", axis=1)
    df["위도"] = [37.1, 35.9, -14.2, 61.5, 36.2, 51.2, 46.2, 55.4, 41.9, 56.1,
                 -25.3, 23.6, 35.9, -38.4, 20.6, 15.9, 51.9, 52.1, 40.4, 38.9]
    df["경도"] = [-95.7, 104.2, -51.9, 105.3, 138.3, 10.5, 2.2, -3.4, 12.6, -106.3,
                 133.8, -102.6, 127.8, -63.6, 78.9, 100.9, 19.1, 5.3, -3.7, 35.2]
    return df

df = load_data()

# ── 헤더 ────────────────────────────────────────────────────
st.markdown('<div class="team-header">🐱 고양이 vs 강아지 🐶</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">세계 반려동물 대전 · 20개국 데이터 · 단위: 백만 마리</div>', unsafe_allow_html=True)

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.header("🎛️ 필터 & 설정")

    team = st.radio("팀 선택", ["⚔️ 전체 비교", "🐱 고양이팀", "🐶 강아지팀"], index=0)

    continents = sorted(df["대륙"].unique())
    sel_cont = st.multiselect("대륙 필터", continents, default=continents)

    st.divider()
    st.subheader("🔍 국가 드릴다운")
    sel_country = st.selectbox("국가 선택", ["(전체)"] + sorted(df["국가"].tolist()))

    st.divider()
    st.subheader("💬 SNS 버블 크기")
    bubble_metric = st.radio("버블 = ", ["반려동물 수", "SNS 해시태그", "1인당 지출"])

    st.divider()
    st.caption("📊 출처: Statista · World Pet Association · 추정치 포함")

# ── 필터 적용 ─────────────────────────────────────────────────
fdf = df[df["대륙"].isin(sel_cont)].copy()

bubble_col_map = {
    "반려동물 수":    "총_반려동물",
    "SNS 해시태그":  "SNS_고양이_해시태그_M",
    "1인당 지출":    "반려동물_지출_USD",
}
bubble_col = bubble_col_map[bubble_metric]

# ── 글로벌 요약 ──────────────────────────────────────────────
total_cat = fdf["고양이_수"].sum()
total_dog = fdf["강아지_수"].sum()
cat_countries = (fdf["우세팀"] == "고양이").sum()
dog_countries = (fdf["우세팀"] == "강아지").sum()
winner = "🐱 고양이팀" if total_cat > total_dog else "🐶 강아지팀"
winner_color = "#fde8f0" if total_cat > total_dog else "#e8f0fd"
winner_text_color = "#c23b7a" if total_cat > total_dog else "#2b5fc2"

st.markdown(
    f'<div class="winner-banner" style="background:{winner_color};color:{winner_text_color};">'
    f'현재 선두 → {winner} ({max(total_cat,total_dog):.1f}M 마리)'
    f'</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("🐱 고양이 총합",  f"{total_cat:.1f}M"),
    ("🐶 강아지 총합",  f"{total_dog:.1f}M"),
    ("고양이 우세 국가", f"{cat_countries}개국"),
    ("강아지 우세 국가", f"{dog_countries}개국"),
    ("고양이 비율",     f"{total_cat/(total_cat+total_dog)*100:.1f}%"),
]
for col, (lbl, val) in zip([c1,c2,c3,c4,c5], metrics):
    col.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("")

# ── 탭 레이아웃 ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 세계 지도", "📊 나라별 대결", "💬 SNS 버블", "🔍 국가 상세"])

# ── Tab 1: 세계 지도 ─────────────────────────────────────────
with tab1:
    map_mode = st.radio("지도 표시", ["고양이 vs 강아지 우세", "고양이 수", "강아지 수"], horizontal=True)

    if map_mode == "고양이 vs 강아지 우세":
        fig_map = px.scatter_geo(
            fdf,
            lat="위도", lon="경도",
            color="우세팀",
            size="총_반려동물",
            hover_name="국가",
            hover_data={"고양이_수":":.1f", "강아지_수":":.1f", "위도":False, "경도":False},
            color_discrete_map={"고양이":"#e91e8c", "강아지":"#1e6ae9"},
            size_max=55,
            title="국가별 고양이 / 강아지 우세 지도",
        )
    else:
        col_key = "고양이_수" if "고양이" in map_mode else "강아지_수"
        emoji = "🐱" if "고양이" in map_mode else "🐶"
        fig_map = px.scatter_geo(
            fdf, lat="위도", lon="경도",
            size=col_key,
            hover_name="국가",
            hover_data={col_key:":.1f", "위도":False, "경도":False},
            color=col_key,
            color_continuous_scale="RdPu" if "고양이" in map_mode else "Blues",
            size_max=55,
            title=f"{emoji} 국가별 {col_key} 분포",
        )

    fig_map.update_layout(
        height=480,
        margin=dict(l=0,r=0,t=40,b=0),
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth",
                 landcolor="#f5f5f0", oceancolor="#e8f4f8", showocean=True,
                 coastlinecolor="#cccccc"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Apple SD Gothic Neo, sans-serif"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ── Tab 2: 나라별 대결 바차트 ────────────────────────────────
with tab2:
    sort_by = st.radio("정렬 기준", ["고양이 수", "강아지 수", "총합"], horizontal=True)
    sort_col = {"고양이 수":"고양이_수","강아지 수":"강아지_수","총합":"총_반려동물"}[sort_by]
    plot_df = fdf.sort_values(sort_col, ascending=True)

    if team == "🐱 고양이팀":
        show_cat, show_dog = True, False
    elif team == "🐶 강아지팀":
        show_cat, show_dog = False, True
    else:
        show_cat, show_dog = True, True

    fig_bar = go.Figure()
    if show_cat:
        fig_bar.add_trace(go.Bar(
            y=plot_df["국가"], x=plot_df["고양이_수"],
            name="🐱 고양이", orientation="h",
            marker_color="#e91e8c",
            text=plot_df["고양이_수"].map("{:.1f}M".format),
            textposition="outside",
        ))
    if show_dog:
        fig_bar.add_trace(go.Bar(
            y=plot_df["국가"], x=plot_df["강아지_수"],
            name="🐶 강아지", orientation="h",
            marker_color="#1e6ae9",
            text=plot_df["강아지_수"].map("{:.1f}M".format),
            textposition="outside",
        ))

    fig_bar.update_layout(
        height=600,
        barmode="group",
        title="국가별 고양이 vs 강아지 수 (백만 마리)",
        xaxis_title="반려동물 수 (백만 마리)",
        yaxis_title="",
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
        margin=dict(l=20,r=80,t=60,b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0"),
        font=dict(family="Apple SD Gothic Neo, sans-serif"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 비율 파이차트
    st.subheader("대륙별 고양이 : 강아지 비율")
    cont_df = fdf.groupby("대륙")[["고양이_수","강아지_수"]].sum().reset_index()
    fig_pie = make_subplots(
        rows=1, cols=len(cont_df),
        specs=[[{"type":"domain"}]*len(cont_df)],
        subplot_titles=cont_df["대륙"].tolist()
    )
    for i, row in cont_df.iterrows():
        fig_pie.add_trace(go.Pie(
            labels=["🐱 고양이","🐶 강아지"],
            values=[row["고양이_수"], row["강아지_수"]],
            name=row["대륙"],
            marker_colors=["#e91e8c","#1e6ae9"],
            hole=0.4,
            textinfo="percent",
        ), row=1, col=list(cont_df.index).index(i)+1)
    fig_pie.update_layout(
        height=280, showlegend=True,
        margin=dict(l=10,r=10,t=40,b=10),
        paper_bgcolor="white",
        font=dict(family="Apple SD Gothic Neo, sans-serif"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Tab 3: SNS 버블 애니메이션 ──────────────────────────────
with tab3:
    st.info("💡 버블 크기 = 사이드바에서 선택한 지표 / X축 = 고양이 SNS / Y축 = 강아지 SNS")

    fig_bubble = px.scatter(
        fdf,
        x="SNS_고양이_해시태그_M",
        y="SNS_강아지_해시태그_M",
        size=bubble_col,
        color="대륙",
        hover_name="국가",
        hover_data={
            "SNS_고양이_해시태그_M":":.0f",
            "SNS_강아지_해시태그_M":":.0f",
            "고양이_수":":.1f",
            "강아지_수":":.1f",
        },
        text="국가",
        size_max=70,
        title="SNS 해시태그 버블 차트 (단위: 백만 건)",
        labels={
            "SNS_고양이_해시태그_M":"🐱 고양이 SNS 해시태그 (M)",
            "SNS_강아지_해시태그_M":"🐶 강아지 SNS 해시태그 (M)",
        },
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_bubble.update_traces(textposition="top center", textfont_size=11)

    # 대각선 기준선 (같은 비율)
    max_val = max(fdf["SNS_고양이_해시태그_M"].max(), fdf["SNS_강아지_해시태그_M"].max()) + 20
    fig_bubble.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                         line=dict(color="#aaaaaa", width=1.5, dash="dot"))
    fig_bubble.add_annotation(x=max_val*0.7, y=max_val*0.73,
                               text="고양이=강아지 기준선",
                               showarrow=False, font=dict(size=11, color="#999"))

    # 고양이/강아지 영역 레이블
    fig_bubble.add_annotation(x=10, y=max_val*0.88, text="🐶 강아지 SNS 강세 영역",
                               showarrow=False, font=dict(size=12, color="#1e6ae9"))
    fig_bubble.add_annotation(x=max_val*0.6, y=10, text="🐱 고양이 SNS 강세 영역",
                               showarrow=False, font=dict(size=12, color="#e91e8c"))

    fig_bubble.update_layout(
        height=540,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(gridcolor="#f5f5f5", zeroline=False),
        yaxis=dict(gridcolor="#f5f5f5", zeroline=False),
        font=dict(family="Apple SD Gothic Neo, sans-serif"),
        margin=dict(l=20,r=20,t=60,b=20),
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

    # 히트맵
    st.subheader("🔥 대륙 × 팀별 SNS 열기 히트맵")
    heat_df = fdf.groupby("대륙")[["SNS_고양이_해시태그_M","SNS_강아지_해시태그_M"]].sum()
    fig_heat = go.Figure(go.Heatmap(
        z=[heat_df["SNS_고양이_해시태그_M"].tolist(), heat_df["SNS_강아지_해시태그_M"].tolist()],
        x=heat_df.index.tolist(),
        y=["🐱 고양이", "🐶 강아지"],
        colorscale="RdBu_r",
        text=[[f"{v:.0f}M" for v in heat_df["SNS_고양이_해시태그_M"]],
              [f"{v:.0f}M" for v in heat_df["SNS_강아지_해시태그_M"]]],
        texttemplate="%{text}",
        textfont=dict(size=13),
    ))
    fig_heat.update_layout(
        height=220, margin=dict(l=20,r=20,t=20,b=20),
        paper_bgcolor="white",
        font=dict(family="Apple SD Gothic Neo, sans-serif"),
        xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Tab 4: 국가 드릴다운 ─────────────────────────────────────
with tab4:
    if sel_country == "(전체)":
        st.info("👈 사이드바에서 국가를 선택하면 상세 분석이 표시됩니다.")

        # 전체일 때: 1인당 지출 vs 반려동물 비율 산점도
        fig_scatter = px.scatter(
            fdf,
            x="반려동물_지출_USD",
            y="고양이_비율",
            color="우세팀",
            size="총_반려동물",
            hover_name="국가",
            color_discrete_map={"고양이":"#e91e8c","강아지":"#1e6ae9"},
            size_max=50,
            title="💰 1인당 반려동물 지출 vs 고양이 선호 비율",
            labels={
                "반려동물_지출_USD":"연간 1인당 반려동물 지출 (USD)",
                "고양이_비율":"고양이 비율 (%)",
            },
        )
        fig_scatter.add_hline(y=50, line_dash="dot", line_color="#aaa",
                              annotation_text="50% 기준선", annotation_position="right")
        fig_scatter.update_layout(
            height=460, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#f5f5f5"),
            yaxis=dict(gridcolor="#f5f5f5"),
            font=dict(family="Apple SD Gothic Neo, sans-serif"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        row = df[df["국가"] == sel_country].iloc[0]
        winner_e = "🐱 고양이팀" if row["우세팀"] == "고양이" else "🐶 강아지팀"
        w_color = "#fde8f0" if row["우세팀"] == "고양이" else "#e8f0fd"
        w_tc = "#c23b7a" if row["우세팀"] == "고양이" else "#2b5fc2"

        st.markdown(
            f'<div class="winner-banner" style="background:{w_color};color:{w_tc};">'
            f'{sel_country}의 승자 → {winner_e}</div>',
            unsafe_allow_html=True,
        )

        d1,d2,d3,d4 = st.columns(4)
        d1.metric("🐱 고양이", f"{row['고양이_수']:.1f}M 마리")
        d2.metric("🐶 강아지", f"{row['강아지_수']:.1f}M 마리")
        d3.metric("💰 반려동물 지출", f"${row['반려동물_지출_USD']:,}")
        d4.metric("👥 인구", f"{row['인구']}M")

        col_left, col_right = st.columns(2)

        with col_left:
            fig_donut = go.Figure(go.Pie(
                labels=["🐱 고양이","🐶 강아지"],
                values=[row["고양이_수"], row["강아지_수"]],
                hole=0.55,
                marker_colors=["#e91e8c","#1e6ae9"],
                textinfo="label+percent",
                textfont_size=14,
            ))
            fig_donut.update_layout(
                title=f"{sel_country} 반려동물 비율",
                height=320, margin=dict(l=10,r=10,t=50,b=10),
                paper_bgcolor="white",
                font=dict(family="Apple SD Gothic Neo, sans-serif"),
                showlegend=False,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_right:
            cats = [row["고양이_수"], row["SNS_고양이_해시태그_M"], row["반려동물_지출_USD"]/100]
            dogs = [row["강아지_수"], row["SNS_강아지_해시태그_M"], row["반려동물_지출_USD"]/100]
            categories = ["반려동물 수(M)", "SNS 해시태그(M)", "지출 지수"]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=cats + [cats[0]], theta=categories + [categories[0]],
                fill="toself", name="🐱 고양이",
                line_color="#e91e8c", fillcolor="rgba(233,30,140,0.15)",
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=dogs + [dogs[0]], theta=categories + [categories[0]],
                fill="toself", name="🐶 강아지",
                line_color="#1e6ae9", fillcolor="rgba(30,106,233,0.15)",
            ))
            fig_radar.update_layout(
                title=f"{sel_country} 종합 레이더",
                polar=dict(radialaxis=dict(visible=True, gridcolor="#eee")),
                height=320, margin=dict(l=40,r=40,t=50,b=20),
                paper_bgcolor="white",
                font=dict(family="Apple SD Gothic Neo, sans-serif"),
                showlegend=True,
                legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # 대륙 내 비교
        st.subheader(f"🌏 {row['대륙']} 내 비교")
        cont_peers = fdf[fdf["대륙"]==row["대륙"]].sort_values("총_반려동물", ascending=False)
        fig_peer = go.Figure()
        colors_cat = ["#e91e8c" if c==sel_country else "#f8aad0" for c in cont_peers["국가"]]
        colors_dog = ["#1e6ae9" if c==sel_country else "#a8c4f5" for c in cont_peers["국가"]]
        fig_peer.add_trace(go.Bar(x=cont_peers["국가"], y=cont_peers["고양이_수"],
                                  name="🐱 고양이", marker_color=colors_cat))
        fig_peer.add_trace(go.Bar(x=cont_peers["국가"], y=cont_peers["강아지_수"],
                                  name="🐶 강아지", marker_color=colors_dog))
        fig_peer.update_layout(
            barmode="group", height=300,
            yaxis_title="반려동물 수 (백만 마리)",
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#f5f5f5"),
            yaxis=dict(gridcolor="#f5f5f5"),
            margin=dict(l=20,r=20,t=20,b=20),
            font=dict(family="Apple SD Gothic Neo, sans-serif"),
            legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_peer, use_container_width=True)

st.divider()
st.caption("🐾 데이터 출처: Statista, World Pet Association, GfK 반려동물 소유 보고서 (2022–2023) · 일부 수치는 추정치입니다.")
