# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 21:15:07 2018

1. Combine a full top file includes all atoms parameter
2. Update atoms index in top file
3. When update(delete) atoms, meanwhile update gro/top files

@author: HuangMing
"""

import sys
import pandas as pd

sys.path.insert(0, './class')

import TopClass as Top
import readGRO
import readTop



def getTop(fileName):
    topInfo = readTop.ReadTop(fileName)
    top = Top.TopInfo()
    top = readTop.TopInfoInput(topInfo, top)
    return top #return a top class

def AppendTopInfo(topInfo, top):
    print('type', type(topInfo))
    atomtypes = topInfo.getAtomTypes()
    atoms = topInfo.getAtoms()
    bonds = topInfo.getBonds()
    pairs = topInfo.getPairs()
    angles = topInfo.getAngles()
    dihedrals = topInfo.getDihedrals()
    
    top.appendAtoms(atoms)
    return top

def CombineTop(monTop, croTop, monName, croName, molList): #This function will return a sum top class, then use readTop.TopInfoExport(top) to write the top file
    top = Top.TopInfo()
    
    i=0
    
    for i in range (len(molList)):
        print('stp: ', i)
        mol = molList[i]
        name = mol.getName()
        if name == monName:
            print("mon: ", len(top.getAtoms()))
            if len(top.getAtoms()) == 0:
                print('1st stp')
                top = getTop(monTop)
            else:
                print('2nd stp')
                mon_top = getTop(monTop)
                top = AppendTopInfo(mon_top, top)
        else:
            print("cro: ", len(top.getAtoms()))
            if len(top.getAtoms()) == 0:
                top = getTop(croTop)
            else:
                print('cro_step: ', 2)
                cro_top = getTop(croTop)
                print(cro_top)
                top = AppendTopInfo(cro_top, top)
                
    return top

fileName1 = 'MON.top'
fileName2 = 'CRO.top'
groFile = 'system.gro'

top_mon = getTop(fileName1)
top_cro = getTop(fileName2)

groInfo = readGRO.ReadGro(groFile) #basic gro info, atoms list, molecules list
#
#atomTypes_Top = top_mon.getAtomTypesList()
#atomName_Top = top_mon.getAtomsName() #Need to compare to decide which atom needs to be deleted
a = CombineTop(fileName1, fileName2, 'MON', 'CRO', groInfo[2])
#b = CombineTop(fileName1, fileName2, 'MON', 'CRO', groInfo[2])

readTop.TopInfoExport(a)