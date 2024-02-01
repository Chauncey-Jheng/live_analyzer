def test_GptCorrector():
    from pycorrector import GptCorrector
    m = GptCorrector()
    print(m.correct_batch(['我今天心清很好','你找到你喜欢的工作，我也很开芯']))

def test_kenlm():
    from pycorrector import Corrector
    m = Corrector()
    print(m.correct_batch(['我今天心清真不错','你找到你喜欢的工作，我也很开芯']))

if __name__ == "__main__":
    test_kenlm()