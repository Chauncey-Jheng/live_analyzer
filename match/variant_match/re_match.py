import re
import itertools
# 读取敏感词库文件的函数
# def read_sensitive_words(file_path):
#     with open(file_path, 'r', encoding="utf-8") as file:
#         return [line.strip() for line in file.readlines()]

# 敏感词库文件路径
# sensitive_words_file_path = 'text_analysis\\违禁词表.txt'

# 从文件读取敏感词库
# sensitive_words = read_sensitive_words(sensitive_words_file_path)
sensitive_words = ["最","临床"]
# 变体词正则表达式
# variant_patterns = [
#     r'[\u4e00-\u9fa5]某[\u4e00-\u9fa5]',  # *某* 形式
#     r'[\u4e00-\u9fa5]什么[\u4e00-\u9fa5]' # *什么* 形式
# ]
# 更新变体词正则表达式
# variant_patterns = [
#     r'([\u4e00-\u9fa5]+)某([\u4e00-\u9fa5]+)',  # *某* 形式
#     r'([\u4e00-\u9fa5]+)什么([\u4e00-\u9fa5]+)', # *什么* 形式
#     r'([\u4e00-\u9fa5]+)小([\u4e00-\u9fa5]+)' #*小* 形式#
# ]

variant_class = ['某', '什么', '小']

variant_patterns = [f'([\u4e00-\u9fa5]+){i}([\u4e00-\u9fa5]+)' for i in variant_class]

def detect_complex_variant_words_in_sensitive(text):
    ''' 检测并处理变体词(要求对应的原词在敏感词库中)'''
    # print("原始输入为：", text)
    detected_variants = []
    for ind, pattern in enumerate(variant_patterns):
        matches = re.finditer(pattern, text)
        for match in matches:
            before_words = match.group(1).split()
            after_words = match.group(2).split()
            before_words_list = list(before_words[0])[-2:]
            after_words_list = list(after_words[0])[:2]
            # 生成所有可能的词组合
            for i in range(1, len(before_words_list)+1):
                for j in range(1, len(after_words_list)+1):
                    for before_combo in itertools.combinations(before_words_list, i):
                        for after_combo in itertools.combinations(after_words_list, j):
                            combined_word = ''.join(before_combo + after_combo)
                            if combined_word in sensitive_words:
                                variants = ''.join(before_combo + tuple(variant_class[ind]) + after_combo)
                                words_pair = (variants, combined_word)
                                detected_variants.append(words_pair)
    return detected_variants

def detect_complex_variant_words(text):
    '''监测并处理变体词'''
    # print("原始输入为：", text)
    detected_variants = []
    for ind, pattern in enumerate(variant_patterns):
        matches = re.finditer(pattern, text)
        for match in matches:
            before_words = match.group(1).split()
            after_words = match.group(2).split()
            # 仅取特殊字符前后各两个字
            before_words_list = list(before_words[0])[-2:]
            after_words_list = list(after_words[0])[:2]
            # 生成所有可能的词组合
            for i in range(1, len(before_words_list)+1):
                for j in range(1, len(after_words_list)+1):
                    for before_combo in itertools.combinations(before_words_list, i):
                        for after_combo in itertools.combinations(after_words_list, j):
                            variants = ''.join(before_combo + tuple(variant_class[ind]) + after_combo)
                            if variants in text:
                                combined_word = ''.join(before_combo + after_combo)
                                words_pair = (variants, combined_word)
                                detected_variants.append(words_pair)
    if len(detected_variants) == 0:
        return None
    match_case = detected_variants[0]
    variant_word = match_case[0]
    origin_word = match_case[1]
    result = {"变体词":variant_word, "原词":origin_word}
    return result

if __name__ == "__main__":
    # 测试文本
    test_text = ["这个产品是最什么受欢迎的", "这对咱们的心脑小管疾病都是有治疗效果的啊","这个的效果在临某床上已经得到验证了","foobar"]
    # 运行检测
    for text in test_text:
        print("原始文本：", text)
        detected_variants = detect_complex_variant_words(text)
        print(detected_variants)