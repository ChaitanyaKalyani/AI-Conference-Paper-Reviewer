from modules.arxiv_retriever import search_arxiv

papers = search_arxiv(
    "welding defect detection"
)

for paper in papers:
    print("\nTITLE:")
    print(paper["title"])

    print("\nURL:")
    print(paper["url"])

    print("-" * 80)