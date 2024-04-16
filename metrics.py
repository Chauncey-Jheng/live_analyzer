from dao.dao import DAO
from match import match
from tqdm import tqdm
from category_recognize import category_recognize_by_llm

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
## 在match设置中要求变体词原词属于敏感词
def calculate_clue_acc():
    dao = DAO()
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    total_cnt = 0
    acc_cnt = 0
    for clue in tqdm(clues):
        text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
        content = eval(clue[fields.index("线索内容")])
        # print(content)
        result = match.text_analysis(text)
        if result == content:
            acc_cnt += 1
        total_cnt += 1
        # print("当前违法线索发现准确率为:", acc_cnt/total_cnt)

    print("违法线索发现准确率为:", acc_cnt/total_cnt)


## 计算变体词相对与ground truth的准确率
    # 在match设置中使用kenlm模型作为纠错模型
    # 在match设置中不要求变体词原词属于敏感词
def calculate_variant_acc():
    dao = DAO()
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    # print(clues)
    variant_total_cnt = 0
    variant_acc_cnt = 0
    for clue in tqdm(clues):
        text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
        content = eval(clue[fields.index("线索内容")])
        # print(content)
        if content['type'] == 2:
            result = match.text_analysis(text)
            variant_total_cnt += 1
            # print("content:",content)
            # print("result:",result)
            if result == content:
                variant_acc_cnt += 1
    print("当前变体词识别准确率为：",variant_acc_cnt/variant_total_cnt)


## 模型分类准确率评估
## 从数据库中读取违法线索发现结果作为ground truth
## 调用match模块对视频进行分析，得到分析结果
## 计算识别结果相对与ground truth的准确率
def calculate_category_recognize_acc():
    dao = DAO()
    fields = dao.get_字段名("证据视频")
    # print(fields)
    clues = dao.get_证据视频()
    clues = list(clues)
    import random
    random.shuffle(clues)
    # print(clues)
    total_cnt = 0
    acc_cnt = 0
    for clue in tqdm(clues[:256]):
        text = clue[fields.index("视频ocr结果")] + clue[fields.index("视频asr结果")]
        kind = clue[fields.index("商品类别")]
        # print(content)
        result = category_recognize_by_llm.category_recognize_with_llama(text)
        total_cnt += 1
        print(text, kind, result, acc_cnt/total_cnt)
        if result == kind:
            acc_cnt += 1
    print("当前商品类别识别准确率为：", acc_cnt/total_cnt)
    
if __name__ == "__main__":
    # calculate_clue_acc()
    # calculate_variant_acc()
    calculate_category_recognize_acc()