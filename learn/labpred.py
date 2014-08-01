import sys
import csv
import pandas as pd
import numpy as np

def sigmoid(v):
    return 1 / (1 + np.exp(-v))

datapath = sys.argv[1]
labparfile = sys.argv[2]

lab_vars = []
lab_pars = np.array([])

with open(labparfile) as par:
    for ln in par.readlines():
        parts = ln.split('\t')
        if parts[0] != "Intercept": lab_vars.append(parts[0])
        lab_pars = np.append(lab_pars, [float(parts[1])])


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

y = []
ids = []

lab_values = {}
for lb in lab_vars: lab_values[lb] = []

id = -1
M = 0
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