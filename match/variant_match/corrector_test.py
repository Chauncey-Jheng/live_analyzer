def test_GptCorrector():
    from pycorrector import GptCorrector
    m = GptCorrector()
    print(m.correct_batch(['我今天心清很好','你找到你喜欢的工作，我也很开芯']))

def test_kenlm():
    from corrector_match import Corrector
    import os
    model_path = os.path.join(os.path.dirname(__file__), ".pycorrector/datasets/zh_giga.no_cna_cmn.prune01244.klm")
    m = Corrector(language_model_path=model_path)
    print(m.correct_batch(['我今天心清真不错','你找到你喜欢的工作，我也很开芯']))

def test_T5():
    from pycorrector import T5Corrector
    m = T5Corrector()
    print(m.correct_batch(['我今天心清真不错','你找到你喜欢的工作，我也很开芯']))
    

if __name__ == "__main__":
    test_kenlm()
    # test_T5()
    # test_GptCorrector()