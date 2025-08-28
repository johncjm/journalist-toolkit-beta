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
    st.markdown("A suite of tools designed to help you think like a journalist and strengthen your work using AI as a Socratic coach.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("📝 I've Got a Job to Do")
        st.markdown("Use a structured 'recipe' to get expert coaching on a specific task.")
        
        if st.button("Prepare a story pitch", type="primary", use_container_width=True):
            go_to_page('questionnaire')
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
        col3, col4 = st.columns(2)
        with col3:
            response_mode = st.radio(
                "**How do you want the coach to respond?**",
                ["Socratic dialogue", "Quick critique"],
                index=0,
                help="Socratic dialogue is a multi-turn conversation to help you think. Quick critique is a direct, one-time analysis."
            )
        with col4:
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

# --- Page 3: The Prompt Recipe ---
elif st.session_state.page == 'recipe':
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown(
        "Below is a prompt that has been expertly crafted based on your questionnaire. This is the 'secret sauce'—"
        "by making the process transparent, we're helping you learn the meta-skill of how to work with AI effectively."
    )
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
    response_mode = data.get('response_mode')
    
    if response_mode == "Socratic dialogue":
        instructions = textwrap.dedent("""
        Structure each of your coaching responses in a two-part rhythm:
        1. **Question:** Begin by asking 1-2 insightful, Socratic questions that prompt the user to reflect on a specific aspect of their pitch.
        2. **Suggestion:** After asking the questions, provide a concise, concrete suggestion or an illustrative example that shows a possible path for improvement.
        """)
    else: # This will catch "Quick critique"
        instructions = textwrap.dedent("""
        Provide a **quick, direct critique**. Immediately provide thoughtful, constructive feedback organized under the following headings:
        - Strengths
        - Weaknesses or Risks
        - Key Question to Consider
        """)

    # --- V5 PROMPT ---
    # This prompt is now structured using the 5-element framework.
    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Your role is to act as a Socratic coach for a student journalist, helping them improve their story pitch through a guided dialogue.

    # 2. CONTEXT
    {full_context}

    # 3. INSTRUCTIONS
    Your coaching style for this session is: **{data.get('coaching_style', 'Default Story Coach')}**.
    {instructions}

    # 4. CONSTRAINTS
    - **Guide, Don't Write:** Your purpose is to help the user improve their own thinking. You may provide illustrative examples or model sentences to clarify a point, but always frame them as possibilities, not as the single correct answer. Do not rewrite the user's work for them.
    - **Method Over Persona:** Your Socratic coaching method (Question-Then-Suggestion) is the primary directive. Your assigned coaching style should only influence the *tone and phrasing* of your response, not the fundamental process.
    - **Focus on the User's Text:** Base all your questions and feedback directly on the pitch and context provided.
    - **Be Concise:** Keep your responses clear and to the point.

    # 5. EMPHASIS
    Your mission has two balanced goals: **Insight and Action**. The primary goal is to make the user **think for themselves** through insightful questioning. The equally important secondary goal is to ensure the user leaves with an **actionable path forward**. Your success is measured by how well you guide the user to their own insights *and* equip them with concrete steps to improve their pitch.
    """)

    st.subheader("1. Your Assembled Prompt")
    st.markdown("Copy the text below and paste it into the AI chat interface of your choice.")
    st.code(final_prompt, language="markdown")
    
    if st.button("Copy Prompt to Clipboard"):
        st.components.v1.html(
            f"""
            <script>
            const text = `{final_prompt.replace("`", "\\`").replace("$", "\\$")}`;
            navigator.clipboard.writeText(text).then(function() {{
                const buttons = window.parent.document.getElementsByTagName('button');
                for (let i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerText.includes("Copy Prompt to Clipboard")) {{
                        buttons[i].innerText = "Copied!";
                        setTimeout(() => {{ buttons[i].innerText = "Copy Prompt to Clipboard"; }}, 2000);
                        break;
                    }}
                }}
            }}, function(err) {{
                console.error('Error copying text: ', err);
            }});
            </script>
            """,
            height=0,
        )

    st.subheader("2. Where to Go")
    st.markdown("For best results, we recommend one of the following consumer-facing AIs:")
    col1, col2, col3 = st.columns(3)
    with col1: st.link_button("Open Google Gemini", "https://gemini.google.com")
    with col2: st.link_button("Open Anthropic's Claude", "https://claude.ai")
    with col3: st.link_button("Open OpenAI's ChatGPT", "https://chat.openai.com")

    st.subheader("3. Tips for Your Conversation")
    st.info(
        "**Be ready to follow up.** The first response is just the beginning.\n\n"
        "**Challenge its assumptions.** If a suggestion feels wrong, tell the AI why and ask for an alternative.\n\n"
        "**Ask for examples.** If the AI gives abstract advice, ask it to 'show me what you mean.'"
    )

    if st.button("← Start a New Pitch"):
        go_to_page('questionnaire')
        st.rerun()
