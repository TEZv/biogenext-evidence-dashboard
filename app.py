"""BioGENext 2026 — From data to clinical decision.

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="BioGENext · From Data to Decision",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: #090d16; color: #e8f0ff; }
    [data-testid="stSidebar"] { background: #0c1322; border-right: 1px solid #1d304d; }
    h1, h2, h3 { color: #f3f7ff; letter-spacing: -0.02em; }
    h1 { font-size: 2.4rem; }
    .subtitle { color: #91a8c8; font-size: 1.05rem; margin-top: -0.5rem; }
    .eyebrow { color: #56f0d0; font-size: 0.78rem; letter-spacing: 0.16em; text-transform: uppercase; }
    .source { color: #7187a8; font-size: 0.78rem; margin-top: 0.4rem; }
    .metric-card {
        background: #101a2b; border: 1px solid #213b60; border-radius: 10px;
        padding: 1rem 1.1rem; min-height: 116px;
    }
    .metric-label { color: #91a8c8; font-size: 0.82rem; }
    .metric-value { color: #56f0d0; font-size: 1.75rem; font-weight: 700; margin-top: 0.35rem; }
    .metric-note { color: #748ba9; font-size: 0.75rem; margin-top: 0.35rem; }
    .callout {
        background: #111c31; border-left: 3px solid #56f0d0; padding: 0.9rem 1rem;
        border-radius: 0 8px 8px 0; color: #d7e4f7;
    }
    .small { color: #9bb0cc; font-size: 0.88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

COLORS = {
    "bg": "#090d16",
    "panel": "#101a2b",
    "grid": "#21334f",
    "text": "#dbe8fa",
    "muted": "#91a8c8",
    "mint": "#56f0d0",
    "blue": "#5da9ff",
    "violet": "#b692ff",
    "orange": "#ffb86b",
    "pink": "#ff76b7",
}


def chart_layout(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text"]),
        margin=dict(l=20, r=20, t=45, b=35),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["muted"])),
        title_font=dict(size=16, color="#f3f7ff"),
    )
    fig.update_xaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"])
    fig.update_yaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"])
    return fig


def metric(label, value, note):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


st.markdown('<div class="eyebrow">BioGENext 2026 · evidence map</div>', unsafe_allow_html=True)
st.title("From data to clinical decision")
st.markdown(
    '<div class="subtitle">Що відбувається між біологічним сигналом, моделлю та рішенням для пацієнта?</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Навігація")
    view = st.radio(
        "Розділ",
        ["Огляд", "Metagenomics", "Models & validation", "Ukraine pipeline", "Evidence notes"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Рівень доказовості**")
    st.caption("Цифри нижче — зі слайдів BioGENext або позначені як benchmark / proposal. Вони не є клінічною валідацією K-RnD Lab.")

if view == "Огляд":
    st.markdown(
        '<div class="callout"><b>Головна теза:</b> у біомедицині недостатньо побудувати модель. '
        'Потрібен маршрут, яким її результат дійде до експерименту, регуляторного середовища та клінічного рішення.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(4)
    with cols[0]:
        metric("Міста в metagenomics study", "60", "conference slide")
    with cols[1]:
        metric("Зразки", "4 728", "conference slide")
    with cols[2]:
        metric("Незіставлені reads", "34,6%", "not mapped to existing databases")
    with cols[3]:
        metric("Pannotator speedup", "4,2×", "8 154 genomes benchmark")

    st.subheader("Один pipeline — кілька точок розриву")
    pipeline = pd.DataFrame(
        {
            "Етап": ["Дані", "Модель", "Експеримент", "Діагностика", "Рішення", "Терапія"],
            "Результат": [100, 82, 58, 35, 18, 8],
        }
    )
    fig = px.funnel(
        pipeline,
        y="Етап",
        x="Результат",
        title="Ілюстративна карта переходу сигналу до рішення (не виміряні дані)",
    )
    fig.update_traces(marker_color=COLORS["mint"], textinfo="value")
    fig.update_xaxes(title="Умовний індекс проходження pipeline (не клінічна метрика)")
    fig.update_yaxes(title="")
    chart_layout(fig, 390)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        '<div class="source">Ілюстративний індекс для пояснення pipeline K-RnD Lab; '
        'значення 100 → 8 не походять із дослідження і не описують реальні втрати.</div>',
        unsafe_allow_html=True,
    )

elif view == "Metagenomics":
    st.subheader("Metagenomics: масштаб даних і межі відомого")
    st.markdown(
        '<div class="small">Одна з презентацій показала не «готову відповідь», а масштаб задачі: '
        'величезна частина біологічного сигналу ще не має надійної відповідності в базах.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    scale = pd.DataFrame(
        {
            "Показник": ["Зразки", "Бактерії", "Віруси", "CRISPR arrays"],
            "Значення": [4728, 748, 10928, 838532],
        }
    )
    fig = px.bar(
        scale,
        x="Показник",
        y="Значення",
        title="Масштаб metagenomics study",
        color="Показник",
        color_discrete_sequence=[COLORS["mint"], COLORS["blue"], COLORS["violet"], COLORS["pink"]],
    )
    fig.update_yaxes(type="log", title="Кількість (логарифмічна шкала)")
    fig.update_xaxes(title="")
    fig.update_layout(showlegend=False)
    chart_layout(fig, 390)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        '<div class="source">Source: Alina Frolova, “Metagenomics in Practice: From Urban Microbiomes to Human Health”, BioGENext 2026 slide.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        unmapped = pd.DataFrame({"Категорія": ["Mapped", "Not mapped"], "Reads": [65.4, 34.6]})
        fig = px.pie(
            unmapped,
            values="Reads",
            names="Категорія",
            hole=0.62,
            title="Reads зіставлені з базами",
            color_discrete_sequence=[COLORS["blue"], COLORS["orange"]],
        )
        fig.update_traces(textinfo="label+percent")
        chart_layout(fig, 330)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="source">34,6% — частка reads, що не зіставили з наявними базами.</div>', unsafe_allow_html=True)
    with right:
        runtime = pd.DataFrame({"Інструмент": ["Bakta", "Pannotator"], "Seconds": [930.9, 220.5]})
        fig = px.bar(
            runtime,
            x="Інструмент",
            y="Seconds",
            title="Annotation runtime на зразок",
            text="Seconds",
            color="Інструмент",
            color_discrete_sequence=[COLORS["pink"], COLORS["mint"]],
        )
        fig.update_yaxes(title="Секунди на зразок")
        fig.update_xaxes(title="")
        fig.update_traces(texttemplate="%{text:.1f}s", textposition="outside")
        chart_layout(fig, 330)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="source">n=8 154; benchmark slide: 930,9 → 220,5 s, приблизно 4,2×.</div>', unsafe_allow_html=True)

elif view == "Models & validation":
    st.subheader("Модель не дорівнює доказу")
    st.markdown(
        '<div class="small">Навіть сильний computational result має пройти експериментальну перевірку. '
        'Тому візуалізація розділяє prediction, benchmark і підтверджене binding.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    tested = pd.DataFrame(
        {
            "Мішень": ["GLP-2", "GABARAP", "MRGPRX2", "STAT6", "ROR1", "WNR"],
            "Tested": [51, 28, 38, 37, 34, 27],
            "Positive / confirmed": [12, 3, 10, 1, 2, 2],
        }
    )
    tested["Rate"] = tested["Positive / confirmed"] / tested["Tested"] * 100
    fig = px.bar(
        tested,
        x="Мішень",
        y=["Tested", "Positive / confirmed"],
        barmode="group",
        title="Boltz: tested compounds vs positive results",
        color_discrete_sequence=[COLORS["blue"], COLORS["mint"]],
    )
    fig.update_yaxes(title="Кількість сполук")
    fig.update_xaxes(title="")
    chart_layout(fig, 390)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        '<div class="source">Source: Boltz presentation, BioGENext 2026. Positive results are not equivalent to an approved drug.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    with cols[0]:
        metric("Werner helicase", "2 / 27", "confirmed binders / tested compounds")
    with cols[1]:
        metric("IC50", "24 & 8,6 μM", "two confirmed binders")
    with cols[2]:
        metric("fastLBP example", "r = 0,28", "CHI3L1 expression prediction")

    st.info(
        "Важливе очищення цифр: 87% зі слайдів належить ErCas12a experimental assay, а не metagenomics-моделі K-RnD Lab. У пості не варто називати це власною accuracy."
    )

elif view == "Ukraine pipeline":
    st.subheader("Український маршрут: від policy до pipeline")
    st.markdown(
        '<div class="small">На конференції показували не лише біологічні моделі, а й інфраструктуру, '
        'яка має зробити їх застосовними.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(4)
    with cols[0]:
        metric("Нові випадки раку / рік", "155 239", "figure shown on policy slide")
    with cols[1]:
        metric("Смерті / рік", "84 153", "figure shown on policy slide")
    with cols[2]:
        metric("Mortality / incidence", "0,54", "EU comparison: 0,35–0,40")
    with cols[3]:
        metric("Phase I pilot", "500 cases", "UBI Hub proposal")

    roadmap = pd.DataFrame(
        {
            "Фаза": ["Phase I", "Phase II", "Phase III"],
            "Період": ["2025–26", "2027–28", "2027–30"],
            "Фокус": ["legal + 500-case pilot", "AI, NGS, OncoAtlas-UA", "ecosystem + partnerships"],
        }
    )
    fig = go.Figure()
    colors = [COLORS["mint"], COLORS["blue"], COLORS["violet"]]
    for i, row in roadmap.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[i, i + 0.8],
                y=[1, 1],
                mode="lines+markers+text",
                line=dict(color=colors[i], width=10),
                marker=dict(size=16, color=colors[i]),
                text=[row["Фаза"], row["Період"]],
                textposition=["top center", "bottom center"],
                hovertext=row["Фокус"],
                hoverinfo="text",
                showlegend=False,
            )
        )
    fig.update_xaxes(range=[-0.4, 2.2], visible=False)
    fig.update_yaxes(range=[0.7, 1.3], visible=False)
    fig.update_layout(title="UBI Hub proposal roadmap", height=250)
    chart_layout(fig, 280)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        '<div class="source">Source: “From Policy to Pipeline” presentation, BioGENext 2026. This is a proposal/roadmap, not a claim that every component is already operational.</div>',
        unsafe_allow_html=True,
    )

elif view == "Evidence notes":
    st.subheader("Що саме означає кожна цифра")
    notes = [
        ("Conference slide", "число показане спікером на слайді; треба цитувати назву доповіді"),
        ("Benchmark", "порівняння інструментів або моделей на певному dataset"),
        ("Experimental", "результат лабораторної перевірки, але не обов’язково клінічний"),
        ("Proposal", "запланована інфраструктура або roadmap, не готова система"),
        ("K-RnD prototype", "дослідницький або simulated результат; не clinical validation"),
    ]
    for label, description in notes:
        st.markdown(f"**{label}** — {description}")

    st.divider()
    st.markdown("### Чого тут навмисно немає")
    st.markdown(
        """
        - 87% accuracy як результат K-RnD metagenomics — такого підтвердження немає.
        - твердження, що лікарі вже використовують ці моделі;
        - висновок, що metagenomics-тест самостійно діагностує або прогнозує хворобу;
        - твердження, що UBI Hub уже повністю працює.
        """
    )
    st.markdown(
        '<div class="callout"><b>Наступний дослідницький крок:</b> додати до кожної метрики dataset, '
        'тип валідації, одиницю вимірювання та наступного користувача результату.</div>',
        unsafe_allow_html=True,
    )
