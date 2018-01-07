from openpyxl import *
from collections import namedtuple
import random
import sys
import copy
import pickle

## Globals
units = {} # Maps strings to lists of VocabWords

activeWord = False
activeUnit = False
activeDisplayMode = 'character' # Marks which part of the active word should be displayed

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


def getActiveDisplayMode():
    global activeDisplayMode
    return activeDisplayMode

def setDisplayMode(mode):
    global activeDisplayMode
    activeDisplayMode = mode

def setActiveWord(word):
    global activeWord
    activeWord = word

def getActiveWord():
    global activeWord
    return activeWord

def getRandomWord():
    global activeUnit
    return random.choice(activeUnit)

def printActiveWord():
    print(activeWord)

def printActiveUnit():
    print(activeUnit)

def printUnits():
    print(units)
    
## Unit handling
def makeUnitActive(name=None):
    global units, activeUnit, activeWord
    if (name == None):
        activeUnit = list(units.values())[0]
        activeWord = activeUnit[0]
    else:
        activeUnit = units[name]
        activeWord = activeUnit[0]

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
def serialize():
    global units, activeDisplayMode, hardMode, displayMode, firstUse
    state = {'units' : units,
             'activeDisplayMode' : activeDisplayMode,
             'displayMode' : displayMode}
    pickle.dump(state, open("state.cm", "wb"))
    
def deserialize():
    return pickle.load(open("state.cm", "rb"))

def setUnits(serializedUnits):
    global units
    units = copy.deepcopy(serializedUnits)
