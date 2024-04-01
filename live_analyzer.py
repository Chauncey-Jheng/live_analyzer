
import time
import os
import shutil
from match import match

from asr.kaldi_asr import run_kaldi_asr
from ocr.paddle_ocr import run_paddle_ocr

from flask import jsonify
from dao.dao import DAO
dao = DAO()

import configparser
config_file = './config.ini'
encoding = 'utf-8-sig'
config = configparser.RawConfigParser()
config.read(config_file, encoding=encoding)
is_keep_normal_live_video = config.get('视频分析配置','是否保留正常内容视频')
save_dir = config.get('视频分析配置','线索视频保存地址')
segment_time = int(config.get('录制设置','视频分段时间(秒)'))

import sqlite3

def video_to_txt(video_file_path:str):
    asr_file_path = video_file_path[:-4] + "_asr.txt"
    ocr_file_path = video_file_path[:-4] + "_ocr.txt"
    run_kaldi_asr(video_file_path, asr_file_path)
    run_paddle_ocr(video_file_path, ocr_file_path)
    asr_result = ""
    ocr_result = ""
    with open(asr_file_path, "r") as f:
        asr_result = f.read()
    with open(ocr_file_path, "r") as f:
        ocr_result = f.read()
    return asr_result, ocr_result

def remove_video(video_file_path:str):
    asr_file_path = video_file_path[:-4] + "_asr.txt"
    ocr_file_path = video_file_path[:-4] + "_ocr.txt"
    try:
        os.remove(video_file_path)
        os.remove(asr_file_path)
        os.remove(ocr_file_path)
        print("Remove normal live video")
    except OSError as e:
        print(f"Error: {e}")

def save_video(video_file_path:str, liveName:str, liveURL:str, result:str):
    asr_file_path = video_file_path[:-4] + "_asr.txt"
    ocr_file_path = video_file_path[:-4] + "_ocr.txt"
    asr_result = ""
    ocr_result = ""
    with open(asr_file_path, "r") as f:
        asr_result = f.read()
    with open(ocr_file_path, "r") as f:
        ocr_result = f.read()
    video_platform_name = os.path.basename(os.path.dirname(os.path.dirname(video_file_path)))
    video_subdir_name = os.path.basename(os.path.dirname(video_file_path))
    video_file_name = os.path.basename(video_file_path)
    save_video_path = os.path.join(save_dir,video_platform_name, video_subdir_name,video_file_name)
    save_asr_path = save_video_path[:-4] + "_asr.txt"
    save_ocr_path = save_video_path[:-4] + "_ocr.txt"
    if not os.path.exists(os.path.dirname(save_video_path)):
        os.makedirs(os.path.dirname(save_video_path))
    try:
        shutil.move(video_file_path, save_video_path)
        shutil.move(asr_file_path, save_asr_path)
        shutil.move(ocr_file_path, save_ocr_path)
        print("Move save video to save dir")
        # 分析直播商品类别
        good_kind = ""
        # 获取当前时间
        from datetime import datetime
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dao.insert_证据视频(save_video_path, ocr_result, asr_result, result, good_kind, cur_time, liveURL, liveName)
    except shutil.Error as e:
        print(f"Error: {e}")

def analyze_video():
    # 连接到数据库
    conn = sqlite3.connect('DouyinLiveRecorder/file_monitor.db')
    c = conn.cursor()

    # 从数据库中选择未分析的文件
    c.execute("SELECT * FROM files WHERE isAnalyzed=?", (False,))
    files_to_analyze = c.fetchall()

    # 分析文件
    for file_data in files_to_analyze:
        filepath, liveName, liveURL, timestamp, _ = file_data
        # 在这里执行文件分析的操作
        print(f"Analyzing file: {filepath}")
        asr_txt, ocr_txt = video_to_txt(filepath)
        live_txt = asr_txt + "\n" + ocr_txt
        result = match.text_analysis(live_txt)
        print(result)
        # 如果该直播视频段落为正常视频 且 不保存正常视频，那么删除该直播
        if result["type"] == "0" and is_keep_normal_live_video != "是":
            remove_video(filepath)
        # 否则，将该直播视频内容保存至线索库
        else:
            save_video(filepath, liveName, liveURL, str(result))

        # 将文件状态标记为已分析
        c.execute("UPDATE files SET isAnalyzed=? WHERE filepath=?", (True, filepath))
        conn.commit()

    # 关闭数据库连接
    conn.close()

if __name__ == "__main__":
    time.sleep(30)
    while True:
        time.sleep(segment_time)
        analyze_video()

