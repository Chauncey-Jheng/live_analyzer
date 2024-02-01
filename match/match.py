if __name__ == "__main__":
    from sensitive_word_analyzer import sensitive_word_match
    from variant_analyzer import hierarchical_match
else:
    from match.sensitive_word_analyzer import sensitive_word_match
    from match.variant_analyzer import hierarchical_match

def text_analysis(txt:str):
    "视频文本内容分析匹配"
    sensitive_word_match_result = sensitive_word_match.match_sensitive_word(txt)
    if sensitive_word_match_result["type"] != 0:
        return sensitive_word_match_result
    variant_match_result = hierarchical_match.hierarchical_analysis(txt)
    if variant_match_result["type"] != 0:
        return variant_match_result
    result = {}
    result["type"] = 0
    return result

if __name__ == "__main__":
    # 测试文本
    test_text = ["这个产品是最什么受欢迎的", "这对咱们的心脑小管疾病都是有治疗效果的啊","这个的效果在临某床上已经得到验证了"]
    # 运行检测
    for text in test_text:
        print("原始文本：", text)
        result = text_analysis(text)
        print(result)