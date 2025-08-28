# v15 - Prompt Persona & Anatomy Update
import streamlit as st
import textwrap

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")

# --- CUSTOM CSS (to approximate the mockup's style) ---
st.markdown("""
<style>
    /* Main card style */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    /* Progress bar styling */
    .step-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2rem;
    }
    .step {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin: 0 0.5rem;
        background: #e9ecef;
        color: #6c757d;
    }
    .step.active { background: #007bff; color: white; }
    .step.completed { background: #28a745; color: white; }
    .step-connector {
        width: 50px;
        height: 2px;
        background: #e9ecef;
    }
    .step-connector.completed { background: #28a745; }
</style>
""", unsafe_allow_html=True)


# --- HELPERS ---
def go_to_page(page_name: str):
    st.session_state.page = page_name

def get_counter(text: str):
    words = len(text.split()) if text else 0
    chars = len(text) if text else 0
    return words, chars

def render_progress_bar(current_page: str):
    pages = ["portal", "questionnaire", "recipe", "follow_on"]
    try:
        current_step_index = pages.index(current_page)
    except ValueError:
        current_step_index = 0 # Default to first step if page not found

    steps_html = ""
    for i, page in enumerate(pages):
        if i > 0:
            connector_class = "step-connector completed" if i <= current_step_index else "step-connector"
            steps_html += f'<div class="{connector_class}"></div>'
        
        step_class = "step"
        if i < current_step_index:
            step_class += " completed"
        elif i == current_step_index:
            step_class += " active"
        
        steps_html += f'<div class="{step_class}">{i+1}</div>'

    st.markdown(f'<div class="step-container">{steps_html}</div>', unsafe_allow_html=True)

def copy_button_js(text_to_copy: str, button_text: str = "Copy to Clipboard", key_suffix=""):
    # A more robust JS for clipboard functionality
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
    render_progress_bar("portal")
    st.title("Welcome to the Journalist's Toolkit 🛠️")
    st.subheader("A suite of tools designed to help you think like a journalist and strengthen your work by using AI as a coach.")
    st.markdown("---")

    st.markdown("#### How It Works")
    st.write("The toolkit guides you through a simple 3-step process to help you with tasks ranging from shaping a story pitch to polishing copy for publication. Along the way, you'll have a chance to learn about productive ways to work with AI models.")

    with st.expander("What’s a “prompt”?"):
        st.markdown("A **prompt** is the request a user makes to an AI, but it's also a set of instructions for how the AI should prepare an answer. **Prompt engineering** is the art of designing those instructions in a way that is most likely to get the best (most accurate, most illuminating) results.")
    
    st.markdown("---")

    colA, colB = st.columns(2)
    with colA:
        st.header("📝 I’ve Got a Job to Do")
        st.markdown("Use a structured prompt to get the best and most reliable coaching on a specific newsroom task.")
        if st.button("Prepare a story pitch", type="primary", use_container_width=True):
            go_to_page("questionnaire"); st.rerun()
        st.button("Structure a first draft", disabled=True, use_container_width=True)
        st.button("Vet a source", disabled=True, use_container_width=True)
    with colB:
        st.header("🤔 I Want to Think Something Through")
        st.markdown("""
            Engage with a "Team of Rivals' -- top AI models ChatGPT, Claude and Gemini work together as an expert panel for more open-ended discussions. They can help you:
            - come up with solutions to complex problems
            - explore new strategies
            - troubleshoot code
            - think through ethical dilemmas
            """)

# =========================
# Page 2: Questionnaire
# =========================
elif st.session_state.page == "questionnaire":
    render_progress_bar("questionnaire")
    st.title("Story Pitch Coach")
    st.markdown("Filling out this questionnaire helps you think through the key elements of your pitch. It also will give the AI model more context to go on.")
    
    with st.form("pitch_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)
        st.subheader("Pitch Details (Optional, but highly recommended)")
        col1, col2 = st.columns(2)
        with col1:
            working_headline = st.text_input("Working headline")
            key_conflict = st.text_input("Key conflict or most interesting point")
            content_type = st.selectbox("Story type", ["News article", "Feature", "Investigation", "Profile", "Opinion", "Other"])
        with col2:
            target_audience = st.selectbox("Target audience", ["General news readers", "Specialist/Expert audience", "Other"])
            sources = st.text_area("Sources & resources", height=90)
            reporting_stage = st.selectbox("How far along are you?", ["Just an idea", "Some reporting done", "Drafting in progress"])
        
        st.subheader("Coaching Preferences")
        coaching_style = st.selectbox("**Choose a coaching style (Optional):**", ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"])
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
# Page 3: Prompt Recipe
# =========================
elif st.session_state.page == "recipe":
    render_progress_bar("recipe")
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown("AI models work best when given well-structured prompts that **provide clear context, define a specific role and goal, and outline the desired format for the response.** What's been assembled here combines the specifics from your story pitch questionnaire with elements from prompts optimized for this task.")

    data = st.session_state.get("form_data", {})
    context_lines = [ f"- Story Type: {data.get('content_type', 'N/A')}", f"- Target Audience: {data.get('target_audience', 'N/A')}", f"- Stage: {data.get('reporting_stage', 'N/A')}",]
    if data.get("working_headline"): context_lines.append(f"- Working Headline: \"{data['working_headline']}\"")
    if data.get("key_conflict"): context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get("sources"): context_lines.append(f"- Sources: {data['sources']}")
    context_lines.append(f"- User's Pitch: \"{data.get('pitch_text', '').strip()}\"")
    full_context = "\n".join(context_lines)

    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Act as a Socratic coach for a student journalist. Your goal is to help them improve their pitch through a collaborative workshop — **coach, not do**. Your tone should be professional, encouraging, and realistic. Praise potential where you see it, but do not offer false encouragement. Be direct about challenges and weaknesses in a constructive way.

    # 2. CONTEXT
    {full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK (Your Internal Engine)
    Before you respond, silently form a preliminary hypothesis about the pitch’s greatest strength and single biggest challenge.

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

    * **Pattern A: Intrigued but need more...** (Good hook; unclear angle/purpose)
        * Example opener: “This could be compelling — the detail about [specific element] pops. I’m not yet seeing the central angle. What’s the one thing that would make a reader stop and pay attention?”

    * **Pattern B: Promising with a clear gap...** (Solid pitch; one major flaw)
        * Example opener: “There’s a strong story here and your sourcing is solid. The main gap is [gap]. To focus that, my first question is: [one precise question about the gap].”

    * **Pattern C: Skeptical but open...** (Topic-y, not yet a story)
        * Example opener: “I’m not seeing a specific angle yet, but I suspect there’s one we can find. What surprised you most when you first thought about this?”

    ## Turn 2–3: Deep Dive
    - Reflect back the user’s answer in one sentence (“So the core tension is X...”).
    - Ask 1–2 follow-ups that push on the core issue.
    - Do **not** provide concrete deliverables yet.

    ## Turn 4+: Targeted Coaching & the “Choice Point”
    After you understand the pitch, provide one concrete deliverable (e.g., verification checklist or next reporting steps). Then:
    1) **Provide the deliverable.**
    2) **Signal completion** (e.g., “This gives you a solid plan to move forward.”)
    3) **Offer a scoped continuation** (e.g., “If one piece is still nagging at you, say which and we’ll probe that.”)

    # 5. CORE CONSTRAINTS (Always Apply)
    - **Failure Mode Handling:** If later info shows you misread the pitch, say so and correct course.
    - **Guide, Don’t Write:** Offer short illustrative examples *as possibilities*. **Do not** draft headlines or nut grafs.
    - **Method Over Persona:** Keep the Socratic method. The assigned style (“{data.get('coaching_style', 'Default Story Coach')}”) changes tone, not process.
    - **Political/Data Hygiene:** For claims about data or impact, ask for sources first and suggest a way the user could independently verify.
    - **Guardrail:** If asked to write the pitch for them, decline and steer back to questions, structure, and next actions.
    - **Final Reminder:** Your primary goal is to be a Socratic coach. Ask guiding questions; do not provide rewritten text or do the work for the user.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=450, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt", "main")
        
    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown("""
        - **1. Introduction:** This sets the stage. It tells the AI its **role** (expert mentor), its **goal** (to coach, not write), and its **persona** (encouraging but realistic).
        - **2. Context:** Here, we inject all the specific details from your questionnaire. This gives the AI the crucial raw material it needs to provide tailored, relevant feedback.
        - **3. Editorial Framework:** This is the AI's 'internal engine.' We give it a specific analytical model (red/green flags) to use, ensuring a high-quality critique.
        - **4. Conversational Flow:** This section structures the entire conversation. By specifying a turn-by-turn process, we prevent the AI from wandering and ensure the session is productive.
        - **5. Core Constraints:** These are the hard-and-fast rules. They handle edge cases, prevent the AI from doing the work for the user, and ensure the interaction stays on track.
        - **6. The Final Reminder:** After all the details, we restate the main goal. It's like planning a party: after discussing the cake and decorations, you say, 'Okay, but let's remember the whole point is to celebrate the birthday person!'
        """)
        if st.button("Just copy it", use_container_width=True):
            st.session_state.just_copied = True
    
    if 'just_copied' in st.session_state and st.session_state.just_copied:
        copy_button_js(final_prompt, "Just copy it", "quick")
        st.session_state.just_copied = False

    st.markdown("---")
    
    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2: st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3: st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.subheader("Tips for Your Coaching Session")
    st.markdown("- **Be an active partner.** Push back, question assumptions, or ask for clarification.\n- **Correct misunderstandings.** If the AI misinterprets something, correct it directly.\n- **Ask for alternatives.** If you don't like a suggestion, ask for a different one.")
    with st.expander("Quick example: weak vs strong opening"):
        st.markdown("**Weak:** “Thoughts?”\n\n**Stronger:** “Acting as a tough but fair editor, what's the single biggest weakness in this pitch that I should fix first?”")
    
    st.markdown("---")

    st.subheader("Come back after you've talked with Coach!")
    st.markdown("To learn more about how to improve your work -- and about how AI works -- come back to this page. You'll be able to continue the discussion with the same AI bot but with it taking on a different perspective, or to get a second opinion on your work -- and an analysis of your interaction with the Coach -- from another AI model.")

    if st.button("Continue to Next Steps →", type="primary"):
        go_to_page("follow_on"); st.rerun()

# =========================
# Page 4: Workshop / Follow-on
# =========================
elif st.session_state.page == "follow_on":
    render_progress_bar("follow_on")
    st.title("Workshop Results & Next Steps")
    st.markdown("Like a newsroom, a **second set of eyes** can reveal new angles and blind spots. Use the tools below to review your session.")
    st.markdown("---")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Get a Second Set of Eyes on Your Workshop")
    st.subheader("Option 1: Ask the **Same** Coach for a Different Perspective")
    new_persona = st.selectbox("Choose a new coaching style:", ["Skeptical Editor", "Audience Advocate", "Tough Desk Editor"])
    if st.button("Generate ‘New Perspective’ Prompt"):
        follow_up_prompt = textwrap.dedent(f"""
        You are continuing a coaching session on a story pitch. Adopt the **{new_persona}** lens for this reply only.
        - Briefly restate what you think the pitch’s reader promise is (1 sentence).
        - Ask **two** pointed questions from this lens that would most improve the pitch.
        - Offer **one** risk you’d want verified before publication.
        
        Finally, add one additional question or risk that wasn’t covered above, based on your editorial instinct.
        Keep it tight (under 150 words). Do **not** rewrite the pitch.
        """)
        st.code(follow_up_prompt, language="markdown")
        st.info("Copy this and paste it into your **existing** AI conversation.")
    
    st.markdown("---")
    
    st.subheader("Option 2: Get a **Full Review** from a **Different** AI")
    transcript = st.text_area("**Paste highlights from your session:**", height=250)
    w, c = get_counter(transcript)
    st.caption(f"Live counter: **{w} words · {c} characters**")
    if st.button("Generate ‘Reviewer’ Prompt"):
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
            2) **What was missed:** List 3 **specific** questions the coach *should* have asked (Socratic, not leading).
            3) **Evidence & verification:** Identify 2 claims/assumptions that need sourcing or a quick check, and say **how** to check them.
            4) **Action plan:** Give the journalist 3 next reporting steps (tight, do-able).
            5) **One risk call-out:** The single biggest failure mode if they proceed as is.
            
            After completing the list above, add one final observation based on your editorial instinct that was not covered.
            
            Constraints: Do **not** rewrite the pitch. Point the human to actions, not prose.
            """)
            st.code(reviewer_prompt, language="markdown")
            st.info("Copy the prompt above and take it to a **different** AI.")
        else:
            st.warning("Please paste a transcript to generate a reviewer prompt.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Self-Reflection")
    st.markdown("- What was the single most useful question the coach asked?\n- Which suggestion did you push back on, and why?\n- What’s your immediate next reporting action?")
    st.markdown('</div>', unsafe_allow_html=True)
    
    colb1, colb2 = st.columns([1,1])
    with colb1:
        if st.button("← Start Another Pitch", use_container_width=True):
            go_to_page("questionnaire"); st.rerun()
    with colb2:
        if st.button("← Back to Portal", use_container_width=True):
            go_to_page("portal"); st.rerun()
