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
            "最什么便宜的",
            "白某障"
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
            "这种药物的林床笑果非常好",
            "咱们医院里的蚁生都在推荐啊",
            "咱们的欣闹学管疾病等等都是可以治疗啊"
        ]
        print("基于纠错模型的变体词匹配测试样例为：",test_example)
        cur_time = time.time()
        print("基于纠错模型的变体词匹配测试样例测试结果为：")
        for i in test_example:
            result = corrector_match.match(i)
            print(result)
        print("运行kenlm_match,跑完所有测试样例,消耗时间为:", time.time() - cur_time)
    # test_re_match()
    def test_llm_match():
        import time
        cur_time = time.time()
        from match.variant_match import llm_match
        test_example = [
            "这种药物的林床笑果非常好",
            "咱们医院里的蚁生都在推荐啊",
            "咱们的欣闹学管疾病等等都是可以治疗啊",
            "如果不是吃了我们的东西的话啊，他第二天就得去医院找白大褂了, 可见我们的产品具有显著的临某床意义, 对我们的心脑血某管都是很有好处的"
        ]
        print("基于大模型的变体词匹配测试样例为：",test_example)
        cur_time = time.time()
        print("基于大模型的变体词匹配测试结果为：")
        for i in test_example:
            result = llm_match.variant_word_match_with_llama(i)
            print(result)
        print("调用大模型，跑完所有测试样例，消耗时间为：", time.time()-cur_time)
    
    # test_re_match()
    test_correct_match()
    # test_llm_match()

def test_ban_sale_match():
    from match.ban_sale_match import ban_sale_match
    test_example = [
        "国家级的马家窑",
        "春秋时期的瓷器",
        "电捕鱼器材",
        "香烟"
    ]
    print("敏感词匹配测试样例为：",test_example)
    print("敏感词匹配测试结果为:")
    for e in test_example:
        result = ban_sale_match.match_ban_limit_goods(e)
        print(result)

def test_goods_match():
    from match.goods_match import goods_conflict_match
    # print(goods_conflict_match.药品_merged)
    # print(goods_conflict_match.保健品_merged)
    # print(goods_conflict_match.化妆品_merged)
    # print(goods_conflict_match.医疗器械_merged)

    test_example = [
        "感冒清片纯中草药制作阿，不含有任何化学成分",
        "感冒清片非常有用",
        "香烟"
    ]
    print("商品矛盾性检测测试样例为：",test_example)
    print("敏感词匹配测试结果为:")
    for e in test_example:
        result = goods_conflict_match.match_goods_conflict_match(e)
        print(result)

if __name__ == "__main__":
    # test_sensitive_word_match()
    test_variant_match()
    # test_ban_sale_match()
    # test_goods_match()