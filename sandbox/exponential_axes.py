from axes_3d import *
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(6., 4))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0,4)
ax.set_ylim(-1.1,1.1)
ax.set_zlim(-1.1,1.1)

ax.scatter(0, 0, 0, s=30, marker='o')

ax.scatter(0, 0, 1, s=30, marker='o', color='black')
ax.scatter(0, 1, 0, s=30, marker='o', color='black')
    
ax.annotate3D('$\overline{0}$', (0, 0, 0), xytext=(3, 3), textcoords='offset points')
ax.annotate3D('$t$ (s)', (4, 0, 0), xytext=(3, 3), textcoords='offset points')
ax.annotate3D('$1$', (0, 1, 0), xytext=(3, 3), textcoords='offset points')
ax.annotate3D('$i$', (0, 0, 1), xytext=(3, 3), textcoords='offset points')

ax.arrow3D(0,0,-2,
           0,0,4,
           mutation_scale=20,
           arrowstyle="-|>",
           linestyle='dashed')
ax.arrow3D(0,-2,0,
           0,4,0,
           mutation_scale=20,
           arrowstyle="-|>",
           linestyle='dashed')
ax.arrow3D(0,0,0,
           4,0,0,
           mutation_scale=20,
           arrowstyle="-|>",
           linestyle='dashed')
#ax.set_title('3D Arrows Demo')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.tight_layout()

#fig = plt.figure()
#ax = plt.axes(xlim=(0, 3), ylim=(-1, 1), zlim=(-1, 1), projection='3d')

# Data for a three-dimensional line
f_0 = 1.5

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

animation.save('animation_axes.gif', fps=fps, savefig_kwargs={"transparent": True})

#plt.show()


