# 从数据库中读取敏感词列表
sensitive_words = ["最","临床"]

def match_sensitive_word(text:str):
    '''将敏感词逐个与输入的语句进行匹配'''

    result = {}
    result["type"] = 0
    for word in sensitive_words:
        if word in text:
            result["type"] = 1
            result["content"] = {"通用敏感词":word}
            return result
    return result