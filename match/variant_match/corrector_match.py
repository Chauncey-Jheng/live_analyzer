from pycorrector import Corrector
m = Corrector()

def kenlm_match(sentence):
    kenlm_result = m.correct(sentence)
    errors = kenlm_result['errors']
    if len(errors) == 0:
        return None
    match_case = errors[0]
    variant_word = match_case[0]
    origin_word = match_case[1]
    result = {"变体词":variant_word, "原词":origin_word}
    return result
