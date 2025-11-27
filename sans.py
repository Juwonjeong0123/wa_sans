import math
import matplotlib.pyplot as plt

G = 6.6743e-11

class celestial_body:
    def __init__(self, mass, radius, x, y, z, v):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.v = v

earth = celestial_body(5.9722e24, 6400, 0, 150000000, 0, 29.7859)
sun = celestial_body(1.9885e30, 690000, 0, 0, 0, 0)

class Simulation:
    def __init__(self, dt_time, G, celestial, time_wa):
        self.dt_time  = dt_time
        self.G = G
        self.celestial = celestial
        self.time_wa = time_wa

    def update(self):
        self.celestial[0].v += self.force(self.celestial[0], self.celestial[1]) \
            / self.celestial[0].mass * self.dt_time
        self.celestial[0].x += self.net_force(self.celestial[0], self.celestial[1])[0] * self.celestial[0].v * self.dt_time
        self.celestial[0].y += self.net_force(self.celestial[0], self.celestial[1])[1] * self.celestial[0].v * self.dt_time
        self.celestial[0].z += self.net_force(self.celestial[0], self.celestial[1])[2] * self.celestial[0].v * self.dt_time

        # print(self.celestial[0].v)
        # print(self.celestial[0].x, self.celestial[0].y, self.celestial[0].z)
        
        return [self.celestial[0].x,  self.celestial[0].y, self.celestial[0].z]


    def force(self, a, b):
        if math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2) == 0:
            return 0

        return G * a.mass * b.mass / math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)

    def net_force(self, a, b):
        vec = [b.x - a.x, b.y - a.y, b.z - a.z]
        r = math.sqrt(((b.x - a.x) ** 2) + ((b.y - a.y) ** 2) * ((b.z - a.z) ** 2))

        if r == 0:
            return vec
        
        vec[0] = vec[0]/r 
        vec[1] = vec[1]/r 
        vec[2] = vec[2]/r

        return vec


li = [earth, sun]

simulation = Simulation(1, G, li, 1)

um_ma = [[], [], []]


for i in range(60*60*1, 24*365):
    um_ma[0].append(simulation.update()[0])
    um_ma[1].append(simulation.update()[1])
    um_ma[2].append(simulation.update()[2])

fig = plt.figure()
ax = plt.axes(projection="3d")

x = um_ma[0]
y = um_ma[1]
z = um_ma[2]

ax.set_xlim(-1000000000000, 1000000000000)
ax.set_ylim(-1000000000000, 1000000000000)
ax.set_zlim(-1000000000000, 1000000000000)

print(um_ma)

ax.plot3D(x, y, z, 'red')
ax.set_title("zzz")
plt.show()





