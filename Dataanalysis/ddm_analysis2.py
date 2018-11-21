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
import pymc as pc  
import matplotlib.pyplot as plt
from kabuki.analyze import gelman_rubin
import pickle
from pymc import Matplot

# %%
#workdir = '/home/mikkel/PM-volition/Dataanalysis'
outdir = '/home/mikkel/PM-volition/Datafiles'
fname = 'alldata2.csv'
#chdir(workdir)
#import ddm_plot
chdir(outdir)

# %% Prepare data
data = hddm.load_csv(op.join(outdir,fname))
data = data.rename(columns={'response':'keypress'})
data = data.rename(columns={'subj':'subj_idx', 'score':'response'})

# %% Plot errors (for inspection)
data_flip = hddm.utils.flip_errors(data)        # Only for plots

fig = plt.figure()
ax = fig.add_subplot(111, xlabel='RT', ylabel='count', title='RT distributions')
for i, subj_data in data_flip.groupby('subj_idx'):
    subj_data.rt.hist(bins=100, histtype='step', ax=ax)

# %% Fit the real model (NB: Takes hours!)
mod1 = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
mod1.find_starting_values()
mod1.sample(10000, burn=2000, dbname='traces21.db', db='pickle')
mod1.save(op.join(outdir,'ddm_model21'))

mod2 = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type']})
mod2.find_starting_values()
mod2.sample(10000, burn=2000, dbname='traces22.db', db='pickle')
mod2.save(op.join(outdir,'ddm_model22'))

# %% Diagnostics and check convergence
chdir(outdir) #Must be in folder to load databases

mod1 = hddm.load(op.join(outdir, 'ddm_model21'))
mod2 = hddm.load(op.join(outdir, 'ddm_model22'))
#mod0 = hddm.load(op.join(outdir,'ddf_model0'))

mod1.plot_posteriors()
mod2.plot_posteriors()

# %% Get R-hat 
models = []
for i in range(3):
    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
    m.find_starting_values()
    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
    models.append(m)
models.append(mod1)

gelman_rubin(models) 

with open(op.join(outdir,'modelsGR1.pkl'),'wb') as fb:
    pickle.dump(models,fb)
    
models = []
for i in range(3):
    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type']})
    m.find_starting_values()
    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
    models.append(m)
models.append(mod1)

gelman_rubin(models) 

with open(op.join(outdir,'modelsGR2.pkl'),'wb') as fb:
    pickle.dump(models,fb)
    
#with open(op.join(outdir,'models.pkl'), 'rb') as f:
#    models = pickle.load(f)  

# %% Summary and plots
mod = hddm.load(op.join(outdir,'ddm_model'))
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
mod.plot_posterior_predictive()
mod.plot_posterior_quantiles()

# Plot posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod1.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod2.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]

hddm.analyze.plot_posterior_nodes([v_fixPM, v_freePM, v_fixFil, v_freeFil])
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{v}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
#plt.savefig('v_post')

a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod1.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod2.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]

hddm.analyze.plot_posterior_nodes([a_fixPM, a_freePM, a_fixFil, a_freeFil])
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{a}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
#plt.savefig('a_post')


z_fixPM, z_freePM, z_fixFil, z_freeFil  = mod1.nodes_db.node[['z(pm.fix)', 'z(pm.free)','z(filler.fix)','z(filler.free)']]
hddm.analyze.plot_posterior_nodes([z_fixPM, z_freePM, z_fixFil, z_freeFil])
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{z}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')

z_fix, z_free  = mod2.nodes_db.node[['z(pm)', 'z(filler)']]
hddm.analyze.plot_posterior_nodes([z_fix, z_free])
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{z}$')
plt.legend(['PM','Filler'], fontsize=8, loc=0, edgecolor='white')

# %% Statistics and difference plots
v_PMdiff = v_fixPM.trace() - v_freePM.trace()
a_PMdiff = a_fixPM.trace() - a_freePM.trace()
z_PMdiff = z_fixPM.trace() - z_freePM.trace()

pd.DataFrame(v_PMdiff).plot(kind='density') # or pd.Series()
plt.axvline(0)
#plt.savefig('a_post')

# Comparison of posteriors
print "PM: P_v(Free < Fix) = ", (v_fixPM.trace() > v_freePM.trace()).mean()
print "Fil: P_v(Free < Fix) = ", (v_fixFil.trace() > v_freeFil.trace()).mean()
print "PM: P_a(Free < Fix) = ", (a_fixPM.trace() > a_freePM.trace()).mean()
print "Fil: P_a(Free < Fix) = ", (a_fixFil.trace() > a_freeFil.trace()).mean()

#%% HPD (67%, 89%, 97%)
hpdi = 0.97
print('a(filler.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(filler.fix)'], 1-hpdi)))
print('a(filler.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(filler.free)'], 1-hpdi)))
print('a(pm.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(pm.fix)'], 1-hpdi)))
print('a(pm.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['a(pm.free)'], 1-hpdi)))

print('v(filler.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(filler.fix)'], 1-hpdi)))
print('v(filler.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(filler.free)'], 1-hpdi)))
print('v(pm.fix) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(pm.fix)'], 1-hpdi)))
print('v(pm.free) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['v(pm.free)'], 1-hpdi)))

print('t(intercept) %s HPD: %s' % (hpdi, pc.utils.hpd(mod.get_traces()['t'], 1-hpdi)))

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

