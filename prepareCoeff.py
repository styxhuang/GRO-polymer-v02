# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 12:24:03 2018

@author: HuangMing
"""

import subprocess
import parmed

GMX = 'gmx'

def PrepareFile(fileName, resName, outputName):
    command1 = 'antechamber -fi mol2 -fo mol2 -c bcc -at gaff -rn {} -i {} -o out.mol2 -pf Y'.format(resName, fileName)
    command2 = 'parmchk2 -i out.mol2 -o out.frcmod -f mol2 -s gaff'
    command3 = 'tleap -f tleap.in'
    
    str1 = 'source leaprc.gaff \nSUS = loadmol2 out.mol2 \ncheck SUS\nloadamberparams out.frcmod \nsaveamberparm SUS out.top out.crd \nquit'
    f = open('tleap.in', 'w')
    f.write(str1)
    f.close()   
    
    subprocess.call(command1, shell=True)
    subprocess.call(command2, shell=True)
    subprocess.call(command3, shell=True)
    
    file = parmed.load_file('out.top', xyz='out.crd')
    file.save('{}.gro'.format(outputName))
    file.save('{}.top'.format(outputName))
    
    #If everything goes right, can delete all the unrelevent files in this step, 
    #and just keep gro & top files
    
def ExtendSys(mon, monNum, cro, croNum, boxSize):
    command1 = '{} insert-molecules -ci {}.gro -nmol {} -o system.gro -box {} {} {}'.format(
            GMX, mon, monNum, boxSize, boxSize, boxSize)
    command2 = '{} insert-molecules -f system.gro -ci {}.gro -nmol {} -o system.gro'.format(
            GMX, cro, croNum)
    
    subprocess.call(command1, shell=True)
    subprocess.call(command2, shell=True)
    
###############################################################################
# Test
#######
monFile = 'DGEBA.mol2'
resMon = 'MON'
numMon = 1
croFile = 'PACM.mol2'
resCro = 'CRO'
numCro = 1
boxSize = 5

PrepareFile(monFile, resMon, resMon)
PrepareFile(croFile, resCro, resCro)

ExtendSys(resMon, numMon, resCro, numCro, boxSize)


