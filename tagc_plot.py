from __future__ import division
import numpy as np
import matplotlib as mat
mat.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import NullFormatter
import sys

almost_black = '#262626'
nullfmt = NullFormatter()         # no labels

def get_phylum_count(tax_list):
	phylum_count = {}
	for phylum in tax_list:
   		if phylum in phylum_count:
   			phylum_count[phylum] += 1
   		else:
   	 		phylum_count[phylum] = 1
   	return phylum_count

# data and sorting
blob_file = sys.argv[1]
blob_data = np.genfromtxt(blob_file, names=True, delimiter="\t", dtype=None)
gc_key = blob_data.dtype.names[2]
cov_key = blob_data.dtype.names[3]
tax_key = blob_data.dtype.names[6]
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
plt.ioff()
plt.figure(figsize=(20,20))
axScatter = plt.axes(rect_scatter, axisbg='#F0F0F5', yscale = 'log')
plt.suptitle(blob_file, fontsize=25)
axScatter.set_xlabel("GC", fontsize=25)
axScatter.set_ylabel("Cov", fontsize=25)
axScatter.grid(True, which="major", lw=2., color='#ffffff', linestyle='-') 
axScatter.set_axisbelow(True)
axScatter.set_xlim( (0, 1) )
axScatter.set_ylim( (0.1, np.amax(y)) )
axHistx = plt.axes(rect_histx, axisbg='#F0F0F5')
axHisty = plt.axes(rect_histy, axisbg='#F0F0F5')
axHistx.xaxis.set_major_formatter(nullfmt) # no labels since redundant
axHistx.set_xlim( axScatter.get_xlim() )
axHisty.yaxis.set_major_formatter(nullfmt) # no labels since redundant
axHisty.set_yscale('log')
axHisty.set_ylim( axScatter.get_ylim() )
axHistx.grid(True, which="major", lw=2., color='#ffffff', linestyle='-')
axHisty.grid(True, which="major", lw=2., color='#ffffff', linestyle='-')
axHistx.set_axisbelow(True)
axHisty.set_axisbelow(True)

# put colormap in colors 
colors = cm.get_cmap(name='Set2')

# define how many phyla should be plotted
max_phylum_plot = 7
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
			axScatter.scatter(x_i, y_i, color= hex_color, s=65, lw = 0.5, alpha=1, edgecolor=almost_black, label=phylum + " (" + str(phylum_count[phylum]) + ")")
			i += 1
		else:
			axScatter.scatter(x_i, y_i, color='#d3d3d3', s=25, lw = 0.1, alpha=0.5, edgecolor=almost_black, label=phylum + " (" + str(phylum_count[phylum]) + ")")
			i += 1
		print " [Done]"
	else:
		break

sys.stdout.write("Plotting histograms")
top_bins = np.arange(0, 1, 0.01)
axHistx.hist(x,  color = 'lightgrey', bins=top_bins)
right_bins = np.logspace(-1, 10, 500, base=10.0)
axHisty.hist(y, color = 'lightgrey', bins=right_bins, orientation='horizontal')
for label in axHisty.get_xticklabels():
    label.set_rotation('vertical')
axScatter.legend(loc=1, fontsize=25, scatterpoints=1)
print " [Done]"

fig_format = 'png'
sys.stdout.write("Saving file " + blob_file + "." + fig_format)
plt.savefig(blob_file + '.png', format=fig_format)
print " [Done]"
#plt.show()
