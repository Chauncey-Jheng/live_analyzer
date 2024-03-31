# 从数据库中读取敏感词列表
from dao.dao import DAO
dao = DAO()

禁限售 = dao.get_禁限售()

# 从数据库中读取禁售物品列表
ban_sale_goods = [i[1] for i in 禁限售 if i[0] == "禁售"]

# 从数据库中读取限售物品列表
limit_sale_goods = [i[1] for i in 禁限售 if i[0] == "限售"]

def match_ban_limit_goods(text:str):
    '''将禁售限售商品逐个与输入的语句进行匹配'''

    result = {}
    result["type"] = 0
    result['content'] = None
    for good in ban_sale_goods:
        if good in text:
            result["type"] = 3
            result["content"] = {"类型":"禁售","商品":good}
            return result
    for good in limit_sale_goods:
        if good in text:
            result["type"] = 3
            result["content"] = {"类型":"限售","商品":good}
            return result
    return result