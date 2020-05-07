import numpy as np 

class QueryMachine():
    def __init__(self, embeddings=None, names=None, types=None):
        self.embeddings = embeddings
        self.names = names 
        self.types = types 

    def update_data(self, embeddings, names, types):
        self.embeddings = embeddings
        self.names = names 
        self.types = types 

    def search(self, src_type, src_name, target_type, k=5):
        print("k",k)
        print("src name",src_name)
        print(src_type, src_name, target_type)
        if self.embeddings is None:
            return ['Not init yet']

        target_names = self.names[self.types==target_type]
        target_embeddings = self.embeddings[self.types==target_type]
        src_names = self.names[self.types==src_type]
        src_embeddings = self.embeddings[self.types==src_type]
        try:
            assert src_name in src_names 
            src_embedding = src_embeddings[src_names==src_name][0]
            distances = -((target_embeddings-src_embedding)**2).sum(1)
            neareast_indexes = np.argpartition(distances, -k)[-k:]
            sorted_nearest_indexes = neareast_indexes[np.argsort(-distances[neareast_indexes])]
        except:
            return []

        return list(target_names[sorted_nearest_indexes])



