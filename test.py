# test sensitive_word_match
def test_sensitive_word_match():
    from match.sensitive_word_match import sensitive_word_match
    test_example = [
        "国家级的",
        "最厉害的"
    ]
    print("敏感词匹配测试样例为：",test_example)
    print("敏感词匹配测试结果为:")
    for e in test_example:
        result = sensitive_word_match.match_sensitive_word(e)
        print(result)

# test variant_match
def test_variant_match():
    def test_re_match():
        from match.variant_match import re_match
        test_example = [
            "临某床",
            "鱼什么油",
            "最什么便宜的"
        ]
        print("基于正则表达式的变体词匹配测试样例为：",test_example)

        print("基于正则表达式的变体词匹配测试，不要求变体词原词属于通用敏感词，测试结果为：")
        for i in test_example:
            result = re_match.detect_complex_variant_words(i)
            print(result)

        print("基于正则表达式的变体词匹配测试，要求变体词原词属于通用敏感词，测试结果为：")
        for i in test_example:
            result = re_match.detect_complex_variant_words_in_sensitive(i)
            print(result)

    def test_correct_match():
        import time
        cur_time = time.time()
        from match.variant_match import corrector_match
        print("引入corrector_match消耗时间为:", time.time() - cur_time)
        cur_time = time.time()

        test_example = [
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错",
            "我今天心清真不错我今天心清真不错我今天心清真不错我今天心清真不错"
        ]
        print("基于纠错模型的变体词匹配测试样例为：",test_example)
        cur_time = time.time()
        print("基于正则表达式的变体词匹配测试，不要求变体词原词属于通用敏感词，测试结果为：")
        for i in test_example:
            result = corrector_match.kenlm_match(i)
            print(result)
        print("运行kenlm_match,跑完所有测试样例,消耗时间为:", time.time() - cur_time)
    # test_re_match()
    test_correct_match()

if __name__ == "__main__":
    # test_sensitive_word_match()
    test_variant_match()