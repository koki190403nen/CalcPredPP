# %%
import numpy as np
from MyThread import MyThread, FitGamma_multi
import datetime
from matplotlib import pyplot as plt

print(datetime.datetime.now())
# %%
RR95_img, RR99_img = FitGamma_multi(n=3, h=320, w=300, span=20)
print('Complete')
print(datetime.datetime.now())
# %%
plt.imshow(RR95_img)