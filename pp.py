import matplotlib.pyplot as plt
import numpy as np
x=np.array([1,3,2,4,5,2])

y=np.array([3,8,1,10,7,9])
plt.subplot(1,2,1)
plt.plot(x,y)
plt.title("hello")
x=np.array([1,2,3,4,5])
y=np.array([3,4,5,6,7])
plt.subplot(1,2,2)
plt.plot(x,y)
plt.title("sale")
plt.suptitle("hiii")
plt.show()