import streamlit as st
import requests
from groq import Groq

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ZotoBibliotherapy",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (Warm, Clean, Professional + Darker Text Fixes) ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #4a4a4a; background-color: #ffffff; }
.main .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 900px; background-color: #ffffff; }
.zoto-header { text-align: center; padding: 2.5rem 0 1.5rem; border-bottom: 1px solid #f0f0f0; margin-bottom: 2rem; }
.zoto-header h1 { font-family: 'Lora', serif; font-size: 2.6rem; font-weight: 600; color: #2c2c2c; letter-spacing: -0.5px; margin: 0; }
.zoto-header .tagline { font-size: 0.95rem; color: #7a7a7a; margin-top: 0.4rem; font-weight: 300; letter-spacing: 0.03em; }
section[data-testid="stSidebar"] { background: #fafafa; border-right: 1px solid #f0f0f0; }
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
.sidebar-title { font-family: 'Lora', serif; font-size: 1rem; color: #2c2c2c; font-weight: 600; margin-bottom: 1.2rem; padding-bottom: 0.5rem; border-bottom: 2px solid #8b6f47; }
label { font-size: 0.82rem !important; font-weight: 500 !important; color: #666666 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div { border-radius: 6px !important; border-color: #e0e0e0 !important; background-color: #ffffff !important; font-family: 'DM Sans', sans-serif !important; color: #2c2c2c !important; }
.stTextArea > div > div > textarea { border-radius: 8px !important; border-color: #e0e0e0 !important; background-color: #ffffff !important; font-family: 'Lora', serif !important; font-size: 1rem !important; line-height: 1.7 !important; color: #2c2c2c !important; }
.stTextArea > div > div > textarea:focus { border-color: #8b6f47 !important; box-shadow: 0 0 0 2px rgba(139,111,71,0.1) !important; }
.stButton > button { background: #8b6f47 !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 0.65rem 2rem !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; font-weight: 500 !important; letter-spacing: 0.05em !important; transition: background 0.2s ease !important; width: 100%; }
.stButton > button:hover { background: #7a5f3a !important; }

/* FIXED: Darker text for readability */
.result-card { 
    background: #fafafa; 
    border: 1px solid #f0f0f0; 
    border-left: 4px solid #8b6f47; 
    border-radius: 8px; 
    padding: 1.6rem 1.8rem; 
    margin: 1.5rem 0; 
    color: #2c2c2c !important; /* Force dark text */
}
.result-card p, .result-card strong, .result-card li, .result-card em {
    color: #2c2c2c !important; /* Force dark text for all markdown elements inside */
}
.result-card h3 { font-family: 'Lora', serif; color: #2c2c2c; font-size: 1.05rem; margin-bottom: 0.8rem; }

[data-testid="stCodeBlock"] { background-color: #ffffff !important; border: 1px solid #e8dfd2 !important; border-left: 4px solid #8b6f47 !important; border-radius: 8px !important; color: #2c2c2c !important; font-family: 'Lora', serif !important; font-size: 1.15rem !important; line-height: 1.6 !important; padding: 1.5rem !important; margin: 1.5rem 0 !important; }
[data-testid="stCodeBlock"] code { font-family: 'Lora', serif !important; font-style: italic !important; color: #2c2c2c !important; background: transparent !important; padding: 0 !important; }

.paper-card { background: #fafafa; border-radius: 6px; padding: 1rem 1.2rem; margin: 0.6rem 0; border: 1px solid #f0f0f0; }
.paper-card .pmid { font-size: 0.75rem; font-weight: 600; color: #8b6f47; text-transform: uppercase; letter-spacing: 0.1em; }
/* FIXED: Darker abstract text */
.paper-card .abstract { font-size: 0.88rem; color: #333333 !important; line-height: 1.6; margin-top: 0.4rem; }

hr { border-color: #f0f0f0 !important; }
.warn-box { background: #fffdf5; border: 1px solid #f0e6d2; border-radius: 6px; padding: 0.7rem 1rem; font-size: 0.85rem; color: #6b5a42; margin-bottom: 1.5rem; }

.fallback-box {
    background: #f0f7ff;
    border: 1px solid #cce0ff;
    border-left: 4px solid #4a90e2;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 1.5rem 0;
    font-size: 0.9rem;
    color: #2c5282;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ── API Client ────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# ── Smart PubMed Fetcher with Fallback ────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_papers_smart(condition: str, age_group: str, n: int = 3):
    session = requests.Session()
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    # Tier 1: Exact Match
    query_tier1 = f"{condition} storytelling children {age_group}"
    search1 = session.get(search_url, params={"db": "pubmed", "term": query_tier1, "retmax": n, "sort": "date", "retmode": "json"}, timeout=15).json()
    ids_tier1 = search1["esearchresult"].get("idlist", [])
    
    if ids_tier1:
        fetch1 = session.get(fetch_url, params={"db": "pubmed", "id": ",".join(ids_tier1), "rettype": "abstract", "retmode": "text"}, timeout=15)
        papers = []
        for i, block in enumerate(fetch1.text.strip().split("\n\n\n")):
            if block.strip() and i < len(ids_tier1):
                papers.append({"id": ids_tier1[i], "text": block.strip()})
        return papers, None 
    
    # Tier 2: Fallback (Drop age constraint, keep condition)
    query_tier2 = f"{condition} storytelling children"
    search2 = session.get(search_url, params={"db": "pubmed", "term": query_tier2, "retmax": n, "sort": "date", "retmode": "json"}, timeout=15).json()
    ids_tier2 = search2["esearchresult"].get("idlist", [])
    
    if ids_tier2:
        fetch2 = session.get(fetch_url, params={"db": "pubmed", "id": ",".join(ids_tier2), "rettype": "abstract", "retmode": "text"}, timeout=15)
        papers = []
        for i, block in enumerate(fetch2.text.strip().split("\n\n\n")):
            if block.strip() and i < len(ids_tier2):
                papers.append({"id": ids_tier2[i], "text": block.strip()})
        
        fallback_msg = f"🔍 **Research Search Note:** We first searched for articles specific to '{age_group}' children with '{condition}'. Since no direct matches were found, we expanded the search to general '{condition}' storytelling research. The suggestions below are based on these broader, condition-specific findings."
        return papers, fallback_msg

    # Tier 3: No papers found at all
    return [], "❌ **No Research Found:** We could not find relevant PubMed articles for this condition. Please try a different condition (e.g., 'learning disabilities') or check your spelling."

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="zoto-header">
    <h1>ZotoBibliotherapy</h1>
    <p class="tagline">Evidence-based writing guidance for children's story authors</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">Story Parameters</div>', unsafe_allow_html=True)

    condition = st.selectbox(
        "Condition",
        ["autism", "ADHD", "dyslexia", "anxiety", "sensory processing disorder"],
        index=0
    )
    custom_condition = st.text_input("Or enter custom condition", placeholder="e.g., selective mutism")
    if custom_condition.strip():
        condition = custom_condition.strip()

    age = st.slider("Child's Age", min_value=3, max_value=12, value=5, step=1)
    age_group = "preschool" if age < 7 else "school-age"
    
    st.markdown("---")
    num_papers = st.slider("Research papers to fetch", min_value=2, max_value=5, value=3)

# ── Main ──────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("#### Your sentence")
with col2:
    st.markdown(f"<div style='text-align:right; font-size:0.8rem; color:#7a7a7a; padding-top:6px;'>Target: {age} yrs · {condition}</div>", unsafe_allow_html=True)

sentence = st.text_area(
    label="sentence_input",
    label_visibility="collapsed",
    value="The little fish swam very far away because he wanted to find his best friend.",
    height=110,
    placeholder="Write or paste a sentence from your story here…"
)

analyze_btn = st.button("Analyze & Revise", type="primary")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not sentence.strip():
        st.warning("Please enter a sentence to analyze.")
    else:
        # Step 1: Smart Fetch
        with st.status("Searching PubMed...", expanded=False) as status:
            papers, fallback_msg = fetch_papers_smart(condition, age_group, n=num_papers)
            
            if not papers:
                status.update(label="No papers found", state="error")
                st.error(fallback_msg)
                st.stop()
            
            status.update(label=f"Found {len(papers)} papers", state="complete")

        if fallback_msg:
            st.markdown(f'<div class="fallback-box">{fallback_msg}</div>', unsafe_allow_html=True)

        # Step 2: Build Context
        context = "\n\n---\n\n".join([f"PMID {p['id']}:\n{p['text'][:900]}" for p in papers])

        # Step 3: Single, Powerful Prompt (Extract Rules + Apply)
        prompt = f"""You are a scientific writing advisor helping children's story authors.

RESEARCH ABSTRACTS (from PubMed):
{context}

AUTHOR'S SENTENCE:
"{sentence}"

TARGET READER: {age}-year-old child with {condition}

INSTRUCTIONS:
1. ANALYZE: Based STRICTLY on the provided abstracts, identify 2 to 3 specific writing rules or adaptations for this target reader.
2. SUGGEST: Provide 2 to 3 actionable suggestions to improve the author's sentence. Each suggestion MUST cite the supporting PMID.
3. REWRITE: Provide a "Final Revised Version" of the sentence that applies these rules. 

CRITICAL RULES FOR AI:
- DO NOT invent citations. Only use PMIDs present in the text above.
- If the abstracts suggest breaking long sentences into shorter, clearer ones, do so in the final rewrite.
- If the abstracts emphasize explicit emotional or sensory language, ensure the final rewrite includes it naturally.
- Keep the final rewrite concise and age-appropriate.

Format your response exactly like this:
### 🔬 Scientific Suggestions
- **Suggestion 1:** [Explanation] (PMID: XXXXXXXX)
- **Suggestion 2:** [Explanation] (PMID: XXXXXXXX)

### ✨ Final Revised Sentence
"[The rewritten sentence(s) here]"
"""

        # Step 4: Call Groq
        with st.status("Analyzing research and revising sentence...", expanded=False) as status:
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=1000
                )
                result_text = response.choices[0].message.content
                status.update(label="Analysis complete", state="complete")
            except Exception as e:
                status.update(label="API error", state="error")
                st.error(f"Groq API error: {e}")
                st.stop()

        # Step 5: Display Results
        st.markdown("---")
        
        if "### ✨ Final Revised Sentence" in result_text:
            parts = result_text.split("### ✨ Final Revised Sentence")
            suggestions_part = parts[0].replace("### 🔬 Scientific Suggestions", "").strip()
            final_sentence_part = parts[1].strip().strip('"')
            
            st.markdown("### 🔬 Scientific Suggestions")
            st.markdown(f'<div class="result-card">{suggestions_part}</div>', unsafe_allow_html=True)
            
            st.markdown("### ✨ Final Revised Sentence")
            st.code(final_sentence_part, language="text")
        else:
            st.markdown(result_text)

        st.markdown("""
        <div class="warn-box">
        ⚠️ <strong>Evidence note:</strong> These suggestions are based on PubMed abstracts, not full papers.
        Always verify recommendations against the full study before applying them to published work.
        </div>
        """, unsafe_allow_html=True)

        # FIXED: Removed the [:500] truncation to show full abstracts
        with st.expander(f"📄 View {len(papers)} source abstracts"):
            for p in papers:
                st.markdown(f"""
                <div class="paper-card">
                    <div class="pmid">PMID · {p['id']}</div>
                    <div class="abstract">{p['text']}</div>
                    <div style="margin-top:0.5rem;">
                        <a href="https://pubmed.ncbi.nlm.nih.gov/{p['id']}/" target="_blank"
                           style="font-size:0.78rem; color:#8b6f47; text-decoration:none; font-weight:500;">
                           → Open on PubMed ↗
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)