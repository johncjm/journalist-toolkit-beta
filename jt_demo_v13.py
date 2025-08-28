import streamlit as st
import textwrap

# --- App Configuration ---
st.set_page_config(page_title="Journalist's Toolkit", layout="wide")

# --- Helpers ---
def go_to_page(page_name: str):
    st.session_state.page = page_name

def get_counter(text: str):
    words = len(text.split()) if text else 0
    chars = len(text) if text else 0
    return words, chars

# --- State Management ---
if "page" not in st.session_state:
    st.session_state.page = "portal"

# =========================
# Page 1: The Portal
# =========================
if st.session_state.page == "portal":
    st.title("Welcome to the Journalist's Toolkit 🛠️")
    st.subheader(
        "A suite of tools designed to help you think like a journalist and strengthen your work by using AI as a coach."
    )
    st.markdown("---")

    st.markdown("#### How It Works")
    st.write(
        "The toolkit guides you through a simple 3-step process to help you with tasks ranging from shaping a story pitch to polishing copy for publication. Along the way, you'll have a chance to learn about productive ways to work with AI models."
    )

    with st.expander("What’s a “prompt”?"):
        st.markdown(
            "A **prompt** is the request a user makes to an AI, but it's also a set of instructions for how the AI should prepare an answer. **Prompt engineering** is the art of designing those instructions in a way that is most likely to get the best (most accurate, most illuminating) results."
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### 1) Choose a Task & Answer Questions")
        st.markdown(
            "Select a journalistic task, like preparing a story pitch. You'll fill out a short questionnaire that helps you think through the key elements—this is the first part of the lesson."
        )
    with col2:
        st.markdown("##### 2) Get Your Expert Prompt")
        st.markdown(
            "We'll use your answers to build a sophisticated, expert-level prompt. We make the prompt transparent so you can learn the crucial AI literacy skill of effective prompt engineering."
        )
    with col3:
        st.markdown("##### 3) Start the Coaching Session")
        st.markdown(
            "You'll copy the prompt and take it to your preferred AI chat tool (Gemini, ChatGPT, etc.) to begin the collaborative workshop."
        )

    with st.expander('Our Core Philosophy: “Coach, not do”'):
        st.markdown(
            "Our goal is to help you learn how to do the work, not to do it for you. We're hoping to give you the kind of guided coaching you might get from a real editor -- minus the grumpiness -- focused on real newsroom tasks."
        )

    st.markdown("---")

    colA, colB = st.columns(2)
    with colA:
        st.header("📝 I’ve Got a Job to Do")
        st.markdown(
            "Use a structured prompt to get the best and most reliable coaching on a specific newsroom task."
        )

        if st.button("Prepare a story pitch", type="primary", use_container_width=True):
            go_to_page("questionnaire")
            st.rerun()
        st.button("Structure a first draft", disabled=True, use_container_width=True)
        st.button("Vet a source", disabled=True, use_container_width=True)
        st.button("Develop interview questions", disabled=True, use_container_width=True)

    with colB:
        st.header("🤔 I Want to Think Something Through")
        st.markdown(
            """
            Engage with a "Team of Rivals' -- top AI models ChatGPT, Claude and Gemini work together as an expert panel for more open-ended discussions. They can help you:
            - come up with solutions to complex problems
            - explore new strategies
            - troubleshoot code
            - think through ethical dilemmas
            """
        )

# =========================
# Page 2: Questionnaire
# =========================
elif st.session_state.page == "questionnaire":
    st.title("Story Pitch Coach")
    st.markdown(
        "Filling out this questionnaire helps you think through the key elements of your pitch. It also will give the AI model more context to go on."
    )
    st.markdown("---")

    with st.form("pitch_form"):
        pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)

        st.subheader("Pitch Details (Optional, but highly recommended)")
        col1, col2 = st.columns(2)
        with col1:
            working_headline = st.text_input("Working headline (doesn’t need to be polished)")
            key_conflict = st.text_input("What’s the key conflict or most interesting point?")
            content_type = st.selectbox(
                "What kind of story is this?",
                ["News article", "Feature", "Investigation", "Profile", "Opinion", "Explainer", "Other"],
            )
            target_audience = st.selectbox(
                "Who is this for?",
                ["General news readers", "Specialist/Expert audience", "Campus audience", "Other"],
            )

        with col2:
            sources = st.text_area("Sources & resources (note which are contacted)", height=90)
            peg = st.text_input("Is there a time peg or other timeliness?")
            visuals = st.text_input("Any potential visuals?")
            reporting_stage = st.selectbox(
                "How far along are you?",
                ["Just an idea", "Some reporting done", "Drafting in progress"],
            )

        st.subheader("Coaching Preferences")
        coaching_style = st.selectbox(
            "**Choose a coaching style (Optional):**",
            ["Default Story Coach", "Tough Desk Editor", "Audience Advocate", "Skeptic"],
            help="This sets tone only — the coaching method stays Socratic."
        )

        submitted = st.form_submit_button("Generate Prompt Recipe", type="primary")

        if submitted:
            if not pitch_text or not pitch_text.strip():
                st.error("Please paste your story pitch before submitting.")
            else:
                st.session_state.form_data = {
                    "pitch_text": pitch_text, "working_headline": working_headline,
                    "key_conflict": key_conflict, "content_type": content_type,
                    "target_audience": target_audience, "sources": sources,
                    "peg": peg, "visuals": visuals,
                    "reporting_stage": reporting_stage, "coaching_style": coaching_style,
                }
                go_to_page("recipe")
                st.rerun()

    if st.button("← Back to Portal"):
        go_to_page("portal")
        st.rerun()

# =========================
# Page 3: Prompt Recipe
# =========================
elif st.session_state.page == "recipe":
    st.title("Your Custom Prompt Recipe 📝")
    st.markdown(
        "AI models work best when given well-structured prompts that **provide clear context, define a specific role and goal, and outline the desired format for the response.** What's been assembled here combines the specifics from your story pitch questionnaire with elements from prompts optimized for this task."
    )
    st.markdown("---")

    # --- PROMPT DATA ASSEMBLY ---
    data = st.session_state.get("form_data", {})
    context_lines = [
        f"- Story Type: {data.get('content_type', 'N/A')}",
        f"- Target Audience: {data.get('target_audience', 'N/A')}",
        f"- Stage: {data.get('reporting_stage', 'N/A')}",
    ]
    if data.get("working_headline"): context_lines.append(f"- Working Headline: \"{data['working_headline']}\"")
    if data.get("key_conflict"): context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get("sources"): context_lines.append(f"- Sources: {data['sources']}")
    if data.get("peg"): context_lines.append(f"- Time Peg: {data['peg']}")
    if data.get("visuals"): context_lines.append(f"- Potential Visuals: {data['visuals']}")
    context_lines.append(f"- User's Pitch: \"{data.get('pitch_text', '').strip()}\"")
    full_context = "\n".join(context_lines)

    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Act as a Socratic coach for a student journalist. Your goal is to help them improve their pitch through a collaborative workshop — **coach, not do**.

    # 2. CONTEXT
    {full_context}

    # 3. EDITORIAL JUDGMENT FRAMEWORK (Your Internal Engine)
    Before you respond, silently form a preliminary hypothesis about the pitch’s greatest strength and single biggest challenge.
    **Red Flags:** Is the writer more excited about the topic than the story? Does it assume readers will care? Does it conflate “important” with “interesting”?
    **Green Flags:** Is the story clear in one sentence? Does it identify specific people affected? Does it show awareness of counterarguments?

    # 4. CONVERSATIONAL FLOW (Your Task)
    ## Turn 1: The Editorial Reaction
    Choose ONE reaction pattern below (don’t announce which):
    * **Pattern A (Intrigued but need more):** Good hook; unclear angle. Opener: “This could be compelling — the detail about [specific element] pops. I’m not yet seeing the central angle. What’s the one thing that would make a reader stop and pay attention?”
    * **Pattern B (Promising with a clear gap):** Solid pitch; one major flaw. Opener: “There’s a strong story here. The main gap is [gap]. To focus that, my first question is: [one precise question about the gap].”
    * **Pattern C (Skeptical but open):** Topic-y, not a story. Opener: “I’m not seeing a specific angle yet, but I suspect we can find one. What surprised you most when you first thought about this?”

    ## Turn 2–3: Deep Dive
    Reflect the user’s answer (“So the core tension is X...”) and ask 1–2 follow-ups. Do **not** provide suggestions yet.

    ## Turn 4+: Targeted Coaching & the “Choice Point”
    After you understand the pitch, provide one concrete deliverable (e.g., verification checklist). Then, signal completion (“This gives you a solid plan...”) and offer a scoped continuation (“If one piece is still nagging at you, we can probe that.”).

    # 5. CORE CONSTRAINTS (Always Apply)
    - **Guide, Don’t Write:** **Do not** draft headlines or nut grafs.
    - **Method Over Persona:** Keep the Socratic method. The assigned style (“{data.get('coaching_style', 'Default Story Coach')}”) changes tone, not process.
    - **Guardrail:** If asked to write the pitch, decline and steer back to questions.
    """)
    
    # --- UI LAYOUT ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Assembled Prompt")
        prompt_display = st.text_area("Prompt Text", final_prompt, height=400, label_visibility="collapsed")
        
        # This is a more robust clipboard functionality
        st.components.v1.html(f"""
            <script>
            function copyToClipboard() {{
                const textToCopy = {prompt_display!r};
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    const button = document.getElementById('copyBtn');
                    button.innerText = 'Copied!';
                    setTimeout(() => {{ button.innerText = 'Copy Full Prompt'; }}, 2000);
                }});
            }}
            </script>
            <button id="copyBtn" onclick="copyToClipboard()">Copy Full Prompt</button>
            """, height=40)

    with col2:
        st.subheader("Anatomy of the Prompt")
        st.markdown(
            """
            - **1. Introduction:** Sets the AI's **role** (expert mentor) and **goal** (to coach, not write).
            - **2. Context:** Injects the specific details you provided, giving the AI raw material to work with.
            - **3. Editorial Framework:** This is the AI's 'internal engine.' We give it a checklist of red and green flags to model how a real editor thinks.
            - **4. Conversational Flow:** This dictates the **process**, ensuring the conversation is productive and doesn't wander.
            - **5. Core Constraints:** These are the guardrails that handle edge cases and reinforce the primary coaching goal.
            """
        )
        if st.button("I don't need to see the prompt, just copy it"):
             st.components.v1.html(f"""...""", height=0) # Same copy logic as above
             st.success("Copied!")

    st.markdown("---")

    st.subheader("Start Your Coaching Session (opens a new tab)")
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2: st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3: st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.subheader("Tips for Your Coaching Session")
    st.markdown(
        "- **Be an active partner.** Don't hesitate to push back, question assumptions, or ask for clarification.\n"
        "- **Correct misunderstandings.** If the AI misinterprets something, correct it directly. \n"
        "- **Ask for alternatives.** If you don't like a suggestion, ask for a different one."
    )
    with st.expander("Quick example: weak vs strong opening"):
        st.markdown(
            "**Weak:** “Thoughts?”\n\n"
            "**Stronger:** “Acting as a tough but fair editor, what's the single biggest weakness in this pitch that I should fix first?”"
        )
    
    st.markdown("---")

    st.subheader("Come back after you've talked with Coach!")
    st.markdown("To learn more about how to improve your work -- and about how AI works -- come back to this page. You'll be able to continue the discussion with the same AI bot but with it taking on a different perspective, or to get a second opinion on your work -- and an analysis of your interaction with the Coach -- from another AI model.")

    if st.button("Continue to Next Steps →", type="primary"):
        go_to_page("follow_on")
        st.rerun()


# =========================
# Page 4: Workshop Results & Next Steps
# =========================
elif st.session_state.page == "follow_on":
    # This page remains the same as v12 for now
    st.title("Workshop Results & Next Steps")
    st.markdown(
        "Like a newsroom, a **second set of eyes** can reveal new angles and blind spots. Use the tools below to review your session."
    )
    st.markdown("---")

    st.header("Get a Second Set of Eyes on Your Workshop")

    st.subheader("Option 1: Ask the **Same** Coach for a Different Perspective")
    st.markdown("Good when you want continuity but a new lens on the same idea.")

    new_persona = st.selectbox(
        "Choose a new coaching style:",
        ["Skeptical Editor", "Audience Advocate", "Tough Desk Editor"],
        key="new_persona_selector",
    )

    if st.button("Generate ‘New Perspective’ Prompt"):
        follow_up_prompt = textwrap.dedent(f"""...""")
        st.code(follow_up_prompt, language="markdown")
        st.info("Copy this and paste it into your **existing** AI conversation.")

    st.markdown("---")
    
    st.subheader("Option 2: Get a **Full Review** from a **Different** AI")
    st.markdown("Great for catching what the first AI missed.")
    
    transcript = st.text_area(...)
    w, c = get_counter(transcript)
    st.caption(f"Live counter: **{w} words · {c} characters**")

    if st.button("Generate ‘Reviewer’ Prompt"):
        if transcript and transcript.strip():
            reviewer_prompt = textwrap.dedent(f"""...""")
            st.code(reviewer_prompt, language="markdown")
            st.info("Copy the prompt above and take it to a **different** AI.")
        else:
            st.warning("Please paste highlights or a transcript to generate a reviewer prompt.")

    st.markdown("---")
    st.header("Finalize Your Work")
    if st.button("Create a Sharable Google Doc for Review (Simulated Demo)"):
        st.success("✅ Success! Your sharable review document has been created.")
        st.link_button("Open Sample Google Doc", "...")

    st.markdown("---")
    st.header("Self-Reflection")
    st.markdown("...")

    if st.button("← Start Another Pitch"):
        go_to_page("questionnaire")
        st.rerun()
