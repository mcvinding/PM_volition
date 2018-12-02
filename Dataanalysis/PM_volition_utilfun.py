#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 09:47:59 2018
@author: mikkel
"""
import matplotlib.pyplot as plt
import numpy as np
#import hddm
from scipy.stats import gaussian_kde
import pymc as pc  


def get_posteriorP(x,y,plot=0):
    diff = x.trace() - y.trace()
    P = (diff > 0).mean()
    if P > 0.5:
        P = 1-P        
    P = P*2     #Two-tailed        
    print ": v P(x-y = 0) = ", P
    if plot:
        plot_posterior_diff(diff)        
    return P, diff

def get_hpdi(node, hpdi=0.97):
    if 'pymc' in type(node).__module__:
        data = node.trace()
    elif type(node).__module__ == 'pandas.core.series':
        data = node.copy()
    elif type(node).__module__ == 'numpy':
        data = node.copy()
    bnd = pc.utils.hpd(data, 1-hpdi)
    avg = round(np.mean(data),3)
    mdn = round(np.median(data),3)
    
    print('Mean =\t %s\nMedian = %s\n%s%% HPDI: %s' % (avg,mdn,hpdi,bnd))
    return bnd  

    
def plot_posterior_nodes2(nodes, bins=100, lb=None, ub=None, shade=1):
    plt.figure(figsize=(6,4))
    if lb is None:
        lb = min([min(node.trace()[:]) for node in nodes])
    if ub is None:
        ub = max([max(node.trace()[:]) for node in nodes])

    xs = np.linspace(lb, ub, bins)
    cmap = plt.cm.tab10
    for i,node in enumerate(nodes):
        trace = node.trace()[:]
        dens = gaussian_kde(trace)
        dens.covariance_factor = lambda : .25
        dens._compute_covariance()

        c = cmap(i)
#        plt.axvline(np.median(node), ls='--', color=c,alpha=0.8)
        plt.plot(xs, dens(xs), label=node.__name__, lw=2,color=c)
        if shade:
            plt.fill_between(xs,dens(xs),0, alpha=0.3,color=c)

    leg = plt.legend(loc='best', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    

def plot_posterior_diff(diff, bins=100, lb=None, ub=None, shade=True):
    plt.figure(figsize=(4,4))
    if lb is None:
        lx = min(diff)
        if lx > 0:
            lx = 0
        lb = 1.5*lx
    if ub is None:
        ux = max(diff)
        if ux < 0:
            ux = 0
        ub = 1.5*ux

    xs = np.linspace(lb, ub, bins)
    dens = gaussian_kde(diff)
    dens.covariance_factor = lambda : .25
    dens._compute_covariance()
    hpdi=get_hpdi(diff)

    plt.axvline(0, ls='--', color='k',alpha=0.6)
    plt.plot(xs, dens(xs), lw=2, color='k')
    if shade:
        plt.fill_between(xs,dens(xs),0, alpha=0.2,color='b')
    plt.hlines(0,hpdi[0],hpdi[1],lw=5,color='k',linestyles='-')
