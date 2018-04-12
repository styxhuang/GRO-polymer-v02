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
    atomtypes = topInfo.getAtomTypes()
    atoms = topInfo.getAtoms()
    bonds = topInfo.getBonds()
    pairs = topInfo.getPairs()
    angles = topInfo.getAngles()
    dihedrals = topInfo.getDihedrals()
    
    top.appendAtomTypes(atomtypes)
    init_idx = top.appendAtoms(atoms)
    top.appendBonds(init_idx, bonds)
    top.appendPairs(init_idx, pairs)
    top.appendAngles(init_idx, angles)
    top.appendDihedrals(init_idx, dihedrals)
    
    return top

def CombineTop(monTop, croTop, monName, croName, molList): #This function will return a sum top class, then use readTop.TopInfoExport(top) to write the top file
    top = Top.TopInfo()
    
    for i in range (len(molList)):
        mol = molList[i]
        name = mol.getName()
        if name == monName:
            if len(top.getAtoms()) == 0:
                top = getTop(monTop)
            else:
                mon_top = getTop(monTop)
                top = AppendTopInfo(mon_top, top)
        else:
            if len(top.getAtoms()) == 0:
                top = getTop(croTop)
            else:
                cro_top = getTop(croTop)
                top = AppendTopInfo(cro_top, top)   
    
    return top


fileName1 = 'MON.top'
fileName2 = 'CRO.top'
groFile = 'system.gro'

top_mon = getTop(fileName1)
top_cro = getTop(fileName2)

groInfo = readGRO.ReadGro(groFile) #basic gro info, atoms list, molecules list

a = CombineTop(fileName1, fileName2, 'MON', 'CRO', groInfo[2]) #fileName1 is the file includes monomer's information

readTop.TopInfoExport(a)