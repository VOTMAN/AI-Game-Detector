import pickle

def cacheEmbeddings(embeddings):
    # print(embeddings)

    with open("../cachedEmbeddings/refEmbed.pkl", "wb") as f:
        pickle.dump(embeddings, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("Cached Reference Embeddings")