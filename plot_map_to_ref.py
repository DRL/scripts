from __future__ import division
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import FuncFormatter
import sys
import operator

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))

    # The percent symbol needs escaping in latex
    if plt.rcParams['text.usetex'] == True:
    	return s + r'$\%$'
    else:
    	return s + '%'

data_file = sys.argv[1]
data = np.genfromtxt(data_file, names=True, delimiter="\t") 
out_file = data_file + ".pdf"
almost_black = '#262626'
grey = '#d3d3d3'
background_grey = '#F0F0F5'
white = '#ffffff'
nullfmt = NullFormatter()
colormap = 'Set2'
blobplots = 3
blue = '#8da0cb'
red = '#fa8e63'
green = '#a7d854'
grey ='#C0C0C0'
brigh_grey ='#A0A0A0'

fig = plt.figure(figsize=(10,20), dpi=300)
name_of_set = ('ERR114517', 'ERR123952', 'ERR123953', 'ERR123954', 'ERR123955', 'ERR123956', 'ERR123957')

list_of_ax = [fig.add_subplot(711), fig.add_subplot(712), fig.add_subplot(713), fig.add_subplot(714), fig.add_subplot(715), fig.add_subplot(716), fig.add_subplot(717)]

#plt.rc('axes',edgecolor=white)

i=0
for name in name_of_set:
	ax = list_of_ax[i]
	y_pos = np.arange(blobplots)
	y_pos = y_pos[::-1]
	#reads_pass = list(data[i])[0:3]
	#reads_fail = list(data[i])[3:6]
	#reads_high = list(data[i])[6:9]
	
	reads_pass_not_map = list(data[i])[0:3]
	reads_pass_map = list(data[i])[3:6]
	reads_pass_multi = list(data[i])[6:9]
	reads_fail_not_map = list(data[i])[12:15]
	reads_fail_map = list(data[i])[15:18]
	reads_fail_multi = list(data[i])[18:21]
	
	#A = reads_pass_map
	A = reads_fail_map
	print A
	#B = map(operator.add, A, reads_pass_not_map)
	B = map(operator.add, A, reads_fail_not_map)
	#B = reads_fail_not_map
	print B
	#C = reads_pass_multi 
	#C = map(operator.add, B, reads_pass_multi)
	
	label_B = 'Reads not mapping'
	#label_C = 'Reads multi mapping '
	label_A = 'Reads mapping'
	#ax.barh(y_pos, C, color=grey, lw = 0.5, edgecolor=white, label=label_C)
	if A == [0,0,0]:
		B = [1,1,1]
		ax.barh(y_pos, B, color='#A0A0A0', hatch="/", lw = 0.5, edgecolor=white, label=label_B)
	else:	
		ax.barh(y_pos, B, color=grey, lw = 0.5, edgecolor=white, label=label_B)
	ax.barh(y_pos, A, color=blue, lw = 0.5, edgecolor=white, label=label_A)
	ax.set_xlim(0, 1)
	ax2 = ax.twinx()
	ax2.get_yaxis().set_ticks([])
	ax2.set_ylabel("1\n\n2\n\n3", fontsize=20, rotation=0, verticalalignment='center', horizontalalignment ='left' )
	ax.get_yaxis().set_ticks([])
	ax.set_ylabel(name, fontsize=25, rotation=90, verticalalignment='baseline', horizontalalignment ='center' )
	if i == 6:
		ax.get_xaxis().set_visible(True)
		#ax.tick_params(labeltop='off', labelleft='off')
	else: 
		ax.get_xaxis().set_visible(False)
	i += 1
	for spine in ax.spines.values():
		spine.set_edgecolor(white)
	#ax.legend( fontsize=25)

formatter = FuncFormatter(to_percent)
plt.gca().xaxis.set_major_formatter(formatter)
ax.set_axisbelow(False)
#ax.set_color(almost_black)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], fontsize = 25, bbox_to_anchor=(0., -0.5, 1., .102), loc=10,
       ncol=1, borderaxespad=0.)
plt.savefig(out_file, format='pdf')