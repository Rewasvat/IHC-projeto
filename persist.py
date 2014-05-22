#!/usr/bin/python3

import pickle

def save(tag, data):
    with open("data/"+tag, "wb") as f:
        pickle.dump(data, f)
  
def load(tag):
    with open("data/"+tag, "rb") as f:
        return pickle.load(f)
