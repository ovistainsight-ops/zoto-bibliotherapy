import requests
import time

def fetch_papers(condition: str, age_group: str, n: int = 5) -> list:
    query = f"{condition} storytelling children {age_group}"
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # ایجاد یک session برای مدیریت بهتر اتصالات
    session = requests.Session()
    
    # Step 1: get IDs
    print("🔍 در حال جستجو در PubMed...")
    search = session.get(url, params={
        "db": "pubmed",
        "term": query,
        "retmax": n,
        "sort": "date",
        "retmode": "json"
    }, timeout=30).json()
    
    ids = search["esearchresult"]["idlist"]
    if not ids:
        print("❌ مقاله‌ای پیدا نشد.")
        return []
    
    print(f"✅ {len(ids)} مقاله پیدا شد. در حال دریافت چکیده‌ها...")
    
    # ⏱️ صبر کوتاه برای جلوگیری از خطای SSL
    time.sleep(1)

    # Step 2: get abstracts
    try:
        fetch = session.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            params={
                "db": "pubmed", 
                "id": ",".join(ids), 
                "rettype": "abstract", 
                "retmode": "text"
            },
            timeout=30
        )
    except requests.exceptions.SSLError as e:
        print(f"⚠️ خطای SSL رخ داد. در حال تلاش مجدد...")
        time.sleep(2)
        fetch = session.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            params={
                "db": "pubmed", 
                "id": ",".join(ids), 
                "rettype": "abstract", 
                "retmode": "text"
            },
            timeout=30,
            verify=False  # غیرفعال کردن تأیید SSL (فقط برای تست)
        )
    
    papers = []
    for i, block in enumerate(fetch.text.strip().split("\n\n\n")):
        if block.strip():
            papers.append({"id": ids[i] if i < len(ids) else "?", "text": block.strip()})
    
    return papers


if __name__ == "__main__":
    results = fetch_papers("autism", "preschool", n=3)
    for p in results:
        print(f"\n--- PMID: {p['id']} ---")
        print(p["text"][:500])
        print("...")