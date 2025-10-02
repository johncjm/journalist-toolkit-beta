# v16.0 - Restores full "Story Pitch" tool functionality
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

    Along with the way, you'll gain insight into what AI bots do and don't do well, and how to get the most out of an AI collaboration.
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
        - **5. Final Goal Reminder:** A final, clear instruction that re-centers the AI on its most important task.
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
        st.markdown(
        """
        - **1. Introduction:** This sets the stage. It tells the AI its **role** (expert mentor), its **goal** (to coach, not write), and its **persona** (encouraging but realistic).
        - **2. Context:** Here, we inject all the specific details from your questionnaire. This gives the AI the crucial raw material it needs to provide tailored, relevant feedback.
        - **3. Editorial Framework:** This is the AI's 'internal engine.' We give it a specific analytical model (red/green flags) to use, ensuring a high-quality critique.
        - **4. Conversational Flow:** This section structures the entire conversation. By specifying a turn-by-turn process, we prevent the AI from wandering and ensure the session is productive.
        - **5. Core Constraints:** These are the hard-and-fast rules. They handle edge cases, prevent the AI from doing the work for the user, and ensure the interaction stays on track.
        - **6. The Final Reminder:** After all the details, we restate the main goal. It's like planning a party: after discussing the cake and decorations, you say, 'Okay, but let's remember the whole point is to celebrate the birthday person!'
        """
        )
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
    colb1, col2 = st.columns([1,1])
    with colb1:
        if st.button("← Start Another Pitch", use_container_width=True):
            go_to_page("questionnaire"); st.rerun()
    with colb2:
        if st.button("← Back to Portal", use_container_width=True):
            go_to_page("portal"); st.rerun()
