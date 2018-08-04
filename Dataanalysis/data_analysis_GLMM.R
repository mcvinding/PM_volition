#PM-volition dataanalysis (GLMM analysis - initial inspection)
###
rm(list=ls())

#Set up foldersd  
out.folder <- '/home/mikkel/PM-volition/Datafiles/'
setwd(out.folder)
load(file='cln_data.RData')

#Libraries
library(brms)
library(ggplot2)
library(mcmcse)
library(sjstats)
source('/home/mikkel/PM-volition/Dataanalysis/publish_theme.vs2.R')

# Get estimate of N-samples needed
minESS(p = 42)

############################################################
################ CORRECT (all data) ####   ####################
############################################################
# load(file='Workspace.RData')

mhit.mot.3 = brm(score~type*volition + (1|subj) + (1|shape) + (1|color), data = x.data.rtclip,
                 family = bernoulli(), save_all_pars = TRUE, iter=10000, warmup=2000, cores=4)
mhit.mot.2 = update(mhit.mot.3, formula = ~. - type:volition,
                    save_all_pars = TRUE, iter=10000, warmup=2000, cores=4)
mhit.mot.1 = update(mhit.mot.2, formula = ~. - volition,
                    save_all_pars = TRUE, iter=10000, warmup=2000, cores=4)
mhit.mot.0 = update(mhit.mot.1, formula = ~. - type,
                    save_all_pars = TRUE, iter=10000, warmup=2000, cores=4)
# Diagnostics
print(mhit.mot.3)
print(mhit.mot.2)
print(mhit.mot.1)
print(mhit.mot.0)

# get HDI
hdi(mhit.mot.3, prob = c(0.67, 0.89, 0.97), type="fixed")
# equi_test(mhit.mot.3, out = "plot", type = "fixed", rope=c(-.20,.20))  #ROPE makes no sense here

# Bayes Factors
bf.type <- bayes_factor(mhit.mot.1, mhit.mot.0)
bf.voli <- bayes_factor(mhit.mot.2, mhit.mot.1)
bf.int2 <- bayes_factor(mhit.mot.3, mhit.mot.2)
bf.int1 <- bayes_factor(mhit.mot.3, mhit.mot.1)

# Save models and BF
setwd(out.folder)
save(file='hit_analysis.RData', mhit.mot.3, mhit.mot.2, mhit.mot.1,mhit.mot.0,bf.type,bf.voli,bf.int2,bf.int1)
# save.image("Workspace.RData")

# Plot
stanplot(mhit.mot.3, type="areas",pars = "^b_")+publish_theme
stanplot(mhit.mot.3, type="dens",pars = "^b_")+publish_theme
stanplot(mhit.mot.3, type="dens_overlay")+publish_theme
# stanplot(mhit.mot.3, type="nuts_divergence") 


### --------------------------------------------------------------------------------- ###
### OLD: Use glmer and compare using BIC (cf. Wagenmakers 2007)
mhit.mot.3 <- glmer(score~type*volition + (1|subj) + (1|color) + (1|shape),
                      data = x.data.rtclip,family = 'binomial')
mhit.mot.2 <- update(mhit.mot.xxx, ~. -type:volition)
mhit.mot.1 <- update(mhit.mot.2, ~. -volition)
mhit.mot.0 <- update(mhit.mot.1, ~. -type)

anova(mhit.mot.xxx,mhit.mot.2,mhit.mot.1,mhit.mot.0)

# Bayes factors from BIC (?)
bfBIC.type <- exp((BIC(mhit.mot.0) - BIC(mhit.mot.1))/2)
bfBIC.type
bfBIC.vol <- exp((BIC(mhit.mot.1) - BIC(mhit.mot.2))/2)
bfBIC.vol
# bfBIC.x <- exp((BIC(mhit.mot.2) - BIC(mhit.mot.3))/2)
# bfBIC.x
bfBIC.xx <- exp((BIC(mhit.mot.1) - BIC(mhit.mot.3))/2)
bfBIC.xx

# Save everything...
setwd(out.folder)
save.image("Workspace.RData")

############################################################################################################

setwd(out.folder)
save.image("Workspace.RData")





