import sys
import csv
import pandas as pd
import numpy as np

datapath = sys.argv[1]
parfile = sys.argv[2]

top_vars = []

with open(parfile) as par:
    for ln in par.readlines():
        top_vars.append(ln.strip())

datafile = datapath + "/data.tsv"
dictfile = datapath + "/dictionary.tsv"

data = []
dict = []
with open(datafile) as tsv:
    for row in csv.reader(tsv, dialect="excel-tab"):        
        data.append(row)
titles = data[0]

types = {}
with open(dictfile) as tsv:
    i = 0
    for row in csv.reader(tsv, dialect="excel-tab"):
        # Get the name from the table titles, since the dictionary will contain the aliases
        name = titles[i]
        type = row[1]
        types[name] = type
        i = i + 1
        
ntot = 0
nhit = 0
nfneg = 0
nfpos = 0
nfneg_ids = []
nfpos_ids = []
id = -1
for row in data[1:len(data)]:
    id = id + 1
    out_idx = titles.index("OUTCOME")

    out = row[out_idx]
    
    if out == '\\N': continue
    
    all_missing = True
    pred = 0
    for lb in top_vars: 
        val = row[titles.index(lb)]
        if row[titles.index(lb)] != '\\N':
            all_missing = False
            if val == '1': pred = 1
        
    if all_missing: continue
    ntot = ntot + 1

    if pred == int(out) - 1:
         nhit = nhit + 1
    elif pred == 1:
         nfpos = nfpos + 1
         nfpos_ids.append(id)
    else:      
         nfneg = nfneg + 1
         nfneg_ids.append(id)

rate = float(nhit) / float(ntot)

print 'Predictor success rate on test set:', nhit,'out of',ntot,round(100 * rate, 2), '%'
print 
print 'False negatives (cases wrongly identified as surviving)',nfneg
print nfneg_ids
print
print 'False positives (cases wrongly identified as dying)',nfpos
print nfpos_ids           

'''


for row in data[1:len(data)]:
    out_idx = titles.index("OUTCOME")
            
    missing = False;
    if row[out_idx] == '\\N': missing = True
    for lb in lab_vars: 
        if row[titles.index(lb)] == '\\N': missing = True 
    
    id = id + 1
    if missing: continue
    M = M + 1
    ids.append(id)

    y.append(float(row[out_idx]) - 1)
    for lb in lab_vars: 
        idx = titles.index(lb)
        lab_values[lb].append(float(row[idx]))

lab_vars.insert(0, "INTERCEPT")
lab_values["INTERCEPT"] = [1] * M    

df = pd.DataFrame(lab_values, columns=lab_vars)

# Building the (normalized) design matrix
N = len(lab_vars)
X = np.ones((M, N))
for j in range(1, N):
    values = df.values[:, j]
    minv = values.min()
    maxv = values.max()
    X[:, j] = (values - minv) / (maxv - minv)
    
ntot = 0
nhit = 0
nfneg = 0
nfpos = 0
nfneg_ids = []
nfpos_ids = []
for i in range(0, M):
    ntot = ntot + 1
    
    pred = 0
    p = sigmoid(np.dot(X[i,:], lab_pars))
    if 0.5 < p: pred = 1
    
    if pred == y[i]:
         nhit = nhit + 1
    elif pred == 1:
         nfpos = nfpos + 1
         nfpos_ids.append(ids[i])
    else:      
         nfneg = nfneg + 1
         nfneg_ids.append(ids[i])
        
rate = float(nhit) / float(ntot)

print 'Predictor success rate on test set:', nhit,'out of',ntot,round(100 * rate, 2), '%'
print 
print 'False negatives (cases wrongly identified as surviving)',nfneg
print nfneg_ids
print
print 'False positives (cases wrongly identified as dying)',nfpos
print nfpos_ids    
'''