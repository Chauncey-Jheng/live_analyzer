import configparser
config_file = './match/config.ini'
encoding = 'utf-8-sig'
config = configparser.RawConfigParser()

from pycorrector import Corrector
m_kenlm = Corrector()
from pycorrector import T5Corrector
m_T5 = T5Corrector()

def match(sentence):
    config.read(config_file, encoding=encoding)
    corrector_kind = config.get('变体词匹配设置','统计语言模型采用')
    if corrector_kind == 'T5':
        result = m_T5.correct(sentence)
    else:
        result = m_kenlm.correct(sentence)
    errors = result['errors']
    if len(errors) == 0:
        return None
    match_case = errors[0]
    variant_word = match_case[0]
    origin_word = match_case[1]
    result = {"变体词":variant_word, "原词":origin_word}
    return result
