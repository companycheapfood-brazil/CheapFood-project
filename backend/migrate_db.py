import sqlite3
import re

def migrate_sql_to_sqlite():
    with open('Cheapfood_DB.sql', 'r', encoding='utf-8') as f:
        sql = f.read()

    sql = sql.replace('BIGSERIAL', 'INTEGER')
    sql = sql.replace('BIGINT', 'INTEGER')
    sql = sql.replace('CREATE OR REPLACE VIEW', 'CREATE VIEW')
    sql = re.sub(r'CURRENT_DATE \+ (\d+)', r"date('now', '+\1 days')", sql)
    
    # Connect to SQLite
    conn = sqlite3.connect('cheapfood.db')
    cursor = conn.cursor()
    
    # Execute the entire script
    try:
        cursor.executescript(sql)
        conn.commit()
        print("Database migrated successfully!")
    except Exception as e:
        print("Error executing SQL:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_sql_to_sqlite()
