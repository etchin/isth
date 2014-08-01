import sys, os
import pandas as pd
import numpy as np
import shutil as sh

data_folder = sys.argv[1]
train_folder = sys.argv[2]
test_folder = sys.argv[3]

data_file = data_folder + "/data.tsv"
train_file = train_folder + "/data.tsv"
test_file = test_folder + "/data.tsv"
addtl_files = ["/config.mira", "/dictionary.tsv", "/groups.xml"]

with open(data_file) as data:
    names = [x.strip() for x in data.readline().split('\t')]

to_string = {}
with open(data_folder + "/dictionary.tsv") as dict:
    lines = dict.readlines()
    for i in range(0, len(lines)):
        parts = lines[i].split('\t')
        if parts[1] != 'float':
            to_string[names[i]] = lambda x : str(x)

df = pd.read_csv(data_file, delimiter='\t', na_values='\\N', converters=to_string)

# Create training set by randomly choosing 70% of rows from each outcome value
y = df["OUTCOME"]
i0 = np.where(y == '1')
i1 = np.where(y == '2')
ri0 = np.random.choice(i0[0], size=0.7*i0[0].shape[0], replace=False)
ri1 = np.random.choice(i1[0], size=0.7*i1[0].shape[0], replace=False)
itrain = np.concatenate((ri1, ri0))
itrain.sort()

itest = [i for i in range(0, len(y)) if i not in itrain]

train_df = df.iloc[itrain,:]
train_df.to_csv(train_file, sep='\t', na_rep='\\N', index=False)

test_df = df.iloc[itest,:]
test_df.to_csv(test_file, sep='\t', na_rep='\\N', index=False)

# TODO: copy config, dict, and groups file to train and test folders

if os.path.isfile(train_folder + "/data.bin"):
    os.remove(train_folder + "/data.bin")
for file in addtl_files:
    if os.path.isfile(data_folder + file):
        sh.copyfile(data_folder + file, train_folder + file)
    
if os.path.isfile(test_folder + "/data.bin"):
    os.remove(test_folder + "/data.bin")
for file in addtl_files:
    if os.path.isfile(data_folder + file):
        sh.copyfile(data_folder + file, test_folder + file)
