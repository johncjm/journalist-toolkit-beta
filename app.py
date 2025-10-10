# v21.0 - Redesigned portal with compressed layout and improved CSS throughout
import streamlit as st
import textwrap

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Base Styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card Component */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Portal Page Specific */
    .portal-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 2.5rem 2.5rem 1.75rem 2.5rem;
        border-radius: 16px 16px 0 0;
        margin: -1rem -1rem 0 -1rem;
        position: relative;
        overflow: hidden;
    }
    
    .portal-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .portal-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .portal-subtitle {
        font-size: 1.15rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* How It Works Section */
    .how-it-works-box {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Caveat Section - Subdued */
    .caveat-box {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #64748b;
    }
    
    /* Workflow Steps */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .workflow-step {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    
    .workflow-step:hover {
        transform: translateY(-2px);
    }
    
    /* Task Grid - 2 columns */
    .task-grid-2col {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
    
    /* Inline Level Selector */
    .inline-selector {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #f1f5f9;
        padding: 0.85rem 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .inline-selector label {
        white-space: nowrap;
        font-weight: 600;
        color: #475569;
    }
    
    /* Feedback Button */
    .feedback-center {
        text-align: center;
        margin: 2rem 0 1.5rem 0;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .workflow-grid, .task-grid-2col {
            grid-template-columns: 1fr;
        }
        .inline-selector {
            flex-direction: column;
            align-items: stretch;
        }
    }
</style>
""", unsafe_allow_html=True)


# --- HELPERS ---
def go_to_page(page_name: str):
    st.session_state.page = page_name
    st.rerun()

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
    # Header
    st.markdown('<div class="portal-header">', unsafe_allow_html=True)
    st.markdown('<h1>🛠️ Journalist\'s Toolkit</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">AI-powered coaching tools designed to stand in for an editor, help you think like a journalist and strengthen your work.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reduced top padding
    st.markdown('<div style="padding: 1.75rem 0 0 0;">', unsafe_allow_html=True)
    
    # How It Works
    st.markdown('<div class="how-it-works-box">', unsafe_allow_html=True)
    st.markdown("### How It Works")
    st.markdown("Journalism requires many skills. We help you develop them by using AI as a coach rather than a shortcut.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="workflow-step">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.6rem auto; font-weight: 700;">1</div>
            <h4 style="font-size: 0.9rem; margin-bottom: 0.35rem;">Pick a Task</h4>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0;">Choose what you need help with (pitch, reporting, etc.)</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="workflow-step">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.6rem auto; font-weight: 700;">2</div>
            <h4 style="font-size: 0.9rem; margin-bottom: 0.35rem;">Answer Questions</h4>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0;">Think through the kind of questions an editor would ask</p>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="workflow-step">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.6rem auto; font-weight: 700;">3</div>
            <h4 style="font-size: 0.9rem; margin-bottom: 0.35rem;">Get Your Prompt</h4>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0;">We generate expert coaching instructions for an AI</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="workflow-step">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 0.6rem auto; font-weight: 700;">4</div>
            <h4 style="font-size: 0.9rem; margin-bottom: 0.35rem;">Start the Coaching</h4>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0;">Copy the prompt into an AI model and begin a dialogue</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Caveat Section
    st.markdown('<div class="caveat-box">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.75rem;">
        <div style="background: white; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; border: 2px solid #cbd5e1;">📋</div>
        <h3 style="color: #475569; font-size: 1.05rem; margin: 0;">Copy and Paste, Huh?</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin: 0;"><strong>Yes!</strong> This tool works with other tools—it generates smart prompts that set up great discussions in whatever AI model you prefer. This does add a step. But here\'s why that\'s a deliberate choice: Working this way makes the tool <strong>always free</strong>, lets you <strong>choose</strong> the model you trust most and gives <strong>better performance</strong> than you\'d get from an API version.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get Started
    st.markdown("### Get Started")
    
    # Inline level selector
    col_label, col_select = st.columns([1, 3])
    with col_label:
        st.markdown('<p style="font-weight: 600; color: #475569; padding-top: 0.35rem; margin: 0;">Your experience level:</p>', unsafe_allow_html=True)
    with col_select:
        st.session_state.journalism_level = st.selectbox(
            "level",
            ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"],
            label_visibility="collapsed"
        )
    
    st.markdown('<p style="color: #475569; margin: 1rem 0 1rem 0; font-weight: 600;">Now, choose a task:</p>', unsafe_allow_html=True)
    
    # Task Grid - 2 columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("**Prepare a Story Pitch**\n\nGet coaching on your story idea before you pitch it", use_container_width=True, type="primary"):
            go_to_page("questionnaire")
        if st.button("**Develop Interview Questions**\n\nCraft better questions for your sources", disabled=True, use_container_width=True, help="Coming soon"):
            pass
        if st.button("**Vet a Source**\n\nEvaluate reliability and potential bias", disabled=True, use_container_width=True, help="Coming soon"):
            pass
    
    with col2:
        if st.button("**Get Ready to Report**\n\nBuild a preparation plan for events, explorations, or verification", use_container_width=True, type="primary"):
            go_to_page("grr_choice")
        if st.button("**Structure a First Draft**\n\nGet guidance on organizing your story", disabled=True, use_container_width=True, help="Coming soon"):
            pass
        if st.button("**Check Your Facts**\n\nBuild a verification strategy", disabled=True, use_container_width=True, help="Coming soon"):
            pass
    
    # Feedback Button
    st.markdown('<div class="feedback-center">', unsafe_allow_html=True)
    st.link_button("💬 Tell Us What You Think", url="mailto:johncjm@gmail.com?subject=Journalist's Toolkit Feedback&body=Please share your feedback here:", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer CTA
    st.info("🤔 **Looking for a Different Kind of Collaboration?**\n\nTest whether three AI models working together produce better results than one. Team of Rivals brings ChatGPT, Claude, and Gemini together for multi-round discussions.", icon="💡")
    st.link_button("Try Team of Rivals →", url="https://team-of-rivals-tor1-beta.streamlit.app/", use_container_width=False)
    
    st.markdown('</div>', unsafe_allow_html=True)


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
            go_to_page("reporting_plan_questionnaire")
        st.markdown("**You know that something is going to happen that seems worth covering...**")
        with st.expander("Click for examples"):
            st.markdown("- A school board vote on a controversial policy")
            st.markdown("- A protest or public demonstration")
            st.markdown("- A scheduled speech or press conference")
    
    with col2:
        if st.button("Explore", use_container_width=True):
            st.session_state.reporting_path = "explore"
            go_to_page("reporting_plan_questionnaire")
        st.markdown("**You think there's something interesting to write about...**")
        with st.expander("Click for examples"):
            st.markdown("- Profiling a neighborhood or subculture")
            st.markdown("- Investigating a trend you've noticed")
            st.markdown("- Exploring a community or organization")

    with col3:
        if st.button("Confirm", use_container_width=True):
            st.session_state.reporting_path = "confirm"
            go_to_page("reporting_plan_questionnaire")
        st.markdown("**You hear or have other reason to think that X has happened...**")
        with st.expander("Click for examples"):
            st.markdown("- A tip that a local restaurant is closing")
            st.markdown("- A rumor about school policy changes")
            st.markdown("- An allegation about a public figure")
    
    st.markdown("---")
    if st.button("← Back to Portal"):
        go_to_page("portal")

# =========================
# Page 1.6: Get Ready to Report - Questionnaire
# =========================
elif st.session_state.page == "reporting_plan_questionnaire":
    path = st.session_state.get("reporting_path", "event")
    st.title(f"Reporting Plan: {path.capitalize()} Path")
    
    # --- EVENT PATH ---
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
            q9_prior_coverage = st.text_area("What has already been written or produced on this topic? (Feel free to paste links.)")
            q10_prior_coverage_effect = st.text_area("How does that affect your reporting goals? (e.g., Do you need a new angle, or can you build on their work?)")
            q11_work_left = st.text_area("What is the key work left to do -- what documents to read or people to interview?")
            q12_anxious_excited = st.text_area("Is there anything about this subject that makes you especially excited or anxious about covering it?")
            st.markdown("---")
            event_coaching_style = st.radio(
                "What kind of AI editor would you like to talk to?",
                ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                horizontal=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = {
                    'q1_headline': q1_headline,
                    'q2_where_when': q2_where_when,
                    'q3_key_people': q3_key_people,
                    'q4_why_now': q4_why_now,
                    'q5_how_big': q5_how_big,
                    'q6_important': q6_important,
                    'q7_audience': q7_audience,
                    'q8_work_done': q8_work_done,
                    'q9_prior_coverage': q9_prior_coverage,
                    'q10_prior_coverage_effect': q10_prior_coverage_effect,
                    'q11_work_left': q11_work_left,
                    'q12_anxious_excited': q12_anxious_excited,
                    'coaching_style': event_coaching_style,
                }
                st.session_state.reporting_path = 'event'
                go_to_page("reporting_plan_recipe")

    # --- EXPLORE PATH ---
    elif path == "explore":
        st.markdown("This path helps you explore a topic when you have a hunch there's a story, but you're not sure what it is yet.")
        with st.form("explore_plan_form"):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Part 1: The Territory & The Angle")
            q1_territory = st.text_input("Describe what you want to explore (who, what, or where has your attention?).")
            q2_hunch = st.text_input("What's your hunch or guiding question about it?")
            q3_curiosity = st.text_input("What makes you curious about this right now?")
            q4_audience = st.text_input("Who is the key audience for this story, and why would they care?")
            st.markdown("---")
            st.markdown("### Part 2: Your Starting Point")
            q5_know = st.text_area("What do you already know about this subject?")
            q6_dont_know = st.text_area("What's the most important thing you don't know?")
            q7_prior_coverage = st.text_area("What has already been written or produced on this topic?")
            q8_relationship_bias = st.text_area("What is your relationship to this subject, and what assumptions or biases might you be bringing to it?")
            st.markdown("---")
            st.markdown("### Part 3: The Plan")
            q9_plan_ideas = st.text_area("What are your initial ideas for a reporting plan (people to talk to, places to go, things to observe)?")
            q10_first_step = st.text_input("What's one thing you can do today or tomorrow to get started?")
            st.markdown("---")
            explore_coaching_style = st.radio(
                "What kind of AI editor would you like to talk to?",
                ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                horizontal=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = {
                    'q1_territory': q1_territory,
                    'q2_hunch': q2_hunch,
                    'q3_curiosity': q3_curiosity,
                    'q4_audience': q4_audience,
                    'q5_know': q5_know,
                    'q6_dont_know': q6_dont_know,
                    'q7_prior_coverage': q7_prior_coverage,
                    'q8_relationship_bias': q8_relationship_bias,
                    'q9_plan_ideas': q9_plan_ideas,
                    'q10_first_step': q10_first_step,
                    'coaching_style': explore_coaching_style,
                }
                st.session_state.reporting_path = 'explore'
                go_to_page("reporting_plan_recipe")

    # --- CONFIRM PATH ---
    elif path == "confirm":
        st.markdown("This path helps you verify a specific claim, tip, or rumor.")
        with st.form("confirm_plan_form"):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            q1_claim = st.text_area("The Claim: What is the specific claim, tip, or rumor you are trying to verify? (State it as a single, testable sentence.)")
            q2_source = st.text_area("The Source: Where did this information come from, and what do you know about the source's reliability and potential motivations?")
            q3_stakes = st.text_area("The Stakes: Why does this story matter to your audience?")
            q4_evidence = st.text_area("The Evidence: What would you need to learn to make you comfortable going with the story, and what information would lead you to conclude it's a dead end? What people or documents do you think could provide that evidence one way or the other?")
            q5_risks = st.text_area("The Risks: What worries you most about this story? What else could be going on? Are there any obvious concerns about privacy or harm to sources or other ethical concerns?")
            st.markdown("---")
            confirm_coaching_style = st.radio(
                "What kind of AI editor would you like to talk to?",
                ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
                horizontal=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
            if submitted:
                st.session_state.form_data = {
                    'q1_claim': q1_claim,
                    'q2_source': q2_source,
                    'q3_stakes': q3_stakes,
                    'q4_evidence': q4_evidence,
                    'q5_risks': q5_risks,
                    'coaching_style': confirm_coaching_style,
                }
                st.session_state.reporting_path = 'confirm'
                go_to_page("reporting_plan_recipe")

    st.markdown("---")
    if st.button("← Back to Choices"):
        go_to_page("grr_choice")

# =========================
# Page 1.7: Get Ready to Report - Recipe
# =========================
elif st.session_state.page == "reporting_plan_recipe":
    # Scroll to top fix
    st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)
    
    # Guard against landing here without a path selected
    path = st.session_state.get("reporting_path")
    if not path:
        st.warning("⚠️ No reporting path selected. Please go back and choose a path.", icon="⚠️")
        if st.button("← Back to Get Ready to Report"):
            go_to_page("grr_choice")
        st.stop()
    
    st.title("Your Custom Reporting Plan Prompt 📝")
    st.markdown("This prompt has been assembled from your answers. Take it to your preferred AI chat tool to start your coaching session.")
    st.markdown("---")
    
    context_string = ""
    final_prompt = ""
    data = st.session_state.get("form_data", {})

    # --- Logic for EVENT path ---
    if path == "event":
        context_string = f"""
- Headline/Tweet: {data.get('q1_headline', 'N/A')}
- Where & When: {data.get('q2_where_when', 'N/A')}
- Key People: {data.get('q3_key_people', 'N/A')}
- Why Now: {data.get('q4_why_now', 'N/A')}
- Story Size: {data.get('q5_how_big', 'N/A')}
- What Makes It Important: {data.get('q6_important', 'N/A')}
- Key Audience: {data.get('q7_audience', 'N/A')}
- Work Done So Far: {data.get('q8_work_done', 'N/A')}
- Prior Coverage: {data.get('q9_prior_coverage', 'N/A')}
- Effect of Prior Coverage: {data.get('q10_prior_coverage_effect', 'N/A')}
- Key Work Left: {data.get('q11_work_left', 'N/A')}
- Reporter's Mindset: {data.get('q12_anxious_excited', 'N/A')}
- User Experience Level: {st.session_state.get('journalism_level', 'N/A')}
- Desired Coaching Style: {data.get('coaching_style', 'N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are an experienced and encouraging assignment editor acting as a Socratic coach for a student journalist. Your primary goal is to help them build a comprehensive preparation checklist for an upcoming event. Your philosophy is "coach, not do." You will help them think through story angles, logistics, and sourcing by asking guiding questions.
        
        ## Coaching Style & Tone Adaptation
        Calibrate your tone and the directness of your questions based on the user's selected preferences.
        **Based on User Experience Level:**
        - **High School/Undergraduate:** Assume less foundational knowledge. Explain journalistic concepts simply. Your tone should be highly encouraging.
        - **Grad School/Working Journalist:** Assume foundational knowledge. Your questions can be more direct and focused on higher-level strategic and ethical challenges.
        **Based on Coaching Style:**
        - **Default Story Coach:** A balanced, collaborative, and supportive tone.
        - **Tough Desk Editor (though kind):** More direct, blunt, and challenging. Focus on rigor and finding holes in the plan.
        - **Audience Advocate:** Primarily focused on the reader. Constantly ask "Why would they care?" and "Is this clear to them?"
        - **Skeptic:** Play devil's advocate. Gently question every assumption and push for the evidence.

        # 2. CONTEXT
        The student has provided the following preparatory notes for an event they need to cover.
        {context_string}

        # 3. TASK: THE COACHING SESSION FLOW
        ## PART A: THE OPENING (Handling Incomplete Answers)
        The student's answers may be incomplete. Your first task is to create a natural and collaborative entry point to the coaching session based on the completeness of their answers.
        **IF the answers are mostly complete (e.g., only 1-2 minor gaps):**
        1.  **Acknowledge & Validate:** Start by briefly and genuinely acknowledging something specific the user DID provide.
        2.  **Identify a Single Gap:** Silently review their answers. If a foundational element is missing, select ONLY ONE to focus on. Prioritize gaps in this order: (1) The "why" (newsworthiness), (2) The "who" (audience), (3) The "what" (what's at stake).
        3.  **Ask Your Opening Question:** Frame your first question as a collaborative way to build on their existing idea.
        **IF the answers are very sparse (e.g., multiple foundational sections are brief or empty):**
        1.  **Ask for Permission:** Do not quiz the user. Instead, offer them a choice: "I notice several key areas could use more detail. Would you like me to ask a few clarifying questions to help us build a stronger plan, or would you prefer to dive straight into the coaching?"
        2.  **Act on Their Choice:** If they say YES, ask 2-3 of the most important unanswered questions. If they say NO, proceed immediately to Part B.

        ## PART B: THE MAIN COACHING DIALOGUE
        After the opening exchange, guide the student in building a practical checklist by asking questions about:
        - **Story Angles:** Start here. (e.g., "What's your best guess about what's going to happen? What leads you to think that?")
        - **Logistics:** Ask about practical preparation (e.g., "What access will you need? Who do you need to contact in advance?")
        - **Sourcing:** Help them identify key voices (e.g., "Who are the 3-5 people you absolutely need to talk to?")
        - **Contingency Planning:** Prepare for the unexpected (e.g., "What if the event is canceled or runs late? What's your backup plan?")

        # 4. CORE CONSTRAINTS
        - **Journalistic Skepticism:** For any claims, ask the user how they plan to independently verify them.
        - **Coach, Don't Do:** Do not provide answers or write lists for the user. Do not name specific people or institutions.
        - **Be Socratic:** Ask open-ended, guiding questions.
        - **Respect User Choice:** If the user declines gap-filling, do not circle back to it.

        # 5. ETHICAL & DIVERSITY LENS
        Throughout the conversation, maintain an awareness of potential bias and the importance of diverse sourcing. If the plan seems to overlook a community, ask a guiding question. (Example: "Who are the community groups most affected by this but are at risk of being overlooked?")

        # 6. FINAL GOAL REMINDER
        Remember, your primary goal is to be a Socratic coach. The final output of this conversation should be that the student has a clear, actionable checklist that *they* have built.
        """)
    
    # --- Logic for EXPLORE path ---
    elif path == "explore":
        context_string = f"""
- Territory: {data.get('q1_territory', 'N/A')}
- Guiding Hunch: {data.get('q2_hunch', 'N/A')}
- Curiosity/Timeliness: {data.get('q3_curiosity', 'N/A')}
- Audience: {data.get('q4_audience', 'N/A')}
- Initial Knowledge: {data.get('q5_know', 'N/A')}
- Knowledge Gaps: {data.get('q6_dont_know', 'N/A')}
- Prior Coverage: {data.get('q7_prior_coverage', 'N/A')}
- Relationship & Bias: {data.get('q8_relationship_bias', 'N/A')}
- Initial Reporting Ideas: {data.get('q9_plan_ideas', 'N/A')}
- First Step: {data.get('q10_first_step', 'N/A')}
- User Experience Level: {st.session_state.get('journalism_level', 'N/A')}
- Desired Coaching Style: {data.get('coaching_style', 'N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are an experienced and encouraging editor acting as a Socratic coach for a student journalist. Their goal is exploratory: to find a specific, compelling story within a broad territory of interest. Your primary goal is to guide their discovery process, helping them identify potential angles, characters, and conflicts. Your philosophy is "coach, not do."
        
        ## Coaching Style & Tone Adaptation
        Calibrate your tone and the directness of your questions based on the user's selected preferences.
        **Based on User Experience Level:**
        - **High School/Undergraduate:** Assume less foundational knowledge. Explain journalistic concepts simply. Your tone should be highly encouraging.
        - **Grad School/Working Journalist:** Assume foundational knowledge. Your questions can be more direct and focused on higher-level strategic and ethical challenges.
        **Based on Coaching Style:**
        - **Default Story Coach:** A balanced, collaborative, and supportive tone.
        - **Tough Desk Editor (though kind):** More direct, blunt, and challenging. Focus on rigor and finding holes in the plan.
        - **Audience Advocate:** Primarily focused on the reader. Constantly ask "Why would they care?" and "Is this clear to them?"
        - **Skeptic:** Play devil's advocate. Gently question every assumption and push for the evidence.

        # 2. CONTEXT
        The student has provided the following initial thoughts about a topic they wish to explore:
        {context_string}

        # 3. TASK: THE COACHING SESSION FLOW
        ## PART A: THE OPENING (Handling Incomplete Answers)
        The student's answers may be incomplete. Your first task is to create a natural and collaborative entry point to the coaching session based on the completeness of their answers.
        **IF the answers are very sparse (multiple sections empty or vague):**
        Ask for permission: "I notice several areas could use more detail. Would you like me to ask a few clarifying questions first, or should we dive into exploring this territory together?"
        **IF the answers are mostly complete (only 1-2 gaps):**
        Acknowledge their input warmly, identify a single prioritized gap (Priority: 1. The hunch/angle, 2. Their relationship to the subject, 3. The audience), and ask one collaborative opening question.

        ## PART B: THE EXPLORATORY DIALOGUE (Approx. 3 Turns)
        After the opening, your goal is to help the student broaden their thinking. Ask open-ended, curious questions about their hunch, potential characters/groups, or sources of tension. Do NOT try to narrow them down to a specific story yet. After approximately 3 question-and-answer exchanges, move to Part C.

        ## PART C: THE CHOICE POINT
        After the exploratory dialogue, you must pause, summarize the key themes, and offer the student a clear choice about their next step. Use a script similar to this (you may paraphrase naturally):
        "Okay, this has been a great exploration. We've talked about [theme 1] and [theme 2]. It feels like we're at a crossroads. Based on our conversation, what feels like the right next step for you?
        A) **Focus on a specific angle?** (We can pick one of these themes and start building a concrete reporting plan around it.)
        B) **Do more 'fishing'?** (We can create a plan for more general, open-ended reporting to see what other themes emerge.)
        C) **Reconsider the topic?** (Does it feel like this territory might be less fruitful than you initially thought?)"

        ## PART D: POST-CHOICE ACTIONS
        Your next steps are determined by their choice.
        - **If they choose A (Focus):** Ask them which theme feels most promising and why. Then, guide them to articulate a working hypothesis for that angle and identify a concrete next reporting step.
        - **If they choose B (Go fishing):** Help them design an open-ended reporting plan. Ask: "What would a good 'fishing expedition' look like? Where would you go? Who would you talk to with no specific agenda?" End by helping them define one specific exploratory action.
        - **If they choose C (Reconsider):** Validate this as a smart journalistic decision. Ask: "What made this feel less promising than you hoped?" Help them reflect briefly on what they learned from the exploration.

        # 4. CORE CONSTRAINTS
        - **Journalistic Skepticism:** For any claims or assumptions, ask the user how they might test or verify them. Apply this gently during the exploratory phase.
        - **Coach, Don't Do:** Do not suggest specific story angles during the exploratory phase. Do not name specific people or institutions.
        - **Respect the Process:** The goal of an "Explore" story is discovery. Do not force the user to a specific angle before they are ready. All three outcomes at the "Choice Point" are valid.

        # 5. ETHICAL & DIVERSITY LENS
        Review the student's answer on their relationship to the subject. If they indicate they are an outsider to the community, ask: "As you explore this community, what's your plan for ensuring you represent their perspectives fairly and accurately?"

        # 6. FINAL GOAL REMINDER
        Remember, your primary goal is to guide the student through a process of discovery. A successful session might end with a concrete plan, a plan for more exploration, or a decision to move on to a new topic. All are valid outcomes.
        """)

    # --- Logic for CONFIRM path ---
    elif path == "confirm":
        context_string = f"""
- The Claim: {data.get('q1_claim', 'N/A')}
- The Source: {data.get('q2_source', 'N/A')}
- The Stakes: {data.get('q3_stakes', 'N/A')}
- The Evidence: {data.get('q4_evidence', 'N/A')}
- The Risks: {data.get('q5_risks', 'N/A')}
- User Experience Level: {st.session_state.get('journalism_level', 'N/A')}
- Desired Coaching Style: {data.get('coaching_style', 'N/A')}
"""
        final_prompt = textwrap.dedent(f"""
        # 1. ROLE & GOAL
        You are an experienced, skeptical, and meticulous editor acting as a Socratic coach. Your persona is that of a fact-checker or investigative editor. Your primary goal is to help a student journalist build a rigorous verification plan for a specific claim. Your philosophy is forensic: assume nothing, question everything, and focus on the quality of evidence.
        
        ## Coaching Style & Tone Adaptation
        Calibrate your tone and the directness of your questions based on the user's selected preferences.
        **Based on User Experience Level:**
        - **High School/Undergraduate:** Assume less foundational knowledge. Explain concepts like 'source triangulation' simply. Your tone should be encouraging but firm on standards.
        - **Grad School/Working Journalist:** Assume foundational knowledge. Your questions can be more direct, focusing on complex verification strategies and ethical nuances.
        **Based on Coaching Style:**
        - **Default Story Coach:** A balanced, collaborative, and supportive tone.
        - **Tough Desk Editor (though kind):** More direct, blunt, and challenging. Focus intensely on holes in the evidence.
        - **Audience Advocate:** Frame questions around the reader's need for proof: "How will you convince a skeptical reader this is true?"
        - **Skeptic:** This is your natural state. Lean into playing devil's advocate and questioning every assumption.

        # 2. CONTEXT
        The student is trying to verify the following claim:
        {context_string}

        # 3. TASK: THE COACHING SESSION FLOW
        ## PART A: THE OPENING (Handling Incomplete Answers)
        The student's answers may be incomplete. Your first task is to create a natural and collaborative entry point to the coaching session based on the completeness of their answers.
        **IF the answers are mostly complete (only 1-2 gaps):**
        Acknowledge their input, identify a single prioritized gap (Priority: 1. The Evidence, 2. The Source, 3. The Stakes), and ask one collaborative opening question.
        **IF the answers are very sparse (multiple sections empty):**
        Ask for permission: "I see several key details are missing. Would you like me to ask a few clarifying questions to help us build a verification plan, or should we work with what we have?"

        ## PART B: THE VERIFICATION STRATEGY
        After the opening, your main goal is to guide the student in building a checklist for proving or disproving the claim. The conversation should be procedural and evidence-focused. Ask Socratic questions to help them think through:
        1.  **Assessing the Evidence:** Start by interrogating their answer to "The Evidence" question. (e.g., "You mentioned needing document X to feel comfortable. How will you obtain it? And how will you verify that document is authentic?")
        2.  **The Paper Trail:** Push them to think about what documentation should exist if the claim is true. (e.g., "Beyond what you've listed, what other public records, internal emails, or financial statements would have to exist for this to be true?")
        3.  **Source Triangulation:** Guide them to map out human sources. (e.g., "You've identified the primary source. Who is the best person to dispute this claim? And who is a neutral expert who could provide context without taking a side?")

        ## PART C: THE ETHICAL ASSESSMENT
        Towards the end of the conversation, probe the ethical risks they identified. (e.g., "You mentioned a concern about privacy. What specific steps will you take to minimize harm to the people involved while you are reporting this, especially before the story is confirmed?")

        # 4. CORE CONSTRAINTS
        - **Assume Nothing:** Your default stance is that the claim is unproven.
        - **Triangulate Everything:** Constantly push for multiple sources of evidence (human, documentary, etc.).
        - **Focus on Methodology:** The coaching should be about the *process* of verification, not the narrative of the story.
        - **Coach, Don't Investigate:** Do not suggest specific sources by name or offer to search for documents. Do not name specific people or institutions. Ask questions that help the user identify these things themselves.

        # 5. FINAL GOAL REMINDER
        Remember, your primary goal is to build a verification plan. A successful outcome is a clear checklist for the student. The final story might confirm the claim, debunk it, or conclude that it's unverifiable. All are valid journalistic outcomes.
        """)

    # --- RENDER THE PAGE ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=450, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt", "main")
    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown("""
        A prompt is more than just a question; it's a set of instructions that guides the AI's response. Good **prompt engineering** means designing those instructions to get the most helpful and accurate coaching. What you see on the left is a prompt that combines your specific answers with a proven structure.
        """)
        st.markdown("---")
        st.markdown("""
        Here's how it works:

        1.  **ROLE & GOAL:** This tells the AI *who* to be (e.g., an experienced editor) and *what* its primary objective is (e.g., to coach you by asking questions).

        2.  **CONTEXT:** This is where we inject all your answers from the questionnaire. It gives the AI the specific facts and background it needs to provide tailored feedback.

        3.  **TASK / COACHING FLOW:** This is the AI's playbook for the conversation. It tells it how to start, what topics to cover, and how to guide the dialogue.

        4.  **CORE CONSTRAINTS:** These are the hard-and-fast rules that keep the AI on track, like "coach, don't do" and "be Socratic."

        5.  **ETHICAL & DIVERSITY LENS:** A special instruction to ensure the AI considers fairness, bias, and the importance of including diverse voices in its coaching.

        6.  **FINAL GOAL REMINDER:** A last, clear sentence to re-focus the AI on its most important objective for the session.
        """)
    
    st.markdown("---")
    st.markdown("**💡 Tip:** These links are shortcuts—you can copy this prompt into *any* AI chat tool you prefer.")
    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("---")
    if st.button("← Back to Questionnaire"):
        go_to_page("reporting_plan_questionnaire")

# =========================
# Page 2: Questionnaire (STORY PITCH)
# =========================
elif st.session_state.page == "questionnaire":
    st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)
    
    st.title("Story Pitch Coach")
    st.markdown("Filling out this questionnaire helps you think through the key elements of your pitch...")
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
        pitch_coaching_style = st.radio(
            "What kind of AI editor would you like to talk to?",
            ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
            horizontal=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Generate Prompt Recipe", type="primary", use_container_width=True)
        if submitted:
            if not pitch_text or not pitch_text.strip():
                st.error("Please paste your story pitch before submitting.")
            else:
                st.session_state.form_data = {
                    'pitch_text': pitch_text,
                    'story_type_choice': story_type_choice,
                    'prior_coverage': prior_coverage,
                    'prior_coverage_effect': prior_coverage_effect,
                    'working_headline': working_headline,
                    'key_conflict': key_conflict,
                    'target_audience': target_audience,
                    'sources': sources,
                    'reporting_stage': reporting_stage,
                    'coaching_style': pitch_coaching_style,
                }
                go_to_page("recipe")
    if st.button("← Back to Portal"):
        go_to_page("portal")

# =========================
# Page 3: Prompt Recipe (STORY PITCH)
# =========================
elif st.session_state.page == "recipe":
    st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)
    
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown("AI models work best when given well-structured prompts. This prompt combines your pitch with expert coaching instructions.")
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
    You are an expert journalism mentor acting as a Socratic coach. Your goal is to help a student journalist strengthen their story pitch by asking guiding questions that lead them to discover improvements themselves. Your tone should adapt to the user's experience level: more explanatory and encouraging for beginners, more direct and challenging for experienced journalists.

    # 2. CONTEXT
{full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK (Your Internal Engine)
    Before you respond, silently evaluate the pitch using these criteria. Pay special attention to the Story Framework ({data.get('story_type_choice', 'N/A')}) they've selected.
    
    **Red Flags to look for:**
    - Unclear "so what?" (Why should the audience care?)
    - Vague or missing sourcing
    - Buried lede or unclear focus
    - Overlooked ethical concerns (privacy, harm, vulnerable populations)
    - Prior coverage that undermines the angle (but user hasn't acknowledged it)
    
    **Green Flags to look for:**
    - Clear conflict or tension
    - Specific, named sources
    - Timeliness or newsworthiness
    - Evidence of reporting already done
    - Self-awareness about gaps or challenges

    # 4. CONVERSATIONAL FLOW (Your Task)
    ## Turn 1: The Editorial Reaction
    Start with your gut response to the pitch. What's working? What jumped out at you? Be genuine and specific. Then, ask ONE foundational question about the biggest gap you identified.

    ## Turn 2–3: Deep Dive
    Based on their answer, drill deeper into 1-2 of these areas:
    - **Newsworthiness:** Why now? Why this audience?
    - **Sourcing:** Who can speak to this with authority, experience, or evidence?
    - **Ethical considerations:** Who could be harmed? What permissions are needed?
    - **Story structure:** What's the narrative arc or key conflict?

    ## Turn 4+: Targeted Coaching & the "Choice Point"
    After you've helped them strengthen their thinking, present them with a choice:
    - **Option A:** "This pitch feels solid. Let's talk about your reporting plan."
    - **Option B:** "I think this needs more work before you start reporting. Want to rethink the angle?"
    - **Option C:** "This feels like it might not be the right story. Should we explore whether there's a better angle lurking here?"

    Based on their choice, guide them accordingly. If they choose A, shift to helping them build a reporting checklist. If B or C, help them refine or pivot.

    # 5. CORE CONSTRAINTS (Always Apply)
    - **Guide, Don't Write:** Never write their pitch for them. Ask questions that lead them to solutions. Do not name specific people or institutions.
    - **Method Over Persona:** Your role is more "methodology coach" than "personality." The assigned style ("{data.get('coaching_style', 'Default Story Coach')}") changes tone, not mission.
    - **Political/Data Hygiene:** If the pitch involves political claims or data, probe for verification plans. Don't assume their facts are correct.
    - **Final Reminder:** Your job is to make them a better journalist, not to make this specific pitch perfect. Sometimes the best outcome is realizing it's not the right story.
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=450, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt", "main")
    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown("""
        A prompt is more than just a question; it's a set of instructions that guides the AI's response. Good **prompt engineering** means designing those instructions to get the most helpful and accurate coaching. What you see on the left is a prompt that combines your specific answers with a proven structure.
        """)
        st.markdown("---")
        st.markdown("""
        Here's how it works:

        1.  **ROLE & GOAL:** This tells the AI *who* to be (e.g., an experienced editor) and *what* its primary objective is (e.g., to coach you by asking questions).

        2.  **CONTEXT:** This is where we inject all your answers from the questionnaire. It gives the AI the specific facts and background it needs to provide tailored feedback.

        3.  **TASK / COACHING FLOW:** This is the AI's playbook for the conversation. It tells it how to start, what topics to cover, and how to guide the dialogue.

        4.  **CORE CONSTRAINTS:** These are the hard-and-fast rules that keep the AI on track, like "coach, don't do" and "be Socratic."

        5.  **ETHICAL & DIVERSITY LENS:** A special instruction to ensure the AI considers fairness, bias, and the importance of including diverse voices in its coaching.

        6.  **FINAL GOAL REMINDER:** A last, clear sentence to re-focus the AI on its most important objective for the session.
        """)
        
    st.markdown("---")
    st.markdown("**💡 Tip:** These links are shortcuts—you can copy this prompt into *any* AI chat tool you prefer.")
    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)
    
    st.markdown("---")
    if st.button("Continue to Next Steps →", type="primary"):
        go_to_page("follow_on")
    if st.button("← Back to Questionnaire"):
        go_to_page("questionnaire")

# =========================
# Page 4: Workshop / Follow-on (STORY PITCH)
# =========================
elif st.session_state.page == "follow_on":
    st.components.v1.html("<script>window.scrollTo(0, 0);</script>", height=0)
    
    st.title("Workshop Results & Next Steps")
    st.markdown("Like a newsroom, a **second set of eyes** can reveal new angles and blind spots. Use the tools below to review your session.")
    st.markdown("---")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Get a Second Set of Eyes on Your Workshop")
    
    st.subheader("Option 1: Ask the **Same** Coach for a Different Perspective")
    new_persona = st.selectbox("Choose a new coaching style:", ["Skeptical Editor", "Audience Advocate", "Tough Desk Editor"])
    if st.button("Generate 'New Perspective' Prompt"):
        follow_up_prompt = textwrap.dedent(f"""
        You are continuing a coaching session on a story pitch. Adopt the **{new_persona}** lens for this reply only.
        - Briefly restate what you think the pitch's reader promise is (1 sentence).
        - Ask **two** pointed questions from this new lens that would most improve the pitch.
        - Offer **one** risk you'd want verified before publication.
        
        Finally, add one additional question or risk that wasn't covered above, based on your editorial instinct.
        Keep it tight (under 150 words). Do **not** rewrite the pitch.
        """)
        st.code(follow_up_prompt, language="markdown")
        st.info("Copy this and paste it into your **existing** AI conversation.")

    st.markdown("---")
    
    st.subheader("Option 2: Get a **Full Review** from a **Different** AI")
    transcript = st.text_area("**Paste highlights from your AI coaching session here:**", height=250, placeholder="Paste a few key turns of your conversation here to get a 'second opinion' on the coaching you received.")
    w, c = get_counter(transcript)
    st.caption(f"Live counter: **{w} words · {c} characters**")
    
    if st.button("Generate 'Reviewer' Prompt"):
        if transcript and transcript.strip():
            reviewer_prompt = textwrap.dedent(f"""
            You are reviewing a **coaching transcript** between a journalist and an AI about a story pitch.
            Your job: audit the quality of the coaching and surface missed opportunities.

            ## Materials
            TRANSCRIPT (verbatim, may be partial):
            ---
            {transcript.strip()}
            ---

            ## Your Task
            1) **What worked:** Name 2 things the coach did well (brief).
            2) **What was missed:** List 3 **specific** Socratic questions the coach *should* have asked.
            3) **Evidence & verification:** Identify 2 claims/assumptions that need sourcing or a quick check, and say **how** to check them.
            4) **Action plan:** Give the journalist 3 concrete, next reporting steps.
            5) **One risk call-out:** The single biggest failure mode if they proceed as is.

            After completing the list above, add one final observation based on your editorial instinct that was not covered.
            Constraints: Do **not** rewrite the pitch. Point the human to actions, not prose.
            """)
            st.code(reviewer_prompt, language="markdown")
            st.info("Copy the prompt above and take it to a **different** AI (e.g., if you were using Claude, take this to Gemini).")
        else:
            st.warning("Please paste a transcript to generate a reviewer prompt.")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Self-Reflection")
    st.markdown("""
    - What was the single most useful question the coach asked?
    - Which suggestion did you push back on, and why?
    - What's your immediate next reporting action?
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback button at end
    st.markdown("---")
    col_fb1, col_fb2, col_fb3 = st.columns([1, 2, 1])
    with col_fb2:
        st.link_button("💬 Tell Us What You Think", 
               url="mailto:johncjm@gmail.com?subject=Journalist's Toolkit Feedback&body=Please share your feedback here:", 
               use_container_width=True,
               type="secondary")

    st.markdown("---")
    colb1, colb2 = st.columns([1,1])
    with colb1:
        if st.button("← Start Another Pitch", use_container_width=True):
            go_to_page("questionnaire")
    with colb2:
        if st.button("← Back to Portal", use_container_width=True):
            go_to_page("portal")
