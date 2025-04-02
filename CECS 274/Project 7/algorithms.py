"""Implementations of some searching and sorting algorithms"""

import random
from Interfaces import List


def linear_search(a: List, x):
  for i in range(len(a)):
    if a[i] == x:
      return i
  return -100


def binary_search(a: List, x):
  l = 0
  r = len(a) - 1
  if len(a) == 1:
    if a[0] == x:
      return 1
    else:
      return -100
  while l <= r:
    m = (l + r) // 2
    if m == 0:
      if a[1] == x:
        return 2
      else:
        return -100
    if a[m] == x:
      return m
    elif a[m] > x:
      b = a[:m]
      #print(b)
      r = binary_search(b, x)
      
      if r < 0:
        return -100
      else:
        return r
    else:
      b = a[m:]
      #print(b)
      #print(f'{len(a[:m])} to the left')
      r = binary_search(b, x) + len(a[:m])
      
      if r < 0:
        return -100
      else:
        return r
  

def _merge(a0: List, a1: List, a: List):
  i0 = 0
  i1 = 0
  for i in range(len(a)):
    if i0 == len(a0):
      a[i] = a1[i1]
      i1 += 1
    elif i1 == len(a1):
    	a[i] = a0[i0]
    	i0 += 1
    elif a0[i0] <= a1[i1]:
      a[i] = a0[i0]
      i0 += 1
    else:
      a[i] = a1[i1]
      i1 += 1
  return a
      

def merge_sort(a: List):
  if len(a) <= 1:
    return a
  m = len(a)//2
  a0 = a[:m]
  
  a1 = a[m:]
  a0 = merge_sort(a0)
  a1 = merge_sort(a1)
  
  return _merge(a0, a1, a)
    
def _partition(a, start, end):
  pivot = a[0]
  L = start
  R = end
  print(f'pivot = {pivot}')
  while L < R:
    L = None
    R = None
    for i in range(start, end):
      if a[i] > pivot and type(L) == type(None):
        L = i
        print(f'new L = {L}')
        
        
    for i in range(end, start, -1):
      if a[i] <= pivot and type(R) == type(None):
        R = i
        print(f'new R = {R}')
        
    print (f'if {L} < {R}')
    if L < R:
      a[L], a[R] = a[R], a[L]
      print(a)
    
  a[0], a[R] = a[R], a[0]
  print('pivot swapped')
  return R
    


def _quick_sort_f(a: List, start, end):
  print(f'if {start} < {end}')
  if start < end:
    print('partition called')
    p = _partition(a, start, end)
    print(a[start:end])
    print(f'p = {p}')
    _quick_sort_f(a, start, p-1)
    _quick_sort_f(a, p+1, end)
    
    
  
  


def _quick_sort_r(a: List, start, end):
  x = random.randint(start, end)
  a[start], a[x] = a[x], a[start]
  return _quick_sort_f(a, start, end)


def quick_sort(a: List, p=True):
  """
    sorts an ArrayList a using the quick sort algorithm.
    If parameter p is True, the quick sort algorithm uses a randomly chosen element from a as pivot.
    Otherwise, the quick sort algorithm uses the first element as pivot.
    """
  if p:
    _quick_sort_r(a, 0, len(a) - 1)
  else:
    _quick_sort_f(a, 0, len(a) - 1)
