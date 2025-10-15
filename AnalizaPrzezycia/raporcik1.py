import numpy as np
import random


def dEW(x, alpha, beta, gamma):
    weibull_cdf = 1 - np.exp(-(x / beta)**alpha)
    weibull_pdf = (alpha / beta) * (x / beta)**(alpha - 1) * np.exp(-(x / beta)**alpha)
    
    return gamma * weibull_pdf * weibull_cdf**(gamma - 1)


def pEW(x, alpha, beta, gamma): 
    return (1 - np.exp(-(x / beta)**alpha))**gamma


def qEW(p, alpha, beta, gamma):
    return beta * (-np.log(1 - p**(1/gamma)))**(1/alpha)


def hazard_EW(x, alpha, beta, gamma):
    f = dEW(x, alpha, beta, gamma)
    F = pEW(x, alpha, beta, gamma)
    
    # Unikanie dzielenia przez zero
    survival = 1 - F
    return np.where(survival > 1e-10, f / survival, np.inf)

def rEW(size, alpha, beta, gamma):
    samples = np.random.uniform(0, 1, size=100)
    return pEW(samples, alpha, beta, gamma)
