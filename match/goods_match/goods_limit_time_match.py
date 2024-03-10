# 从数据库中读取所有的商品名称列表,列表中每一个元素都为一个二元组，二元组为（商品名称，有效时间）
goods_with_limit_time = []



def match_goods_limit_time(text:str):
    '''将敏感词逐个与输入的语句进行匹配'''

    result = {}
    result["type"] = 0
    result['content'] = None
    for good_with_time in goods_with_limit_time:
        goods_name = good_with_time[0]
        limit_time = good_with_time[1]
        import time
        current_time = time.time()
        if goods_name in text and limit_time < current_time:
            result["type"] = 3
            result["content"] = {"商品":goods_name,"认证到期时间":limit_time}
            return result
    return result