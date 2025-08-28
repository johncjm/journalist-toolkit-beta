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
        "Tools that help you **think like a journalist** by using AI as a coach — not a ghostwriter."
    )
    st.markdown("---")

    st.markdown("#### How It Works")
    st.write(
        "The Toolkit guides you through a simple 3-step loop. You’ll practice a newsroom task (like shaping a story pitch), learn what makes a strong prompt, and then get a second opinion."
    )

    with st.expander("What’s a “prompt recipe”? (one-liner)"):
        st.markdown(
            "**Recipe = your answers + our expert template → a ready-to-use prompt.** "
            "It’s transparent so you can see how strong prompts are built."
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### 1) Choose a Task & Answer Questions")
        st.markdown(
            "Pick a task (e.g., prepare a story pitch). A short questionnaire helps you clarify the core elements — that’s part of the lesson."
        )
    with col2:
        st.markdown("##### 2) Get Your Expert Prompt (the “recipe”)")
        st.markdown(
            "We assemble a clear, structured prompt from your answers. You can study it, tweak it, and reuse it."
        )
    with col3:
        st.markdown("##### 3) Start the Coaching Session")
        st.markdown(
            "Copy the prompt and paste it in your preferred AI chat (Gemini, ChatGPT, Claude). The conversation happens **in a separate tab**."
        )

    with st.expander('Our Core Philosophy: “Coach, not do”'):
        st.markdown(
            "We help you **do the work yourself**. Expect probing questions, verification habits, and concrete next steps — the way a good editor works (minus the grumpiness)."
        )

    st.markdown("---")

    colA, colB = st.columns(2)
    with colA:
        st.header("📝 I’ve Got a Job to Do")
        st.markdown(
            "Use a structured prompt to get reliable, on-task coaching for a newsroom job."
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
            "Try a “Team of Rivals” panel: ChatGPT, Claude, and Gemini in dialogue for open-ended problems (coming soon). Good for:\n"
            "- complex tradeoffs\n- strategy brainstorming\n- troubleshooting\n- ethics scenarios"
        )
        st.link_button("Go to Team of Rivals (ToR)", "about:blank", disabled=True, use_container_width=True)

# =========================
# Page 2: Questionnaire
# =========================
elif st.session_state.page == "questionnaire":
    st.title("Story Pitch Coach")
    st.markdown(
        "Fill this out to sharpen your pitch and give the AI enough context to coach you well."
    )
    st.markdown("---")

    with st.form("pitch_form"):
        pitch_text = st.text_area("**Paste your story pitch here (Required):**", height=200)

        st.subheader("Pitch Details (Optional, but recommended)")
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
        response_mode = "Socratic dialogue"  # Locked for this version
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
                    "pitch_text": pitch_text,
                    "working_headline": working_headline,
                    "key_conflict": key_conflict,
                    "content_type": content_type,
                    "target_audience": target_audience,
                    "sources": sources,
                    "peg": peg,
                    "visuals": visuals,
                    "reporting_stage": reporting_stage,
                    "response_mode": response_mode,
                    "coaching_style": coaching_style,
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
        "AI models do best with **well-structured prompts** that provide: clear context, a defined role and goal, and a crisp output shape. "
        "Below is your assembled recipe (from your answers + our expert template)."
    )

    st.info(
        "**Where to use it**\n\n"
        "Copy the prompt and paste it into **Gemini, Claude, or ChatGPT in a new tab**. "
        "Manual copy-paste keeps things simple and free, and it helps you **see** what makes a strong prompt."
    )
    st.markdown("---")

    data = st.session_state.get("form_data", {})

    context_lines = [
        f"- Story Type: {data.get('content_type', 'N/A')}",
        f"- Target Audience: {data.get('target_audience', 'N/A')}",
        f"- Stage: {data.get('reporting_stage', 'N/A')}",
    ]
    if data.get("working_headline"):
        context_lines.append(f"- Working Headline: \"{data['working_headline']}\"")
    if data.get("key_conflict"):
        context_lines.append(f"- Key Conflict: {data['key_conflict']}")
    if data.get("sources"):
        context_lines.append(f"- Sources: {data['sources']}")
    if data.get("peg"):
        context_lines.append(f"- Time Peg: {data['peg']}")
    if data.get("visuals"):
        context_lines.append(f"- Potential Visuals: {data['visuals']}")
    context_lines.append(f"- User's Pitch: \"{data.get('pitch_text', '').strip()}\"")
    full_context = "\n".join(context_lines)

    final_prompt = textwrap.dedent(f"""
    # 1. INTRODUCTION
    You are an expert journalism mentor. Act as a Socratic coach for a student journalist. Your goal is to help them improve their pitch through a collaborative workshop — **coach, not do**.

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
    """)

    st.subheader("Your Assembled Prompt")
    with st.expander("Show/Hide Full Prompt Recipe"):
        st.code(final_prompt, language="markdown")

    if st.button("Copy Prompt to Clipboard"):
        st.components.v1.html(
            f"""
            <script>
              const text = {final_prompt!r};
              navigator.clipboard.writeText(text);
            </script>
            """,
            height=0,
        )
        st.success("Copied!")

    st.subheader("Tips for Your Coaching Session")
    st.markdown(
        "- **Be an active partner.** Push back, ask for clarifications, and steer.\n"
        "- **Correct misunderstandings.** e.g., “Actually, the key point is X, not Y.”\n"
        "- **Ask for alternatives.** If you dislike a suggestion: “Try that again from a skeptical editor’s view.”"
    )
    with st.expander("Quick example: weak vs strong opening"):
        st.markdown(
            "**Weak:** “Thoughts?”\n\n"
            "**Stronger:** “Acting as a tough but fair editor, what's the single biggest weakness in this pitch that I should fix first?”"
        )

    st.subheader("Start Your Coaching Session (opens a new tab)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with col2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with col3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("---")
    st.markdown("**Don’t skip the follow-up.**")
    st.write(
        "Next you’ll get a **second opinion** — either a new angle from the same AI or a full review from a different AI. "
        "That’s where blind spots surface and the plan gets sharper."
    )

    colx, coly = st.columns([1,1])
    with colx:
        if st.button("Continue to Next Steps →", type="primary", use_container_width=True):
            go_to_page("follow_on")
            st.rerun()
    with coly:
        if st.button("← Start a New Pitch", use_container_width=True):
            go_to_page("questionnaire")
            st.rerun()

# =========================
# Page 4: Workshop Results & Next Steps
# =========================
elif st.session_state.page == "follow_on":
    st.title("Workshop Results & Next Steps")
    st.markdown(
        "Like a newsroom, a **second set of eyes** can reveal new angles and blind spots. Use the tools below to review your session."
    )
    st.markdown("---")

    st.header("Get a Second Set of Eyes on Your Workshop")

    st.subheader("Option 1: Ask the **Same** Coach for a Different Perspective")
    st.markdown(
        "Good when you want continuity but a new lens on the same idea."
    )

    new_persona = st.selectbox(
        "Choose a new coaching style:",
        ["Skeptical Editor", "Audience Advocate", "Tough Desk Editor"],
        key="new_persona_selector",
    )

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
    st.markdown(
        "Great for catching what the first AI missed. If you used Gemini, try Claude; if you used ChatGPT, try Gemini — and so on."
    )

    st.caption("Tip: Highlights (2–4 exchanges) are usually enough. Up to ~800–1,200 words works well.")
    transcript = st.text_area(
        "**Paste highlights (or the full transcript) from your session:**",
        height=250,
        key="transcript_input",
        help="Aim for 2–4 back-and-forths that show the main reasoning. Full transcripts are OK if concise."
    )
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
            st.info(
                "Copy the prompt above and take it to a **different** AI (e.g., if your first session was in Gemini, try Claude)."
            )
        else:
            st.warning("Please paste highlights or a transcript to generate a reviewer prompt.")

    st.markdown("---")

    st.header("Finalize Your Work")
    if st.button("Create a Sharable Google Doc for Review (Simulated Demo)"):
        with st.spinner("Connecting to Google Drive and creating your document..."):
            import time
            time.sleep(3)
        st.success("✅ Success! Your sharable review document has been created.")
        st.link_button(
            "Open Sample Google Doc",
            "https://docs.google.com/document/d/1Yg-vVi85kO3r-2a-sYhZ2gT6tQ_xWJ_c-3kF_eD_B_c/edit?usp=sharing",
        )

    st.markdown("---")

    st.header("Self-Reflection")
    st.markdown(
        "- What was the single most useful question the coach asked?\n"
        "- Which suggestion did you push back on, and why?\n"
        "- What’s your immediate next reporting action?"
    )

    colb1, colb2 = st.columns([1,1])
    with colb1:
        if st.button("← Start Another Pitch", use_container_width=True):
            go_to_page("questionnaire")
            st.rerun()
    with colb2:
        if st.button("← Back to Portal", use_container_width=True):
            go_to_page("portal")
            st.rerun()
