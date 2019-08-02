import jieba
jieba.load_userdict("./legal_word.txt")
word_list = jieba.cut("我今天不处理逾期信用贷款，因为你们的按份赔偿责任有毒")
print("|".join(word_list))