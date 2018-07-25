### ---------------------------------------------- ###
# Import PM-volition data.
# Import individual csv files and save as a single file.
### ---------------------------------------------- ###

###
rm(list=ls())

#Set up foldersd  
data.folder <-  '/home/mikkel/PM-volition/PM-volition data files/'      
out.folder <- '/home/mikkel/PM-volition/Datafiles/'

setwd(data.folder)

all_files <- list.files(data.folder)
all_files <- all_files[grepl('.csv', all_files)]   #Find all *.csv files

# Import all data
x.data <- data.frame()
for (ii in 1:length(all_files)) {
  filename = all_files[ii]
  
  sub.data <- read.csv(filename, sep=",",header=T) #, stringsAsFactors=F)
  sub.data$org.filename <- filename
  sub.data$subject <- as.factor(sub.data$subject)
  
  x.data <- rbind(x.data,sub.data)  
}

setwd(out.folder)

# Fix factors
x.data$volition <- as.factor(x.data$volition)
x.data$rt.ms <- x.data$rt*1000
x.data$practice <- as.logical(x.data$practice)
levels(x.data$volition) <- c('fix','free')
x.data$subj <- x.data$subject
levels(x.data$subj) <- as.character(1:length(levels(x.data$subject)))
x.data <- subset(x.data, pm_first!="") #Remove weird value
x.data$pm_first <- droplevels(x.data$pm_first)
x.data$gender <- factor(x.data$gender)
x.data$correct_answer <- factor( x.data$correct_answer)
x.data$response <- factor(x.data$response)
x.data$pm_shape <- factor(x.data$response)
x.data$log.rt <- log(x.data$rt)
# x.data$meanChoiceTime <- x.data$choice_rt/x.data$choice_shifts

save(x.data,file='raw_data.RData')
