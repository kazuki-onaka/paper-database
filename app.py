"""
役割
Flaskのルート（エンドポイント）を設定し、Webインターフェースを提供する。
論文の検索機能を提供し、データベースから情報を取得。
検索結果をHTMLページに表示する。
"""

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# トップページ
@app.route('/')
def index():
    return render_template('index.html')

# 論文検索ページ
@app.route('/search', methods=['GET', 'POST'])
def search_paper():
    if request.method == 'POST':
        query = request.form['query']

        conn = sqlite3.connect('papers.db')
        cursor = conn.cursor()

        # 検索実行
        cursor.execute('''
            SELECT * FROM papers
            WHERE title LIKE ? OR keywords LIKE ? OR author LIKE ? OR year LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))

        results = cursor.fetchall()
        conn.close()

        return render_template('search_results.html', results=results, query=query, page=1, total_pages=1)

    # GET リクエスト時は検索フォームページを表示
    return render_template('search_paper.html')

@app.route('/paper/<int:paper_id>')
def paper_detail(paper_id):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
    paper = cursor.fetchone()
    
    conn.close()

    if not paper:
        return "論文が見つかりませんでした。", 404

    return render_template('paper_detail.html', paper=paper)

# アプリを実行
if __name__ == "__main__":
    app.run(debug=True)