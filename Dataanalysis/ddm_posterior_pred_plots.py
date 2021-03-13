# -*- coding: utf-8 -*-
"""
Plot posterior predictive checks of DDM analysis.  
Use adapted version of kabuki.analyze.plot_posterior_predictive.
@author: Mikkel
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
%matplotlib qt
#import hddm
#import pickle
from os import chdir
import os.path as op
import sys


workdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Dataanalysis'
outdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Datafiles'

sys.path.append(workdir)
import PM_volition_utilfun as pm2

chdir(outdir)

#%% Load data
mod = hddm.load(op.join(outdir, 'ddm_model31'))

#%% PLOT                             
# Plot options
figsize=(8,10)
plot_func = kabuki.analyze._plot_posterior_pdf_node
observeds = mod.get_observeds()
max_items = max([len(i[1]) for i in
     observeds.groupby('tag').groups.items()])
columns = min(3, max_items)

# Plot different conditions (new figure for each)
for tag, nodes in observeds.groupby('tag'):
    fig = plt.figure(figsize=figsize)
    tg = tag[0].upper()+' '+tag[1].upper()
    fig.suptitle(tg, fontsize=12)
    fig.subplots_adjust(top=0.9, hspace=.8, wspace=.15)

    # Plot individual subjects (if present)
    i = 0
    for subj_i, (node_name, bottom_node) in enumerate(nodes.iterrows()):
        i += 1
        if not hasattr(bottom_node['node'], 'pdf'):
            continue # skip nodes that do not define the required_method

        ax = fig.add_subplot(np.ceil(len(nodes)/columns), columns, subj_i+1)
        if 'subj_idx' in bottom_node:
            ax.set_title(str(int(bottom_node['subj_idx'])), pad=0.5)

        plot_func(bottom_node['node'], ax, value_range=np.linspace(-1.5, 1.5, 100))

    # Save figures 
    fname = 'ppq_' + '_'.join(tag)+'.tif'
    if isinstance(format, str):
        format = ('tif', 'png')
    fig.savefig(op.join(outdir, fname), format='tif', dpi=600)

#END