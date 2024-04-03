# 从数据库中读取敏感词列表
from dao.dao import DAO
dao = DAO()

def test_通用敏感词():
    sensitive_words = [i[0] for i in dao.get_通用敏感词()]
    print(sensitive_words)

def test_变体词():
    variant_words = dao.get_专项变体词()
    print(variant_words)
    dao.insert_专项变体词("保某养","保养")
    dao.delete_专项变体词_重复记录()
 
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

def test_证据视频():
    # kind = dao.get_证据视频_商品类别_by_直播间名称("carslan_makeup_12230761")[0]
    # print(kind)
    field = dao.get_字段名("证据视频")
    clues = dao.get_证据视频()
    contents = [eval(clue[field.index("线索内容")]) for clue in clues]
    type_0_cnt = 0
    type_1_cnt = 0
    type_2_cnt = 0
    type_3_cnt = 0
    type_4_cnt = 0
    total_cnt = 0
    for content in contents:
        if content["type"] == 0:
            type_0_cnt += 1
        if content["type"] == 1:
            type_1_cnt += 1
        if content["type"] == 2:
            type_2_cnt += 1
        if content["type"] == 3:
            type_3_cnt += 1
        if content["type"] == 4:
            type_4_cnt += 1
        total_cnt += 1

    print("总视频个数:",total_cnt, 
          "正常视频个数:",type_0_cnt, "占比:",type_0_cnt/total_cnt,
          "敏感词线索视频个数:",type_1_cnt, "占比:",type_1_cnt/total_cnt,
          "变体词线索视频个数:",type_2_cnt, "占比:",type_2_cnt/total_cnt,
          "禁限售线索视频个数:",type_3_cnt, "占比:",type_3_cnt/total_cnt,
          "商品内容矛盾线索视频个数:",type_4_cnt, "占比:",type_4_cnt/total_cnt,)
    
if __name__ == "__main__":
    # test_通用敏感词()
    # test_禁限售()
    # test_保健品()
    # test_证据视频()
    test_变体词()