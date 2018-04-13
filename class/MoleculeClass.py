# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 12:53:50 2018

@author: huang
"""

class MoleculeInfo(object):
    def __init__(self):
        self.__index__ = 0
        self.__name__ = ""
        self.__atoms__ = []
        
    def setIndex(self, index):
        self.__index__ = index
    
    def setName(self, name):
        self.__name__ = name
        
    def setAtoms(self, atom):
        self.__atoms__.append(atom)
        
    def getIndex(self):
        return self.__index__
    
    def getName(self):
        return self.__name__
    
    def getAtoms(self):
        return self.__atoms__
    
    def getAtomsName(self):
        name = []
        for atom in self.__atoms__:
            name.append(atom.getatomName())
        return name

    def delAtoms(self, index, rename):
        atoms = self.getAtoms()
#        print(len(atoms))
        del atoms[index]
#        print('atoms_new', len(atoms))
        self.__atoms__ = []
        i = 0
        for atom in atoms:
#            print('rename', rename)
            atom.setmolName(rename)
            atom.setlocalIndex(i)
            self.setAtoms(atom)
            i += 1
            
    def outputInfo(self):
        print("Index: ", self.__index__, "\tName: ", self.__name__, "\t", len(self.__atoms__))
        for i in range (len(self.__atoms__)):
            molName = self.__atoms__[i].getmolName()
            index = self.__atoms__[i].getglobalIndex()
            name = self.__atoms__[i].getatomName()
            print(index, "\t", molName, '\t', name)
            
            