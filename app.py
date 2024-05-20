from flask import Flask,render_template,url_for,redirect
from flask import request as req
from requests import request
from comics import track_update
from create_table import create_table
from setting import *
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__ , static_folder='images')

# 建立資料表
create_table()

@app.route("/") # 函式的裝飾 (Decorator): 以函式為基礎，提供附加的功能
def home():
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM score_list "
    cursor.execute(sql)
    score_list_datas = cursor.fetchall()
    conn.close()
    cursor.close()
    
    sched = BlockingScheduler()
    # 每2小時觸發
    sched.add_job(track_update(), 'interval', hours=1)
    sched.start()
    
    return render_template("hello.html",score_list_datas = score_list_datas)

@app.route("/show_comics_datas")
def show_comics_datas():
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM comics ORDER BY created_at DESC"
    cursor.execute(sql)
    comics_datas = cursor.fetchall()
    conn.close()
    cursor.close()
    return render_template("show_comics_datas.html",comics_datas=comics_datas)

@app.route("/insert",methods = ["POST"])
def insert():
    conn = sql_connect()
    cursor = conn.cursor()
    now = datetime.now()
    comics_id = req.values["comics_id"]
    sql = "INSERT INTO comics(comics_id,episode,created_at,updated_at) values('{}','{}','{}','{}')".format(comics_id,"待更新",now,now)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()
    return  redirect(url_for('show_comics_datas')) 

@app.route("/delete/<int:comics_id>",methods = ['GET','POST'])
def delete(comics_id):
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "DELETE FROM comics WHERE comics_id = '{}'".format(comics_id)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()
    return  redirect(url_for('show_comics_datas'))     

# @app.route("/update_comics")
# def update_comics():
#     track_update()
    
if __name__=="__main__": # 如果以主程式執行
    app.run(debug=True) # 立刻啟動伺服器
