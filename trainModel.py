from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import nltk
import corpus



#text = nltk.corpus.gutenberg.sents('melville-moby_dick.txt')

text = corpus.llista

text = [[w] for sub in text for w in sub]

l = []
for s in text:
    input = nltk.word_tokenize(str(s).lower())
    l.append(input)

print(l)
#print(text)
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(l)]

#print(common_texts)
#documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]

#print(len(text))
model = Doc2Vec(documents)
#, vector_size=5, window=2, min_count=1, workers=4

#model.save("models/doc2vec_model")
#model = Doc2Vec.load("models/doc2vec_model")  # you can continue training with the loaded model!
#print(model.most_similar(['Emma']))


input = nltk.word_tokenize("Proleukin".lower())
input_v = model.infer_vector(input)

#sentences = [ " ".join(w) for w in text]
print(text[:5])
llista = []
for sen in text:
    v = model.infer_vector(sen)
    llista.append(v)


similituds = []
i = 0
for v in llista:
    similituds.append([1-spatial.distance.cosine(input_v,v),i])
    i+=1

s = sorted(similituds, key=lambda x: x[0])


print(text[s[-1][1]])
