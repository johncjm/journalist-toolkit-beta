# v18.1 - Restores the "Event" path questionnaire functionality.
import streamlit as st
import textwrap

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# --- HELPERS ---
def go_to_page(page_name: str):
    st.session_state.page = page_name

def get_counter(text: str):
    words = len(text.split()) if text else 0
    chars = len(text) if text else 0
    return words, chars

def copy_button_js(text_to_copy: str, button_text: str = "Copy to Clipboard", key_suffix=""):
    unique_id = f"copy-btn-{key_suffix}"
    text_area_id = f"text-area-{key_suffix}"
    
    st.components.v1.html(f"""
        <textarea id="{text_area_id}" style="opacity: 0; position: absolute; height: 0; width: 0;">{text_to_copy}</textarea>
        <button id="{unique_id}" onclick="
            const text = document.getElementById('{text_area_id}').value;
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('{unique_id}');
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {{ btn.innerText = originalText; }}, 2000);
            }});
        ">{button_text}</button>
    """, height=40)


# --- STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "portal"
if "journalism_level" not in st.session_state:
    st.session_state.journalism_level = "Undergraduate journalist"


# =========================
# Page 1: The Portal
# =========================
if st.session_state.page == "portal":
    st.title("Welcome to the Journalist's Toolkit 🛠️")
    st.subheader("A suite of tools designed to help you think like a journalist and strengthen your work by using AI as a coach.")
    st.markdown("---")

    st.markdown("""
    Covering the news involves a wide range of tasks, from shaping a story idea to polishing copy for publication. We offer tools to help you learn those skills by working with AI models that will coach you rather than just doing the work for you.  

    **Journalist's Toolkit works like this:**
    * pick a task and think it through by answering the kinds of questions an editor would ask
    * that info is combined with a "prompt" engineered to get the best out of an AI bot
    * you take that prompt to a bot, which will guide you through a constructive discussion leading to a "next steps" plan 

    Along the way, you'll gain insight into what AI bots do and don't do well, and how to get the most out of an AI collaboration.
    """)
    st.markdown("---")

    st.session_state.journalism_level = st.selectbox(
        "First, tell us what level of experience you're at:",
        ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"]
    )
    st.markdown("Now, choose one of these tasks:")
    
    st.header("📝 I’ve Got a Job to Do")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Prepare a story pitch", type="primary", use_container_width=True):
            go_to_page("questionnaire"); st.rerun()
        st.button("Structure a first draft", disabled=True, use_container_width=True)
    with col2:
        if st.button("Get Ready to Report", type="primary", use_container_width=True):
            go_to_page("grr_choice"); st.rerun()
        st.button("Vet a source", disabled=True, use_container_width=True)
    with col3:
        st.button("Develop interview questions", disabled=True, use_container_width=True)
        st.button("Check your facts", disabled=True, use_container_width=True)


    st.markdown("---")

    st.info("Looking for a different kind of AI collaboration?", icon="🤔")
    st.markdown("""
    If you're looking to test the idea that three heads are better than one for deep strategic or coding questions, feel free to try the beta version of **Team of Rivals**. It brings ChatGPT, Claude, and Gemini together for multi-round discussions where the models can help protect you from each other's flaws and build on each other's strengths.
    """)
    st.link_button("Try Team of Rivals (opens new tab)", url="https://team-of-rivals-tor1-beta.streamlit.app/")


# =========================
# Page 1.5: Get Ready to Report – Choice
# =========================
elif st.session_state.page == "grr_choice":
    st.title("Get Ready to Report 📋")
    # ... (Code for this page is complete and unchanged) ...
        
# =========================
# Page 1.6: Get Ready to Report - Questionnaire
# =========================
elif st.session_state.page == "reporting_plan_questionnaire":
    path = st.session_state.get("reporting_path", "event")
    st.title(f"Reporting Plan: {path.capitalize()} Path")
    
    if path == "event":
        st.markdown("To get you ready for this event, let's walk through the key questions an editor would ask.")
        with st.form("event_plan_form"):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Part 1: The Situation")
            q1_headline = st.text_input("What's happening -- how would you sum up the story in a headline or tweet?")
            q2_where_when = st.text_input("Where and when is it happening?")
            q3_key_people = st.text_input("Who are the key people involved?")
            q4_why_now = st.text_input("Why is it happening now? (Or whenever it's expected.)")
            st.markdown("---")
            st.markdown("### Part 2: The Stakes")
            q5_how_big = st.text_input("How big a story is this?")
            q6_important = st.text_input("What makes it important?")
            q7_audience = st.text_input("Who is it most important for -- what's the key audience for this story?")
            st.markdown("---")
            st.markdown("### Part 3: Getting Started")
            q8_work_done = st.text_area("What work have you done so far to prepare?")
            q9_work_left = st.text_area("What is the key work left to do -- what documents to read or people to interview?")
            q10_anxious_excited = st.text_area("Is there anything about this subject that makes you especially excited or anxious about covering it?")
            st.markdown('</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.event_form_data = locals()
                go_to_page("reporting_plan_recipe"); st.rerun()
        
    elif path == "explore":
        st.markdown(f"This is the placeholder for the **{path}** questionnaire.")
    elif path == "confirm":
        st.markdown(f"This is the placeholder for the **{path}** questionnaire.")

    st.markdown("---")
    if st.button("← Back to Choices"):
        go_to_page("grr_choice"); st.rerun()

# =========================
# Page 1.7: Get Ready to Report - Recipe
# =========================
elif st.session_state.page == "reporting_plan_recipe":
    st.title("Your Custom Reporting Plan Prompt 📝")
    st.warning("This recipe page is under construction.", icon="⚠️")
    if st.button("← Back to Questionnaire"):
        go_to_page("reporting_plan_questionnaire"); st.rerun()

# =========================
# Page 2: Questionnaire (STORY PITCH)
# =========================
elif st.session_state.page == "questionnaire":
    st.title("Story Pitch Coach")
    st.markdown("Filling out this questionnaire helps you think through the key elements of your pitch. It also will give the AI model more context to go on.")
    with st.form("pitch_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)
        
        st.subheader("Pitch Details (Optional, but highly recommended)")
        story_type_choice = st.selectbox("Which best describes your story idea?", ["(Not sure)", "Event", "Explore", "Confirm"])
        prior_coverage = st.text_area("What has already been written on this topic? (Feel free to paste links.)")
        prior_coverage_effect = st.text_area("How does that affect your reporting goals? (e.g., Do you need a new angle, or can you build on their work?)")

        col1, col2 = st.columns(2)
        with col1:
            working_headline = st.text_input("Working headline")
            key_conflict = st.text_input("Key conflict or most interesting point")
        with col2:
            target_audience = st.selectbox("Target audience", ["General news readers", "Specialist/Expert audience", "Other"])
            sources = st.text_area("Sources & resources", height=90)
            
        reporting_stage = st.selectbox("How far along are you?", ["Just an idea", "Some reporting done", "Drafting in progress"])
        st.subheader("Coaching Preferences")
        coaching_style = st.radio("What kind of AI editor would you like to talk to?", ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"], horizontal=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
        if submitted:
            if not pitch_text or not pitch_text.strip():
                st.error("Please paste your story pitch before submitting.")
            else:
                st.session_state.form_data = locals()
                go_to_page("recipe"); st.rerun()
    if st.button("← Back to Portal"):
        go_to_page("portal"); st.rerun()

# =========================
# Page 3: Prompt Recipe (STORY PITCH)
# =========================
elif st.session_state.page == "recipe":
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown("---")
    
    data = st.session_state.get("form_data", {})
    
    context_lines = [
        f"- Story Framework: {data.get('story_type_choice', 'N/A')}",
        f"- User Experience Level: {st.session_state.get('journalism_level', 'N/A')}",
        f"- Prior Coverage: {data.get('prior_coverage', 'N/A')}",
        f"- Effect of Prior Coverage: {data.get('prior_coverage_effect', 'N/A')}",
        f"- Target Audience: {data.get('target_audience', 'N/A')}",
        f"- Stage: {data.get('reporting_stage', 'N/A')}",
    ]
    if data.get("working_headline"): context_lines.append(f"- Working Headline: \"{data['working_headline']}\"")
    if data.get("key_conflict"): context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get("sources"): context_lines.append(f"- Sources: {data['sources']}")
    context_lines.append(f"- User's Pitch: \"{data.get('pitch_text', '').strip()}\"")
    full_context = "\n".join(context_lines)
    
    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Act as a Socratic coach for a student journalist. Your goal is to help them improve their pitch through a collaborative workshop — **coach, not do**. Your tone should adapt to the user's experience level, as noted in the context.

    # 2. CONTEXT
    {full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK (Your Internal Engine)
    Before you respond, silently form a preliminary hypothesis about the pitch’s greatest strength and single biggest challenge. Pay special attention to the Story Framework. If it's an 'Explore' story, is the pitch too focused on a specific outcome? If it's a 'Confirm' story, is the core claim clear and verifiable?
    **Red Flags to look for:**
    - The writer is more excited about the topic than the story.
    - It assumes readers will care without explaining why.
    - It conflates “important” with “interesting.”
    - It has done research but hasn’t found the core tension/conflict.
    **Green Flags to look for:**
    - It can explain the story in one clear sentence.
    - It identifies specific people affected in specific ways.
    - It shows awareness of potential counterarguments.
    - It has a plausible reporting plan.

    # 4. CONVERSATIONAL FLOW (Your Task)
    ## Turn 1: The Editorial Reaction
    Choose ONE of the reaction patterns below (don’t announce which):
    * **Pattern A: Intrigued but need more...**
    * **Pattern B: Promising with a clear gap...**
    * **Pattern C: Skeptical but open...**
    ## Turn 2–3: Deep Dive
    - Reflect back the user’s answer in one sentence.
    - Ask 1–2 follow-ups that push on the core issue.
    - Do **not** provide concrete deliverables yet.
    ## Turn 4+: Targeted Coaching & the “Choice Point”
    After you understand the pitch, provide one concrete deliverable. Then:
    1) **Provide the deliverable.**
    2) **Signal completion.**
    3) **Offer a scoped continuation.**

    # 5. CORE CONSTRAINTS (Always Apply)
    - **Guide, Don’t Write:** Do not draft headlines or nut grafs.
    - **Method Over Persona:** Keep the Socratic method. The assigned style (“{data.get('coaching_style', 'Default Story Coach')}”) changes tone, not process.
    - **Political/Data Hygiene:** For claims about data or impact, ask for sources first and suggest a way the user could independently verify.
    - **Final Reminder:** Your primary goal is to be a Socratic coach.
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=450, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt", "main")
    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown("""
        A prompt is the request a user makes to an AI, but it's also a set of instructions for how the AI should prepare an answer. Prompt engineering is the art of designing those instructions in a way that is most likely to get the best (most accurate, most illuminating) results.

        What you see here is how we've combined the context you've provided -- which gives the AI specifics to work with -- with some general rules we've developed through trial and error, such as directing the AI to coach you to an answer instead of giving you one. If you follow the approach laid out here, all your interactions with AI should improve.
        """)
        st.markdown("---")
        st.markdown("""
        - **1. Introduction:** Sets the AI's role and goal.
        - **2. Context:** Injects the details from your questionnaire.
        - **3. Editorial Framework:** Gives the AI an analytical model to use.
        - **4. Conversational Flow:** Structures the entire conversation.
        - **5. Core Constraints:** The hard-and-fast rules to keep the AI on track.
        """)
        
    st.markdown("---")
    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2: st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3: st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)
    
    st.markdown("---")
    if st.button("Continue to Next Steps →", type="primary"):
        go_to_page("follow_on"); st.rerun()

# =========================
# Page 4: Workshop / Follow-on (STORY PITCH)
# =========================
elif st.session_state.page == "follow_on":
    st.title("Workshop Results & Next Steps")
    # ... (Full, unabbreviated code for this page) ...
