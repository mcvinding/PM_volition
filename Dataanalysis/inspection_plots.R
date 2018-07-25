### ----------------------------------------------- ###
### Summary
out.folder <- '/home/mikkel/PM-volition/Datafiles/'
setwd(out.folder)
load('cln_data.RData')
source('/home/mikkel/PM-volition/Dataanalysis/publish_theme.vs2.R')

library(ggplot2)

## %-correct //////////////////////////////////////////////////////////
#pooled % -----------------------------------------------------
tab.free <- xtabs(~score+type, data=x.data.rtclip, subset=volition=='free')
prop.table(tab.free,2)
tab.fix <- xtabs(~score+type, data=x.data.rtclip, subset=volition=='fix')
prop.table(tab.fix,2)
#sub specific -----------------------------------------------------

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

# Plot all individual 
pct_corrt = ggplot(prob.dat, aes(x=subj,y=dat,fill=tasks))+
  geom_bar(position="dodge",stat="identity")+
  ylab("%-correct")+
  labs(title="%-correct for each condition between subjects")+
  theme_bw()
ggsave('pct_correct_all',pct_corrt,device='png',width=10,height=5, units='cm',scale = 2)

pct_corrt2 = ggplot(prob.dat, aes(x=tasks,y=dat,fill=subj))+
  geom_dotplot(binaxis="y",position=position_dodge(.5))+
  ylab("%-correct")+
  labs(title="%-correct for each subject between conditions")+
  theme_bw()
ggsave('pct_correct_all2.png',pct_corrt2,device='png',width=6,height=6, units='cm',scale = 3)

# Group level summary
aggregate(dat~tasks, FUN=median, data=prob.dat)
aggregate(dat~tasks, FUN=range, data=prob.dat)

p.summary <- aggregate(prob.dat$dat, list(prob.dat$tasks), median)
names(p.summary) <- c("Task","mean")

p.summary.sd <- aggregate(prob.dat$dat, list(prob.dat$tasks), sd)
p.summary.qt <- aggregate(prob.dat$dat, list(prob.dat$tasks), quantile, probs=c(0.025,0.975))
qts <- p.summary.qt[2]

p.summary$Volition <- rep(c("fix","free"),each=2)
p.summary$PM.type <- rep(c("fil","pm"),2)
p.summary$sd <- p.summary.sd$x
p.summary$se <- p.summary$sd/sqrt(100)
p.summary$lower = p.summary.qt$x[,1]
p.summary$upper = p.summary.qt$x[,2]

# Group level bar-and-whiskers plot.
group_bar_pctCorrt = ggplot(p.summary, aes(x=PM.type,y=mean, fill=Volition))+
  geom_bar(position="dodge",colour="black",stat="identity")+
  geom_errorbar(aes(ymin=mean-2*se,ymax=mean+2*se),position=position_dodge(.9), width=.3)+
  labs(title="Group level %-correct (+/- 2se)")
ggsave('pct_correct_group',group_bar_pctCorrt,device='png',width=6,height=6, units='cm',scale = 3)

# THE GOOD %-CORRECT PLOT
pct_corrt = ggplot(prob.dat, aes(x=tasks,y=dat,fill=subj))+
  geom_point(aes(x=tasks, y=dat, color=subj), position = position_dodge(width = 0.3))+
  geom_crossbar(data=p.summary,aes(x=Task,y=mean, ymin=mean,ymax=mean), width = 0.5)+
  geom_errorbar(data=p.summary,aes(x=Task,y=mean, ymin=lower, ymax=upper), width=0.2)+
  ylab("%-correct")+
  xlab('Task')+
  labs(title="Performance", tag="B") + guides(fill=F)+
  publish_theme + theme(legend.position = "none")
ggsave('pct_correct_all.png', pct_corrt,
       device='png',width=5,height=3, units='cm', dpi = 600, scale = 4)

# plot1 <- ggplot(rt.dat) + 
#   geom_point(aes(x=tasks, y=RT, color=subj), position = position_dodge(width = 0.3)) +   
#   geom_crossbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=mean,ymax=mean), width = 0.5) + theme_bw() +
#   geom_errorbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=mean-sd, ymax=mean+sd), width=0.2) +
#   # scale_color_manual(values=c("blue","red"))+
#   xlab("Task") +
#   ylab("Reaction time (ms)") + ylim(0, max(rt.dat$RT))+
#   ggtitle("Reaction time")

## RT ///////////////////////////////////////////////////////////
# pooled rt -----------------------------------------------------
mean.summary <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type),mean)
sd.summary <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type),sd)

rt.summary <- mean.summary
names(rt.summary) <- c('Volition','PM.type','mean')
rt.summary$sd <- sd.summary$x

rt_pool <- ggplot(rt.summary, aes(x=PM.type,y=mean, fill=Volition))+
  geom_bar(position="dodge",colour="black",stat="identity")+
  geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd),position=position_dodge(.9), width=.3)+
  labs(title="Pooled RT (+/- sd)")
rt_pool+theme_bw()
ggsave('rt_pool.png',rt_pool,device='png',width=6,height=6, units='cm',scale = 2)

# per subject RT -----------------------------------------------------
rt.dat <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),median)
rt.dat.se <- aggregate(x.data.rtclip$rt.ms, list(x.data.rtclip$volition,x.data.rtclip$type,x.data.rtclip$subj),sd)

names(rt.dat) <- c("volition","task","subj","RT")
rt.dat$sd <- rt.datse$x
rt.dat$tasks <- factor(paste(rt.dat$volition,rt.dat$task), levels = c("free pm", "free filler", "fix pm", "fix filler"))
levels(rt.dat$tasks) <- tasks

rt.grouplvl <- aggregate(rt.dat$RT,list(rt.dat$tasks), mean)
names(rt.grouplvl) <- c("tasks","mean")
rt.grouplvl$sd <- aggregate(rt.dat$RT,list(rt.dat$volition,rt.dat$task),sd)$x
rt.grouplvl$se <- rt.grouplvl$sd/sqrt(10)
rt.grouplvl.qt <- aggregate(rt.dat$RT, list(rt.dat$tasks), quantile, probs=c(0.025,0.975))
rt.grouplvl$lower = rt.grouplvl.qt$x[,1]
rt.grouplvl$upper = rt.grouplvl.qt$x[,2]

ggplot(x.data.rtclip, aes(x=rt.ms, fill=type))+
  geom_histogram(alpha=.4,position="identity",colour="black")+
  labs(title="RT per sub for PM-task")+
  facet_wrap(~subj, ncol=5)+publish_theme
ggsave('rt_hist_pmTask.png',device='png',width=10,height=10, units='cm',scale = 2)


ggplot(x.data.rtclip, aes(x=rt.ms, fill=volition))+
  geom_histogram(alpha=.3,colour="black",position="identity")+
  labs(title="RT per sub for volition type")+
  scale_fill_manual(values=c("red","blue"))+
  facet_wrap(~subj, ncol=5)
ggsave('rt_hist_volTask.png',device='png',width=10,height=10, units='cm',scale = 2)


ggplot(rt.dat, aes(x=subj, y=RT, fill=tasks))+
  geom_bar(position="dodge",stat="identity")+
  geom_errorbar(aes(ymax=RT+sd,ymin=RT-sd),position=position_dodge(.9),width=.2)+
  ylab("RT")+
  labs(title="Mean-RT (sd) for each subject between conditions")+
  theme_bw()
ggsave('rt_allsub.png',device='png',width=15,height=5, units='cm',scale = 2)

ggplot(rt.dat, aes(x=tasks,y=RT,fill=subj))+
  geom_dotplot(binaxis="y",position=position_jitterdodge(.003),binwidth=10)+
  ylab("RT")+
  labs(title="RT for each subject between conditions")+
  theme_bw()+
  geom_crossbar(data=rt.grouplvl, aes(x=tasks,y=mean, ymin=mean,ymax=mean), width = 0.4) + theme_bw()
  
ggsave('rt_allsub2.png',device='png',width=6,height=6, units='cm',scale = 3)

# THE GOOD REACTION TIME PLOT
plot1 <- ggplot(rt.dat) + 
  geom_point(aes(x=tasks, y=RT, color=subj), position = position_dodge(width = 0.3)) +   
  geom_crossbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=mean,ymax=mean), width = 0.5) +
  geom_errorbar(data=rt.grouplvl,aes(x=tasks,y=mean, ymin=lower, ymax=upper), width=0.2) +
  # scale_color_manual(values=c("blue","red"))+
  xlab("Task") +
  ylab("Reaction time (ms)") + ylim(0, max(rt.dat$RT))+
  ggtitle("Reaction time")+
  labs(title="Reaction time", tag="A") + guides(fill=F)+
  publish_theme + theme(legend.position = "none")
plot1

ggsave('rt_allsub2b.png', plot1,
       device='png',width=5,height=3, units='cm', dpi = 600, scale = 4)
