colClasses <- c("factor","factor","factor","factor","factor","factor","numeric","numeric","numeric","numeric","factor","integer","numeric","integer","numeric","numeric")
results <- read.csv('model/run1/results.csv', colClasses=colClasses)

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

library(ggplot2)
ggplot(subset(results,gen==500),aes(ar_sd,ave_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_theta/ar_sd,ave_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_sd,sd_fid)) + geom_point() + geom_smooth(method='lm')
ggplot(subset(results,gen==500),aes(ar_theta,ave_fid)) + geom_point() + geom_smooth(method='lm')


library(pracma)
t1 <- read.csv('model/environments.csv', header=FALSE, colClasses=c("numeric","numeric","numeric"))
t1$run <- 1:nrow(t1)
names(t1)[1:3]<-c("theta", "sd", "bias")
t2 <- melt(t1,id=c('run','theta','sd','bias'))
ggplot(t2) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_wrap(~run)

t1 <- read.csv('model/environments-factorial.csv', header=FALSE, colClasses=c("numeric","numeric","numeric"))
t1$run <- 1:nrow(t1)
names(t1)[1:3]<-c("theta", "sd", "bias")
t2 <- melt(t1,id=c('run','theta','sd','bias'))
ggplot(subset(t2,bias==0)) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_grid(theta~sd)
ggplot(subset(t2,sd!=0)) + geom_line(aes(x=as.numeric(variable),y=value)) + facet_grid(theta~bias)


t2 <- t1[,1:3]
names(t2)[1]<-"theta"
names(t2)[2]<-"sd"
names(t2)[3]<-"bias"
for(n in 1:nrow(t1)) {t2[n,'sample_entropy'] <- sample_entropy(unlist(t1[n,4:52],use.names=FALSE))}
for(n in 1:nrow(t1)) {t2[n,'approx_entropy'] <- approx_entropy(unlist(t1[n,4:52],use.names=FALSE))}

summary(lm(sample_entropy~theta+sd,data=t2)) # F-statistic: 2.359 on 2 and 497 DF,  p-value: 0.09561 - no real linear model
summary(lm(approx_entropy~theta + sd, data = t2)) # F-statistic:   1.9 on 2 and 497 DF,  p-value: 0.1506 - even less relationship...
ggplot(t2, aes(sd,sample_entropy)) + geom_point() + geom_smooth(method='lm') # formula not required