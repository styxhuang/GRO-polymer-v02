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
import readGRO

def findHydrogen():
    pass

def delHydron():
    pass

def findBondsAtoms():
    pass

def findAngleAtoms():
    pass

def findDihedralAtoms():
    pass



groFile = 'system.gro'
groInfo = readGRO.ReadGro(groFile) #info, atomsList, molList

monR_list = [1,47]
monRH_list = [3,48]
croR_list = [54, 91]
monRH_list = [57, 93]
