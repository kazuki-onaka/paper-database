#このスクリプトは、papers.db を初期化し、テーブルを削除・再作成します。
#全データが削除されるため、実行前にバックアップを推奨！
import sqlite3

def reset_database():
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    # 既存のテーブルを削除
    cursor.execute("DROP TABLE IF EXISTS papers")

    # 新しいテーブルを作成
    cursor.execute('''
        CREATE TABLE papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            author TEXT,
            year TEXT,
            keywords TEXT,
            summary TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("データベースをリセットしました。")

if __name__ == "__main__":
    reset_database()