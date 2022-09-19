from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
# 目前直接使用stanford预训练好的glove模型, 并转化成word2vec利用gensim进行使用
# https://github.com/maciejkula/glove-python 这里是python实现

glove_input_file = 'D:/EntityMatchingProject/glove.6B.300d.txt'
word2vec_output_file = 'glove.840B.300d.word2vec.txt'

glove2word2vec(glove_input_file, word2vec_output_file)

glove_model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary = False)

cat_vec = glove_model['cat']
# 获取cat的词向量
print(cat_vec.shape)
print(glove_model.most_similar('frog'))



