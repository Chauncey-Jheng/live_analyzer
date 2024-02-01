if __name__ == "__main__":
    import llm_match
    import re_match
else:
    from match.variant_analyzer import llm_match
    from match.variant_analyzer import re_match

def hierarchical_analysis(text:str):
    '''层级式分析变体词'''
    result = {}
    result["type"] = 0
    re_match_result = re_match.detect_complex_variant_words_in_sensitive(text)
    if len(re_match_result) != 0:
        result["type"] = 2 # 存在变体词
        result["content"] = {"匹配对":str(re_match_result),"匹配方式":"正则表达式"}
    else:
        llm_match_result = llm_match.variant_word_match(text)
        if len(llm_match_result) != 0:
            result["type"] = 2
            result["content"] = {"匹配对":str(llm_match_result),"匹配方式":"大模型"}
    return result

if __name__ == "__main__":
    # 测试文本
    test_text = ["这个产品是最什么受欢迎的", "这对咱们的心脑小管疾病都是有治疗效果的啊","这个的效果在临某床上已经得到验证了"]
    # 运行检测
    for text in test_text:
        print("原始文本：", text)
        result = hierarchical_analysis(text)
        print(result)
