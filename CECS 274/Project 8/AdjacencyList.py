"""An implementation of the adjacency list representation of a graph"""
from Interfaces import Graph, List
import numpy as np
import copy
import ArrayList
import ArrayStack
import ArrayQueue


class AdjacencyList(Graph):

  def __init__(self, n: int):
    self.n = n
    self.adj = np.zeros(n, dtype=ArrayList.ArrayList)
    for i in range(self.n):
      self.adj[i] = ArrayList.ArrayList()

  def add_edge(self, i: int, j: int):
    if i < 0 or i >= self.n or j < 0 or j >= self.n:
      raise IndexError("Invalid index")
    if not self.has_edge(i, j):
      self.adj[i].append(j)

  def remove_edge(self, i: int, j: int):
    if i < 0 or i >= self.n or j < 0 or j >= self.n:
      raise IndexError("Invalid index")
    for k in range(self.adj[i].size()):
      if self.adj[i].get(k) == j:
        self.adj[i].remove(k)

  def has_edge(self, i: int, j: int) -> bool:
    if i < 0 or i >= self.n or j < 0 or j >= self.n:
      raise IndexError("Invalid index")
    for k in range(self.adj[i].size()):
      if self.adj[i].get(k) == j:
        return True
    return False

  def out_edges(self, i) -> List:
    if i < 0 or i >= self.n:
      raise IndexError("Invalid index")
    return self.adj[i]
  
  def in_edges(self, j) -> List:
    if j < 0 or j >= self.n:
      raise IndexError("Invalid index")
    temp = []
    for i in range(self.n):
      if self.has_edge(i, j):
        temp.append(i)
    return temp

  def bfs(self, r: int):
    # initialize
    traversal = []
    seen = []
    for i in range(self.n):
      seen += [False]
    q = ArrayQueue.ArrayQueue()

    # visiting vertex
    q.add(r)
    traversal += [r]
    seen[r] = True

    while q.size() != 0:
      current = q.remove()
      neighbors = self.out_edges(current)
      for neighbor in neighbors:
        if not seen[neighbor]:
          q.add(neighbor)
          traversal += [neighbor]
          seen[neighbor] = True
    return traversal
    
  def dfs(self, r: int):
    # initialize
    traversal = []
    s = ArrayStack.ArrayStack()
    seen = []
    for i in range(self.n):
      seen += [False]
    s.push(r)

    while s.size() != 0:
      current = s.pop()
      if not seen[current]:
        traversal += [current]
        seen[current] = True
        neighbors = self.out_edges(current)
        for neighbor in reversed(neighbors):
          if seen[neighbor] == False:
            s.push(neighbor)
    return traversal

  def size(self):
    return self.n
  
  def __str__(self):
    s = ""
    for i in range(0, self.n):
      s += "%i:  %r\n" % (i, self.adj[i].__str__())
    return s

  def __str__(self):
    s = ""
    for i in range(0, self.n):
      s += "%i,%r\n" % (i, self.adj[i].__str__())
    return s
