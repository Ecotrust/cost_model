#setwd("~/projects/forestplanner/cost_model_validation")
d <- read.csv("results.csv")
library(ggplot2)

d$diff = d$predicted - d$actual
#d$diff =  d$actual - d$predicted

p <- ggplot(d, aes(x=predicted, y=actual)) + geom_point()
ggsave("scatter.pdf", p)

dmeans <- aggregate( cbind(predicted, actual, diff) ~ name, d, mean )


p <- ggplot(d, aes(x=predicted)) +
    geom_histogram(alpha=0.5) +
    geom_vline(data=d, aes(xintercept=actual)) +
    geom_vline(data=dmeans, aes(xintercept=predicted), linetype="dashed") +
    geom_text(data=dmeans, aes(x=predicted*1.02, y=0, label=round(diff)), hjust=0, size=3) +
    facet_grid(~name) 
ggsave("histograms.pdf", p)
