import numpy as np

def likelihood_ratio_test(data, test):
    n = len(data)
    r = np.sum(data < np.max(data))
    data = np.sort(data)
    data_uncenzored = data[:r]
    s = np.sum(data_uncenzored)
    t0 = data_uncenzored[-1]
    match test:
        case "a":
            print("sdds")
        case "b":
            print()
        case "c":
            print
    


# p-value 0.0043 