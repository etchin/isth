import sys
import csv
import pandas as pd
import numpy as np

def sigmoid(v):
    return 1 / (1 + np.exp(-v))

datapath = sys.argv[1]
hiparfile = sys.argv[2]
loparfile = sys.argv[3]

hi_vars = []
lo_vars = []

hi_pars = np.array([])
lo_pars = np.array([])

with open(hiparfile) as par:
    for ln in par.readlines():
        parts = ln.split('\t')
        if parts[0] != "Intercept": hi_vars.append(parts[0])
        hi_pars = np.append(hi_pars, [float(parts[1])])


with open(loparfile) as par:
    for ln in par.readlines():
        parts = ln.split('\t')
        if parts[0] != "Intercept": lo_vars.append(parts[0])
        lo_pars = np.append(lo_pars, [float(parts[1])])

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

hi_values = {}
for hi in hi_vars: hi_values[hi] = []

lo_values = {}
for lo in lo_vars: lo_values[lo] = []

id = -1
M = 0
for row in data[1:len(data)]:
    out_idx = titles.index("OUTCOME")
    age_idx = titles.index("AGE")

    outrange = False 
#     if row[age_idx] != '\\N': 
#         age = int(row[age_idx])
#         outrange = age < 10 or 60 < age
            
    missing = False;
    if row[out_idx] == '\\N': missing = True
    for hi in hi_vars: 
        if row[titles.index(hi)] == '\\N': missing = True 
    for lo in lo_vars: 
        if row[titles.index(lo)] == '\\N': missing = True 
    
    id = id + 1
    if missing or outrange: continue
    M = M + 1
    ids.append(id)

    y.append(float(row[out_idx]) - 1)
    for hi in hi_vars: 
        idx = titles.index(hi)
        hi_values[hi].append(float(row[idx]))
    for lo in lo_vars: 
        idx = titles.index(lo)
        lo_values[lo].append(float(row[idx]))    

hi_vars.insert(0, "INTERCEPT")
lo_vars.insert(0, "INTERCEPT")    
hi_values["INTERCEPT"] = [1] * M    
lo_values["INTERCEPT"] = [1] * M

hidf = pd.DataFrame(hi_values, columns=hi_vars)
lodf = pd.DataFrame(lo_values, columns=lo_vars)

# Building the (normalized) design matrix
hiN = len(hi_vars)
hiX = np.ones((M, hiN))
for j in range(1, hiN):
    values = hidf.values[:, j]
    minv = values.min()
    maxv = values.max()
    hiX[:, j] = (values - minv) / (maxv - minv)

loN = len(lo_vars)
loX = np.ones((M, loN))
for j in range(1, loN):
    values = lodf.values[:, j]
    minv = values.min()
    maxv = values.max()
    loX[:, j] = (values - minv) / (maxv - minv)
    
ntot = 0
nhit = 0
nfneg = 0
nfpos = 0
nfneg_ids = []
nfpos_ids = []
for i in range(0, M):
    ntot = ntot + 1
    
    pred = 0
    hip = sigmoid(np.dot(hiX[i,:], hi_pars))
    if 0.5 < hip: pred = 1
    else:
        lop = sigmoid(np.dot(loX[i,:], lo_pars))
        if 0.5 < lop: pred = 1
    
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