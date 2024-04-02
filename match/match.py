# import sys
# sys.path.append("match/ban_sale_match/")
# sys.path.append("match/goods_match/")
# sys.path.append("match/sensitive_word_match/")
# sys.path.append("match/variant_match/")
# import sensitive_word_match
# import hierarchical_match
# import ban_sale_match
# import goods_conflict_match

from .sensitive_word_match import sensitive_word_match
from .variant_match import hierarchical_match
from .ban_sale_match import ban_sale_match
from .goods_match import goods_conflict_match

import configparser
config_file = './match/config.ini'
encoding = 'utf-8-sig'

def text_analysis(txt:str):
    "视频文本内容分析匹配"

    config = configparser.RawConfigParser()
    config.read(config_file, encoding=encoding)
    is_open_sensitive_word_match = config.get('总体匹配设置','是否开启敏感词匹配')
    is_open_variant_match = config.get('总体匹配设置','是否开启变体词匹配')
    is_open_bansale_match = config.get('总体匹配设置','是否开启禁限售匹配')
    is_open_goods_match = config.get('总体匹配设置','是否开启商品内容匹配')

    result = {}
    result["type"] = 0
    result["content"] = None

    if(is_open_sensitive_word_match == '是'):
        sensitive_word_match_result = sensitive_word_match.match_sensitive_word(txt)
        if sensitive_word_match_result["type"] != 0:
            return sensitive_word_match_result
    
    if(is_open_variant_match == '是'):
        variant_match_result = hierarchical_match.hierarchical_analysis(txt)
        if variant_match_result["type"] != 0:
            return variant_match_result
    
    if(is_open_bansale_match == '是'):
        ban_sale_match_result = ban_sale_match.match_ban_limit_goods(txt)
        if ban_sale_match_result['type'] != 0:
            return ban_sale_match_result
    
    if(is_open_goods_match == '是'):
        goods_match_result = goods_conflict_match.match_goods_conflict_match(txt)
        if goods_match_result['type'] != 0:
            return goods_match_result

    return result