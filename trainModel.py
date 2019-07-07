from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import nltk
import corpus



#text = nltk.corpus.gutenberg.sents('melville-moby_dick.txt')

f = open("sentences.txt","r")
s = f.read()
f.close()
text = s.splitlines()

#text = [[s] for s in text]
#sentences = [[w] for sub in text for w in sub]

l = []
for s in text:
    input = nltk.word_tokenize(s.lower())
    l.append(input)


print(l)
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(l)]

print(documents)
#documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]

#print(len(text))
model = Doc2Vec(documents, vector_size=2, window=2, min_count=1, workers=4,epochs=10)
#, vector_size=5, window=2, min_count=1, workers=4

#model.save("models/doc2vec_model")
#model = Doc2Vec.load("models/doc2vec_model")  # you can continue training with the loaded model!


input = nltk.word_tokenize("Proleukin".lower())
input_v = model.infer_vector(input)

#sentences = [ " ".join(w) for w in text]

llista = []
for sen in text:
    v = model.infer_vector([sen.lower()])
    llista.append(v)


similituds = []
i = 0
for v in llista:
    similituds.append([1-spatial.distance.cosine(input_v,v),i])
    i+=1

s = sorted(similituds, key=lambda x: x[0])
print(s)
#print(model.docvecs.similarity("proleukin",'4'))
for i in range(1,10):
    print(i," : ",text[s[-i][1]])
