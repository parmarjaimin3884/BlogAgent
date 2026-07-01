import streamlit as st
import sys
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BlogAgent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0f1117;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

/* ── Hero title ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.3rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: #64748b;
    margin-bottom: 2rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Input area ── */
.stTextArea textarea {
    background: #161b27 !important;
    border: 1.5px solid #1e2d45 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

/* ── Generate button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid #1e2535;
    background: #161b27;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: #7c3aed;
    background: #1a1030;
    box-shadow: 0 0 0 1px rgba(124,58,237,0.3);
}
.step-card.done {
    border-color: #065f46;
    background: #0a1f1a;
}
.step-card.waiting {
    opacity: 0.45;
}
.step-icon { font-size: 1.2rem; }
.step-label {
    font-size: 0.88rem;
    font-weight: 500;
    color: #94a3b8;
}
.step-card.active .step-label { color: #a78bfa; }
.step-card.done .step-label  { color: #34d399; }

/* ── Metric chips ── */
.metrics-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.metric-chip {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 8px;
    padding: 10px 18px;
    text-align: center;
    flex: 1;
    min-width: 90px;
}
.metric-chip .val {
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa;
    font-family: 'Playfair Display', serif;
}
.metric-chip .lbl {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}

/* ── Blog preview card ── */
.blog-card {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 2rem 2.2rem;
    margin-top: 1rem;
}

/* ── Section pills ── */
.section-pill {
    display: inline-block;
    background: #1e2535;
    color: #7c3aed;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: #1e2535 !important;
    color: #a78bfa !important;
    border: 1px solid #7c3aed !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

/* ── Divider ── */
hr { border-color: #1e2535 !important; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b27;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1e2535 !important;
    color: #a78bfa !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #161b27 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 3px; }

/* ── Status text ── */
.status-text {
    font-size: 0.82rem;
    color: #7c3aed;
    font-weight: 500;
    margin-left: auto;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.divider()
    st.markdown("### 🎛️ Blog Settings")

    blog_kind = st.selectbox(
        "Blog Type",
        ["explainer", "tutorial", "comparison", "news_roundup", "system_design"],
        help="Controls the structure the planner uses"
    )

    num_sections = st.slider("Sections", min_value=4, max_value=8, value=6)

    tone = st.selectbox(
        "Tone",
        ["Informative", "Conversational", "Technical", "Enthusiastic"]
    )

    st.divider()
    st.markdown("""
    <div style='font-size:0.78rem; color:#334155; line-height:1.6'>
    <b style='color:#475569'>Pipeline</b><br>
    Router → Research → Planner<br> → Writers → Assembler
    </div>
    """, unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Blog Writing Agent ✍️</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Drop a topic. The agent researches, plans, and writes a complete technical blog automatically.</div>', unsafe_allow_html=True)

topic_input = st.text_area(
    "",
    placeholder="e.g.  Write a blog on Open Source LLMs in 2026",
    height=100,
    label_visibility="collapsed"
)

col_btn, col_spacer = st.columns([1, 3])
with col_btn:
    generate = st.button("⚡ Generate Blog", use_container_width=True)

st.divider()

# ── Pipeline steps definition ──────────────────────────────────────────────────
STEPS = [
    ("🔀", "Router",        "Deciding research strategy…"),
    ("🔍", "Research",      "Searching the web for evidence…"),
    ("🗂️",  "Planner",      "Structuring blog sections…"),
    ("✍️", "Writers",       "Writing sections in parallel…"),
    ("📦", "Assembler",     "Combining & embedding images…"),
]

def render_pipeline(active_idx: int, done_idxs: set):
    cols = st.columns(len(STEPS))
    for i, (icon, label, _) in enumerate(STEPS):
        if i in done_idxs:
            state_cls = "done"
            icon_show = "✅"
        elif i == active_idx:
            state_cls = "active"
            icon_show = icon
        else:
            state_cls = "waiting"
            icon_show = icon

        cols[i].markdown(f"""
        <div class="step-card {state_cls}">
            <span class="step-icon">{icon_show}</span>
            <span class="step-label">{label}</span>
        </div>
        """, unsafe_allow_html=True)


# ── Generation logic ───────────────────────────────────────────────────────────
if generate:
    if not topic_input.strip():
        st.warning("Please enter a topic first.")
        st.stop()
    

    # Import backend (after env vars are set)
    try:
        from bwa_backend import run as run_agent
    except Exception as e:
        st.exception(e)
        st.stop()

    # ── Pipeline UI ──
    st.markdown("### 🔄 Pipeline")
    pipeline_placeholder = st.empty()
    status_placeholder   = st.empty()

    def show_step(active, done, msg=""):
        with pipeline_placeholder.container():
            render_pipeline(active, done)
        if msg:
            status_placeholder.markdown(
                f'<p style="font-size:0.83rem;color:#7c3aed;margin-top:4px">⏳ {msg}</p>',
                unsafe_allow_html=True
            )

    # Simulate step-by-step progress while backend runs
    # (LangGraph runs synchronously; we show steps as it progresses)
    show_step(0, set(), STEPS[0][2])
    time.sleep(0.6)
    show_step(1, {0}, STEPS[1][2])

   

    with st.spinner(""):
        try:
            # Enrich topic with sidebar settings
            enriched_topic = (
            f"{topic_input.strip()} "
            f"[tone: {tone}, blog_kind: {blog_kind}, sections: {num_sections}]"
                )

            show_step(2, {0, 1}, STEPS[2][2])

            result = run_agent(enriched_topic)

            show_step(3, {0,1,2}, STEPS[3][2])
            time.sleep(0.5)

            show_step(4, {0,1,2,3}, STEPS[4][2])
            time.sleep(0.3)
            show_step(-1, {0,1,2,3,4}, "Done!")
            status_placeholder.empty()

        except Exception as e:
            st.error(f"❌ Generation failed: {e}")
            st.stop()

    # ── Results ──
    final_md   = result.get("final", "")
    plan       = result.get("plan")
    sections   = result.get("sections", [])
    word_count = len(final_md.split())

    st.divider()
    st.markdown("### 📊 Blog Stats")
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-chip"><div class="val">{len(sections)}</div><div class="lbl">Sections</div></div>
        <div class="metric-chip"><div class="val">{word_count:,}</div><div class="lbl">Words</div></div>
        <div class="metric-chip"><div class="val">{len(plan.tasks) if plan else 0}</div><div class="lbl">Tasks</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs: Preview / Raw Markdown / Plan ──
    tab1, tab2, tab3 = st.tabs(["📖 Preview", "📝 Raw Markdown", "🗂️ Plan"])

    with tab1:
        st.markdown('<div class="blog-card">', unsafe_allow_html=True)
        st.markdown(final_md, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.code(final_md, language="markdown")

    with tab3:
        if plan:
            st.markdown(f"**Title:** {plan.blog_title}")
            st.markdown(f"**Audience:** {plan.audience} &nbsp;|&nbsp; **Tone:** {plan.tone} &nbsp;|&nbsp; **Kind:** {plan.blog_kind}")
            st.divider()
            for task in plan.tasks:
                with st.expander(f"Section {task.id} — {task.title}"):
                    st.markdown(f"**Goal:** {task.goal}")
                    st.markdown(f"**Target words:** {task.target_words}")
                    for b in task.bullets:
                        st.markdown(f"- {b}")
                    if task.tags:
                        st.markdown(" ".join([f"`{t}`" for t in task.tags]))

    # ── Download ──
    st.divider()
    safe = "".join(c if c.isalnum() or c in " _-" else "" for c in (plan.blog_title if plan else "blog"))
    fname = safe.strip().lower().replace(" ", "_") + ".md"

    docx_path = result["docx_path"]

    with open(docx_path, "rb") as f:
        docx_bytes = f.read()

    st.download_button(
        label="📄 Download Word",
        data=docx_bytes,
        file_name=os.path.basename(docx_path),
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
