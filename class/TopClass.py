# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 13:17:58 2018

@author: HuangMing
"""

import pandas as pd

class TopInfo(object):
    def __init__(self):
        self.__defaults__ = pd.DataFrame()
        self.__atomTypes__ = pd.DataFrame()
        self.__moleculeType__ = pd.DataFrame()
        self.__atoms__ = pd.DataFrame()
        self.__bonds__ = pd.DataFrame()
        self.__pairs__ = pd.DataFrame()
        self.__angles__ = pd.DataFrame()
        self.__dihedrals__ = pd.DataFrame()
    
    def setDefaults(self, df):
        self.__defaults__ = df
        
    def setAtomTypes(self, df):
        self.__atomTypes__ = df

    def setMoleculeTypes(self, df):
        self.__moleculeType__ = df
    
    def setAtoms(self, df):
        self.__atoms__ = df
        
    def setBonds(self, df):
        self.__bonds__ = df
        
    def setPairs(self, df):
        self.__pairs__ = df
        
    def setAngles(self, df):
        self.__angles__ = df
        
    def setDihedrals(self, df):
        self.__dihedrals__ = df
    
    
    def getDefaults(self):
        return self.__defaults__
    
    def getAtomTypes(self):
        return self.__atomTypes__
    
    def getMoleculeTypes(self):
        return self.__moleculeType__
    
    def getAtoms(self):
        return self.__atoms__
    
    def getBonds(self):
        return self.__bonds__
    
    def getPairs(self):
        return self.__pairs__
    
    def getAngles(self):
        return self.__angles__
    
    def getDihedrals(self):
        return self.__dihedrals__
    
    def appendAtomTypes(self, df):
        ori_types = self.getAtomTypesList(self.__atomTypes__)
        input_types = self.getAtomTypesList(df)
        tmp = pd.DataFrame(index=range(1))
        tmp.loc[:,0] = ''
        
        new_item = [ i for i in input_types if i not in ori_types]
        append_item = []
        if len(new_item) > 1:
            df = self.removeUselessLine('atomtypes', df)
            for item in new_item:
                content = df[df[0].str.contains(item)][0].iloc[0]
                print(len(content))
                append_item.append(content)
            
            i = 0
            for item in append_item:
                tmp.loc[i] = item
                i += 1
            df_ori = self.removeUselessLine('dump',self.__atomTypes__)
            df_Tot = df_ori.append(tmp, ignore_index=True)
    
            self.setAtomTypes(df_Tot)
        
    def list2Str(self, atom = None, bond = None, pairs = None, angles = None, dihedrals = None,
                 Atom=False, Bond = False, Pairs = False, Angles = False, Dihedrals = False): #atoms output format
        if Atom:
            tmp = '{:>5}{:>11}{:>7}{:>7}{:>7}{:>7}{:>11}{:>11}'.format(
                    atom[0], atom[1], atom[2], atom[3], 
                    atom[4], atom[5], atom[6], atom[7])
        if Bond:
            tmp = '{:>7}{:>7}{:>6}{:>10}{:>14}'.format(
                    bond[0], bond[1], bond[2], bond[3], bond[4])
        
        if Pairs:
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
    
    def appendAtoms(self, df_new):
        df_ori = self.removeUselessLine('atoms', self.__atoms__)
        df_new = self.removeUselessLine('atoms', df_new)
        init_idx = len(df_ori)
        tmp = df_new[0].str.split() #assume the df only contains atoms info, no other info, also index starts from 0
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,0] = ''
        
        i = 0
        for atom in tmp:
            atom[0] = int(atom[0]) + init_idx
            atom[5] = int(atom[5]) + init_idx
            atom = self.list2Str(atom = atom, Atom = True)
            df.loc[i] = atom
            i += 1
        df_Tot = self.__atoms__.append(df, ignore_index=True)

        self.setAtoms(df_Tot)
        return init_idx
    
    def appendBonds(self, init_idx, df):
        df_new = self.removeUselessLine('bonds', df)
        tmp = df_new[0].str.split()    
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,0] = ''
        
        i = 0 
        for bond in tmp:
            bond[0] = int(bond[0]) + init_idx
            bond[1] = int(bond[1]) + init_idx
            bond = self.list2Str(bond = bond, Bond = True)
            df.loc[i] = bond
            i += 1
        df_Tot = self.__bonds__.append(df, ignore_index=True)
        self.setBonds(df_Tot)
        
    def appendPairs(self, init_idx, df):
        df_new = self.removeUselessLine('pairs', df)
        tmp = df_new[0].str.split()    
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,0] = ''
        
        i = 0 
        for pairs in tmp:
            pairs[0] = int(pairs[0]) + init_idx
            pairs[1] = int(pairs[1]) + init_idx
            pairs = self.list2Str(pairs = pairs, Pairs = True)
            df.loc[i] = pairs
            i += 1
        df_Tot = self.__pairs__.append(df, ignore_index=True)
        self.setPairs(df_Tot)
    
    def appendAngles(self, init_idx, df):
        df_new = self.removeUselessLine('angles', df)
        tmp = df_new[0].str.split()    
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,0] = ''
        
        i = 0 
        for angles in tmp:
            angles[0] = int(angles[0]) + init_idx
            angles[1] = int(angles[1]) + init_idx
            angles[2] = int(angles[2]) + init_idx
            
            angles = self.list2Str(angles = angles, Angles = True)
            df.loc[i] = angles
            i += 1
        df_Tot = self.__angles__.append(df, ignore_index=True)
        self.setAngles(df_Tot)
    
    def appendDihedrals(self, init_idx, df):
        df_new = self.removeUselessLine('dihedrals', df)
        tmp = df_new[0].str.split()    
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,0] = ''
        
        i = 0 
        for dihedrals in tmp:
            dihedrals[0] = int(dihedrals[0]) + init_idx
            dihedrals[1] = int(dihedrals[1]) + init_idx
            dihedrals[2] = int(dihedrals[2]) + init_idx
            dihedrals[3] = int(dihedrals[3]) + init_idx
            dihedrals = self.list2Str(dihedrals = dihedrals, Dihedrals = True)
            df.loc[i] = dihedrals
            i += 1
        df_Tot = self.__dihedrals__.append(df, ignore_index=True)
        self.setDihedrals(df_Tot)
    
    def getAtomTypesList(self, df):
        df_ori = df
        tmp = self.removeUselessLine('atomtypes', df_ori)
        name = []
        for atomName in tmp[0].str.split():
            if len(atomName) < 1:
                continue
            else:
                name.append(atomName[0])
        return name
    
    def getAtomsName(self):
        name = []
        df_ori = self.__atoms__
        df = self.removeUselessLine('atoms', df_ori)
        for atom in df[0].str.split():
            name.append(atom[1])
        return name
        
    def removeUselessLine(self, key, df):
        df_ori = df
        df_new = df_ori[df_ori[0].str[0] != ';']
        df_new = df_new[df_new[0].str.contains(key) == False].reset_index(drop=True)
        return df_new
        