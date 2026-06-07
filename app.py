import streamlit as st
from groq import Groq
from multi_fetch import fetch_all_sources

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ZotoBibliotherapy",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme: Warm Parchment & Sage ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Top Streamlit Header */

header[data-testid="stHeader"] {
    background: #2e4a3e !important;
    border-bottom: 1px solid #c9a84c !important;
}

/* Toolbar Area */

[data-testid="stToolbar"] {
    background: #2e4a3e !important;
}

/* Main app top area */

[data-testid="stAppViewContainer"] > .main {
    background: #f8f6f1 !important;
}


/* ── Base ── */
html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    color: #2c2416;
    background: linear-gradient(
        180deg,
        #f8fafc 0%,
        #f1f5f9 100%
    ) !important;
}

.main {
    background: transparent !important;
    min-height: 100vh;
}

.main .block-container {
    background: transparent !important;
}

.main .block-container {
    padding-top: 0;
    padding-bottom: 5rem;
    max-width: 980px;
    background: transparent;
}

/* ── Header banner ── */
.zoto-header {
 background: linear-gradient(
     135deg,
     #2e4a3e 0%,
     #476b5b 100%
 );
    margin: -1rem -1rem 2.5rem -1rem;
    padding: 2.8rem 3rem 2.2rem;
    border-bottom: 3px solid #c9a84c;
}
.zoto-header h1 {
    font-family: 'Lora', serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: #f5f0e8;
    letter-spacing: -0.3px;
    margin: 0 0 0.35rem 0;
}
.zoto-header .tagline {
    font-size: 0.92rem;
    color: #9ec4b0;
    font-weight: 400;
    letter-spacing: 0.04em;
    margin: 0;
}
.zoto-header .header-badge {
    display: inline-block;
    background: rgba(201,168,76,0.2);
    border: 1px solid rgba(201,168,76,0.4);
    color: #c9a84c;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #f0ece4;
    border-right: 1px solid #d8d0c0;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.8rem;
}

.sidebar-title {
    font-family: 'Lora', serif;
    font-size: 0.95rem;
    color: #2e4a3e;
    font-weight: 600;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #c9a84c;
    letter-spacing: 0.02em;
}
.sidebar-section {
    font-size: 0.7rem;
    font-weight: 600;
    color: #8a7c6a;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 1.4rem 0 0.5rem 0;
}

/* ── Labels ── */
label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #6b5d4e !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 7px !important;
    border: 1.5px solid #c8bfaf !important;
    background-color: #ffffff !important;
    color: #2c2416 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #2e4a3e !important;
    box-shadow: 0 0 0 3px rgba(46,74,62,0.1) !important;
}

.stSelectbox > div > div {
    border-radius: 7px !important;
    border: 1.5px solid #c8bfaf !important;
    background-color: #ffffff !important;
    color: #2c2416 !important;
}
.stSelectbox svg { fill: #2e4a3e !important; }

.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid #c8bfaf !important;
    background-color: #ffffff !important;
    font-family: 'Lora', serif !important;
    font-size: 1.05rem !important;
    line-height: 1.85 !important;
    color: #2c2416 !important;
    transition: border-color 0.15s !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #2e4a3e !important;
    box-shadow: 0 0 0 3px rgba(46,74,62,0.1) !important;
}

/* ── Button ── */
.stButton > button {
    background: #2e4a3e !important;
    color: #f5f0e8 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    width: 100%;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover {
    background: #1e3329 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Sentence label row ── */
.sentence-label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.4rem;
}
.sentence-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: #2c2416;
}
.target-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #e8f0ec;
    border: 1px solid #a8c4b4;
    color: #2e4a3e;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}

/* ── Result section header ── */
.result-section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #e0d8cc;
}
.result-section-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}
.result-section-title {
    font-family: 'Lora', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #2c2416;
    margin: 0;
}
.result-section-subtitle {
    font-size: 0.8rem;
    color: #8a7c6a;
    margin: 0;
    font-weight: 400;
}

/* ── Box cards ── */
.box-card {
 background: rgba(255,255,255,0.92);
 backdrop-filter: blur(12px);
 border-radius: 18px;
 border: 1px solid rgba(255,255,255,0.6);
 box-shadow:
     0 8px 24px rgba(0,0,0,0.05),
     0 2px 8px rgba(0,0,0,0.03);
    border: 1px solid #e0d8cc;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.box-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #f0ece4;
}
.box-card-accent {
    width: 4px;
    border-radius: 2px;
    height: 22px;
    flex-shrink: 0;
}
.box-card-title {
    font-family: 'Lora', serif;
    font-size: 0.97rem;
    font-weight: 600;
    color: #2c2416;
    margin: 0;
}
.focus-pill {
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 9px;
    border-radius: 20px;
    margin-left: auto;
}

/* ── Suggestion item ── */
.suggestion-item {
 background: #ffffff;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    margin: 0 0 8px 0;
    border-left: 3px solid transparent;
}
/* Box card now acts as the outer container; suggestions sit directly below */
.box-card + .suggestion-item {
    margin-top: 0;
}
.suggestion-number {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    color: #8a7c6a;
}
.suggestion-text {
    font-size: 0.9rem;
    color: #2c2416;
    line-height: 1.7;
}

/* ── Example sentence block ── */
.example-block {
    margin-top: 0.7rem;
    border-top: 2px solid #d94040;
    padding-top: 0.6rem;
}
.example-warning {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #d94040;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 4px;
}
.example-sentence {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 0.95rem;
    color: #3a2e22;
    line-height: 1.8;
    padding: 0.55rem 0.9rem;
    background: #fff5f5;
    border-radius: 6px;
    margin-bottom: 0.4rem;
}
.example-label-sm {
    font-size: 0.68rem;
    color: #b36060;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 3px;
}

/* ── Final sentence ── */
.final-sentence-wrapper {
    background: #2e4a3e;
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin: 1.2rem 0;
}
.final-sentence-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ec4b0;
    margin-bottom: 0.6rem;
}
.final-sentence-text {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: #f5f0e8;
    line-height: 1.85;
}

/* ── Fallback / warning box ── */
.info-box {
    background: #e8f0ec;
    border: 1px solid #a8c4b4;
    border-left: 4px solid #2e4a3e;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    color: #2e4a3e;
    line-height: 1.6;
    margin: 0.8rem 0 1.4rem 0;
}
.warn-box {
    background: #fef9ec;
    border: 1px solid #e8d89a;
    border-left: 4px solid #c9a84c;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.83rem;
    color: #6b5518;
    margin: 1.4rem 0 0.5rem 0;
    line-height: 1.6;
}

/* ── Paper cards ── */
.paper-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    border: 1px solid #e0d8cc;
}
.paper-source {
    font-size: 0.7rem;
    font-weight: 700;
    color: #2e4a3e;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.paper-abstract {
    font-size: 0.87rem;
    color: #5a4e40;
    line-height: 1.7;
}

/* ── Divider ── */
hr { border-color: #e0d8cc !important; }

/* ── Slider ── */
.stSlider > div > div > div > div { background: #2e4a3e !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f0ece4;
    padding: 4px;
    border-radius: 10px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: #6b5d4e !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.1rem !important;
    border: none !important;
    font-size: 0.88rem !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #2e4a3e !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# ── API Client ────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# ── Condition profiles ────────────────────────────────────────────────────────
CONDITION_PROFILES = {
    "autism": {
        "reading_challenges": "literal language processing, difficulty inferring implied emotions or intentions, sensitivity to ambiguous pronouns, preference for explicit and predictable narrative structure",
        "quantity_focus": "avoid pronouns that require inference (e.g. 'he', 'it') — use character names explicitly; avoid implied causality — state it directly; prefer short declarative sentences with one idea each",
        "quality_focus": "use concrete sensory details over abstract emotional language; avoid idioms and figurative speech; name emotions explicitly rather than implying them; use consistent and predictable narrative patterns",
        "example_contrast": "AVOID: 'He felt sad inside.' USE: 'The fish was not happy. He could not find his friend.'",
    },
    "adhd": {
        "reading_challenges": "short attention span, difficulty tracking long or multi-clause sentences, easily distracted by unnecessary words, benefits from high-action and immediately engaging openings",
        "quantity_focus": "split multi-clause sentences aggressively; front-load the action or subject — never bury it in a 'because' clause; cut filler words like 'very', 'really', 'away'; aim for under 8 words per sentence",
        "quality_focus": "use high-energy verbs instead of adverbs (darted, zoomed, searched vs. swam very far); create immediate narrative tension; use rhythm and repetition to hold attention; make every word earn its place",
        "example_contrast": "AVOID: 'The little fish swam very far away because he wanted to find his best friend.' USE: 'The fish darted away. Where was his friend?'",
    },
    "dyslexia": {
        "reading_challenges": "phonological decoding difficulty, slow word recognition, high cognitive load from long or complex words, benefits from high-frequency and phonetically regular vocabulary",
        "quantity_focus": "replace multi-syllable words with shorter equivalents (e.g. 'wanted' → 'tried', 'because' → 'to'); break sentences at natural breath pauses; avoid words with complex spelling patterns",
        "quality_focus": "choose words that are phonetically predictable and high-frequency; use alliteration sparingly to aid memory; short concrete nouns and strong single-syllable verbs; avoid homophones and visually similar words",
        "example_contrast": "AVOID: 'because he wanted to find'. USE: 'to find' — removing 'because he wanted' reduces decoding load without losing meaning",
    },
    "anxiety": {
        "reading_challenges": "hyper-sensitivity to threatening or ambiguous language, may catastrophise open-ended narrative tension, benefits from emotionally safe and resolution-oriented language",
        "quantity_focus": "avoid cliff-hanger sentence structure; keep cause and effect close together so the child does not linger on a negative state; shorter sentences reduce the time spent in emotional uncertainty",
        "quality_focus": "pair any negative emotion with an immediate signal of safety or agency; use warm and reassuring vocabulary; avoid words like 'lost', 'alone', 'far away' without quick resolution language nearby",
        "example_contrast": "AVOID: '...swam very far away' (open-ended loss). USE: 'The fish swam away — and soon he heard a friendly voice.' — resolution is immediate",
    },
    "sensory processing disorder": {
        "reading_challenges": "may be overwhelmed by overly complex or stimulating text; benefits from grounded, sensory-concrete language; rhythm and texture of language matters as much as meaning",
        "quantity_focus": "use shorter sentences with clear rhythmic beats; avoid stacking multiple sensory ideas in one sentence; one sensory anchor per sentence works better than many",
        "quality_focus": "ground the narrative in specific physical sensations (cool water, soft fins, quiet bubbles); avoid abstract relational words; concrete and tactile language creates a calming, accessible reading experience",
        "example_contrast": "AVOID: 'swam very far away because he wanted'. USE: 'The little fish pushed through the cool, still water. He looked for his friend.'",
    },
    "slow learner": {
        "reading_challenges": "slower processing speed, difficulty with multi-step causal reasoning, benefits from repetition and familiar sentence patterns, needs explicit and simple vocabulary",
        "quantity_focus": "use the simplest possible sentence structure (subject + verb + object); split causal chains into separate sentences; repeat key nouns rather than using pronouns",
        "quality_focus": "use highly familiar, high-frequency vocabulary; rely on concrete and visual imagery; repeat sentence patterns to build predictability; avoid figurative language entirely",
        "example_contrast": "AVOID: 'swam very far away because he wanted to find'. USE: 'The fish swam far. The fish wanted his friend. He looked and looked.'",
    },
    "dysgraphia": {
        "reading_challenges": "dysgraphia primarily affects writing production, but co-occurs with reading fatigue and attention difficulties; benefits from shorter reading chunks that do not overwhelm a child already fatigued from writing tasks",
        "quantity_focus": "keep sentences very short to reduce cognitive load for children who also struggle with output; clear sentence boundaries help the child track place on the page",
        "quality_focus": "use vivid, memorable images so fewer words carry more meaning; strong visual anchors reduce re-reading; simple but striking word choices are easier to retain",
        "example_contrast": "AVOID: long multi-clause sentences. USE: short punchy sentences with one strong image each — the child can hold the image without re-reading",
    },
}

def get_condition_profile(condition: str) -> dict:
    key = condition.lower().strip()
    if key in CONDITION_PROFILES:
        return CONDITION_PROFILES[key]
    return {
        "reading_challenges": f"reading and comprehension challenges specific to {condition}",
        "quantity_focus": f"use simple sentence structures and limit word count appropriate for a child with {condition}",
        "quality_focus": f"use clear, concrete, and emotionally accessible language appropriate for a child with {condition}",
        "example_contrast": f"Adapt vocabulary and sentence complexity specifically to the known challenges of {condition}.",
    }

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="zoto-header">
    <div class="header-badge">Evidence-Based Tool</div>
    <h1>ZotoBibliotherapy</h1>
    <p class="tagline">Research-backed writing guidance for children's story authors</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">Story Parameters</div>', unsafe_allow_html=True)

    condition = st.selectbox(
        "Condition",
        ["autism", "ADHD", "dyslexia", "anxiety", "sensory processing disorder", "slow learner", "dysgraphia"],
        index=0
    )
    custom_condition = st.text_input("Or enter a custom condition", placeholder="e.g., selective mutism")
    if custom_condition.strip():
        condition = custom_condition.strip()

    age = st.slider("Child's Age", min_value=3, max_value=12, value=5, step=1)
    age_group = "preschool" if age < 7 else "school-age"

    st.markdown('<div class="sidebar-section">Research Settings</div>', unsafe_allow_html=True)
    num_papers = st.slider("Papers to fetch", min_value=5, max_value=10, value=7)

    st.markdown("---")
    st.markdown(
        f'<div style="background:#e8f0ec; border:1px solid #a8c4b4; border-radius:8px; padding:0.7rem 0.9rem; margin-bottom:0.8rem;">'
        f'<div style="font-size:0.68rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#2e4a3e; margin-bottom:4px;">Active target</div>'
        f'<div style="font-size:0.92rem; font-weight:600; color:#1e3329;">📖 {age} yrs · {condition}</div>'
        f'<div style="font-size:0.75rem; color:#5a8a74; margin-top:2px;">{age_group} · {num_papers} papers</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    # Show what the app knows about this condition
    _profile = get_condition_profile(condition)
    with st.expander("What we know about this condition"):
        st.markdown(
            f'<div style="font-size:0.78rem; color:#2c2416; line-height:1.65;">'
            f'<strong style="color:#2e4a3e;">Key challenges:</strong><br>{_profile["reading_challenges"]}'
            f'</div>',
            unsafe_allow_html=True
        )

# ── Main Input ────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="sentence-label-row">'
    f'<span class="sentence-label">Your sentence</span>'
    f'<span class="target-chip">📖 {age} yrs · {condition}</span>'
    f'</div>',
    unsafe_allow_html=True
)

sentence = st.text_area(
    label="sentence_input",
    label_visibility="collapsed",
    value="The little fish swam very far away because he wanted to find his best friend.",
    height=115,
    placeholder="Write or paste a sentence from your story here…"
)

analyze_btn = st.button("Analyze & Revise →", type="primary")

PROMPT_QUANTITY = """You are a scientific writing advisor helping children's story authors.

CONDITION-SPECIFIC CONTEXT FOR {condition}:
This child's key reading challenges: {reading_challenges}
For QUANTITY suggestions specifically, research and clinical guidance says: {quantity_focus}
Contrast example to guide your rewrites: {example_contrast}

RESEARCH ABSTRACTS (cite only IDs that appear here):
{context}

AUTHOR'S SENTENCE: "{sentence}"
TARGET READER: {age}-year-old child with {condition}

YOUR TASK — QUANTITY FOCUS:
Each suggestion must address a SPECIFIC challenge listed above for {condition}.
Do NOT give generic "shorten the sentence" advice — explain WHY that change matters for THIS condition.
The example rewrites must look visibly different from each other and both reflect the condition-specific need.

RULES:
- Only cite IDs present in the abstracts above. Do NOT invent citations.
- Each suggestion must start by naming the specific {condition} challenge it addresses.
- For each box, give exactly 2 suggestions.
- For each suggestion, give exactly 2 example rewrites that are clearly different from each other.

Format EXACTLY:

### 📘 BOX 1 — European Language Suggestions (Quantity)
(Based on research about English, Norwegian, Dutch, or French-speaking children)

**Suggestion 1:** [Start with: "For children with {condition}, [specific challenge]. Research shows [what to do]. Applied here: [how this changes the sentence].] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite angle 1 — e.g. split into two sentences]
EXAMPLE_B: [Rewrite angle 2 — e.g. remove subordinate clause entirely]

**Suggestion 2:** [Different specific challenge for {condition}. Research shows [what to do]. Applied here: [how this changes the sentence].] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite angle 1]
EXAMPLE_B: [Rewrite angle 2]

### 🌙 BOX 2 — Eastern/Middle Eastern Language Suggestions (Quantity)
(Based on research about Persian or Arabic-speaking children, or different script directions)

**Suggestion 1:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

**Suggestion 2:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

### 📗 BOX 3 — General & Multilingual Suggestions (Quantity)
(Applies across languages and cultures)

**Suggestion 1:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

**Suggestion 2:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

### ✨ Final Revised Sentence (Quantity-Optimised for {condition})
"[Best rewritten sentence that most directly addresses the quantity needs of a child with {condition}]"

If insufficient evidence for a box: "No direct evidence found in current abstracts for this language group."
"""

PROMPT_QUALITY = """You are a scientific writing advisor helping children's story authors.

CONDITION-SPECIFIC CONTEXT FOR {condition}:
This child's key reading challenges: {reading_challenges}
For QUALITY suggestions specifically, research and clinical guidance says: {quality_focus}
Contrast example to guide your rewrites: {example_contrast}

RESEARCH ABSTRACTS (cite only IDs that appear here):
{context}

AUTHOR'S SENTENCE: "{sentence}"
TARGET READER: {age}-year-old child with {condition}

YOUR TASK — QUALITY FOCUS:
Each suggestion must address a SPECIFIC challenge listed above for {condition}.
Do NOT give generic "use richer language" advice — explain WHY that change matters for THIS condition.
The example rewrites must look visibly different from each other and both reflect the condition-specific need.

RULES:
- Only cite IDs present in the abstracts above. Do NOT invent citations.
- Each suggestion must start by naming the specific {condition} challenge it addresses.
- For each box, give exactly 2 suggestions.
- For each suggestion, give exactly 2 example rewrites that are clearly different from each other.

Format EXACTLY:

### 📘 BOX 1 — European Language Suggestions (Quality)
(Based on research about English, Norwegian, Dutch, or French-speaking children)

**Suggestion 1:** [Start with: "For children with {condition}, [specific challenge]. Research shows [what to do]. Applied here: [how this changes the sentence's quality].] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite angle 1 — e.g. add sensory grounding]
EXAMPLE_B: [Rewrite angle 2 — e.g. make emotion explicit instead of implied]

**Suggestion 2:** [Different specific challenge for {condition}. Research shows [what to do]. Applied here.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite angle 1]
EXAMPLE_B: [Rewrite angle 2]

### 🌙 BOX 2 — Eastern/Middle Eastern Language Suggestions (Quality)
(Based on research about Persian or Arabic-speaking children, or different script directions)

**Suggestion 1:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

**Suggestion 2:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

### 📗 BOX 3 — General & Multilingual Suggestions (Quality)
(Applies across languages and cultures)

**Suggestion 1:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

**Suggestion 2:** [Condition-specific challenge + research finding + application.] (ID: XXXXXXXX)
EXAMPLE_A: [Rewrite]
EXAMPLE_B: [Rewrite]

### ✨ Final Revised Sentence (Quality-Optimised for {condition})
"[Best rewritten sentence that most directly addresses the quality/language needs of a child with {condition}]"

If insufficient evidence for a box: "No direct evidence found in current abstracts for this language group."
"""

# ── Render helpers ────────────────────────────────────────────────────────────
BOX_DEFS = {
    "BOX 1": {
        "icon": "📘", "title": "European Language Suggestions",
        "accent": "#3B6D11", "pill_bg": "#EAF3DE", "pill_color": "#3B6D11",
        "border": "#3B6D11",
    },
    "BOX 2": {
        "icon": "🌙", "title": "Eastern / Middle Eastern Language Suggestions",
        "accent": "#854F0B", "pill_bg": "#FAEEDA", "pill_color": "#854F0B",
        "border": "#854F0B",
    },
    "BOX 3": {
        "icon": "📗", "title": "General & Multilingual Suggestions",
        "accent": "#185FA5", "pill_bg": "#E6F1FB", "pill_color": "#185FA5",
        "border": "#185FA5",
    },
}

def parse_and_render(result_text: str, focus_label: str):
    for box_key, bd in BOX_DEFS.items():
        # find start
        start = None
        for candidate in [
            f"### {bd['icon']} {box_key} —",
            f"### {box_key} —",
            f"### {bd['icon']} {box_key}",
            f"### {box_key}",
        ]:
            if candidate in result_text:
                start = result_text.index(candidate)
                break
        if start is None:
            continue

        # find end
        ends = []
        for other_key, other_bd in BOX_DEFS.items():
            if other_key == box_key:
                continue
            for mc in [f"### {other_bd['icon']} {other_key}", f"### {other_key}"]:
                if mc in result_text and result_text.index(mc) > start:
                    ends.append(result_text.index(mc))
        if "### ✨ Final Revised Sentence" in result_text:
            fi = result_text.index("### ✨ Final Revised Sentence")
            if fi > start:
                ends.append(fi)
        end = min(ends) if ends else len(result_text)

        raw = result_text[start:end]
        lines = [l for l in raw.split("\n") if not l.strip().startswith("###") and not (l.strip().startswith("(") and l.strip().endswith(")"))]

        # parse suggestions
        suggestions = []
        cur_text = ""
        cur_examples = []

        def flush(t, exs):
            if t.strip() or exs:
                suggestions.append({"text": t.strip(), "examples": exs})

        for line in lines:
            s = line.strip()
            if s.startswith("**Suggestion"):
                flush(cur_text, cur_examples)
                cur_text = s.replace("**", "")
                cur_examples = []
            elif s.startswith("EXAMPLE_A:") or s.startswith("EXAMPLE_B:"):
                ex = s.split(":", 1)[1].strip().strip('"')
                cur_examples.append(ex)
            elif s:
                if cur_text:
                    cur_text += " " + s
                else:
                    cur_text = s
        flush(cur_text, cur_examples)

        # ── Box header ──
        st.markdown(f"""
        <div class="box-card">
            <div class="box-card-header">
                <div class="box-card-accent" style="background:{bd['accent']};"></div>
                <div><div class="box-card-title">{bd['icon']} {bd['title']}</div></div>
                <span class="focus-pill" style="background:{bd['pill_bg']}; color:{bd['pill_color']};">{focus_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Each suggestion as its own st.markdown call ──
        for i, sg in enumerate(suggestions):
            # Build example HTML safely
            examples_html = ""
            for j, ex in enumerate(sg["examples"]):
                ltr = chr(65 + j)
                # escape any stray < > in the AI text
                safe_ex = ex.replace("<", "&lt;").replace(">", "&gt;")
                examples_html += (
                    f'<div style="margin-bottom:6px;">'
                    f'<div class="example-label-sm">Example {ltr}</div>'
                    f'<div class="example-sentence">{safe_ex}</div>'
                    f'</div>'
                )

            example_block = ""
            if examples_html:
                example_block = (
                    f'<div class="example-block">'
                    f'<div class="example-warning">&#9888; Illustrative only — use your own skill to craft the best version</div>'
                    f'{examples_html}'
                    f'</div>'
                )

            safe_text = sg["text"].replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(
                f'<div class="suggestion-item" style="border-left-color:{bd["accent"]}; margin-bottom:8px;">'
                f'<div class="suggestion-number">Suggestion {i + 1}</div>'
                f'<div class="suggestion-text">{safe_text}</div>'
                f'{example_block}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Close box-card visual gap
        st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)

    # Final sentence
    marker = "### ✨ Final Revised Sentence"
    if marker in result_text:
        final = result_text.split(marker)[1].strip()
        if final.startswith("("):
            final = final.split(")", 1)[-1].strip()
        final = final.strip().strip('"')
        st.markdown(f"""
        <div class="final-sentence-wrapper">
            <div class="final-sentence-label">✨ Final revised sentence — {focus_label}</div>
            <div class="final-sentence-text">"{final}"</div>
        </div>
        """, unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not sentence.strip():
        st.warning("Please enter a sentence to analyze.")
    else:
        with st.status("Searching PubMed, Semantic Scholar, and OpenAlex…", expanded=False) as status:
            papers, fallback_msg = fetch_all_sources(condition, age_group, n_each=max(2, num_papers // 3))
            if not papers:
                status.update(label="No papers found", state="error")
                st.error(fallback_msg)
                st.stop()
            status.update(label=fallback_msg, state="complete")

        st.markdown(f'<div class="info-box">{fallback_msg}</div>', unsafe_allow_html=True)

        context = "\n\n---\n\n".join([
            f"ID {p['id']} (Source: {p.get('source', 'PubMed')}):\n{p['text'][:900]}"
            for p in papers
        ])

        profile = get_condition_profile(condition)

        results = {}
        with st.status("Running analysis — quantity & quality passes…", expanded=False) as status:
            for focus, tmpl in [("Quantity", PROMPT_QUANTITY), ("Quality", PROMPT_QUALITY)]:
                filled = tmpl.format(
                    context=context,
                    sentence=sentence,
                    age=age,
                    condition=condition,
                    reading_challenges=profile["reading_challenges"],
                    quantity_focus=profile["quantity_focus"],
                    quality_focus=profile["quality_focus"],
                    example_contrast=profile["example_contrast"],
                )
                try:
                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": filled}],
                        temperature=0.4,
                        max_tokens=1400
                    )
                    results[focus] = resp.choices[0].message.content
                except Exception as e:
                    status.update(label="API error", state="error")
                    st.error(f"Groq API error ({focus}): {e}")
                    st.stop()
            status.update(label="Analysis complete", state="complete")

        st.markdown("---")
        tab1, tab2 = st.tabs(["📏  Quantity suggestions", "✨  Quality suggestions"])

        with tab1:
            st.markdown(
                '<div style="font-size:0.87rem; color:#6b5d4e; margin-bottom:1.2rem; line-height:1.65;">'
                'Focused on <strong style="color:#2c2416;">word count, sentence length, and structural simplicity</strong>.'
                '</div>', unsafe_allow_html=True
            )
            parse_and_render(results["Quantity"], "Quantity")

        with tab2:
            st.markdown(
                '<div style="font-size:0.87rem; color:#6b5d4e; margin-bottom:1.2rem; line-height:1.65;">'
                'Focused on <strong style="color:#2c2416;">emotional clarity, vocabulary richness, and narrative engagement</strong>.'
                '</div>', unsafe_allow_html=True
            )
            parse_and_render(results["Quality"], "Quality")

        st.markdown("""
        <div class="warn-box">
            ⚠️ <strong>Evidence note:</strong> Suggestions are based on research abstracts, not full papers.
            Verify recommendations against the full study before applying to published work.
            Example sentences are illustrative — always apply your own craft.
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"📄 View {len(papers)} source abstracts"):
            for p in papers:
                source = p.get("source", "PubMed")
                if source == "PubMed":
                    link = f"https://pubmed.ncbi.nlm.nih.gov/{p['id']}/"
                elif source == "Semantic Scholar":
                    link = f"https://www.semanticscholar.org/paper/{p['id']}"
                else:
                    link = f"https://openalex.org/{p['id']}"
                st.markdown(f"""
                <div class="paper-card">
                    <div class="paper-source">{source} · {p['id']}</div>
                    <div class="paper-abstract">{p['text']}</div>
                    <a href="{link}" target="_blank"
                       style="font-size:0.78rem; color:#2e4a3e; text-decoration:none; font-weight:600; margin-top:0.5rem; display:inline-block;">
                       → Open source ↗
                    </a>
                </div>
                """, unsafe_allow_html=True)

