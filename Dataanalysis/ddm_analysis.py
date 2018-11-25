# -*- coding: utf-8 -*-
"""
Analyse PM-volition data by HDDM.
Note: Run in py 2.7
"""
import sys
import hddm
import os.path as op
from os import chdir
import pandas as pd
import pymc as pc  
import numpy as np
import matplotlib.pyplot as plt
from kabuki.analyze import gelman_rubin
import pickle
from pymc import Matplot
from scipy.stats import gaussian_kde

workdir = '/home/mikkel/PM-volition/Dataanalysis'
outdir = '/home/mikkel/PM-volition/Datafiles'
chdir(outdir)

sys.path.append(workdir)
import PM_volition_utilfun as pm # plot_posterior_diff, plot_posterior_nodes2, get_posteriorP

# %% Prepare data
fname = 'alldata2.csv'

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

# %% Inspect posteriors
mod1.plot_posteriors()
mod2.plot_posteriors()

mod1.plot_posterior_predictive()
mod2.plot_posterior_predictive()

# %% Get R-hat [NB re-run due to save errors]
#models = []
#for i in range(3):
#    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
#    m.find_starting_values()
#    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
#    models.append(m)
#models.append(mod1)
#
#with open(op.join(outdir,'modelsGR1.pkl'),'wb') as fb:
#    pickle.dump(models,fb)
    
models = []
for i in range(3):
    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type']})
    m.find_starting_values()
    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
    models.append(m)
models.append(mod2)

with open(op.join(outdir,'modelsGR2.pkl'),'wb') as fb:
    pickle.dump(models,fb)

## Re-load    
# Gelman-Rubin R-hat    
#with open(op.join(outdir,'modelsGR1.pkl'), 'rb') as f:
#    models = pickle.load(f)  
#gelman_rubin(models) 
#    
with open(op.join(outdir,'modelsGR2.pkl'), 'rb') as f:
    models = pickle.load(f)    
gelman_rubin(models) 

# %% Load
chdir(outdir) #Must be in folder to load databases
#mod1 = hddm.load(op.join(outdir, 'ddm_model21'))
mod = hddm.load(op.join(outdir, 'ddm_model22'))

# %% Summary and plots
# Compare DIC (not useful)
#print 'DIC model1 = ', mod1.dic
print 'DIC model2 = ', mod.dic

# Get statistics from posterior
stats = mod.gen_stats()
mod.print_stats()
mod.get_group_nodes()

# Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
#z_fixPM, z_freePM, z_fixFil, z_freeFil  = mod1.nodes_db.node[['z(pm.fix)', 'z(pm.free)','z(filler.fix)','z(filler.free)']]
z_PM, z_Fil  = mod.nodes_db.node[['z(pm)', 'z(filler)']]
t = mod.nodes_db.node['t']

# %% Statistics
# Get P and generate difference distribtions (plots only for inspection)
P, a_PMdiff = pm.get_posteriorP(a_fixPM,a_freePM, plot=1)
P, v_PMdiff = pm.get_posteriorP(v_fixPM,v_freePM, plot=1)
#P, z_PMdiff = pm.get_posteriorP(z_fixPM,z_freePM, plot=1)

P, a_Fildiff = pm.get_posteriorP(a_fixFil,a_freeFil, plot=1)
P, v_Fildiff = pm.get_posteriorP(v_fixFil,v_freeFil, plot=0)
#P, z_Fildiff = pm.get_posteriorP(z_fixFil,z_freeFil, plot=0)

P = pm.get_posteriorP(v_fixPM,v_fixFil, plot=1)
P = pm.get_posteriorP(v_freePM,v_freeFil, plot=1)
P = pm.get_posteriorP(a_fixPM,a_fixFil, plot=1)
P = pm.get_posteriorP(a_freePM,a_freeFil, plot=1)
#P = pm.get_posteriorP(z_fixPM,z_fixFil, plot=1)
#P = pm.get_posteriorP(z_freePM,z_freeFil, plot=1)
P, z_diff = pm.get_posteriorP(z_PM,z_Fil, plot=1)

# HPDI
hpdi = 0.97

bnd = pm.get_hpdi(a_fixPM,hpdi)
bnd = pm.get_hpdi(a_freePM,hpdi)
bnd = pm.get_hpdi(a_fixFil,hpdi)
bnd = pm.get_hpdi(a_freeFil,hpdi)

bnd = pm.get_hpdi(v_fixPM,hpdi)
bnd = pm.get_hpdi(v_freePM,hpdi)
bnd = pm.get_hpdi(v_fixFil,hpdi)
bnd = pm.get_hpdi(v_freeFil,hpdi)

#bnd = pm.get_hpdi(z_fixPM,hpdi)
#bnd = pm.get_hpdi(z_freePM,hpdi)
#bnd = pm.get_hpdi(z_fixFil,hpdi)
#bnd = pm.get_hpdi(z_freeFil,hpdi)

bnd = pm.get_hpdi(z_PM,hpdi)
bnd = pm.get_hpdi(z_Fil,hpdi)

bnd = pm.get_hpdi(t,hpdi)

# %% Plots
# Posterior plots
dpi=600

# v
fig =hddm.analyze.plot_posterior_nodes([v_fixPM, v_freePM, v_fixFil, v_freeFil],lb=2.0, ub=4.0)
plt.ylim(-0.05*5,5)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{v}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
plt.savefig(op.join(outdir,'v_post2'),dpi=dpi)

# a
hddm.analyze.plot_posterior_nodes([a_fixPM, a_freePM, a_fixFil, a_freeFil],lb=1.2, ub=2.6)
plt.ylim(-0.05*10,10)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{a}$')
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
plt.savefig(op.join(outdir,'a_post2'),dpi=dpi)

# z
#hddm.analyze.plot_posterior_nodes([z_fixPM, z_freePM, z_fixFil, z_freeFil], lb=0.1, ub=0.6)
hddm.analyze.plot_posterior_nodes([z_PM, z_Fil], lb=0.1, ub=0.6)
plt.ylim(-0.05*60,60)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{z}$')
plt.legend(['PM-cue','Filler'], fontsize=8, loc=0, edgecolor='white')
plt.savefig(op.join(outdir,'z_post'),dpi=dpi)

hddm.analyze.plot_posterior_nodes([t], lb=0.1, ub=0.5)
plt.ylim(-0.05*50,50)
plt.ylabel('Density')
plt.xlabel('Value')
plt.title('Posterior: $\it{t}$')
plt.legend(['t'], fontsize=8, loc=0, edgecolor='white')
plt.savefig(op.join(outdir,'t_post'),dpi=dpi)

# Posterior differences
pm.plot_posterior_diff(v_PMdiff,lb=-1, ub=1)
plt.ylim(-0.05*3.5,3.5)
plt.ylabel('Density')
plt.xlabel('Difference')
plt.title('Fixed - Free: $\it{v}$')
plt.tight_layout()
plt.savefig(op.join(outdir,'v_PMdiff'),dpi=dpi)

pm.plot_posterior_diff(a_PMdiff,lb=-0.5, ub=0.5)
plt.ylim(-0.05*7,7)
plt.ylabel('Density')
plt.xlabel('Difference')
plt.title('Fixed - Free: $\it{a}$')
plt.tight_layout()
plt.savefig(op.join(outdir,'a_PMdiff'),dpi=dpi)

pm.plot_posterior_diff(z_diff)
plt.ylim(-0.05*45,45)
plt.ylabel('Density')
plt.xlabel('Difference')
plt.title('Fixed - Free: $\it{z}$')
plt.tight_layout()
plt.savefig(op.join(outdir,'z_diff'),dpi=dpi)
