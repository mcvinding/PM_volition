### ---------------------------------------------- ###
# Import PM-volition data
# Last updatet 16-11-15 by MCV
### ---------------------------------------------- ###

###
rm(list=ls())

#Set up foldersd  
data.folder <-  '/home/mikkel/Dropbox/PM-volition/PM-volition data files/'      #'C:\\Users\\Administrator\\Copy\\PM-volition\\PM-volition data files'  
out.folder <- '/home/mikkel/Dropbox/PM-volition/Dataanalysis/'
# load(paste(out.folder, 'Workspace.RData',sep=''))

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

x.data$volition <- as.factor(x.data$volition)
x.data$rt.ms <- x.data$rt*1000
x.data$practice <- as.logical(x.data$practice)
levels(x.data$volition) <- c('fix','free')
x.data$subj <- x.data$subject
levels(x.data$subj) <- as.character(1:length(levels(x.data$subject)))

x.data <- subset(x.data, x.data$practice==F)

# x.data.rtclip = subset(x.data, x.data$rt< 1 & x.data$rt> .2)

save(x.data,file='raw_data.RData')


