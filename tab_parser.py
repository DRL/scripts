#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import Series,DataFrame
import sys 
import pandas as pd
import matplotlib.pyplot as plt

def genus(desc):
    line = desc
    line = line.split(' ')[0]
    return line

def counter(seq):
    """make a freq dict with species as key"""
    seq_dict = {}
    for n in seq:
        if n in seq_dict:
            seq_dict[n] += 1
        else:
            seq_dict[n] = 1
    return seq_dict

# most frequent species/genus/kingdom in table 
if __name__ == "__main__":
    in_file = sys.argv[1]
    data = pd.read_table(in_file)
    #data.info()
    #print data["gc"].mean()
    species = data['taxlevel_species']
    desc_list = [genus(tax) for tax in species] #make a list of names
    desc_dict = counter(desc_list)
    most_freq8 = sorted(desc_dict,key=lambda x:desc_dict[x],reverse=True)[:8]
    most_freq_dict = dict(((spec,desc_dict[spec]) for spec in most_freq8)) 
    print most_freq_dict
    hist_data = DataFrame([[key,most_freq_dict[key]] for key in most_freq_dict])
    print hist_data
    hist_data = DataFrame([most_freq_dict[key] for key in most_freq_dict],columns = ['Frequency'],index=most_freq_dict.keys())
    print hist_data #we use the same dictionary(most_freq_dict) for columns and index, so this will work!
    fig = plt.figure(1, figsize=(20,20), dpi=400)
    axes = plt.axes(hist_data)
    axes.set_ylabel("Species")
    axes.set_xlabel("Frequency")
    axes.set_title("Bla bla")
    plt.show()