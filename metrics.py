from dao.dao import DAO
from match import match

## OCR准确率评估
## 从数据库中读取OCR识别结果作为ground truth
## 调用OCR模型对视频进行识别,得到识别结果
## 计算识别结果相对与ground truth的准确率


## ASR准确率评估
## 从数据库中读取ASR识别结果作为ground truth
## 调用ASR模型对视频进行识别,得到识别结果
## 计算识别结果相对与ground truth的准确率


## 违法线索发现准确率评估
## 从数据库中读取违法线索发现结果作为ground truth
## 调用match模块对视频进行分析，得到分析结果
## 计算识别结果相对与ground truth的准确率
def calculate_clue_acc():
    dao = DAO()
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    total_cnt = 0
    acc_cnt = 0
    variant_total_cnt = 0
    variant_acc_cnt = 0
    for clue in clues:
        text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
        content = eval(clue[fields.index("线索内容")])
        # print(content)
        result = match.text_analysis(text)
        if content['type'] == 2:
            variant_total_cnt += 1
            print("content:",content)
            print("result:",result)
            if result == content:
                variant_acc_cnt += 1
            print("当前变体词识别准确率为：",variant_acc_cnt/variant_total_cnt)
        if result == content:
            acc_cnt += 1
        total_cnt += 1
        print("当前违法线索发现准确率为:", acc_cnt/total_cnt)

    print("违法线索发现准确率为:", acc_cnt/total_cnt)
    print("变体词识别准确率为：",variant_acc_cnt/variant_total_cnt)


## 变体词识别准确率评估
## 从数据库中读取ASR识别结果作为ground truth
## 调用ASR模型对视频进行识别,得到识别结果
## 计算识别结果相对与ground truth的准确率


## 模型分类准确率评估
## 从数据库中读取违法线索发现结果作为ground truth
## 调用match模块对视频进行分析，得到分析结果
## 计算识别结果相对与ground truth的准确率
    
if __name__ == "__main__":
    calculate_clue_acc()