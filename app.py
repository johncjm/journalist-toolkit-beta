
# v15.9 - Adds "Anatomy of the Prompt" explainer to the Event recipe page
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


# =========================
# Page 1: The Portal
# =========================
if st.session_state.page == "portal":
    st.title("Welcome to the Journalist's Toolkit 🛠️")
    st.subheader("A suite of tools designed to help you think like a journalist and strengthen your work by using AI as a coach.")
    st.markdown("---")

    st.header("📝 I’ve Got a Job to Do")
    st.markdown("""
    Covering the news involves a wide range of tasks, from shaping a story idea to polishing copy for publication. We offer tools to help you learn those skills by working with AI models that will coach you rather than just doing the work for you.  

    **Journalist's Toolkit works like this:**
    * pick a task and think it through by answering the kinds of questions an editor would ask
    * that info is combined with a "prompt" engineered to get the best out of an AI bot
    * you take that prompt to a bot, which will guide you through a constructive discussion leading to a "next steps" plan 

    Along the way, you'll gain insight into what AI bots do and don't do well, and how to get the most out of an AI collaboration.
    """)
    
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
    st.markdown("Different kinds of stories call for different kinds of preparation. How would you describe your story?")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Event", use_container_width=True):
            st.session_state.reporting_path = "event"
            go_to_page("reporting_plan_questionnaire"); st.rerun()
        st.markdown("**You know that something is going to happen that seems worth covering, whether a one-shot City Council meeting or a months-long City Council campaign.**")
        with st.expander("Click for examples"):
            st.markdown("""
            - A school board vote on a controversial new curriculum.
            - A planned protest at a corporate headquarters.
            - The quarterly earnings report for a major local employer.
            - A star athlete's final home game before retirement.
            """)
    
    with col2:
        if st.button("Explore", use_container_width=True):
            st.session_state.reporting_path = "explore"
            go_to_page("reporting_plan_questionnaire"); st.rerun()
        st.markdown("**You think there's something interesting to write about in a given subject, whether it's a social-media craze or a neighborhood or a business trend, but you aren't sure what the story angle will turn out to be.**")
        with st.expander("Click for examples"):
            st.markdown("""
            - Profiling a neighborhood that's rapidly gentrifying.
            - Investigating the rise of a new local fashion trend.
            - Understanding the culture of a local amateur sports league.
            - Documenting the daily life of a street artist.
            """)

    with col3:
        if st.button("Confirm", use_container_width=True):
            st.session_state.reporting_path = "confirm"
            go_to_page("reporting_plan_questionnaire"); st.rerun()
        st.markdown("**You hear or have other reason to think that X has happened or is happening and are trying to figure out if that's true -- and how to get enough material to be able to write about it.**")
        with st.expander("Click for examples"):
            st.markdown("""
            - A tip that a local restaurant is closing due to health violations.
            - A rumor that a city official has a conflict of interest.
            - A claim on social media that a local factory is polluting a river.
            - An observation that a specific crime is on the rise in a community.
            """)
    
    st.markdown("---")
    if st.button("← Back to Portal"):
        go_to_page("portal"); st.rerun()
        
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
        st.markdown(f"This is the placeholder for the **{path}** questionnaire. We will build the form here.")
    elif path == "confirm":
        st.markdown(f"This is the placeholder for the **{path}** questionnaire. We will build the form here.")

    st.markdown("---")
    if st.button("← Back to Choices"):
        go_to_page("grr_choice"); st.rerun()

# =========================
# Page 1.7: Get Ready to Report - Recipe
# =========================
elif st.session_state.page == "reporting_plan_recipe":
    st.title("Your Custom Reporting Plan Prompt 📝")
    st.markdown("This prompt has been assembled from your answers. Take it to your preferred AI chat tool to start your coaching session.")
    st.markdown("---")
    
    data = st.session_state.get("event_form_data", {})
    
    context_string = f"""
- Headline/Tweet: {data.get('q1_headline', 'N/A')}
- Where & When: {data.get('q2_where_when', 'N/A')}
- Key People: {data.get('q3_key_people', 'N/A')}
- Why Now: {data.get('q4_why_now', 'N/A')}
- Story Size: {data.get('q5_how_big', 'N/A')}
- What Makes It Important: {data.get('q6_important', 'N/A')}
- Key Audience: {data.get('q7_audience', 'N/A')}
- Work Done So Far: {data.get('q8_work_done', 'N/A')}
- Key Work Left: {data.get('q9_work_left', 'N/A')}
- Reporter's Mindset: {data.get('q10_anxious_excited', 'N/A')}
"""

    final_prompt = textwrap.dedent(f"""
    # 1. ROLE & GOAL
    You are an experienced and encouraging assignment editor acting as a Socratic coach for a student journalist. Your primary goal is to help them build a comprehensive preparation checklist for an upcoming event. Your philosophy is "coach, not do." You will help them think through story angles, logistics, and sourcing by asking guiding questions.

    # 2. CONTEXT
    The student has provided the following preparatory notes for an event they need to cover.
    {context_string}

    # 3. TASK: THE COACHING SESSION FLOW

    ## PART A: THE OPENING (Handling Incomplete Answers)
    The student's answers may be incomplete. Your first task is to create a natural and collaborative entry point to the coaching session based on the completeness of their answers.

    **IF the answers are mostly complete (e.g., only 1-2 minor gaps):**
    1.  **Acknowledge & Validate:** Start by briefly and genuinely acknowledging something specific the user DID provide (e.g., "Thanks for laying this out. You've clearly identified the key players...").
    2.  **Identify a Single Gap:** Silently review their answers. If a foundational element is missing, select ONLY ONE to focus on. Prioritize gaps in this order: (1) The "why" (newsworthiness), (2) The "who" (audience), (3) The "what" (what's at stake).
    3.  **Ask Your Opening Question:** Frame your first question as a collaborative way to build on their existing idea. Use curious, empowering language. (e.g., "A great place for us to start is to build on your idea about X. To help focus our plan, could you tell me more about Y?").

    **IF the answers are very sparse (e.g., multiple foundational sections are brief or empty):**
    1.  **Ask for Permission:** Do not quiz the user. Instead, offer them a choice. Use this script: "Thanks for this start. To give you the best possible coaching, I see a few areas where more detail would be helpful. Shall we quickly walk through those now, or would you prefer to just dive into the main discussion?"
    2.  **Act on Their Choice:**
        - If they say YES, ask 2-3 of the most important unanswered questions.
        - If they say NO, proceed immediately to Part B using only the information you have.

    ## PART B: THE MAIN COACHING DIALOGUE
    After the opening exchange, your primary task is to guide the student in building a practical checklist. Engage in a Socratic dialogue, asking questions that help them think through:
    - **Story Angles:** Start here. Ask them what they expect to happen and why, and what the alternatives are. (e.g., "What's your best guess about what's going to happen? What leads you to think that? What else might happen?")
    - **Logistics:** Beyond the when/where, what do they need to arrange? (e.g., "What's your plan for getting there and setting up? Do you need press credentials?")
    - **Sourcing:** Who do they need to talk to before, during, and after the event? (e.g., "Besides the key players, who else might have a unique perspective on this?")
    - **Contingency Planning:** What could go wrong? (e.g., "What's your backup plan if you can't get a comment from your key source?")

    # 4. CORE CONSTRAINTS
    - Coach, Don't Do: Do not provide answers or write lists for the user. Your role is to ask the questions that help them build their own plan.
    - Be Socratic: Ask open-ended, guiding questions.
    - Respect User Choice: If the user declines the initial gap-filling, do not circle back to it.
    - Goal-Oriented: Keep the conversation focused on the goal: producing a concrete, actionable preparation checklist for the student.

    # 5. FINAL GOAL REMINDER
    Remember, your primary goal is to be a Socratic coach. The final output of this conversation should be that the student has a clear, actionable checklist that *they* have built. Your role is to ask the guiding questions that lead them to that outcome.
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=450, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt", "main")
    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown("""
        - **1. Role & Goal:** Sets the AI's persona (an experienced editor) and its core objective (to coach, not do).
        - **2. Context:** Injects the specific answers from your questionnaire, giving the AI the raw material it needs.
        - **3. The Coaching Flow:** This is the AI's main playbook. It includes our sophisticated two-tiered logic for starting the conversation and then outlines the key topics for the main coaching dialogue.
        - **4. Core Constraints:** These are the hard-and-fast rules to keep the AI on track, ensuring it remains a Socratic guide.
        - **5. Final Goal Reminder:** A final, clear instruction that re-centers the AI on its most important task: helping the user build their own plan.
        """)

    st.markdown("---")
    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2: st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3: st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("---")
    if st.button("← Back to Questionnaire"):
        go_to_page("reporting_plan_questionnaire"); st.rerun()

# =========================
# Page 2: Questionnaire
# =========================
elif st.session_state.page == "questionnaire":
    st.title("Story Pitch Coach")
    # ... (Full, unchanged code for the Story Pitch tool) ...

# =========================
# Page 3: Prompt Recipe
# =========================
elif st.session_state.page == "recipe":
    st.title("Your Custom Prompt Recipe 📝")
    # ... (Full, unchanged code for the Story Pitch tool) ...

# =========================
# Page 4: Workshop / Follow-on
# =========================
elif st.session_state.page == "follow_on":
    st.title("Workshop Results & Next Steps")
    # ... (Full, unchanged code for the Story Pitch tool) ...
