from . import llm_match
from . import re_match
from . import corrector_match

from dao.dao import DAO
dao = DAO()
sensitive_words = [i[0] for i in dao.get_通用敏感词()]

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
    is_variant_origin_is_sensitive = config.get('变体词匹配设置','是否要求原词属于敏感词')
    llm_name = config.get('变体词匹配设置','大语言模型采用')

    result = {}
    result["type"] = 0
    result["content"] = None
    
    if(is_open_re_match == '是'):
        re_match_result = re_match.detect_variant_words_in_database(text)
        if re_match_result != None:
            发现方式 = '正则表达式'
            result["type"] = 2 # 存在变体词
            result["content"] = {"匹配对":re_match_result,"匹配方式":发现方式}
            return result
        re_match_result = re_match.detect_complex_variant_words(text)
        if re_match_result != None:
            变体词 = re_match_result["变体词"]
            原词 = re_match_result["原词"]
            发现方式 = '正则表达式'
            if 原词 not in sensitive_words and is_variant_origin_is_sensitive == "是":
                return result
            dao.insert_专项变体词(变体词,原词,发现方式)
            result["type"] = 2 # 存在变体词
            result["content"] = {"匹配对":re_match_result,"匹配方式":发现方式}
            return result
        
    if(is_open_corrector_match == '是'):
        corrector_match_result = corrector_match.match(text)
        if corrector_match_result != None:
            变体词 = corrector_match_result["变体词"]
            原词 = corrector_match_result["原词"]
            发现方式 = '统计语言模型'
            if 原词 not in sensitive_words and is_variant_origin_is_sensitive == "是":
                return result
            dao.insert_专项变体词(变体词,原词,发现方式)
            result["type"] = 2
            result["content"] = {"匹配对":corrector_match_result,"匹配方式":发现方式}
            return result

    if(is_open_llm_match == '是'):
        llm_match_result = None
        if llm_name == "spark":
            llm_match_result = llm_match.variant_word_match_with_spark(text)
        elif llm_name == "llama":
            llm_match_result = llm_match.variant_word_match_with_llama(text)
        if llm_match_result != None:
            变体词 = llm_match_result["变体词"]
            原词 = llm_match_result["原词"]
            发现方式 = '大模型'
            if 原词 not in sensitive_words and is_variant_origin_is_sensitive == "是":
                return result
            dao.insert_专项变体词(变体词,原词,发现方式)
            result["type"] = 2
            result["content"] = {"匹配对":llm_match_result,"匹配方式":发现方式}
            return result

    return result