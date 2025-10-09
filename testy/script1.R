set.seed(131131)

# Zad 1

datan <- rnorm(100)
plot(seq(-3, 3, 0.1), pnorm(seq(-3, 3, 0.1)))
lines(ecdf(datan))

datae <- rexp(100)
plot(seq(0, 6, 0.1), pexp(seq(0, 6, 0.1)))
lines(ecdf(datae))

# Zad 2

# Funkcje Pomocnicze
L <- function(sample,u) {
    #print(sample)
    ext <- (sample - u)
    return(ext)
}
U <- function(sample,u) {
    ext <- (sample + u)
    return(ext)
}

# Preprocesing
alpha <- 0.05
n <- 100
M <- 1
error <- 0
epsilon_n <- sqrt((log(2 / alpha) / (2 * n)))


# Symulacja
for (i in 1:M) {
    samples <- rexp(n)
    samplesc <- table(samples)
    sampless1 <- cumsum(sort(samples)) / sum(samples)
    sampless <- samples / sum(samples)


    #plot(seq(0, 6, 0.1), sampless)
    plot(sampless1)
    for (j in 1:n-1) {
        
        J <- j/n
        LL <- L(sampless1[j], epsilon_n)
        UU <- U(sampless1[j], epsilon_n)

        if (LL > pexp(J) || UU < pexp(J)) {
            print(J)
            #print(epsilon_n)
            #print((pexp(j)))
            #print(LL)
            print(qexp(J))
            print(UU)
            error <- error + 1
        }
    }
}
print(error)






