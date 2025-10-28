import numpy as np
# from report_part1 import wzor_do_base64

# --- Dane dla leku A ---
remisja_A = np.array([
    0.03345514,
    0.08656403,
    0.08799947,
    0.24385821,
    0.27755032,
    0.40787247,
    0.58825664,
    0.64125620,
    0.90679161,
    0.94222208
])

bez_remisji_A = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

# --- Dane dla leku B ---
remisja_B = np.array([
    0.03788958,
    0.12207257,
    0.20319983,
    0.24474299,
    0.30492413,
    0.34224462,
    0.42950144,
    0.44484582,
    0.63805066,
    0.69119721
])

# 10 pacjentow bez remisji (cenzurowanie w czasie 1.0)
bez_remisji_B = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

A = np.concatenate((remisja_A, bez_remisji_A))
B = np.concatenate((remisja_B, bez_remisji_B))

# 1A
L_A = np.mean(A)
L_B = np.mean(B)
print(f'L_A: {L_A}')
print(f'L_B: {L_B}')

# 2A
L_A = len(remisja_A) / (np.sum(remisja_A) + len(bez_remisji_A) + len(bez_remisji_A) - len(remisja_A))
L_B = len(remisja_B) / (np.sum(remisja_B) + len(bez_remisji_B) + len(bez_remisji_B) - len(remisja_B))
print(f'L_A: {L_A}')
print(f'L_B: {L_B}')
