# ----------------------------------------------------------- #
# PM-volition dataanalysis data-cleaning. Get summaries:
# * N-trial summary
# * Subject performance
# ----------------------------------------------------------- #
rm(list=ls())

#Set up foldersd  
out.folder <- '/home/mikkel/PM-volition/Datafiles/'
out.folder <- 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Datafiles'
setwd(out.folder)
load(file='raw_data.RData')

x.data <- read.csv("raw_data.csv", sep=",",header=T)
x.data$subj <- as.factor(x.data$subj)

x.data <- subset(x.data, x.data$practice==F)  # Remove practice trials

## Removing outlines on subject by subject basis
ntrials <- data.frame(sub=unique(x.data$subj))
ntrials$orig <- 0
ntrials$good <- 0

# # Remove (pre-set curoff)
x.data$valid.RT <- x.data$rt.ms < 2500 & x.data$rt.ms > 150

for (sub in unique(x.data$subj)) {
  ntrials$orig[ntrials$sub==sub] <- length(x.data$rt.ms[x.data$subj==sub])
  ntrials$good[ntrials$sub==sub] <- sum(x.data$valid.RT[x.data$subj==sub])
}

summary(ntrials)
summary(x.data)

# Remove outliers
x.data.rtclip <- subset(x.data, valid.RT == 1)    # Remove outliers (RT)

### --------------------------------------------------------------------- ###
### Get summary of reaction time and %-correct (before removing bad subject)
## %-correct
tasks <-  c('Free (PM) ', 'Free (filler)', 'Fixed (PM)', 'Fixed (filler)')

prob.dat <- data.frame()
for (jj in levels(x.data.rtclip$subj)){
  x.sub <- subset(x.data.rtclip, x.data.rtclip$subj==jj)
  sub.tab.free <- prop.table(xtabs(~score+type,data=x.sub, subset=volition=='free'),2)
  sub.tab.fix <- prop.table(xtabs(~score+type,data=x.sub, subset=volition=='fix'),2)
  
  subj <- rep(jj,4)
  dat <- c(sub.tab.free[4],sub.tab.free[2],sub.tab.fix[4],sub.tab.fix[2])
  SS <- data.frame(subj,tasks,dat)
  
  prob.dat <- rbind(prob.dat,SS)
}

# See bad subject performance
subset(prob.dat, subj=='8')

## ---------------------------------------------------------------------- ##
### Get summary of reaction time and %-correct (after removing bad subject)
# Remove bad subject
x.data.rtclip <- subset(x.data.rtclip, subj != '8')
x.data.rtclip$subj <- droplevels(x.data.rtclip$subj)
ntrials <- subset(ntrials, sub != '8')
prob.dat <- subset(prob.dat, subj != '8')

# N-tirals summary
ntrials$removed <- ntrials$orig-ntrials$good
range(ntrials$good)
median(ntrials$good)
range(ntrials$removed)
median(ntrials$removed)
sum(x.data$valid.RT)

## Summary of %-correct
aggregate(dat~tasks, FUN=mean, data=prob.dat)
aggregate(dat~tasks, FUN=range, data=prob.dat)

## RT
rt.dat <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),median)
rt.dat.sd <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),sd)

names(rt.dat) <- c("volition","task","subj","RT")
rt.dat$sd <- rt.dat.sd$x
rt.dat$tasks <- factor(paste(rt.dat$volition,rt.dat$task), levels = c("free pm", "free filler", "fix pm", "fix filler"))
levels(rt.dat$tasks) <- tasks

aggregate(rt.dat$RT, list(rt.dat$tasks), range)
aggregate(rt.dat$RT, list(rt.dat$tasks), mean)
aggregate(rt.dat$RT, list(rt.dat$tasks), sd)

# Get PM trials only
PM.data <- subset(x.data.rtclip, type=="pm")

### -------------------------------SAVE--------------------------------- ###
# Save
save(x.data.rtclip, file='cln_data2.RData')
save(PM.data, file='PM_data.RData')

# Export data for HDDM in Python (export to csv)
out.name <- paste0(out.folder,'\\alldata2.csv')
write.csv(x.data.rtclip, file=out.name)
out.name2 <- paste0(out.folder,'\\PM_data.csv')
write.csv(PM.data, file=out.name2)

# END