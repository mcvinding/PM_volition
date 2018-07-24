#PM-volition dataanalysis (GLMM analysis - initial inspection)
###
rm(list=ls())

#Set up foldersd  
data.folder <-  '/home/mikkel/PM-volition/PM-volition data files/'
out.folder <- '/home/mikkel/PM-volition/Dataanalysis/'
setwd(out.folder)
load(file='cln_data.RData')

#Libraries
library(lme4)
library(arm)
# library("lattice")
library(brms)

# Prepare data (unused)
str(x.data.rtclip)
summary(x.data.rtclip)

free.data <- x.data.rtclip[x.data.rtclip$volition=="free",]   # Only free-choice conditions
free.data.choice <- subset(free.data, choice_shifts >= 1)
pm.data <- x.data.rtclip[x.data.rtclip$type == "pm",]

############################################################
################ CORRECT (all data) ########################
############################################################
library(brms)
load(file='Workspace.RData')

mhit.mot.3 = brm(score~type*volition + (1|subj) + (1|shape) + (1|color), data = x.data.rtclip,
                 family = bernoulli(), save_all_pars = TRUE, iter=20000, warmup=2000)
mhit.mot.2 = update(mhit.mot.3, formula = ~. - type:volition)
mhit.mot.1 = update(mhit.mot.2, formula = ~. - volition)
mhit.mot.0 = update(mhit.mot.1, formula = ~. - type)

bf.type <- bayes_factor(mhit.mot.1, mhit.mot.0)
bf.voli<- bayes_factor(mhit.mot.2, mhit.mot.1)
bf.int <- bayes_factor(mhit.mot.3, mhit.mot.2)
bf.int0 <- bayes_factor(mhit.mot.3, mhit.mot.1)

# Save models and BF
setwd(out.folder)
save(file='hit_analysis.RData', mhit.mot.3, mhit.mot.2, mhit.mot.1,mhit.mot.0,bf.type,bf.voli,bf.int,bf.int0)
# save.image("Workspace.RData")

# TO DO
# * mean+CI from posterior

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
#PM-only
hit.mod.pm.0 <- glmer(score~1 + (1|subj) + (1|color) + (1|pm_first) + (1|shape), data = pm.data, family = 'binomial')
dotplot(ranef(hit.mod.pm, postVar=TRUE))

hit.mod.pm.1 <- update(hit.mod.pm.0, .~. +choice_rt)
hit.mod.pm.2 <- update(hit.mod.pm.1, .~. +volition)
hit.mod.pm.x <- update(hit.mod.pm.2, .~. +volition:choice_rt)

anova(hit.mod.pm.0,hit.mod.pm.1,hit.mod.pm.2,hit.mod.pm.x)

dotplot(ranef(hit.mod.pm.x, postVar=TRUE))


hit.mod.pm <- glmer(score~volition)
#////////////////////////////////////////////////////////////////////////////////

setwd(out.folder)
save.image("Workspace.RData")





