# %%
import numpy as np
from matplotlib import pyplot as plt

# %%
def combine():
    h,w = 400, 1500
    R95_out = np.zeros((1600,w))
    R99_out = np.zeros((1600,w))

    R95_n0 = np.fromfile('./img/RR95_n0.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    R95_n1 = np.fromfile('./img/RR95_n1.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    R95_n2 = np.fromfile('./img/RR95_n2.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    R95_n3 = np.fromfile('./img/RR95_n3.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)

    R95_out[0:400,:] = R95_n0
    R95_out[400:800,:] = R95_n1
    R95_out[800:1200,:] = R95_n2
    R95_out[1200:1600,:] = R95_n3



    R99_n0 = np.fromfile('./img/RR99_n0.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    try:
        R99_n1 = np.fromfile('./img/RR99_n1.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    except:
        R99_n1 = np.zeros((h,w), dtype=np.float64)
    R99_n2 = np.fromfile('./img/RR99_n2.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)
    R99_n3 = np.fromfile('./img/RR99_n3.A1900001.h400w1500.raw', count=h*w, dtype=np.float64).reshape(h,w)

    R99_out[0:400,:] = R99_n0
    R99_out[400:800,:] = R99_n1
    R99_out[800:1200,:] = R99_n2
    R99_out[1200:1600,:] = R99_n3

    return R95_out, R99_out


# %%
R95_img, R99_img = combine()
plt.figure(dpi=100)
plt.imshow(R95_img, 'jet')
plt.colorbar()
plt.title(r'RR 95%ile')
plt.show()


plt.figure(dpi=100)
plt.imshow(R99_img, 'jet')
plt.colorbar()
plt.title(r'RR 99%ile')
plt.show()
# %%
R95_img.tofile('./img/RR95.A1900001.float64_h1600w1500.raw')
R99_img.tofile('./img/RR99.A1900001.float64_h1600w1500.raw')