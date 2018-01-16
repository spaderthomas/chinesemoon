from openpyxl import *
from collections import namedtuple
import random
import sys
import copy
import pickle
import os

## Globals
units = {} # Maps strings to lists of VocabWords

activeWord = False
activeUnits = False

hardModeCutoff = .66

## Data containers
class Struct: 
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

''' 
string character;
string pinyin;
string definition;
int accessed;
int correct;
'''
class VocabWord(Struct):
    def __str__(self):
        if (self.accessed == 0):
            ratio = 0
        else:
            ratio = float(self.correct) / self.accessed
                
        return('character = ' + self.character + ","
               + 'pinyin = ' + self.pinyin + ","
               + 'definition = ' + self.definition + ","
               + 'ratio = ' + str(ratio))

# Getters and setters
def getActiveWord():
    global activeWord
    return activeWord

def getUnits():
    global units
    return units

def getActiveUnits():
    global activeUnits
    return activeUnits

# Note: This is actually a bad random function, because it favors words in smaller units
# But it's good enough for our purposes
def getRandomWord():
    global activeUnits
    randKey = random.choice(list(activeUnits.keys()))
    return random.choice(activeUnits[randKey])

def setDisplayMode(mode):
    global activeDisplayMode
    activeDisplayMode = mode

def setActiveWord(word):
    global activeWord
    activeWord = word

def resetActiveWordStats():
    global activeWord
    activeWord.accessed = 0
    activeWord.correct = 0

    
## Unit handling
# Clears out active units and sets unit denoted by name to be active
def makeUnitActive(name=None):
    global units, activeUnits, activeWord

    # Case where we just want to set first unit to active (init from file, delete active unit)
    if (name == None): 
        if (len(units)):
            name = list(units.keys())[0]
            activeUnits = {name : list(units.values())[0]}
            activeWord = activeUnits[name][0]
        else:
            activeUnits = False
            activeWord = False
    else:
        activeUnits = {name : units[name]}
        activeWord = activeUnits[name][0]

def addUnitToActive(name):
    global units, activeUnits
    activeUnits[name] = units[name]

def delUnitFromActive(name):
    global activeUnits
    if name in activeUnits:
      del activeUnits[name]
    
def addUnit(unitName, newUnit):
    global units, activeUnit
    units[unitName] = newUnit;

def delUnit(name):
    global units
    del units[name]
    
def unitFromXLSX(path):
    global units
    vocab = []
    unit = load_workbook(path, read_only=True)
    sheet = unit['Sheet1']
    for row in sheet:
        newWord = VocabWord(character=row[0].value,
                            pinyin=row[1].value,
                            definition=row[2].value,
                            accessed=0,
                            correct=0)
        vocab.append(newWord)
        
    return vocab


## Marking
def markIncorrect(word):
    word.accessed += 1
    
def markCorrect(word):
    word.accessed += 1
    word.correct += 1

            
## Persistence functions
def serializeController():
    global units, activeDisplayMode
    state = {'units' : units}
    pickle.dump(state, open("state.cm", "wb"))
    
def deserializeController():
    curDir = os.path.dirname(__file__)
    path = os.path.join(curDir, 'state.cm')
    return pickle.load(open(path, "rb"))

def loadUnits(serializedUnits):
    global units
    units = copy.deepcopy(serializedUnits)
