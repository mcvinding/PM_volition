# Scripts for running analysis

## Data summaries
Read data into *R* and make summaries of task performance and reaction times presented i section X.X of the paper. Make a summary figure of performance and reaction times (Figure X). All scripts written for *R* and run with *RStudio*.
* `import_data.R`: import the output files from PsychoPy to R for each subject. Arrange data in a single data frame. Save data frame as R-data and `csv` (shared).
* `data_cleaning.R`: remove outliers based on reaction times and remove bad subject. Get summaries of reaction times and task performance. Save cleaned data in `csv` format for DDM analysis.
* `subjectSummary.R`: get summary of age and sex of subjects.
* `summary_figures.R`: make scatter plots with errorbars showing (1) task performance and (2) reaction times across conditions.
### Dependencies
**R packages:** *ggplot2*, 

## Drift-diffusion analysis

* 
### Dependencies
*HDDM toolbox* (link)