import math
import matplotlib.pyplot as plt

G = 6.6743e-11

class Body:
    def __init__(self, name, mass, radius, x, y, z, vx, vy, vz):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

sun  = Body("Sun", 1.9885e30, 6.90e8, 0.0,        0.0, 0.0,   0.0,    0.0,   0.0)
earth1 = Body("Earth", 5.9722e24, 6.371e6,  1.496e11, 0.0, 0.0,   0.0,  29785.0, 0.0)

bodies = [sun, earth1]
# bodies = [earth1, earth2, earth3]

class Simulation:
    def __init__(self, bodies, dt, G=6.67430e-11):
        self.bodies = bodies
        self.dt = dt
        self.G = G

    def acceleration_on(self, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z

        r2 = dx*dx + dy*dy + dz*dz

        if r2==0:
            return (0.0, 0.0, 0.0)

        r = math.sqrt(r2)

        factor = self.G * b.mass / (r2 * r)
        return (factor * dx, factor * dy, factor * dz)

    def step(self):
        accs = []

        for i, a in enumerate(self.bodies):
            ax = ay = az = 0.0 
            for j, b in enumerate(self.bodies):
                if i == j:
                    continue

                dax, day, daz = self.acceleration_on(a, b)

                ax += dax
                ay += day
                az += daz

            accs.append((ax, ay, az))

        # 속도(반암시적) 업데이트 -> 위치 업데이트
        for i, body in enumerate(self.bodies):
            ax, ay, az = accs[i]
            # 속도 업데이트
            body.vx += ax * self.dt
            body.vy += ay * self.dt
            body.vz += az * self.dt
            # 위치 업데이트
            body.x += body.vx * self.dt
            body.y += body.vy * self.dt
            body.z += body.vz * self.dt

        # 한 스텝 후 모든 몸체의 위치 반환
        return [(b.x, b.y, b.z) for b in self.bodies]

"""    def update(self):
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
            return [0, 0, 0]
        
        vec[0] = vec[0]/r 
        vec[1] = vec[1]/r 
        vec[2] = vec[2]/r

        return vec
"""

dt = 3600.0 
# dt = 3600.0 * 24
sim = Simulation(bodies, dt)

steps = 24 * 365
# steps = 365 * 100



# 위치 기록 리스트 (각 몸체마다 별도의 리스트)
trajectories = [ ([], [], []) for _ in bodies ]  # list of (xs, ys, zs)

for _ in range(steps):
    positions = sim.step()   # 한 번의 step으로 모든 bodies가 전진됨
    for i, pos in enumerate(positions):
        x, y, z = pos
        trajectories[i][0].append(x)
        trajectories[i][1].append(y)
        trajectories[i][2].append(z)

# 플롯
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

colors = ['yellow', 'red']  # Sun, earth1, earth2, earth3
# colors = ['red', 'blue', 'green']  # Sun, earth1, earth2, earth3
for i, body in enumerate(bodies):
    xs, ys, zs = trajectories[i]
    ax.plot(xs, ys, zs, label=body.name, color=colors[i])
    # 마지막 위치에 점 표시 (현재 위치)
    ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color=colors[i], s=30)

ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.set_title('All orbits (1 year, dt=1 hour)')
ax.legend()
plt.show()

"""
xs1 = []
ys1 = []
zs1 = []
xs2 = []
ys2 = []
zs2 = []
xs3 = []
ys3 = []
zs3 = []


for _ in range(steps):
    x1, y1, z1 = sim.step(0)
    xs1.append(x1)
    ys1.append(y1)
    zs1.append(z1)
for _ in range(steps):
    x2, y2, z2 = sim.step(1)
    xs2.append(x2)
    ys2.append(y2)
    zs2.append(z2)
for _ in range(steps):
    x3, y3, z3 = sim.step(2)
    xs3.append(x3)
    ys3.append(y3)
    zs3.append(z3)



li = [earth, sun]

simulation = Simulation(1, G, li, 1)

um_ma = [[], [], []]


for i in range(60*60*1, 24*365):
    um_ma[0].append(simulation.update()[0])
    um_ma[1].append(simulation.update()[1])
    um_ma[2].append(simulation.update()[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs1, ys1, zs1, color='red')
ax.plot(xs2, ys2, zs2, color='blue')
ax.plot(xs3, ys3, zs3, color='yellow')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.set_title("sans")
plt.show()
"""




