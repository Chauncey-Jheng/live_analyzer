
import time
import os
import shutil
from match import match
from multiprocessing import Process

from asr.kaldi_asr import run_kaldi_asr
from ocr.paddle_ocr import run_paddle_ocr

from flask import jsonify

sensitive_dir = "static/video/sensitive/"
variant_dir = "static/video/variant/"


def crawl_live():
    '''爬取直播视频'''
    while True:
        crawler.update_config()
        crawler.parallel_download()
        time.sleep(3)

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

cache_video_list = []
def get_cache_videos():
    '''获取当前缓冲区视频名称列表'''
    global cache_video_list
    cache_path = "static/video/record"
    for root, dirs, files in os.walk(cache_path):
        for file in files:
            if file[-3:].lower() == "mp4":
                cache_video_list.append(os.path.join(root,file))

def test():
    from dao.dao import DAO
    dao = DAO()
    get_cache_videos()
    print(cache_video_list)
    video_file_path = cache_video_list[0]
    asr_file_path = video_file_path[:-4] + "_asr.txt"
    ocr_file_path = video_file_path[:-4] + "_ocr.txt"

    video_subdir_name = os.path.basename(os.path.dirname(video_file_path))
    video_file_name = os.path.basename(video_file_path)

    asr_result, ocr_result = video_to_txt(video_file_path)
    txt = asr_result +"\n" + ocr_result
    print(txt)
    result = match.text_analysis(txt)
    print(result)
    # 如果该直播视频段落为正常视频，那么删除该直播
    if(result["type"] == 0):
        try:
            os.remove(video_file_path)
            os.remove(asr_file_path)
            os.remove(ocr_file_path)
            print("Remove normal live video")
        except OSError as e:
            print(f"Error: {e}")

    # 如果该直播视频段落为通用敏感词类型，那么将其转移至对应文件夹下
    elif(result["type"] == 1):
        sensitive_video_path = os.path.join(sensitive_dir,video_subdir_name,video_file_name)
        sensitive_asr_path = sensitive_video_path[:-4] + "_asr.txt"
        sensitive_ocr_path = sensitive_video_path[:-4] + "_ocr.txt"
        if not os.path.exists(os.path.dirname(sensitive_video_path)):
            os.makedirs(os.path.dirname(sensitive_video_path))
        try:
            shutil.move(video_file_path, sensitive_video_path)
            shutil.move(asr_file_path, sensitive_asr_path)
            shutil.move(ocr_file_path, sensitive_ocr_path)
            print("Move sensitive video to sensitive dir")
            dao.insert_证据视频(sensitive_video_path, sensitive_ocr_path, sensitive_asr_path, jsonify(result))
        except shutil.Error as e:
            print(f"Error: {e}")
            
    # 如果该直播视频段落为变体词类型，那么将其转移至对应文件夹下
    elif(result["type"] == 2):
        variant_video_path = os.path.join(variant_dir, video_subdir_name, video_file_name)
        variant_asr_path = variant_video_path[:-4] + "_asr.txt"
        variant_ocr_path = variant_video_path[:-4] + "_ocr.txt"
        if not os.path.exists(os.path.dirname(variant_video_path)):
            os.makedirs(os.path.dirname(variant_video_path))
        try:
            shutil.move(video_file_path, video_file_path)
            shutil.move(asr_file_path, variant_asr_path)
            shutil.move(ocr_file_path, variant_ocr_path)
            print("Move variant video to variant dir")
        except shutil.Error as e:
            print(f"Error: {e}")

def test2():
    video_to_txt("static/video/sensitive/卡姿兰直播间/卡姿兰直播间.mp4")
    video_to_txt("static/video/sensitive/新西兰鱼油世家/新西兰鱼油世家.mp4")
    video_to_txt("static/video/sensitive/AUX奥克斯/AUX奥克斯.mp4")
    video_to_txt("static/video/variant/新西兰鱼油世家/新西兰鱼油世家2.mp4")
    video_to_txt("static/video/variant/新西兰鱼油世家/新西兰鱼油世家3.mp4")
    video_to_txt("static/video/variant/新西兰鱼油世家/新西兰鱼油世家4.mp4")


if __name__ == "__main__":
    # p = Process(target=crawl_live)
    # p.start()
    from crawler import crawler
    # test()
    test2()
