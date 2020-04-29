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

    def search(self, src_type, src_name, target_type, k=10):
        print(src_type, src_name, target_type)
        if self.embeddings is None:
            return ['Not init yet']

        target_names = self.names[self.types==target_type]
        target_embeddings = self.embeddings[self.types==target_type]
        src_names = self.names[self.types==src_type]
        src_embeddings = self.embeddings[self.types==src_type]

        assert src_name in src_names 
        src_embedding = src_embeddings[src_names==src_name][0]
        print(src_embedding)
        distances = ((target_embeddings-src_embedding)**2).sum(1)
        print(distances)
        neareast_indexes = np.argpartition(distances, -k)[-k:]
        print(neareast_indexes)
        sorted_nearest_indexes = neareast_indexes[np.argsort(distances[neareast_indexes])]

        return list(target_names[sorted_nearest_indexes])



