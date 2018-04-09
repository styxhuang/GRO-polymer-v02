# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 10:18:53 2018

@author: HuangMing
"""
import sys
import pandas as pd

sys.path.insert(0, './class') #add another directory, where to put class module

import AtomClass as Atom
import MoleculeClass as Mol


def SplitString(s):
    string = []
    digit = []
    for i in s:
        if i.isdigit():
            digit.append(i)
        else:
            string.append(i)
    string = ''.join(string)
    dig = ''.join(digit)
    
    return dig, string

def AtomInfoInput(atom, line):
    str1 = SplitString(line[0])
    molNum = str1[0]
    molName = str1[1]
    atomName = line[1]
    atomIndex = line[2]
    atomPos = [round(float(line[3]), 3), round(float(line[4]), 3), round(float(line[5]), 3)]
    atom.setmolNum(molNum)   
    atom.setmolName(molName)
    atom.setatomName(atomName)
    atom.setglobalIndex(atomIndex)
    atom.setPos(atomPos)
    return atom


def SplitAtom(baseList):
    atomsList = []
    for i in range (len(baseList)):
        atom = Atom.AtomsInfo()
        atom = atomsList.append(AtomInfoInput(atom, baseList.iloc[i]))
    
    return atomsList

def MolInfoInput(index, name, atomList):
    mol = Mol.MoleculeInfo()
    mol.setIndex(str(int(index) + 1)) #this mol index start from 0
    mol.setName(name)
    for i in range(len(atomList)):
        atomList[i].setlocalIndex(i)
        mol.setAtoms(atomList[i])
    return mol

def GetTopMol(atomList): #get the top molecules from the list
    index = atomList[0].getmolNum()
    name = atomList[0].getmolName()
    i = 0
    localIndex = 0
    while (i < len(atomList)):
        idx = atomList[i].getmolNum()
        atomList[i].setlocalIndex(localIndex)
        if idx != index:
            mol = MolInfoInput(index, name, atomList[0:i])
            return i, mol
        i += 1
        localIndex += 1
    index = atomList[i-1].getmolNum()
    name = atomList[i-1].getmolName()
    mol = MolInfoInput(index, name, atomList[0:i])
    return i, mol

def Atom2Mol(atomsList):
    molList = []
    i = 0
    num = 1
    while i < len(atomsList):
        info = GetTopMol(atomsList[i:])
        mol = info[1]
        molList.append(mol)
        num += 1
        i += info[0]
    return molList

def ReadGro(fileName): #Return the system's info, list of atoms and molecules
    df = pd.read_csv(fileName, header=None, sep='\n', skip_blank_lines=False)
    baseList = df.iloc[2:-1].reset_index(drop=True)[0].str.split()
    molName = df.iloc[0][0]
    molNum = df.iloc[1][0]
    molSize = df.iloc[-1][0]
    info = [molName, molNum, molSize]
    
    atomsList = SplitAtom(baseList)
    molList = Atom2Mol(atomsList)

    return info, atomsList, molList

def CountAtoms(molList):
    num = 0
    for mol in molList:
        atoms = mol.getAtoms()
        for atom in atoms:
            num += 1
    return num

def ExportGRO(info, outputName, molList): #info includes system info, name, atoms num, size
    index = 1
    for i in range (len(molList)):
        length = len(molList[i].getAtoms())
        atoms = molList[i].getAtoms()
        for ii in range (len(atoms)):
            idx = index + ii
            atom = atoms[ii]
            atom.update(idx, globalIndex=True)
        index += length
    f = open(outputName, 'w')
    molName = info[0] + '\n'

    num = CountAtoms(molList)
    molNum = str(num) + '\n'
    molSize = info[2] + '\n'
    
    f.write(molName)
    f.write(molNum)

    for mol in molList:
        atoms = mol.getAtoms()
        for atom in atoms:
            str1 = atom.outputInfo() + '\n'
            f.write(str1)
    f.write(molSize)
    f.close()
    
fileName = 'system.gro'
outputName = 'tst.gro'
a = ReadGro(fileName)
ExportGRO(a[0], outputName, a[2])