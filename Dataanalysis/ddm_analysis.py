# -*- coding: utf-8 -*-
"""
Analyse PM-volition data by HDDM.
Note: Run in py 2.7
"""
#import matplotlib
import hddm
import os.path as op
from os import chdir
import os.path as op
import pandas as pd
import pymc as pc  
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

modz = hddm.HDDM(data, depends_on ={'v': 'type', 'a':'type'})
modz.find_starting_values()
modz.sample(10000, burn=2000, dbname='traces0.db', db='pickle')
modz.save(op.join(outdir,'ddf_modelZ'))

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

# %% Diagnostics and check convergence
mod = hddm.load('ddf_model')
mod.plot_posteriors()

# Get R-hat
models = []
for i in range(3):
    m = hddm.HDDM(data,depends_on ={'v': ['type','volition'], 'a':['type','volition']})
    m.find_starting_values()
    m.sample(10000, burn=2000)
    models.append(m)
models.append(mod)

gelman_rubin(models) 

with open(op.join(outdir,'models.pkl'),'wb') as fb:
    pickle.dump(models,fb)
    
#with open(op.join(outdir,'models.pkl'), 'rb') as f:
#        pickle.load(f)  

# %% Summary and plots
mod = hddm.load(op.join(outdir,'ddf_model'))
#modz = hddm.load(op.join(outdir,'ddf_modelZ'))

# Compare DIC (not useful)
print 'DIC full model = ', mod.dic
print 'DIC null model = ', mod0.dic
print 'DIC type model = ', modz.dic
print 'DIC a model = ', moda.dic
print 'DIC v model = ', modv.dic

# Get statistics from posterior
stats = mod.gen_stats()
mod.print_stats()
mod.get_group_nodes()

# Posterior checks
#mod.plot_posterior_predictive()
mod.plot_posterior_quantiles()

# Plot posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
hddm.analyze.plot_posterior_nodes([v_fixPM, v_freePM, v_fixFil, v_freeFil], lb=1.6, ub=3.3)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{v}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('v_post')

a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
hddm.analyze.plot_posterior_nodes([a_fixPM, a_freePM, a_fixFil, a_freeFil], lb=1.0, ub=2.5)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{a}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('a_post')

# Comparison of posteriors
print "PM: P_v(Free < Fix) = ", (v_fixPM.trace() > v_freePM.trace()).mean()
print "Fil: P_v(Free < Fix) = ", (v_fixFil.trace() > v_freeFil.trace()).mean()
print "PM: P_a(Free < Fix) = ", (a_fixPM.trace() > a_freePM.trace()).mean()
print "Fil: P_a(Free < Fix) = ", (a_fixFil.trace() > a_freeFil.trace()).mean()


#%% HPD (67%, 89%, 97%)
hpdi = 0.67
print('a(filler.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(filler.fix)'], 1-hpdi)))
print('a(filler.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(filler.free)'], 1-hpdi)))
print('a(pm.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(pm.fix)'], 1-hpdi)))
print('a(pm.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(pm.free)'], 1-hpdi)))

print('v(filler.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(filler.fix)'], 1-hpdi)))
print('v(filler.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(filler.free)'], 1-hpdi)))
print('v(pm.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(pm.fix)'], 1-hpdi)))
print('v(pm.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(pm.free)'], 1-hpdi)))

#%% Plot "null" model posterior denisty

# Plot posteriors
v_PM, v_Fil  = modz.nodes_db.node[['v(pm)','v(filler)']]
hddm.analyze.plot_posterior_nodes([v_PM, v_Fil] ) #, lb=1.6, ub=3.3)
plt.gca().get_lines()[0].set_color("olive")
plt.gca().get_lines()[1].set_color("purple")
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{v}$')
plt.legend(['PM-cue','Filler'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('v_postz')

a_PM, a_Fil  = modz.nodes_db.node[['a(pm)','a(filler)']]
hddm.analyze.plot_posterior_nodes([a_PM, a_Fil], lb=1.0, ub=2.5)
plt.gca().get_lines()[0].set_color("olive")
plt.gca().get_lines()[1].set_color("purple")
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{a}$')
plt.legend(['PM-cue','Filler'], fontsize=8, loc=0, edgecolor='white')
plt.savefig('a_postz')



