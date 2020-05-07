import pandas as pd

def get_embeddings_from_tsv(filepath):
    df = pd.read_csv(filepath, sep="\t")
    return df.values

def get_meta_from_tsv(filepath):
    df = pd.read_csv(filepath, sep="\t",skiprows=1)
    return df.values[:,0], df.values[:,1]