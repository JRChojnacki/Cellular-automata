# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 22:37:30 2020

@author: Janek
"""
from PIL import Image, ImageDraw 
import numpy as np
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
    
def Bit(number):
    rulebinary=''
    end=str("{0:b}".format(number))
    zeros=width-len(end)
    for i in range(zeros):
        rulebinary+='0'
    return(rulebinary+end)

def Decimal(string):
    Rulebinary=string
    Rulebinary=Rulebinary[::-1]
    Ruledecimal=0
    j=0
    for i in Rulebinary:
        i=int(i)
        Ruledecimal+=i*2**j
        j+=1
        print(i,' ',Ruledecimal)
    return(Ruledecimal)
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
    img.save('test.png',"PNG")
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
    img.save('testR.png',"PNG")
 
width=300
time=500
#RuleBinary='00000001'
RuleDecimal=110
RuleBinary=Bit(RuleDecimal)
rulearray=ArrayRule(RuleBinary)
Initialize()
displayReversible()
#display()
