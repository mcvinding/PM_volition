### ----------------------------------------------- ###
### Make summary plots of reaction time and %-correct

# out.folder <- '/home/mikkel/PM-volition/Datafiles/'
out.folder <- 'C:\\Users\\Mikkel\\Documents\\PM-volition\\Datafiles'

# source('/home/mikkel/PM-volition/Dataanalysis/publish_theme.vs2.R')
source('C:\\Users\\Mikkel\\Documents\\PM-volition\\Dataanalysis\\publish_theme.vs2.R')
library(ggplot2)

setwd(out.folder)

########################### %-correct #################################
## Prepare data
load('cln_data2.RData')

tasks <-  c('Choice (PM) ', 'Choice (filler)', 'No-choice (PM)', 'No-choice (filler)')

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

# Group level summary
p.summary <- aggregate(prob.dat$dat, list(prob.dat$tasks), mean)
names(p.summary) <- c("Task","mean")

p.summary.sd <- aggregate(prob.dat$dat, list(prob.dat$tasks), sd)
p.summary.qt <- aggregate(prob.dat$dat, list(prob.dat$tasks), quantile, probs=c(0.025,0.975))
qts <- p.summary.qt[2]

p.summary$Volition <- rep(c("fix","free"),each=2)
p.summary$PM.type <- rep(c("fil","pm"),2)
p.summary$sd <- p.summary.sd$x
p.summary$se <- p.summary$sd/sqrt(29)
p.summary$lower = p.summary.qt$x[,1]
p.summary$upper = p.summary.qt$x[,2]

### THE GOOD %-CORRECT PLOT
pct_corrt = ggplot(prob.dat, aes(x=tasks,y=dat, fill=subj))+
  geom_point(position = position_jitterdodge(dodge.width = 0.4),color='black',shape=21,size=2)+
  geom_crossbar(data=p.summary,aes(x=Task,y=mean, ymin=mean,ymax=mean), width = 0.5)+
  geom_errorbar(data=p.summary,aes(x=Task,y=mean, ymin=lower, ymax=upper), width=0.2)+
  ylab("%-correct")+
  xlab('Task')+ylim(c(.5, 1))+
  labs(title="Performance", tag="B") + guides(fill=F)+
  publish_theme + 
  theme(legend.position = "none",
        axis.text.x = element_text(size=9))
pct_corrt
ggsave('pct_correct_all.png', pct_corrt,
       device='png',width=4,height=4, units='cm', dpi = 600, scale = 3.5)

############################## RT ####################################
## Prepare data
rt.dat <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),median)
rt.dat.sd <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),sd)

names(rt.dat) <- c("volition","task","subj","RT")
rt.dat$sd <- rt.dat.sd$x
rt.dat$tasks <- factor(paste(rt.dat$volition,rt.dat$task), levels = c("free pm", "free filler", "fix pm", "fix filler"))
levels(rt.dat$tasks) <- tasks

rt.grouplvl <- aggregate(rt.dat$RT,list(rt.dat$tasks), mean)
names(rt.grouplvl) <- c("tasks","mean")
rt.grouplvl$sd <- aggregate(rt.dat$RT,list(rt.dat$volition,rt.dat$task),sd)$x
rt.grouplvl$se <- rt.grouplvl$sd/sqrt(10)
rt.grouplvl.qt <- aggregate(rt.dat$RT, list(rt.dat$tasks), quantile, probs=c(0.025,0.975))
rt.grouplvl$lower = rt.grouplvl.qt$x[,1]
rt.grouplvl$upper = rt.grouplvl.qt$x[,2]

# THE GOOD REACTION TIME PLOT
rt_plt <- ggplot(rt.dat,aes(x=tasks, y=RT, fill=subj)) + 
  geom_point(position = position_jitterdodge(dodge.width = 0.4),color='black',shape=21,size=2)+
  geom_crossbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=mean,ymax=mean), width = 0.5) +
  geom_errorbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=lower, ymax=upper), width=0.2) +
  xlab("Task") +
  ylab("Reaction time (ms)") + ylim(200, 900)+
  ggtitle("Reaction time")+
  labs(title="Reaction time", tag="A") + guides(fill=F)+
  publish_theme +
  theme(legend.position = "none",
        axis.text.x = element_text(size=9))
rt_plt
ggsave('rt_all.png', rt_plt,
       device='png',width=4,height=4, units='cm', dpi = 600, scale = 3.5)

# END