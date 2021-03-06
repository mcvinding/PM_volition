#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Plot posterior od DDM. Created on Sat Dec 8 11:50:04 2018.
@author: mcvinding
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
%matplotlib qt
import hddm
#import pickle
from os import chdir
import os.path as op
import sys

#workdir = '/home/mikkel/PM-volition/Dataanalysis'
#outdir = '/home/mikkel/PM-volition/Datafiles'

workdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Dataanalysis'
outdir = 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Datafiles'

sys.path.append(workdir)
import PM_volition_utilfun as pm # plot_posterior_diff, plot_posterior_nodes2, get_posteriorP

# %% Plot options
dpi=600

# %% Load model
chdir(outdir)                   #Must be in folder to load databases
mod = hddm.load(op.join(outdir, 'ddm_model31'))

#f = open(op.join(outdir,"ddm_model22"),"rb")
#mod = pickle.load(f)

#%% Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fix, a_free = mod.nodes_db.node[['a(fix)', 'a(free)']]
t_int  = mod.nodes_db.node['t']

## Difference between posteriors: PM
_, v_PMdiff = pm.get_posteriorP(v_fixPM, v_freePM, plot=0)
_, v_Fildiff = pm.get_posteriorP(v_fixFil, v_freeFil, plot=0)
_, a_diff = pm.get_posteriorP(a_fix, a_free, plot=0)

#_, z_PMdiff = pm.get_posteriorP(z_fixPM, z_freePM, plot=0)
#_, t_PMdiff = pm.get_posteriorP(t_fixPM, t_freePM, plot=0)
#
## Difference between posteriors: Filler
#_, v_Fildiff = pm.get_posteriorP(v_fixFil, v_freeFil, plot=0)
#_, a_Fildiff = pm.get_posteriorP(a_fixFil, a_freeFil, plot=0)
#_, z_Fildiff = pm.get_posteriorP(z_fixFil, z_freeFil, plot=0)
#_, t_Fildiff = pm.get_posteriorP(t_fixFil, t_freeFil, plot=0)
#
## Difference between posteriors: fixed
#_, v_fixdiff = pm.get_posteriorP(v_fixFil, v_fixPM, plot=0)
#_, a_fixdiff = pm.get_posteriorP(a_fixFil, a_fixPM, plot=0)
#_, z_fixdiff = pm.get_posteriorP(z_fixFil, z_fixPM, plot=0)
#_, t_fixdiff = pm.get_posteriorP(t_fixFil, t_fixPM, plot=0)
#
## Difference between posteriors: free
#_, v_freediff = pm.get_posteriorP(v_freeFil, v_freePM, plot=0)
#_, a_freediff = pm.get_posteriorP(a_freeFil, a_freePM, plot=0)
#_, z_freediff = pm.get_posteriorP(z_freeFil, z_freePM, plot=0)
#_, t_freediff = pm.get_posteriorP(t_freeFil, t_freePM, plot=0)

# %% Posterior plots
# v
pm.plot_posterior_nodes2([v_fixPM, v_freePM, v_fixFil, v_freeFil],lb=1.20, ub=3.0,shade=False)
plt.ylim(-0.05*7, 7)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Drift rate ($\it{v}$)',fontsize=14)
plt.legend(['PM-cue: No-choice','PM-cue: Choice','Filler: No-choice','Filler: Choice'], fontsize=8, loc='best', edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'v_post2'), dpi=dpi)

# a
pm.plot_posterior_nodes2([a_fix, a_free],lb=1.4, ub=2.2,shade=False)
plt.ylim(-0.05*8, 8)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Boundary separation ($\it{a}$)',fontsize=14)
plt.legend(['No-choice','Choice'], fontsize=8, loc=2, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'a_post2'), dpi=dpi)

# z
#pm.plot_posterior_nodes2([z_fix, z_free], lb=0.3, ub=0.50,shade=False)
#plt.ylim(-0.05*45,45)
#plt.ylabel('Density',fontsize=12)
#plt.xlabel('Value',fontsize=12)
#plt.title('Bias ($\it{z}$)', fontsize=14)
#plt.legend(['Fixed','Free',], fontsize=8, loc=0, edgecolor='white')
##plt.tight_layout()
#plt.savefig(op.join(outdir,'z_post'),dpi=dpi)

# t
pm.plot_posterior_nodes2([t_int], lb=0.2, ub=0.375, shade=False)
plt.ylim(-0.05*40, 40)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Non-decision time ($\it{t}$)',fontsize=14)
plt.legend(['Intercept'], fontsize=8, loc=2, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'t_post'), dpi=dpi)

#%% Posterior differences
# Posterior differences: PM
pm.plot_posterior_diff(a_diff,lb=-1, ub=1)
plt.ylim(-0.05*6,6)
plt.ylabel('Density', fontsize=12)
plt.xlabel('Difference', fontsize=12)
plt.title('Boundary separation ($\it{a}$)',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'a_diff'),dpi=dpi)

pm.plot_posterior_diff(v_PMdiff,lb=-1, ub=1)
plt.ylim(-0.05*5, 5)
plt.ylabel('Density', fontsize=12)
plt.xlabel('Difference', fontsize=12)
plt.title('Drift rate ($\it{v}$): PM cues',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'v_PMdiff'),dpi=dpi)

#pm.plot_posterior_diff(z_PMdiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Bias ($\it{z}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'z_PMdiff'),dpi=dpi)

#pm.plot_posterior_diff(t_PMdiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Non-decision time ($\it{t}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'t_PMdiff'),dpi=dpi)

## Posterior differences: Fil
#pm.plot_posterior_diff(a_Fildiff,lb=-0.5, ub=0.5)
#plt.ylim(-0.05*8,8)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Decision threshold ($\it{a}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'a_Fildiff'),dpi=dpi)

pm.plot_posterior_diff(v_Fildiff,lb=-1, ub=1)
plt.ylim(-0.05*5, 5)
plt.ylabel('Density', fontsize=12)
plt.xlabel('Difference', fontsize=12)
plt.title('Drift rate ($\it{v}$): filler trials',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'v_Fildiff'),dpi=dpi)

#pm.plot_posterior_diff(z_Fildiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Bias ($\it{z}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'z_Fildiff'),dpi=dpi)
#
#pm.plot_posterior_diff(t_Fildiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Non-decision time ($\it{t}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'t_Fildiff'),dpi=dpi)
#
## Posterior differences: Fixed
#pm.plot_posterior_diff(a_fixdiff,lb=-0.5, ub=0.5)
#plt.ylim(-0.05*8,8)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Decision threshold ($\it{a}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'a_fixdiff'),dpi=dpi)
#
#pm.plot_posterior_diff(v_fixdiff)
#plt.ylim(-0.05*3.5, 3.5)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Drift rate ($\it{v}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'v_fixdiff'),dpi=dpi)
#
#pm.plot_posterior_diff(z_fixdiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Bias ($\it{z}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'z_fixdiff'),dpi=dpi)
#
#pm.plot_posterior_diff(t_fixdiff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Non-decision time ($\it{t}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'t_fixdiff'),dpi=dpi)
#
## Posterior differences: Free
#pm.plot_posterior_diff(a_freediff)
#plt.ylim(-0.05*8,8)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Decision threshold ($\it{a}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'a_freediff'),dpi=dpi)
#
#pm.plot_posterior_diff(v_freediff)
#plt.ylim(-0.05*3.5, 3.5)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Drift rate ($\it{v}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'v_freediff'),dpi=dpi)
#
#pm.plot_posterior_diff(z_freediff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Bias ($\it{z}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'z_freediff'),dpi=dpi)
#
#pm.plot_posterior_diff(t_freediff)
#plt.ylim(-0.05*30, 30)
#plt.ylabel('Density', fontsize=12)
#plt.xlabel('Difference', fontsize=12)
#plt.title('Non-decision time ($\it{t}$)',fontsize=14)
#plt.tight_layout()
#plt.savefig(op.join(outdir,'t_freediff'),dpi=dpi)

#%%
plt.close('all')

#END