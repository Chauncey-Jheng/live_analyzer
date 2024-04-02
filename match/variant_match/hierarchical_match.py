from . import llm_match
from . import re_match
from . import corrector_match

from dao.dao import DAO
dao = DAO()

import configparser
config_file = './match/config.ini'
encoding = 'utf-8-sig'

def hierarchical_analysis(text:str):
    '''层级式分析变体词'''

    config = configparser.RawConfigParser()
    config.read(config_file, encoding=encoding)
    is_open_re_match = config.get('变体词匹配设置','是否开启正则表达式匹配')
    is_open_corrector_match = config.get('变体词匹配设置','是否开启统计语言模型匹配')
    is_open_llm_match = config.get('变体词匹配设置','是否开启大模型匹配')

    result = {}
    result["type"] = 0
    result["content"] = None
    
    if(is_open_re_match == '是'):
        re_match_result = re_match.detect_complex_variant_words(text)
        if re_match_result != None:
            变体词 = re_match_result["变体词"]
            原词 = re_match_result["原词"]
            dao.insert_专项变体词(变体词,原词)
            result["type"] = 2 # 存在变体词
            result["content"] = {"匹配对":re_match_result,"匹配方式":"正则表达式"}
            return result
    
    if(is_open_corrector_match == '是'):
        corrector_match_result = corrector_match.kenlm_match(text)
        if corrector_match_result != None:
            变体词 = corrector_match_result["变体词"]
            原词 = corrector_match_result["原词"]
            dao.insert_专项变体词(变体词,原词)
            result["type"] = 2
            result["content"] = {"匹配对":corrector_match_result,"匹配方式":"统计语言模型"}
            return result

    if(is_open_llm_match == '是'):
        llm_match_result = llm_match.variant_word_match(text)
        if llm_match_result != None:
            变体词 = llm_match_result["变体词"]
            原词 = llm_match_result["原词"]
            dao.insert_专项变体词(变体词,原词)
            result["type"] = 2
            result["content"] = {"匹配对":llm_match_result,"匹配方式":"大模型"}
            return result

    return result

if __name__ == "__main__":
    # 测试文本
    test_text = ["这个产品是最什么受欢迎的", "这对咱们的心脑小管疾病都是有治疗效果的啊","这个的效果在临某床上已经得到验证了"]
    # 运行检测
    for text in test_text:
        print("原始文本：", text)
        result = hierarchical_analysis(text)
        print(result)
