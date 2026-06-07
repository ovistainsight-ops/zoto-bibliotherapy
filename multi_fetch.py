import requests

def fetch_semantic_scholar(condition: str, age_group: str, n: int = 4) -> list:
    query = f"{condition} children storytelling {age_group} language"
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    try:
        resp = requests.get(url, params={"query": query, "limit": n, "fields": "paperId,title,abstract,year"}, timeout=15)
        papers = []
        for p in resp.json().get("data", []):
            if p.get("abstract"):
                papers.append({"id": p["paperId"][:8], "text": f"{p.get('title', '')}\n\n{p['abstract']}", "source": "Semantic Scholar"})
        return papers
    except Exception:
        return []

def fetch_openalex(condition: str, n: int = 4) -> list:
    query = f"{condition} children reading language learning"
    url = "https://api.openalex.org/works"
    try:
        resp = requests.get(url, params={"search": query, "per-page": n, "filter": "has_abstract:true", "mailto": "research@zotobio.app"}, timeout=15)
        papers = []
        for p in resp.json().get("results", []):
            abstract = p.get("abstract_inverted_index")
            if abstract:
                words = {v: k for k, vals in abstract.items() for v in vals}
                text = " ".join(words[i] for i in sorted(words))
                papers.append({"id": p.get("id", "")[-8:], "text": f"{p.get('title', '')}\n\n{text}", "source": "OpenAlex"})
        return papers
    except Exception:
        return []

def fetch_all_sources(condition: str, age_group: str, n_each: int = 3) -> tuple:
    from pubmed_fetch import fetch_papers as fetch_pubmed
    pubmed = fetch_pubmed(condition, age_group, n=n_each)
    semantic = fetch_semantic_scholar(condition, age_group, n=n_each)
    openalex = fetch_openalex(condition, n=n_each)
    
    all_papers = pubmed + semantic + openalex
    if not all_papers:
        return [], "❌ No research found across all databases."
    
    source_summary = f"📚 Found {len(pubmed)} PubMed · {len(semantic)} Semantic Scholar · {len(openalex)} OpenAlex papers"
    return all_papers, source_summary
