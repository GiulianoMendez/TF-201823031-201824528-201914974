import json
import random
import math
import heapq as hq
import datetime as dt
from math import sin, cos, sqrt, atan2, radians
from perlin_noise import PerlinNoise


nodes = []
edges = []
streets = []
with open("streets.txt") as nf:
  for line in nf:
    streets.append(line[:-1])
with open("nodes.txt") as nf:
  for line in nf:
    line_split_1 = list(map(lambda x: float(x), line.split()[:2]))
    line_split_2 = list(map(lambda x: int(x), line.split()[2:]))
    line_split = line_split_1 + line_split_2
    nodes.append(line_split)
with open("edges.txt") as nf:
  for line in nf:
    line_split = list(map(lambda x: int(x), line.split()))
    edges.append(line_split)

# Función para verificar si "x" se encuentra en el rango "start-end"
def time_in_range(start, end, x):
    # Return true if x is in the range [start, end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
# De ser necesario se puede actualizar la hora del trafico  
def updateDayTime(t, hour, min = 0, sec = 0):
  t = dt.time(hour,min,sec)
  return t
def trafficWeights(tim = -1):
  # Se establecen las horas de cambio de estado del tráfico
  sixAM = dt.time(6,0,0)
  nineAM = dt.time(9,0,0)
  twoPM = dt.time(14,0,0)
  sixPM = dt.time(18,0,0)
  ninePM = dt.time(21,0,0)
  elevenPM = dt.time(23,0,0)
  # Se obtiene la hora local en caso no se especifique una hora
  if tim == -1:
    tim = dt.datetime.now(dt.timezone(dt.timedelta(hours = -5))).time()
  if (time_in_range(sixAM,nineAM,tim) or time_in_range(sixPM,ninePM,tim)):
    state = 2
  elif (time_in_range(twoPM,sixPM,tim) or time_in_range(ninePM,elevenPM,tim)):
    state = 1.5
  else:
    state = 0.8
  return state
def GenerarPerlinNoise(a,b):
    noise1 = PerlinNoise(octaves=2)
    noise2 = PerlinNoise(octaves=4)
    noise3 = PerlinNoise(octaves=8)
    noise4 = PerlinNoise(octaves=12)
    xpix, ypix = a,b
    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise1([i/xpix, j/ypix])
            noise_val += 0.100 * noise2([i/xpix, j/ypix])
            noise_val += 0.070 * noise3([i/xpix, j/ypix])
            noise_val += 0.035 * noise4([i/xpix, j/ypix])
            row.append(noise_val)
      
        pic.append(row)
    return pic
def varPrlNoise(pic, edge, a, b):
  m = edge[0] % a
  n = edge[1] % b
  if pic[m][n] > 0.5:
    return random.randint(10000000,90000000)
  if pic[m][n] <= 0.5 and pic[m][n] >= 0.3:
    return random.randint(1000000,9000000)
  if pic[m][n] <= 0.3 and pic[m][n] >= 0.1:
    return random.randint(1,9000000000)
  if pic[m][n] <= 0.1 and pic[m][n] >= -0.1:
    return random.randint(10,100)
  if pic[m][n] <= -0.1 and pic[m][n] >= -0.3:
    return random.randint(20,50)
  if pic[m][n] <= -0.3 and pic[m][n] >= -0.5:
    return random.randint(10,20)
  if pic[m][n] <= -0.5:
    return random.randint(1,10)
def distancia(lat1, lon1, lat2, lon2):
  # approximate radius of earth in km
  R = 6373.0
  lat1 = radians(lat1)
  lon1 = radians(lon1)
  lat2 = radians(lat2)
  lon2 = radians(lon2)
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance = R * c
  return distance
def GenerarPesos(edge, time, prl):
  v1 = nodes[edge[0]]
  v2 = nodes[edge[1]]
  PrlNoiseVar = varPrlNoise(prl,edge,61,58)
  d = distancia(v1[0],v1[1], v2[0], v2[1])
  timevar = trafficWeights(time)
  wide = 1 ## Aumentar para que los pesos sean más grandes
  return round(d*timevar*PrlNoiseVar*wide)

def transformGraph():
  G = [[] for _ in range(len(nodes))]
  prl = GenerarPerlinNoise(61,58)
  tiempo = dt.time(7,0,0)
  ##tiempo = updateDayTime(tiempo,7,0,0) ## Cambiar por si se desea usar una hora especifica
              ## o utilizar la función updateDayTime
  for i in range(len(edges)):
    weight = GenerarPesos(edges[i], tiempo, prl)
    G[edges[i][0]].append((edges[i][1], weight))

  Loc = [(nodes[i][0], nodes[i][1]) for i in range(len(nodes))]
  return G, Loc

def bfs(G, s):
  n= len(G)
  visited= [False]*n
  path= [-1]*n # parent
  queue= [s]
  visited[s]= True

  while queue:
    u= queue.pop(0)
    for v, _ in G[u]:
      if not visited[v]:
        visited[v]= True
        path[v]= u
        queue.append(v)

  return path

def dfs(G, s, t):
  n= len(G)
  path= [-1]*n
  visited= [False]*n

  stack= [s]
  while stack:
    u= stack.pop()
    visited[u]= True
    if u == t:
        break
    for v, _ in G[u]:
      if not visited[v]:
        path[v]= u
        stack.append(v)

  return path

def dijkstra(G, s):
    n= len(G)
    visited= [False]*n
    path= [-1]*n
    cost= [math.inf]*n

    cost[s]= 0
    pqueue= [(0, s)]
    while pqueue:
        g, u= hq.heappop(pqueue)
        if not visited[u]:
            visited[u]= True
            for v, w in G[u]:
                if not visited[v]:
                    f= g + w
                    if f < cost[v]:
                        cost[v]= f
                        path[v]= u
                        hq.heappush(pqueue, (f, v))

    return path, cost

G, Loc= transformGraph()

def graph():
    return json.dumps({"loc": Loc, "g": G})


def paths(s, t):
    bestpath, _= dijkstra(G, s)
    path1= bfs(G, s)
    path2= dfs(G, s, t)

    return json.dumps({"bestpath": bestpath, "path1": path1, "path2": path2})