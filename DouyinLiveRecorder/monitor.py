import os
import sqlite3
import time

import configparser
config_file = './config/config.ini'
encoding = 'utf-8-sig'
config = configparser.RawConfigParser()
config.read(config_file, encoding=encoding)
segment_time = int(config.get('录制设置','视频分段时间(秒)'))

# 连接到数据库，如果不存在则创建
db_path = os.getcwd() + '/file_monitor.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 创建一个表来存储文件的信息
c.execute('''CREATE TABLE IF NOT EXISTS files
             (filepath TEXT, liveName TEXT, liveURL TEXT, timestamp REAL, isAnalyzed BOOLEAN)''')

# 设置要监视的文件夹路径
folder_to_watch = os.getcwd() + '/downloads'

def monitor_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and file_path[-3:].lower() == 'mp4':
                # 检查数据库中是否已经存在该文件
                c.execute("SELECT * FROM files WHERE filepath=? AND isAnalyzed=?", (file_path,False))
                result = c.fetchone()
                if result is None:
                    # 如果数据库中不存在该文件，则将其添加到数据库中
                    liveName = os.path.basename(os.path.dirname(file_path))
                    liveURL = ""
                    with open("./config/URL_config.ini",'r',encoding='utf-8') as file:
                        for line in file:
                            if liveName in line:
                                liveURL = line.split(',')[0]
                                break
                    c.execute("INSERT INTO files (filepath, liveName, liveURL, timestamp, isAnalyzed) VALUES (?, ?, ?, ?)", 
                              (file_path, liveName, liveURL, time.time(), False))
                    conn.commit()
                    print(f"New file detected: {file_path}")

while True:
    time.sleep(segment_time)
    monitor_folder(folder_to_watch)
