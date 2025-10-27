# css_probe.py  — Selector diagnostics
import streamlit as st

st.set_page_config(page_title="CSS Probe", layout="wide")
st.caption("🧪 CSS Probe • Streamlit " + st.__version__)

st.markdown("""
<style>
/* TEST A — global baseline */
html, body { background:#f8fafc !important; outline: 4px solid magenta !important; }

/* TEST B — modern Streamlit container */
[data-testid="stAppViewContainer"] { background:#eef2ff !important; }  /* pale indigo */

/* TEST C — header strip */
header[data-testid="stHeader"] { background: transparent !important; box-shadow:none !important; }

/* TEST D — top padding on main block */
section.main > div.block-container { padding-top: 8px !important; }

/* TEST E — class-based style (ensures our own classes can apply) */
.jt-test-box {
  background:#ffffff; border:2px dashed #2563eb; padding:16px; border-radius:10px;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}
</style>
""", unsafe_allow_html=True)

st.subheader("If you don't see a magenta outline or colored backgrounds, CSS injection is failing.")

st.markdown("### Test Elements")
st.markdown('<div class="jt-test-box">TEST E: This box should have a white background, dashed blue border, and subtle shadow.</div>', unsafe_allow_html=True)
st.write("TEST A: Page should have a **magenta outline**.")
st.write("TEST B: Main app area should have a **pale indigo** background (#eef2ff).")
st.write("TEST C: The Streamlit header should be **transparent** (no white bar).")
st.write("TEST D: There should be **tight top padding** (content close to the top).")
