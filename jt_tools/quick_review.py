# jt_tools/quick_review.py
# Quick Review / Second Set of Eyes — final scan before publication
# v1.0

import streamlit as st
import textwrap
import html
import uuid


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def copy_button_js(text_to_copy: str, button_text: str = "Copy to Clipboard"):
    """Safe copy-to-clipboard: escapes content and uses unique IDs each call."""
    unique_key = uuid.uuid4().hex[:8]
    unique_id = f"copy-btn-{unique_key}"
    text_area_id = f"text-area-{unique_key}"
    safe = html.escape(text_to_copy or "", quote=True)
    st.components.v1.html(
        f"""
        <textarea id="{text_area_id}" style="opacity:0;position:absolute;height:0;width:0;">{safe}</textarea>
        <button id="{unique_id}" onclick="
            const text = document.getElementById('{text_area_id}').value;
            if (!navigator.clipboard) {{ return; }}
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('{unique_id}');
                const original = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {{ btn.innerText = original; }}, 1500);
            }});
        ">{button_text}</button>
        """,
        height=40,
    )


def render_quick_review():
    """Main entry point for Quick Review module. Handles internal page routing."""
    
    # Initialize module-specific state
    if "quick_review_page" not in st.session_state:
        st.session_state.quick_review_page = "questionnaire"
    
    if st.session_state.quick_review_page == "questionnaire":
        _render_questionnaire()
    elif st.session_state.quick_review_page == "recipe":
        _render_recipe()
    else:
        st.session_state.quick_review_page = "questionnaire"
        st.rerun()


def _render_questionnaire():
    """Quick Review questionnaire — 5 questions, minimal friction."""
    
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    
    st.title("Quick Review 👀")
    st.markdown("*A smart friend reading your draft in the hallway before you hit submit.*")
    st.markdown("---")
    
    # Experience level selector
    level = st.radio(
        "Your experience level (affects tone):",
        ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"],
        index=["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"]
            .index(st.session_state.get("journalism_level", "High School journalist")),
        horizontal=True,
        key="qr_level_selector"
    )
    st.session_state.journalism_level = level
    
    st.markdown("---")
    st.markdown("### Five quick questions, then you'll get a prompt for your review.")
    st.markdown("")
    
    with st.form("quick_review_form"):
        with st.container(border=True):
            # Question 1: The draft
            q1_draft = st.text_area(
                "**1. Paste your draft here:**",
                height=300,
                help="Include headline if you have one."
            )
            
            st.markdown("---")
            
            # Question 2: Publication
            q2_publication = st.text_input(
                "**2. What publication is this for?**",
                placeholder="e.g., school paper, class assignment, local news site"
            )
            
            st.markdown("---")
            
            # Question 3: What's the story
            q3_story_purpose = st.text_area(
                "**3. In one sentence: what is this story about and why does it matter?**",
                height=80,
                help="This helps check if your headline and lede deliver on your intent."
            )
            
            st.markdown("---")
            
            # Question 4: Blindside check
            q4_criticized = st.text_area(
                "**4. Is there anyone in this story who might feel criticized or exposed?**",
                height=80,
                help="Think about anyone quoted, named, or affected by the story's subject."
            )
            
            st.markdown("---")
            
            # Question 5: Biggest worry
            q5_unsure = st.text_area(
                "**5. What's the one thing you're most unsure about?**",
                height=80,
                help="Could be a fact, a quote, the structure, the headline—anything."
            )
        
        submitted = st.form_submit_button("Generate Quick Review Prompt", type="primary", use_container_width=True)
        
        if submitted:
            if not q1_draft or not q1_draft.strip():
                st.error("Please paste your draft before continuing.")
            elif not q3_story_purpose or not q3_story_purpose.strip():
                st.error("Please describe what your story is about (Question 3).")
            else:
                st.session_state.qr_form_data = dict(
                    draft=q1_draft.strip(),
                    publication=q2_publication.strip() if q2_publication else "Not specified",
                    story_purpose=q3_story_purpose.strip(),
                    criticized=q4_criticized.strip() if q4_criticized else "None identified",
                    unsure=q5_unsure.strip() if q5_unsure else "Nothing specific",
                )
                st.session_state.quick_review_page = "recipe"
                st.rerun()
    
    st.markdown("---")
    if st.button("← Back to Portal"):
        st.session_state.quick_review_page = "questionnaire"  # Reset for next time
        go_to("portal")


def _render_recipe():
    """Quick Review recipe page — the prompt for substantive flags."""
    
    st.components.v1.html("""<script>window.scrollTo(0,0);</script>""", height=0)
    
    st.title("Your Quick Review Prompt 👀")
    st.markdown("Copy this into your preferred AI chat for a fast, final-pass review.")
    st.markdown("---")
    
    data = st.session_state.get("qr_form_data", {})
    level = st.session_state.get("journalism_level", "High School journalist")
    
    if not data:
        st.warning("No draft found. Please go back and complete the questionnaire.")
        if st.button("← Back to Questionnaire"):
            st.session_state.quick_review_page = "questionnaire"
            st.rerun()
        return
    
    # Build the prompt
    final_prompt = textwrap.dedent(f"""
# QUICK REVIEW: Final Scan Before Publication

## 1. YOUR ROLE
You are a smart, experienced friend doing a quick read of a student journalist's draft before they publish. You are NOT a developmental editor—this is a final check, not a revision session. Think: hallway read, ten minutes, catch the things that would be embarrassing to miss.

Calibrate your tone for a **{level}**. Be warm but direct.

## 2. THE DRAFT AND CONTEXT

**Publication:** {data.get('publication', 'Not specified')}

**The student says this story is about:** {data.get('story_purpose', 'Not provided')}

**People who might feel criticized or exposed:** {data.get('criticized', 'None identified')}

**What the student is most unsure about:** {data.get('unsure', 'Nothing specific')}

**THE DRAFT:**
---
{data.get('draft', '[No draft provided]')}
---

## 3. YOUR TASK

Do a quick scan for these four things only:

### A. Hed/Lede Alignment
Does the headline promise what the lede delivers? Does the lede promise what the story delivers? If there's a mismatch, flag it briefly.

### B. Blindside Check
Scan the draft yourself—regardless of what the student said in their answer. Is there anyone quoted, named, or implicated who might feel the story is unfair or inaccurate? Did they appear to get a chance to respond? Flag any gaps.

### C. Obvious Factual Soft Spots
Any claims that seem unsupported? Numbers that appear from nowhere? Quotes without clear attribution? Don't do a full fact-check—just flag anything that looks thin.

### D. Copyediting Patterns
Note any recurring mechanical issues (comma splices, passive voice, attribution style, etc.). Name the pattern; do NOT itemize every instance.

## 4. HOW TO RESPOND

**Lead with one thing that works.** A single, specific, genuine compliment about the draft. (If the draft has serious problems, acknowledge the effort instead: "You've done real reporting here.")

**Then give your flags.** Each flag is 1–2 sentences max. Be brief.

**Offer dialogue only if something is seriously wrong.** If the lede actively misleads about the story's content, or there's a fairness issue that could prompt a correction—offer a short exchange (2–3 turns max). For everything else, just flag and move on.

**Circuit breaker:** If the draft has fundamental problems (no clear story, major structural issues, serious sourcing gaps), say so briefly and suggest they take it back to their editor or advisor before a final review. Do NOT attempt a developmental edit.

**End with ownership.** After your flags, say: "Here's what I noticed. You decide what matters. Ready to publish, or want to look at any of these?"

Then offer: "Would you like a detailed copyedit list before you go? I can flag specific spelling, grammar, punctuation, and style errors for you to fix. (I won't fix them for you.)"

## 5. WHAT YOU MUST NOT DO

- Do NOT rewrite any text. Do not suggest reworded sentences.
- Do NOT suggest structural reorganization or moving paragraphs.
- Do NOT itemize every grammar error in the main review.
- Do NOT open a fact-checking deep-dive.
- Do NOT turn this into a developmental edit.
- If the student asks you to rewrite something, decline and suggest they use a revision-focused tool or talk to their editor.

## 6. IF THEY REQUEST THE DETAILED COPYEDIT LIST

If the student says yes to the copyedit offer:

- Ask: "What style guide should I use? (AP is standard for most news writing.)"
- Produce a numbered list of specific mechanical errors (spelling, punctuation, grammar, style).
- Format: "[Quoted phrase or sentence] — [Issue, e.g., 'comma splice,' 'AP style uses numerals for ages']"
- Do NOT provide corrections—just identify the errors.
- Cap the list at 15–20 items. If there are more, say: "I found additional issues of the same types. You'll catch them once you see the pattern."
- Do NOT editorialize or prioritize. Just list.
    """).strip()
    
    # Display
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("Your Assembled Prompt")
        st.text_area("Prompt Text", final_prompt, height=500, label_visibility="collapsed")
        copy_button_js(final_prompt, "Copy Full Prompt")
    
    with col_side:
        with st.container(border=True):
            st.markdown("## What This Does")
            st.markdown(
                "This prompt asks an AI to do a **fast, final-pass review** of your draft—"
                "the kind of quick read a friend or editor might do right before you publish."
            )
            st.markdown("---")
            st.markdown(
                """
**It checks for:**

1. **Hed/Lede match** — Does your headline deliver on its promise?

2. **Blindside risks** — Anyone who might feel unfairly treated?

3. **Soft spots** — Claims or numbers that look unsupported?

4. **Patterns** — Recurring copyediting issues worth a read-through.

**It does NOT:**

- Rewrite your sentences
- Reorganize your structure
- Do deep fact-checking
- Replace your editor's judgment
                """
            )
    
    st.markdown("---")
    st.markdown("**💡 Tip:** Paste this into any AI chat tool.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("Open Google Gemini", "https://gemini.google.com", use_container_width=True)
    with c2:
        st.link_button("Open Anthropic Claude", "https://claude.ai", use_container_width=True)
    with c3:
        st.link_button("Open OpenAI ChatGPT", "https://chat.openai.com", use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Questionnaire", use_container_width=True):
            st.session_state.quick_review_page = "questionnaire"
            st.rerun()
    with col2:
        if st.button("← Back to Portal", use_container_width=True):
            st.session_state.quick_review_page = "questionnaire"  # Reset for next time
            go_to("portal")
