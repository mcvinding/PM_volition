# -*- coding: utf-8 -*-
"""
Analyse PM-volition data by HDDM.
@author: mcvinding
"""
import sys
import hddm
import os.path as op
from os import chdir
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
%matplotlib qt
from kabuki.analyze import gelman_rubin
import pickle

#workdir = '/home/mikkel/PM-volition/Dataanalysis'
#outdir = '/home/mikkel/PM-volition/Datafiles'

workdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Dataanalysis'
outdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Datafiles'

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
mod1 = hddm.HDDM(data, bias=False, depends_on ={'v': ['type','volition'], 'a':['volition']})
mod1.find_starting_values()
mod1.sample(10000, burn=2000, dbname='traces31.db', db='pickle')
#mod1.save(op.join(outdir,'ddm_model21'))  # ERROR

# save
fhandler = open(op.join(outdir,"ddm_model31"),"wb")
pickle.dump(mod1, fhandler)
fhandler.close()

# %% Fit model with "volition" on all parameters
#mod2 = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition'], 't':['type','volition']})
#mod2.find_starting_values()
#mod2.sample(10000, burn=2000, dbname='traces22.db', db='pickle')
##mod2.save(op.join(outdir,"ddm_model22"))  # ERROR
#
## save
#fhandler = open(op.join(outdir,"ddm_model22"),"wb")
#pickle.dump(mod2, fhandler)
#fhandler.close()

# %% Model with only intercept on non-decision time
mod3 = hddm.HDDM(data, bias=False, depends_on ={'v': ['type','volition'], 'a':['type','volition']})
mod3.find_starting_values()
mod3.sample(10000, burn=2000, dbname='traces23.db', db='pickle')
mod3.save(op.join(outdir,"ddm_model33"))
#
## save
fhandler = open(op.join(outdir,"ddm_model23"),"wb")
pickle.dump(mod3, fhandler)
fhandler.close()

# %% Inspect posteriors
#mod1.plot_posteriors()
#mod2.plot_posteriors()
#mod3.plot_posteriors()
#
#mod1.plot_posterior_predictive()
#mod2.plot_posterior_predictive()
#
#print('DIC model1 = ', mod1.dic)
#print('DIC model2 = ', mod2.dic)
#print('DIC model3 = ', mod3.dic)

# %% Get R-hat
#models = []
#for i in range(3):
#    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
#    m.find_starting_values()
#    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
#    models.append(m)
#models.append(mod1)
#with open(op.join(outdir,'modelsGR1.pkl'),'wb') as fb:
#    pickle.dump(models,fb)

## MODEL 2 (full model)
mod = hddm.load(op.join(outdir, 'ddm_model31'))
    
models = []
for i in range(3):
    m = hddm.HDDM(data, bias=False, depends_on ={'v': ['type','volition'], 'a':['volition']})
    m.find_starting_values()
    m.sample(10000, burn=2000, dbname='traces31_'+str(i)+'.db', db='pickle')
    models.append(m)
models.append(mod)

# save
with open(op.join(outdir,'modelsGR3.pkl'),'wb') as fb:
    pickle.dump(models,fb)

# Re-load
with open(op.join(outdir,'modelsGR3.pkl'), 'rb') as f:
    models = pickle.load(f)

# Gelman-Rubin model diagnostics
gelman_rubin(models) 

## MODEL 3
#mod3 = hddm.load(op.join(outdir, 'ddm_model23'))
#
#models3 = []
#for i in range(3):
#    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
#    m.find_starting_values()
#    m.sample(10000, burn=2000, dbname='traces23_'+str(i)+'.db', db='pickle')
#    models3.append(m)
#models3.append(mod3)
#
## save
#with open(op.join(outdir,'modelsGR3.pkl'),'wb') as fb:
#    pickle.dump(models3,fb)
#
#gelman_rubin(models3)

# %% Load (/NOT WORKING)
chdir(outdir) #Must be in folder to load databases
#mod1 = hddm.load(op.join(outdir, 'ddm_model21'))
mod = hddm.load(op.join(outdir, 'ddm_model31'))

# %% Model diagnostics
# Compare DIC (not useful)
print('DIC model1 = ', mod.dic)
#print('DIC model2 = ', mod.dic)

ppc_data = hddm.utils.post_pred_gen(mod)
ppc_compare = hddm.utils.post_pred_stats(data, ppc_data)
ppc_stats = hddm.utils.post_pred_stats(data, ppc_data, call_compare=False)

#%% Summary and plots
# Get statistics from posterior
stats = mod.gen_stats()
mod.print_stats()
mod.get_group_nodes()

# Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fix, a_free = mod.nodes_db.node[['a(fix)', 'a(free)']]
t_int  = mod.nodes_db.node['t']

# Get parameters and HPDI
hpdi = 0.97

bnd = pm.get_hpdi(v_fixPM, hpdi)
bnd = pm.get_hpdi(v_freePM, hpdi)
bnd = pm.get_hpdi(v_fixFil, hpdi)
bnd = pm.get_hpdi(v_freeFil, hpdi)

bnd = pm.get_hpdi(a_fix, hpdi)
bnd = pm.get_hpdi(a_free, hpdi)

bnd = pm.get_hpdi(t_int, hpdi)

# Get P and generate difference distribtions (plots only for inspection)
# Fix vs Free
P = pm.get_posteriorP(v_fixPM, v_freePM, plot=0)
P = pm.get_posteriorP(v_fixFil, v_freeFil, plot=0)
P = pm.get_posteriorP(a_fix, a_free, plot=0)

#PM vs. Filler
P = pm.get_posteriorP(v_fixPM, v_fixFil, plot=0)
P = pm.get_posteriorP(v_freePM, v_freeFil, plot=0)

# %% SUMMARY MODEL 3
# Get statistics from posterior
stats = mod3.gen_stats()
mod3.print_stats()
mod3.get_group_nodes()

# Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod3.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod3.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
z_fixPM, z_freePM, z_fixFil, z_freeFil  = mod3.nodes_db.node[['z(pm.fix)', 'z(pm.free)','z(filler.fix)','z(filler.free)']]
t_int  = mod3.nodes_db.node['t']

# PM trials: Fix vs Free
P = pm.get_posteriorP(a_fixPM, a_freePM, plot=1)
P = pm.get_posteriorP(v_fixPM, v_freePM, plot=1)
P = pm.get_posteriorP(z_fixPM, z_freePM, plot=1)

# Filler trials: Fix vs Free
P = pm.get_posteriorP(a_fixFil, a_freeFil, plot=1)
P = pm.get_posteriorP(v_fixFil, v_freeFil, plot=1)
P = pm.get_posteriorP(z_fixFil, z_freeFil, plot=1)

# Fixed: PM vs. Filler
P = pm.get_posteriorP(a_fixPM, a_fixFil, plot=1)
P = pm.get_posteriorP(v_fixPM, v_fixFil, plot=1)
P = pm.get_posteriorP(z_fixPM, z_fixFil, plot=1)

# Free: PM vs. filler
P = pm.get_posteriorP(a_freePM, a_freeFil, plot=1)
P = pm.get_posteriorP(v_freePM, v_freeFil, plot=1)
P = pm.get_posteriorP(z_freePM, z_freeFil, plot=1)
 
# Get parameters and HPDI
hpdi = 0.97

bnd = pm.get_hpdi(a_fixPM, hpdi)
bnd = pm.get_hpdi(a_freePM, hpdi)
bnd = pm.get_hpdi(a_fixFil, hpdi)
bnd = pm.get_hpdi(a_freeFil, hpdi)

bnd = pm.get_hpdi(v_fixPM, hpdi)
bnd = pm.get_hpdi(v_freePM, hpdi)
bnd = pm.get_hpdi(v_fixFil, hpdi)
bnd = pm.get_hpdi(v_freeFil, hpdi)

bnd = pm.get_hpdi(z_fixPM, hpdi)
bnd = pm.get_hpdi(z_freePM, hpdi)
bnd = pm.get_hpdi(z_fixFil, hpdi)
bnd = pm.get_hpdi(z_freeFil, hpdi)

bnd = pm.get_hpdi(t_int, hpdi)

#END