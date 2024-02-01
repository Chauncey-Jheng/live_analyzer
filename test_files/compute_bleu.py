import nltk
from nltk.translate.bleu_score import sentence_bleu
nltk.download('punkt')
# 原始参考文本
reference = ["这是参考文本。"]

# 生成的文本
candidate = "这是生成的文本。"

# 将参考文本和生成文本分词
reference_tokens = [nltk.word_tokenize(ref.lower()) for ref in reference]
candidate_tokens = nltk.word_tokenize(candidate.lower())

# 计算BLEU-1
bleu_1 = sentence_bleu(reference_tokens, candidate_tokens, weights=(1, 0, 0, 0))
print(f"BLEU-1分数：{bleu_1}")

# 计算BLEU-2
bleu_2 = sentence_bleu(reference_tokens, candidate_tokens, weights=(0.5, 0.5, 0, 0))
print(f"BLEU-2分数：{bleu_2}")

# 计算BLEU-3
bleu_3 = sentence_bleu(reference_tokens, candidate_tokens, weights=(0.33, 0.33, 0.33, 0))
print(f"BLEU-3分数：{bleu_3}")

# 计算BLEU-4
bleu_4 = sentence_bleu(reference_tokens, candidate_tokens, weights=(0.25, 0.25, 0.25, 0.25))
print(f"BLEU-4分数：{bleu_4}")
