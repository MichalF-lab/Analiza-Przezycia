# Instalacja pakietu (jeœli nie jest zainstalowany)

# Parametry rozk³adu
rho <- 0.5
rho1 <- sqrt(0.5)

# Funkcja gêstoœci warunkowej
rho.cond <- function(x, y, rho) {
    dnorm(x, rho * y, sqrt(1 - rho ^ 2))
}

# Inicjalizacja wektora startowego
x0 <- c(3, 1)

# Symulacja z u¿yciem Parami Gibbsa
set.seed(12387) # Dla odtwarzalnoœci wyników
n.samples <- 600 # Liczba iteracji
x <- matrix(NA, nrow = n.samples, ncol = 2)
x[1,] <- x0
for (i in 2:n.samples) {
    x[i, 1] <- rnorm(1, rho * x[i - 1, 2], sqrt(1 - rho ^ 2))
    x[i, 2] <- rnorm(1, rho * x[i, 1], sqrt(1 - rho ^ 2))
}

# Badanie czasu burn-in
burn.in <- 300 # Liczba iteracji do odrzucenia
y <- head(x,burn.in)
x <- x[(burn.in + 1):n.samples,]


# Ilustracja rozk³adu docelowego
par(mfrow = c(1, 2))
plot(x[, 1], x[, 2], xlab = "X1", ylab = "X2", main = "Rozk³ad docelowy")
abline(h = 0, v = 0, lty = 2)

# Kowariancja wspó³rzêdnych
cov(x)

par(mfrow = c(2, 1))
plot(x[, 1], type = "p", xlab = "Iteracja", ylab = "X1", main = "Wykres œledz¹cy X1")
plot(y[, 1], type = "p", xlab = "Iteracja", ylab = "Y1", main = "Wykres œledz¹cy Y2")
