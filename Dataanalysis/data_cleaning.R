#PM-volition dataanalysis data-cleaning
###
rm(list=ls())
library(lme4)

#Set up foldersd  
data.folder <-  '/home/mikkel/Dropbox/PM-volition/PM-volition data files/'
out.folder <- '/home/mikkel/Dropbox/PM-volition/Dataanalysis/'
setwd(out.folder)
load(file='raw_data.RData')

# Different subsets
x.data$log.rt <- log(x.data$rt)
x.data$meanChoiceTime <- x.data$choice_rt/x.data$choice_shifts

x.data <- subset(x.data, pm_first!="") #Remove weird value
x.data$pm_first <- droplevels(x.data$pm_first)

x.data$valid.RT <- x.data$rt.ms < 1500 & x.data$rt.ms > 150
x.data$valid.choice_shifts <- x.data$choice_shifts >= 1 | x.data$volition =="fix"

x.data.rtclip <- x.data[x.data$valid.RT == 1,] # Remove unplausible reaction times: 200 ms < RT < 1500 ms
free.data <- x.data.rtclip[x.data.rtclip$volition=="free",]   # Only free-choice conditions

x.data.cln <- x.data[x.data$valid.RT == T & x.data$valid.choice_shifts == T,]
pm.data <- x.data.cln[x.data.cln$type == "pm",]

## Prepare data for HDDM (export to Python - csv)
out.name <- paste0(out.folder,'alldata.csv')

write.csv(x.data.cln,file=out.name)


