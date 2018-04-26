# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:19:02 2018

@author: HuangMing

When generate bonds:
    1. find and delete hydrogens
    2. update bonds/angles/dihedrals section in the top
        - For bonds, need to find which two atom numbers will fill in 
        - For angles, need to find which three atom numbers will fill in 
        - For dihedrals, need to find which four atom numbers will fill in
"""
import pandas as pd
import sys

import readGRO
import readTop
import updateFile

dictBond = {
        'C-N': '1, 0.14647, 272713.120000'
        }

dictAngle = { #TODO: keep update angle coefficient
        'N-C-N': '1, 110.380, 553.9616',
        'C-O-C': '1, 117.600, 522.1632',
        'C-C-N': '1, 111.04005, 552.455360',
        'C-N-C': '1, 112.35005, 534.045760',
        'N-C-C': '1, 111.04005, 552.455360',
        'H-C-N': '1, 109.88005, 414.467040',
        'C-N-H': '1, 109.29005, 396.810560',
        'N-C-H': '1, 109.88005, 414.467040',
        'H-N-C': '1, 109.29005, 396.810560' 
        }

dictDihedral = { #Has little different on the 3 column, some combination is 2 and 3'
        'C-C-O-C': '1, 180.000, 3.766, 2',
        'C-O-C-C': '1, 180.000, 4.602, 2',
        'C-N-C-C': '1, 180.00008, 2.00832, 2',
        'C-C-N-C': '1, 180.00008, 2.00832, 2',
        'H-C-N-C': '1, 0.00000, 1.25520, 3',
        'C-C-C-N': '1, 0.00000, 0.65084, 3',
        'N-C-C-C': '1, 0.00000, 0.65084, 3',
        'N-C-C-O': '1, 0.00000, 0.65084, 3',
        'H-C-N-H': '1, 0.00000, 1.25520, 3',
        'H-N-C-H': '1, 0.00000, 1.25520, 3',
        'C-C-N-H': '1, 0.00000, 1.25520, 3',
        'H-N-C-C': '1, 0.00000, 1.25520, 3',
        'H-C-C-N': '1, 0.00000, 0.65084, 3',
        'N-C-C-H': '1, 0.00000, 0.65084, 3',
        'C-N-C-H': '1, 0.00000, 1.25520, 3',
        'O-C-C-N': '1, 0.00000, 0.65084, 3' 
        }

def ExtraLetterCheck(inString):
    string = ['C', 'N', 'O', 'H']
    return [char for char in inString if char in string]

def list2Str(atom = None, bond = None, pairs = None, angles = None, dihedrals = None,
             Bond = False, Pair = False, Angles = False, Dihedrals = False): #atoms output format
    if Bond:
#        print(bond)
        tmp = '{:>7}{:>7}{:>6}{:>10}{:>14}'.format(
                bond[0], bond[1], bond[2], bond[3], bond[4])
    if Pair:
        tmp = '{:>7}{:>7}{:>6}'.format(
                pairs[0], pairs[1], pairs[2])
        
    if Angles:
        tmp = '{:>7}{:>7}{:>7}{:>6}{:>12}{:>11}'.format(
                angles[0], angles[1], angles[2], angles[3], angles[4], angles[5])
    
    if Dihedrals:
        tmp = '{:>7}{:>7}{:>7}{:>7}{:>6}{:>11}{:>11}{:>3}'.format(
                dihedrals[0], dihedrals[1], dihedrals[2], dihedrals[3], 
                dihedrals[4], dihedrals[5], dihedrals[6], dihedrals[7])
    return tmp

def list2DF(lst, Bond = False, Pairs = False, Angles = False, Dihedrals = False):
    df = pd.DataFrame(index=range(1))
    df.loc[:,0] = ''
    if Bond:
        lst = list2Str(bond = lst, Bond = True)
    elif Pairs:
        lst = list2Str(pairs = lst, Pair = True)
    elif Angles:
        lst = list2Str(angles = lst, Angles = True)
    elif Dihedrals:
        lst = list2Str(dihedrals = lst, Dihedrals = True)
            
    df.loc[0] = lst

    return df

def findHydrogen():
    pass

def delHydrogen():
    pass

def findBondsAtoms():
    pass

def updateTopBonds(idx1, idx2, atomList, ori_top):
    idx1_in = idx1 - 1
    idx2_in = idx2 - 1
    
    atom1 = atomList[idx1_in]
    atom2 = atomList[idx2_in]
    name1 = ''.join(ExtraLetterCheck(atom1.getatomName()))
    name2 = ''.join(ExtraLetterCheck(atom2.getatomName()))
    
    str1 = name1 + '-' + name2
    if str1 in dictBond:
        coeff = dictBond[str1].split(',')
        print('coeff', coeff)
        tmp = [idx1, idx2, coeff[0], coeff[1], coeff[2]]
        df = list2DF(tmp, Bond = True)
        print('df', df)
        top = appendBonds(ori_top, df)
        
        return top
    else:
        print('Bonds atoms: ', str1)
        print('Needs extra information for the bond pair')
        return ori_top

def appendBonds(top, str1):   
    df = top.getBonds()
    df = df.append(str1, ignore_index=True)
    top.setBonds(df)
    return top

def updateTopPairs(idx1, idx2, ori_top):
    tmp = [idx1, idx2, 1]
    df = list2DF(tmp, Pairs = True)
    print('df', df)
    top = appendPairs(ori_top, df)
    return top
    
def appendPairs(top, str1):
    df = top.getPairs()
    df = df.append(str1, ignore_index=True)
    top.setPairs(df)
    return top
    
def findAngleAtoms():
    pass

def updateTopAngles(idx1, idx2, idx3, atomList, ori_top):
    idx1_in = idx1 - 1
    idx2_in = idx2 - 1
    idx3_in = idx3 - 1
    
    atom1 = atomList[idx1_in]
    atom2 = atomList[idx2_in]
    atom3 = atomList[idx3_in]
    name1 = ''.join(ExtraLetterCheck(atom1.getatomName()))
    name2 = ''.join(ExtraLetterCheck(atom2.getatomName()))
    name3 = ''.join(ExtraLetterCheck(atom3.getatomName()))
    
    str1 = name1 + '-' + name2 + '-' + name3
    print(str1)
    if str1 in dictAngle:
        coeff = dictAngle[str1].split(',')
    
        tmp = [idx1, idx2, idx3, coeff[0], coeff[1], coeff[2]]
        df = list2DF(tmp, Angles = True)
        print(df)
        top = appendAngles(ori_top, df)
        print('top length: ', len(top.getAngles()))
        return top
    else:
        print('Angles atoms: ', str1)
        print('Needs extra information for the angles pair')
        return ori_top
    
def appendAngles(top, str1):
    df = top.getAngles()
    df = df.append(str1, ignore_index=True)
    top.setAngles(df)
    
    return top


def updateTopDihedrals(idx1, idx2, idx3, idx4, atomList, ori_top):
    idx1_in = idx1 - 1
    idx2_in = idx2 - 1
    idx3_in = idx3 - 1
    idx4_in = idx4 - 1
    
    atom1 = atomList[idx1_in]
    atom2 = atomList[idx2_in]
    atom3 = atomList[idx3_in]
    atom4 = atomList[idx4_in]
    name1 = ''.join(ExtraLetterCheck(atom1.getatomName()))
    name2 = ''.join(ExtraLetterCheck(atom2.getatomName()))
    name3 = ''.join(ExtraLetterCheck(atom3.getatomName()))
    name4 = ''.join(ExtraLetterCheck(atom4.getatomName()))
    
    str1 = name1 + '-' + name2 + '-' + name3 + '-' + name4
    print(str1)
    if str1 in dictDihedral:
        coeff = dictDihedral[str1].split(',')
    
        tmp = [idx1, idx2, idx3, idx4, coeff[0], coeff[1], coeff[2], coeff[3]]
        str1 = list2DF(tmp, Dihedrals = True)
        print(str1)
        top = appendDihedrals(ori_top, str1)
        return top
    else:
        print('Dih atoms: ', str1)
        print('Needs extra information for the Dih pair')
        return ori_top
    
def appendDihedrals(top, str1):
    df = top.getDihedrals()
    df = df.append(str1, ignore_index=True)
    top.setDihedrals(df)
    
    return top

def findDihedralAtoms():
    pass



#TODO: the coefficient seems not right, when running nvt simulation, always met linc error
fileName1 = 'MON.top'
fileName2 = 'CRO.top'
mon_react = 'MOR'
cro_react = 'COR'
groFile = 'system.gro'

groInfo = readGRO.ReadGro(groFile) #info, atomsList, molList
atomList = groInfo[1]
molList = groInfo[2]
monR_list = [1,47] #local index
monRH_list = [3,48]
croR_list = [1, 38]
croRH_list = [4, 40]

listInfo = updateFile.DelAtomGRO(3, 'MOR', atomList, molList)
listInfo = updateFile.DelAtomGRO(56, 'COR', listInfo[0], listInfo[1])
new_TOP = updateFile.CombineTop(fileName1, fileName2, 'MON', 'CRO', 'MOR', 'COR', listInfo[1])
a = updateTopBonds(1, 53, atomList, new_TOP)

a = updateTopPairs(3, 54, new_TOP)
a = updateTopPairs(4, 54, new_TOP)
a = updateTopPairs(2, 54, new_TOP)
a = updateTopPairs(2, 55, new_TOP)
a = updateTopPairs(3, 55, new_TOP)
a = updateTopPairs(4, 55, new_TOP)
a = updateTopPairs(5, 53, new_TOP)
a = updateTopPairs(7, 53, new_TOP)
a = updateTopPairs(8, 53, new_TOP)
a = updateTopPairs(1, 64, new_TOP)
a = updateTopPairs(1, 56, new_TOP)
a = updateTopPairs(1, 69, new_TOP)

a = updateTopAngles(4, 1, 53, atomList, a)
a = updateTopAngles(3, 1, 53, atomList, a)
a = updateTopAngles(55, 53, 1, atomList, a)
a = updateTopAngles(2, 1, 53, atomList, a)
a = updateTopAngles(1, 53, 54, atomList, a)
#
#a = updateTopDihedrals(54, 53, 1, 2, atomList, a) #angle section seems fine, but dih has extreme different
a = updateTopDihedrals(3, 1, 53, 54, atomList, a)
a = updateTopDihedrals(4, 1, 53, 54, atomList, a)
a = updateTopDihedrals(2, 1, 53, 54, atomList, a)
a = updateTopDihedrals(2, 1, 53, 55, atomList, a)
a = updateTopDihedrals(3, 1, 53, 55, atomList, a)
a = updateTopDihedrals(4, 1, 53, 55, atomList, a)
a = updateTopDihedrals(5, 2, 1, 53, atomList, a)
a = updateTopDihedrals(7, 2, 1, 53, atomList, a)
a = updateTopDihedrals(8, 2, 1, 53, atomList, a)
a = updateTopDihedrals(1, 53, 54, 64, atomList, a)
a = updateTopDihedrals(1, 53, 54, 56, atomList, a)
a = updateTopDihedrals(1, 53, 54, 69, atomList, a)

readTop.TopInfoExport(a)
