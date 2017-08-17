import pandas as pd
import numpy as np
import math

def imputation(filename):
    baseball = pd.read_csv(filename)
    avg_weight = np.mean(baseball['weight'])
    baseball['weight'] = baseball['weight'].fillna(avg_weight)
    #print baseball['weight']
    return baseball

print imputation('C:\Users\CJH\PycharmProjects\Udacity_DataScience\Master.csv')

