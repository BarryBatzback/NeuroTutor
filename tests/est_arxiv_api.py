# test_arxiv_api.py
import arxiv

try:
    search = arxiv.Search(
        query="machine learning",
        max_results=2
    )
    papers = list(search.results())
    print(f"✅ arXiv: найдено {len(papers)} статей")
except Exception as e:
    print(f"❌ arXiv ошибка: {e}")