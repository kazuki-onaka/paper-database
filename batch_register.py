import os
import sqlite3
import fitz  # PyMuPDF
from fetch_paper_info import get_paper_info  # Google Scholar & CrossRef からデータ取得

# データベース接続
conn = sqlite3.connect('papers.db')
cursor = conn.cursor()

def extract_metadata_and_content(file_path):
    doc = fitz.open(file_path)
    metadata = doc.metadata

    title = metadata.get("title", "").strip() or os.path.splitext(os.path.basename(file_path))[0]
    author = metadata.get("author", "").strip() or "Unknown"
    creation_date = metadata.get("creationDate", "")

    year = "Unknown"
    if creation_date.startswith("D:"):
        year = creation_date[2:6]

    summary = doc[0].get_text("text").strip() if len(doc) > 0 else "No summary available"
    summary = summary.replace("\xa0", " ")[:400]

    # Google Scholar & CrossRef で著者・発行年・要約を補完
    if author == "Unknown" or year == "Unknown":
        fetched_author, fetched_year, fetched_summary = get_paper_info(title)
        author = fetched_author if author == "Unknown" else author
        year = fetched_year if year == "Unknown" else year
        summary = fetched_summary if summary == "No summary available" else summary

    return title, author, year, summary

def register_pdfs(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.endswith(".pdf"):
            print(f"スキップ: {filename}（PDFではない）")
            continue

        file_path = os.path.join(folder_path, filename)
        title, author, year, summary = extract_metadata_and_content(file_path)

        cursor.execute("SELECT * FROM papers WHERE title = ?", (title,))
        existing_paper = cursor.fetchone()
        if existing_paper:
            print(f"スキップ: {title} (既に登録済み)")
            continue

        cursor.execute('''
            INSERT INTO papers (title, author, year, keywords, summary)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, year, "Batch Import", summary))
        print(f"登録: {title}")

    conn.commit()
    conn.close()
    print("登録完了！")

folder_path = r"C:\Users\USER\Documents\修士研究\グローバルマーケティング"
register_pdfs(folder_path)