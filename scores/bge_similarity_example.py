from pprint import pprint
from sentence_transformers import SentenceTransformer, util

model_path = "/home/kdzlys/data-disk/sjj/bge-large-zh-v1.5"
model = SentenceTransformer(model_path)

# Single list of sentences
sentences = ['猫猫坐在门口',
             '一个男人在弹吉他',
             '我喜欢披萨',
             '新电影好好看啊',
             '猫猫在花园里面玩',
             '一个女人在看电影',
             '新电影真不错',
             '你喜欢披萨吗？']

pprint(model.encode(sentences, convert_to_tensor=True))

#Compute embeddings
embeddings = model.encode(sentences, convert_to_tensor=True)

#Compute cosine-similarities for each sentence with each other sentence
cosine_scores = util.cos_sim(embeddings, embeddings)

#Find the pairs with the highest cosine similarity scores
pairs = []
for i in range(len(cosine_scores)-1):
    for j in range(i+1, len(cosine_scores)):
        pairs.append({'index': [i, j], 'score': cosine_scores[i][j]})

#Sort scores in decreasing order
pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)

for pair in pairs[0:10]:
    i, j = pair['index']
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[i], sentences[j], pair['score']))