#!/usr/bin/env python
# coding=utf-8

# File   :  	tagc_plot.py
# Author : 		Dominik R. Laetsch, dominik.laetsch at gmail dot com 

# # # # # 
# MODULES										
# # # # # 

from __future__ import division
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import NullFormatter
import sys, argparse, os

# # # # # # 
# FUNCTIONS	
# # # # # # 

def check_file(infile):
	# Checks for existence of file
	if not os.path.exists(infile):
		parser.error("The file %s does not exist!"%infile)
	else:
		return infile

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_parameters(p, f, t):
	# Validates and returns values for window size and minimum region length.
	if (p < 1):
		parser.error("Specify the number of phyla to plot !")
	elif (f != 'png' and f != 'pdf'):
		parser.error("Specify the output format")
	elif (t < 0 or t >3):
		parser.error("Specify the tax level [0-3]")
	else:
		return p, f, t

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_phylum_count(tax_list):
	phylum_count = {}
	for phylum in tax_list:
   		if phylum in phylum_count:
   			phylum_count[phylum] += 1
   		else:
   	 		phylum_count[phylum] = 1
   	return phylum_count


if __name__ == "__main__":

	# # # # # # # # # # # # # # # # 
	# COMMAND-LINE ARGUMENT PARSING
	# # # # # # # # # # # # # # # # 

	parser = argparse.ArgumentParser(
		prog='tagc_plot.py',
		usage = '%(prog)s infile [-p max_phylum_plot] [-f fig_format] [-t tax_level] [-m] [-h]',
		add_help=True)
	parser.add_argument('i', metavar = 'infile', 		 			help='Input file (blobplot.txt)')
	parser.add_argument('-p', metavar = 'max_phylum_plot', 			default=7, 		type = int, 	help='Maximum number of phyla to plot (Default = 7)')
	parser.add_argument('-f', metavar = 'fig_format', 	default="png", 	help='Format in which figure(s) to plot (Default = png)') 
	parser.add_argument('-t', metavar = 'tax_level', 			default=1, 		type = int, 	help='Taxonomic level on which to plot. Superkingdom = 0, Phylum = 1, Order = 2, Species = 3 (Default = 1)')
	parser.add_argument('-m', action='store_true' , help='Set flag for multi-figure plotting.') 
	args = parser.parse_args()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	blob_file = check_file(args.i)
	multi_plot = args.m
	max_phylum_plot, fig_format, tax_level = check_parameters(args.p, args.f, args.t)
	out_file = blob_file + str(".") + str(fig_format) 

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# 									CONSTANTS							 	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	almost_black = '#262626'
	grey = '#d3d3d3'
	background_grey = '#F0F0F5'
	white = '#ffffff'
	nullfmt = NullFormatter()         # no labels on axes


	blob_data = np.genfromtxt(blob_file, names=True, delimiter="\t", dtype=None)
	gc_key = blob_data.dtype.names[2]
	cov_key = blob_data.dtype.names[3]
	tax_key = blob_data.dtype.names[7-tax_level]
	x, y, phy = blob_data[gc_key], blob_data[cov_key], blob_data[tax_key]

	phylum_count=get_phylum_count(blob_data[tax_key])
	sorted_phyla = sorted(phylum_count, key=lambda x : phylum_count[x], reverse=True)

	# definitions for the axes 
	left, width = 0.1, 0.65
	bottom, height = 0.1, 0.65
	bottom_h = left_h = left+width+0.02
	rect_scatter = [left, bottom, width, height]
	rect_histx = [left, bottom_h, width, 0.2]
	rect_histy = [left_h, bottom, 0.2, height]

	# Setting up plots and axes
	plt.figure(1, figsize=(20,20))
	axScatter = plt.axes(rect_scatter, axisbg=background_grey, yscale = 'log')
	plt.suptitle(blob_file, fontsize=25, verticalalignment='bottom')
	axScatter.set_xlabel("GC", fontsize=25)
	axScatter.set_ylabel("Cov", fontsize=25)
	axScatter.grid(True, which="major", lw=2., color=white, linestyle='-') 
	axScatter.set_axisbelow(True)
	axScatter.set_xlim( (0, 1) )
	axScatter.set_ylim( (0.1, np.amax(y)) )
	axHistx = plt.axes(rect_histx, axisbg=background_grey)
	axHisty = plt.axes(rect_histy, axisbg=background_grey)
	axHistx.xaxis.set_major_formatter(nullfmt) # no labels since redundant
	axHistx.set_xlim( axScatter.get_xlim() )
	axHisty.yaxis.set_major_formatter(nullfmt) # no labels since redundant
	axHisty.set_yscale('log')
	axHisty.set_ylim( axScatter.get_ylim() )
	axHistx.grid(True, which="major", lw=2., color= white, linestyle='-')
	axHisty.grid(True, which="major", lw=2., color= white, linestyle='-')
	axHistx.set_axisbelow(True)
	axHisty.set_axisbelow(True)

	# put colormap in colors 
	colors = cm.get_cmap(name='Set2')

	# Plotting
	top_bins = np.arange(0, 1, 0.01)
	right_bins = np.logspace(-1, 10, 500, base=10.0)
	i = 0
	print "Plotting :"
	for phylum in sorted_phyla:
		if i < max_phylum_plot:
			cond = (phy == phylum )
			sys.stdout.write("\t" + phylum)
			x_i = x[cond]
			y_i = y[cond]
			hex_color = mat.colors.rgb2hex(colors(1.0 * (i/max_phylum_plot)))
			if phylum != 'Not annotated':
				s = 65
				lw = 0.5
				alpha = 1
				color = hex_color
			else:
				s = 25
				lw = 0.1
				alpha = 0.5
				color = grey
			axHistx.hist(x_i, color = color, bins = top_bins)
			axHisty.hist(y_i, color = color, bins = right_bins, histtype='bar', orientation='horizontal')
			axScatter.scatter(x_i, y_i, color = color, s = s, lw = lw, alpha=alpha, edgecolor=almost_black, label=phylum + " (" + str(phylum_count[phylum]) + ")")
			axScatter.legend(loc=1, fontsize=25, scatterpoints=1)
			i += 1
			if (multi_plot): # MULTI-PLOT!!!
				plt.savefig(out_file, format=fig_format)
			print " [Done]"
		else:
			break

	axScatter.legend(loc=1, fontsize=25, scatterpoints=1)
	sys.stdout.write("Saving file " + blob_file + "." + fig_format)
	plt.savefig(out_file, format=fig_format)
	print " [Done]"
	#plt.show()