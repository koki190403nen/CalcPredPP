# %%
import numpy as np
from MyThread import MyThread, FitGamma_multi
import datetime
from matplotlib import pyplot as plt

print(datetime.datetime.now())
# %%
RR95_img, RR99_img = FitGamma_multi(n=3, h=1600, w=1500, span=100)
print('Complete')
print(datetime.datetime.now())
