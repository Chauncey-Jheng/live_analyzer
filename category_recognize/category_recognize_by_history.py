# 通过已知的历史直播间名称确定商品类别
from dao.dao import DAO
dao = DAO()

def recognize_category_by_history(live_name:str):
    kind = dao.get_证据视频_商品类别_by_直播间名称(live_name)[0]
    return kind
    

