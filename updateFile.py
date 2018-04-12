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

def UpdateTop(idx):
    top = getTop('MON.top')
    top.updateAtoms(idx+1) #because the top index starts from 1

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
def CmpList(list1, list2): #list1 is the ori, list2 after deleted
    idx = []
    tmp = 0
    i = 0
    while ((i - tmp) < len(list2)):
#        print('i', i)
#        print('list1[i]', list1[i])
#        print('list2[i + tmp]', list2[i - tmp])
        if list1[i] != list2[i - tmp]:
            idx.append(i)
            tmp += 1
#        print('tmp', tmp, '\n')
        i += 1
    return idx
        
def CombineTop(monTop, croTop, monName, croName, morName, crorName, molList): #This function will return a sum top class, then use readTop.TopInfoExport(top) to write the top file
    top = Top.TopInfo()
    
    for i in range (len(molList)):
        mol = molList[i]
        name = mol.getName()
#        print('name', name)
#        print('morName: ', morName)
        if name == monName:
            if len(top.getAtoms()) == 0:
                top = getTop(monTop)
            else:
                mon_top = getTop(monTop)
                top = AppendTopInfo(mon_top, top)
        elif name == croName:
            if len(top.getAtoms()) == 0:
                top = getTop(croTop)
            else:
                cro_top = getTop(croTop)
                top = AppendTopInfo(cro_top, top)   
        elif name == morName:
            top_st = getTop(monTop)
            name_st = top_st.getAtomsName()
            name = mol.getAtomsName()
#            print(name_st)
#            print(name)
            a = CmpList(name_st, name) #Can get all deleted atoms index in the ori top files
            print('a: ', a)
            for i in range (len(a)):
                print(name_st[a[i]])
                UpdateTop(a[0])
    return top

def DelAtomGRO(atom_idx, rename, atomList, molList): #Get del atom index and update gro file
        
    for atom in atomList:
        idx = atom.getglobalIndex()
        if idx == atom_idx:
            molNum = int(atom.getmolNum())
            idx_local = atom.getlocalIndex()
        
    molList[molNum - 1].delAtoms(idx_local, rename)
    molList[molNum - 1].outputInfo()
    
    readGRO.ExportGRO(['','',''], 'tsttst.gro', molList)
    return molList

fileName1 = 'MON.top'
fileName2 = 'CRO.top'
mon_react = 'MOR'
cro_react = 'COR'

groFile = 'tsttst.gro'

top_mon = getTop(fileName1)
#top_cro = getTop(fileName2)

groInfo = readGRO.ReadGro(groFile) #basic gro info, atoms list, molecules list

a = CombineTop(fileName1, fileName2, 'MON', 'CRO', 'MOR', 'COR', groInfo[2]) #fileName1 is the file includes monomer's information

#readTop.TopInfoExport(a)

#a = DelAtomGRO(22, 'MOR', groInfo[1], groInfo[2])