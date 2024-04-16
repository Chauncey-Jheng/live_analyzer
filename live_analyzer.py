
import time
import os
import shutil
from match import match
from category_recognize import category_recognize

from asr.kaldi_asr import run_kaldi_asr
from ocr.paddle_ocr import run_paddle_ocr

from dao.dao import DAO
dao = DAO()

import configparser
config_file = './config.ini'
encoding = 'utf-8-sig'
config = configparser.RawConfigParser()
config.read(config_file, encoding=encoding)
is_keep_normal_live_video = config.get('视频分析配置','是否保留正常内容视频')
is_open_category_recognize = config.get('视频分析配置','是否开启视频商品分类')
save_dir = config.get('视频分析配置','线索视频保存地址')
clue_queue_len = int(config.get('视频分析设置','暂存线索队列最大长度'))
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
        good_kind = None
        if is_open_category_recognize == "是":
            good_kind = category_recognize.recognize_category(liveName, asr_result+'\n'+ocr_result)
        else:
            good_kind = None
        # 获取当前时间
        from datetime import datetime
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dao = DAO()
        dao.insert_证据视频(save_video_path, ocr_result, asr_result, result, good_kind, cur_time, liveURL, liveName)
        dao.close()
    except shutil.Error as e:
        print(f"Error: {e}")

# 线索暂存队列，该队列用处是用来防止保存一个直播中过多相同的线索视频
clue_queue = []

def analyze_video():
    '''
    逐个分析直播视频，生成证据视频线索
    '''
    # 连接到待分析直播视频池
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
            # 如果当前队列数量未满，则直接将线索加入队列，并保存视频
            if len(clue_queue) < clue_queue_len:
                clue_queue.append(result)
                save_video(filepath, liveName, liveURL, str(result))
            # 若线索暂存队列已满
            else:
                # 如果当前线索与线索暂存队列中任一线索存在不同，则弹出队列首部线索，并将当前线索加入队列尾部
                for clue in clue_queue:
                    if clue != result:
                        clue_queue.pop(0)
                        clue_queue.append(result)
                        save_video(filepath, liveName, liveURL, str(result))
                        break
                # 如果当前线索与线索暂存队列中任一线索均相同，那么则可以认为该线索重复了，不保存
                remove_video(filepath)

        # 将文件状态标记为已分析
        c.execute("UPDATE files SET isAnalyzed=? WHERE filepath=?", (True, filepath))
        conn.commit()

    # 关闭数据库连接
    conn.close()


def analyze_video_with_accumulate_for_variant():
    '''
    累积式分析视频，用于分析获取变体词
    '''
    from match.variant_match import llm_match
    from match.variant_match import re_match
    from match.variant_match import corrector_match

    llm_match_accumulate_time = 300 # 单位：秒
    corrector_match_accumulate_time = 120
    re_match_accumulate_time = 60

    llm_match_cnt_max = llm_match_accumulate_time // segment_time
    corrector_match_cnt_max = corrector_match_accumulate_time // segment_time
    re_match_cnt_max = re_match_accumulate_time // segment_time

    llm_match_cnt = 0
    corrector_match_cnt = 0
    re_match_cnt = 0

    accumulate_live_txt_for_llm = ''
    accumulate_live_txt_for_corrector = ''
    accumulate_live_txt_for_re = ''

    # 连接到待分析直播视频池
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
        accumulate_live_txt_for_llm += live_txt
        accumulate_live_txt_for_corrector += live_txt
        accumulate_live_txt_for_re += live_txt
        re_match_cnt += 1
        corrector_match_cnt += 1
        llm_match_cnt += 1

        if re_match_cnt >= re_match_cnt_max:
            result = re_match.detect_complex_variant_words(accumulate_live_txt_for_re)
            print(result)
            if result != None:
                变体词 = result["变体词"]
                原词 = result["原词"]
                发现方式 = '正则表达式'
                dao.insert_专项变体词(变体词,原词,发现方式)
                re_match_cnt = 0
                accumulate_live_txt_for_re = ''

        if corrector_match_cnt >= corrector_match_cnt_max:
            result = corrector_match.match(accumulate_live_txt_for_corrector)
            print(result)
            if result != None:
                变体词 = result["变体词"]
                原词 = result["原词"]
                发现方式 = '统计语言模型'
                dao.insert_专项变体词(变体词,原词,发现方式)
                corrector_match_cnt = 0
                accumulate_live_txt_for_corrector = ''

        if llm_match_cnt >= llm_match_cnt_max:
            result = llm_match.variant_word_match_with_llama(accumulate_live_txt_for_llm)
            print(result)
            if result != None:
                变体词 = result["变体词"]
                原词 = result["原词"]
                发现方式 = '大模型'
                dao.insert_专项变体词(变体词,原词,发现方式)
                llm_match_cnt = 0
                accumulate_live_txt_for_llm = ''


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

