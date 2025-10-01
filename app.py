# v15.7 - New, granular questionnaire for the "Event" path
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
# Page 1.7: Get Ready to Report - Recipe (shell)
# =========================
elif st.session_state.page == "reporting_plan_recipe":
    st.title("Your Custom Reporting Plan Prompt 📝")
    st.markdown("This is the placeholder for the final prompt recipe. We will build it here.")
    
    st.markdown("---")
    if st.button("← Back to Questionnaire"):
        go_to_page("reporting_plan_questionnaire"); st.rerun()

# =========================
# Page 2: Questionnaire
# =========================
elif st.session_state.page == "questionnaire":
    st.title("Story Pitch Coach")
    # ... (Full, unchanged code for the Story Pitch tool)
    with st.form("pitch_form"):
        # ...
# =========================
# Page 3: Prompt Recipe
# =========================
elif st.session_state.page == "recipe":
    st.title("Your Custom Prompt Recipe 📝")
    # ... (Full, unchanged code for the Story Pitch tool)
# =========================
# Page 4: Workshop / Follow-on
# =========================
elif st.session_state.page == "follow_on":
    st.title("Workshop Results & Next Steps")
    # ... (Full, unchanged code for the Story Pitch tool)
