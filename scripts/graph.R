setwd("~/projects/forestplanner/cost_model_validation")
d <- read.csv("results.csv")
library(ggplot2)

p <- ggplot(d, aes(x=predicted, y=actual)) + geom_point()
ggsave("scatter.pdf", p)

p <- ggplot(d, aes(x=predicted)) + geom_histogram(alpha=0.5) + geom_vline(data=d, aes(xintercept=actual)) + facet_grid(~name) 
ggsave("histograms.pdf", p)
