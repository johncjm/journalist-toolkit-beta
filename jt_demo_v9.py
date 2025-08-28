import streamlit as st
import textwrap

# --- App Configuration ---
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'portal'

def go_to_page(page_name):
    st.session_state.page = page_name

# --- Page 1: The Portal ---
if st.session_state.page == 'portal':
    st.title("Welcome to the Journalist's Toolkit 🛠️")
    # TODO: Add more explanatory text on the JT process here.
    st.markdown("A suite of tools designed to help you think like a journalist and strengthen your work using AI as a Socratic coach.")
    st.markdown("---")
        
    col1, col2 = st.columns(2)

    with col1:
        st.header("📝 I've Got a Job to Do")
        st.markdown("Use a structured 'recipe' to get expert coaching on a specific task.")
        
        if st.button("Prepare a story pitch", type="primary", use_container_width=True):
            go_to_page('questionnaire')
            st.rerun() # FIX: Prevents double-click issue
        st.button("Structure a first draft", disabled=True, use_container_width=True)
        st.button("Vet a source", disabled=True, use_container_width=True)
        st.button("Develop interview questions", disabled=True, use_container_width=True)

    with col2:
        st.header("🤔 I Want to Think Something Through")
        st.markdown(
            "Engage with a 'Team of Rivals'—a panel of AI perspectives—to stress-test complex ideas, "
            "explore ethical dilemmas, or find unexpected angles."
        )
        st.link_button("Go to Team of Rivals (ToR)", "about:blank", disabled=True, use_container_width=True)
        st.info("The Journalist's Toolkit (JT) helps you with specific tasks, while Team of Rivals (ToR) is for open-ended strategic brainstorming.")

# --- Page 2: The Questionnaire ---
elif st.session_state.page == 'questionnaire':
    st.title("Story Pitch Coach")
    st.markdown("This questionnaire helps you think through the key elements of your pitch. The more context you provide, the better the coaching will be.")
    st.markdown("---")

    with st.form("pitch_form"):
        pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)

        st.subheader("Pitch Details (Optional, but highly recommended)")
        col1, col2 = st.columns(2)
        with col1:
            working_headline = st.text_input("Working headline (doesn't need to be polished)")
            key_conflict = st.text_input("What is the key conflict or point of greatest interest?")
            content_type = st.selectbox("What kind of story is this?", ["News article", "Feature", "Investigation", "Profile", "Opinion", "Explainer", "Other"])
            target_audience = st.selectbox("Who is this for?", ["General news readers", "Specialist/Expert audience", "Campus audience", "Other"])
            
        with col2:
            sources = st.text_area("Sources & resources (which have been contacted?)", height=90)
            peg = st.text_input("Is there a peg or other time-relevant element?")
            visuals = st.text_input("Any potential visuals for the piece?")
            reporting_stage = st.selectbox("How far along are you?", ["Just an idea", "Some reporting done", "Drafting in progress"])

        st.subheader("Coaching Preferences")
        response_mode = "Socratic dialogue" # Locked for this version to test the V9 logic
        coaching_style = st.selectbox(
            "**Choose a coaching style (Optional):**",
            ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
            help="Select a specific persona for the AI to adopt for its feedback."
        )

        submitted = st.form_submit_button("Generate Prompt Recipe", type="primary")

        if submitted:
            if not pitch_text:
                st.error("Please paste your story pitch before submitting.")
            else:
                st.session_state.form_data = {
                    "pitch_text": pitch_text, "working_headline": working_headline, "key_conflict": key_conflict,
                    "content_type": content_type, "target_audience": target_audience, "sources": sources,
                    "peg": peg, "visuals": visuals, "reporting_stage": reporting_stage,
                    "response_mode": response_mode, "coaching_style": coaching_style
                }
                go_to_page('recipe')
                st.rerun()

    if st.button("← Back to Portal"):
        go_to_page('portal')
        st.rerun()

# --- Page 3: The Prompt Recipe ---
elif st.session_state.page == 'recipe':
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown("This prompt contains our final V9 'Choice Point' logic. Copy the text below to test it with your preferred AI.")
    st.markdown("---")

    data = st.session_state.get('form_data', {})

    context_lines = [
        f"- Story Type: {data.get('content_type', 'N/A')}",
        f"- Target Audience: {data.get('target_audience', 'N/A')}",
        f"- Stage: {data.get('reporting_stage', 'N/A')}",
    ]
    if data.get('working_headline'): context_lines.append(f"- Working Headline: \"{data['working_headline']}\"")
    if data.get('key_conflict'): context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get('sources'): context_lines.append(f"- Sources: {data['sources']}")
    if data.get('peg'): context_lines.append(f"- Time Peg: {data['peg']}")
    if data.get('visuals'): context_lines.append(f"- Potential Visuals: {data['visuals']}")
    context_lines.append(f"- User's Pitch: \"{data.get('pitch_text', '').strip()}\"")
    
    full_context = "\n".join(context_lines)
    
    # --- V9 PROMPT with "Choice Point" logic ---
    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Your role is to act as a Socratic coach for a student journalist. Your goal is to help them improve their pitch through a collaborative workshop, not to do the work for them.

    # 2. CONTEXT
    {full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK (Your Internal Engine)
    Before you respond, silently use this framework to form a preliminary hypothesis about the pitch's greatest strength and single biggest challenge.

    **Red Flags to look for:**
    - The writer is more excited about the topic than the story.
    - It assumes readers will care without explaining why.
    - It conflates "important" with "interesting."
    - It has done research but hasn't found the core tension/conflict.

    **Green Flags to look for:**
    - It can explain the story in one clear sentence.
    - It identifies specific people affected in specific ways.
    - It shows awareness of potential counterarguments.
    - It has a plausible reporting plan.

    # 4. CONVERSATIONAL FLOW (Your Task)

    ## Turn 1: The Editorial Reaction
    Based on your internal assessment, you MUST choose ONE of the three reaction patterns below for your first response. Choose the pattern that best matches, but **do not announce which pattern you are using.**

    * **Pattern A: Intrigued but need more...** (Use for pitches with a good hook but an unclear angle or purpose).
        * **Example:** "This feels like it could be compelling—I can see why the detail about [specific element from their pitch] caught your attention. But I'm not quite grasping your central angle yet. What's the one thing about this story that would make someone stop scrolling and pay attention?"

    * **Pattern B: Promising with a clear gap...** (Use for solid pitches with one significant, identifiable flaw).
        * **Example:** "There's definitely a strong story here, and your sourcing plan is solid. The main gap that jumped out at me immediately is the lack of a clear time peg. To focus on that, my first question is: [ask one Socratic question aimed directly at the identified flaw]."

    * **Pattern C: Skeptical but open...** (Use for pitches that feel more like a broad topic than a focused story).
        * **Example:** "I'm having trouble seeing the specific story angle here, but I suspect there's one we can find together. To help me see what you're seeing, can you [ask one broad, curiosity-driven question about what motivated the user or what they found most surprising]?"

    ## Turn 2-3: Deep Dive
    After the user responds to your opener, your goal is to probe deeper.
    - Reflect back what you heard in one sentence (e.g., "Okay, so you're saying the core tension is X...").
    - Ask 1-2 follow-up questions that push deeper on the core issue.
    - Do not provide concrete suggestions yet.

    ## Turn 4+: Targeted Coaching & The "Choice Point"
    After you have a clear understanding of the user's thinking from the Deep Dive, you can shift to providing a final, concrete deliverable (e.g., a verification checklist, next reporting steps). You must then conclude the conversation using the "Choice Point" model:
    1.  **Provide the deliverable.**
    2.  **Signal completion** with a phrase that gives the user permission to exit. Example: "This gives you a solid plan to move forward with your reporting."
    3.  **Offer a scoped continuation.** Frame an optional final question that is limited in scope. Example: "If there's a particular aspect of this that's still nagging at you, we can dig in. Otherwise, you've got what you need."

    # 5. CORE CONSTRAINTS (Always Apply)
    - **Failure Mode Handling:** If the user's response suggests you chose the wrong reaction pattern, acknowledge this directly. Example: "Actually, based on what you're telling me, I think I misread your pitch initially. Let me refocus on..."
    - **Guide, Don't Write:** You may provide short, illustrative examples, but always frame them as possibilities. Do not draft headlines or nut grafs.
    - **Method Over Persona:** Your Socratic coaching method is the primary directive. Your assigned coaching style (**{data.get('coaching_style', 'Default Story Coach')}**) should only influence your *tone*, not the core process.
    - **Political Hygiene:** If the pitch includes claims about data or political impact, your first step is to ask for the source and then suggest a way the user could independently verify it.
    """)

    st.subheader("Your Assembled V9 Prompt")
    st.code(final_prompt, language="markdown")
    
    if st.button("Copy Prompt to Clipboard"):
        # This approach uses a hidden textarea and JavaScript to copy text, which is more reliable in Streamlit.
        st.components.v1.html(
            f"""
            <textarea id="prompt-text" style="opacity: 0; position: absolute; height: 0px; width: 0px;">{final_prompt}</textarea>
            <script>
                const textToCopy = document.getElementById('prompt-text').value;
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    const buttons = window.parent.document.getElementsByTagName('button');
                    for (let button of buttons) {{
                        if (button.innerText.includes("Copy Prompt to Clipboard")) {{
                            button.innerText = "Copied!";
                            setTimeout(() => {{ button.innerText = "Copy Prompt to Clipboard"; }}, 2000);
                            break;
                        }}
                    }}
                }});
            </script>
            """, height=0
        )

    st.subheader("Where to Go")
    col1, col2, col3 = st.columns(3)
    with col1: st.link_button("Open Google Gemini", "https://gemini.google.com")
    with col2: st.link_button("Open Anthropic's Claude", "https://claude.ai")
    with col3: st.link_button("Open OpenAI's ChatGPT", "https://chat.openai.com")

    if st.button("← Start a New Pitch"):
        go_to_page('questionnaire')
        st.rerun()
