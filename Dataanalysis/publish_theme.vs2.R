# Make a theme
# Last edited 2018-04-21 by MCV
library(ggplot2)

publish_theme <- theme_bw() +
  theme(
    # panel.grid.major = element_line(size=.5,colour="grey"),
    # panel.grid.minor = element_line(size=.2,colour="grey"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.border = element_blank(),
    panel.background = element_blank(),
    axis.line = element_line(size=.7, colour="black"),
    text = element_text(size = 12, family="Helvetica", color="black"),       # Size changes from 10, added color = "black"
    plot.title = element_text(size = 20, face="bold", lineheight = NULL, hjust = 0.5),    # Size changes from 8, removed vjust = 1.5,
    plot.tag = element_text(size = 14, face="bold"),
    axis.text = element_text(size=12, color="black"),                                 # Size changes from 8, added color = "black"
    axis.title = element_text(size = 12, face="bold"),                                    # Size changes from 8, vjust = .5
        # legend.background=element_rect(linetype=1, size=.2, fill="white", colour=NULL),
    plot.margin = unit(c(1,1.5,1,1),"lines"),
    legend.box="vertical",
    legend.box.just="top",
#         legend.key.height=unit(.5,"line"),
    legend.direction="vertical",
    legend.key=element_blank(),
    legend.text = element_text(size=10),                          # Size changes from 8
       
    strip.background = element_rect(fill="white",colour="black", size=1)
  ) 