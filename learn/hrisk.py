''' Adds high-risk score as the value of the logistic predictor

'''

import sys
import numpy as np

vars = []
params = np.array([])

def sigmoid(v):
    return 1 / (1 + np.exp(-v))

def init():
    global vars
    global params
    with open("high-risk-params") as data:
        for ln in data.readlines():
            parts = ln.split('\t')
            if parts[0] != "Intercept": vars.append(parts[0])
            params = np.append(params, [float(parts[1])])
    print vars
    print params

def variables():
    return vars

def get_name():
    return "HI_RISK"

def get_title():
    return "High risk score"

def get_type():
    return "float"

def calculate(values):
    if '\N' in values.values(): return '\N'
    
    temp = [1.0]
    for v in vars: temp.append(float(values[v]) - 1)
    x = np.array(temp)

    p = sigmoid(np.dot(x, params))
    return str(p)
        
def get_range(): 
    return "0,1"

def get_table(): 
    return "Risk scores"