#!/usr/bin/env python3

import queue

# IVE ONLY KEYED IN THE FIRST MAZE
maze_walls = {
  ((0,1),(5,2)):
    (
      [(1,0),(4,0),(5,0),(2,1),(3,1),(4,1),(1,2),(4,2),(1,3),(2,3),(3,3),(4,3),(1,4),(4,4)],
      # coordinates of tiles with inner bottom walls
      [(2,0),(0,1),(2,1),(0,2),(2,2),(0,3),(3,3),(2,4),(4,4),(1,5),(3,5)]
      # coordinates of tiles with inner right walls
    ),
  ((1,3),(4,1)):
    (
      [],
      []
    ),
  ((3,3),(5,3)): 
    (
      [],
      []
    ),
  ((0,0),(0,3)): 
    (
      [],
      []
    ),
  ((3,5),(4,2)): 
    (
      [],
      []
    ),
  ((2,4),(4,0)): 
    (
      [],
      []
    ),
  ((1,0),(1,5)): 
    (
      [],
      []
    ),
  ((2,3),(3,0)): 
    (
      [],
      []
    ),
  ((0,4),(2,1)): 
    (
      [],
      []
    )
}

# constants for puzzle dimensions
WDT = HGT = 6

# given circle coordinates return wall data
def getWalls (p1, p2):
  for k in maze_walls:
    if (k == (p1,p2) or k == (p2,p1)):
      return maze_walls[k]
  return None

# MAZE DATA -------------------------------------------------------------------

# coordinate to index
def ctoi (p):
  x, y = p
  return x + y * WDT

# index to coordinate
def itoc (i):
  return (i%WDT,i//WDT)

# COORDINATE CONVERSION -------------------------------------------------------

def getGridAdjList(walls):
  adjList = [[] for i in range(WDT * HGT)]
  # initialize all to no connection
  if walls == None:
    return None
  bWall, rWall = walls
  for x in range(WDT):
    for y in range(HGT):
      s = (x,y)
      ts = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
      for z in range(4):
        if((x == 0 and z == 1)
        or (x == WDT - 1 and z == 0)
        or (y == 0 and z == 3)
        or (y == HGT - 1 and z == 2)
        # skip if out of bounds connections
        or (z == 0 and s in rWall)
        or (z == 1 and ts[1] in rWall)
        or (z == 2 and s in bWall)
        or (z == 3 and ts[3] in bWall)):
        # skip if walls block
          continue
        adjList[ctoi(s)].append(ctoi(ts[z]))
  return adjList

def printShortestPath(adjList, start, end):
  if adjList == None:
    return "No such maze exists, are you sure about those circle coordinates?"
  visited = [False for i in range(WDT * HGT)]
  endi = ctoi(end)
  Q = queue.Queue()
  Q.put((ctoi(start),[]))
  while not Q.empty():
    cur,path = Q.get()
    visited[cur] = True
    if cur == endi:
      path.append(cur)
      return indexPathToDirections(path)
    for n in filter(lambda i: not visited[i],adjList[cur]):
      nextPath = path.copy()
      nextPath.append(cur)
      Q.put((n,nextPath))
  return "no path exist"

# CORE ------------------------------------------------------------------------

# determine direction of travel from p1 to p2 if neighbouring
# if not neighbouring "X" is returned
def getDirection (p1, p2):
  x1, y1 = p1
  if (x1+1,y1) == p2:
    return "R"
  elif (x1-1,y1) == p2:
    return "L"
  elif (x1,y1+1) == p2:
    return "D"
  elif (x1,y1-1) == p2:
    return "U"
  return "X"

def indexPathToDirections (path):
  path = list(map(itoc,path))
  return ",".join(map(getDirection, path[: len(path) - 1], path[1:]))

# PRINTING --------------------------------------------------------------------

print(
  printShortestPath(
    getGridAdjList(
      getWalls(
        (
          int(input("Circle 1 x:")),
          int(input("Circle 1 y:"))
        ),
        (
          int(input("Circle 2 x:")),
          int(input("Circle 2 y:"))
        )
      )
    ),
    (int(input("start x:")),int(input("start y:"))),
    (int(input("end x:")),int(input("end y:")))
  )
)

# I/O -------------------------------------------------------------------------