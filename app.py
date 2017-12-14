"""
Workflow:
Create a new unit
Load character data from CSV, XLSX, whatever
Save unit
Select unit to practice
Spam notecards until done.

Features:
"""

from tkinter import *
from tkinter import filedialog
from collections import namedtuple
from openpyxl import *
import random

# Data containers
VocabWord = namedtuple('VocabWord', ['character', 'pinyin', 'definition'])
testWord = VocabWord(character='我', pinyin="wo", definition="I");


def unitFromXLSX(path):
    vocab = []
    testUnit = load_workbook(path, read_only=True)
    sheet = testUnit['Sheet1']
    for row in sheet:
        newWord = VocabWord(character=row[0].value,
                            pinyin=row[1].value,
                            definition=row[2].value)
        vocab.append(newWord)
        
    return vocab

if __name__ == "__main__":
    # UI definitions
    root = Tk()
    root.title("Chinese!")
    frame = Frame(root, width=160, height=100)

    vocab = []
    global activeWord
    
    # Definitions for each button
    notecardButton = Button(frame, text="Click to choose a unit!")
    def showPinyin(event):
        notecardButton["text"] = activeWord.pinyin

    def showDef(event):
        notecardButton["text"] = activeWord.definition
        
    def onMainButtonStartupClick():
        global vocab, activeWord
        root.withdraw()
        path = filedialog.askopenfilename()
        root.deiconify()
        
        vocab = unitFromXLSX(path)
        activeWord = vocab[0]
        notecardButton["text"] = activeWord.character
        notecardButton["command"] = showDef
        
    notecardButton["command"] = onMainButtonStartupClick
    notecardButton.pack()
    
    def nextWord(event):
        global activeWord
        activeWord = random.choice(vocab)
        print(activeWord)
        notecardButton["text"] = activeWord.character
    
    root.bind("n", nextWord)
    root.bind("p", showPinyin)
    root.bind("d", showDef)
    frame.pack()
    root.mainloop()

    


