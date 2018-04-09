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
        pass
    
    def appendAtoms(self, df): #TODO:
        df_init = self.removeUselessLine('atoms', self.__atoms__)
        init_idx = len(df_init)
        tmp = df_init[0].str.split() #assume the df only contains atoms info, no other info, also index starts from 0
        df = pd.DataFrame(index=range(len(tmp)))
        df.loc[:,'0'] = ''
        
        i = 0
        for atom in tmp:
            atom[0] = int(atom[0]) + init_idx
            atom[5] = int(atom[5]) + init_idx
            atom = self.list2Str(atom, Atom=True)
#            print('atom: ', atom)
            df.loc[i] = atom
#            print(df.iloc[i])
            i += 1
#        print(df)
        df_Tot = self.__atoms__.append(df, ignore_index=True)
        print(df_Tot)
#        print('Length: ', len(df_Tot))
#        self.setAtoms(df_Tot)
        return df_Tot
    
    def list2Str(self, atom, Atom=False):
        if Atom:
            tmp = '{:>5}{:>11}{:>7}{:>7}{:>7}{:>7}{:>11}{:>11}'.format(
                    atom[0], atom[1], atom[2], atom[3], 
                    atom[4], atom[5], atom[6], atom[7])
        
        return tmp
    
    def appendBonds(self, df):
        pass
    
    def appendPairs(self, df):
        pass
    
    def appendAngles(self, df):
        pass
    
    def appendDihedrals(self, df):
        pass
    
    def getAtomTypesList(self):
        df_ori = self.__atomTypes__
        df = self.removeUselessLine('atomtypes', df_ori)
        name = []
        for atomName in df[0].str.split():
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
        df_new = df_new[df_new[0].str.contains(key) == False]
        return df_new
        