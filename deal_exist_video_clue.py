# 逐个读取每个敏感视频的asr和ocr结果，并将其整合为一个str
# 将这个str文件用match进行匹配
# 将生成的结果存放入csv文件中

import os
import json

from match import match
from category_recognize import category_recognize_by_llm

from dao.dao import DAO
from tqdm import tqdm
import random
dao = DAO()


def deal_exist_video_clue_v1():
    walk = os.walk("/media/sf_share/sensitive_live_data")
    cnt = 0
    for path,dirs,files in walk:
        for file in files:
            if file[-3:] == "flv":
                origin_name = file[:-23]
                time_name = file[-23:-4]
                asr_file_path = path + '/' + origin_name + "_asr" + time_name + ".txt"
                ocr_file_path = path + '/' + origin_name + "_ocr" + time_name + ".txt"
                try:
                    with open(asr_file_path, 'r',encoding='GBK') as f:
                        asr_txt = f.read()
                    with open(ocr_file_path, 'r',encoding='GBK') as f:
                        ocr_txt = f.read()
                    txt = asr_txt + ' ' + ocr_txt
                    result = match.text_analysis(txt)
                    # category = category_recognize.category_recognize(txt) 
                    category = None
                    print("result:",result)
                    print("category:",category)
                    result_json = str(result)
                    video_path = path + '/' + file
                    dao.insert_证据视频(video_path,ocr_txt,asr_txt,result_json,category,time_name,"",origin_name)
                    print("insert finish")
                    cnt += 1
                
                except:
                    continue

    print(cnt)

def findout_current_live_name():
    fields = dao.get_字段名("证据视频")
    clues = dao.get_证据视频()
    live_names = set([clue[fields.index("直播间名称")][:-9] for clue in clues])
    print(live_names)

def findout_current_live_kind():
    fields = dao.get_字段名("证据视频")
    clues = dao.get_证据视频()
    live_kinds = [clue[fields.index("商品类别")] for clue in clues]
    from collections import Counter
    count = Counter(live_kinds)
    print(count)

def add_variant_clue():
    """
    不要求变体词原词属于通用敏感词,从标记正常的样本中识别可能存在的变体词
    """
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    for clue in tqdm(clues):
        content = eval(clue[fields.index("线索内容")])
        if content["type"] == 0:
            if(random.random() < 0.45):
                text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
                result = match.text_analysis(text)
                clue = list(clue)
                clue[fields.index("线索内容")] = str(result)
                dao.insert_证据视频(clue[fields.index("视频文件地址")],
                                clue[fields.index("视频ocr结果")],
                                clue[fields.index("视频asr结果")],
                                clue[fields.index("线索内容")],
                                clue[fields.index("商品类别")],
                                clue[fields.index("获取时间")],
                                clue[fields.index("直播间链接")],
                                clue[fields.index("直播间名称")])

def add_variant_clue_from_T5():
    """
    对已用kenlm识别出的变体词，再次使用T5模型进行识别
    """
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    for clue in tqdm(clues):
        content = eval(clue[fields.index("线索内容")])
        if content["type"] == 2:
            if(random.random() < 0.23):
                text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
                result = match.text_analysis(text)
                clue = list(clue)
                clue[fields.index("线索内容")] = str(result)
                dao.insert_证据视频(clue[fields.index("视频文件地址")],
                                clue[fields.index("视频ocr结果")],
                                clue[fields.index("视频asr结果")],
                                clue[fields.index("线索内容")],
                                clue[fields.index("商品类别")],
                                clue[fields.index("获取时间")],
                                clue[fields.index("直播间链接")],
                                clue[fields.index("直播间名称")])


def deal_exist_video_clue_v2():
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    for clue in tqdm(clues):
        text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
        result = match.text_analysis(text)
        live_name = clue[fields.index("直播间名称")]
        good_kind = ""
        化妆品_set = ["makeup","arslan","SKIN","Carslan","carslan","SOCORSKIN","skin"]
        保健品_set = ["health","fish","product","bah","fishoil"]
        药品_set = ["medicine",]
        医疗器械_set = ["device","medical"]
        for i in 化妆品_set:
            if i in live_name:
                good_kind = "化妆品"
        for i in 保健品_set:
            if i in live_name:
                good_kind = "保健品"
        for i in 药品_set:
            if i in live_name:
                good_kind = "药品"
        for i in 医疗器械_set:
            if i in live_name:
                good_kind = "医疗器械"

        dao.update_证据视频_线索内容_by_path(clue[fields.index("视频文件地址")],str(result))
        # dao.update_证据视频_商品类别_by_path(clue[fields.index("视频文件地址")],good_kind)

if __name__ == "__main__":
    # findout_current_live_name()
    # deal_exist_video_clue_v2()
    # findout_current_live_kind()
    # add_variant_clue()
    add_variant_clue_from_T5()