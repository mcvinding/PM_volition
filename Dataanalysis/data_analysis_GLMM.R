#PM-volition dataanalysis (GLMM analysis - initial inspection)
###
rm(list=ls())

#Set up foldersd  
data.folder <-  '/home/mikkel/Dropbox/PM-volition/PM-volition data files/'
out.folder <- '/home/mikkel/Dropbox/PM-volition/Dataanalysis/'
setwd(out.folder)
load(file='raw_data.RData')

#Libraries
library(lme4)
library(arm)
# library("lattice")
library(brms)

# Prepare data
x.data$log.rt <- log(x.data$rt)
x.data$meanChoiceTime <- x.data$choice_rt/x.data$choice_shifts
x.data <- subset(x.data, pm_first!="")
x.data$pm_first <- droplevels(x.data$pm_first)
x.data$valid = x.data$rt.ms < 2000 & x.data$rt.ms > 150
x.data$gender <- factor(x.data$gender)
x.data$response <- factor(x.data$response)
x.data$pm_shape <- factor(x.data$response)
x.data$correct_answer <- factor( x.data$correct_answer)
str(x.data)
summary(x.data)

x.data.rtclip <- x.data[x.data$rt.ms < 2000 & x.data$rt.ms > 150,] # Remove implausible reaction times: 200 ms < RT < 2000 ms

free.data <- x.data.rtclip[x.data.rtclip$volition=="free",]   # Only free-choice conditions
free.data.choice <- subset(free.data, choice_shifts >= 1)
pm.data <- x.data.rtclip[x.data.rtclip$type == "pm",]

save(file='rtData.R',x.data.rtclip)

#REACTION TIME ANALYSIS (ALL DATA) DO NOT RUN AGAIN UNLESS NECESSARY (takes ~1 hour)
# load(file='rtData.R')
# load(file='Workspace.RData')

# Lmer model
# rt.mod.full <- lmer(log.rt~type*volition +
#                    (type*volition|subj)+(1|shape)+(1|color)+(1|pm_first),
#                  data = x.data.rtclip, subset = practice == F,verbose=T, REML=F)
# 
# rt.mod.2 <- update(rt.mod.full, .~. -type:volition)
# rt.mod.1 <- update(rt.mod.2, .~. -volition)
# rt.mod.0 <- update(rt.mod.1, .~. -type)
# 
# anova(rt.mod.0,rt.mod.1,rt.mod.2,rt.mod.full)
# 
# qqplot(resid(rt.mod.full),fitted(rt.mod.full))
# qqline(resid(rt.mod.full),fitted(rt.mod.full))
# 
# dotplot(ranef(rt.mod.full, condVar=TRUE))

# Extended lmer model (choice RT as fixed)
# rt.mod.ChoVol1 <- update(rt.mod.full, .~. +choice_rt)
# rt.mod.ChoVolX <- update(rt.mod.ChoVol1, .~. +volition:choice_rt)
# rt.mod.ChoVolXX <- update(rt.mod.ChoVolX, .~. +type:choice_rt)
# rt.mod.ChoVolXXX <- update(rt.mod.ChoVolXX, .~. +type:choice_rt:volition)
# 
# anova(rt.mod.full,rt.mod.ChoVol1,rt.mod.ChoVolX,rt.mod.ChoVolXX,rt.mod.ChoVolXXX)
# 
# dotplot(ranef(rt.mod.ChoVolXXX, condVar=TRUE))
# 
# rt.mod.switch <- update(rt.mod.0, .~. -(1|choice_shifts)+choice_shifts)

#Full random effects (choice shifts as fixed) -----### DOES NOT WORK! ####-----
# Test effects
# rt.mod.ChsVol1 <- update(rt.mod.0F, .~. +choice_shifts)
# rt.mod.ChsVol2 <- update(rt.mod.ChsVol1, .~. +volition)
# rt.mod.ChsVolX <- update(rt.mod.ChsVol2, .~. +volition:choice_shifts)
# rt.mod.ChsVolX1 <- update(rt.mod.ChsVolX, .~. +type)
# rt.mod.ChsVolXX1 <- update(rt.mod.ChsVolX1, .~. +type:choice_shifts)
# rt.mod.ChsVolXX2 <- update(rt.mod.ChsVolXX1, .~. +type:volition)
# rt.mod.ChsVolXXX <- update(rt.mod.ChsVolXX2, .~. +type:choice_shifts:volition)
# 
# anova(rt.mod.0F,rt.mod.ChsVol1,rt.mod.ChsVol2,rt.mod.ChsVolX,rt.mod.ChsVolX1,rt.mod.ChsVolXX1,rt.mod.ChsVolXX2,rt.mod.ChsVolXXX)
# 
# dotplot(ranef(rt.mod.ChoVolXXX, postVar=TRUE))

###########################################################
###                    BAYES FACTOR
###########################################################
library(BayesFactor)
load(file='rtData.R')
load(file='Workspace.RData')
load(file='rt_analysis.RData')

# Main analysis
BF.full = anovaBF(log.rt~type*volition+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T, multicore=T)    #Note: Progress bars and callbacks are suppressed when running multicore.

BF.type <- BF.full[2]
BF.voli <- BF.full[3]/BF.type
BF.volXtype <- BF.full[4]/BF.full[3]

BF.vsType <- BF.full/BF.full[2]

# get posterior
BF.full.post = posterior(BF.full, index=4, iterations=10000, progress=T)

# TO DO
# * mean+CI from posterior

### Include choice_rt ###
BF.Chs0 = lmBF(log.rt~type+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)
BF.Chs1 = lmBF(log.rt~type+choice_rt+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)
BF.Chs2 = lmBF(log.rt~type+volition+choice_rt+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)
BF.Chs2a = lmBF(log.rt~type+volition*choice_rt+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)
BF.Chs2b = lmBF(log.rt~volition+type*choice_rt+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)
BF.Chs2c = lmBF(log.rt~volition+type+choice_rt+volition:choice_rt+type:choice_rt+subj+shape+color,
                whichRandom = c('subj','shape','color'), data=x.data.rtclip,
                progress=T)
BF.Chs3 = lmBF(log.rt~type*volition*choice_rt+subj+shape+color,
               whichRandom = c('subj','shape','color'), data=x.data.rtclip,
               progress=T)

# Summary
bf0t <- BF.Chs0t/BF.Chs0
bf.crt <- BF.Chs1/BF.Chs0
bf.crt
bf.vol <- BF.Chs2/BF.Chs1
bf.vol
bf.2a <- BF.Chs2a/BF.Chs2
bf.2a
bf.2b <- BF.Chs2b/BF.Chs2
bf.2b
bf.2c <- BF.Chs2c/BF.Chs2
bf.2c
bf.full <- BF.Chs3/BF.Chs2
bf.full

# Save everything...
setwd(out.folder)
save(file='rt_analysis.RData', BF.full, BF.full.post, BF.Chs0,BF.Chs1,BF.Chs2,BF.Chs2a,BF.Chs2b,BF.Chs2c,BF.Chs3)
save.image("Workspace.RData")

############################################################
################ CORRECT (all data) ########################
############################################################
library(brms)
load(file='rtData.R')
load(file='Workspace.RData')

mhit.mot.3 = brm(score~type*volition + (1|subj) + (1|shape) + (1|color), data = x.data.rtclip, family = bernoulli(), save_all_pars = TRUE)
mhit.mot.2 = update(mhit.mot.3, formula = ~. - type:volition)
mhit.mot.1 = update(mhit.mot.2, formula = ~. - volition)
mhit.mot.0 = update(mhit.mot.1, formula = ~. - type)

bf.type <- bayes_factor(mhit.mot.1, mhit.mot.0)
bf.voli<- bayes_factor(mhit.mot.2, mhit.mot.1)
bf.int <- bayes_factor(mhit.mot.3, mhit.mot.2)
bf.int0 <- bayes_factor(mhit.mot.3, mhit.mot.1)


# TO DO
# * mean+CI from posterior
setwd(out.folder)
save(file='hit_analysis.RData', mhit.mot.3, mhit.mot.2, mhit.mot.1,mhit.mot.0,bf.type,bf.voli,bf.int,bf.int0)
save.image("Workspace.RData")






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





