import requests
from bs4 import BeautifulSoup
import time
from setting import *
from datetime import datetime

def track_update():
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
            }
    
    # 資料庫連結
    conn = sql_connect()
    cursor = conn.cursor()
    sql = "SELECT comics_id,episode FROM comics order by created_at desc"
    cursor.execute(sql)
    comics_ids = cursor.fetchall()
    
    # notify
    for comics_id in comics_ids:
        try:
            now = datetime.now()
            
            data = {
                "comics_id":comics_id[0],
                "episode":comics_id[1]
            }
            request = requests.get(f"https://m.manhuagui.com/comic/{data['comics_id']}/",headers=headers)
            soup = BeautifulSoup(request.text, 'html.parser')

            # title
            title_tag = soup.find_all("div", class_= "main-bar bar-bg1")
            piece_name = title_tag[0].string

            # episode
            cont_list = soup.find_all("div",class_="cont-list")[0].find_all("dl") #介紹列表
            update_episode = f"{cont_list[0].dd.string}"
            
            if data["episode"] == update_episode:
                print(f"{comics_id} 已為最新集數")
                time.sleep(5)
                continue
                
            # episode_update_time
            episode_update_time = f"{cont_list[1].dd.string}"
            
            # episode_url
            first_chatlist = soup.find_all("div",class_="chapter-list")
            episode_url = "https://m.manhuagui.com"+first_chatlist[0].a.get('href')
            
            headers = {
                    "Authorization": "Bearer " + line_notify_token,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            params = {"message":"\n" + "piece_name：" + piece_name + "\n" + "update_episode：" + update_episode + "\n" + 
                    "episode_update_time：" + episode_update_time + "\n" + "episode_url：" + episode_url}
            r = requests.post("https://notify-api.line.me/api/notify",
                            headers=headers, params=params)
            
            # update sql episode
            sql = f"UPDATE comics SET episode = '{update_episode}',name = '{piece_name}',updated_at = '{now}',url = '{episode_url}' WHERE comics_id = '{data['comics_id']}'"
            cursor.execute(sql)
            conn.commit()
            
            print(f"{comics_id,piece_name,update_episode}執行中")
            time.sleep(5)
        except:
            print(f"{comics_id,piece_name,update_episode}執行錯誤")
            time.sleep(5)
            continue