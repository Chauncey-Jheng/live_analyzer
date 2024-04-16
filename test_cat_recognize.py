def test_category_recognize_by_history():
    test_example = [
        "自然堂"
        ]
    from category_recognize import category_recognize_by_history
    for i in test_example:
        result = category_recognize_by_history.recognize_category_by_history(i)
        print(result)

def test_category_recognize_by_llm():
    test_example = [
        "抖音商城年货节 59.9元 89.9 358元 50g 抗波·面霜 抖音官方旗舰店 自然美椰要 有模有漾 全国 过敏 假 包邮 包退 赔四 ",
        "刀你涂了也拉拉菲产品对不对是的那这个要链接是不是又没了没没有了这个要零件学会了姐妹我们就去按照小董说的这个方式去用就可以了如果才有自己没有拍到的还想不想要今天直播间这个机制真的划算",
    ]
    def test_spark():
        from category_recognize import category_recognize_by_llm
        for i in test_example:
            result = category_recognize_by_llm.category_recognize_with_spark(i)
            print(result)
    def test_llama():
        from category_recognize import category_recognize_by_llm
        for i in test_example:
            result = category_recognize_by_llm.category_recognize_with_llama(i)
            print(result)
    
    # print("spark测试结果:")
    # test_spark()

    print("llama测试结果")
    test_llama()

if __name__ == "__main__":
    test_category_recognize_by_history()
    test_category_recognize_by_llm()