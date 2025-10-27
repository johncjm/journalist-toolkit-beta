# prepare_interview_prep.py
# Standalone JT module — Prepare for an Interview (coaching recipe + plain-text handoff)
# v0.5.3 — adds Subject field, removes mode caption, adds "Re-center" section, updates Anatomy text

import streamlit as st
import textwrap
import html
import uuid
import re

st.set_page_config(page_title="JT — Prepare for an Interview (TEST)", page_icon="🧭", layout="wide")

# ---------- Helpers ----------

def copy_button_js(text_to_copy: str, button_text: str = "Copy to Clipboard"):
    """Safe copy-to-clipboard with fallback and unique element IDs."""
    unique_key = uuid.uuid4().hex[:8]
    unique_id = f"copy-btn-{unique_key}"
    text_area_id = f"text-area-{unique_key}"
    safe = html.escape(text_to_copy or "", quote=True)
    st.components.v1.html(
        f"""
        <textarea id="{text_area_id}" style="opacity:0;position:absolute;height:0;width:0;">{safe}</textarea>
        <button id="{unique_id}" title="Copy the recipe to your clipboard" onclick="
            const text = document.getElementById('{text_area_id}').value;
            if (!navigator.clipboard) {{
                const ta = document.getElementById('{text_area_id}');
                const prevStyle = ta.getAttribute('style') || '';
                ta.setAttribute('style','position:fixed;left:-9999px;opacity:1;');
                ta.focus(); ta.select();
                try {{ document.execCommand('copy'); }} catch(e) {{}}
                ta.setAttribute('style', prevStyle);
                return;
            }}
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('{unique_id}');
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                setTimeout(() => {{ btn.innerText = originalText; }}, 1500);
            }});
        ">{button_text}</button>
        """,
        height=42,
    )

def dedupe_keep_order(items):
    seen = set()
    out = []
    for s in items:
        s2 = (s or "").strip()
        key = s2.casefold()
        if s2 and key not in seen:
            seen.add(key)
            out.append(s2)
    return out

def infer_time_mode(constraints_text: str) -> str:
    """Infer SHORT vs NORMAL from constraints text. SHORT for ≤10 minutes or informal/hallway cues."""
    t = (constraints_text or "").lower()

    # numeric minutes & ranges (5-10 min, 5–10 mins, 10 min, 10m)
    nums = []
    for a, b in re.findall(r"\b(\d+)\s*(?:-|–|—|to)?\s*(\d+)?\s*(?:min(?:s|\.|ute)?|m)\b", t):
        try:
            nums.append(int(a))
            if b: nums.append(int(b))
        except (ValueError, AttributeError):
            pass

    # hyphenated “10-minute” etc.
    for a in re.findall(r"\b(\d+)\s*[- ]?\s*minute(?:s)?\b", t):
        try:
            nums.append(int(a))
        except ValueError:
            pass

    # comparatives / approximations: under/≤/<=/~10 min
    if re.search(r"\b(under|≤|<=|~|approx(?:\.|imately)?)\s*10\b.*\bmin", t):
        nums.append(10)

    if nums and min(nums) <= 10:
        return "SHORT"

    # spelled-out small numbers (optional)
    words = {"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
    for w, n in words.items():
        if re.search(rf"\b{w}\b.*\bmin", t):
            if n <= 10:
                return "SHORT"

    # quick-hit hints
    hints = [
        "informal","hallway","scrum","gaggle","doorstep","standup","stand-up",
        "before the meeting","after the meeting","quick","q&a","press gaggle",
        "avail","availability","door stop","quick hit","on the way out"
    ]
    if any(h in t for h in hints):
        return "SHORT"

    return "NORMAL"

def lens_modifier(lens: str) -> str:
    if lens == "Skeptical Editor":
        return "Ask what finding would falsify their claim; surface assumptions; avoid leading questions."
    if lens == "Audience Advocate":
        return "Tie each line of inquiry to reader impact and clarity; avoid insider jargon."
    return "Maintain balance, clarity, and verification across all buckets."

def level_note(level: str) -> str:
    if level.startswith("High School"):
        return "Use plain language and add a bit more scaffolding when the reporter seems uncertain."
    if level.startswith("Undergraduate"):
        return "Keep language clear; push for specifics; model verification thinking."
    if level.startswith("Grad"):
        return "Be concise; expect sharper reasoning; push for sourcing rigor."
    return "Be direct and efficient; focus on sequencing, verification, and ethics under constraints."

def ethics_tail(level: str) -> str:
    if level.startswith("High School"):
        return ("Confirm on/off/background before starting, ask before recording, and don’t promise anonymity "
                "without teacher/editor approval.")
    if level.startswith("Undergraduate"):
        return ("Confirm ground rules up front. Don’t grant anonymity casually—note the justification and terms.")
    return ("Be explicit about ground rules and potential harm. If anonymity is requested, document rationale, terms, and approver.")

def display_lens(lens: str) -> str:
    return "News Editor" if lens == "Standard News Editor" else lens

def make_recipe(
    subject: str,
    level: str,
    lens: str,
    aim: str,
    why_person: str,
    musts: list[str],
    pushbacks: str,
    constraints: str,
    recording: str,
    team_up: str | None,
    ethics: str,
):
    musts_clean = dedupe_keep_order(musts)
    mode = infer_time_mode(constraints)
    n_buckets = 2 if mode == "SHORT" else 3

    # Context bullets
    musts_bullets = "\n".join(f"  - {m}" for m in musts_clean if m)
    pushbacks_line = pushbacks.strip() if pushbacks and pushbacks.strip() else "None specified"
    team_line = f"\n- Teaming: {team_up.strip()}" if team_up and team_up.strip() else ""
    ethics_block = ethics.strip() if ethics and ethics.strip() else "No specific sensitivities noted by the reporter."
    ethics_block += f"\n- {ethics_tail(level)}"

    coaching_arc = textwrap.dedent(f"""
    Help the reporter:
    1) Organize their must-learns into **{n_buckets} goal-driven topic buckets** (not a script).
    2) For each bucket, clarify **what success looks like** and **what could verify or falsify it** (doc/record/person).
    3) Anticipate likely **pushback patterns** and agree on a neutral pivot that re-anchors to the bucket goal.
    4) Keep **ethics** visible (consent, recording, anonymity standards, harm minimization). If anonymity is on the table, confirm they'll consult a teacher/editor before promising.
    5) Adapt to the reporter’s needs—if buckets are solid, spend time on evasion & verification; if they’re unsure, scaffold and simplify.
    """).strip()

    # Plain-text Practice Brief handoff
    practice_brief_template = textwrap.dedent(f"""
    PRACTICE BRIEF
    SUBJECT: {subject}
    LEVEL: {level}
    LENS: {lens}
    MODE: {mode}
    FORMAT: <phone | video | in-person>
    TIME: <e.g., 10 minutes>

    STORY AIM (1 LINE):
    <why this matters / what the story needs>

    WHY THIS PERSON (1–2 LINES):
    <role/title and what they uniquely add>

    MUST-LEARNS (3 BULLETS MAX):
    - <item 1>
    - <item 2>
    - <item 3>

    TOPIC BUCKETS (GOAL-DRIVEN, NOT QUESTIONS):
    - Bucket 1 — Goal: <what success looks like>; Verification: <doc/person/record>
    - Bucket 2 — Goal: <…>; Verification: <…>
    {'' if mode=='SHORT' else '- Bucket 3 — Goal: <…>; Verification: <…>'}

    PUSHBACKS (PATTERN → NEUTRAL PIVOT):
    - <pattern 1> → <acknowledge + re-anchor to bucket goal>
    - <pattern 2> → <…>

    ETHICS & CONSENT:
    <any sensitivities, anonymity policy, recording consent>

    PRE-INTERVIEW CHECK:
    - Confirm time/method; backup ready
    - Recording plan and consent
    - Needed docs open
    - Ground rules (on/off/background)
    """).strip()

    # Final re-centering nudge (per Amditis-style guidance)
    recenter = textwrap.dedent("""
    ## 5) RE-CENTER ON THE CORE GOAL
    Before you produce the brief, state—in one sentence—the **most important outcome** the reporter should achieve in this interview (from the audience’s point of view). Keep it visible as a north star while coaching.
    """).strip()

    recipe = textwrap.dedent(f"""
    # PREPARE FOR AN INTERVIEW — Coaching Recipe

    ## 1) ROLE & MISSION
    You are an experienced **{display_lens(lens)}** coaching a **{level}**. {level_note(level)}
    Your job is to guide thinking via Socratic questions. **Do not** write question scripts or numbered lists.

    ## 2) CONTEXT (Reporter’s inputs)
    - Interview subject: {subject.strip()}
    - Story aim: {aim.strip()}
    - Why this person: {why_person.strip()}
    - Must-learns:
    {musts_bullets if musts_bullets else '  - (none provided)'}
    - Expected pushbacks: {pushbacks_line}
    - Constraints: {constraints.strip() if constraints else 'None specified'}
    - Recording plan: {recording.strip() if recording else 'None specified'}{team_line}
    - Ethics:
      {ethics_block}
    - Mode: {mode} → target **{2 if mode=='SHORT' else 3}** topic buckets
    - Lens modifier: {lens_modifier(lens)}

    ## 3) COACHING ARC (descriptive, not prescriptive)
    {coaching_arc}

    ## 4) CORE CONSTRAINTS
    - Coach, don’t do: no question scripts or prose to read aloud.
    - No invented facts, names, or institutions.
    - Probe verification for all factual claims.
    - Keep ethics visible; minimize harm; be clear about ground rules.

    {recenter}

    ---
    ## 6) FINAL STEP — Generate the Practice Brief
    When the coaching is complete, produce a **single plain-text block** using the following format (copy exactly these headings). 
    Keep it under **~350 words**. **No question scripts.** Buckets are **goals**, not pre-written questions.

    {practice_brief_template}
    """).strip()

    return recipe

# ---------- UI ----------

st.caption("🔧 JT experimental module • Prepare for an Interview (local test)")
st.title("Prepare for an Interview 🧭")
st.write("_This prompt combines your notes with structured coaching instructions. **Scroll down** for a copy button and tools to begin a session with an AI model._")

# Global selectors
colA, colB = st.columns([1,1])
with colA:
    level = st.selectbox(
        "Reporter level",
        ["High School journalist", "Undergraduate journalist", "Grad school journalist", "Working journalist"],
        index=0,  # HS default
    )
with colB:
    lens = st.selectbox(
        "Choose the kind of editor you want to talk this over with",
        ["Standard News Editor", "Skeptical Editor", "Audience Advocate"],
        index=0,
    )

st.markdown("---")

with st.form("prep_form"):
    st.subheader("Interview Subject")
    q0_subject = st.text_input(
        "Interview subject — name, position/title, organization",
        placeholder="e.g., Pat Lopez, Lunch Program Coordinator, Central High School"
    )

    st.subheader("Story Context")
    q1_aim = st.text_area(
        "In one sentence, what’s the story aim?",
        placeholder="e.g., Understand why the district changed the lunch policy and how it affects students",
        height=70,
    )
    q2_why = st.text_area(
        "Why do you want or need to interview this person? What could they add to the story?",
        placeholder="e.g., They authored the policy memo and can explain the decision; they know the timeline and constraints",
        height=90,
    )

    st.subheader("What you must learn (3 max)")
    q3_m1 = st.text_input("Must-learn #1", placeholder="e.g., What changed and why")
    q3_m2 = st.text_input("Must-learn #2", placeholder="e.g., The decision timeline and who signed off")
    q3_m3 = st.text_input("Must-learn #3 (optional)", placeholder="e.g., Where documentation lives / who can verify")

    st.subheader("Pushback & Constraints")
    q4_push = st.text_area(
        "Not all interview subjects are cooperative. Do you expect any resistance or pushback? What do you think you might encounter?",
        placeholder="e.g., 'I can’t discuss personnel'; 'That’s taken out of context'; jargon to dodge specifics",
        height=80,
    )
    q5_constraints = st.text_area(
        "Time/format constraints (and how will the interview be recorded?)",
        placeholder="e.g., 10 minutes in hallway after meeting; phone call; Zoom; plan to record on phone + backup",
        height=80,
    )
    team_up = None
    if level.startswith("High School"):
        team_up = st.text_input("(HS) Can you team up with anyone for the interview?", placeholder="e.g., classmate to handle notes/recording")

    st.subheader("Ethics & Consent")
    q6_ethics = st.text_area(
        "Interviews can raise issues like privacy or bias. Is anything especially sensitive about this issue or interview subject? Would granting anonymity be appropriate or not?",
        help="Required. If truly not applicable, enter ‘None’ and explain why.",
        placeholder="e.g., Student privacy concerns; avoid naming minors without consent; clarify on/off/background; no casual anonymity",
        height=100,
    )

    submitted = st.form_submit_button("Generate Coaching Recipe", type="primary")

if submitted:
    errors = []
    if not (q0_subject and q0_subject.strip()):
        errors.append("Please add the interview subject (name, title, organization).")
    if not (q1_aim and q1_aim.strip()):
        errors.append("Please add a one-sentence story aim.")
    if not (q2_why and q2_why.strip()):
        errors.append("Please explain why this person matters to the story.")
    if not any([(q3_m1 or "").strip(), (q3_m2 or "").strip(), (q3_m3 or "").strip()]):
        errors.append("Provide at least one ‘must-learn’.")
    if not (q4_push and q4_push.strip()):
        errors.append("Add at least one expected pushback/resistance pattern.")
    if not (q5_constraints and q5_constraints.strip()):
        errors.append("Add time/format constraints (and recording plan).")
    if not (q6_ethics and q6_ethics.strip()):
        errors.append("Add an ethics note (OK to write ‘None’ if truly N/A).")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    musts = [q3_m1, q3_m2, q3_m3]
    recipe_text = make_recipe(
        subject=q0_subject,
        level=level,
        lens=lens,
        aim=q1_aim,
        why_person=q2_why,
        musts=musts,
        pushbacks=q4_push,
        constraints=q5_constraints,
        recording=q5_constraints,
        team_up=team_up,
        ethics=q6_ethics,
    )

    st.markdown("---")

    # Side-by-side layout: Recipe (left) and Anatomy (right)
    left, right = st.columns([2,1])
    with left:
        st.subheader("Assembled Coaching Prompt")
        st.code(recipe_text, language="markdown")
        copy_button_js(recipe_text, "Copy Recipe to Clipboard")

        st.markdown("#### Start a coaching session (opens a new tab)")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.link_button("ChatGPT", url="https://chat.openai.com/", use_container_width=True, type="secondary")
        with c2:
            st.link_button("Claude", url="https://claude.ai/chats", use_container_width=True, type="secondary")
        with c3:
            st.link_button("Gemini", url="https://gemini.google.com/app", use_container_width=True, type="secondary")
        with c4:
            st.link_button("Other…", url="https://duckduckgo.com/?q=AI+chat", use_container_width=True, type="secondary")

    with right:
        st.subheader("Anatomy of a Good Coaching Prompt")
        st.markdown(
            "1) **Role & mission** — what we're asking the AI model to do — and not do.\n"
            "2) **Context** — we're helping the model be more specific by sharing the information from your questionnaire.\n"
            "3) **Coaching arc** — a suggestion for how the model can move through the various facets of preparation.\n"
            "4) **Constraints** — reminding the model of what it should avoid: no scripts, no invented facts, verification mindset.\n"
            "5) **Handoff** — a short, structured Practice Brief the model produces at the end that can be used by the student or fed into the next stage of the Journalist’s Toolkit."
        )
