#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Plot posterior od DDM
Created on Sat Dec  8 11:50:04 2018. @author: mikkel
"""
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import hddm
import pickle
from os import chdir
import os.path as op
workdir = '/home/mikkel/PM-volition/Dataanalysis'
outdir = '/home/mikkel/PM-volition/Datafiles'
import sys
sys.path.append(workdir)
import PM_volition_utilfun as pm # plot_posterior_diff, plot_posterior_nodes2, get_posteriorP

# %% Load model
chdir(outdir)                   #Must be in folder to load databases
mod = hddm.load(op.join(outdir, 'ddm_model22'))

f = open(op.join(outdir,"ddm_model22"),"rb")
mod = pickle.load(f)

# %% Generate posteriors
v_fixPM, v_freePM, v_fixFil, v_freeFil  = mod.nodes_db.node[['v(pm.fix)', 'v(pm.free)','v(filler.fix)','v(filler.free)']]
a_fixPM, a_freePM, a_fixFil, a_freeFil  = mod.nodes_db.node[['a(pm.fix)', 'a(pm.free)','a(filler.fix)','a(filler.free)']]
z_fixPM, z_freePM, z_fixFil, z_freeFil  = mod.nodes_db.node[['z(pm.fix)', 'z(pm.free)','z(filler.fix)','z(filler.free)']]
t_fixPM, t_freePM, t_fixFil, t_freeFil  = mod.nodes_db.node[['t(pm.fix)', 't(pm.free)','t(filler.fix)','t(filler.free)']]


_, v_PMdiff = pm.get_posteriorP(v_fixPM,v_freePM, plot=0)
_, a_PMdiff = pm.get_posteriorP(a_fixPM,a_freePM, plot=0)
_, z_PMdiff = pm.get_posteriorP(z_fixPM,z_freePM, plot=0)
_, t_PMdiff = pm.get_posteriorP(a_fixPM,a_freePM, plot=0)

#_, z_diff = pm.get_posteriorP(z_PM,z_Fil, plot=1)

# %% Plots
# Posterior plots
dpi=600

# v
pm.plot_posterior_nodes2([v_fixPM, v_freePM, v_fixFil, v_freeFil],lb=2.0, ub=4.0,shade=False)
plt.ylim(-0.05*6,6)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Drift rate ($\it{v}$)',fontsize=14)
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'v_post2'),dpi=dpi)

# a
pm.plot_posterior_nodes2([a_fixPM, a_freePM, a_fixFil, a_freeFil],lb=1.2, ub=2.6,shade=False)
plt.ylim(-0.05*10,10)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Decision threshold ($\it{a}$)',fontsize=14)
plt.legend(['PM-cue: Fixed','PM-cue: Free','Filler: Fixed','Filler: Free'], fontsize=8, loc=0, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'a_post2'),dpi=dpi)

# z
pm.plot_posterior_nodes2([z_PM, z_Fil], lb=0.1, ub=0.6,shade=False)
plt.ylim(-0.05*60,60)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Bias ($\it{z}$)', fontsize=14)
plt.legend(['PM-cue','Filler'], fontsize=8, loc=0, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'z_post'),dpi=dpi)

# t
pm.plot_posterior_nodes2([t], lb=0.1, ub=0.5, shade=False)
plt.ylim(-0.05*50,50)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Value',fontsize=12)
plt.title('Non-decision time ($\it{t}$)',fontsize=14)
plt.legend(['t'], fontsize=8, loc=0, edgecolor='white')
#plt.tight_layout()
plt.savefig(op.join(outdir,'t_post'),dpi=dpi)

# Posterior differences
pm.plot_posterior_diff(v_PMdiff,lb=-1, ub=1)
plt.ylim(-0.05*3.5,3.5)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Difference',fontsize=12)
plt.title('Drift rate ($\it{Fixed}$ - $\it{Free}$)',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'v_PMdiff'),dpi=dpi)

pm.plot_posterior_diff(a_PMdiff,lb=-0.5, ub=0.5)
plt.ylim(-0.05*7,7)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Difference',fontsize=12)
plt.title('Decision threshold ($\it{Fixed}$ - $\it{Free}$)',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'a_PMdiff'),dpi=dpi)

pm.plot_posterior_diff(z_diff)
plt.ylim(-0.05*45,45)
plt.ylabel('Density',fontsize=12)
plt.xlabel('Difference',fontsize=12)
plt.title('Bias ($\it{PM}$ - $\it{Filler}$)',fontsize=14)
plt.tight_layout()
plt.savefig(op.join(outdir,'z_diff'),dpi=dpi)
