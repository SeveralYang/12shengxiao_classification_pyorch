import os

import matplotlib.pyplot as plt


def get_sorted_list(d, reverse=False):
    return sorted(d.items(), key=lambda x: x[0], reverse=reverse)


rate = {}
for file_name in os.listdir("../weight"):
    d = file_name.split("epoch_correct")
    rate[int(d[0])] = float(d[1][0:-4])
rate = get_sorted_list(rate)
print(rate)
rate = [x[1] for x in rate]
print(max(rate), rate.index(max(rate)))
plt.plot(rate)
plt.show()
