#!/usr/bin/env python

from __future__ import division
#from pylab import *
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import sys

def read_fasta_to_dict (filename):
	with open(filename) as fh:
		contig = ''
		seq = ''
		for line in fh:
		    line = line.rstrip("\n")
		    if line.startswith(">"):
		    	if (contig):
		        	add_to_fasta_dict(contig, seq)
		        seq = ''
		        contig = line.replace("|", ":").replace(",","_").replace(" ", "_").replace("__","_")
		    elif not line.strip():
		    	continue
		    else:
		        seq += line
		add_to_fasta_dict(contig, seq)
	return fasta

def get_gc(seq):
	length = len(seq) - seq.count('N') # length w/o Ns
	gc_content = (seq.count('G') + seq.count('C'))/length
	return gc_content

def add_to_fasta_dict(contig, seq):
	fasta[contig] = {'seq':'', 'len':0, 'gc':0}
	seq = seq.upper()
	fasta[contig]['seq'] = seq.upper()
	fasta[contig]['len'] = str(len(seq))
	fasta[contig]['gc'] = "%.2f" % round(get_gc(seq),2)

def plot_gc_length(fasta):
	gc = []
	length = []
	label = fasta.keys()
	for values in fasta.values():
		gc.append(float(values['gc']))
		length.append(int(values['len']))
	data = Scatter(x=gc, y=length, text=label,mode='markers')
	data = Data([data])
	layout = Layout(showlegend=False)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename = 'text-chart-basic')
	print unique_url

fasta = {}
#fasta = defaultdict(lambda: defaultdict(str))
fasta = read_fasta_to_dict(sys.argv[1])

py.sign_in("DRL", "qfpez62vvt")
plot_gc_length(fasta)
