import random
import sys
import os

id = list()
node = input("Number of nodes: ")
edges = input("Number of edges: ")
def initialize():
    for i in range(1,int(node)+1):
        id.append(i)
def root(x):
    if (x != id[x]):
        id[x] = id[id[x]]
        x = id[x]
    return x
initialize()
v = []
weight =[]
for i in range(1,int(edges)+1):
    v.append(list())

for i in range(1,int (edges)+1):
    a, b, curr_w = map(int, input().split())
    weight.append(curr_w)
    v[int(a)-1].append(int(b))
for i in range(int(node)):
    v[i].append(int(weight[i]))

v.sort()
print(v)
