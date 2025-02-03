#このスクリプトは、要約 (summary) が None または空のデータを「No summary available」に更新します。
import sqlite3

def fix_summaries():
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    # summaryカラムがNULLまたは空文字のデータを修正
    cursor.execute('''
        UPDATE papers
        SET summary = "No summary available"
        WHERE summary IS NULL OR summary = ""
    ''')

    conn.commit()
    conn.close()
    print("データベース内の要約データを修正しました。")

if __name__ == "__main__":
    fix_summaries()
