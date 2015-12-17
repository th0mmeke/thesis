# ave cor,ave fit,gen,pop,sd cor,sd fit
# 0.5545283508318075,0.8419380979405692,6,10380,0.3873342071576403,0.25925553541282276,0,0,0,0,0,0,0,0

load_df <- function(t){
  while ("df" %in% search()) {detach(df)}

  colClasses <- c("numeric","numeric","integer","integer","numeric","numeric","numeric","numeric","integer","integer","numeric","numeric","factor","factor","factor","factor","factor","factor","factor")
  df <- read.csv(t, colClasses=colClasses, header=T)
  df$response_cor <- df$final_ave_cor-df$initial_ave_cor
  df$response_fit <- df$final_ave_fit-df$initial_ave_fit
  df[df$truncate==1,]
}

model <- function(df) {
  fit<-lm(response~(p_reproduce+p_selection+n_offspring+distribution+fitness_correlation+correlation_correlation)^2, data=df) # ^2 = main effects and two-factor interactions only
#  print(100*abs(fit$effect[-1])/sum(abs(fit$effect)[-1])) # percentage effects
#  print(anova(fit))
  fit
}

# Check effect of population limits


#twoway.plots(df1$diff,df1$correlation_correlation,df1$fitness_correlation)

df_high <- load_df("results_highstart.data")
df_low <- load_df("results_lowstart.data")

between <- var(c(mean(df_high$response_cor),mean(df_low$response_cor)))
within <- mean(c(var(df_high$response_cor),var(df_low$response_cor)))
power.anova.test(groups=2,n=dim(df_high)[1],between.var=between,within.var=within)
# or alternatively...
# power.anova.test(groups=2,between.var=between,within.var=within, sig.level=0.05, power=0.999) returns n=10.43...

df_low <- load_df("results_lowstart.data")
m0 <- lm(response_cor~(p_reproduce+p_selection+n_offspring+distribution+fitness_correlation+correlation_correlation)^2, data=df_low)
# Check model m0 for fit
plot(m0,which=c(1,2)) # residuals and qq plot - residuals decreasing variability (wider range at lhs), qq plot strongly s-shaped
# Try to improve model
# Only one two-factor interaction in any way significant - p_reproduce:p_selection
# So simplify model to lm(response~(p_reproduce+p_selection+n_offspring+distribution+fitness_correlation+correlation_correlation + p_reproduce:p_selection)
m1 <- lm(response_cor~(p_reproduce+p_selection+n_offspring+distribution+fitness_correlation+correlation_correlation + p_reproduce:p_selection),data=df_low)
anova(m0,m1) # no difference
drop1(m1, test="F") # distribution has largest p-value, so candidate for deletion
m2 <- lm(response_cor~(p_reproduce+p_selection+n_offspring+fitness_correlation+correlation_correlation + p_reproduce:p_selection),data=df_low)
anova(m1,m2) # different, with Pr=0.0143, so m1 is candidate model


fit_high <- model(df_high)
summary(fit_high)
anova(fit_high)
checking.plots(fit_high) # check assumptions of errors (residuals) independent, normally distributed, constant variance
plot(fit_high)

df_high_changing <- load_df("results_highstart_changing.data")
fit_high_changing <- model(df_high_changing)
summary(fit_high_changing)
anova(fit_high_changing)

df_low_changing <- load_df("results_lowstart_changing.data")
fit_low_changing <- model(df_low_changing)
summary(fit_low_changing)
anova(fit_low_changing)

#
# boxplot(Correlation~Distribution, data=df, main="X", names=c("Gauss","Uniform"), ylab="Correlation")
#
# #hist(df$Number.of.cycles, main="Histogram", xlab="Number.of.cycles")
# shapiro.test(df_high$Number.of.cycles)
# # HYPOTHESIS TEST
# t.test(df_high$Number.of.cycles, df_low$Number.of.cycles, var.equal=FALSE)
#
# # FACTOR INTERACTIONS
#
# interaction.plot(Energy,FoodSet,Number.of.cycles)
#
# # CHECK POWER OF TEST
#
# between <- var(c(mean(df_1$Number.of.cycles),mean(df_2$Number.of.cycles)))
# within <- mean(c(var(df_1$Number.of.cycles),var(df_2$Number.of.cycles)))
# power.anova.test(groups=2,between.var=between,within.var=within,sig.level=0.05,n=length(df_1$Number.of.cycles))
#
# library(PASWR) # For checking.plots
# library(car) # For leveneTest
#
# # CHECK ASSUMPTIONS
#
# m.aov <- aov(Number.of.cycles~Bond.Energies*Energy*FoodSet)
# checking.plots(m.aov)
# boxcox(m.aov)
# summary(m.aov)
# checking.plots(m.aov)
# leveneTest(m.aov)
#
# modfull <- lm(log(Number.of.cycles)~Bond.Energies*Energy*FoodSet)
# modreduced <- lm(log(Number.of.cycles)~Bond.Energies+Energy+FoodSet)
# anova(modfull, modreduced) # p-value = 0.4326
# m.aov <- aov(log(Number.of.cycles)~Bond.Energies*Energy*FoodSet)
# stepAIC(m.aov) # log(Number.of.cycles) ~ Bond.Energies + Energy + FoodSet + Bond.Energies:Energy
# plot(m.aov,which=1)

detach(df)
