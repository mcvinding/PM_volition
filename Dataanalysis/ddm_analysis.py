# -*- coding: utf-8 -*-
"""
Analyse PM-volition data by HDDM.
Note: Run in py 2.7
"""
#import matplotlib
import hddm
import os.path as op
from os import chdir
import pandas as pd
import matplotlib.pyplot as plt
from kabuki.analyze import gelman_rubin
import pickle
from pymc import Matplot

# %%
workdir = '/home/mikkel/PM-volition/Dataanalysis'
outdir = '/home/mikkel/PM-volition/Datafiles'
fname = 'alldata.csv'
#chdir(workdir)
#import ddm_plot
chdir(outdir)

# %% Prepare data
data = hddm.load_csv(op.join(workdir,fname))
data = data.rename(columns={'response':'keypress'})
data = data.rename(columns={'subj':'subj_idx', 'score':'response'})

# %% Plot errors (for inspection)
data_flip = hddm.utils.flip_errors(data)        # Only for plots

fig = plt.figure()
ax = fig.add_subplot(111, xlabel='RT', ylabel='count', title='RT distributions')
for i, subj_data in data_flip.groupby('subj_idx'):
    subj_data.rt.hist(bins=100, histtype='step', ax=ax)

# %% Fit the real model (NB: Takes hours!)
mod = hddm.HDDM(data, depends_on ={'v': ['type','volition'], 'a':['type','volition']})
mod.find_starting_values()
mod.sample(10000, burn=2000, dbname='traces.db', db='pickle')
mod.save(op.join(outdir,'ddf_model'))

# %% Make a null-model and models with only one parameter between groups
mod0 = hddm.HDDM(data)
mod0.find_starting_values()
mod0.sample(10000, burn=2000, dbname='traces0.db', db='pickle')
mod0.save(op.join(outdir,'ddf_model0'))

modv = hddm.HDDM(data, depends_on ={'v': ['type','volition'], 'a':'type'})
modv.find_starting_values()
modv.sample(10000, burn=2000, dbname='traces.db', db='pickle')
modv.save(op.join(outdir,'ddf_modelV'))

moda = hddm.HDDM(data, depends_on ={'v':'type','a':['type','volition']})
moda.find_starting_values()
moda.sample(10000, burn=2000, dbname='traces.db', db='pickle')
moda.save(op.join(outdir,'ddf_modelA'))

# %% Fit the real model with bias (NB: Takes hours! Does not work!)

#modz = hddm.HDDM(data, depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
#modz.find_starting_values()
#modz.sample(10000, burn=2000, dbname='traces.db', db='pickle')
#modz.save(op.join(outdir,'ddf_modelZ'))

# %% Check convergence
mod = hddm.load('ddf_model')
mod.plot_posteriors()

models = []
for i in range(5):
    m = hddm.HDDM(data,depends_on ={'v': ['type','volition'], 'a':['type','volition']})
    m.find_starting_values()
    m.sample(10000, burn=2000)
    models.append(m)

gelman_rubin(models)

with open('models.txt','wb') as fb:
    pickle.dump(models,fb)

# %% Summary and plots
mod = hddm.load(op.join(workdir,'ddf_model'))
#modz = hddm.load(op.join(outdir,'ddf_modelZ'))

# Compare DIC


# Get statistics from posterior
stats = mod.gen_stats()
mod.print_stats()
mod.get_group_nodes()

# Posterior checks
mod.plot_posterior_predictive()

v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
hddm.analyze.plot_posterior_nodes([v_fixPM, v_freePM, v_fixFil, v_freeFil], lb=1.4, ub=3.0)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{v}$')
plt.legend(['Fixed: PM-cue','Free: PM-cue','Fixed: Filler','Free: Filler'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('v_post')

a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
hddm.analyze.plot_posterior_nodes([a_fixPM, a_freePM, a_fixFil, a_freeFil], lb=1.4, ub=3.0)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{a}$')
plt.legend(['Fixed: PM-cue','Free: PM-cue','Fixed: Filler','Free: Filler'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('a_post')

print "P_v(Free < Fix) = ", (v_fixPM.trace() > v_freePM.trace()).mean()
print "P_v(Free < Fix) = ", (v_fixFil.trace() > v_freeFil.trace()).mean()
print "P_a(Free < Fix) = ", (a_fixPM.trace() > a_freePM.trace()).mean()
print "P_a(Free < Fix) = ", (a_fixFil.trace() > a_freeFil.trace()).mean()
