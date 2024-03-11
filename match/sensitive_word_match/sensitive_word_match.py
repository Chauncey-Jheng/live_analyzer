# 从数据库中读取敏感词列表
from dao.dao import DAO
dao = DAO()

# sensitive_words = ["最","临床"]
sensitive_words = [i[0] for i in dao.get_通用敏感词()]

def match_sensitive_word(text:str):
    '''将敏感词逐个与输入的语句进行匹配'''

    result = {}
    result["type"] = 0
    result["content"] = None
    for word in sensitive_words:
        if word in text:
            result["type"] = 1
            result["content"] = {"通用敏感词":word}
            return result
    return result