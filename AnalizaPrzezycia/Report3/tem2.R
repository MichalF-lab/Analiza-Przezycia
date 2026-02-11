library(survival)
library(timereg)

# Przygotowanie danych
data(lung, package = "survival")

# 1. Czyszczenie danych: prop.odds nie lubi brakujących wartości (NA)
# Zbiór już zawiera zmienną sex2
lung_clean <- na.omit(lung[, c("time", "status", "age", "ph.ecog", "ph.karno", "sex2")])

print(nrow(lung_clean))
