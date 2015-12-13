# ave cor,ave fit,gen,pop,sd cor,sd fit
# 0.5545283508318075,0.8419380979405692,6,10380,0.3873342071576403,0.25925553541282276,0,0,0,0,0,0,0,0

colClasses <- c("numeric","numeric","integer","integer","numeric","numeric","factor","factor","factor","factor","factor","factor","factor","factor")
df <- read.csv("results.data", colClasses=colClasses, skip=1)

# VISUAL ASSESSMENT - cycles-by-dimensionality.pdf

#par(mfrow=c(2,3))
attach(df)
boxplot(Correlation~Distribution, data=df, main="X", names=c("Gauss","Uniform"), ylab="Correlation")

#hist(df$Number.of.cycles, main="Histogram", xlab="Number.of.cycles")
shapiro.test(df_high$Number.of.cycles)
# HYPOTHESIS TEST
t.test(df_high$Number.of.cycles, df_low$Number.of.cycles, var.equal=FALSE)

# FACTOR INTERACTIONS

interaction.plot(Energy,FoodSet,Number.of.cycles)

# CHECK POWER OF TEST

between <- var(c(mean(df_1$Number.of.cycles),mean(df_2$Number.of.cycles)))
within <- mean(c(var(df_1$Number.of.cycles),var(df_2$Number.of.cycles)))
power.anova.test(groups=2,between.var=between,within.var=within,sig.level=0.05,n=length(df_1$Number.of.cycles))

library(PASWR) # For checking.plots
library(car) # For leveneTest

# CHECK ASSUMPTIONS

m.aov <- aov(Number.of.cycles~Bond.Energies*Energy*FoodSet)
checking.plots(m.aov)
boxcox(m.aov)
summary(m.aov)
checking.plots(m.aov)
leveneTest(m.aov)

modfull <- lm(log(Number.of.cycles)~Bond.Energies*Energy*FoodSet)
modreduced <- lm(log(Number.of.cycles)~Bond.Energies+Energy+FoodSet)
anova(modfull, modreduced) # p-value = 0.4326
m.aov <- aov(log(Number.of.cycles)~Bond.Energies*Energy*FoodSet)
stepAIC(m.aov) # log(Number.of.cycles) ~ Bond.Energies + Energy + FoodSet + Bond.Energies:Energy
plot(m.aov,which=1)

detach(df)
