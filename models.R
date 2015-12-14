# ave cor,ave fit,gen,pop,sd cor,sd fit
# 0.5545283508318075,0.8419380979405692,6,10380,0.3873342071576403,0.25925553541282276,0,0,0,0,0,0,0,0

colClasses <- c("numeric","numeric","integer","integer","numeric","numeric","numeric","numeric","integer","integer","numeric","numeric","factor","factor","factor","factor","factor","factor","factor")
df <- read.csv("results.data", colClasses=colClasses, header=T)
df$diff <- df$final_ave_cor - df$initial_ave_cor

df1<-df[df$truncate==1,]
fit<-lm(diff~(p_reproduce+p_selection+n_offspring+distribution+fitness_correlation+correlation_correlation)^2, data=df1) # up to 2nd order interactions
100*abs(fit$effect[-1])/sum(abs(fit$effect)[-1]) # percentage effects
anova(fit)

> fit$effects
              (Intercept)              p_reproduce1              p_selection1              n_offspring1             distribution1
            -1.9203157481             -0.0515546229             -0.4533279392              0.0551325901              0.5464759105
     fitness_correlation1  correlation_correlation1 p_reproduce1:p_selection1
             0.0227962349              0.4876673553              0.0156605678             -0.0017563140             -0.0054636214

            -0.0001237185             -0.0011022630             -0.0065996571              0.0072315422              0.0020345169

             0.0012429985


              (Intercept)              p_reproduce1              p_selection1              n_offspring1             distribution1
            -1.9254932244             -0.0478424754             -0.4581400969              0.0470998479              0.5397128421
     fitness_correlation1  correlation_correlation1 p_reproduce1:p_selection1
             0.0438330852              0.4606984662              0.0416756003             -0.0070575233              0.0149759653

             0.0048904974              0.0043400702              0.0008031987              0.0091367842              0.0033622395

            -0.0055039876 

fit<-lm(ave_fit~p_reproduce*p_selection*n_offspring*truncate*distribution*fitness_correlation*correlation_correlation*low_start, data=df)

                          (Intercept)                          p_reproduce1                          p_selection1
                        -7.320380e+00                         -3.734384e-01                         -1.023950e-02
                         n_offspring1                             truncate1                         distribution1
                        -1.301125e-01                          5.204246e-01                         -1.115440e+00
                 fitness_correlation1              correlation_correlation1                            low_start1
                        -4.082354e-02                          1.139381e+00                         -3.102069e-01
            p_reproduce1:p_selection1             p_reproduce1:n_offspring1                p_reproduce1:truncate1
                        -1.955233e-01                         -1.126892e-02                         -1.099277e+00
           p_reproduce1:distribution1     p_reproduce1:fitness_correlation1 p_reproduce1:correlation_correlation1
                         5.045012e-01                         -2.429901e-01                          5.719760e-01
              p_reproduce1:low_start1
                        -6.413825e-02
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
