# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:55:55 2020

@author: Janek
"""

from PIL import Image, ImageDraw 
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
def Initialize():
    global L, L0 
    L=10*np.random.rand(width)
    L=np.floor(L)
    L=np.mod(L,2)
    L=np.array(list(L), dtype=int)
    L0=10*np.random.rand(width)
    L0=np.floor(L0)
    L0=np.mod(L,2)
    L0=np.array(list(L0), dtype=int)
    return(L)
def Bit(number):
    rulebinary=''
    end=str("{0:b}".format(number))
    zeros=width-len(end)
    for i in range(zeros):
        rulebinary+='0'
    return(rulebinary+end)

def Decimal(array):
    array=np.flip(array)
    return(np.sum(array*(2**np.arange(width))))
def ArrayRule(string):
    string=string[::-1]
    return(np.fromiter(string, dtype=int))
def neighbourhood_detection():
   global L,neighbourhood
   left=np.roll(L,-1)
   right=np.roll(L,1)
   neighbourhood=right*4+L*2+left*1 
def update():
    global rulearray,L,newstate
    newstate=rulearray[neighbourhood]
    L=newstate
    return(newstate)
def updateReversible():
    global rulearray,L,newstate, L0
    newstate=rulearray[neighbourhood]
    newstate=(newstate+L0)%2
    L0=L
    L=newstate
    return(newstate)

def display():
    global L
    data=L
    for dt in range(time):
        neighbourhood_detection()
        update()
        data=np.vstack((data,newstate))
    img = Image.new("RGB",(width,time),(255,255,255))
    draw = ImageDraw.Draw(img)
    for y in range(time):
        for x in range(width):
            if data[y][x]:
                draw.point((x,y),(0,0,0))
    img.save('CA90.png',"PNG")
def displayReversible():
    global L,L0
    #L0=np.array([0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0])
    #L=np.array([0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0])
    data=L0
    data=np.vstack((data,L))
    for dt in range(time):
        neighbourhood_detection()
        updateReversible()
        data=np.vstack((data,newstate))
    img = Image.new("RGB",(width,time),(255,255,255))
    draw = ImageDraw.Draw(img)
    for y in range(time):
        for x in range(width):
            if data[y][x]:
                draw.point((x,y),(0,0,0))
    img.save('CA90R1.png',"PNG")
def setup():
    global matrix
    matrix=np.zeros(width,dtype=int)
    for i in range(order):
        new=Bit(i)
        new=ArrayRule(new)
        matrix=np.vstack((matrix,new))
    matrix=np.unique(matrix,axis=0)
    return(matrix)
def entropy():
    global matrix
    states=np.zeros(0)
    for i in matrix:
       states= np.append(states,Decimal(i))
    a=Counter(states)
    p=np.fromiter(a.values(),dtype=float)/order
    return(np.sum(-p*np.log(p)))
def evolve():
    global L
    t=[]
    s=[]
    for dt in range(time):
        print(dt)
        s.append(entropy())
        t.append(dt)
        for i in range(order):
            L=matrix[i]
            neighbourhood_detection()
            matrix[i]=update()
    return(t,s)


width=12
time=40
order=2**width
T=[]
S=[]
#RuleBinary='00000001'
RuleDecimal=110
RuleBinary=Bit(RuleDecimal)
rulearray=ArrayRule(RuleBinary)
#Initialize()
setup()
T,S=evolve()
plt.plot(T, S, color='black', linestyle='-', linewidth=1)
# plots with a red line
plt.xlabel('Entropy', fontsize=14)
plt.xlabel('Time', fontsize=14)
plt.title('Rule 110 entropy evolution for 12 cells', fontsize=20)
plt.grid(True)
#plt.savefig("Entropy1.png")

