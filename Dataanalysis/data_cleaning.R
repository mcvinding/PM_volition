# ----------------------------------------------------------- #
#PM-volition dataanalysis data-cleaning. Get summaries:
# * N-trial summary
# ----------------------------------------------------------- #
rm(list=ls())

#Set up foldersd  
out.folder <- '/home/mikkel/PM-volition/Datafiles/'
setwd(out.folder)
load(file='raw_data.RData')

x.data <- subset(x.data, x.data$practice==F)  # Remove practice trials
x.data$log.rt <- log(x.data$rt)
x.data$meanChoiceTime <- x.data$choice_rt/x.data$choice_shifts

## Testing robust methods for removing outlines
ntrials <- data.frame(sub=unique(x.data$subj))
ntrials$orig <- 0
ntrials$good <- 0

# # Remove (pre-set)
# x.data$valid.RT <- x.data$rt.ms < 1500 & x.data$rt.ms > 150
# x.data$valid.choice_shifts <- x.data$choice_shifts >= 1 | x.data$volition =="fix"

# # Remove (quantiles)
# x.data$valid.qt <- logical(1)
# for (sub in unique(x.data$subject)) {
#   temp <- x.data$rt.ms[x.data$subject==sub]
#   qnt <- quantile(temp,c(0.025,0.975))
#   good <- temp > qnt[1] & temp < qnt[2]
#   x.data$valid.qt[x.data$subject==sub] <- good
# }

# Remove (log-trans +/- 2sd; Ratcliff, 1993) USING THIS
x.data$valid.sd <- logical(1)
for (sub in unique(x.data$subj)) {
  temp <- x.data$log.rt[x.data$subj==sub]
  cut <- c(mean(temp)-2*sd(temp), mean(temp)+2*sd(temp))
  good <- temp > cut[1] & temp < cut[2]
  x.data$valid.sd[x.data$subj==sub] <- good
  
  ntrials$orig[ntrials$sub==sub] <- length(temp)
  ntrials$good[ntrials$sub==sub] <- sum(good)
}

# N-tirals summary
ntrials$removed <- ntrials$orig-ntrials$good
range(ntrials$good)
median(ntrials$good)
range(ntrials$removed)
median(ntrials$removed)
sum(x.data$valid.sd)

# Remove outliers
x.data.rtclip <- x.data[x.data$valid.sd == 1,] # Remove outliers

# x.data.cln <- x.data[x.data$valid.RT == T & x.data$valid.choice_shifts == T,]
# pm.data <- x.data.cln[x.data.cln$type == "pm",]

# Save
save(x.data.rtclip,file='cln_data.RData')

# Export data for HDDM in Python (export to csv)
out.name <- paste0(out.folder,'alldata.csv')
write.csv(x.data.rtclip,file=out.name)



