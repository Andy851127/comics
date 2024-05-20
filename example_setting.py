import os
import psycopg2

# 連線資料庫
def sql_connect():
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a python-flask-comics').read()[:-1]
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn=psycopg2.connect(
        host="host",
        database="database",
        user="username",
        password="password"
    )
    return conn

line_notify_token = "line_notify_token"