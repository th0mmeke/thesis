### RESULTS - FIDELITY AGAINST CHANGE

library(ggplot2)

colClasses <- c("factor","factor","factor","factor","factor","factor","numeric","numeric","numeric","numeric","factor","integer","numeric","integer","numeric","numeric")
results <- read.csv('run1/results.csv', colClasses=colClasses)

ggplot(subset(results,gen==500),aes(ar_sd,ave_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_theta/ar_sd,ave_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_sd,sd_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_theta,ave_fid)) + geom_point() + geom_smooth(method='lm')

### SAMPLE ENVIRONMENTAL CHANGES

library(pracma)
library(reshape2)
library(ggplot2)

t1 <- read.csv('model/environments.csv', header=FALSE, colClasses=c("numeric","numeric","numeric"))
t1$run <- 1:nrow(t1)
names(t1)[1:3]<-c("theta", "sd", "bias")
t2 <- melt(t1,id=c('run','theta','sd','bias'))
t2$theta <- round(t2$theta,3)
t2$sd <- round(t2$sd,3)
t2$bias <- round(t2$bias,3)
ggplot(t2) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_wrap(~theta+sd+bias, labeller='label_both') + labs(x="t", y="Fitness change")


### FACTORIAL OF THETA, SD AND BIAS

t1 <- read.csv('model/environments-factorial.csv', header=FALSE, colClasses=c("numeric","numeric","numeric"))

t1$run <- 1:nrow(t1)
names(t1)[1:3]<-c("theta", "sd", "bias")
t2 <- melt(t1,id=c('run','theta','sd','bias'))
t2$theta <- round(t2$theta,3)
t2$sd <- round(t2$sd,3)
t2$bias <- round(t2$bias,3)
ggplot(subset(t2,bias==0)) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_grid(theta~sd, labeller='label_both') + labs(x="t", y="Fitness change")
ggplot(subset(t2,sd!=0)) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_grid(theta~bias, labeller='label_both') + labs(x="t", y="Fitness change")

### EFFECT ON FITNESS

for (r in unique(t2$run)) {
    t2[t2$run==r,'t'] <- 1:50 # tag with timestamp

    fitness <- 0.5
    for (t in 1:50) {
        fitness <- max(0,min(1,fitness + t2[t2$run==r & t2$t==t,'value']))
        t2[t2$run==r & t2$t==t,'fitness'] = fitness
    }
}

t2$theta <- round(t2$theta,3)
t2$sd <- round(t2$sd,3)
t2$bias <- round(t2$bias,3)
ggplot(t2) + geom_line(aes(x=t,y=fitness)) + facet_wrap(~theta+sd+bias, labeller='label_both') + theme(strip.text.x = element_text(size = 8))

#### SAMPLE AND APPROXIMATE ENTROPY FIT

t2 <- t1[,1:3]
names(t2)[1]<-"theta"
names(t2)[2]<-"sd"
names(t2)[3]<-"bias"
for(n in 1:nrow(t1)) {t2[n,'sample_entropy'] <- sample_entropy(unlist(t1[n,4:52],use.names=FALSE))}
for(n in 1:nrow(t1)) {t2[n,'approx_entropy'] <- approx_entropy(unlist(t1[n,4:52],use.names=FALSE))}

summary(lm(sample_entropy~theta+sd,data=t2)) # F-statistic: 2.359 on 2 and 497 DF,  p-value: 0.09561 - no real linear model
summary(lm(approx_entropy~theta + sd, data = t2)) # F-statistic:   1.9 on 2 and 497 DF,  p-value: 0.1506 - even less relationship...
ggplot(t2, aes(sd,sample_entropy)) + geom_point() + geom_smooth(method='lm') # formula not required

### CALCULATE SAMPLE ENTROPY FOR ALL RUNS

library(pracma)
n_runs <- 200
for(i in 0:(n_runs-1)) {
   filename <- paste("model/run1/environments",i,".csv",sep="")
   e <- read.csv(filename, header=FALSE)
   for(n in 1:nrow(e)) {
        e[n,'se'] <- sample_entropy(unlist(subset(e,V2==n-1)[,3:502],use.names=FALSE))
   }
   print(e$se)
   results[results$run==i,'sample_entropy'] <- mean(e$se)
}
