# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 11:16:50 2018

@author: HuangMing
"""

#from residue name export top info, seperate into three sections

import sys
import pandas as pd

sys.path.insert(0, './class')

import AtomClass as Atom
import MoleculeClass as Mol
import TopClass as Top

def CheckIndex(key, df): #get start and end index for a section
    idx = df.index[df[0].str.contains(key)].tolist()[0]
    df_end = df.iloc[idx:]
    idx_end = df_end.index[df_end[0].str.contains(';##########')].tolist()[0]
    return idx, idx_end

def ReadTop(fileName): #Get information from the monomer top file
    df_ori = pd.read_csv(fileName, header=None, skip_blank_lines=False, sep='\n')
    df = df_ori.fillna(';##########') #fill the blank row with 10 '#'
    idx0 = CheckIndex('defaults', df) 
    idx1 = CheckIndex('atomtypes', df)
    idx2 = CheckIndex('moleculetype', df)
    idx3 = CheckIndex('atoms', df)
    idx4 = CheckIndex('bonds', df)
    idx5 = CheckIndex(' pairs', df)
    idx6 = CheckIndex('angles', df)
    idx7 = CheckIndex('dihedrals', df)
    
    defaults = df.iloc[idx0[0]:idx0[1]+1].reset_index(drop=True)
    atomType = df.iloc[idx1[0]:idx1[1]+1].reset_index(drop=True)
    moleculeType = df.iloc[idx2[0]:idx2[1]+1].reset_index(drop=True)
    atoms = df.iloc[idx3[0]:idx3[1]+1].reset_index(drop=True)
    bonds = df.iloc[idx4[0]:idx4[1]+1].reset_index(drop=True)
    pairs= df.iloc[idx5[0]:idx5[1]+1].reset_index(drop=True)
    angles = df.iloc[idx6[0]:idx6[1]+1].reset_index(drop=True)
    dihedrals = df.iloc[idx7[0]:idx7[1]+1].reset_index(drop=True)
    
    return atomType, moleculeType, atoms, bonds, pairs, angles, dihedrals, defaults

def TopInfoInput(topInfo, top):
    atomType = topInfo[0]
    moleculeType = topInfo[1]
    atoms = topInfo[2]
    bonds = topInfo[3]
    pairs = topInfo[4]
    angles = topInfo[5]
    dihedrals = topInfo[6]
    defaults = topInfo[7]
    
    top.setDefaults(defaults)
    top.setAtomTypes(atomType)
    top.setMoleculeTypes(moleculeType)
    top.setAtoms(atoms)
    top.setBonds(bonds)
    top.setPairs(pairs)
    top.setAngles(angles)
    top.setDihedrals(dihedrals)
    
    return top
    
def TopInfoExport(top):
    str1 = ' [ system ] \n; name of the system \nsystem \n\n[ molecules ] \n; Compounds\t#mols \nMON\t1\n\n'
    df = top.getDefaults()
    df = df.append(top.getAtomTypes())
    df = df.append(top.getMoleculeTypes())
    df = df.append(top.getAtoms())
    df = df.append(top.getBonds())
    df = df.append(top.getPairs())
    df = df.append(top.getAngles())
    df = df.append(top.getDihedrals())
    
    f = open('tst.top','w')
    for i in range(len(df)):
        line = str(df.iloc[i][0]) + '\n'
        f.write(line)
    f.write(str1)
    f.close()
    


#fileName = 'MON.top'
#topInfo = ReadTop(fileName)
#
#top = Top.TopInfo()
#top1 = TopInfoInput(topInfo, top)
##TopInfoExport(top1)
#
#a = topInfo[2]