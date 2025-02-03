#このスクリプトは、データベース内で同じタイトルの論文が複数登録されている場合、一つだけ残し他を削除します。
import sqlite3

def remove_duplicates():
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()

    # タイトルが重複している場合、最も古いID以外を削除
    cursor.execute('''
        DELETE FROM papers
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM papers
            GROUP BY title
        )
    ''')

    conn.commit()
    conn.close()
    print("重複データを削除しました。")

if __name__ == "__main__":
    remove_duplicates()