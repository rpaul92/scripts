#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
# Richard Paul
# Simple barcode script, creates any legal barcode.


from Graphics import *


#-----------------------------------------------------
#Variable Declarations


serial = str(input("Please enter a 13-character string, only digits..."))
while len(serial) < 13:
    serial = '0'+ serial
sFactor = int(input("Please set scale 1-10...")) #pixel size of stripe
bcWidth = 113 * sFactor #in stripes
bcHeight = 113 * sFactor #in stripes

upperQuiet = 9 #in stripes
sideQuiet = 9 #in stripes

uQuiet = sFactor * upperQuiet
sQuiet = sFactor * sideQuiet

longBar = 95 #in stripes
lBarF = sFactor*longBar
shortBar = 90 #in stripes
sBarF = sFactor*shortBar

L_Group   = ["LLLLLL",  "LLGLGG",  "LLGGLG",  "LLGGGL",  "LGLLGG",  \
             "LGGLLG",  "LGGGLL",  "LGLGLG",  "LGLGGL",  "LGGLGL"] 
 
R_Group   = ["RRRRRR",  "RRRRRR",  "RRRRRR",  "RRRRRR",  "RRRRRR",  \
             "RRRRRR",  "RRRRRR",  "RRRRRR",  "RRRRRR",  "RRRRRR"] 
 
L_Code    = ["WWWBBWB", "WWBBWWB", "WWBWWBB", "WBBBBWB", "WBWWWBB", \
             "WBBWWWB", "WBWBBBB", "WBBBWBB", "WBBWBBB", "WWWBWBB"] 
 
G_Code    = ["WBWWBBB", "WBBWWBB", "WWBBWBB", "WBWWWWB", "WWBBBWB", \
             "WBBBWWB", "WWWWBWB", "WWBWWWB", "WWWBWWB", "WWBWBBB"] 
 
R_Code    = ["BBBWWBW", "BBWWBBW", "BBWBBWW", "BWWWWBW", "BWBBBWW", \
             "BWWBBBW", "BWBWWWW", "BWWWBWW", "BWWBWWW", "BBBWBWW"]

sList = []
for CH in serial:
    sList.append(CH)
    
Canvas = makeEmptyPicture(bcWidth,bcHeight, white)
L_Pattern = L_Group[int(sList[0])]
R_Pattern = R_Group[int(sList[0])]

offset = 0

#--------------------------------------------------------
#Functions

def longblack():
    global offset
    for y in range(sFactor):
        VerticalLine(Canvas,uQuiet+offset,sQuiet,sQuiet+lBarF,black)
        offset += 1

def longwhite():
    global offset
    for y in range(sFactor):
        VerticalLine(Canvas,uQuiet+offset,sQuiet,sQuiet+lBarF,white)
        offset += 1     

def shortblack():
    global offset
    for y in range(sFactor):
        VerticalLine(Canvas,uQuiet+offset,sQuiet,sQuiet+sBarF,black)
        offset += 1
        
def shortwhite():
    global offset
    for y in range(sFactor):
        VerticalLine(Canvas,uQuiet+offset,sQuiet,sQuiet+sBarF,white)
        offset += 1 

def endGuard():
    global offset
    longblack()
    longwhite()
    longblack()

def leftGroup():
    global offset
    for p in range(6):
        if(L_Pattern[p] == 'L'):
            for i in range(len(L_Code[int(sList[p+1])])):
                if(L_Code[int(sList[p+1])][i] == 'B'): shortblack()
                elif(L_Code[int(sList[p+1])][i] == 'W'): shortwhite()
        elif(L_Pattern[p] == 'G'):
            for j in range(len(G_Code[int(sList[p+1])])):
                if(G_Code[int(sList[p+1])][j] == 'B'): shortblack()
                elif(G_Code[int(sList[p+1])][j] == 'W'): shortwhite()

def midGuard():
    global offset
    longwhite()
    longblack()
    longwhite()
    longblack()
    longwhite()


def rightGroup():
    global offset
    for z in range(6):      
        for k in range(len(R_Code[int(sList[z+7])])):
            if(R_Code[int(sList[z+7])][k] == 'B'): shortblack()
            elif(R_Code[int(sList[z+7])][k] == 'W'): shortwhite()
    
#------------------------------------------------------------------------
#Main Program



endGuard()
leftGroup()
midGuard()
rightGroup()
endGuard()
WriteBMP('BarCode.bmp',Canvas)
print("The barcode has been successfully created.")
