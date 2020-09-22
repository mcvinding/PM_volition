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

workdir = '/home/mikkel/PM-volition/Dataanalysis'
outdir = '/home/mikkel/PM-volition/Datafiles'

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
mod1 = hddm.HDDM(data, include='z', depends_on ={'v': ['volition'], 'a':['volition'], 'z':['volition']})
mod1.find_starting_values()
mod1.sample(10000, burn=2000, dbname='traces21.db', db='pickle')
#mod1.save(op.join(outdir,'ddm_model21'))  # ERROR

# save
fhandler = open(op.join(outdir,"ddm_model21"),"wb")
pickle.dump(mod1, fhandler)
fhandler.close()

# %% Fit model with "volition" on all parameters

mod2 = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition'], 't':['type','volition']})
mod2.find_starting_values()
mod2.sample(10000, burn=2000, dbname='traces22.db', db='pickle')
#mod2.save(op.join(outdir,"ddm_model22"))  # ERROR

# save
fhandler = open(op.join(outdir,"ddm_model22"),"wb")
pickle.dump(mod2, fhandler)
fhandler.close()

# %% Model with only intercept on non-decision time
mod3 = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
mod3.find_starting_values()
mod3.sample(10000, burn=2000, dbname='traces23.db', db='pickle')
#mod3.save(op.join(outdir,"ddm_model23"))

# save
fhandler = open(op.join(outdir,"ddm_model23"),"wb")
pickle.dump(mod3, fhandler)
fhandler.close()


# %% Inspect posteriors
mod1.plot_posteriors()
mod2.plot_posteriors()
mod3.plot_posteriors()

mod1.plot_posterior_predictive()
mod2.plot_posterior_predictive()

print('DIC model1 = ', mod1.dic)
print('DIC model2 = ', mod2.dic)
print('DIC model3 = ', mod3.dic)

# %% Get R-hat [NB re-run due to save errors]
#models = []
#for i in range(3):
#    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition']})
#    m.find_starting_values()
#    m.sample(10000, burn=2000, dbname='traces21_'+str(i)+'.db', db='pickle')
#    models.append(m)
#models.append(mod1)
#with open(op.join(outdir,'modelsGR1.pkl'),'wb') as fb:
#    pickle.dump(models,fb)

mod2 = hddm.load(op.join(outdir, 'ddm_model22'))
    
models = []
for i in range(3):
    m = hddm.HDDM(data, include='z', depends_on ={'v': ['type','volition'], 'a':['type','volition'], 'z':['type','volition'], 't':['type','volition']})
    m.find_starting_values()
    m.sample(10000, burn=2000, dbname='traces22_'+str(i)+'.db', db='pickle')
    models.append(m)
models.append(mod2)

# save
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

# Gelman-Rubin model diagnostics
gelman_rubin(models) 

# %% Load (/NOT WORKING)
chdir(outdir) #Must be in folder to load databases
#mod1 = hddm.load(op.join(outdir, 'ddm_model21'))
mod = hddm.load(op.join(outdir, 'ddm_model22'))

# %% Summary and plots
# Compare DIC (not useful)
#print 'DIC model1 = ', mod1.dic
print('DIC model2 = ', mod.dic)

# Get statistics from posterior
stats = mod.gen_stats()
mod.print_stats()
mod.get_group_nodes()

# Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
z_fixPM, z_freePM, z_fixFil, z_freeFil  = mod.nodes_db.node[['z(pm.fix)', 'z(pm.free)','z(filler.fix)','z(filler.free)']]
t_fixPM, t_freePM, t_fixFil, t_freeFil  = mod.nodes_db.node[['t(pm.fix)', 't(pm.free)','t(filler.fix)','t(filler.free)']]

#z_PM, z_Fil  = mod.nodes_db.node[['z(pm)', 'z(filler)']]
#t = mod.nodes_db.node['t']

# %% Statistics
# Get P and generate difference distribtions (plots only for inspection)

# PM trials: Fix vs Free
P = pm.get_posteriorP(a_fixPM, a_freePM, plot=0)
P = pm.get_posteriorP(v_fixPM, v_freePM, plot=0)
P = pm.get_posteriorP(z_fixPM, z_freePM, plot=0)
P = pm.get_posteriorP(t_fixPM, t_freePM, plot=0)

# Filler trials: Fix vs Free
P = pm.get_posteriorP(a_fixFil, a_freeFil, plot=0)
P = pm.get_posteriorP(v_fixFil, v_freeFil, plot=0)
P = pm.get_posteriorP(z_fixFil, z_freeFil, plot=0)
P = pm.get_posteriorP(t_fixFil, t_freeFil, plot=0)

# Fixed: PM vs. Filler
P = pm.get_posteriorP(a_fixPM, a_fixFil, plot=0)
P = pm.get_posteriorP(v_fixPM, v_fixFil, plot=0)
P = pm.get_posteriorP(z_fixPM, z_fixFil, plot=0)
P = pm.get_posteriorP(t_fixPM, t_fixFil, plot=0)

# Free: PM vs. filler
P = pm.get_posteriorP(a_freePM, a_freeFil, plot=0)
P = pm.get_posteriorP(v_freePM, v_freeFil, plot=0)
P = pm.get_posteriorP(z_freePM, z_freeFil, plot=0)
P = pm.get_posteriorP(t_freePM, t_freeFil, plot=0)

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

bnd = pm.get_hpdi(t_fixPM, hpdi)
bnd = pm.get_hpdi(t_freePM, hpdi)
bnd = pm.get_hpdi(t_fixFil, hpdi)
bnd = pm.get_hpdi(t_freeFil, hpdi)

#END