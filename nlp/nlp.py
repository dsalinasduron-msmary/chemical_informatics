import pickle
import pandas as pd
from transformers import pipeline


#ds = [ "\n".join(r["PC_AssayContainer"][0]["assay"]["descr"]["description"]) for r in js ]

ds = []
with open("descriptions.txt") as f :
    d = ""
    for L in f.readlines() :
        if L == "END DESCRIPTION\n" :
            ds.append(d)
            d = ""
        else :
            d = d + L

generator  = pipeline(model="dmis-lab/biobert-base-cased-v1.1-squad")
summarizer = pipeline(task="summarization",model="NotXia/pubmedbert-bio-ext-summ")
#generator = pipeline(task="question-answering",model="SaeedMLK/MT5Tokenizer_reading-comprehension")
#question="""What was the assay?"""
questions=["What was the assay?","What cell lines were used?"]

#responses = [generator(context=d,question=question) for d in ds]

sort_f = lambda x : x["score"]

for d in ds :
    print(d)
    s = summarizer(d)
    rs = sorted([ generator(context=s,question=q) for q in questions ],key=sort_f,reverse=True)
    print(rs[0]["answer"])
