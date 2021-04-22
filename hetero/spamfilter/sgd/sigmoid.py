import numpy as np


def sigmoid(e):
  return 1 / (1 + np.exp(-e))


indices = [i for i in range(0, 512)]

exp_ix = [i * 4.0 / 512. for i in indices]


sig_pos = [sigmoid(e) for e in exp_ix]

sig_neg = [sigmoid(-e) for e in exp_ix]


ix = 0
line = ""
for s in sig_neg:
  if ix % 4 == 0:
    line = line + "\n"
  line = line + str(s) + ","
  ix = ix + 1

print(line)

    