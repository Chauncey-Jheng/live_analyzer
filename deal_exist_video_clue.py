# 逐个读取每个敏感视频的asr和ocr结果，并将其整合为一个str
# 将这个str文件用match进行匹配
# 将生成的结果存放入csv文件中

import os
import json

from match import match
from category_recognize import category_recognize

from dao.dao import DAO
dao = DAO()


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
                category = category_recognize.category_recognize(txt)
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