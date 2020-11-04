# @Author: ASHISH SASMAL <ashish>
# @Date:   04-11-2020
# @Last modified by:   ashish
# @Last modified time: 05-11-2020



import cv2
import numpy as np
import time
import sys
from custom_heap import heappush, heappop

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.d=float('inf')
        self.parent = None



def build(img,srcx,srcy,matrix,q):
    rows,cols=img.shape[0],img.shape[1]
    for r in range(rows):
        for c in range(cols):
            matrix[r][c] = Point(c,r)
            q.append(matrix[r][c])
    matrix[srcy][srcx].d = 0

def eqDis(img,u,v):
    if img[v]>150:
        return 2
    else:
        return float("inf")

def getNeighbors(matrix,x,y):
    l=[]
    if x>0 : # above
        l.append(matrix[x-1][y])
    if y>0 : # left
        l.append(matrix[x][y-1])
    if x<len(matrix)-1 :  # below
        l.append(matrix[x+1][y])
    if y<len(matrix[0])-1 :  # right
        l.append(matrix[x][y+1])

    return l


img = cv2.imread(f"Test/{sys.argv[1]}",0)
matrix =[]
rows,cols=img.shape[0],img.shape[1]
for r in range(rows):
    matrix.append([0]*cols)

src = (119,8)
q=[]
build(img,src[0],src[1],matrix,q)
print(len(matrix),len(matrix[0]))
print(img.shape)

heappush(q,matrix[src[1]][src[0]])

c=0
while q!=[]:
    c+=1
    u = heappop(q)
    neighbors = getNeighbors(matrix,u.y,u.x)
    # print(neighbors)
    for v in neighbors:
        dst = eqDis(img,(u.y,u.x),(v.y,v.x))
        if u.d+dst<v.d:
            v.d = u.d+dst
            v.parent = (u.x,u.y)
            heappush(q,v)

print(c)
dst = (108,108)
path=[]
temp=matrix[dst[1]][dst[0]]
path.append((dst[0],dst[1]))
c=0
while(temp.x!=src[0] or temp.y!=src[1]):
    path.append((temp.x,temp.y))
    temp=matrix[temp.parent[1]][temp.parent[0]]

path.append((src[0],src[1]))
print(len(path))
img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

x0,y0=path[0]
for Point in path[1:]:
    x1,y1=Point
    cv2.line(img,(x0,y0),(x1,y1),(0,255,0),2)
    x0,y0=Point
    cv2.imshow("Output",img)
    cv2.waitKey(0)

cv2.imwrite("Result/result2.png",img)
