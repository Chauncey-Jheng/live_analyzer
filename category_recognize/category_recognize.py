from . import category_recognize_by_llm
from . import category_recognize_by_history

import configparser
config_file = './category_recognize/config.ini'
encoding = 'utf-8-sig'

def recognize_category(live_name:str, content:str):
    '''
    用于识别商品类别;
    live_name 为 直播间名称;
    content 为 直播视频片段文本内容
    '''
    config = configparser.RawConfigParser()
    config.read(config_file, encoding=encoding)
    is_open_cat_recognize_by_history = config.get('商品类别识别设置','是否开启根据历史记录中直播间名称判定类别')
    is_open_cat_recognize_by_llm = config.get('商品类别识别设置','是否开启根据大模型判定商品类别')

    kind = None
    if is_open_cat_recognize_by_history == "是":
        kind = category_recognize_by_history.recognize_category_by_history(live_name)
    if is_open_cat_recognize_by_llm == "是" and kind == None:
        kind = category_recognize_by_llm.category_recognize(content)
    return kind
