# portal_preview.py
# Standalone preview of the Journalist's Toolkit portal (no navigation logic)
import streamlit as st

st.set_page_config(page_title="Journalist's Toolkit — Portal Preview", layout="wide")

# --- Minimal, safer CSS shims (work across recent Streamlit versions) ---
st.markdown("""
<style>
/* App background */
[data-testid="stAppViewContainer"] { background: #f8fafc !important; }
/* Remove the white header strip */
header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
/* Top padding across multiple builds */
section.main > div.block-container,
[data-testid="stAppViewContainer"] .main .block-container,
[data-testid="stAppViewContainer"] [data-testid="block-container"] { padding-top: 1rem !important; }
/* Button legibility */
.stButton > button, .stLinkButton { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# --- Hero / header (inline styles so we don't rely on Streamlit wrappers) ---
st.markdown("""
<div style="
  background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
  color: white; padding: 24px 28px 16px 28px;
  border-radius: 16px; margin-bottom: 0;">
  <h1 style="margin: 0 0 8px 0; font-size: 2.3rem; font-weight: 800;">
    🛠️ Journalist's Toolkit
  </h1>
  <p style="margin: 0; font-size: 1.12rem; opacity: 0.95;">
    AI-powered coaching tools designed to stand in for an editor, help you think like a journalist and strengthen your work.
  </p>
</div>
""", unsafe_allow_html=True)

# --- “How It Works” — compact card with 4 steps ---
st.markdown("""
<div style="
  background: #ffffff; border-radius: 12px; padding: 16px 18px;
  margin-top: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
  <h3 style="margin: 0 0 8px 0; font-size: 1.25rem;">How It Works</h3>
  <p style="margin: 0 0 10px 0; color: #475569; font-size: 1rem; line-height: 1.55;">
    Journalism requires many skills. We help you develop them by using AI as a coach rather than a shortcut.
  </p>
</div>
""", unsafe_allow_html=True)

def step_html(n, title, desc):
    return f"""
    <div style="
      text-align: center; padding: 14px 10px; background: #fff;
      border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
      <div style="
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white; width: 36px; height: 36px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 8px auto; font-weight: 700;">{n}</div>
      <div style="font-size: 1rem; font-weight: 600; margin-bottom: 6px;">{title}</div>
      <div style="font-size: 0.92rem; color: #64748b; line-height: 1.5;">{desc}</div>
    </div>
    """

c1, c2 = st.columns(2)
with c1:
    st.markdown(step_html(1, "Pick a Task", "Choose what you need help with (pitch, reporting, etc.)"), unsafe_allow_html=True)
with c2:
    st.markdown(step_html(2, "Answer Questions", "Think through the kind of questions an editor would ask"), unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown(step_html(3, "Get Your Prompt", "We generate expert coaching instructions for an AI"), unsafe_allow_html=True)
with c4:
    st.markdown(step_html(4, "Start the Coaching", "Copy the prompt into an AI model and begin a dialogue"), unsafe_allow_html=True)

# --- Caveat / Copy & Paste callout ---
st.markdown("""
<div style="
  background: #f8fafc; border-radius: 12px; padding: 14px;
  margin-top: 12px; border-left: 4px solid #64748b;">
  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
    <div style="background: white; width: 36px; height: 36px; border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 1.1rem; border: 2px solid #cbd5e1;">📋</div>
    <h3 style="color: #475569; font-size: 1.08rem; margin: 0;">Copy and Paste, Huh?</h3>
  </div>
  <p style="color: #475569; font-size: 0.98rem; line-height: 1.55; margin: 0;">
    <strong>Yes!</strong> This tool works with other tools—it generates smart prompts that set up great discussions in whatever AI model you prefer.
    That adds a step, but it keeps the tool <strong>free</strong>, lets you <strong>choose</strong> the model you trust,
    and often yields <strong>better performance</strong> than an API-only approach.
  </p>
</div>
""", unsafe_allow_html=True)

# --- Get Started ---
st.markdown('<h3 style="margin: 14px 0 8px 0; font-size: 1.25rem;">Get Started</h3>', unsafe_allow_html=True)

lc, rc = st.columns([1,3])
with lc:
    st.markdown('<div style="padding-top: 6px; font-weight: 600; color: #475569;">Your experience level:</div>', unsafe_allow_html=True)
with rc:
    level = st.selectbox("level", ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"], label_visibility="collapsed")

st.markdown('<div style="color: #475569; margin: 12px 0; font-weight: 600;">Now, choose a task:</div>', unsafe_allow_html=True)

# --- Task buttons (no navigation in preview; we just simulate) ---
b1c, b2c = st.columns(2)
with b1c:
    if st.button("Prepare a Story Pitch", type="primary", use_container_width=True):
        st.success("Navigate → questionnaire (preview)")
    st.button("Develop Interview Questions", disabled=True, use_container_width=True, help="Coming soon - Craft better questions for your sources")
    st.button("Vet a Source", disabled=True, use_container_width=True, help="Coming soon - Evaluate reliability and potential bias")

with b2c:
    if st.button("Get Ready to Report", type="primary", use_container_width=True):
        st.success("Navigate → grr_choice (preview)")
    st.button("Structure a First Draft", disabled=True, use_container_width=True, help="Coming soon - Get guidance on organizing your story")
    st.button("Check Your Facts", disabled=True, use_container_width=True, help="Coming soon - Build a verification strategy")

# --- Feedback & Footer CTA ---
st.markdown('<div style="text-align:center; margin: 24px 0 18px 0;">', unsafe_allow_html=True)
st.link_button("💬 Tell Us What You Think",
               url="mailto:johncjm@gmail.com?subject=Journalist%27s%20Toolkit%20Feedback&body=Please%20share%20your%20feedback%20here%3A",
               type="secondary",
               use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

st.info("🤔 **Looking for a Different Kind of Collaboration?**\n\nTest whether three AI models working together produce better results than one. Team of Rivals brings ChatGPT, Claude, and Gemini together for multi-round discussions.", icon="💡")
st.link_button("Try Team of Rivals →", url="https://team-of-rivals-tor1-beta.streamlit.app/", use_container_width=False)

# Build/version crumb so you can confirm what’s running
st.caption(f"Preview build • Streamlit {st.__version__} • Level selected: {level}")
