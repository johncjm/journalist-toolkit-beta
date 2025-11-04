# v21.5-stable — Crew release (+Prepare-for-Interview hook, indentation + scrollTo fixes)
# - Portal hero + Get Started row with inline Experience selector
# - Streamlit 1.50 CSS compat shim (safe selectors only)
# - Event / Explore / Confirm flows (questionnaire + recipe pages)
# - Story Pitch flow (questionnaire + recipe pages)
# - Workshop follow-on page
# - Copy-to-clipboard helper (html.escape + uuid)
# - Prepare-for-Interview module routed via jt_tools if available

import streamlit as st
import textwrap
import html
import uuid

# --- Prepare-for-an-Interview tool (jt_tools) ---
try:
    from jt_tools.prepare_interview_prep import render_prepare_interview_prep
    _HAS_PREP = True
except Exception as _e:
    _HAS_PREP = False
    _PREP_IMPORT_ERR = _e

# ---------- APP CONFIG ----------
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")
st.caption(f"🛠️ Journalist’s Toolkit • v21.5-stable • Streamlit {st.__version__}")

# ---------- LIGHT COMPAT CSS SHIM (safe selectors only) ----------
st.markdown(
    """
<style>
/* App background container (stable selector) */
[data-testid="stAppViewContainer"] { background: #f8fafc !important; }
/* Remove header white strip */
header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
/* Top padding across builds */
section.main > div.block-container,
[data-testid="stAppViewContainer"] .main .block-container,
[data-testid="stAppViewContainer"] [data-testid="block-container"] { padding-top: 1.0rem !important; }
/* Minor typography smoothing */
h1,h2,h3 { letter-spacing: -0.01em; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HELPERS ----------
def go_to(page: str):
    st.session_state.page = page
    st.rerun()

def copy_button_js(text_to_copy: str, button_text: str = "Copy to Clipboard"):
    """Safe copy-to-clipboard: escapes content and uses unique IDs each call."""
    unique_key = uuid.uuid4().hex[:8]
    unique_id = f"copy-btn-{unique_key}"
    text_area_id = f"text-area-{unique_key}"
    safe = html.escape(text_to_copy or "", quote=True)
    st.components.v1.html(
        f"""
        <textarea id="{text_area_id}" style="opacity:0;position:absolute;height:0;width:0;">{safe}</textarea>
        <button id="{unique_id}" onclick="
            const text = document.getElementById('{text_area_id}').value;
            if (!navigator.clipboard) {{ return; }}
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('{unique_id}');
                const original = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {{ btn.innerText = original; }}, 1500);
            }});
        ">{button_text}</button>
        """,
        height=40,
    )

def get_counter(text: str):
    words = len(text.split()) if text else 0
    chars = len(text) if text else 0
    return words, chars

# ---------- STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "portal"
if "journalism_level" not in st.session_state:
    st.session_state.journalism_level = "Undergraduate journalist"

# =========================================================
# PAGE: PORTAL
# =========================================================
if st.session_state.page == "portal":
    # Hero (inline styles = robust to DOM changes)
    st.markdown(
        """
<div style="
  background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
  color: white; border-radius: 16px;
  padding: 1.25rem 1.5rem 1rem 1.5rem; margin-bottom: 0.5rem;">
  <h1 style="margin:0 0 .5rem 0; font-weight:800;">Journalist’s Toolkit</h1>
  <p style="margin:0; opacity:.95;">AI-powered coaching tools that stand in for an editor, help you think like a journalist, and strengthen your work.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # Get Started row with inline experience selector
    col1, col2 = st.columns([1.2, 2.8])
    with col1:
        st.markdown("### Get Started")
    with col2:
        st.session_state.journalism_level = st.selectbox(
            "Your experience level:",
            ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"],
            index=["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"]
            .index(st.session_state.journalism_level),
            label_visibility="visible",
        )

    # How It Works
    with st.container(border=True):
        st.markdown("### How It Works")
        st.markdown(
            "Journalism requires many skills. This app uses AI as a **coach**, not a shortcut—"
            "guiding you with the kinds of questions a good editor would ask."
        )
        a, b = st.columns(2)
        with a:
            st.markdown("**1. Pick a Task**  \nPitch, reporting prep, etc.")
        with b:
            st.markdown("**2. Answer Questions**  \nThink through an editor’s checklist.")
        c, d = st.columns(2)
        with c:
            st.markdown("**3. Get Your Prompt**  \nWe assemble expert coaching instructions.")
        with d:
            st.markdown("**4. Start Coaching**  \nPaste the prompt into your preferred AI.")

    # Caveat / philosophy
    with st.container(border=True):
        st.markdown("### Copy and Paste, Huh?")
        st.markdown(
            "**Yes.** Prompts here are meant to be pasted into any AI you prefer. "
            "This keeps the tool **free**, lets you **choose** the model, and often performs **better** than an API hookup."
        )

    # Task buttons
    st.markdown("#### Now, choose a task:")
    left, right = st.columns(2)
    with left:
        if st.button("Prepare a Story Pitch", type="primary", use_container_width=True):
            go_to("questionnaire")
        if st.button("Prepare for an Interview", use_container_width=True):
            if _HAS_PREP:
                go_to("prep")
            else:
                st.error("Prepare-for-Interview module not available.\n\n"
                         f"{_PREP_IMPORT_ERR if '_PREP_IMPORT_ERR' in globals() else ''}")
        st.button("Vet a Source", use_container_width=True, disabled=True, help="Coming soon")
    with right:
        if st.button("Get Ready to Report", type="primary", use_container_width=True):
            go_to("grr_choice")
        st.button("Structure a First Draft", use_container_width=True, disabled=True, help="Coming soon")
        st.button("Check Your Facts", use_container_width=True, disabled=True, help="Coming soon")

    # Footer CTA
    with st.container(border=True):
        st.info(
            "💡 **Looking for a different kind of collaboration?** "
            "Test whether three AI models working together produce better results than one. "
            "Team of Rivals brings ChatGPT, Claude, and Gemini together for multi-round discussions."
        )
        st.link_button("Try Team of Rivals →", "https://team-of-rivals-tor1-beta.streamlit.app/", use_container_width=False)

# =========================================================
# PAGE: Prepare-for-Interview (jt_tools)
# =========================================================
elif st.session_state.page == "prep":
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    if _HAS_PREP:
        render_prepare_interview_prep()
    else:
        st.error("Prepare-for-Interview module failed to load.")
    if st.button("← Back to Portal"):
        go_to("portal")

# =========================================================
# PAGE: Get Ready to Report — Choice
# =========================================================
elif st.session_state.page == "grr_choice":
    st.title("Get Ready to Report 📋")
    st.markdown("Different kinds of stories call for different prep. Which best describes your situation?")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Event", use_container_width=True):
            st.session_state.reporting_path = "event"
            go_to("reporting_plan_questionnaire")
        st.caption("Something scheduled is worth covering (vote, protest, presser).")
    with c2:
        if st.button("Explore", use_container_width=True):
            st.session_state.reporting_path = "explore"
            go_to("reporting_plan_questionnaire")
        st.caption("There’s a territory or community you want to understand.")
    with c3:
        if st.button("Confirm", use_container_width=True):
            st.session_state.reporting_path = "confirm"
            go_to("reporting_plan_questionnaire")
        st.caption("You’ve heard a claim/rumor and need to verify it.")
    st.markdown("---")
    if st.button("← Back to Portal"):
        go_to("portal")

# =========================================================
# PAGE: GRR Questionnaire
# =========================================================
elif st.session_state.page == "reporting_plan_questionnaire":
    path = st.session_state.get("reporting_path", "event")
    st.title(f"Reporting Plan: {path.capitalize()} Path")

    if path == "event":
        st.markdown("Let’s prep you for the event. Answer what you can; blanks are okay.")
        with st.form("event_plan_form"):
            with st.container(border=True):
                st.markdown("### Part 1: The Situation")
                q1_headline = st.text_input("What’s happening — a headline/tweet-length summary?")
                q2_where_when = st.text_input("Where and when is it happening?")
                q3_key_people = st.text_input("Who are the key people involved?")
                q4_why_now = st.text_input("Why is it happening now?")
                st.markdown("---")
                st.markdown("### Part 2: The Stakes")
                q5_how_big = st.text_input("How big a story is this?")
                q6_important = st.text_input("What makes it important?")
                q7_audience = st.text_input("Who’s the key audience?")
                st.markdown("---")
                st.markdown("### Part 3: Getting Started")
                q8_work_done = st.text_area("What prep have you done so far?")
                q9_prior_coverage = st.text_area("What’s already been covered? (links welcome)")
                q10_prior_coverage_effect = st.text_area("How does that affect your goals?")
                q11_work_left = st.text_area("What’s the key work left (docs/people)?")
                q12_anxious_excited = st.text_area("Anything you’re excited/anxious about?")
                st.markdown("---")
                event_style = st.radio(
                    "AI editor style?",
                    ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                    horizontal=True,
                )
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = dict(
                    q1_headline=q1_headline,
                    q2_where_when=q2_where_when,
                    q3_key_people=q3_key_people,
                    q4_why_now=q4_why_now,
                    q5_how_big=q5_how_big,
                    q6_important=q6_important,
                    q7_audience=q7_audience,
                    q8_work_done=q8_work_done,
                    q9_prior_coverage=q9_prior_coverage,
                    q10_prior_coverage_effect=q10_prior_coverage_effect,
                    q11_work_left=q11_work_left,
                    q12_anxious_excited=q12_anxious_excited,
                    coaching_style=event_style,
                )
                st.session_state.reporting_path = "event"
                go_to("reporting_plan_recipe")

    elif path == "explore":
        st.markdown("Help the editor understand your territory and hunch.")
        with st.form("explore_plan_form"):
            with st.container(border=True):
                st.markdown("### Part 1: Territory & Angle")
                q1_territory = st.text_input("What do you want to explore (who/what/where)?")
                q2_hunch = st.text_input("What’s your hunch or guiding question?")
                q3_curiosity = st.text_input("Why this now — what makes you curious?")
                q4_audience = st.text_input("Who’s the audience and why would they care?")
                st.markdown("---")
                st.markdown("### Part 2: Starting Point")
                q5_know = st.text_area("What do you already know?")
                q6_dont_know = st.text_area("What’s the most important thing you don’t know?")
                q7_prior_coverage = st.text_area("What has been covered already?")
                q8_relationship_bias = st.text_area("Your relationship to this subject; assumptions/biases?")
                st.markdown("---")
                st.markdown("### Part 3: The Plan")
                q9_plan_ideas = st.text_area("Initial reporting ideas (people/places/observations)")
                q10_first_step = st.text_input("One thing you can do today/tomorrow")
                st.markdown("---")
                explore_style = st.radio(
                    "AI editor style?",
                    ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                    horizontal=True,
                )
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = dict(
                    q1_territory=q1_territory,
                    q2_hunch=q2_hunch,
                    q3_curiosity=q3_curiosity,
                    q4_audience=q4_audience,
                    q5_know=q5_know,
                    q6_dont_know=q6_dont_know,
                    q7_prior_coverage=q7_prior_coverage,
                    q8_relationship_bias=q8_relationship_bias,
                    q9_plan_ideas=q9_plan_ideas,
                    q10_first_step=q10_first_step,
                    coaching_style=explore_style,
                )
                st.session_state.reporting_path = "explore"
                go_to("reporting_plan_recipe")

    elif path == "confirm":
        st.markdown("State the claim, the source, the stakes—and how you’ll verify.")
        with st.form("confirm_plan_form"):
            with st.container(border=True):
                q1_claim = st.text_area("**The Claim:** State a single, testable sentence.")
                q2_source = st.text_area("**The Source:** Where did it come from? Reliability/motivations?")
                q3_stakes = st.text_area("**The Stakes:** Why does this matter to your audience?")
                q4_evidence = st.text_area(
                    "**The Evidence:** What would make you comfortable running the story? "
                    "What findings would kill it? (People/docs for both.)"
                )
                q5_risks = st.text_area(
                    "**The Risks:** What worries you most? Privacy, harm, legal, ethical concerns?"
                )
                st.markdown("---")
                confirm_style = st.radio(
                    "AI editor style?",
                    ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                    horizontal=True,
                )
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = dict(
                    q1_claim=q1_claim,
                    q2_source=q2_source,
                    q3_stakes=q3_stakes,
                    q4_evidence=q4_evidence,
                    q5_risks=q5_risks,
                    coaching_style=confirm_style,
                )
                st.session_state.reporting_path = "confirm"
                go_to("reporting_plan_recipe")

    st.markdown("---")
    if st.button("← Back to Choices"):
        go_to("grr_choice")

# =========================================================
# PAGE: GRR Recipe (Event / Explore / Confirm)
# =========================================================
elif st.session_state.page == "reporting_plan_recipe":
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)

    path = st.session_state.get("reporting_path")
    if not path:
        st.warning("⚠️ No reporting path selected. Please go back and choose a path.", icon="⚠️")
        if st.button("← Back to Get Ready to Report"):
            go_to("grr_choice")
        st.stop()

    st.title("Your Custom Reporting Plan Prompt 📝")
    st.markdown("Copy this into your preferred AI chat to start the coaching session.")
    st.markdown("---")

    data = st.session_state.get("form_data", {})
    level = st.session_state.get("journalism_level", "N/A")

    if path == "event":
        context_string = f"""
- Headline/Tweet: {data.get('q1_headline','N/A')}
- Where & When: {data.get('q2_where_when','N/A')}
- Key People: {data.get('q3_key_people','N/A')}
- Why Now: {data.get('q4_why_now','N/A')}
- Story Size: {data.get('q5_how_big','N/A')}
- What Makes It Important: {data.get('q6_important','N/A')}
- Key Audience: {data.get('q7_audience','N/A')}
- Work Done So Far: {data.get('q8_work_done','N/A')}
- Prior Coverage: {data.get('q9_prior_coverage','N/A')}
- Effect of Prior Coverage: {data.get('q10_prior_coverage_effect','N/A')}
- Key Work Left: {data.get('q11_work_left','N/A')}
- Reporter Mindset: {data.get('q12_anxious_excited','N/A')}
- User Experience Level: {level}
- Desired Coaching Style: {data.get('coaching_style','N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are an experienced and encouraging **assignment editor** acting as a **Socratic coach** for a student journalist. Your goal is to help them build a **comprehensive prep checklist** for an upcoming event. Philosophy: **coach, not do**.

        ## Coaching Style & Tone
        Calibrate tone to the user's level (**{level}**) and chosen style (**{data.get('coaching_style','N/A')}**).

        # 2. CONTEXT
        The student provided the following:
        {context_string}

        # 3. TASK: SESSION FLOW
        **Opening (handle gaps)**  
        - If answers are mostly complete: acknowledge something specific; identify one gap (priority: Why → Audience → What); ask one opening question.  
        - If sparse: ask permission to fill gaps; if yes, ask 2–3 essentials; if no, proceed.

        **Main dialogue**  
        Ask about: Story angles → Logistics → Sourcing → Contingencies. Keep it question-led.

        # 4. CORE CONSTRAINTS
        - Journalistic skepticism: ask how they’ll independently verify claims.  
        - Coach, don’t do: **no lists or writing for them**; **don’t name people/institutions**.  
        - Be Socratic; respect user choices.

        # 5. ETHICAL & DIVERSITY LENS
        Nudge for diverse sourcing and overlooked communities.

        # 6. FINAL GOAL
        End with a clear, **student-built** checklist for covering the event.
        """)

    elif path == "explore":
        context_string = f"""
- Territory: {data.get('q1_territory','N/A')}
- Guiding Hunch: {data.get('q2_hunch','N/A')}
- Curiosity/Timeliness: {data.get('q3_curiosity','N/A')}
- Audience: {data.get('q4_audience','N/A')}
- Initial Knowledge: {data.get('q5_know','N/A')}
- Knowledge Gaps: {data.get('q6_dont_know','N/A')}
- Prior Coverage: {data.get('q7_prior_coverage','N/A')}
- Relationship & Bias: {data.get('q8_relationship_bias','N/A')}
- Initial Reporting Ideas: {data.get('q9_plan_ideas','N/A')}
- First Step: {data.get('q10_first_step','N/A')}
- User Experience Level: {level}
- Desired Coaching Style: {data.get('coaching_style','N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are an experienced editor acting as a **Socratic coach** for exploratory reporting. Goal: help the student discover potential angles, characters, and conflicts—**without** writing the story for them. Philosophy: **coach, not do**.

        ## Coaching Style & Tone
        Adapt to **{level}** and style **{data.get('coaching_style','N/A')}**.

        # 2. CONTEXT
        The student shared:
        {context_string}

        # 3. TASK: SESSION FLOW
        **Opening**  
        - If sparse: ask permission to clarify; if yes, ask 2–3 essentials.  
        - If mostly complete: acknowledge, surface one prioritized gap (Hunch → Relationship → Audience), ask one opening question.

        **Exploratory dialogue (~3 turns)**  
        Ask open, curious questions about hunches, characters/groups, sources of tension. **Do not** force a specific angle.

        **Choice point**  
        Summarize themes and offer:  
        A) Focus a specific angle → build a concrete plan.  
        B) Do more “fishing” → design an open-ended plan.  
        C) Reconsider the topic.

        **Post-choice**  
        - A: Ask for working hypothesis, define next reporting step.  
        - B: Design an open plan; end with one concrete exploratory action.  
        - C: Validate; reflect on learning.

        # 4. CORE CONSTRAINTS
        - Gentle skepticism; ask how to **test** assumptions.  
        - **Don’t suggest specific angles or name people/institutions** during exploration.

        # 5. ETHICAL & DIVERSITY LENS
        If they’re an outsider to the community, ask how they’ll ensure fair, accurate representation.

        # 6. FINAL GOAL
        Either a concrete plan, a plan for more exploration, or the decision to move on—all valid outcomes.
        """)

    elif path == "confirm":
        context_string = f"""
- The Claim: {data.get('q1_claim','N/A')}
- The Source: {data.get('q2_source','N/A')}
- The Stakes: {data.get('q3_stakes','N/A')}
- The Evidence: {data.get('q4_evidence','N/A')}
- The Risks: {data.get('q5_risks','N/A')}
- User Experience Level: {level}
- Desired Coaching Style: {data.get('coaching_style','N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are a skeptical **investigative editor / fact-checker** acting as a **Socratic coach**. Goal: help the student build a rigorous **verification plan** for a specific claim. Philosophy: assume nothing; question everything.

        ## Coaching Style & Tone
        Adapt to **{level}** and style **{data.get('coaching_style','N/A')}**.

        # 2. CONTEXT
        The student is trying to verify:
        {context_string}

        # 3. TASK: SESSION FLOW
        **Opening**  
        - If mostly complete: acknowledge; focus one gap (priority: Evidence → Source → Stakes).  
        - If sparse: ask permission to clarify; proceed accordingly.

        **Verification strategy**  
        1) Evidence review: how to obtain and **authenticate** required docs; chain of custody issues.  
        2) Paper trail: what records **must exist** if true (public filings, emails, financials, logs).  
        3) Source triangulation: primary; best counter-source; neutral context expert.

        **Ethical assessment**  
        Probe privacy/harm concerns and mitigation while reporting **before** confirmation.

        # 4. CORE CONSTRAINTS
        - Default stance: unproven.  
        - Triangulate everything.  
        - Focus on **method**; **do not name** specific people/institutions; **do not investigate** for them.

        # 5. FINAL GOAL
        A clear, actionable **verification checklist**. Outcome may confirm, debunk, or remain inconclusive—all legitimate.
        """)

    # Render
    cmain, cside = st.columns([2, 1])
    with cmain:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=460, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt")
    with cside:
        with st.container(border=True):
            st.markdown("## Anatomy of the Prompt")
            st.markdown(
                "A prompt is more than just a question; it's a set of instructions that guides the AI's response. "
                "Good **prompt engineering** means designing those instructions to get the most helpful and accurate coaching."
            )
            st.markdown("---")
            st.markdown(
                """
1. **ROLE & GOAL** — Who the AI should be (e.g., an experienced editor) and what it’s trying to accomplish (coach you by asking questions, not doing the work).

2. **CONTEXT** — Your answers from the questionnaire. This gives the AI concrete facts so its questions are specific and relevant.

3. **FLOW** — The conversation game plan: how to open (acknowledge + find gaps), where to probe (angles, logistics, sourcing, risks), and when to offer a choice about next steps.

4. **CONSTRAINTS** — Guardrails that keep the AI on track: *coach, don’t do*; be Socratic; avoid naming specific people/institutions; push for verification when claims are made.

5. **ETHICAL LENS** — Consider bias, harm, privacy, diverse sourcing; plan mitigation before publishing.

6. **FINAL GOAL REMINDER** — You leave with a clear, actionable checklist that **you** built (not prose written for you).
                """
            )

    st.markdown("---")
    st.markdown("**💡 Tip:** These links are shortcuts—you can paste this into *any* AI chat tool.")
    g1, g2, g3 = st.columns(3)
    with g1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with g2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with g3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("---")
    if st.button("Continue to Workshop →", type="primary"):
        go_to("follow_on")
    if st.button("← Back to Questionnaire"):
        go_to("reporting_plan_questionnaire")

# =========================================================
# PAGE: Story Pitch Questionnaire
# =========================================================
elif st.session_state.page == "questionnaire":
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    st.title("Story Pitch Coach")
    st.markdown("Answer what you can—this helps you think like an editor before you pitch.")
    with st.form("pitch_form"):
        with st.container(border=True):
            pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)
            st.subheader("Pitch Details (Optional, but recommended)")
            story_type_choice = st.selectbox("Which best describes your story idea?", ["(Not sure)", "Event", "Explore", "Confirm"])
            prior_coverage = st.text_area("What has already been written on this topic? (Links welcome)")
            prior_coverage_effect = st.text_area("How does that affect your reporting goals?")
            col1, col2 = st.columns(2)
            with col1:
                working_headline = st.text_input("Working headline")
                key_conflict = st.text_input("Key conflict or most interesting point")
            with col2:
                target_audience = st.selectbox("Target audience", ["General news readers", "Specialist/Expert audience", "Other"])
                sources = st.text_area("Sources & resources", height=90)
            reporting_stage = st.selectbox("How far along are you?", ["Just an idea", "Some reporting done", "Drafting in progress"])
            pitch_style = st.radio(
                "AI editor style?",
                ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                horizontal=True,
            )
        submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
        if submitted:
            if not pitch_text or not pitch_text.strip():
                st.error("Please paste your story pitch before submitting.")
            else:
                st.session_state.form_data = dict(
                    pitch_text=pitch_text,
                    story_type_choice=story_type_choice,
                    prior_coverage=prior_coverage,
                    prior_coverage_effect=prior_coverage_effect,
                    working_headline=working_headline,
                    key_conflict=key_conflict,
                    target_audience=target_audience,
                    sources=sources,
                    reporting_stage=reporting_stage,
                    coaching_style=pitch_style,
                )
                go_to("recipe")
    if st.button("← Back to Portal"):
        go_to("portal")

# =========================================================
# PAGE: Pitch Recipe
# =========================================================
elif st.session_state.page == "recipe":
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown("This prompt combines your pitch with expert coaching instructions.")
    st.markdown("---")

    data = st.session_state.get("form_data", {})
    level = st.session_state.get("journalism_level", "N/A")

    context_lines = [
        f"- Story Framework: {data.get('story_type_choice', 'N/A')}",
        f"- User Experience Level: {level}",
        f"- Prior Coverage: {data.get('prior_coverage', 'N/A')}",
        f"- Effect of Prior Coverage: {data.get('prior_coverage_effect', 'N/A')}",
        f"- Target Audience: {data.get('target_audience', 'N/A')}",
        f"- Stage: {data.get('reporting_stage', 'N/A')}",
    ]
    if data.get("working_headline"):
        context_lines.append(f'- Working Headline: "{data["working_headline"]}"')
    if data.get("key_conflict"):
        context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get("sources"):
        context_lines.append(f"- Sources: {data['sources']}")
    context_lines.append(f'- User Pitch: "{(data.get("pitch_text","").strip())}"')
    full_context = "\n".join(context_lines)

    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor acting as a Socratic coach. Your goal is to help a student journalist strengthen their story pitch by asking guiding questions—**not** by writing for them. Adapt your tone to the user's experience level (**{level}**).

    # 2. CONTEXT
{full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK
    Before you respond, silently evaluate the pitch with red/green flags (newsworthiness, sourcing, ethics, prior coverage).

    # 4. CONVERSATION FLOW
    - **Turn 1:** Genuine editorial reaction + one foundational question about the biggest gap.
    - **Turns 2–3:** Drill on (newsworthiness, sourcing, ethics, structure).
    - **Turn 4+:** Offer a choice → A) move to reporting plan; B) rethink angle; C) consider a different story.

    # 5. CORE CONSTRAINTS
    - **Guide, don’t write.** Do not name specific people/institutions.
    - Probe verification for any political/data claims.
    - The outcome is better judgment, not perfect prose.
    """)

    cmain, cside = st.columns([2, 1])
    with cmain:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=460, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt")
    with cside:
        with st.container(border=True):
            st.markdown("## Anatomy of the Prompt")
            st.markdown(
                "A prompt is more than just a question; it's a set of instructions that guides the AI's response. "
                "Good **prompt engineering** means designing those instructions to get the most helpful and accurate coaching."
            )
            st.markdown("---")
            st.markdown(
                """
1. **ROLE & GOAL** — Who the AI should be and what it’s trying to achieve.

2. **CONTEXT** — Your answers/pitch so questions are specific and relevant.

3. **FLOW** — Plan for opening, probing, and choice of next steps.

4. **CONSTRAINTS** — Guardrails: *coach, don’t do*; be Socratic; avoid naming people/institutions; require verification.

5. **ETHICAL LENS** — Consider bias, harm, privacy, diverse sourcing.

6. **FINAL GOAL REMINDER** — You leave with a clear, actionable checklist you built.
                """
            )

    st.markdown("---")
    st.markdown("**💡 Tip:** Paste this into any AI chat.")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with a2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with a3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("---")
    if st.button("Continue to Workshop →", type="primary"):
        go_to("follow_on")
    if st.button("← Back to Questionnaire"):
        go_to("questionnaire")

# =========================================================
# PAGE: Workshop / Follow-on
# =========================================================
elif st.session_state.page == "follow_on":
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    st.title("Workshop Results & Next Steps")
    st.markdown("Paste highlights from your coaching session for a **second opinion** or to plan next steps.")
    st.markdown("---")

    with st.container(border=True):
        st.subheader("Option 1: Ask the **Same** Coach for a New Lens")
        new_persona = st.selectbox("New coaching style:", ["Skeptical Editor", "Audience Advocate", "Tough Desk Editor"])
        if st.button("Generate 'New Perspective' Prompt"):
            follow_up = textwrap.dedent(f"""
            You are continuing a coaching session on a story/pitch. Adopt the **{new_persona}** lens for this reply only.
            - Briefly restate the pitch’s reader promise (1 sentence).
            - Ask **two** pointed questions from this lens that would most improve the work.
            - Offer **one** risk you’d want verified before publication.
            End under 150 words. Do **not** rewrite the pitch.
            """)
            st.code(follow_up, language="markdown")
            st.info("Copy this into your **existing** AI conversation.")

    with st.container(border=True):
        st.subheader("Option 2: Get a **Full Review** from a **Different** AI")
        transcript = st.text_area("Paste 5–15 key turns from your AI coaching session:", height=220)
        w, c = get_counter(transcript)
        st.caption(f"Live counter: **{w} words · {c} characters**")
        if st.button("Generate 'Reviewer' Prompt"):
            if transcript.strip():
                reviewer = textwrap.dedent(f"""
                You are reviewing a **coaching transcript** between a journalist and an AI about a story/pitch.
                Your job: audit the **quality of the coaching** and surface missed opportunities.

                TRANSCRIPT (may be partial):
                ---
                {transcript.strip()}
                ---

                TASK
                1) **What worked:** 2 things the coach did well (brief).
                2) **What was missed:** 3 **specific** Socratic questions the coach *should* have asked.
                3) **Evidence & verification:** 2 claims/assumptions that need sourcing and **how** to check them.
                4) **Action plan:** 3 concrete next reporting steps.
                5) **One risk call-out:** The single biggest failure mode if they proceed as is.

                Do **not** rewrite the pitch; point the human to actions, not prose.
                """)
                st.code(reviewer, language="markdown")
                st.info("Paste the prompt above into a **different** AI (e.g., if you used Claude, try Gemini).")
            else:
                st.warning("Please paste transcript highlights first.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Start Another Pitch", use_container_width=True):
            go_to("questionnaire")
    with col2:
        if st.button("← Back to Portal", use_container_width=True):
            go_to("portal")
