from flair.embeddings import BertEmbeddings
from flair.data import Sentence

# init embedding
embedding = BertEmbeddings(layers='-10')

# create a sentence
sentence = Sentence('The grass is green .')

# embed words in sentence
print(embedding.embed(sentence))

for token in sentence:
    print(token)
    print(token.embedding)
    print(token.embedding.shape)
