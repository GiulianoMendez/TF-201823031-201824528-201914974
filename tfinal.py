import numpy as np
import math
import random
import heapq as hq
import datetime as dt
from perlin_noise import PerlinNoise
from math import sin, cos, sqrt, atan2, radians

def dijkstra(G, s):
  n = len(G)
  visited = [False]*n
  path = [-1]*n
  cost = [math.inf]*n

  cost[s] = 0
  pqueue = [(0, s)]
  while pqueue:
    g, u = hq.heappop(pqueue)
    if not visited[u]:
      visited[u] = True
      for v, w in G[u]:
        if not visited[v]:
          f = g + w
          if f < cost[v]:
            cost[v] = f
            path[v] = u
            hq.heappush(pqueue, (f, v))

  return path, cost

  #Funcion para agregar una arista
def addEdge(adj, u, v, w):
 
    adj[u].append((v, w));
    adj[v].append((u, w));

    # Funcion para eliminar una arista
def delEdge(adj,  u,  v):
    aux = math.inf
    for i in range(len(adj[u])):
        if (adj[u][i][0] == v):
          # Adicionalmente guardaremos el valor del peso 
            aux = adj[u].pop(i)[1]
            break
    for i in range(len(adj[v])):
     
        if (adj[v][i][0] == u):
             
            adj[v].pop(i)
            break
          # Y lo retornaremos
    return aux

def ruta(start,end,path):
  # Se obtiene el nodo inicial, destino y el camino
  ruta = [ ]
  aux = end
  # Se va recorriendo el camino y añadiendo los nodos recorridos desde el
  # destino hasta el final
  while aux != start:
   aux = path[aux]
   if (aux != start):
    ruta.append(aux)
  ruta.reverse()
  return ruta

# Funcion para hallar la ruta más corta
def first(G, start,end):
  path, cost = dijkstra(G,start)
  aux = ruta(start,end,path)
  return aux,cost[end]

# Funcion para hallar la 2da ruta más corta
def second(G,start,end):
  path, cost = dijkstra(G,start)
  aux = path[end]
  # Eliminamos la arista y guardamos el peso
  pesoaux = delEdge(G,end,aux)
  # Una vez eliminado el camino entre el nodo por el cual se accedia 
  # al nodo final a través de la ruta más corta, aplicamos dijkstra otra 
  # vez y encontraremos la 2da ruta más corta
  path1, cost1 = dijkstra(G,start)
  aux1 = ruta(start,end,path1)
  # Volvemos a agregar dicha arista con su respectivo peso
  # para que el grafo no se vea afectado
  addEdge(G, end, aux, pesoaux)
  return aux1,cost1[end]

# Funcion para hallar la 3ra ruta más corta
def third(G,start,end):
  path, cost = dijkstra(G,start)
  aux = path[end]
  # Aplicaremos el mismo método para hallar la 3ra ruta más corta
  pesoaux = delEdge(G,end,path[end])
  path1, cost1 = dijkstra(G,start)
  aux1 = path1[end]
  pesoaux1 = delEdge(G,end,path1[end])
  path2, cost2 = dijkstra(G,start)
  aux2 = ruta(start,end,path2)
  # Agregamos las aristas que quitamos con sus respectivos pesos
  addEdge(G, end, aux, pesoaux)
  addEdge(G, end, aux1, pesoaux1)
  return aux2,cost2[end]

# Crearemos una función que consolide las anteriores 3 funciones y nos retorne 
# todas las rutas en una sola pasada, evitando así tener que ejecutar dijkstra 
# una y otra vez
def getRutas(G, start, end):
  path, cost = dijkstra(G,start)
  shortest = ruta(start,end,path) #Ruta más corta
  aux = path[end]

  pesoaux = delEdge(G,end,aux) # Primer arista borrada
  path1, cost1 = dijkstra(G,start)
  shorter = ruta(start,end,path1) # 2da ruta más corta
  aux1 = path1[end]
  pesoaux1 = delEdge(G,end,path1[end]) #Segunda arista borrada
  path2, cost2 = dijkstra(G,start)
  short = ruta(start,end,path2) # 3ra ruta más corta

  # Agregamos las aristas borradas
  addEdge(G, end, aux, pesoaux)
  addEdge(G, end, aux1, pesoaux1)

  return shortest, cost[end], shorter, cost1[end], short, cost2[end]

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
    return random.uniform(3.5,4)
  if pic[m][n] <= 0.5 and pic[m][n] >= 0.3:
    return random.uniform(3,3.5)
  if pic[m][n] <= 0.3 and pic[m][n] >= 0.1:
    return random.uniform(2.5,3)
  if pic[m][n] <= 0.1 and pic[m][n] >= -0.1:
    return random.uniform(2,2.5)
  if pic[m][n] <= -0.1 and pic[m][n] >= -0.3:
    return random.uniform(1.5,2)
  if pic[m][n] <= -0.3 and pic[m][n] >= -0.5:
    return random.uniform(1,1.5)
  if pic[m][n] <= -0.5:
    return random.uniform(0.5,1)

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
  wide = 30 ## Aumentar para que los pesos sean más grandes
  return round(d*timevar*PrlNoiseVar*wide)


G = [[] for _ in range(len(nodes))]
prl = GenerarPerlinNoise(61,58)
tiempo = -1 ## Cambiar por si se desea usar una hora especifica
            ## o utilizar la función updateDayTime
for i in range(len(edges)):
  weight = GenerarPesos(edges[i], tiempo, prl)
  G[edges[i][0]].append((edges[i][1], weight))

Loc = [ (nodes[i][0], nodes[i][1]) for i in range(len(nodes))]