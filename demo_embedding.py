import math

from src.llm import get_embeddings

sentences = [
    "I love traveling to new countries.",
    "Visiting foreign places makes me happy.",
    "The cat sat on the sofa.",
]

emb = get_embeddings()
vectors =emb.embed_documents(sentences)

print("Vektör sayısı:", len(vectors))
print("Her vektörün uzunluğu:", len(vectors[0]))
print("İlk cümlenin ilk 5 sayısı:", [round(x, 4) for x in vectors[0][:5]])


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)


print()
print("1 ile 2 (anlamca benzer):  ", round(cosine(vectors[0], vectors[1]), 3))
print("1 ile 3 (alakasız):        ", round(cosine(vectors[0], vectors[2]), 3))
print("2 ile 3 (alakasız):        ", round(cosine(vectors[1], vectors[2]), 3))