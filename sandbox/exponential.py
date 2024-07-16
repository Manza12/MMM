from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython import display 
from mpl_toolkits.mplot3d.proj3d import proj_transform


fig = plt.figure()
ax = plt.axes(xlim=(0, 3), ylim=(-1, 1), zlim=(-1, 1), projection='3d')

# Data for a three-dimensional line
f_0 = 2

xline = np.linspace(0, 3, 1000)
yline = np.cos(2*np.pi*f_0*xline)
zline = np.sin(2*np.pi*f_0*xline)
#ax.plot3D(xline, yline, zline, 'gray')

# lists storing x and y values 
x, y, z = [], [] , []

line, = ax.plot3D(0, 1, 0, c='k') 

ax.grid(False)
plt.axis('off')
           
fps=60

def animation_function(frame_number):
    t = frame_number / fps
    x.append(t)
    y.append(np.cos(2*np.pi*f_0*t))
    z.append(np.sin(2*np.pi*f_0*t))
    line.set_data_3d(x, y, z)
    return line, 


animation = FuncAnimation(fig,
                          func=animation_function,
                          frames=np.arange(fps*3),
                          interval=10)

animation.save('animation.gif', fps=fps)

