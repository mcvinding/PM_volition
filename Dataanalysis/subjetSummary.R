## subject summary - PM-volition
rm(list=ls())

#Set up foldersd  
data.folder <-  '/home/mikkel/PM-volition/PM-volition data files/'
out.folder <- '/home/mikkel/PM-volition/Dataanalysis/'
setwd(out.folder)
load(file='cln_data.RData')

age.data <- aggregate(age~subj,FUN=mean,data=x.data.rtclip)
sex.data <- aggregate(gender~subj,FUN=unique,data=x.data.rtclip)
sub.data = merge(age.data,sex.data,by='subj')

summary(sub.data)
mean(sub.data$age)
median(sub.data$age)
range(sub.data$age)
sd(sub.data$age)
hist(sub.data$age,20)

table(sub.data$gender)
