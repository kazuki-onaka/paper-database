import sqlite3

# データベース接続
conn = sqlite3.connect('papers.db')
cursor = conn.cursor()

# 論文データを取得
cursor.execute("SELECT * FROM papers")
papers = cursor.fetchall()

# データがあるか確認
if papers:
    print("登録されている論文一覧:")
    for paper in papers:
        print(paper)
else:
    print("データベースに論文が登録されていません。")

conn.close()