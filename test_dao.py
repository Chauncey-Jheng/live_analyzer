# 从数据库中读取敏感词列表
from dao.dao import DAO
dao = DAO()

def test_通用敏感词():
    sensitive_words = [i[0] for i in dao.get_通用敏感词()]
    print(sensitive_words)

def test_禁限售():
    ban_sale_goods = dao.get_禁限售()
    禁售_goods = [i[1] for i in dao.get_禁限售() if i[0] == "禁售"]
    限售_goods = [i[1] for i in dao.get_禁限售() if i[0] == "限售"]
    print(ban_sale_goods)
    print(禁售_goods)
    print(限售_goods)

def test_保健品():
    保健品 = dao.get_保健品()
    字段名 = dao.get_字段名("保健品")
    print(保健品)
    print(字段名)

if __name__ == "__main__":
    # test_通用敏感词()
    # test_禁限售()
    test_保健品()