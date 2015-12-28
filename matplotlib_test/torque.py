from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

x = np.loadtxt('test1.csv', unpack=True, delimiter = ',')
y = np.loadtxt('test.csv', unpack=True, delimiter = ',')
plt.plot(x,y,'g',linewidth=5)
plt.title('Torque Speed c/c')
#plt.grid(True, color='k')
plt.show()

