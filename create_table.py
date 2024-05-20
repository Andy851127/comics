from setting import *

def create_table():
    try:
        conn = sql_connect()
        cursor = conn.cursor()

        sql = """
        CREATE TABLE comics (
            id serial PRIMARY KEY,
            comics_id int UNIQUE NOT NULL,
            name VARCHAR (255) NULL,
            episode VARCHAR (255) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            url VARCHAR (255)
        );"""
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()
    except:
        pass