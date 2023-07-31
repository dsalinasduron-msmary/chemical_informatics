import requests
import pandas as pd
import pickle
import time

jsons = []
with open("aids.txt") as f :
    for aid in f.readlines() :
        global r
        r = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{}/description/json".format(aid.rstrip().lstrip()))
        if r.status_code == 200 :
            j = r.json()
            jsons.append(j)
            print("BEGIN DESCRIPTION")
            print("\n".join(j["PC_AssayContainer"][0]["assay"]["descr"]["description"]))
            print("END DESCRIPTION")
        time.sleep(0.5)

f = open("assays.pickle","wb")
pickle.dump(jsons,f)
f.close()

"""
r.json()["PC_AssayContainer"][0]["assay"]["descr"]["description"]
"""
